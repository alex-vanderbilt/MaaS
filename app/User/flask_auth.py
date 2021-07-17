import string

from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash

from .user_credentials import UserCredentials
from .user_auth import authenticated_user
import pyotp

from AMC.AMC import AMCMovie
from AMC.AMCRequest import AMCRequest

auth = Blueprint('auth', __name__)


@auth.route('/search', methods=['POST'])
def search_zip():
    zip_code = str(request.form.get('zip_code'))
    request_value = str(request.form.get('theaterList'))
    # print(request_value)
    # print(zip_code)
    # TODO - Check this input data from the user. Likely use some zip_code library
    username = authenticated_user.first_name + " " + authenticated_user.last_name
    requester = AMCRequest()
    if zip_code != "None":
        authenticated_user.update_last_zipcode(zip_code)
    if zip_code == "None":
        theater_list = requester.get_locations_via_zip(authenticated_user.last_searched_zipcode)
    else:
        theater_list = requester.get_locations_via_zip(zip_code)
    current_movie_list = requester.get_current_movies()
    if request_value != "None":
        i = 1
        for theater in theater_list:
            if i == int(request_value):
                authenticated_user.set_favorited_theater(theater)
            i += 1
    if authenticated_user.favorite_theater != "None":
        theater_string = authenticated_user.favorite_theater.name + ", " + authenticated_user.favorite_theater.street_address + ", " + authenticated_user.favorite_theater.city + ", " + authenticated_user.favorite_theater.state + ", " + authenticated_user.favorite_theater.zip_code
        authenticated_user.set_theater_information(theater_string)
        database_credentials = UserCredentials("testDB.db", "user_creds")
        database_credentials.access_database("WOOO!!!!!!!!!!")
        database_credentials.update_user_favorite_theater(authenticated_user.username, theater_string)
        authenticated_user.favorite_theater_name = authenticated_user.favorite_theater.name
    return render_template('profile.html', name=username, theater_list=theater_list, zip_code=zip_code,
                           movie_list=current_movie_list,
                           verified_user=authenticated_user.verified,
                           first_name=authenticated_user.first_name, favorited_theater=authenticated_user.theater_string,
                           current_user=authenticated_user,
                           is_fav_theater=authenticated_user.favorite_theater_name)

@auth.route('/login', methods=['POST'])
def login_post():
    name = str(request.form.get('name')).lower()
    password = str(request.form.get('password'))

    database_credentials = UserCredentials("testDB.db", "user_creds")
    database_credentials.access_database("WOOO!!!!!!!!!!")

    login_user = database_credentials.authenticate_user(name, password)

    if login_user:
        database_user_information = database_credentials.fetch_entire_table()
        for user in database_user_information:
            if name == str(user[0]):
                authenticated_user.update_user(user[0], user[2], user[3], user[4], user[5], user[6], user[7], user[9],
                                               user[11])
                authenticated_user.theater_string = database_credentials.fetch_users_favorited_theater(
                    authenticated_user.username)
                authenticated_user.favorite_theater_name = database_credentials.fetch_user_theater_name(
                    authenticated_user.username)
                # if user[10] == "false":
                #     return redirect(url_for('auth.two_factor_enroll'))
                # else:
                #     return redirect(url_for('auth.two_factor_verification'))
                return redirect(url_for('main.profile_post', verified_user=authenticated_user.verified,
                                        first_name=authenticated_user.first_name,
                                        favorited_theater=authenticated_user.theater_string,
                                        current_user=authenticated_user,
                                        is_fav_theater=authenticated_user.favorite_theater_name,
                                        name=authenticated_user.username))
    else:
        # print("here")
        flash('Please check your login details and try again')
        return redirect(url_for('auth.login', verified_user=authenticated_user.verified,
                                first_name=authenticated_user.first_name, favorited_theater=authenticated_user.theater_string,
                                name=authenticated_user.username))


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
    authenticated_user.log_out_user()
    return redirect(url_for('auth.login', verified_user=authenticated_user.verified,
                            first_name=authenticated_user.first_name, favorited_theater=authenticated_user.theater_string,
                            name=authenticated_user.username))


@auth.route('/signup', methods=['POST'])
def signup_post():
    email = str(request.form.get('email'))
    name = str(request.form.get('name')).lower()
    password = str(request.form.get('password'))
    first_name = str(request.form.get('firstName'))
    last_name = str(request.form.get('lastName'))
    phone_number = str(request.form.get('phoneNumber'))
    zipcode = str(request.form.get('zipcode'))
    preferred_comm = str(request.form.get('commMethod'))
    favorite_theater = "AMC"
    favorite_genre = str(request.form.get('genre'))

    database_credentials = UserCredentials("testDB.db", "user_creds")
    database_credentials.access_database("WOOO!!!!!!!!!!")

    key_in_database = database_credentials.fetch_table_column("login_username")

    for entry in key_in_database:
        if entry == name:
            flash('Username is already in use')
            print('Username is already in use')
            return redirect(url_for('auth.signup', verified_user=authenticated_user.verified,
                                    first_name=authenticated_user.first_name, favorited_theater=authenticated_user.theater_string,
                                    name=authenticated_user.username))

    hashed_password = generate_password_hash(password)
    database_credentials.populate_table(name, hashed_password, email, first_name, last_name, phone_number, zipcode,
                                        preferred_comm, favorite_theater, favorite_genre)
    database_credentials.commit_changes()
    # test_print = database_credentials.fetch_entire_table()
    # print(test_print)

    return redirect(url_for('auth.login', verified_user=authenticated_user.verified,
                            first_name=authenticated_user.first_name, favorited_theater=authenticated_user.theater_string,
                            name=authenticated_user.username))


@auth.route('/2FA/Enrollment', methods=['Get', 'POST'])
def two_factor_enroll():
    database_credentials = UserCredentials("testDB.db", "user_creds")
    database_credentials.access_database("WOOO!!!!!!!!!!")

    if request.method == 'POST':
        # print("here")
        otp = int(request.form.get("otp"))
        if pyotp.TOTP(authenticated_user.secret_key).verify(otp):
            database_credentials.update_user_enrollment(authenticated_user.username)
            database_credentials.commit_changes()
            flash("You have successfully enrolled 2FA for your profile, please authenticate yourself once more!",
                  "success")
            return redirect(url_for('auth.two_factor_verification'))
        else:
            flash("The OTP provided is invalid, it has either expired or was generated using a wrong SECRET!", "danger")
            return redirect(url_for('auth.two_factor_enroll'))

    return render_template('2faenroll.html', secret=authenticated_user.secret_key, favorited_theater=authenticated_user.theater_string,
                           name=authenticated_user.username)


@auth.route('/2FA/Verification', methods=['Get', 'POST'])
def two_factor_verification():
    if request.method == "POST":
        otp = int(request.form.get("otp"))

        if pyotp.TOTP(authenticated_user.secret_key).verify(otp):
            authenticated_user.user_authenticated()
            return redirect(url_for('main.profile_post', verified_user=authenticated_user.verified,
                                    first_name=authenticated_user.first_name, favorited_theater=authenticated_user.theater_string,
                                    current_user=authenticated_user,
                                    is_fav_theater=authenticated_user.favorite_theater_name,
                                    name=authenticated_user.username))
        else:
            flash("The OTP provided is invalid, it has either expired or was generated using a wrong SECRET!", "danger")
            return redirect(url_for('auth.two_factor_verification'))

    return render_template('2faverify.html')
