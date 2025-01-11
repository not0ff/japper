from flask_login import LoginManager
from flask_migrate import Migrate
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_uploads import UploadSet, IMAGES
from flask_moment import Moment

db: SQLAlchemy = SQLAlchemy()
migrate: Migrate = Migrate()
csrf: CSRFProtect = CSRFProtect()
session: Session = Session()
login_manager: LoginManager = LoginManager()
moment: Moment = Moment()

login_manager.login_view = 'auth.login'
login_manager.session_protection = 'strong'
login_manager.login_message = 'You need to log in to access this page'
login_manager.login_message_category = 'warning'

profile_imgs: UploadSet = UploadSet('profiles', IMAGES)
post_imgs: UploadSet = UploadSet('posts', IMAGES)
uploads: list[UploadSet] = [profile_imgs, post_imgs]
