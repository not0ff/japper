import os
from typing import Optional

from cachelib.file import FileSystemCache
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # TODO: Try loading .env outside of config class
    load_dotenv()
    SECRET_KEY: Optional[str] = os.getenv('SECRET_KEY')

    # MAX_CONTENT_LENGTH = 10 * 1024 * 1024
    # UPLOAD_EXTENSIONS = ['jpg', 'jpeg', 'png', 'webp']

    SESSION_TYPE: str = 'cachelib'
    SESSION_CACHELIB: FileSystemCache = FileSystemCache(cache_dir='sessions')
    SESSION_PERMANENT: bool = False
    USE_SESSION_FOR_NEXT: bool = True

    SQLALCHEMY_DATABASE_URI: str = os.getenv(
        'DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
