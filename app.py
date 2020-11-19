from Tool import app, db
import os
import pandas as pd
import numpy as np
from Tool.forms import RegistrationForm, LoginForm, QueryForm, csv_name
from Tool.models import User
from flask import render_template, request, url_for, redirect, flash, abort
from flask_login import current_user, login_required, login_user, logout_user
from picture_handler import add_profile_pic
from sqlalchemy import desc, asc
from werkzeug.utils import secure_filename
from flask import send_from_directory
import csv
from sklearn.linear_model import LinearRegression

ALLOWED_EXTENSIONS = {'csv'}


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.htm")


@app.route('/querygen', methods=['GET', 'POST'])
@login_required
def querygen():
    return render_template("howto.htm")


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def linear():
    try:
        mylist = ['import pandas as pd', 'import numpy as np',
                  'from sklearn.linear_model import LinearRegression']
        numeric_column = []
        df_test = pd.read_csv('Tool/static/csvs/' +
                              current_user.username + 'test' + '.csv')
        df_train = pd.read_csv('Tool/static/csvs/' +
                               current_user.username + 'train' + '.csv')
        for i in df_train.columns:
            if type(df_train[i][0]) == str:
                continue
            else:
                numeric_column.append(i)
        if request.method == 'POST':
            train_csv_name = request.form.get("train_csv")
            test_csv_name = request.form.get("test_csv")
            y = request.form.get("column_name")
            numeric_column.remove(y)
            mylist.append("df_train = pd.read_csv('" + train_csv_name + "')")
            mylist.append("df_test = pd.read_csv('" + test_csv_name + "')")
            mylist.append('X_train = df_train[' + str(numeric_column) + ']')
            mylist.append("y_train = df_train['" + y + "']")
            mylist.append('X_test = df_test[' + str(numeric_column) + ']')
            mylist.append('lm = LinearRegression()')
            mylist.append('lm.fit(X_train , y_train)')
            mylist.append('predictions = lm.predict(X_test)')
            flash(mylist)
    except:
        return redirect(url_for('upload_file'))
    return render_template("dashboard.htm", numeric_column=numeric_column)

@app.route('/ytakelinear' , methods = ['GET' , 'POST'])
@login_required
def ylinear():
    numeric_column = []
    df_train = pd.read_csv('Tool/static/csvs/' +
                           current_user.username + 'train' + '.csv')
    for i in df_train.columns:
        if type(df_train[i][0]) == str:
            continue
        else:
            numeric_column.append(i)
    if request.method == 'POST':
        y = request.form.get("y_column")
        print(y)
        return redirect(url_for('linear_predict' , y = y))
    return render_template('linearpredicty.htm' , numeric_column = numeric_column)

@app.route('/linearpredict/<y>' , methods = ['GET' , 'POST'])
@login_required
def linear_predict(y):
    numeric_column = []
    X_test = []
    df_train = pd.read_csv('Tool/static/csvs/' + current_user.username + 'train' + '.csv')
    for i in df_train.columns:
        if type(df_train[i][0]) == str:
            continue
        else:
            numeric_column.append(i)
    numeric_column.remove(y)
    if request.method == 'POST':
        X_train = df_train[numeric_column]
        y_train = df_train[y]
        for j in request.form.getlist('x_cases'):
            X_test.append(int(j))
        X_test = pd.DataFrame([X_test],index=[0],columns=numeric_column)
        lm = LinearRegression()
        lm.fit(X_train , y_train)
        predictions = lm.predict(X_test)
        flash(predictions)
    return render_template('linear_predict.htm' , numeric_column = numeric_column )

# logistic regression


