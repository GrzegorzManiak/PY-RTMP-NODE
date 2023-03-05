from functools import wraps
from flask import request, Response
from env import SECRET

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
            if request.headers.get('Authorization') == SECRET:
                return view_func(*args, **kwargs)
            else: return Response(
                'Unauthorized',
                status=401,
            )
        return wrapper
    
    return decorator
