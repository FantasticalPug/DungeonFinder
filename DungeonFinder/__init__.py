"""DungeonFinder Package Initializer."""
import flask

app = flask.Flask(__name__)

app.config.from_object('DungeonFinder.config')

app.config.from_envvar('DUNGEONFINDER_SETTINGS', silent=True)

import DungeonFinder.views
import DungeonFinder.model
import DungeonFinder.api
