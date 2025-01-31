from datetime import datetime, timezone
from typing import Optional

import sqlalchemy as sa
from flask_login import UserMixin, current_user
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, backref, mapped_column, relationship
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db, login_manager


followers = sa.Table('followers',
                     db.metadata,
                     sa.Column('follower_id', sa.Integer, sa.ForeignKey(
                         'user.id'), primary_key=True),
                     sa.Column('followed_id', sa.Integer,
                               sa.ForeignKey('user.id'), primary_key=True)
                     )


class User(UserMixin, db.Model):  # type: ignore
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    username: Mapped[str] = mapped_column(
        sa.String(16), unique=True)
    bio: Mapped[str | None] = mapped_column(sa.String(120), nullable=True)
    password_hash: Mapped[str | None] = mapped_column(
        db.String(120), nullable=True)
    posts: Mapped['Post'] = relationship(
        'Post', backref=backref('author'))
    likes: Mapped[list['Like']] = relationship(
        'Like', backref=backref('user'))
    following: Mapped[list['User']] = relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        back_populates='followers')
    followers: Mapped[list['User']] = relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.followed_id == id),
        secondaryjoin=(followers.c.follower_id == id),
        back_populates='following')
    notifications: Mapped['Notification'] = relationship(
        'Notification', backref=backref('user'), foreign_keys='Notification.user_id')
    notified: Mapped['Notification'] = relationship(
        'Notification', backref=backref('issuer'), foreign_keys='Notification.issuer_id')

    @hybrid_property
    def followed(self):
        return current_user in self.followers

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        if self.password_hash is None:
            return False
        return check_password_hash(self.password_hash, password)

    def add_like(self, post: 'Post') -> None:
        if not post.liked:
            like: Like = Like(user_id=self.id, post_id=post.id)
            db.session.add(like)

    def remove_like(self, post: 'Post') -> None:
        if post.liked:
            Like.query.filter_by(
                user_id=self.id,
                post_id=post.id
            ).delete()

    def follow(self, user: 'User') -> None:
        if not user.followed:
            self.following.append(user)
            db.session.add(self)

    def unfollow(self, user: 'User') -> None:
        if user.followed:
            self.following.remove(user)
            db.session.add(self)


class Post(db.Model):  # type: ignore
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        sa.Integer, sa.ForeignKey(User.id), index=True)
    content: Mapped[str | None] = mapped_column(sa.String(200), nullable=True)
    timestamp: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc), index=True)
    edited: Mapped[bool] = mapped_column(
        sa.Boolean, default=False, onupdate=True)
    likes: Mapped[list['Like']] = relationship(
        'Like', backref=backref('post'))

    @hybrid_property
    def liked(self):
        return set(current_user.likes) & set(self.likes)


class Like(db.Model):  # type: ignore
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        sa.Integer, sa.ForeignKey(User.id), index=True)
    post_id: Mapped[int] = mapped_column(
        sa.Integer, sa.ForeignKey(Post.id), index=True)


class Notification(db.Model):  # type: ignore
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        sa.Integer, sa.ForeignKey(User.id), index=True)
    issuer_id: Mapped[int] = mapped_column(
        sa.Integer, sa.ForeignKey(User.id), index=True)
    timestamp: Mapped[float] = mapped_column(
        default=lambda: datetime.now(timezone.utc).timestamp(), index=True)
    content: Mapped[str] = mapped_column(sa.String(50))
    read: Mapped[bool] = mapped_column(sa.Boolean, default=False)

    def mark_read(self) -> None:
        if not self.read:
            self.read = True
            db.session.add(self)


@login_manager.user_loader
def load_user(id: str) -> Optional[User]:
    return User.query.get(int(id))
