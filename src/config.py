import os
from dotenv import load_dotenv
from cachelib.file import FileSystemCache

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # TODO: Try loading .env outside of config class
    load_dotenv()
    SECRET_KEY = os.getenv('SECRET_KEY')

    # MAX_CONTENT_LENGTH = 10 * 1024 * 1024
    # UPLOAD_EXTENSIONS = ['jpg', 'jpeg', 'png', 'webp']

    SESSION_TYPE = 'cachelib'
    SESSION_CACHELIB = FileSystemCache(cache_dir='sessions')
    SESSION_PERMANENT = False

    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
