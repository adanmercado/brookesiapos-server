from uuid import uuid4

from flask import Response, request, json, abort

from . import terminals_bp
from brookesiapos.database import db_manager
from brookesiapos.utils.auth import http_auth

TERMINALS_API_ENDPOINT = '/api/terminals'
TABLE_NAME = 'terminals'

@terminals_bp.route('/api/uuid')
def create_uuid():
    return Response(
        response=json.dumps({
            'response_status': {
                'status': 200
            },
            'data': {
                'uuid': str(uuid4())
            }
        }),
        status=200,
        content_type='application/json'
    )

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

@terminals_bp.route(f'{TERMINALS_API_ENDPOINT}/<int:terminal_id>')
@http_auth.login_required
def list_terminal(terminal_id: int):
    data = db_manager.select_one_from_table(TABLE_NAME, terminal_id)

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

@terminals_bp.route(TERMINALS_API_ENDPOINT, methods=['POST'])
@http_auth.login_required
def create_terminal():
    body = request.get_json()
    mandatory_fields = ['terminal_number', 'name', 'uuid']
    
    if not body:
        abort(400, f'You must provide the following fields in the request body: {mandatory_fields}')

    missing_fields = []
    for field in mandatory_fields:
        if not field in body:
            missing_fields.append(field)

    if missing_fields:
        abort(400, f'You must provide the following fields in the request body: {missing_fields}')

    terminal_number = body['terminal_number']
    if db_manager.item_exists(TABLE_NAME, 'terminal_number', terminal_number):
        abort(409, f'The number \'{terminal_number}\' is already assigned to a registered terminal, use the PUT method to update it.')

    terminal_name = body['name']
    if db_manager.item_exists(TABLE_NAME, 'name', terminal_name):
        abort(409, f'The name \'{terminal_name}\' is already assigned to a registered terminal, use the PUT method to update it.')

    terminal_uuid = body['uuid']
    if db_manager.item_exists(TABLE_NAME, 'uuid', terminal_uuid):
        abort(409, f'The UUID \'{terminal_uuid}\' is already assigned to a registered terminal, use the PUT method to update it.')

    last_ip = None
    if 'last_ip' in body:
        last_ip = body['last_ip']

    terminal = {
        'terminal_number': terminal_number,
        'name': terminal_name,
        'uuid': terminal_uuid,
        'last_ip': last_ip
    }

    data = db_manager.insert_into_table(TABLE_NAME, terminal)
    if not data:
        abort(500)

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


@terminals_bp.route(f'{TERMINALS_API_ENDPOINT}/<int:terminal_id>', methods=['PUT'])
@http_auth.login_required
def update_terminal(terminal_id: int):
    body = request.get_json()

    if not body:
        abort(400, 'You must provide the fields to update.')

    filter_fields = ['id', 'uuid']
    for field in filter_fields:
        if field in body:
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

    terminal = db_manager.select_one_from_table(TABLE_NAME, terminal_id)
    if not terminal:
        abort(404)

    terminal_number = None
    if 'terminal_number' in body:
        terminal_number = body['terminal_number']

    if terminal_number and terminal_number != terminal[0]['terminal_number'] and db_manager.item_exists(TABLE_NAME, 'terminal_number', terminal_number):
        abort(409, f'The number \'{terminal_number}\' is already assigned to another registered terminal, please specify another terminal number.')

    terminal_name = None
    if 'name' in body:
        terminal_name = body['name']

    if terminal_name and terminal_name != terminal[0]['name'] and db_manager.item_exists(TABLE_NAME, 'name', terminal_name):
        abort(409, f'The name \'{terminal_name}\' is already assigned to another registered terminal, please specify another terminal name.')

    data = db_manager.update_item(TABLE_NAME, body, terminal_id)
    if not data:
        abort(500)

    return Response(
        response=json.dumps({
            'response_status': {
                'status': 200
            },
            'data': data
        }),
        status=200,
        content_type='applicatio/json'
    )