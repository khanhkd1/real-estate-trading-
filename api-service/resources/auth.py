from flask import request
from database.models import User
from flask_restful import Resource


class SignupApi(Resource):
    def post(self):
        body = request.get_json()
        user = User(
            username=body['username'],
            password=body['password'],
            email=None,
            fullname=None,
            address=None,
            phone=None,
            privilege_id=2,
            avatar_id=1,
            verified=False,
        )
        user.sign_up()
        return 'ok'
