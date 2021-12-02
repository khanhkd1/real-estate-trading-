from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from database.db import db
from database.models import Post, User
from .post import post_process


class FollowsApi(Resource):
    @jwt_required()
    def get(self):
        user_id = int(get_jwt_identity())
        user = db.session.query(User).filter(User.user_id == user_id).first()
        followed_posts = []
        if user is not None:
            for i in range(len(user.followed_posts)):
                post = post_process(post_process(user.followed_posts[i]), True)
                del post['time_upload'], post['address'], post['description'], post['longitude'], post['latitude'], \
                    post['investor'], post['price'], post['user']['email'], post['user']['phone'], \
                    post['user']['address'], post['user_id'], post['time_priority']
                followed_posts.append(post)
            return {'followed_posts': followed_posts}, 200
        return {'error': 'user not found'}, 401


class FollowApi(Resource):
    @jwt_required()
    def post(self, post_id):
        user_id = int(get_jwt_identity())
        user = db.session.query(User).filter(User.user_id == user_id).first()
        post = db.session.query(Post).filter(Post.post_id == post_id).first()
        if user is not None and post is not None:
            user.posts.append(post)
            db.session.commit()
            return {'msg': 'done'}, 200
        return {'error': 'add post to followed list fail'}, 400

    @jwt_required()
    def delete(self, post_id):
        user_id = int(get_jwt_identity())
        user = db.session.query(User).filter(User.user_id == user_id).first()
        post = db.session.query(Post).filter(Post.post_id == post_id).first()
        if user is not None and post is not None:
            if post in user.posts:
                user.posts.remove(post)
                db.session.commit()
                return {'msg': 'done'}, 200
            return {'error': 'post not in followed list'}, 400
        return {'error': 'post not exist'}, 400
