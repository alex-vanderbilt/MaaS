import sys
from flask import Blueprint, render_template, redirect, url_for

from authenticateduser import authenticated_user
from UserCredentials import UserCredentials


main = Blueprint('main', __name__)


@main.route('/')
def index():
    database_credentials = UserCredentials("testDB.db", "user_creds")
    database_credentials.access_database("WOOO!!!!!!!!!!")
    print(database_credentials.get_new_movie_trailer())
    return render_template('index.html', verified_user=authenticated_user.verified,
                           first_name=authenticated_user.first_name, link=str(database_credentials.get_new_movie_trailer()))


@main.route('/profile/Welcome')
def profile_post():
    username = authenticated_user.first_name + " " + authenticated_user.last_name
    return render_template('profile.html', name=username, verified_user=authenticated_user.verified,
                           first_name=authenticated_user.first_name)


@main.route('/profile')
def profile():
    if authenticated_user.username is None:
        return redirect(url_for('auth.login', verified_user=authenticated_user.verified,
                                first_name=authenticated_user.first_name))
    else:
        return redirect(url_for('main.profile_post', verified_user=authenticated_user.verified,
                                first_name=authenticated_user.first_name))
