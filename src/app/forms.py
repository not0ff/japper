from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import ValidationError, DataRequired, EqualTo, Length
from app.models import User


class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(
        message='Enter a username'), Length(min=3, max=16, message='Username must be between %(min)d and %(max)d characters long')])
    password = PasswordField('Password', validators=[DataRequired(
        message='Enter a password'), Length(min=8, max=120, message='Password must have at least %(min)d characters')])
    confirm_password = PasswordField('Repeat password', validators=[
                                     DataRequired(message='Repeat your password'), EqualTo('password', message='Passwords must be equal')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('This username is already taken')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(message='Enter a username')])
    password = PasswordField('Password', validators=[
                             DataRequired(message='Enter a password')])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')
