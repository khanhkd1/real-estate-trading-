from database.db import db
from database.models import Privilege, Avatar, Post


def process_user(user):
    user = user.as_dict()
    user['privilege'] = str(db.session.query(Privilege).filter(Privilege.privilege_id == user['privilege_id']).one())
    user['avatar'] = str(db.session.query(Avatar).filter(Avatar.avatar_id == user['avatar_id']).one())
    del user['user_id'], user['password'], user['privilege_id'], user['avatar_id']
    return user


def get_default(parameters):
    filters = {}
    order = Post.time_priority
    limit = 20
    if 'page' not in parameters:
        page = 1
    else:
        page = int(parameters['page'])
    offset = (page - 1) * limit

    if 'filter' in parameters and parameters['filter'] != "":
        for filter_ in parameters['filter'].split(','):
            filters[filter_.split(':')[0]] = filter_.split(':')[1]
    if "search" in parameters and parameters['search'] != "":
        search_values = parameters['search'].split(",")
    else:
        search_values = None

    return limit, page, offset, order, search_values, filters
