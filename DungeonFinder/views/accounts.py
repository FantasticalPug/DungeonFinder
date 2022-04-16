"""DungeonFinder Account Management."""
import hashlib
import uuid
import flask
import datetime
import pathlib
import DungeonFinder

@DungeonFinder.app.route('/accounts/login/')
def show_login():
    """Display the login page."""
    logname = check_session()
    if logname != False:
        return flask.redirect('/')
    context = {
        "logname": "Login",
        "page": "Log In"
    }
    return flask.render_template("login.html", **context)

@DungeonFinder.app.route('/accounts/create/')
def show_create():
    """Display the create account page."""
    logname = check_session()
    if logname != False:
        return flask.redirect('/')
    context = {
        "logname": "Login",
        "page": "Sign Up"
    }
    return flask.render_template("create.html", **context)

@DungeonFinder.app.route('/accounts/delete/')
def show_delete():
    """Display the delete account confirmation page."""
    logname = check_session()
    if logname == False:
        return flask.redirect('/accounts/login/')
    context = {
        "logname": logname,
        "page": "Delete Account"
    }
    return flask.render_template("delete.html", **context)

@DungeonFinder.app.route('/accounts/edit/')
def show_edit():
    """Display the edit account page."""
    logname = check_session()
    if logname == False:
        return flask.redirect('/accounts/login/')
    context = {
        "logname": logname,
        "page": "Edit Account"
    }
    return flask.render_template("edit.html", **context)

@DungeonFinder.app.route('/accounts/password/')
def show_update_password():
    """Display the update password page."""
    logname = check_session()
    if logname == False:
        return flask.redirect('/accounts/login/')
    context = {
        "logname": logname,
        "page": "Change Password"
    }
    return flask.render_template("password.html", **context)

def hash_password(password, salt):
    """Hash the password with the sha512 algorithm."""
    algorithm = "sha512"
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    return "$".join([algorithm, salt, password_hash])

def check_session():
    """Check for existing session."""
    if flask.session.get('username', False) == False:
        return False
    return flask.session.get('username')

def save_file(filename, fileobj):
    """Save uploaded user files."""
    stem = uuid.uuid4().hex
    suffix = pathlib.Path(filename).suffix
    uuid_basename = f"{stem}{suffix}"
    path = DungeonFinder.app.config["UPLOAD_FOLDER"]/uuid_basename
    fileobj.save(path)
    return uuid_basename


def create(username, password, email, dob):
    """Create a new user account."""
    connection = DungeonFinder.model.get_db()
    cur = connection.execute(
        "SELECT * FROM users WHERE username = ?",
        (username, )
    )
    data = cur.fetchall()
    if len(data) > 0:
        return 409
    salt = uuid.uuid4().hex
    hashed_password = hash_password(password, salt)
    today = datetime.date.today()
    birth = datetime.datetime.strptime(dob, '%Y-%m-%d')
    age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
    cur = connection.execute(
        "INSERT INTO users(username, password, email, age, favorites, bio, exper, discord, filename) "
        "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (username, hashed_password, email, age, "", "", "", "", "", )
    )
    flask.session['username'] = username

def login(username, password):
    """Log the user in."""
    connection = DungeonFinder.model.get_db()
    cur = connection.execute(
        "SELECT * FROM users WHERE username = ?",
        (username, )
    )
    data = cur.fetchall()
    if len(data) != 1:
        return 401
    actual_password = data[0]['password']
    salt = actual_password.split('$')[1]
    hashed_password = hash_password(password, salt)
    if hashed_password == actual_password:
        flask.session['username'] = username

@DungeonFinder.app.route('/accounts/logout/')
def logout():
    """Log the user out."""
    flask.session.pop('username')
    return flask.redirect('/accounts/login/')

@DungeonFinder.app.route('/accounts/', methods=['POST'])
def manage_account():
    """Manage user account."""
    operation = flask.request.form['operation']
    if operation == "login":
        username = flask.request.form['username']
        password = flask.request.form['password']
        if login(username, password) == 401:
            message = "Based on our Insight Check, we suspect your username or password was incorrect!"
            return flask.redirect(f"/error/?code=401&message={message}")
    elif operation == "create":
        username = flask.request.form['username']
        password = flask.request.form['password']
        email = flask.request.form['email']
        dob = flask.request.form['dob']
        if create(username, password, email, dob) == 409:
            message = "Uh-Oh! Our Rogue rolled Investigation and discovered that username already exists! Please use a different username!"
            return flask.redirect(f"/error/?code=409&message={message}")
    elif operation == "delete":
        connection = DungeonFinder.model.get_db()
        connection.execute(
            "DELETE FROM users WHERE username = ?",
            (flask.session['username'], )
        )
        flask.session.pop('username')
    elif operation == "edit":
        connection = DungeonFinder.model.get_db()
        email = flask.request.form['email']
        connection.execute(
            "UPDATE users SET email = ? WHERE username = ?",
            (email, flask.session['username'], )
        )
    elif operation == "password":
        connection = DungeonFinder.model.get_db()
        old_password = flask.request.form['old-password']
        new_password = flask.request.form['new-password']
        cur = connection.execute(
            "SELECT * FROM users WHERE username = ?",
            (flask.session['username'], )
        )
        data = cur.fetchall()
        if len(data) != 1:
            message = "Our Rogue rolled a Nat 1 on Investigation and couldn't find your account! Make sure you are logged in and have an account with DungeonFinder!"
            return flask.redirect(f"/error/?code=400&message={message}")
        actual_password = data[0]['password']
        salt = actual_password.split('$')[1]
        hashed_password = hash_password(old_password, salt)
        if hashed_password != actual_password:
            message = "You rolled a Nat 1 on your Persuasion check as you entered an incorrect OLD password!"
            return flask.redirect(f"/error/?code=403&message={message}")
        salt = uuid.uuid4().hex
        hashed_password = hash_password(new_password, salt)
        cur = connection.execute(
            "UPDATE users SET password = ? WHERE username = ?",
            (hashed_password, flask.session['username'], )
        )
    target = flask.request.args['target']
    return flask.redirect(target)
