import os
from flask import Flask, render_template, g, send_from_directory
from flask_restx import Api
from controller.login.controller_login import LOGIN
from controller.user.controller_user import USER


def create_app():
    app = Flask(__name__, static_folder='../web/', template_folder='../web')
    app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)
    api = Api(app)
    api.add_namespace(USER, '/api/user')
    api.add_namespace(LOGIN, '/api/login')

    @app.route('/hello', methods=['GET'])
    def index():
        return 'Hello World!'

    @app.route('/main', methods=['GET'])
    def catch_all():
        g.jinja2_test = 'made by gtttpark!'
        return render_template('index.html')

    return app