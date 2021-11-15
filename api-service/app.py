from flask import Flask
from flask_restful import Api
from database.db import initialize_db
from resources.routes import initialize_routes
from config import SQLALCHEMY_DATABASE_URI

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

initialize_db(app)
initialize_routes(api)

if __name__ == '__main__':
    app.run(debug=True)
