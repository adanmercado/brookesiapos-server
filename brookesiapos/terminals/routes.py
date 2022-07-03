from flask import Response, request, json, abort

from . import terminals_bp
from brookesiapos.database import db_manager
from brookesiapos.utils.auth import http_auth

TERMINALS_API_ENDPOINT = '/api/terminals'
TABLE_NAME = 'terminals'

@terminals_bp.route(TERMINALS_API_ENDPOINT)
@http_auth.login_required
def list_terminals():
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