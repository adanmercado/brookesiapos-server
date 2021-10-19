import sqlite3
from flask_httpauth import HTTPBasicAuth
from sqlite3 import Error

from brookesiapos.database import connection

http_auth = HTTPBasicAuth()

@http_auth.verify_password
def verify_password(username, password):
    conn = connection.create_connection()
    sql_query = f'SELECT password FROM users WHERE username="{username}";'

    try:
        cursor = conn.cursor()
        cursor.execute(sql_query)
        
        row = cursor.fetchone()
        if row:
            passwd = row[0]
            if passwd and passwd == password:
                return username
    except Error as e:
        print(f'Database error: {str(e)}')
        #pass
    finally:
        if conn:
            cursor.close()
            conn.close()