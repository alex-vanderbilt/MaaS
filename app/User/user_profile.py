from flask import Blueprint, render_template, redirect, url_for, request, flash

from AMC.AMC import AMCMovie
from AMC.AMCRequest import AMCRequest

from .user_credentials import UserCredentials
from .user_auth import authenticated_user

user_profile = Blueprint('user_profile', __name__)


# @user_profile.route('/search', methods=['POST'])
# def search_zip():
#     zip_code = str(request.form.get('zip_code'))
#     print(zip_code)
#
#     username = authenticated_user.first_name + " " + authenticated_user.last_name
#     requester = AMCRequest()
#     theater_list = requester.get_locations_via_zip(zip_code)
#     current_movie_list = requester.get_current_movies()
#     return render_template('profile.html', name=username, theater_list=theater_list, movie_list=current_movie_list,
#                            verified_user=authenticated_user.verified,
#                            first_name=authenticated_user.first_name)
