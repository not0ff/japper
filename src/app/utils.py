from io import BytesIO
from typing import Optional, Sequence, Union

import sqlalchemy as sa
from flask import current_app, flash, redirect, request, session, url_for
from flask.typing import ResponseReturnValue
from flask_login import current_user
from flask_wtf import FlaskForm
from is_safe_url import is_safe_url
from PIL import Image
from werkzeug.datastructures import FileStorage

from app.extensions import db
from app.models import Like, Notification, Post, User


def optimize_img(image: FileStorage, resize: bool = False) -> FileStorage:
    img: Image.Image = Image.open(image)

    if img.mode != 'RGB':
        img = img.convert('RGB')

    if resize:
        img = img.resize((512, 512))

    output: BytesIO = BytesIO()
    img.save(output, format='WEBP', optimize=True, quality=60)
    output.seek(0)

    return FileStorage(
        stream=output,
        filename='filename.webp',
        content_type="image/webp"
    )


def get_post(data: Optional[dict]) -> tuple[int, Union[Post, str]]:
    if data is None or 'id' not in data:
        return 400, 'Invalid request'

    try:
        id = int(data['id'])
    except (ValueError, TypeError):
        return 400, 'Invalid post ID'

    post: Post = Post.query.get(id)
    if post is None:
        return 404, 'Post not found'

    return 200, post


def get_profile(data: Optional[dict]) -> tuple[int, Union[User, str]]:
    if data is None or 'id' not in data:
        return 400, 'Invalid request'

    try:
        id = int(data['id'])
    except (ValueError, TypeError):
        return 400, 'Invalid user ID'

    user: User = User.query.get(id)
    if user is None:
        return 404, 'User not found'

    return 200, user


def get_feed() -> Sequence[Post]:
    query: sa.Select = sa.select(Post, ((
        sa.select(
            sa.func.count())
        .where(Like.post_id == Post.id)
        .scalar_subquery()) / ((
            sa.func.strftime('%s', sa.func.now()) -
            sa.func.strftime('%s', Post.timestamp)
        ) + 1)
    ).label('rank')
    ).order_by(sa.literal_column('rank').desc())

    return db.session.execute(query).scalars().all()


def add_notification(user: User, content: str, issuer: User = current_user) -> None:
    notification = Notification(
        user_id=user.id, issuer_id=issuer.id, content=content)
    db.session.add(notification)


def search_post(pattern: str) -> Sequence[Post]:
    pattern = '%'.join(pattern.split())
    return Post.query.filter(Post.content.like(f'%{pattern}%')).order_by(sa.desc(Post.timestamp)).all()


def redirect_to_referrer(fallback: Optional[str] = None) -> ResponseReturnValue:
    next_page = request.referrer
    if next_page is not None and is_safe_url(next_page, {request.host}):
        return redirect(next_page)
    if fallback is None:
        with current_app.app_context():
            return redirect(url_for('core.index'))
    return redirect(fallback)


def redirect_to_next(fallback: Optional[str] = None) -> ResponseReturnValue:
    next_page = session.pop('next', None)
    if next_page is not None and is_safe_url(next_page, {request.host}):
        return redirect(next_page)
    if fallback is None:
        with current_app.app_context():
            return redirect(url_for('core.index'))
    return redirect(fallback)


def flash_form_errors(form: FlaskForm) -> None:
    for field, errors in form.errors.items():
        for error in errors:
            flash(f'{field.capitalize()}: {error}', category='danger')
