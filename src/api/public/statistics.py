from env import LOG_FOLDER
from lib import authenticated
from . import public_blueprint
from stats import get_cache
from flask import Response

import json
import os

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



"""
    :name: logs
    :description: Get the core logs as a list of dictionaries
"""
@public_blueprint.route(
    '/logs',
    methods=['POST', 'GET']
)
@authenticated()
def logs():

    # -- Get the logs
    logs = []

    for file in os.listdir(LOG_FOLDER):
        logs.append(file)

    return Response(
        json.dumps(logs),
        mimetype='application/json'
    )



"""
    :name: log
    :description: Return the log file as a string
"""
@public_blueprint.route(
    '/logs/<log>',
    methods=['POST', 'GET']
)
@authenticated()
def log(log):
    try:
        with open(f'{LOG_FOLDER}/{log}', 'r') as f:
            return Response(
                f.read(),
                mimetype='text/plain'
            )
    except:
        return Response(
            'Log not found',
            mimetype='text/plain'
        )
    