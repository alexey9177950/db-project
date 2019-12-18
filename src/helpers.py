import os
from os.path import dirname, join
from hashlib import sha256
from flask import escape
import sqlite3

SRC_PATH = dirname(os.path.realpath(__file__))
PROJ_PATH = dirname(SRC_PATH)
DB_PATH = join(PROJ_PATH, 'data', 'base.db')

def table_to_html(table, header=None):
    html_rows = []
    if header:
        html_rows.append(" ".join("<th>" + i + "</th>" for i in header))
    for row in table:
        html_rows.append(" ".join("<td>" + str(i) + "</td>" for i in row))
    # TODO: escape

    return "<table>" +\
           "\n".join("<tr>" + i + "</tr>" for i in html_rows) +\
           "</table>"


def salted_hash(s):
    hasher = sha256()
    hasher.update('PREEEEFIX'.encode('utf-8'))
    hasher.update(s.encode('utf-8'))
    return hasher.hexdigest()


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
