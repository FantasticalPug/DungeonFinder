"""REST API V1."""
import flask
import DungeonFinder

@DungeonFinder.app.route('/api/v1/')
def get_services():
    """Return the API Services."""
    context = {
        "unlink_discord": "/api/v1/users/unlink/",
        "discord_status": "/api/v1/users/discord/",
        "join_game": "/api/v1/games/join/",
        "leave_game": "/api/v1/games/leave/",
        "game_status": "/api/v1/games/status/",
        "add_player": "/api/v1/applications/add/",
        "retrieve_application_questions": "/api/v1/applications/questions/"
    }
    return flask.jsonify(**context)
