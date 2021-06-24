import sys
from flask import Blueprint, render_template, redirect, url_for
from authenticateduser import authenticated_user


main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile/Welcome')
def profile_post():
    username = authenticated_user.first_name + " " + authenticated_user.last_name
    return render_template('profile.html', name=username)


@main.route('/profile')
def profile():
    if authenticated_user.username is None:
        return redirect(url_for('auth.login'))
    else:
        return redirect(url_for('main.profile_post'))
