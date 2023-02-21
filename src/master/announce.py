"""
    This module is responsible for announcing this node
    to the master server and getting back a secret that
    has to be used with all requests to the master server
    (bar this one ofc)
"""

# -- Imports
import urllib.request
import os
import json
import time

from logger import log


"""
    :name: announce
"""
def announce() -> list[bool, dict]:
    log('ANNOUNCE', 'Announcing to master server...', 'DEBUG')

    # -- Get our external IP
    external_ip = urllib.request.urlopen(
        'https://v4.ident.me/').read().decode('utf8')

    # -- Construct the data
    data = {
        'rtmp_ip': external_ip,
        'rtmp_port': os.environ['NGINX_RTMP_PORT'],
        'http_ip': external_ip,
        'http_port': os.environ['NGINX_HTTP_PORT'],
    }

    headers = {
        'Content-Type': 'application/json',
        'Authorization': os.environ['MASTER_KEY']
    }

    # -- Construct the endpoints
    endpoint = os.environ['MASTER_SERVER'] + os.environ['ANNOUNCE_ENDPOINT']
    
    # -- Send the request
    try:
        req = urllib.request.Request(
            endpoint, 
            json.dumps(data).encode('utf8'), 
            headers,
            method='POST'
        )
        response = urllib.request.urlopen(req).read().decode('utf8')
        log('ANNOUNCE', 'Announced to master server successfully', 'DEBUG')
        return [True, json.loads(response)]

    except Exception as e:
        log('ANNOUNCE', f'Failed to announce to master server: {e}', 'error')
        return [False, {}]

    return [False, {}]
