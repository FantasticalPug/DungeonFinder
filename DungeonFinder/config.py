"""DungeonFinder Development Configuration."""
import pathlib

APPLICATION_ROOT = '/'

SECRET_KEY = b'8H\xc3\xf1T\xecs\xe0ZY\x9c\xd3\xbf\x06Z;\x87o\n\x16h \x1e<\x8b?_hC\xa1M\xfa'
SESSION_COOKIE_NAME = 'login'

DF_ROOT = pathlib.Path(__file__).resolve().parent.parent
UPLOAD_FOLDER = DF_ROOT/'var'/'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

DATABASE_FILENAME = DF_ROOT/'var'/'df.sqlite3'
