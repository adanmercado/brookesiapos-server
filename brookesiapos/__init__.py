import sys

from flask import Flask

from .database.connection import db_filepath
from .users import users_bp
from .utils import error_handler

if not db_filepath.exists():
    print(f'The database file {str(db_filepath)} does not exist. Run the database/setup.py script to create and initialize the database and try again or configure the database manually.')
    sys.exit(0)

app = Flask(__name__)
app.register_blueprint(users_bp)
#app.register_error_handler(404, error_handler.not_found)
app.register_error_handler(404, error_handler.generic_error_handler)
app.register_error_handler(500, error_handler.generic_error_handler)