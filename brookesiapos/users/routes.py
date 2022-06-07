from flask import Response, json, abort

from . import users_bp
from brookesiapos.database import db_manager
from brookesiapos.utils.auth import http_auth

@users_bp.route('/api/users')
@http_auth.login_required
def list_users():
    data = db_manager.select_all_from_table('users')

    if data == False:
        abort(500)
    else:
        return Response(
            response=json.dumps({
                'response_status': {
                    'status': 200,
                },
                'data': data
            }),
            status=200,
            content_type='application/json'
        )


@users_bp.route('/api/users/<int:item_id>')
@http_auth.login_required
def list_user(item_id):
    data = db_manager.select_one_from_table('users', item_id)

    if data:
        return Response(
            response=json.dumps({
                'response_status': {
                    'status': 200,
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