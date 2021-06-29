import sys
from flask import Flask
from AMC.config import api_secret

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = api_secret

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
