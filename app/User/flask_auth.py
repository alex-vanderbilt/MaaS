from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash

from .user_credentials import UserCredentials
from .user_auth import authenticated_user
import pyotp

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
def login_post():
    name = str(request.form.get('name'))
    password = str(request.form.get('password'))

    database_credentials = UserCredentials("testDB.db", "user_creds")
    database_credentials.access_database("WOOO!!!!!!!!!!")

    login_user = database_credentials.authenticate_user(name, password)

    if login_user:
        database_user_information = database_credentials.fetch_entire_table()
        for user in database_user_information:
            if name == str(user[0]):
                authenticated_user.update_user(user[0], user[2], user[3], user[4], user[5], user[6], user[8], user[10])
                # return redirect(url_for('main.profile_post', verified_user=authenticated_user.verified,
                #                         first_name=authenticated_user.first_name))
                # print(user[10])
                if user[9] == "false":
                    return redirect(url_for('auth.two_factor_enroll'))
                else:
                    return redirect(url_for('auth.two_factor_verification'))
    else:
        # print("here")
        flash('Please check your login details and try again')
        return redirect(url_for('auth.login', verified_user=authenticated_user.verified,
                                first_name=authenticated_user.first_name))


@auth.route('/login')
def login():
    return render_template('login.html', verified_user=authenticated_user.verified,
                           first_name=authenticated_user.first_name)


@auth.route('/signup')
def signup():
    return render_template('signup.html', verified_user=authenticated_user.verified,
                           first_name=authenticated_user.first_name)


@auth.route('/logout')
def logout():
    authenticated_user.log_out_user()
    return redirect(url_for('auth.login', verified_user=authenticated_user.verified,
                            first_name=authenticated_user.first_name))


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

    database_credentials = UserCredentials("testDB.db", "user_creds")
    database_credentials.access_database("WOOO!!!!!!!!!!")

    key_in_database = database_credentials.fetch_table_column("login_username")

    for entry in key_in_database:
        if entry == name:
            flash('Username is already in use')
            print('Username is already in use')
            return redirect(url_for('auth.signup', verified_user=authenticated_user.verified,
                                    first_name=authenticated_user.first_name))

    hashed_password = generate_password_hash(password)
    database_credentials.populate_table(name, hashed_password, email, first_name, last_name, phone_number,
                                        preferred_comm, favorite_theater, favorite_genre)
    database_credentials.commit_changes()
    # test_print = database_credentials.fetch_entire_table()
    # print(test_print)

    return redirect(url_for('auth.login', verified_user=authenticated_user.verified,
                            first_name=authenticated_user.first_name))


@auth.route('/2FA/Enrollment', methods=['Get', 'POST'])
def two_factor_enroll():
    database_credentials = UserCredentials("testDB.db", "user_creds")
    database_credentials.access_database("WOOO!!!!!!!!!!")

    if request.method == 'POST':
        print("here")
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

    return render_template('2faenroll.html', secret=authenticated_user.secret_key)


@auth.route('/2FA/Verification', methods=['Get', 'POST'])
def two_factor_verification():
    if request.method == "POST":
        otp = int(request.form.get("otp"))

        if pyotp.TOTP(authenticated_user.secret_key).verify(otp):
            return redirect(url_for('main.profile_post', verified_user=authenticated_user.verified,
                                    first_name=authenticated_user.first_name))
        else:
            flash("The OTP provided is invalid, it has either expired or was generated using a wrong SECRET!", "danger")
            return redirect(url_for('auth.two_factor_verification'))

    return render_template('2faverify.html')
