import sys
from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from UserCredentials import UserCredentials
from authenticateduser import authenticated_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
def login_post():
    name = str(request.form.get('name'))
    password = str(request.form.get('password'))

    database_credentials = UserCredentials("testDB.db", "user_movie_credentials")
    database_credentials.access_database("WOOO!!!!!!!!!!")

    login_user = database_credentials.authenticate_user(name, password)

    if login_user:
        database_user_information = database_credentials.fetch_entire_table()
        for user in database_user_information:
            if name == str(user[0]):
                authenticated_user.update_user(user[0], user[2], user[3], user[4], user[5], user[6], user[8])
                # username = user[3] + " " + user[4]
                return redirect(url_for('main.profile_post'))
    else:
        print("here")
        flash('Please check your login details and try again')
        return redirect(url_for('auth.login'))


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
    first_name = str(request.form.get('firstName'))
    last_name = str(request.form.get('lastName'))
    phone_number = str(request.form.get('phoneNumber'))
    preferred_comm = str(request.form.get('commMethod'))
    favorite_theater = "AMC"
    favorite_genre = str(request.form.get('genre'))

    database_credentials = UserCredentials("testDB.db", "user_movie_credentials")
    database_credentials.access_database("WOOO!!!!!!!!!!")

    key_in_database = database_credentials.fetch_table_column("login_username")

    for entry in key_in_database:
        if entry == name:
            flash('Username is already in use')
            print('Username is already in use')
            return redirect(url_for('auth.signup'))

    hashed_password = generate_password_hash(password)
    print(check_password_hash(hashed_password, password))
    print("boolean check")
    database_credentials.populate_table(name, hashed_password, email, first_name, last_name, phone_number,
                                        preferred_comm, favorite_theater, favorite_genre)
    database_credentials.commit_changes()
    test_print = database_credentials.fetch_entire_table()
    print(test_print)

    return redirect(url_for('auth.login'))
