from Tool import app, db
import os
from Tool.forms import RegistrationForm, LoginForm, ProjectForm, TaskForm, QueryForm, QueryReq, UpdateTask, QueryReqWhere, UpdateQuery
from Tool.models import User
from flask import render_template, request, url_for, redirect, flash, abort
from flask_login import current_user, login_required, login_user, logout_user
from picture_handler import add_profile_pic
from sqlalchemy import desc, asc
from werkzeug.utils import secure_filename
from flask import send_from_directory
import csv

ALLOWED_EXTENSIONS = {'csv'}


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.htm")


@app.route('/querygen', methods=['GET', 'POST'])
@login_required
def querygen():
    return render_template("howto.htm")


@app.route('/create/select', methods=['GET', 'POST'])
@login_required
def dashboard():
    try:
        mystr = "SELECT "
        form = QueryReq()
        if form.validate_on_submit():
            table_name = form.table_name.data
        data = open('Tool/static/csvs/' + current_user.username +
                    '.csv', encoding='utf-8')
        csv_data = csv.reader(data)
        data_lines = list(csv_data)
        if request.method == 'POST':
            filter_list = request.form.getlist("filter_value")
            column_list = request.form.getlist("column_name")
            filter_list = [i for i in filter_list if i]
            for sublist in column_list:
                mylist = sublist.split(',')
                data = mylist[0]
                mydata = data[2:-1]
                mystr = mystr + mydata + ','
            mystr = mystr[:-1]
            mystr = mystr + " FROM " + table_name
            flash(mystr)
    except:
        return redirect(url_for('upload_file'))
    return render_template("dashboard.htm", data_lines=data_lines, form=form, mystr=mystr)


@app.route('/create/table', methods=['GET', 'POST'])
@login_required
def create_table():
    try:
        form = QueryReq()
        data = open('Tool/static/csvs/' + current_user.username +
                    'table_create' + '.csv', encoding='utf-8')
        csv_data = csv.reader(data)
        data_lines = list(csv_data)
        if form.validate_on_submit():
            table_name = form.table_name.data
            mystr = 'CREATE TABLE '
        if request.method == 'POST':
            primary_key = request.form.getlist("primary_key")
            line_one = mystr + table_name + ' ('
            myquery = [line_one]
            for v, d in data_lines:
                myquery.append('    ' + v + d + ',')
            myquery.append("PRIMARY_KEY" + " (" + primary_key[0] + ")")
            myquery.append(');')
            flash(myquery)
    except:
        return redirect(url_for('upload_file_create_table'))
    return render_template("table.htm", form=form, data_lines=data_lines)


@app.route('/create/where', methods=['GET', 'POST'])
@login_required
def create_where():
    try:
        value = ""
        mystr = "SELECT * FROM "
        myquery = []
        form = QueryReq()
        if form.validate_on_submit():
            table_name = form.table_name.data
            line_one = mystr + table_name
            myquery = [line_one]
        data = open('Tool/static/csvs/' + current_user.username +
                    'where' + '.csv', encoding='utf-8')
        csv_data = csv.reader(data)
        data_lines = list(csv_data)
        if request.method == 'POST':
            column_list = request.form.getlist("column_name")
            value_list_1 = request.form.getlist("value")
            value_list = []
            for i in value_list_1:
                if i:
                    value_list.append(i)
            line_two = "WHERE "
            for i in column_list:
                line_two = line_two + i + "=" + value_list.pop(0) + " AND "
            line_two = line_two[0:-4] + ";"
            myquery.append(line_two)
            flash(myquery)
            print(column_list)
            print(value_list)
    except:
        return redirect('upload_file_create_where')
    return render_template("where.htm", data_lines=data_lines, form=form, myquery=myquery)


@app.route('/create/update', methods=['GET', 'POST'])
@login_required
def update_query():
    form = UpdateQuery()
    if form.validate_on_submit():
        table_name = form.table_name.data
        column_name = form.column_name.data
        value = form.changed_val.data
        query = ["UPDATE " + table_name, "SET " + column_name + " = " + value]
        flash(query)
    return render_template("updatequery.htm", form=form)


@app.route('/edit_task/<projectid>', methods=['GET', 'POST'])
@login_required
def edit_task(projectid):
    tasks = Task.query.filter_by(projectid=projectid)
    na = 'No'
    nas = 'NO'
    taskss = []
    for task in tasks:
        taskss.append(task)
    taskss.reverse()
    return render_template("edit_task.htm", tasks=taskss, projectid=projectid, na=na, nas=nas)


@app.route('/edit_project', methods=['GET', 'POST'])
@login_required
def edit_project():
    projects = Project.query.filter_by(userid=current_user.id)
    projectss = []
    for project in projects:
        projectss.append(project)
    projectss.reverse()
    return render_template('edit_project.htm', projects=projectss)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():

        user = User(name=form.name.data,
                    username=form.username.data,
                    email=form.email.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()

        if form.picture.data is not None:
            id = user.id
            pic = add_profile_pic(form.picture.data, id)
            user.profile_image = pic
            db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.htm', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = ''
    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        if user is not None and user.check_password(form.password.data):

            login_user(user)

            next = request.args.get('next')
            if next == None or not next[0] == '/':
                next = url_for('projects')
            return redirect(next)
        elif user is not None and user.check_password(form.password.data) == False:
            error = 'Wrong Password'
        elif user is None:
            error = 'No such login Pls create one'
    return render_template('login.htm', form=form, error=error)


@app.route('/queryform', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            file.save('Tool/static/csvs/' + current_user.username + '.csv')
            return redirect(url_for('dashboard'))
    return render_template('query.htm')


@app.route('/querytableform', methods=['GET', 'POST'])
@login_required
def upload_file_create_table():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            file.save('Tool/static/csvs/' + current_user.username +
                      'table_create' + '.csv')
            return redirect(url_for('create_table'))
    return render_template('query.htm')


@app.route('/querywhereform', methods=['GET', 'POST'])
@login_required
def upload_file_create_where():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            file.save('Tool/static/csvs/' +
                      current_user.username + 'where' + '.csv')
            return redirect(url_for('create_where'))
    return render_template('query.htm')


if __name__ == '__main__':
    app.run(debug=True)
