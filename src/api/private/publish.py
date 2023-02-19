from flask import request, Response
from lib import destructure_multi_dict, ensure_valid_secret
from logger import log
from connection import Connection, ConnectionType
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

    # -- Destructure the request
    stream_data = destructure_multi_dict(request.form)
    

    # -- Make sure the stream is valid
    required = ['call', 'name', 'addr', 'clientid', 'app']
    if (
        stream_data is None or
        not all(key in stream_data for key in required) or
        stream_data['call'] != 'publish'
    ):
        log('PUBLISH', 'Invalid publish request', 'error')
        # 302: For some reason, this is what nginx-rtmp
        #      expects to be returned when the stream
        #      is invalid
        return Response(status=302)

    # -- Make sure the secret is valid
    if not ensure_valid_secret(stream_data['name']):
        log('PUBLISH', 'Invalid secret', 'error')
        return Response(status=302)

    # 
    # TODO: Authenticate the stream, this stuff
    #       will go here when I get around to it
    # 


    # -- Create the stream
    connection = Connection(
        connection_type=ConnectionType.PUBLISH,
        client_id=stream_data['clientid'],
        address=stream_data['addr'],
        app=stream_data['app'],
        secret=stream_data['name']
    )
    

    # -- Allow the stream to be published
    log('PUBLISH', f'Publishing stream {connection}')
    return Response(
        status=200
    )