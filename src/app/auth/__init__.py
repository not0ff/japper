from flask import Blueprint

auth: Blueprint = Blueprint(
    'auth', __name__,
    url_prefix='/auth',
    template_folder='templates'
)

from . import routes
