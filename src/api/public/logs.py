from env import LOG_FOLDER
from lib import authenticated, filter_logs, truncate
from . import public_blueprint
from flask import Response, request

import json
import os

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
    # -- Check for an optional start and end
    start = request.args.get('start')
    end = request.args.get('end')
    logger = request.args.get('logger')

    try:
        with open(f'{LOG_FOLDER}/{log}', 'r') as f: return Response(
            filter_logs(truncate(f.read(), start, end), logger),
            mimetype='text/plain'
        )
        
    except: return Response(
        'Log not found',
        mimetype='text/plain'
    )
    


"""
    :name: logs_latest
    :description: Return the latest log file as a string
"""
@public_blueprint.route(
    '/logs/latest',
    methods=['POST', 'GET']
)
@authenticated()
def logs_latest():
    # -- Check for an optional start and end
    start = request.args.get('start')
    end = request.args.get('end')
    logger = request.args.get('logger')

    # -- Get the logs
    logs = []

    for file in os.listdir(LOG_FOLDER):
        logs.append(file)

    try:
        # -- Get the latest log
        log = sorted(logs)[-1]

        with open(f'{LOG_FOLDER}/' + log, 'r') as f: return Response(
            filter_logs(truncate(f.read(), start, end), logger),
            mimetype='text/plain'
        )
        

    except: return Response(
        'Log not found',
        mimetype='text/plain'
    )