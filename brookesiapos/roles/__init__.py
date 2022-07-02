from flask import blueprints

roles_bp = blueprints.Blueprint('roles_routes', __name__)

from . import routes