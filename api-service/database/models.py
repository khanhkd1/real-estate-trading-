from .db import db
from flask_bcrypt import generate_password_hash, check_password_hash


class Privilege(db.Model):
    __tablename__ = 'privilege'
    privilege_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)


class Avatar(db.Model):
    __tablename__ = 'avatar'
    avatar_id = db.Column(db.Integer, primary_key=True)
    avatar_url = db.Column(db.String)

    def __repr__(self):
        return self.avatar_url


class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True)
    fullname = db.Column(db.String)
    address = db.Column(db.String)
    phone = db.Column(db.String)
    privilege_id = db.Column(db.Integer, db.ForeignKey('privilege.privilege_id'), primary_key=True)
    avatar_id = db.Column(db.Integer, db.ForeignKey('avatar.avatar_id'), primary_key=True)
    verified = db.Column(db.Boolean)

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def sign_up(self):
        self.hash_password()
        db.session.add(self)
        db.session.commit()
        return self

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Otp(db.Model):
    __tablename__ = 'otp'
    otp_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    otp = db.Column(db.String)
    validate = db.Column(db.DateTime)


class Post(db.Model):
    __tablename__ = 'post'
    post_id = db.Column(db.Integer, primary_key=True)
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
    distance = db.Column(db.Float)
    time_upload = db.Column(db.DateTime)
    time_priority = db.Column(db.DateTime)
    sold = db.Column(db.Boolean)
    description = db.Column(db.String)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Image(db.Model):
    __tablename__ = 'image'
    image_id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post_id'))
    image_url = db.Column(db.String)

    def __repr__(self):
        return self.image_url
