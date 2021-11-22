from flask import request, render_template
from flask_jwt_extended import create_access_token, decode_token
from database.models import User
from flask_restful import Resource
import datetime
from jwt.exceptions import ExpiredSignatureError, DecodeError, InvalidTokenError
from services.mail_service import send_email
from database.db import db


class ForgotPassword(Resource):
    def post(self):
        url = request.host_url + 'reset/'
        body = request.get_json()
        email = body.get('email')
        user = db.session.query(User).filter(User.email == email).first()
        if not user:
            return {'error': "Couldn't find the user with given email address"}, 400

        expires = datetime.timedelta(hours=24)
        reset_token = create_access_token(str(user.user_id), expires_delta=expires)

        return send_email('[Real Estate Trading] Reset Your Password',
                          sender='khanhkd.digitalocean@gmail.com',
                          recipients=[user.email],
                          text_body=render_template('email/reset_password.txt',
                                                    url=url + reset_token),
                          html_body=render_template('email/reset_password.html',
                                                    url=url + reset_token))


class ResetPassword(Resource):
    def post(self):
        url = request.host_url + 'reset/'
        body = request.get_json()
        reset_token = body.get('reset_token')
        password = body.get('password')

        if not reset_token or not password:
            return {"error": "Request is missing required fields"}, 400

        user_id = decode_token(reset_token)['identity']
        user = db.session.query(User).filter(User.user_id == user_id).first()

        user.modify(password=password)
        user.hash_password()

        db.session.commit()

        return send_email('[Real Estate Trading] Password reset successful',
                          sender='khanhkd.digitalocean@gmail.com',
                          recipients=[user.email],
                          text_body='Password reset was successful',
                          html_body='<p>Password reset was successful</p>')
