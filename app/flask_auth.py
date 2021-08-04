from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from __init__ import db
from AMC.AMCRequest import AMCRequest

auth = Blueprint('auth', __name__)


@auth.route('/search', methods=['POST'])
def search_zip():
    zip_code = str(request.form.get('zip_code'))
    request_value = str(request.form.get('theaterList'))
    # TODO - Check this input data from the user. Likely use some zip_code library
    requester = AMCRequest()
    theater_list = None
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
    current_user.preferred_time = time_of_day
    current_user.preferred_day = day_of_week
    db.session.commit()
    return render_template('profile.html', theater_list=None)


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


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


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
        flash('Username already exists')
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
    # login_user(new_user, remember=False)
    db.session.commit()

    # return render_template('phoneVerify.html')
    return redirect(url_for('auth.login'))


# @auth.route('/verify', methods=['POST'])
# def verify_phone():
#     verificationNum = str(request.form.get('verificationNum'))
#
#     print('verification num:' + verificationNum)
#     phone = current_user.phone
#     print('User phone: ' + str(phone))
#
#     # return redirect(url_for('auth.login'))