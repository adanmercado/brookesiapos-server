from flask_httpauth import HTTPBasicAuth

from brookesiapos.database import db_manager

http_auth = HTTPBasicAuth()

@http_auth.verify_password
def verify_password(username, password):
    data = db_manager.select_item_from_table('users', 'username', username)

    if data and data[0]['password'] == password:
        return username