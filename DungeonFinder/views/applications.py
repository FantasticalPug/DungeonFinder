"""DungeonFinder Application Views."""
import flask
import DungeonFinder
from DungeonFinder.views.accounts import check_session

@DungeonFinder.app.route('/games/<path:gameid>/apply/')
def show_application(gameid):
    """Show the application page."""
    logname = check_session()
    if logname == False:
        return flask.redirect('/accounts/login/')
    connection = DungeonFinder.model.get_db()
    cur = connection.execute(
        f"SELECT * FROM apply_{gameid}"
    )
    data = cur.fetchall()
    i = 1
    for question in data:
        question['number'] = i
        i += 1
    cur = connection.execute(
        "SELECT * FROM games WHERE gameid = ?",
        (gameid, )
    )
    game = cur.fetchall()[0]
    context = {
        "logname": logname,
        "questions": data,
        "game": game,
        "page": "Apply"
    }
    return flask.render_template("apply.html", **context)

@DungeonFinder.app.route('/games/<path:gameid>/apply/submit/', methods=['POST'])
def submit_application(gameid):
    """Submit an application for game owner to review."""
    logname = check_session()
    if logname == False:
        return flask.redirect('/accounts/login/')
    connection = DungeonFinder.model.get_db()
    connection.execute(
        f"INSERT INTO sessions(gameid, player, status) "
        "VALUES(?, ?, ?)",
        (gameid, logname, "Applied", )
    )
    for answer in flask.request.form:
        connection.execute(
            f"INSERT INTO responses_{gameid} (questionid, answer, player) "
            "VALUES(?, ?, ?)",
            (answer, flask.request.form[answer], logname, )
        )
    return flask.redirect(f'/games/{gameid}/')

@DungeonFinder.app.route('/games/<path:gameid>/apply/view/')
def show_applications(gameid):
    """Show all the applications for a given game."""
    logname = check_session()
    if logname == False:
        return flask.redirect('/accounts/login/')
    connection = DungeonFinder.model.get_db()
    cur = connection.execute(
        f"SELECT * FROM apply_{gameid}"
    )
    questions = cur.fetchall()
    cur = connection.execute(
        f"SELECT * FROM responses_{gameid}"
    )
    responses_dict = {}
    data = cur.fetchall()
    for response in data:
        responses_dict[response['player']] = []
    responses = []
    for response in responses_dict:
        cur = connection.execute(
            f"SELECT * FROM responses_{gameid} WHERE player = ?",
            (response, )
        )
        responses.append(cur.fetchall())
    found = len(responses) > 0
    context = {
        "logname": logname,
        "questions": questions,
        "responses": responses,
        "found": found,
        "gameid": gameid,
        "page": "Applications"
    }
    return flask.render_template("applications.html", **context)

@DungeonFinder.app.route('/games/<path:gameid>/apply/accept/')
def accept_player(gameid):
    """Accept the player to the game."""
    logname = check_session()
    if logname == False:
        return flask.redirect('/accounts/login/')
    connection = DungeonFinder.model.get_db()
    player = flask.request.args['player']
    connection.execute(
        "UPDATE sessions SET status = ? WHERE gameid = ? AND player = ?",
        ("Joined", gameid, player, )
    )
    connection.execute(
        f"DELETE FROM responses_{gameid} WHERE player = ?",
        (player, )
    )
    return flask.redirect(f'/games/{gameid}/apply/view/')
