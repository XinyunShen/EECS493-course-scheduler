"""wolfpack development configuration."""

import pathlib

# Root of this application, useful if it doesn't occupy an entire domain
APPLICATION_ROOT = '/'

# Secret key for encrypting cookies
SECRET_KEY = b'\xeeD~\xf0\x98\xe4\x8b\x0b$s\x00\x8f\
                K\xbf^\xcduL\xb3\x0b\xdd;\xa3&'
SESSION_COOKIE_NAME = 'login'

# File Upload to var/uploads/
wolfpack_ROOT = pathlib.Path(__file__).resolve().parent.parent
# UPLOAD_FOLDER = wolfpack_ROOT/'var'/'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# Database file is var/wolfpack.sqlite3
DATABASE_FILENAME = wolfpack_ROOT/'var'/'wolfpack.sqlite3'
UPLOAD_FOLDER = wolfpack_ROOT/'wolfpack'/'static'/'profile_img'
