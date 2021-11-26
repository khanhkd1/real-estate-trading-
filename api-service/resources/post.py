from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from database.db import db
from database.models import Post, Image, User
from flask import request
from sqlalchemy import or_, desc
from config import FORMAT_STRING_DATETIME
from function.function import get_default


class PostsApi(Resource):
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
            posts[i] = post_process(posts[i])

            del posts[i]['time_upload'], posts[i]['address'], posts[i]['description'], posts[i]['distance'], \
                posts[i]['longitude'], posts[i]['latitude'], posts[i]['investor'], posts[i]['price'], \
                posts[i]['user']['email'], posts[i]['user']['phone'], posts[i]['user']['address'], \
                posts[i]['user_id'], posts[i]['time_priority']

        return {
                   'paging': {
                       'total_count': total_count,
                       'total_page': total_count // limit if total_count % limit == 0 else total_count // limit + 1,
                       'current_page': page
                   },
                   'posts': posts
               }, 200

    @jwt_required()
    def post(self):
        user_id = int(get_jwt_identity())
        data = request.get_json()
        pass


class PostApi(Resource):
    @jwt_required()
    def get(self, post_id):
        post = db.session.query(Post).filter(Post.post_id == post_id).first()
        if post is None:
            return {'error': 'post_id not found'}, 400
        post = post_process(post)
        del post['user_id'], post['time_priority']
        return post, 200

    @jwt_required()
    def put(self, post_id):
        status, msg, code = get_post_check_user(post_id)
        if not status:
            return msg, code

        data = request.get_json()
        for col in ['user_id', 'post_id', 'time_priority', 'time_upload']:
            if col in data.keys():
                del data[col]

        db.session.query(Post).filter(Post.post_id == post_id).update(data)
        db.session.commit()

        post = post_process(db.session.query(Post).filter(Post.post_id == post_id).first())
        del post['user_id'], post['time_priority']
        return post, 200

    @jwt_required()
    def delete(self, post_id):
        status, msg, code = get_post_check_user(post_id)
        if not status:
            return msg, code

        db.session.query(Post).filter(Post.post_id == post_id).delete()
        db.session.commit()
        return {'msg': 'done'}, 200


def get_post_check_user(post_id):
    user_id = int(get_jwt_identity())
    post = db.session.query(Post).filter(Post.post_id == post_id).first()
    if post is None:
        return False, {'error': 'post_id not found'}, 400

    post = post_process(post)
    if user_id != post['user_id']:
        return False, {'error': 'user have no permission'}, 401
    return True, None, None


def post_process(post):
    post = post.as_dict()

    # image
    images = db.session.query(Image).filter(Image.post_id == post['post_id']).all()
    post['images'] = [str(image) for image in images]

    # user
    user = db.session.query(User).filter(User.user_id == post['user_id']).one()
    post['user'] = {
        'fullname': user.fullname,
        'email': user.email,
        'phone': user.phone,
        'address': user.address,
    }

    # datetime type to string
    post['time_upload'] = post['time_upload'].strftime(FORMAT_STRING_DATETIME)
    post['time_priority'] = post['time_priority'].strftime(FORMAT_STRING_DATETIME)

    return post
