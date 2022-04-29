"""DungeonFinder Games Views."""
import flask
import os
import DungeonFinder
from DungeonFinder.views.accounts import check_session, save_file

@DungeonFinder.app.route('/games/create/')
def show_create_game():
    """Display the page for users to create a game post."""
    logname = check_session()
    if logname == False:
        return flask.redirect('/accounts/login/')
    context = {
        "logname": logname,
        "page": "Create Game"
    }
    return flask.render_template("post.html", **context)

@DungeonFinder.app.route('/games/<path:gameid>/')
def show_game(gameid):
    """Show game details page."""
    logname = check_session()
    if logname == False:
        return flask.redirect('/accounts/login/')
    connection = DungeonFinder.model.get_db()
    cur = connection.execute(
        "SELECT * FROM games WHERE gameid = ?",
        (gameid, )
    )
    data = cur.fetchall()
    if len(data) == 0:
        message = "Our Rogue rolled a Nat 1 on his Investigation Check and was unable to find the game you're looking for! Perhaps the owner deleted it..."
        return flask.redirect(f"/error/?code=404&message={message}")
    data = data[0]
    cur = connection.execute(
        "SELECT * FROM sessions WHERE gameid = ? AND status = ?",
        (gameid, "Joined", )
    )
    players = cur.fetchall()
    data['joined'] = players
    data['players'] = len(players)
    cur = connection.execute(
        "SELECT * FROM sessions WHERE gameid = ? AND player = ?",
        (gameid, logname, )
    )
    data2 = cur.fetchall()
    logname_joined = len(data2) == 1
    status = "None"
    if len(data2) == 1:
        status = data2[0]['status']
    cur = connection.execute(
        f"SELECT * FROM responses_{gameid}"
    )
    applications = len(cur.fetchall())
    context = {
        "logname": logname,
        "game": data,
        "joined": logname_joined,
        "status": status,
        "page": data['name'],
        "applications": applications
    }
    return flask.render_template("game.html", **context)

@DungeonFinder.app.route('/games/post/', methods=['POST'])
def post_game():
    """Add a new game to the database."""
    logname = check_session()
    if logname == False:
        return flask.redirect('/accounts/login/')
    campaign = flask.request.form['campaign']
    system = flask.request.form['system']
    days = flask.request.form.getlist('day[]')
    begin = flask.request.form['begin']
    end = flask.request.form['end']
    frequency = flask.request.form['frequency']
    exper = flask.request.form.getlist('exp[]')
    apply = flask.request.form.get('apply', 0)
    if apply == "Y":
        apply = 1
    exper_helper = ""
    if len(exper) == 4:
        exper = "All Are Welcome!"
    else:
        for exp in exper:
            if len(exper_helper) == 0:
                exper_helper = f"{exp}"
            else:
                exper_helper = f"{exper_helper}, {exp}"
        exper = exper_helper
    avail = ""
    if len(days) == 7:
        days = "Anyday"
    else:
        days_helper = ""
        for day in days:
            if len(days_helper) == 0:
                days_helper = f"{day}"
            else:
                days_helper = f"{days_helper}, {day}"
        days = days_helper
    begin_time = begin.split(':')
    hour = int(begin_time[0])
    ante = 'AM'
    if hour >= 12:
        ante = 'PM'
    hour = hour % 12
    if hour == 0:
        hour = '12'
    begin = f"{hour}:{begin_time[1]} {ante}"
    end_time = end.split(':')
    hour = int(end_time[0])
    ante = 'AM'
    if hour >= 12:
        ante = 'PM'
    hour = hour % 12
    if hour == 0:
        hour = '12'
    end = f"{hour}:{end_time[1]} {ante}"
    avail = f"{days} from {begin} until {end}"
    connection = DungeonFinder.model.get_db()
    fileobj = flask.request.files["profile"]
    filename = fileobj.filename
    if filename != "":
        filename = save_file(filename, fileobj)
    tags = flask.request.form['tags']
    description = flask.request.form['description']
    slots = flask.request.form['slots']
    cur = connection.execute(
        "INSERT INTO games(owner, name, system, tags, description, slots, exper, avail, frequency, filename, must_apply) "
        "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (logname, campaign, system, tags, description, slots, exper, avail, frequency, filename, apply, )
    )
    cur = connection.execute(
        "SELECT last_insert_rowid() FROM games"
    )
    game = cur.fetchall()[0]['last_insert_rowid()']
    cur = connection.execute(
        "SELECT * FROM games WHERE gameid = ?",
        (game, )
    )
    game = cur.fetchall()[0]
    gameid = game['gameid']
    if apply == 1:
        cur = connection.execute(
            f"CREATE TABLE apply_{gameid} ("
            "questionid INTEGER PRIMARY KEY AUTOINCREMENT,"
            "question TEXT NOT NULL"
            ");"
        )
        cur = connection.execute(
            f"CREATE TABLE responses_{gameid}("
            "answerid INTEGER PRIMARY KEY AUTOINCREMENT,"
            "answer TEXT NOT NULL,"
            "questionid int NOT NULL,"
            "player VARCHAR(30) NOT NULL,"
            f"FOREIGN KEY(questionid) REFERENCES apply_{gameid}(questionid) ON DELETE CASCADE"
            ");"
        )
        return flask.redirect(f"/games/{gameid}/apply/create/")
    return flask.redirect(f'/games/{gameid}/')

