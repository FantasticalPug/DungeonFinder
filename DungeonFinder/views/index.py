"""DungeonFinder Index View."""
import flask
import requests
import DungeonFinder
from DungeonFinder.views.accounts import check_session

@DungeonFinder.app.route('/')
def show_index():
    """Display the index page."""
    logname = check_session()
    if logname == False:
        return flask.redirect('/accounts/login/')
    context = {
        "logname": logname,
        "page": "Search"
    }
    return flask.render_template("index.html", **context)

@DungeonFinder.app.route('/service-worker.js')
def service():
	"""Reroute for the Service Worker."""
	return flask.send_from_directory(DungeonFinder.app.root_path, 'service-worker.js')

@DungeonFinder.app.route('/offline.html')
def offline():
    """Reroute for when the user is offline."""
    return flask.send_from_directory(DungeonFinder.app.root_path, 'offline.html')

@DungeonFinder.app.route('/robots.txt')
def robots():
    """Reroute for the robots.txt file."""
    return flask.send_from_directory(DungeonFinder.app.root_path, 'robots.txt')

@DungeonFinder.app.route('/uploads/<path:filename>')
def download_file(filename):
    """Retrieve an uploaded file from storage."""
    logname = check_session()
    if logname == False:
        return flask.redirect('/accounts/login/')
    folder = DungeonFinder.app.config['UPLOAD_FOLDER']
    return flask.send_from_directory(folder, filename)

@DungeonFinder.app.route('/discord/')
def discord_authorized():
    """Redirect back to user profile after discord was authorized."""
    logname = check_session()
    if logname == False:
        return flask.redirect('/accounts/login/')
    if flask.request.args.get('code', None) is None:
        return flask.redirect(f"/users/{logname}/")
    data = {
        'client_id': "953184670315589662",
        'client_secret': "MuyqhIzVyVWtwN-Z1hEykzEYPVHsZOFV",
        'grant_type': 'authorization_code',
        'code': flask.request.args['code'],
        'redirect_uri': "https://www.thedungeonfinder.com/discord/"
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.post('%s/oauth2/token' % "https://discord.com/api/v8", data=data, headers=headers)
    response.raise_for_status()
    data = response.json()
    headers = {
        "Authorization": f"{data['token_type']} {data['access_token']}"
    }
    response = requests.get("https://discord.com/api/v8/users/@me", headers=headers)
    data = response.json()
    discord = f"{data['username']}#{data['discriminator']}"
    connection = DungeonFinder.model.get_db()
    connection.execute(
        "UPDATE users SET discord = ? WHERE username = ?",
        (discord, logname, )
    )
    return flask.redirect(f"/users/{logname}/")

@DungeonFinder.app.route('/error/')
def error():
    """Show a helpful error message for the user."""
    logname = check_session()
    if logname == False:
        logname = "Login"
    code = flask.request.args['code']
    message = flask.request.args['message']
    context = {
        "logname": logname,
        "code": code,
        "message": message,
        "page": "Error"
    }
    return flask.render_template("error.html", **context)
