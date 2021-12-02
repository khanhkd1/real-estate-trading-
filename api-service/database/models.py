from flask_bcrypt import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token
import datetime
from .db import db


class Privilege(db.Model):
    __tablename__ = 'privilege'
    privilege_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def __repr__(self):
        return self.name


follow_table = db.Table('follow',
                        db.Column('user_id', db.Integer, db.ForeignKey('user.user_id'), primary_key=True),
                        db.Column('post_id', db.Integer, db.ForeignKey('post.post_id'), primary_key=True)
                        )


class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True)
    fullname = db.Column(db.String)
    address = db.Column(db.String)
    phone = db.Column(db.String)
    privilege_id = db.Column(db.Integer, db.ForeignKey('privilege.privilege_id'), primary_key=True)
    avatar = db.Column(db.String)
    verified = db.Column(db.Boolean)

    followed_posts = db.relationship('Post', secondary=follow_table, back_populates='users')

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def sign_up(self):
        self.hash_password()
        db.session.add(self)
        try:
            db.session.commit()
            return True
        except IntegrityError:
            db.session.rollback()
            return False

    def sign_in(self):
        expires = datetime.timedelta(days=7)
        return create_access_token(identity=str(self.user_id), expires_delta=expires)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Post(db.Model):
    __tablename__ = 'post'
    post_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    title = db.Column(db.String)
    address = db.Column(db.String)
    price = db.Column(db.Float)
    acreage = db.Column(db.Float)
    investor = db.Column(db.String)
    bedroom = db.Column(db.Integer)
    toilet = db.Column(db.Integer)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    time_upload = db.Column(db.DateTime)
    time_priority = db.Column(db.DateTime)
    sold = db.Column(db.Boolean)
    description = db.Column(db.String)

    users = db.relationship('User', secondary=follow_table, back_populates='followed_posts')

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Image(db.Model):
    __tablename__ = 'image'
    image_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id'))
    image_url = db.Column(db.String)

    def __repr__(self):
        return self.image_url
