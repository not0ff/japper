from typing import Optional

from flask_login import UserMixin
from sqlalchemy.orm import Mapped
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db, login_manager


class User(UserMixin, db.Model):  # type: ignore
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    username: Mapped[str] = db.Column(
        db.String(16), unique=True, nullable=False)
    bio: Mapped[Optional[str]] = db.Column(db.String(120), nullable=True)
    password_hash: Mapped[Optional[str]] = db.Column(
        db.String(120), nullable=True)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        if self.password_hash is None:
            return False
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(id: str) -> Optional[User]:
    return User.query.get(int(id))
