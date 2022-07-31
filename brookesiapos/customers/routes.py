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


@customers_bp.route(CUSTOMERS_API_ENDPOINT, methods=['POST'])
@http_auth.login_required
def create_customer():
    body = request.get_json()
    mandatory_fields = ['name']
    
    if not body:
        abort(400, f'You must provide the following fields in the request body: {mandatory_fields}')

    missing_fields = []
    for field in mandatory_fields:
        if not field in body:
            missing_fields.append(field)

    if missing_fields:
        abort(400, f'You must provide the following fields in the request body: {missing_fields}')

    name = body['name']
    if db_manager.item_exists(TABLE_NAME, 'name', name):
        abort(409, f'The name \'{name}\' is already assigned to a registered customer, use the PUT method to update it.')

    address = None
    if 'address' in body:
        address = body['address']

    phone = None
    if 'phone' in body:
        address = body['phone']

    email = None
    if 'email' in body:
        address = body['email']

    customer = {
        'name': name,
        'address': address,
        'phone': phone,
        'email': email
    }

    data = db_manager.insert_into_table(TABLE_NAME, customer)
    if data:
        return Response(
            response=json.dumps({
                'response_status': {
                    'status': 200,
                    'message': 'Customer created successfully.'
                },
                'data': data
            }),
            status=200,
            content_type='application/json'
        )
    else:
        abort(500)