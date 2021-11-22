from database.db import db
from database.models import Privilege, Avatar


def process_user(user):
    user = user.as_dict()
    user['privilege'] = str(db.session.query(Privilege).filter(Privilege.privilege_id == user['privilege_id']).one())
    user['avatar'] = str(db.session.query(Avatar).filter(Avatar.avatar_id == user['avatar_id']).one())
    del user['user_id'], user['password'], user['privilege_id'], user['avatar_id']
    return user
