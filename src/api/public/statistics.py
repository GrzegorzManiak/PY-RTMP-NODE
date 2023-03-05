from lib import authenticated, truncate
from . import public_blueprint
from stats import get_cache
from flask import Response

import json

"""
    :name: statistics
    :description: Get the nginx statistics
"""
@public_blueprint.route(
    '/statistics', 
    methods=['POST', 'GET']
)
@authenticated()
def statistic():
    return Response(
        json.dumps(get_cache()),
        mimetype='application/json'
    )