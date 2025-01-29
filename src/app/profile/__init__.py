from flask import Blueprint

profile: Blueprint = Blueprint(
    'profile', __name__,
    url_prefix='/profile',
    template_folder='templates'
)

from . import routes
