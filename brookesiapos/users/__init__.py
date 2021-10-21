from flask import blueprints

users_bp = blueprints.Blueprint('users_routes', __name__)

from . import routes