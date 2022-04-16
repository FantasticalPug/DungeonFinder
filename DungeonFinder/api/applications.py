"""REACT API for Application Process Functions."""
import flask
import DungeonFinder
from DungeonFinder.views.accounts import check_session

@DungeonFinder.app.route('/api/v1/applications/add/', methods=['POST'])
def add_question():
    """Add a question for the application."""
    logname = check_session()
    if logname == False:
        return flask.redirect('/accounts/login/')
    gameid = flask.request.args['gameid']
    question = flask.request.args['question']
    connection = DungeonFinder.model.get_db()
    cur = connection.execute(
        "SELECT * FROM games WHERE gameid = ? AND owner = ?",
        (gameid, logname, )
    )
    if len(cur.fetchall()) != 1:
        context = {
            "code": 403,
            "message": "Forbidden"
        }
        return flask.jsonify(**context), 403
    cur = connection.execute(
        f"INSERT INTO apply_{gameid}(question) "
        "VALUES(?)",
        (question, )
    )
    cur = connection.execute(
        f"SELECT * FROM apply_{gameid}"
    )
    data = cur.fetchall()
    context = {
        "questions": data
    }
    return flask.jsonify(**context)

@DungeonFinder.app.route('/api/v1/applications/questions/')
def get_questions():
    """Retrieve the questions for the application."""
    logname = check_session()
    if logname == False:
        return flask.redirect('/accounts/login/')
    gameid = flask.request.args['gameid']
    connection = DungeonFinder.model.get_db()
    cur = connection.execute(
        "SELECT * FROM games WHERE gameid = ? AND owner = ?",
        (gameid, logname, )
    )
    if len(cur.fetchall()) != 1:
        context = {
            "code": 403,
            "message": "Forbidden"
        }
        return flask.jsonify(**context), 403
    cur = connection.execute(
        f"SELECT * FROM apply_{gameid}"
    )
    data = cur.fetchall()
    context = {
        "questions": data
    }
    return flask.jsonify(**context)
