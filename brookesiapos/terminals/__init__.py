from flask import blueprints

terminals_bp = blueprints.Blueprint('terminals_routes', __name__)

from . import routes