"""
    :name: destructure_multi_dict
    :desc: Destructure a Flask MultiDict into just
           a regular Python dict
        
    :param multi_dict: The MultiDict to destructure
    
    :return: A regular Python dict
"""
def destructure_multi_dict(multi_dict) -> dict:
    return {key: multi_dict[key] for key in multi_dict}