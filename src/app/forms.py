from filetype import guess_extension
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileSize
from wtforms import (
    BooleanField,
    Field,
    HiddenField,
    PasswordField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError

from app.extensions import db, profile_imgs
from app.models import Post, User


# Post Id of current user's post
def validate_post_id(form: FlaskForm, field: Field) -> None:
    post: Post | None = (
        db.session.query(Post).filter_by(id=field.data, user_id=current_user.id).first()
    )
    if post is None:
        raise ValidationError("Invalid PostId")


def validate_profile_id(form: FlaskForm, profile_id: Field) -> None:
    user: User | None = db.session.query(User).filter_by(id=profile_id.data).first()
    if user is None or user == current_user:
        return ValidationError("Invalid ProfileId")


def validate_username(form: FlaskForm, field: Field) -> None:
    user: User | None = db.session.query(User).filter_by(username=field.data).first()
    if user is not None:
        raise ValidationError("This username is already taken")


def validate_image(form: FlaskForm, field: Field) -> None:
    if not field.data:
        return
    ext = guess_extension(field.data)
    if ext is None or not profile_imgs.extension_allowed(ext):
        raise ValidationError("Invalid image format")


class SignupForm(FlaskForm):
    username: StringField = StringField(
        "Username",
        validators=[
            DataRequired("Enter a username"),
            Length(
                min=3,
                max=16,
                message="Username must be between %(min)d and %(max)d characters long",
            ),
            validate_username,
        ],
    )
    password: PasswordField = PasswordField(
        "Password",
        validators=[
            DataRequired("Enter a password"),
            Length(
                min=8, max=120, message="Password must have at least %(min)d characters"
            ),
        ],
    )
    confirm_password: PasswordField = PasswordField(
        "Repeat password",
        validators=[
            DataRequired("Repeat your password"),
            EqualTo("password", message="Passwords must be equal"),
        ],
    )
    submit: SubmitField = SubmitField("Sign Up")


class LoginForm(FlaskForm):
    username: StringField = StringField(
        "Username", validators=[DataRequired("Enter a username")]
    )
    password: PasswordField = PasswordField(
        "Password", validators=[DataRequired("Enter a password")]
    )
    remember: BooleanField = BooleanField("Remember me")
    submit: SubmitField = SubmitField("Login")


class EditProfileForm(FlaskForm):
    image: FileField = FileField(
        "Profile picture",
        description="Up to 8MB in size",
        validators=[
            FileAllowed(profile_imgs, message="Pick an image file!"),
            FileSize(max_size=8 * 1024 * 1024, message="File is bigger than 8MB!"),
            validate_image,
        ],
    )
    bio: TextAreaField = TextAreaField(
        "Bio",
        description="Use at most 120 characters",
        validators=[Length(max=120, message="You can use at most 120 characters")],
    )
    submit: SubmitField = SubmitField("Save changes")


class FollowProfileForm(FlaskForm):
    profile_id: HiddenField = HiddenField(
        "ProfileId",
        validators=[DataRequired("ProfileId is required"), validate_profile_id],
    )
    submit: SubmitField = SubmitField()


class PostForm(FlaskForm):
    content: TextAreaField = TextAreaField(
        "Content",
        description="200 character limit applies",
        validators=[
            DataRequired("Provide your post content"),
            Length(
                max=200, message="Your post cannot contain more than 200 characters"
            ),
        ],
    )
    submit: SubmitField = SubmitField("Publish")


class EditPostForm(FlaskForm):
    content: TextAreaField = TextAreaField(
        "Content",
        description="200 character limit applies",
        validators=[
            DataRequired("Provide your post content"),
            Length(max=200, message="Your post cannot use more than 200 characters"),
        ],
    )
    post_id: HiddenField = HiddenField(
        "PostId", validators=[DataRequired("PostId is required"), validate_post_id]
    )
    submit: SubmitField = SubmitField("Save")


class DeletePostForm(FlaskForm):
    post_id: HiddenField = HiddenField(
        "PostId", validators=[DataRequired("PostId is required"), validate_post_id]
    )
    submit: SubmitField = SubmitField("Delete")


class SearchPostForm(FlaskForm):
    query: StringField = StringField(
        "Query",
        description="Search up posts",
        validators=[
            DataRequired("Provide searchable text"),
            Length(
                min=3,
                max=200,
                message="Text for search must have %(min)d-%(max)d characters",
            ),
        ],
    )
    submit: SubmitField = SubmitField("Search")
