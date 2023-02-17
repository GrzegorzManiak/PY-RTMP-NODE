import threading
import time
import os

from nginx import kill_all_nginx, start_nginx, check_config
from api import start_api

# -- Start Nginx
if kill_all_nginx() == False:
    print("Failed to kill all nginx processes")
    exit(1)

if start_nginx() == False:
    print("Failed to start nginx")
    exit(1)


print(f'Nginx started successfully: {os.getenv("NGINX_HTTP_API")}');


# -- Start the API
start_api()
print("API started successfully")


# -- Keep the script running
while True:
    
    # -- Check if nginx is running
    if os.system("pgrep nginx") != 0:
        print("Nginx is not running, restarting...")
        if start_nginx() == False:
            print("Failed to start nginx")
            exit(1)


    # -- Check if the config file has changed
    if check_config() == False:
        print("Config file has changed, reloading nginx...")
        

    # -- Sleep for x seconds
    time.sleep(2)