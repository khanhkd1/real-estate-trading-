from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from database.db import db
from database.models import User, Privilege


class AdminUsersApi(Resource):
    @jwt_required()
    def get(self):
        if not check_admin():
            return {'error': 'Permission denied'}, 401
        users = db.session.query(User).all()
        for i in range(len(users)):
            users[i] = users[i].as_dict()
        return users, 200


class AdminUserApi(Resource):
    @jwt_required()
    def delete(self, user_id):
        if not check_admin():
            return {'error': 'Permission denied'}, 401
        db.session.query(User).filter(User.user_id == user_id).delete()
        db.session.commit()
        return {'msg': 'done'}, 200


def check_admin():
    admin = db.session.query(User).filter(User.user_id == int(get_jwt_identity())).first()
    if db.session.query(Privilege).filter(Privilege.privilege_id == admin.privilege_id).first().name != 'admin':
        return False
    return True
