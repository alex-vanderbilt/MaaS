from flask import Flask
from flask_login import LoginManager
from AMC.config import database_secret_key
from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()
#
#
# def create_app():
#     app = Flask(__name__)
#     # login_manager = LoginManager()
#
#     app.config['SECRET_KEY'] = database_secret_key
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
#     db.init_app(app)
#     from flask_auth import auth as auth_blueprint
#     app.register_blueprint(auth_blueprint)
#
#     from main import main as main_blueprint
#     app.register_blueprint(main_blueprint)
#
#     return app

db = SQLAlchemy()
app = Flask(__name__)


app.config['SECRET_KEY'] = 'put super secret passcode here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

from models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from flask_auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

from main import main as main_blueprint
app.register_blueprint(main_blueprint)


if __name__ == '__main__':
    login_manager.init_app(app)
    app.run(debug=True)
