"""REST API for User Functions."""
import flask
import DungeonFinder
from DungeonFinder.views.accounts import check_session

@DungeonFinder.app.route('/api/v1/users/unlink/', methods=["POST"])
def unlink_discord():
    """Unlink Discord from DungeonFinder."""
    logname = check_session()
    if logname == False:
        return flask.redirect('/accounts/login/')
    connection = DungeonFinder.model.get_db()
    connection.execute(
        "UPDATE users SET discord = ? WHERE username = ?",
        ("", logname, )
    )
    context = {
        "user": logname,
        "discord": ""
    }
    return flask.jsonify(**context)

@DungeonFinder.app.route('/api/v1/users/discord/')
def discord_status():
    """Retrieve user's Discord status."""
    logname = check_session()
    if logname == False:
        return flask.redirect('/accounts/login/')
    connection = DungeonFinder.model.get_db()
    cur = connection.execute(
        "SELECT * FROM users WHERE username = ?",
        (logname, )
    )
    discord = cur.fetchall()[0]['discord']
    context = {
        "user": logname,
        "discord": discord
    }
    return flask.jsonify(**context)
