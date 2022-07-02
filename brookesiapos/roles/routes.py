from flask import Response, request, json, abort

from . import roles_bp
from brookesiapos.database import db_manager
from brookesiapos.utils.auth import http_auth

ROLES_API_ENDPOINT = '/api/roles'

@roles_bp.route(ROLES_API_ENDPOINT)
@http_auth.login_required
def list_user_roles():
    data = db_manager.select_all_from_table('user_roles')

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