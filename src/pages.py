from os.path import join
from flask import Flask, render_template, request, redirect, url_for, make_response

from helpers import PROJ_PATH, run_sql, salted_hash, table_to_html

app = Flask(__name__, static_url_path=join(PROJ_PATH, 'static'))


def check_password(role, login, passw_hash):
    table_name = {'mentor' : 'Mentors', 'student' : 'Students'}[role]
    query = "SELECT 1 FROM %s WHERE login=? AND password_hash=?;" % table_name
    return len(run_sql(query, (login, passw_hash))) > 0


def check_user(handler):
    def new_handler():
        role = request.cookies.get('user_role')
        login = request.cookies.get('login')
        passw_hash = request.cookies.get('passw_hash')
        try:
            if check_password(role, login, passw_hash):
                return handler()
        except BaseException as ex:
            print(ex)
        return redirect(url_for('page_login'))
    new_handler.__name__ = handler.__name__
    return new_handler


@app.route("/logout", methods=['GET'])
def page_unlogin():
    resp = make_response('logged out')
    resp.set_cookie('user_role', '', expires=0)
    resp.set_cookie('login', '', expires=0)
    resp.set_cookie('passw_hash', '', expires=0)
    return resp


@app.route("/login", methods=['GET'])
def page_login():
    return render_template('unlogged.html')


@app.route("/login", methods=['POST'])
def page_login_post():
    resp = make_response("login OK")
    role = request.form['role']
    login = request.form['login']
    passw_hash = salted_hash(request.form['password'])
    
    if not check_password(role, login, passw_hash):
        return "Invalid login or password"

    resp.set_cookie('user_role', role)
    resp.set_cookie('login', login)
    resp.set_cookie('passw_hash', passw_hash)
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


@app.route("/mentors_projects", methods=['GET'])
@check_user
def mentors_projects():
    assert request.cookies.get('user_role') == 'mentor'
    columns = ['name', 'description', 'result_description', 'keywords']
    query = "SELECT %s FROM Projects WHERE mentor=?;" % ",".join(columns)
    data = run_sql(query, (request.cookies.get('login'),))
    return render_template(
        'view_table.html',
        name="Мои проекты",
        table=table_to_html(data, columns)
    )


@app.route("/mentors_appl", methods=['GET'])
@check_user
def mentors_applications():
    assert request.cookies.get('user_role') == 'mentor'
    columns = ['team', 'project', 'Teams.name', 'Projects.name', 'is_approved', 'Teams.date_created']
    query = """
        SELECT %s FROM Team_Project_rel
                JOIN Projects ON Team_Project_rel.project = Projects.id
                JOIN Teams ON Team_Project_rel.team = Teams.id
        WHERE project IN
        (SELECT id FROM Projects WHERE mentor=?);
    """ % ",".join(columns)
    data = run_sql(query, (request.cookies.get('login'),))
    return render_template(
        'view_table.html',
        name="Мои проекты",
        table=table_to_html(data, ['team', 'project', 'is approved', 'created'])
    )

@app.route("/", methods=['GET'])
@check_user
def logged():
    if request.cookies.get('user_role') == 'mentor':
        return render_template("main_mentor.html")
    else:
        return render_template("main_student.html")

@app.route("/reg_student", methods=['GET'])
def reg_student_get():
    return render_template('form_reg_student.html')


@app.route("/reg_student", methods=['POST'])
def reg_student_post():
    login = request.form['login']
    passw = request.form['password']
    full_name = request.form['fullname']
    uni_group = request.form['unigroup']
    run_sql(
        "INSERT INTO Students(login, password_hash, full_name, uni_group) VALUES (?,?,?,?);",
        [login, passw, full_name, uni_group],
        commit=True
    )
    return "registration completed"
 

@app.route("/reg_mentor", methods=['GET'])
def reg_mentor_get():
    return render_template('form_reg_mentor.html')


@app.route("/reg_mentor", methods=['POST'])
def reg_mentor_post():
    login = request.form['login']
    passw = request.form['password']
    full_name = request.form['fullname']
    run_sql(
        "INSERT INTO Mentors(login, password_hash, full_name) VALUES (?,?,?);",
        [login, passw, full_name],
        commit=True
    )
    return "registration completed"


@app.route("/add_proj", methods=['GET'])
def add_proj_get():
    return render_template('form_add_project.html')


@app.route("/add_proj", methods=['POST'])
def add_proj_post():
    run_sql(
        "INSERT INTO Projects(name, description, keywords) VALUES (?,?,?);",
        [request.form[i] for i in ['name', 'description', 'keywords']],
        commit=True
    )
    return "project added"
