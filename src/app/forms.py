from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length

class SignupForm(FlaskForm):
    username = StringField('Username', description='Enter a username 3-16 characters long', validators=[DataRequired(message='Enter a username'), Length(min=3, max=16, message='Username must be between %(min)d and %(max)d characters long')])
    password = PasswordField('Password', description='Provide a passwords with at least 8 characters',validators=[DataRequired(message='Enter a password'), Length(min=8, max=120, message='Password must have at least %(min)d characters')])
    confirm_password = PasswordField('Repeat password', description='Enter a matching password', validators=[DataRequired(message='Repeat your password'), EqualTo('password', message='Passwords must be equal')])
    submit = SubmitField('Submit')
    
class LoginForm(FlaskForm):
    username = StringField('Username', description='Enter your username', validators=[DataRequired(message='Enter a username')])
    password = PasswordField('Password', description='Provide a valid password', validators=[DataRequired(message='Enter a password')])
    submit = SubmitField('Submit')