from flask import Response, request, json, abort

from . import roles_bp
from brookesiapos.database import db_manager
from brookesiapos.utils.auth import http_auth

ROLES_API_ENDPOINT = '/api/roles'
TABLE_NAME = 'user_roles'

@roles_bp.route(ROLES_API_ENDPOINT)
@http_auth.login_required
def list_user_roles():
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

@roles_bp.route(f'{ROLES_API_ENDPOINT}/<int:role_id>')
@http_auth.login_required
def list_user_role(role_id: int):
    data = db_manager.select_one_from_table(TABLE_NAME, role_id)

    if data:
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
    elif data == False:
        abort(500)
    else:
        abort(404)