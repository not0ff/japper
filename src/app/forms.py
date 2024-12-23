from typing import Optional

from flask_wtf import FlaskForm
from wtforms import (BooleanField, Field, PasswordField, StringField,
                     SubmitField)
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError

from app.models import User


class SignupForm(FlaskForm):
    username: StringField = StringField('Username', validators=[DataRequired(
        message='Enter a username'), Length(min=3, max=16, message='Username must be between %(min)d and %(max)d characters long')])
    password: PasswordField = PasswordField('Password', validators=[DataRequired(
        message='Enter a password'), Length(min=8, max=120, message='Password must have at least %(min)d characters')])
    confirm_password: PasswordField = PasswordField('Repeat password', validators=[
        DataRequired(message='Repeat your password'), EqualTo('password', message='Passwords must be equal')])
    submit: SubmitField = SubmitField('Sign Up')

    def validate_username(self, username: Field) -> None:
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('This username is already taken')


class LoginForm(FlaskForm):
    username: StringField = StringField('Username', validators=[
        DataRequired(message='Enter a username')])
    password: PasswordField = PasswordField('Password', validators=[
        DataRequired(message='Enter a password')])
    remember: BooleanField = BooleanField('Remember me')
    submit: SubmitField = SubmitField('Login')
