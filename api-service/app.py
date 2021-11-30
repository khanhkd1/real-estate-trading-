from flask import Flask
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from database.db import initialize_db, db
from database.models import User, Post, Image

app = Flask(__name__)

app.config.from_pyfile('config.py')

admin = Admin(app)
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Post, db.session))
admin.add_view(ModelView(Image, db.session))

mail = Mail(app)

from resources.routes import initialize_routes_api

api = Api(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

initialize_db(app)
initialize_routes_api(api)
