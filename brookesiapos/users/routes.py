from crypt import methods
from flask import Response, json, abort, request

from . import users_bp
from brookesiapos.database import db_manager
from brookesiapos.utils.auth import http_auth

#from brookesiapos import users
from brookesiapos.users import users_bp

USERS_API_ENDPOINT = '/api/users'

@users_bp.route(USERS_API_ENDPOINT)
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


@users_bp.route(f'{USERS_API_ENDPOINT}/<int:item_id>')
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

@users_bp.route(f'{USERS_API_ENDPOINT}', methods=['POST'])
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
    if db_manager.item_exists('users', 'username', username):
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

    data = db_manager.insert_into_table('users', user)
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
    else:
        abort(500)