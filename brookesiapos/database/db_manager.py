import sqlite3
from . import connection

def select_all_from_table(table_name):
    conn = connection.create_connection()

    sql_query = f'SELECT * FROM {table_name}'

    try:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(sql_query)

        rows = cursor.fetchall()
        data = [dict(row) for row in rows]
        return data
    except sqlite3.Error as e:
        print(f'Error at select_all_from_table({table_name}): {str(e)}')
        return False
    finally:
        if conn:
            cursor.close()
            conn.close()