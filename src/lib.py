from functools import wraps
from flask import request, Response
from env import SECRET
import os

"""
    :name: destructure_multi_dict
    :desc: Destructure a Flask MultiDict into just
           a regular Python dict
        
    :param multi_dict: The MultiDict to destructure
    
    :return: A regular Python dict
"""
def destructure_multi_dict(multi_dict) -> dict:
    return {key: multi_dict[key] for key in multi_dict}



"""
    :name: ensure_valid_secret
    :desc: Ensure that the secret is valid
           Longer than 32 characters, and only
           contains alphanumeric characters
    
    :param secret: The secret to check
    :return: bool
"""
def ensure_valid_secret(secret: str) -> bool:
    return len(secret) > 32 and secret.isalnum()



"""
    :name: authenticated
    :description: A decorator to check if the user is authenticated,
        will be used to protect routes as we are exposing some of the
        API to the public (public as in for admins not the common user)
"""
def authenticated():
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            if (
                request.headers.get('Authorization') is not None and
                os.environ.get('SERVER_SECRET') is not None and

                request.headers.get('Authorization') == SECRET or
                request.headers.get('nodesecret') == os.environ.get('SERVER_SECRET')
            ): return view_func(*args, **kwargs)

            else: return Response('Unauthorized', status=401)
        return wrapper
    
    return decorator



"""
    :name: truncate
    :description: Truncate a text to a lenght of lines
    :param text: The file to truncate
    :param start: The start of the file to truncate
    :param end: The end of the file to truncate (optional)
"""
def truncate(text: str, start: int, end: int = None):
    # -- Get the lines
    lines = text.splitlines()

    if start and start.isdigit():
        lines = lines[int(start):]

    if end and end.isdigit():
        lines = lines[:int(end)]

    # -- Return the lines
    return lines



"""
    :name: filter_logs
    :description: Filter the logs by the header
    :param logs: The logs to filter
    :param logger: The logger to filter by
    :return: The filtered logs
"""
def filter_logs(logs: list, logger: str) -> list:
    # EG: 2023-03-05 20:45:16,196 - urllib3.connectionpool - DEBUG - Starting new HTTP connection (1): 127.0.0.1:2042
    # Timestamp, logger, level, message

    if not logger: return logs
    if logger.lower() != 'root':
        return [log for log in logs if log.split(' - ')[1].lower() == logger.lower()]
    
    return [log.split('>?')[1] for log in logs if log.split(' - ')[1].lower() == 'root']

