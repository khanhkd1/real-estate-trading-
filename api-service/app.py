from flask import Flask
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_cors import CORS
from database.db import initialize_db

app = Flask(__name__)
CORS(app)

app.config.from_pyfile('config.py')

mail = Mail(app)

from resources.routes import initialize_routes_api

api = Api(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

initialize_db(app)
initialize_routes_api(api)
