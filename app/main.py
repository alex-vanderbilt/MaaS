from flask import Blueprint, render_template
from flask_login import login_required
from AMC.AMCRequest import AMCRequest


main = Blueprint('main', __name__)


@main.route('/')
def index():
    requester = AMCRequest()
    current_movie_list = requester.get_current_movies()
    return render_template('index.html', movie_list=current_movie_list)


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', theater_list=None)