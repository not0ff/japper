from flask import Blueprint

notification: Blueprint = Blueprint(
    "notification", __name__, url_prefix="/notification", template_folder="templates"
)

from . import routes  # noqa: E402

__all__ = ["notification", "routes"]
