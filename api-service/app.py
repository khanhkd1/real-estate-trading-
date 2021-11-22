from flask import Flask
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from database.db import initialize_db

from config import SQLALCHEMY_DATABASE_URI, JWT_SECRET_KEY, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD, MAIL_SERVER, \
    MAIL_USE_TLS

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
app.config['MAIL_SERVER'] = MAIL_SERVER
app.config['MAIL_PORT'] = MAIL_PORT
app.config['MAIL_USE_TLS'] = MAIL_USE_TLS
app.config['MAIL_USERNAME'] = MAIL_USERNAME
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD

mail = Mail(app)
from resources.routes import initialize_routes

api = Api(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

initialize_db(app)
initialize_routes(api)