@app.route('/dashboard2', methods=['GET', 'POST'])
@login_required
def logistic():
    try:
        mylist = ['import pandas as pd', 'import numpy as np',
                  'from sklearn.linear_model import LogisticRegression']
        numeric_column = []
        df_test = pd.read_csv('Tool/static/csvs/' +
                              current_user.username + 'test' + 'logic'+ '.csv')
        df_train = pd.read_csv('Tool/static/csvs/' +
                               current_user.username + 'train' +'logic'+ '.csv')
        for i in df_train.columns:
            if type(df_train[i][0]) == str:
                continue
            else:
                numeric_column.append(i)
        form = csv_name()
        if request.method == 'POST':
            train_csv_name = request.form.get("train_csv")
            test_csv_name = request.form.get("test_csv")
            y = request.form.get("column_name")
            numeric_column.remove(y)
            mylist.append("df_train = pd.read_csv('" + train_csv_name + "')")
            mylist.append("df_test = pd.read_csv('" + test_csv_name + "')")
            mylist.append('X_train = df_train[' + str(numeric_column) + ']')
            mylist.append("y_train = df_train['" + y + "']")
            mylist.append('X_test = df_test[' + str(numeric_column) + ']')
            mylist.append('lg = LogisticRegression()')
            mylist.append('lg.fit(X_train , y_train)')
            mylist.append('predictions = lg.predict(X_test)')
            flash(mylist)
    except:
        return(redirect(url_for('upload_file_logic')))
    return render_template("dashboard2.htm", numeric_column=numeric_column)

# knn

@app.route('/dashboard3', methods=['GET', 'POST'])
@login_required
def knn():
    mylist = ['import pandas as pd', 'import numpy as np',
              'from sklearn.preprocessing import StandardScaler',
              'from sklearn.neighbors import KNeighborsClassifier']
    numeric_column = []
    df_test = pd.read_csv('Tool/static/csvs/' +
                          current_user.username + 'test' + '.csv')
    df_train = pd.read_csv('Tool/static/csvs/' +
                           current_user.username + 'train' + '.csv')
    for i in df_train.columns:
        if type(df_train[i][0]) == str:
            continue
        else:
            numeric_column.append(i)
    form = csv_name()
    if request.method == 'POST':
        train_csv_name = request.form.get("train_csv")
        test_csv_name = request.form.get("test_csv")
        y = request.form.get("column_name")
        numeric_column.remove(y)
        mylist.append('scaler = StandardScaler()')
        mylist.append('scaler.fit(df_train)')
        mylist.append('scaled_features = scaler.transform(df_train)')
        mylist.append('df_feat = pd.DataFrame(scaled_features, columns=df_train.columns)')
        mylist.append('X_train = df_train[' + str(numeric_column) + ']')
        mylist.append("y_train = df_train['" + y + "']")
        mylist.append('X_test = df_test[' + str(numeric_column) + ']')
        mylist.append('knn = KNeighborsClassifier(n_neighbors=10)')
        mylist.append('knn.fit(X_train , y_train)')
        mylist.append('predictions = knn.predict(X_test)')
        flash(mylist)
    return render_template("dashboard3.htm", numeric_column=numeric_column)


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
                next = url_for('linear')
            return redirect(next)
        elif user is not None and user.check_password(form.password.data) == False:
            error = 'Wrong Password'
        elif user is None:
            error = 'No such login Pls create one'
    return render_template('login.htm', form=form, error=error)


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


@app.route('/queryform', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        train = request.files['train']
        test = request.files['test']
        train.save('Tool/static/csvs/' +
                   current_user.username + 'train' + '.csv')
        test.save('Tool/static/csvs/' +
                  current_user.username + 'test' + '.csv')
        return redirect(url_for('linear'))
    return render_template('query.htm')

@app.route('/queryform2', methods=['GET', 'POST'])
@login_required
def upload_file_logic():
    if request.method == 'POST':
        train = request.files['train']
        test = request.files['test']
        train.save('Tool/static/csvs/' +
                   current_user.username + 'train' + 'logic'+ '.csv')
        test.save('Tool/static/csvs/' +
                  current_user.username + 'test' +'logic' +'.csv')
        return redirect(url_for('logistic'))
    return render_template('query.htm')

if __name__ == '__main__':
    app.run(debug=True)
