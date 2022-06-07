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


def select_one_from_table(table_name, item_id):
    conn = connection.create_connection()

    sql_query = f'SELECT * FROM {table_name} WHERE id = {item_id}'

    try:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(sql_query)

        row = cursor.fetchone()
        if row:
            data = dict(row)
            return data
    except sqlite3.Error as e:
        print(f'Error at select_one_from_table(table_name, item_id): {str(e)}')
        return False
    finally:
        if conn:
            cursor.close()
            conn.close()

        
def insert_into_table(table_name, data_dict):
    conn = connection.create_connection()

    data = dict(data_dict)

    columns = ','.join(data.keys())
    placeholders = ','.join(['%s'] * len(data))
    values = data.values()

    sql_query = f'INSERT INTO {table_name}({columns}) VALUES({placeholders})'

    try:
        cursor = conn.cursor()
        cursor.execute(sql_query)
        return data
    except sqlite3.Error as e:
        print(f'Error at insert_into_table(table_name, data_dict): {str(e)}')
        return False
    finally:
        if conn:
            cursor.close()
            conn.close()