from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.db import db
from database.models import User, Post, Privilege


class DashBoard(Resource):
    @jwt_required()
    def get(self):
        user_id = int(get_jwt_identity())
        user = db.session.query(User).filter(User.user_id == user_id).first()
        if db.session.query(Privilege).filter(Privilege.privilege_id == user.privilege_id).first().name != 'admin':
            return {'error': 'Permission denied'}, 401

        return {
            'number_users': db.session.query(User).count(),
            'number_posts': db.session.query(Post).count()
        }, 200
