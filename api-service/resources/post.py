from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from database.db import db
from database.models import Post, Image, User
from flask import request
from sqlalchemy import or_, desc
from config import FORMAT_STRING_DATETIME
from function.function import get_default


class PostsApi(Resource):
    # @jwt_required()
    def get(self):
        limit, page, offset, order, search_values, filters = get_default(request.args)
        posts = db.session.query(Post)

        # filter
        for key in filters.keys():
            if key == 'address':
                posts = posts.filter(Post.address.like(f'%{filters[key].lower()}%'))
            elif key == 'bedroom':
                posts = posts.filter(Post.bedroom == int(filters[key]))
            else:
                posts = posts.filter(Post.toilet == int(filters[key]))

        # search
        if search_values is not None:
            for search_value in search_values:
                posts = posts.filter(or_(key.like('%' + search_value.lower() + '%') for key in Post.__table__.columns))

        total_count = posts.count()
        posts = posts.order_by(desc(order)).offset(offset).limit(limit).all()

        for i in range(len(posts)):
            posts[i] = posts[i].as_dict()

            # images
            images = db.session.query(Image).filter(Image.post_id == posts[i]['post_id']).all()
            posts[i]['images'] = [str(image) for image in images]

            # user
            user = db.session.query(User).filter(User.user_id == posts[i]['user_id']).one()
            posts[i]['user'] = user.fullname

            del posts[i]['user_id'], posts[i]['time_priority'], posts[i]['time_upload'], posts[i]['address'], \
                posts[i]['description'], posts[i]['distance'], posts[i]['longitude'], posts[i]['latitude'], \
                posts[i]['investor'], posts[i]['price']

            # datetime type to string
            # posts[i]['time_upload'] = posts[i]['time_upload'].strftime(FORMAT_STRING_DATETIME)
            # posts[i]['time_priority'] = posts[i]['time_priority'].strftime(FORMAT_STRING_DATETIME)

            # posts[i]['user'] = {
            #     'fullname': user.fullname,
            #     'email': user.email,
            #     'phone': user.phone,
            #     'address': user.address,
            # }

        return {
                   'paging': {
                       'total_count': total_count,
                       'total_page': total_count//limit if total_count % limit == 0 else total_count//limit + 1,
                       'current_page': page
                   },
                   'posts': posts
               }, 200
