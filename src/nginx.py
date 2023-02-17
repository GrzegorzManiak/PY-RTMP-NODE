import os
from env import (
    NGINX_BIN, 
    NGINX_CONF,
    NGINX_CONF_PARSED
)


"""
    :name: parse_nginx_conf
    :desc: Parse the nginx config file replaces 
           the variables with the values from the .env file
           and outputs it to a nginx.temp.conf file
    :return: bool
"""
def parse_nginx_conf() -> bool:
    try: 
        # -- Variables are in the format of $VAR_NAME
        #    So we need to add the $ to the env variables
        #    to match the format in the config file
        env_vars = {}
        for key, value in os.environ.items():
            env_vars[f"${key}"] = value

        # -- Read the config file
        text = ""
        with open(NGINX_CONF, 'r') as f:
            text = f.read()
            f.close()

        # -- Replace the variables with the values
        for key, value in env_vars.items():
            text = text.replace(key, value)

        # -- Write the new config to a temp file
        with open(NGINX_CONF_PARSED, 'w') as f:
            f.write(text)
            f.close()

        return True

    except: return False





"""
    :name: kill_all_nginx
    :desc: Kill all nginx processes
    :return: bool
"""
def kill_all_nginx() -> bool:
    try:
        os.system("killall -9 nginx")
        return True
    except: return False



"""
    :name: start_nginx
    :desc: Start nginx
    :return: bool
"""
def start_nginx() -> bool:
    try:
        if parse_nginx_conf() == False: return False
        os.system(f'{NGINX_BIN} -c {NGINX_CONF_PARSED} -g "daemon on;"')
        return True
    except: return False



"""
    :name: reload_nginx
    :desc: Reloads nginx with the new config 
            without dropping any connections
"""
def reload_nginx() -> bool:
    try:
        if parse_nginx_conf() == False: return False
        os.system(f'{NGINX_BIN} -c {NGINX_CONF_PARSED} -s reload')
        return True
    except: return False



"""
    :name: read_conf
    :desc: Read the config file
    :return: str
"""
def read_conf() -> str:
    text = ""
    with open(NGINX_CONF, 'r') as f:
        text = f.read()
        f.close()
    return text



# -- Gets the current config
#    To check if it has changed
current_confing = read_conf()
"""
    :name: check_config
    :desc: Check if the config file has changed
           And reload nginx if it has changed
    :return: bool : True if the config has not changed
"""
def check_config() -> bool:
    global current_confing
    if read_conf() != current_confing:
        current_confing = read_conf()
        if reload_nginx() == False:
            print("Failed to reload nginx")
            exit(1)
        return False
    return True
