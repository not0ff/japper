from typing import Dict

from flask import Flask
from flask.wrappers import Request
from flask_uploads import configure_uploads

from app.extensions import (csrf, db, login_manager, migrate, moment, session,
                            uploads)
from app.forms import EditPostForm, PostForm, DeletePostForm
from config import Config


def create_app(config_class=Config) -> Flask:
    app: Flask = Flask(__name__)
    app.config.from_object(config_class)

    session.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)
    configure_uploads(app, uploads)

    from app.core import core
    app.register_blueprint(core)

    from app.auth import auth
    app.register_blueprint(auth)

    from app.api import api
    app.register_blueprint(api)

    @app.context_processor
    def pass_post_form() -> Dict[str, PostForm]:
        return {'post_form': PostForm(), 'edit_post_form': EditPostForm(), 'delete_post_form': DeletePostForm()}

    @app.after_request
    def add_header(request: Request) -> Request:
        request.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        request.headers['Pragma'] = 'no-cache'
        request.headers['Expires'] = '0'
        return request

    return app
