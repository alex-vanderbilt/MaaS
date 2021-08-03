from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User

from User.user_credentials import UserCredentials
from User.user_auth import authenticated_user
import pyotp
from __init__ import db

from AMC.AMC import AMCMovie
from AMC.AMCRequest import AMCRequest

auth = Blueprint('auth', __name__)


@auth.route('/search', methods=['POST'])
def search_zip():
    zip_code = str(request.form.get('zip_code'))
    request_value = str(request.form.get('theaterList'))
    # TODO - Check this input data from the user. Likely use some zip_code library
    requester = AMCRequest()
    if zip_code != "None":
        current_user.last_searched_zip = zip_code
        db.session.commit()
    if zip_code == "None":
        theater_list = requester.get_locations_via_zip(current_user.last_searched_zip)
    else:
        theater_list = requester.get_locations_via_zip(zip_code)
    if request_value != "None":
        i = 1
        for theater in theater_list:
            if i == int(request_value):
                current_user.favorite_theater_id = theater.id
                current_user.favorite_theater_string = theater.name + ", " + theater.street_address + ", " + theater.city + ", " + theater.state + ", " + theater.zip_code
                db.session.commit()
            i += 1
    return render_template('profile.html', theater_list=theater_list)

@auth.route('/update_preferences', methods=['POST'])
def save_preferences():
    day_of_week = str(request.form.get('day_of_week'))
    time_of_day = str(request.form.get('time_of_day'))
    # Because we automatically select "Monday" and "Morning" the form should never return None
    database_credentials = UserCredentials("testDB.db", "user_creds")
    database_credentials.access_database("WOOO!!!!!!!!!!")
    database_credentials.update_notification_day(authenticated_user.username, day_of_week)
    database_credentials.update_time_of_day(authenticated_user.username, time_of_day)
    database_credentials.close_database()
    authenticated_user.set_day_of_week(day_of_week)
    authenticated_user.set_time_of_day(time_of_day)
    zip_code = "None"
    theater_list = None
    return render_template('profile.html', theater_list=theater_list, zip_code=zip_code,
                           verified_user=authenticated_user.verified,
                           first_name=authenticated_user.first_name,
                           favorited_theater=authenticated_user.theater_string,
                           current_user=authenticated_user,
                           is_fav_theater=authenticated_user.favorite_theater_name)

@auth.route('/login', methods=['POST'])
def login_post():
    username = str(request.form.get('name')).lower()
    password = str(request.form.get('password'))
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))  # if the user doesn't exist or password is wrong, reload the page

        # if the above check passes, then we know the user has the right credentials
    else:
        login_user(user, remember=remember)
        return redirect(url_for('main.profile'))

    # database_credentials = UserCredentials("testDB.db", "user_creds")
    # database_credentials.access_database("WOOO!!!!!!!!!!")

    # login_user = database_credentials.authenticate_user(name, password)
    #
    # if login_user:
    #     database_user_information = database_credentials.fetch_entire_table()
    #     for user in database_user_information:
    #         if name == str(user[0]):
    #             authenticated_user.update_user(user[0], user[2], user[3], user[4], user[5], user[6], user[7], user[9],
    #                                            user[11])
    #             authenticated_user.theater_string = database_credentials.fetch_users_favorited_theater(
    #                 authenticated_user.username)
    #             authenticated_user.favorite_theater_name = database_credentials.fetch_user_theater_name(
    #                 authenticated_user.username)
    #             authenticated_user.preferred_day = database_credentials.fetch_desired_notification_day(
    #                 authenticated_user.username)
    #             authenticated_user.preferred_time = database_credentials.fetch_desired_notification_time(
    #                 authenticated_user.username)
    #             database_credentials.close_database()
    #             # if user[10] == "false":
    #             #     return redirect(url_for('auth.two_factor_enroll'))
    #             # else:
    #             #     return redirect(url_for('auth.two_factor_verification'))
    #             return redirect(url_for('main.profile_post', verified_user=authenticated_user.verified,
    #                                     first_name=authenticated_user.first_name,
    #                                     favorited_theater=authenticated_user.theater_string,
    #                                     current_user=authenticated_user,
    #                                     is_fav_theater=authenticated_user.favorite_theater_name,
    #                                     name=authenticated_user.username))
    # else:
    #     # print("here")
    #     database_credentials.close_database()
    #     flash('Please check your login details and try again')
    #     return redirect(url_for('auth.login', verified_user=authenticated_user.verified,
    #                             first_name=authenticated_user.first_name, favorited_theater=authenticated_user.theater_string,
    #                             name=authenticated_user.username))


