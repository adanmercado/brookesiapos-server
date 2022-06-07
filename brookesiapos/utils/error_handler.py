from flask import Response, json

def generic_error_handler(e):
    return Response(
        response=json.dumps({
            'response_status': {
                'status': e.code,
                'message': e.name #e.description
            },
            'data': []
        }),
        status=e.code,
        content_type='application/json'
    )