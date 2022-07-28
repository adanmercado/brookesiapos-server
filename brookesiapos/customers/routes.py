from flask import Response, json, abort, request

from . import customers_bp
from brookesiapos.database import db_manager
from brookesiapos.utils.auth import http_auth

CUSTOMERS_API_ENDPOINT = '/api/customers'
TABLE_NAME = 'customers'


@customers_bp.route(CUSTOMERS_API_ENDPOINT)
@http_auth.login_required
def list_customers():
    data = db_manager.select_all_from_table(TABLE_NAME)

    if data == False:
        abort(500)
    else:
        return Response(
            response=json.dumps({
                'response_status': {
                    'status': 200
                },
                'data': data
            }),
            status=200,
            content_type='application/json'
        )