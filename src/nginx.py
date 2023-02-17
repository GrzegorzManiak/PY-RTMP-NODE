import os

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
        nginx_bin = os.path.abspath(os.getenv("NGINX_BIN"))
        nginx_conf = os.path.abspath(os.getenv("NGINX_CONF"))

        os.system(f'{nginx_bin} -c {nginx_conf} -g "daemon on;"')
        return True
    except: return False


"""
    :name: reload_nginx
    :desc: Reloads nginx with the new config 
            without dropping any connections
"""
def reload_nginx() -> bool:
    try:
        nginx_bin = os.path.abspath(os.getenv("NGINX_BIN"))
        nginx_conf = os.path.abspath(os.getenv("NGINX_CONF"))

        os.system(f'{nginx_bin} -c {nginx_conf} -s reload')
        return True
    except: return False