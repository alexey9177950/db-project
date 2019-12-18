from os.path import join
from flask import Flask, render_template, request, redirect, url_for, make_response

from helpers import PROJ_PATH
from helpers import run_select
from hashlib import sha256


app = Flask(__name__, static_url_path=join(PROJ_PATH, 'static'))


def check_user(handler):
    def new_handler():
        role = request.cookies.get('user_role')
        login = request.cookies.get('login')
        passw_hash = request.cookies.get('passw_hash')
        try:
            check_passw(role, login, pass_hash)
        except: pass
        return redirect(url_for('page_login'))
    new_handler.__name__ = handler.__name__
    return new_handler


def check_user(handler):
    def new_handler():
        c1 = request.cookies.get('uid')
        c2 =  request.cookies.get('passw_hash')
        try:
            c1, c2 = int(c1), int(c2)
            if c1 + 3 == c2:
                return handler()
        except: pass
        return redirect(url_for('page_login'))
    new_handler.__name__ = handler.__name__
    return new_handler


@app.route("/logout", methods=['GET'])
def page_unlogin():
    resp = make_response('logged out')
    resp.set_cookie('uid', '', expires=0)
    resp.set_cookie('passw_hash', '', expires=0)
    return resp


@app.route("/login", methods=['GET'])
def page_login():
    c1 = request.cookies.get('uid', '42')
    return render_template('unlogged.html')


@app.route("/login", methods=['POST'])
def page_login_post():
    resp = make_response("login OK")
    resp.set_cookie('uid', '42')
    resp.set_cookie('passw_hash', '45')
    return resp


@app.route("/view")
def page_view_table():
    table_name=request.args.get('table')
    search_by = request.args.get('searchby')
    search_val = request.args.get('searchval')
    table = run_select(table_name, search_by, search_val)
    return render_template(
        "view_table.html",
        table_name=table_name,
        search_by=search_by or "",
        search_val=search_val or "",
        table=table
    )

@app.route("/", methods=['GET'])
@check_user
def logged():
    return "main pagged for logged users"
