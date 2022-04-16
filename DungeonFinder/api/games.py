"""REST API for Games Functions."""
import flask
import DungeonFinder
from DungeonFinder.views.accounts import check_session

@DungeonFinder.app.route('/api/v1/games/join/', methods=['POST'])
def join_campaign():
    """Join a game."""
    logname = check_session()
    if logname == False:
        return flask.redirect('/accounts/login/')
    gameid = flask.request.args['gameid']
    connection = DungeonFinder.model.get_db()
    cur = connection.execute(
        "SELECT * FROM sessions WHERE gameid = ?",
        (gameid, )
    )
    data = cur.fetchall()
    cur = connection.execute(
        "SELECT * FROM games WHERE gameid = ?",
        (gameid, )
    )
    limit = cur.fetchall()[0]
    limit = limit['slots']
    if limit <= len(data):
        context = {
            "joined": True
        }
        return flask.jsonify(**context)
    cur = connection.execute(
        "INSERT INTO sessions(gameid, player, status) "
        "VALUES(?, ?, ?)",
        (gameid, logname, "Joined")
    )
    cur = connection.execute(
        "SELECT * FROM games WHERE gameid = ?",
        (gameid, )
    )
    data = cur.fetchall()[0]
    slots = data['slots']
    cur = connection.execute(
        "SELECT * FROM sessions WHERE gameid = ? AND status = ?",
        (gameid, "Joined", )
    )
    players = cur.fetchall()
    avail = len(players)
    context = {
        "joined": True,
        "avail": avail,
        "slots": slots
    }
    return flask.jsonify(**context)

@DungeonFinder.app.route('/api/v1/games/leave/', methods=['POST'])
def leave_game():
    """Leave a game."""
    logname = check_session()
    if logname == False:
        return flask.redirect('/accounts/login/')
    gameid = flask.request.args['gameid']
    connection = DungeonFinder.model.get_db()
    connection.execute(
        "DELETE FROM sessions WHERE gameid = ? AND player = ?",
        (gameid, logname, )
    )
    cur = connection.execute(
        "SELECT * FROM games WHERE gameid = ?",
        (gameid, )
    )
    data = cur.fetchall()[0]
    slots = data['slots']
    cur = connection.execute(
        "SELECT * FROM sessions WHERE gameid = ?",
        (gameid, )
    )
    players = cur.fetchall()
    avail = len(players)
    context = {
        "joined": False,
        "avail": avail,
        "slots": slots
    }
    return flask.jsonify(**context)

@DungeonFinder.app.route('/api/v1/games/status/')
def game_status():
    """Retrieve whether or not the user joined the game."""
    logname = check_session()
    if logname == False:
        return flask.redirect('/accounts/login/')
    gameid = flask.request.args['gameid']
    connection = DungeonFinder.model.get_db()
    cur = connection.execute(
        "SELECT * FROM sessions WHERE player = ? AND gameid = ?",
        (logname, gameid, )
    )
    data = cur.fetchall()
    joined = False
    if len(data) == 1:
        joined = True
    cur = connection.execute(
        "SELECT * FROM games WHERE gameid = ?",
        (gameid, )
    )
    data = cur.fetchall()[0]
    slots = data['slots']
    cur = connection.execute(
        "SELECT * FROM sessions WHERE gameid = ?",
        (gameid, )
    )
    players = cur.fetchall()
    avail = len(players)
    context = {
        "joined": joined,
        "avail": avail,
        "slots": slots
    }
    return flask.jsonify(**context)

@DungeonFinder.app.route('/api/v1/games/players/')
def retrieve_players():
    """Get player list for the given game."""
    logname = check_session()
    if logname == False:
        return flask.redirect('/accounts/login/')
    gameid = flask.request.args['gameid']
    connection = DungeonFinder.model.get_db()
    cur = connection.execute(
        "SELECT * FROM sessions WHERE gameid = ? AND status = ?",
        (gameid, "Joined", )
    )
    players = cur.fetchall()
    cur = connection.execute(
        "SELECT * FROM games WHERE gameid = ?",
        (gameid, )
    )
    data = cur.fetchall()[0]
    slots = data['slots']
    context = {
        "players": players,
        "slots": slots,
        "avail":len(players)
    }
    return flask.jsonify(**context)

@DungeonFinder.app.route('/api/v1/games/remove/', methods=["DELETE"])
def remove_player():
    """Remove a player from the game."""
    logname = check_session()
    if logname == False:
        return flask.redirect('/accounts/login/')
    player = flask.request.args['user']
    gameid = flask.request.args['gameid']
    connection = DungeonFinder.model.get_db()
    cur = connection.execute(
        "SELECT * FROM games WHERE gameid = ? AND owner = ?",
        (gameid, logname, )
    )
    if len(cur.fetchall()) != 1:
        cur = connection.execute(
            "SELECT * FROM sessions WHERE gameid = ?",
            (gameid, )
        )
        players = cur.fetchall()
        cur = connection.execute(
            "SELECT * FROM games WHERE gameid = ?",
            (gameid, )
        )
        data = cur.fetchall()[0]
        slots = data['slots']
        context = {
            "players": players,
            "slots": slots,
            "avail":len(players)
        }
        return flask.jsonify(**context)
    connection.execute(
        "DELETE FROM sessions WHERE gameid = ? AND player = ?",
        (gameid, player, )
    )
    cur = connection.execute(
        "SELECT * FROM sessions WHERE gameid = ?",
        (gameid, )
    )
    players = cur.fetchall()
    cur = connection.execute(
        "SELECT * FROM games WHERE gameid = ?",
        (gameid, )
    )
    data = cur.fetchall()[0]
    slots = data['slots']
    context = {
        "players": players,
        "slots": slots,
        "avail":len(players)
    }
    return flask.jsonify(**context)
