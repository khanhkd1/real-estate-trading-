from flask import request, render_template, make_response
from flask_jwt_extended import create_access_token, decode_token
from database.models import User
from flask_restful import Resource
from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired
import datetime
from services.mail_service import send_email
from database.db import db


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Reset Password')


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

        send_email('[Real Estate Trading] Reset Your Password',
                   sender='khanhkd.digitalocean@gmail.com',
                   recipients=[user.email],
                   text_body=render_template('email/reset_password.txt',
                                             url=url + reset_token),
                   html_body=render_template('email/reset_password.html',
                                             url=url + reset_token))
        return {'msg': 'Reset password request has been sent to your email'}, 200


class ResetPassword(Resource):
    def get(self, reset_token):
        form = ResetPasswordForm()
        return make_response(render_template('reset_password/reset_password.html', title='Reset Password', form=form),
                             200, {'Content-Type': 'text/html'})

    def post(self, reset_token):
        user_id = int(decode_token(reset_token)['sub'])
        user = db.session.query(User).filter(User.user_id == user_id).first()

        form = ResetPasswordForm()
        if form.validate_on_submit():
            user.password = form.password.data
            user.hash_password()
            db.session.commit()

        send_email('[Real Estate Trading] Password reset successful',
                   sender='khanhkd.digitalocean@gmail.com',
                   recipients=[user.email],
                   text_body='Password reset was successful',
                   html_body='<p>Password reset was successful</p>')
        return make_response(render_template('reset_password/reset_successfully.html'), 200,
                             {'Content-Type': 'text/html'})
