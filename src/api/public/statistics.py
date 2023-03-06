from lib import authenticated
from . import public_blueprint
from stats import get_cache, server_statistics_cache
from flask import Response

import json

"""
    :name: statistic_nginx
    :description: Get the nginx statistics
"""
@public_blueprint.route(
    '/statistics/nginx', 
    methods=['POST', 'GET']
)
@authenticated()
def statistic_nginx():
    return Response(
        json.dumps(get_cache()),
        mimetype='application/json'
    )



"""
    :name: statistic_server
    :description: Get the server statistics
        in a formated graph
"""
@public_blueprint.route(
    '/statistics/server',
    methods=['POST', 'GET']
)
@authenticated()
def statistic_server():
    return Response(
        json.dumps({
            'data': server_statistics_cache,
            'message': 'Success'
        }),
        mimetype='application/json'
    )