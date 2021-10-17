import sqlite3
from brookesiapos.utils import standard_paths

db_filepath = standard_paths.config_path() / 'brookesiapos-server/brookesiapos.db'

def create_connection():
    connection = None

    try:
        connection = sqlite3.connect(db_filepath)
    except sqlite3.Error as e:
        print(f'Error connecting to database: {str(e)}')

    return connection