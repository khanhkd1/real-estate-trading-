from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from database.db import db
from database.models import Post, Image, User, Privilege
from flask import request
from sqlalchemy import or_, desc
import datetime
from config import FORMAT_STRING_DATETIME
from function.function import get_default
import math
import numpy as np
from run import bayesian_ridge_model, address_encode, investor_encode


class PostsApi(Resource):
    def get(self):
        posts = db.session.query(Post)
        return query_posts(posts)


class PostApi(Resource):
    @jwt_required()
    def get(self, post_id):
        user_id = int(get_jwt_identity())
        return get_post_by_id(user_id, post_id)

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
        return {
                   'msg': 'Update successfully',
                   'post': post
               }, 200

    @jwt_required()
    def delete(self, post_id):
        status, msg, code = get_post_check_user(post_id)
        if not status:
            return msg, code

        db.session.query(Post).filter(Post.post_id == post_id).delete()
        db.session.commit()
        return {'msg': 'done'}, 200


class PostsUserApi(Resource):
    @jwt_required()
    def get(self):
        user_id = int(get_jwt_identity())
        posts = db.session.query(Post).filter(Post.user_id == user_id)
        return query_posts(posts)

    @jwt_required()
    def post(self):
        user_id = int(get_jwt_identity())
        data = request.form.to_dict()
        post = Post(
            user_id=user_id,
            title=data['title'],
            address=data['address'],
            bedroom=data['bedroom'],
            toilet=data['toilet'],
            investor=data['investor'],
            acreage=data['acreage'],
            price=data['price'],
            latitude=data['latitude'],
            longitude=data['longitude'],
            sold=False,
            time_upload=datetime.datetime.now(),
            time_priority=datetime.datetime.now(),
            description=data['description']
        )
        db.session.add(post)
        db.session.flush()

        post_id = post.post_id
        db.session.commit()

        for image_url in data['images']:
            image = Image(
                post_id=post_id,
                image_url=image_url
            )
            db.session.add(image)
        db.session.commit()

        return get_post_by_id(user_id, post_id)


class PredictPrice(Resource):
    @jwt_required()
    def post(self):
        data = request.form.to_dict()
        for col in ['address', 'bedroom', 'toilet', 'investor', 'acreage', 'lat', 'long']:
            if col not in data:
                return {'error': 'not enough columns'}, 400
        return bayesian_ridge_model.predict(np.array([[
            address_encode.transform([data['address']])[0],
            int(data['bedroom']), int(data['toilet']),
            investor_encode.transform([data['investor']])[0],
            float(data['acreage']), float(data['lat']), float(data['long']),
            distance_to_center([float(data['lat']), float(data['long'])])
        ]]).reshape(1, -1))[0]


def distance_to_center(location):
    center = list(map(lambda x: math.radians(x), [21.028889, 105.8525]))
    location = list(map(lambda x: math.radians(x), location))
    return 6378 * math.acos((math.sin(location[0]) * math.sin(center[0]))
                            + (math.cos(location[0]) * math.cos(center[0]) * math.cos(center[1] - location[1])))


def query_posts(posts):
    limit, page, offset, order, search_values, filters = get_default(request.args)
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

        del posts[i]['time_upload'], posts[i]['address'], posts[i]['description'], posts[i]['longitude'], \
            posts[i]['latitude'], posts[i]['investor'], posts[i]['price'], posts[i]['user']['email'], \
            posts[i]['user']['phone'], posts[i]['user']['address'], posts[i]['user_id'], posts[i]['time_priority']

    return {
               'paging': {
                   'total_count': total_count,
                   'total_page': total_count // limit if total_count % limit == 0 else total_count // limit + 1,
                   'current_page': page
               },
               'posts': posts
           }, 200


def get_post_check_user(post_id):
    user_id = int(get_jwt_identity())
    post = db.session.query(Post).filter(Post.post_id == post_id).first()
    if post is None:
        return False, {'error': 'post_id not found'}, 400

    post = post_process(post)
    user = db.session.query(User).filter(User.user_id == user_id).one()
    if user_id != post['user_id'] and db.session.query(Privilege).filter(
            Privilege.privilege_id == user.privilege_id).first().name != 'admin':
        return False, {'error': 'user have no permission'}, 401
    return True, None, None


def post_process(post, followed=False):
    if not followed:
        post = post.as_dict()

        # datetime type to string
        post['time_upload'] = post['time_upload'].strftime(FORMAT_STRING_DATETIME)
        post['time_priority'] = post['time_priority'].strftime(FORMAT_STRING_DATETIME)

    post['title'] = post['title'].strip().title()

    # image
    images = db.session.query(Image).filter(Image.post_id == post['post_id']).all()
    post['images'] = [str(image) for image in images]

    if not post['images']:
        post['images'].append('https://i.imgur.com/RYKgdEW.png')

    # user
    user = db.session.query(User).filter(User.user_id == post['user_id']).one()
    post['user'] = {
        'fullname': user.fullname,
        'avatar': user.avatar,
        'email': user.email,
        'phone': user.phone,
        'address': user.address,
    }

    return post


def get_post_by_id(user_id, post_id):
    post = db.session.query(Post).filter(Post.post_id == post_id).first()
    user = db.session.query(User).filter(User.user_id == user_id).first()
    if post is None or user is None:
        return {'error': 'query error'}, 400
    post_tmp = post_process(post)
    del post_tmp['user_id'], post_tmp['time_priority']

    if post in user.followed_posts:
        post_tmp['followed'] = True
    else:
        post_tmp['followed'] = False
    return post_tmp, 200
