import sys
from flask import Blueprint, render_template, redirect, url_for
from authenticateduser import authenticated_user
from UserCredentials import UserCredentials


main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


# @main.route('/profile/<name>')
# def profile_post(name):
#     print(authenticated_user.username)
#     print(authenticated_user.email)
#     print(authenticated_user.first_name)
#     print(authenticated_user.last_name)
#     print(authenticated_user.phone_number)
#     print(authenticated_user.fmg)
#     print(authenticated_user.pcm)
#     return render_template('profile.html', name=name)
@main.route('/profile/Welcome')
def profile_post():
    username = authenticated_user.first_name + " " + authenticated_user.last_name
    return render_template('profile.html', name=username)


@main.route('/profile')
def profile():
    if authenticated_user.username is None:
        database_credentials = UserCredentials("testDB.db", "user_movie_credentials")
        database_credentials.access_database("WOOO!!!!!!!!!!")
        database_credentials.truncate_table()
        return redirect(url_for('auth.login'))
    else:
        return redirect(url_for('main.profile_post'))
