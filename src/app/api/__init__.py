from flask import Blueprint

api: Blueprint = Blueprint(
    'api', __name__,
    url_prefix='/api',
    template_folder='templates'
)

from . import routes
