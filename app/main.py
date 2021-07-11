import sys
from flask import Blueprint, render_template, redirect, url_for

from User.user_auth import authenticated_user
from User.user_credentials import UserCredentials
from AMC.AMC import AMCMovie
from AMC.AMCRequest import AMCRequest

main = Blueprint('main', __name__)


@main.route('/')
def index():
    database_credentials = UserCredentials("testDB.db", "user_creds")
    database_credentials.access_database("WOOO!!!!!!!!!!")
    if authenticated_user.authenticated == "False":
        authenticated_user.log_out_user()
    # database_credentials.create_movie_trailer_table()
    # database_credentials.populate_movie_trailer_table()
    requester = AMCRequest()
    current_movie_list = requester.get_current_movies()
    return render_template('index.html', verified_user=authenticated_user.verified, movie_list = current_movie_list,
                           first_name=authenticated_user.first_name, link=str(database_credentials.get_new_movie_trailer()),
                           favorited_theater=authenticated_user.theater_string)


@main.route('/profile/Welcome')
def profile_post():
    username = authenticated_user.first_name + " " + authenticated_user.last_name

    testMovie = AMCMovie(name="LOTR", actors=["Frodo","Legolas","Boromir"], director="Peter Jackson", genre="Fantasy", rating="PG-13")
    testMovie2 = AMCMovie(name="LOTR", actors=["Frodo", "Legolas", "Boromir"], director="Peter Jackson", genre="Fantasy",
                         rating="PG-13")
    movieList = [testMovie, testMovie2]
    requester = AMCRequest()
    theater_list = requester.get_locations_via_zip('90210')
    current_movie_list = requester.get_current_movies()
    return render_template('profile.html', name=username, theater_list=None, movie_list=current_movie_list, verified_user=authenticated_user.verified,
                           first_name=authenticated_user.first_name, favorited_theater=authenticated_user.theater_string,
                           is_fav_theater=authenticated_user.favorite_theater_name)


@main.route('/profile')
def profile():
    if authenticated_user.username is None:
        return redirect(url_for('auth.login', verified_user=authenticated_user.verified,
                                first_name=authenticated_user.first_name, favorited_theater=authenticated_user.theater_string))
    else:
        return redirect(url_for('main.profile_post', verified_user=authenticated_user.verified,
                                first_name=authenticated_user.first_name, favorited_theater=authenticated_user.theater_string,
                                is_fav_theater=authenticated_user.favorite_theater_name))
