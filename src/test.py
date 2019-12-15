from datetime import datetime

import sqlite3

DB_PATH = '../data/base.db'

query = "INSERT INTO Universities VALUES (?, ?, ?), (?, ?, ?);"
params = [
    1, 'kek', datetime.now(),
    2, 'mem',  datetime.now()
]

connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()
cursor.execute(query, params)
cursor.execute("SELECT * FROM Universities")
print(cursor.fetchall())
connection.close()
