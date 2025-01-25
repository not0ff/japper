from flask import Blueprint

api: Blueprint = Blueprint(
    'api', __name__,
    template_folder='templates'
)

from . import routes
