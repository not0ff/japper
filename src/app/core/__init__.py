from flask import Blueprint

core: Blueprint = Blueprint("core", __name__, template_folder="templates")

from . import routes  # noqa: E402

__all__ = ["core", "routes"]
