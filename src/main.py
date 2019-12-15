import os
from os.path import join

from generate_data import generate_data
from helpers import SRC_PATH, PROJ_PATH, DB_PATH, run_sql
from pages import app

def init_db(gen_data=True, rewrite=True):
    if not rewrite and os.path.isfile(DB_PATH):
        return
    commands = open(join(SRC_PATH, "create_db.sql")).read().split('\n\n')
    run_sql(commands, commit=True)
    if gen_data:
        generate_data()


init_db()
app.run()
