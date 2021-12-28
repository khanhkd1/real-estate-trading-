from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from database.db import db
from database.models import Post, Image, User, Privilege


class AdminUserApi(Resource):
    @jwt_required()
    def get(self):
        user = db.session.query(User).filter(User.user_id == int(get_jwt_identity())).first()
        if db.session.query(Privilege).filter(Privilege.privilege_id == user.privilege_id).first().name != 'admin':
            return {'error': 'Permission denied'}, 401

        users = db.session.query(User).all()
        for i in range(len(users)):
            users[i] = users[i].as_dict()
        return users, 200
