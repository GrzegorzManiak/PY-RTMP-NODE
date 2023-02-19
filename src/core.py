import signal
import time
import os

from nginx import kill_all_nginx, start_nginx, check_config
from api import start_api
from logger import log
from stats import stats_refresh_thread


# -- Threading
global threads
threads = []


# -- Start services
start_nginx()
start_api(threads)
stats_refresh_thread(threads, 1)

# -- Start the exit listener
def exit_listener(signum, frame):
    print('')
    log('CORE', 'Exiting...', 'DEBUG')

    # -- Kill all nginx processes
    kill_all_nginx()

    # -- Kill all the threads weve created
    for thread in threads:
        log('CORE', f'Killing thread: {thread.name}', 'DEBUG')
        thread.join()

    # -- Exit the script
    log('CORE', 'Exited successfully')
    raise SystemExit

signal.signal(signal.SIGINT, exit_listener)


# -- Keep the script running
while True:
    
    # -- Check if nginx is running
    if len(os.popen('ps -A | grep nginx').read()) == 0:
        log('NGINX', 'Nginx is not running, restarting...', 'ERROR')
        kill_all_nginx()
        start_nginx()

    # -- Check if the config file has changed
    check_config();

    # -- Sleep for x seconds
    time.sleep(2)