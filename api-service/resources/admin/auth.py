from flask import request
from flask_restful import Resource
from database.db import db
from database.models import User, Privilege
from function.function import process_user


class AdminLoginApi(Resource):
    def post(self):
        username = request.form['username']
        password = request.form['password']
        user = db.session.query(User).filter(User.username == username).first()
        if user is None or not user.check_password(password):
            return {'error': 'Username or Password invalid'}, 401

        elif db.session.query(Privilege).filter(Privilege.privilege_id == user.privilege_id).first().name != 'admin':
            return {'error': 'Permission denied'}, 401

        token = user.sign_in()
        user = process_user(user)
        del user['email'], user['fullname'], user['address'], user['phone'], user['verified'], user['privilege']

        return {'token': token,
                'user': user}, 200
