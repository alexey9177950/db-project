import os
from os.path import dirname, join
import sqlite3

SRC_PATH = dirname(os.path.realpath(__file__))
PROJ_PATH = dirname(SRC_PATH)
DB_PATH = join(PROJ_PATH, 'data', 'base.db')

def run_sql(query, params=[], commit=False):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    if type(query) == str:
        cursor.execute(query, params)
    else:
        for cmd in query:
            print(cmd)
            cursor.execute(cmd)
    res = cursor.fetchall()
    if commit:
        connection.commit()
    connection.close()
    return res


def insert_data(table_name, values):
    values = list(values)
    row_len = len(values[0])
    row_num = len(values)

    template = "INSERT INTO %s VALUES (" + ",".join("?" for i in range(row_len)) + ");"
    print(template)

    connection = sqlite3.connect(DB_PATH)
    connection.cursor().executemany(template % table_name, values)
    connection.commit()
    connection.close()


def run_select(table_name, search_by=None, search_val=None):
    if search_by:
        query = "SELECT * FROM {table_name} WHERE {search_by}={search_val}".format(
            table_name=table_name,
            search_by=search_by,
            search_val=search_val
        )
    else:
        query = "SELECT * FROM {table_name}".format(table_name=table_name)
    return run_sql(query)
