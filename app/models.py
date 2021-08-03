from flask_login import UserMixin
from __init__ import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    username = db.Column(db.String(1000), unique=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    comm_preference = db.Column(db.String(100))
    fav_genre = db.Column(db.String(100))
    last_searched_zip = db.Column(db.String(100))
    favorite_theater = db.Column(db.String(100))
    preferred_time = db.Column(db.String(100))
    preferred_day = db.Column(db.String(100))

