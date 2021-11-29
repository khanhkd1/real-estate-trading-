from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from flask import request
from flask_bcrypt import generate_password_hash
from database.db import db
from database.models import User
from function.function import process_user


class UserApi(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = db.session.query(User).filter(User.user_id == user_id).first()
        if user is None:
            return {'error': 'user not found'}, 400
        return process_user(user), 200

    @jwt_required()
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
            for col in ['user_id', 'username', 'privilege_id', 'verified', 'current_password', 'new_password']:
                if col in body.keys():
                    del body[col]
            if 'email' in body.keys():
                user = db.session.query(User).filter(User.email == body.get('email')).first()
                if user:
                    return {
                        'error': 'email has been used for another account'
                    }, 400
            db.session.query(User).filter(User.user_id == user_id).update(body)
        db.session.commit()
        user = db.session.query(User).filter(User.user_id == user_id).first()

        if user.email is not None and user.fullname is not None and user.phone is not None:
            db.session.query(User).filter(User.user_id == user_id).update({'verified': True})
        else:
            db.session.query(User).filter(User.user_id == user_id).update({'verified': False})
        db.session.commit()

        user = db.session.query(User).filter(User.user_id == user_id).first()
        return {
            'msg': 'Update successfully',
            'user': process_user(user)
        }, 200

    @jwt_required()
    def delete(self):
        user_id = get_jwt_identity()
        password = request.get_json().get('password')
        user = db.session.query(User).filter(User.user_id == user_id).first()
        if user is None:
            return {'error': 'user not found'}, 400

        if user.check_password(password):
            db.session.query(User).filter(User.user_id == user_id).delete()
            db.session.commit()
            return {'msg': 'Account was deleted'}, 200
        return {'error': 'Password invalid'}, 401
