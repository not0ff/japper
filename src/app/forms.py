from typing import Optional

from filetype import guess_extension
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileSize
from wtforms import (BooleanField, Field, PasswordField, StringField,
                     SubmitField, TextAreaField)
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError

from app.extensions import profile_imgs
from app.models import User


class SignupForm(FlaskForm):
    username: StringField = StringField('Username', validators=[
        DataRequired(message='Enter a username'),
        Length(min=3, max=16, message='Username must be between %(min)d and %(max)d characters long')])
    password: PasswordField = PasswordField('Password', validators=[
        DataRequired(message='Enter a password'),
        Length(min=8, max=120, message='Password must have at least %(min)d characters')])
    confirm_password: PasswordField = PasswordField('Repeat password', validators=[
        DataRequired(message='Repeat your password'),
        EqualTo('password', message='Passwords must be equal')])
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


class EditProfileForm(FlaskForm):
    image: FileField = FileField('Profile picture', validators=[
        FileAllowed(profile_imgs, message='Pick an image file!'),
        FileSize(max_size=8*1024*1024, message='File is bigger than 8MB!')])
    bio: TextAreaField = TextAreaField('Bio', 
        description='Use at most 120 characters', validators=[
        Length(max=120, message='You can use at most 120 characters')])
    submit: SubmitField = SubmitField('Save changes')

    def validate_profile_img(self, img: Field) -> None:
        if not img.data:
            return
        ext = guess_extension(img.data)
        if ext is None or not profile_imgs.extension_allowed(ext):
            raise ValidationError('Invalid image format')


class PostForm(FlaskForm):
    post: TextAreaField = TextAreaField('Post', 
        description= '200 character limit applies',validators=[
        DataRequired('Provide your post content'),
        Length(max=200, message='Your post cannot use more than 200 characters')])
    submit: SubmitField = SubmitField('Publish')
