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