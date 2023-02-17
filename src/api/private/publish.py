from flask import request, Response
from . import private_blueprint

# Path: src/api/private/publish.py
@private_blueprint.route(
    '/publish', 
    methods=['POST', 'GET']
)
def publish():
    print(request)

    # ...
    return Response(
        status=200
    )