from flask import request, Response
from logger import log
from . import private_blueprint

# ImmutableMultiDict([
#   ('call', 'publish'), 
#   ('name', ''), 
#   ('type', 'live'), 
#   ('addr', '127.0.0.1'), 
#   ('clientid', '1'), 
#   ('app', 'live'), 
#   ('flashver', 'FMLE/3.0 (compatible; FMSc/1.0)'), 
#   ('swfurl', 'rtmp://127.0.0.1:1935/live'), 
#   ('tcurl', 'rtmp://127.0.0.1:1935/live')
# ])

# Path: src/api/private/publish.py
@private_blueprint.route(
    '/publish', 
    methods=['POST', 'GET']
)
def publish():

    
    return Response(
        status=200
    )