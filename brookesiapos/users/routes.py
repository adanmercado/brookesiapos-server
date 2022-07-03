from flask import Response, json, abort, request

from . import users_bp
from brookesiapos.database import db_manager
from brookesiapos.utils.auth import http_auth

USERS_API_ENDPOINT = '/api/users'
TABLE_NAME = 'users'

@users_bp.route(USERS_API_ENDPOINT)
@http_auth.login_required
def list_users():
    data = db_manager.select_all_from_table(TABLE_NAME)

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


@users_bp.route(f'{USERS_API_ENDPOINT}/<int:user_id>')
@http_auth.login_required
def list_user(user_id):
    data = db_manager.select_one_from_table(TABLE_NAME, user_id)

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

@users_bp.route(USERS_API_ENDPOINT, methods=['POST'])
@http_auth.login_required
def create_user():
    body = request.get_json()
    mandatory_fields = ['name', 'username', 'password', 'role']

    if not body:
        abort(400)
    
    for field in mandatory_fields:
        if not field in body:
            abort(400)

    username = body['username']
    if db_manager.item_exists(TABLE_NAME, 'username', username):
        abort(409)

    address = None
    if 'address' in body:
        address = body['address']

    phone = None
    if 'phone' in body:
        phone = body['phone']

    email = None
    if 'email' in body:
        email = body['email']

    picture = None
    if 'picture' in body:
        picture = body['picture']

    user = {
        'name': body['name'],
        'address': address,
        'phone': phone,
        'email': email,
        'username': username,
        'password': body['password'],
        'role': body['role'],
        'picture': picture
    }

    data = db_manager.insert_into_table(TABLE_NAME, user)
    if data:
        return Response(
            response=json.dumps({
                'response_status': {
                    'status': 200,
                    'message': 'User created successfully.'
                },
                'data': data
            }),
            status=200,
            content_type='application/json'
        )
    else:
        abort(500)

@users_bp.route(f'{USERS_API_ENDPOINT}/<int:user_id>', methods=['PUT'])
@http_auth.login_required
def update_user(user_id):
    body = request.json

    if not body:
        abort(400)

    filter_fields = ['id', 'username']
    for field in filter_fields:
        body.pop(field, None)

    if not body:
        return Response(
            response=json.dumps({
                'response_status': {
                    'status': 200,
                    'message': 'There is not content to update.'
                },
                'data': []
            }),
            status=200,
            content_type='application/json'
        )

    if not db_manager.item_exists(TABLE_NAME, 'id', user_id):
        abort(404)

    data = db_manager.update_item(TABLE_NAME, body, user_id)
    if data:
        return Response(
            response=json.dumps({
                'response_status': {
                    'status': 200,
                    'message': 'User updated successfully.'
                },
                'data': data
            }),
            status=200,
            content_type='application/json'
        )
    else:
        abort(500)