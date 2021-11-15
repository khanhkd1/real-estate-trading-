from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from flask import request
from flask_bcrypt import generate_password_hash
from database.db import db
from database.models import User
from function.function import process_user


class UserApi(Resource):
    @jwt_required
    def put(self):
        user_id = get_jwt_identity()
        body = request.get_json()
        user = db.session.query(User).filter(User.user_id == user_id).first()

        # change password
        if 'current_password' in body and 'new_password' in body:
            if user.check_password(body['current_password']):
                db.session.query(User).filter(User.user_id == user_id).update({
                    'password': generate_password_hash(body['new_password'])
                })
            else:
                return {'error': 'Password invalid'}, 401
        # change another info
        else:
            db.session.query(User).filter(User.user_id == user_id).update(body)
        db.session.commit()
        user = db.session.query(User).filter(User.user_id == user_id).first()
        return {
            'user': process_user(user)
        }, 200
