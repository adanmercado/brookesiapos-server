import sys

from flask import Flask
from .database.connection import db_filepath

if not db_filepath.exists():
    print(f'The database file {str(db_filepath)} does not exist. Run the database/setup.py script to create and initialize the database and try again or configure the database manually.')
    sys.exit(0)

app = Flask(__name__)