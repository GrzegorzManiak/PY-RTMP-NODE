from . import public_blueprint
from stats import get_cache
from flask import Response

import json

@public_blueprint.route(
    '/statistics', 
    methods=['POST', 'GET']
)
def statistic():
    return Response(
        json.dumps(get_cache()),
        mimetype='application/json'
    )