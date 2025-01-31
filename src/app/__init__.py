from datetime import datetime, timezone

from flask import Flask, request
from flask.wrappers import Request
from flask_uploads import configure_uploads

from app.extensions import (csrf, db, login_manager, migrate, moment, session,
                            uploads)
from app.forms import DeletePostForm, EditPostForm, PostForm
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

    from app.post import post
    app.register_blueprint(post)

    from app.profile import profile
    app.register_blueprint(profile)

    from app.notification import notification
    app.register_blueprint(notification)

    from app.errors import bad_request, unauthorized, forbidden, not_found, method_not_allowed, payload_too_large, internal_error
    app.register_error_handler(400, bad_request)
    app.register_error_handler(401, unauthorized)
    app.register_error_handler(403, forbidden)
    app.register_error_handler(404, not_found)
    app.register_error_handler(405, method_not_allowed)
    app.register_error_handler(413, payload_too_large)
    app.register_error_handler(500, internal_error)

    @app.template_filter()
    def timestamp_to_datetime(timestamp):
        return datetime.fromtimestamp(timestamp, timezone.utc)

    @app.context_processor
    def pass_post_form() -> dict[str, PostForm]:
        if request.method == 'GET':
            return {'post_form': PostForm(), 'edit_post_form': EditPostForm(), 'delete_post_form': DeletePostForm()}
        return {}
        
    @app.after_request
    def add_header(request: Request) -> Request:
        request.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        request.headers['Pragma'] = 'no-cache'
        request.headers['Expires'] = '0'
        return request

    return app
