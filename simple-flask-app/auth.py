import sys
from flask import Blueprint, render_template, redirect, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash
from UserCredentials import UserCredentials


auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/logout')
def logout():
    return 'Logout'


@auth.route('/signup', methods=['POST'])
def signup_post():
    email = str(request.form.get('email'))
    name = str(request.form.get('name'))
    password = str(request.form.get('password'))

    database_credentials = UserCredentials("testDB.db", "credentials")
    database_credentials.access_database("WOOO!!!!!!!!!!")

    key_in_database = database_credentials.fetch_table_column("login_username")

    for entry in key_in_database:
        if entry:
            return redirect(url_for('auth.signup'))

    hashed_password = generate_password_hash(password, method='sha256')
    database_credentials.populate_table(name, hashed_password, email)
    # database_credentials.commit_changes()
    test_print = database_credentials.fetch_entire_table()
    print(test_print)

    return redirect(url_for('auth.login'))
