import sqlite3
import re
from . import connection

def select_all_from_table(table_name: str):
    sql_query = f'SELECT * FROM {table_name}'
    rows = execute_query(sql_query)
    data = [dict(row) for row in rows]
    return data


def select_one_from_table(table_name: str, item_id: int):
    sql_query = f'SELECT * FROM {table_name} WHERE id = {item_id}'
    rows = execute_query(sql_query)
    data = [dict(row) for row in rows]
    return data

        
def insert_into_table(table_name: str, data_dict: dict):
    columns = ','.join(data_dict.keys())
    placeholders = ','.join(['?'] * len(data_dict))
    values = tuple(x for x in data_dict.values())

    sql_query = f'INSERT INTO {table_name}({columns}) VALUES({placeholders})'

    inserted_id = execute_query(sql_query, values)
    if inserted_id:
        data_dict['id'] = inserted_id
        return data_dict
    else:
        return False

def item_exists(table_name, field, value):
    sql_query = f'SELECT {field} FROM {table_name} WHERE {field}=\'{value}\''
    item = execute_query(sql_query)
    return item

def execute_query(query: str, values: tuple = None):
    conn = connection.create_connection()

    try:
        if re.match('SELECT\s[{}_=\\\'"A-Za-z\s*]+', query) != None:
            conn.row_factory = sqlite3.Row

        cursor = conn.cursor()
        if values != None:
            cursor.execute(query, values)
        else:
            cursor.execute(query)
        
        if re.match('SELECT\s[{}_=\\\'"A-Za-z\s*]+', query) != None:
            data = cursor.fetchall()
            return data
        elif re.match('INSERT\s[{}_=\\\'"A-Za-z\s*]+', query) != None:
            conn.commit()
            inserted_id = cursor.lastrowid
            return inserted_id
    except sqlite3.Error as e:
        print(f'Error executing query: {str(e)}')
        return False
    finally:
        if conn:
            cursor.close()
            conn.close()