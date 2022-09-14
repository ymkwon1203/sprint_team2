import os
from flask import Flask
from flask_restx import Api
from controller.login.controller_login import LOGIN
from controller.user.controller_user import USER


def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)
    api = Api(app)
    api.add_namespace(USER, '/api/user')
    api.add_namespace(LOGIN, '/api/login')

    @app.route('/hello', methods=['GET'])
    def index():
        return 'Hello World!'

    return app