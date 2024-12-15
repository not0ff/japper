from flask import Flask
from flask_session import Session

from config import Config
from app.extensions import db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    Session(app)
    db.init_app(app)
    
    from app.core import core
    app.register_blueprint(core)
    
    @app.after_request
    def add_header(request):
        request.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        request.headers['Pragma'] = 'no-cache'
        request.headers['Expires'] = '0'
        return request
    
    return app