import sys
from flask import Blueprint, render_template, redirect, url_for

from User.user_auth import authenticated_user
from User.user_credentials import UserCredentials
from AMC.AMC import AMCMovie
from AMC.AMCRequest import AMCRequest

main = Blueprint('main', __name__)



# application = Flask(__name__)
# application.config['SECRET_KEY'] = 'put super secret passcode here'

# if __name__ == '__main__':
    # from User.flask_auth import auth as auth_blueprint
    # application.register_blueprint(auth_blueprint)
    #
    # import main as main_blueprint
    # application.register_blueprint(main_blueprint)

    # return application


@main.route('/')
def index():
    database_credentials = UserCredentials("testDB.db", "user_creds")
    database_credentials.access_database("WOOO!!!!!!!!!!")
    link = database_credentials.get_new_movie_trailer()
    database_credentials.close_database()
    # if authenticated_user.authenticated == "False":
    #     authenticated_user.log_out_user()
    # database_credentials.create_movie_trailer_table()
    # database_credentials.populate_movie_trailer_table()
    requester = AMCRequest()
    current_movie_list = requester.get_current_movies()
    return render_template('index.html', verified_user=authenticated_user.verified, movie_list = current_movie_list,
                           first_name=authenticated_user.first_name, link=str(link),
                           favorited_theater=authenticated_user.theater_string,
                           name=authenticated_user.username)


@main.route('/profile/Welcome')
def profile_post():
    requester = AMCRequest()
    current_movie_list = requester.get_current_movies()
    return render_template('profile.html', theater_list=None, verified_user=authenticated_user.verified,
                           first_name=authenticated_user.first_name,
                           favorited_theater=authenticated_user.theater_string,
                           is_fav_theater=authenticated_user.favorite_theater_name,
                           current_user=authenticated_user)


@main.route('/profile')
def profile():
    if authenticated_user.username is None:
        return redirect(url_for('auth.login', verified_user=authenticated_user.verified,
                                first_name=authenticated_user.first_name, favorited_theater=authenticated_user.theater_string,
                                name=authenticated_user.username))
    else:
        return redirect(url_for('main.profile_post', verified_user=authenticated_user.verified,
                                first_name=authenticated_user.first_name, favorited_theater=authenticated_user.theater_string,
                                is_fav_theater=authenticated_user.favorite_theater_name,
                                current_user=authenticated_user,
                                name=authenticated_user.username,))


@main.route('/developer_console')
def developer():
    return render_template('main.profile_post', theater_list=None,
                           verified_user=authenticated_user.verified, first_name=authenticated_user.first_name,
                           favorited_theater=authenticated_user.theater_string,
                           is_fav_theater=authenticated_user.favorite_theater_name,
                           current_user=authenticated_user,
                           name=authenticated_user.username,
                           )
