"""DungeonFinder User Views."""
import flask
import os
import DungeonFinder
from DungeonFinder.views.accounts import check_session, save_file

@DungeonFinder.app.route('/users/<path:user>/')
def show_user(user):
    """Show game details page."""
    logname = check_session()
    if logname == False:
        return flask.redirect('/accounts/login/')
    connection = DungeonFinder.model.get_db()
    cur = connection.execute(
        "SELECT * FROM users WHERE username = ?",
        (user, )
    )
    data = cur.fetchall()
    if len(data) == 0:
        message = "Our Rogue rolled a Nat 1 on Investigation and was unable to find the Adventurer you seek! Perhaps they've been vanquished the the Hordes..."
        return flask.redirect(f"/error/?code=404&message={message}")
    data = data[0]
    cur = connection.execute(
        "SELECT * FROM games WHERE owner = ?",
        (logname, )
    )
    running = cur.fetchall()
    cur = connection.execute(
        "SELECT * FROM sessions WHERE player = ? AND status = ?",
        (logname, "Joined", )
    )
    joined = cur.fetchall()
    for game in joined:
        cur = connection.execute(
            "SELECT * FROM games WHERE gameid = ?",
            (game['gameid'], )
        )
        game['name'] = cur.fetchall()[0]['name']
    context = {
        "logname": logname,
        "user": data,
        "running": running,
        "joined": joined,
        "page": data['username']
    }
    return flask.render_template("user.html", **context)

@DungeonFinder.app.route('/users/edit/')
def show_edit_profile():
    """Show page to edit a user profile."""
    logname = check_session()
    if logname == False:
        return flask.redirect('/accounts/login/')
    connection = DungeonFinder.model.get_db()
    cur = connection.execute(
       "SELECT * FROM users WHERE username = ?",
       (logname, )
    )
    data = cur.fetchall()[0]
    context = {
        "logname": logname,
        "user": data,
        "page": "Edit Profile"
    }
    return flask.render_template("profile.html", **context)

@DungeonFinder.app.route('/users/edit/update/', methods=["POST"])
def edit_profile():
    """Update the user profile information."""
    logname = check_session()
    if logname == False:
        return flask.redirect('/accounts/login/')
    connection = DungeonFinder.model.get_db()
    cur = connection.execute(
        "SELECT * FROM users WHERE username = ?",
        (logname, )
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
    exper = flask.request.form['experience']
    favorites = flask.request.form['favorite']
    bio = flask.request.form['bio']
    connection.execute(
        "UPDATE users SET filename = ?, exper = ?, favorites = ?, bio = ? WHERE username = ?",
        (filename, exper, favorites, bio, logname, )
    )
    return flask.redirect(f"/users/{logname}/")
