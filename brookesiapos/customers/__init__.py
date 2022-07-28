from flask.blueprints import Blueprint

customers_bp = Blueprint('customers_routes', __name__)

from . import routes