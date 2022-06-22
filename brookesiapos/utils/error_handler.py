from flask import Response, json

def generic_error_handler(e):
    return Response(
        response=json.dumps({
            'response_status': {
                'status': e.code,
                'message': f'{e.name}: {e.description}'
            },
            'data': []
        }),
        status=e.code,
        content_type='application/json'
    )

def conflict_error_handler(e):
    return Response(
        response=json.dumps({
            'response_status': {
                'status': e.code,
                'message': f'{e.name}: The request could not be completed because the resource to create already exists, use the PUT method to update it.'
            },
            'data': []
        }),
        status=e.code,
        content_type='application/json'
    )