@DungeonFinder.app.route('/games/edit/')
def show_game_edit():
    """Show the page for editing an existing game."""
    logname = check_session()
    if logname == False:
        return flask.redirect('/accounts/login/')
    connection = DungeonFinder.model.get_db()
    gameid = flask.request.args['gameid']
    cur = connection.execute(
        "SELECT * FROM games WHERE gameid = ?",
        (gameid, )
    )
    game = cur.fetchall()[0]
    if game['owner'] != logname:
        message = "You rolled a Nat 1 on your Deception Check! Make sure you are the owner of a campaign before attempting to edit it! Manipulating campaigns you do not own is a violation of our Terms of Service!"
        return flask.redirect(f"/error/?code=403&message={message}")
    context = {
        "logname": logname,
        "game": game,
        "page": f"Update {game['name']}"
    }
    return flask.render_template("update.html", **context)

@DungeonFinder.app.route('/games/update/', methods=['POST'])
def edit_game():
    """Update the game information."""
    logname = check_session()
    if logname == False:
        return flask.redirect('/accounts/login/')
    connection = DungeonFinder.model.get_db()
    gameid = flask.request.form['gameid']
    cur = connection.execute(
        "SELECT * FROM games WHERE gameid = ? AND owner = ?",
        (gameid, logname, )
    )
    data = cur.fetchall()
    if len(data) != 1:
        message = "You rolled a Nat 1 on your Deception Check! Make sure you are the owner of a campaign before attempting to edit it! Manipulating campaigns you do not own is a violation of our Terms of Service!"
        return flask.redirect(f"/error/?code=403&message={message}")
    campaign = flask.request.form['campaign']
    system = flask.request.form['system']
    days = flask.request.form.getlist('day[]')
    begin = flask.request.form['begin']
    end = flask.request.form['end']
    frequency = flask.request.form['frequency']
    exper = flask.request.form.getlist('exp[]')
    apply = flask.request.form.get('apply', 0)
    old_apply = data[0]['must_apply']
    if apply == "Y":
        apply = 1
    exper_helper = ""
    if len(exper) == 4:
        exper = "All Are Welcome!"
    else:
        for exp in exper:
            if len(exper_helper) == 0:
                exper_helper = f"{exp}"
            else:
                exper_helper = f"{exper_helper}, {exp}"
        exper = exper_helper
    avail = ""
    if len(days) == 7:
        days = "Anyday"
    else:
        days_helper = ""
        for day in days:
            if len(days_helper) == 0:
                days_helper = f"{day}"
            else:
                days_helper = f"{days_helper}, {day}"
        days = days_helper
    begin_time = begin.split(':')
    hour = int(begin_time[0])
    ante = 'AM'
    if hour >= 12:
        ante = 'PM'
    hour = hour % 12
    if hour == 0:
        hour = '12'
    begin = f"{hour}:{begin_time[1]} {ante}"
    end_time = end.split(':')
    hour = int(end_time[0])
    ante = 'AM'
    if hour >= 12:
        ante = 'PM'
    hour = hour % 12
    if hour == 0:
        hour = '12'
    end = f"{hour}:{end_time[1]} {ante}"
    avail = f"{days} from {begin} until {end}"
    cur = connection.execute(
        "SELECT * FROM games WHERE gameid = ?",
        (gameid, )
    )
    oldfilename = cur.fetchall()[0]['filename']
    fileobj = flask.request.files["profile"]
    filename = fileobj.filename
    if oldfilename != "" and filename != "":
        os.remove(os.path.join(DungeonFinder.app.config['UPLOAD_FOLDER'], oldfilename))
    if filename != "":
        filename = save_file(filename, fileobj)
    else:
        cur = connection.execute(
            "SELECT * FROM users WHERE username = ?",
            (logname, )
        )
        filename = cur.fetchall()[0]['filename']
    tags = flask.request.form['tags']
    description = flask.request.form['description']
    slots = flask.request.form['slots']
    cur = connection.execute(
        "UPDATE games SET owner = ?, name = ?, system = ?, tags = ?, description = ?, slots = ?, avail = ?, frequency = ?, exper = ?, filename = ?, must_apply = ? WHERE gameid = ?",
        (logname, campaign, system, tags, description, slots, avail, frequency, exper, filename, apply, gameid, )
    )
    cur = connection.execute(
        "SELECT * FROM games WHERE gameid = ?",
        (gameid, )
    )
    gameid = cur.fetchall()[0]['gameid']
    if old_apply == 0 and apply == 1:
        cur = connection.execute(
            f"CREATE TABLE apply_{gameid} ("
            "questionid INTEGER PRIMARY KEY AUTOINCREMENT,"
            "question TEXT NOT NULL"
            ");"
        )
        cur = connection.execute(
            f"CREATE TABLE responses_{gameid}("
            "answerid INTEGER PRIMARY KEY AUTOINCREMENT,"
            "answer TEXT NOT NULL,"
            "questionid int NOT NULL,"
            "player VARCHAR(30) NOT NULL,"
            f"FOREIGN KEY(questionid) REFERENCES apply_{gameid}(questionid) ON DELETE CASCADE"
            ");"
        )
        return flask.redirect(f'/games/{gameid}/apply/create/')
    if old_apply == 1 and apply == 0:
        cur = connection.execute(
            f"DROP TABLE apply_{gameid}"
        )
        cur = connection.execute(
            f"DROP TABLE responses_{gameid}"
        )
    return flask.redirect(f'/games/{gameid}/')

