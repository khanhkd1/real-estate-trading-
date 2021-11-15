from flask import Flask
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

from database.db import initialize_db
from resources.routes import initialize_routes
from config import SQLALCHEMY_DATABASE_URI, JWT_SECRET_KEY

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
api = Api(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

initialize_db(app)
initialize_routes(api)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
