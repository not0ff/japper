from datetime import datetime, timezone
from typing import Optional

import sqlalchemy as sa
from sqlalchemy.orm import mapped_column, relationship, Mapped, WriteOnlyMapped
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db, login_manager


class User(UserMixin, db.Model):  # type: ignore
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    username: Mapped[str] = mapped_column(
        sa.String(16), unique=True, nullable=False)
    bio: Mapped[Optional[str]] = mapped_column(sa.String(120), nullable=True)
    password_hash: Mapped[Optional[str]] = mapped_column(
        db.String(120), nullable=True)
    posts: WriteOnlyMapped['Post'] = relationship(back_populates='author')

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        if self.password_hash is None:
            return False
        return check_password_hash(self.password_hash, password)


class Post(db.Model):  # type: ignore
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        sa.Integer, sa.ForeignKey(User.id), index=True)
    timestamp: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc), index=True)
    post: Mapped[str] = mapped_column(sa.String(200), nullable=True)
    author: Mapped[User] = relationship(back_populates='posts')


@login_manager.user_loader
def load_user(id: str) -> Optional[User]:
    return User.query.get(int(id))