@DungeonFinder.app.route('/games/delete/', methods=['POST'])
def delete_game():
    """Delete a game from the database."""
    logname = check_session()
    if logname == False:
        return flask.redirect('/accounts/login/')
    gameid = flask.request.form['gameid']
    connection = DungeonFinder.model.get_db()
    cur = connection.execute(
        "SELECT * FROM games WHERE owner = ? AND gameid = ?",
        (logname, gameid, )
    )
    if len(cur.fetchall()) != 1:
        message = "You rolled a Nat 1 on your Deception Check! Make sure you are the owner of a campaign before attempting to edit it! Manipulating campaigns you do not own is a violation of our Terms of Service!"
        return flask.redirect(f"/error/?code=403&message={message}")
    cur = connection.execute(
        "DELETE FROM games WHERE gameid = ?",
        (gameid, )
    )
    return flask.redirect(f'/users/{logname}/')

@DungeonFinder.app.route('/games/<path:gameid>/apply/create/')
def show_create_application(gameid):
    """Create an application to join the game."""
    logname = check_session()
    if logname == False:
        return flask.redirect('/accounts/login/')
    connection = DungeonFinder.model.get_db()
    cur = connection.execute(
        "SELECT * FROM games WHERE gameid = ?",
        (gameid, )
    )
    game = cur.fetchall()[0]
    context = {
        "logname": logname,
        "game": game,
        "page": "Create Application"
    }
    return flask.render_template("form.html", **context)
