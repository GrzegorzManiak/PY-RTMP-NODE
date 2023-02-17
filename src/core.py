import time
from dotenv.main import load_dotenv
import os

from nginx import kill_all_nginx, start_nginx, reload_nginx

load_dotenv('../.env')

nginx_conf = os.path.abspath(os.getenv("NGINX_CONF"))
def read_conf() -> str:
    text = ""
    with open(nginx_conf, 'r') as f:
        text = f.read()
        f.close()
    return text
conf = read_conf()

# -- Start Nginx
if kill_all_nginx() == False:
    print("Failed to kill all nginx processes")
    exit(1)

if start_nginx() == False:
    print("Failed to start nginx")
    exit(1)

print("Nginx started successfully")


# -- Keep the script running
while True:
    
    # -- Check if nginx is running
    if os.system("pgrep nginx") != 0:
        print("Nginx is not running, restarting...")
        if start_nginx() == False:
            print("Failed to start nginx")
            exit(1)


    # -- Check if the config file has changed
    if read_conf() != conf:
        print("Config file has changed, reloading...")
        conf = read_conf()

        if reload_nginx() == False:
            print("Failed to reload nginx")
            exit(1)
            
        print("Nginx reloaded successfully")
    

    # -- Sleep for x seconds
    time.sleep(5)