@auth.route('/login')
def login():
    return render_template('login.html', verified_user=authenticated_user.verified,
                           first_name=authenticated_user.first_name, favorited_theater=authenticated_user.theater_string,
                           name=authenticated_user.username)


@auth.route('/signup')
def signup():
    return render_template('signup.html', verified_user=authenticated_user.verified,
                           first_name=authenticated_user.first_name, favorited_theater=authenticated_user.theater_string,
                           name=authenticated_user.username)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
    # authenticated_user.log_out_user()
    # return redirect(url_for('auth.login', verified_user=authenticated_user.verified,
    #                         first_name=authenticated_user.first_name, favorited_theater=authenticated_user.theater_string,
    #                         name=authenticated_user.username))


@auth.route('/signup', methods=['POST'])
def signup_post():
    email = str(request.form.get('email'))
    username = str(request.form.get('name')).lower()
    password = str(request.form.get('password'))
    first_name = str(request.form.get('firstName'))
    last_name = str(request.form.get('lastName'))
    phone_num = str(request.form.get('phoneNumber'))
    comm_preference = str(request.form.get('commMethod'))
    fav_genre = str(request.form.get('genre'))

    user = User.query.filter_by(username=username).first()

    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    new_user = User(email=email,
                    username=username,
                    password=generate_password_hash(password, method='sha256'),
                    first_name=first_name,
                    last_name=last_name,
                    phone=phone_num,
                    comm_preference=comm_preference,
                    fav_genre=fav_genre,
                    last_searched_zip="None",
                    favorite_theater_id="None",
                    favorite_theater_string="None",
                    preferred_time="None",
                    preferred_day="None")
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))
    # database_credentials = UserCredentials("testDB.db", "user_creds")
    # database_credentials.access_database("WOOO!!!!!!!!!!")

    # key_in_database = database_credentials.fetch_table_column("login_username")

    # for entry in key_in_database:
    #     if entry == name:
    #         flash('Username is already in use')
    #         print('Username is already in use')
    #         return redirect(url_for('auth.signup', verified_user=authenticated_user.verified,
    #                                 first_name=authenticated_user.first_name, favorited_theater=authenticated_user.theater_string,
    #                                 name=authenticated_user.username))
    #
    # hashed_password = generate_password_hash(password)
    # database_credentials.populate_table(name, hashed_password, email, first_name, last_name, phone_number, zipcode,
    #                                     preferred_comm, favorite_theater, favorite_genre)
    # database_credentials.commit_changes()
    # database_credentials.close_database()
    # test_print = database_credentials.fetch_entire_table()
    # print(test_print)

    # return redirect(url_for('auth.login', verified_user=authenticated_user.verified,
    #                         first_name=authenticated_user.first_name, favorited_theater=authenticated_user.theater_string,
    #                         name=authenticated_user.username))


# @auth.route('/2FA/Enrollment', methods=['Get', 'POST'])
# def two_factor_enroll():
#     database_credentials = UserCredentials("testDB.db", "user_creds")
#     database_credentials.access_database("WOOO!!!!!!!!!!")
#
#     if request.method == 'POST':
#         # print("here")
#         otp = int(request.form.get("otp"))
#         if pyotp.TOTP(authenticated_user.secret_key).verify(otp):
#             database_credentials.update_user_enrollment(authenticated_user.username)
#             database_credentials.commit_changes()
#             database_credentials.close_database()
#             flash("You have successfully enrolled 2FA for your profile, please authenticate yourself once more!",
#                   "success")
#             return redirect(url_for('auth.two_factor_verification'))
#         else:
#             database_credentials.close_database()
#             flash("The OTP provided is invalid, it has either expired or was generated using a wrong SECRET!", "danger")
#             return redirect(url_for('auth.two_factor_enroll'))
#
#     return render_template('2faenroll.html', secret=authenticated_user.secret_key, favorited_theater=authenticated_user.theater_string,
#                            name=authenticated_user.username)
#
#
# @auth.route('/2FA/Verification', methods=['Get', 'POST'])
# def two_factor_verification():
#     if request.method == "POST":
#         otp = int(request.form.get("otp"))
#
#         if pyotp.TOTP(authenticated_user.secret_key).verify(otp):
#             authenticated_user.user_authenticated()
#             return redirect(url_for('main.profile_post', verified_user=authenticated_user.verified,
#                                     first_name=authenticated_user.first_name, favorited_theater=authenticated_user.theater_string,
#                                     current_user=authenticated_user,
#                                     is_fav_theater=authenticated_user.favorite_theater_name,
#                                     name=authenticated_user.username))
#         else:
#             flash("The OTP provided is invalid, it has either expired or was generated using a wrong SECRET!", "danger")
#             return redirect(url_for('auth.two_factor_verification'))
#
#     return render_template('2faverify.html')
