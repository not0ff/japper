from flask import Blueprint

post: Blueprint = Blueprint(
    'post', __name__,
    url_prefix='/post',
    template_folder='templates'
)

from . import routes
