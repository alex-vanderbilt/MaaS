from flask import Flask
from flask_login import LoginManager
from User.flask_auth import auth as auth_blueprint
from main import main as main_blueprint

# def create_app():
app = Flask(__name__)
login_manager = LoginManager()
app.config['SECRET_KEY'] = 'put super secret passcode here'


app.register_blueprint(auth_blueprint)


app.register_blueprint(main_blueprint)

# return app

if __name__ == '__main__':
    login_manager.init_app(app)
    app.run(debug=True)