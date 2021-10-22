from flask import Response

def not_found(e):
    return Response(status=404)