import sys
from flask import Flask
sys.path.append("C:/Users/jmsm1/Documents/MaaS/simple-flask-app")
import UserCredentials


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'put super secret passcode here'

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
