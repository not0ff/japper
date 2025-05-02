import os
from datetime import timedelta

from cachelib.file import FileSystemCache
from dotenv import load_dotenv

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY: str | None = os.getenv("SECRET_KEY")

    UPLOADED_PROFILES_DEST = os.path.join(basedir, "uploads/profiles")
    UPLOADED_POSTS_DEST = os.path.join(basedir, "uploads/posts")
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024

    SESSION_TYPE: str = "cachelib"
    SESSION_CACHELIB: FileSystemCache = FileSystemCache(cache_dir="sessions")
    USE_SESSION_FOR_NEXT: bool = True
    REMEMBER_COOKIE_DURATION: timedelta = timedelta(weeks=1)

    SQLALCHEMY_DATABASE_URI: str = os.getenv(
        "DATABASE_URI"
    ) or "sqlite:///" + os.path.join(basedir, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
