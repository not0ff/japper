from datetime import datetime, timezone
from typing import Literal, Optional, Union

import sqlalchemy as sa
from flask_login import UserMixin, current_user
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, backref, mapped_column, relationship
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db, login_manager


class User(UserMixin, db.Model):  # type: ignore
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    username: Mapped[str] = mapped_column(
        sa.String(16), unique=True, nullable=False)
    bio: Mapped[Optional[str]] = mapped_column(sa.String(120), nullable=True)
    password_hash: Mapped[Optional[str]] = mapped_column(
        db.String(120), nullable=True)
    posts: Mapped['Post'] = relationship(
        'Post', backref=backref('author'))
    likes: Mapped[list['Like']] = relationship(
        'Like', backref=backref('user'), uselist=True, lazy='select'
    )

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        if self.password_hash is None:
            return False
        return check_password_hash(self.password_hash, password)

    def add_like(self, post: 'Post') -> None:
        if not post.liked:
            like = Like(user_id=self.id, post_id=post.id)
            db.session.add(like)

    def remove_like(self, post: 'Post') -> None:
        if post.liked:
            Like.query.filter_by(
                user_id=self.id,
                post_id=post.id
            ).delete()


class Post(db.Model):  # type: ignore
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        sa.Integer, sa.ForeignKey(User.id), index=True)
    timestamp: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc), index=True)
    post: Mapped[str] = mapped_column(sa.String(200), nullable=True)
    likes: Mapped[list['Like']] = relationship(
        'Like', backref=backref('post'), uselist=True, lazy='select'
    )

    @hybrid_property
    def liked(self):
        return set(current_user.likes) & set(self.likes)


class Like(db.Model):  # type: ignore
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        sa.Integer, sa.ForeignKey(User.id), index=True)
    post_id: Mapped[int] = mapped_column(
        sa.Integer, sa.ForeignKey(Post.id), index=True)


@login_manager.user_loader
def load_user(id: str) -> Optional[User]:
    return User.query.get(int(id))
