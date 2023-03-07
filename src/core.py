import signal
import uuid
import time
import os

from nginx import kill_all_nginx, start_nginx, check_config
from api import start_api
from logger import log
from stats import stats_refresh_thread
from master import announce

# -- Threading
global threads
threads = []


# -- Start services
start_nginx()
start_api(threads)
stats_refresh_thread(threads, 1)

# -- Check if we have a .id file
if os.path.isfile('.id'):
    with open('.id', 'r') as f:
        os.environ['SERVER_ID'] = f.read()
        f.close()

else:
    with open('.id', 'w') as f:
        os.environ['SERVER_ID'] = str(uuid.uuid4())
        f.write(os.environ['SERVER_ID'])
        f.close()
        


# -- Start the Server authentication and 
#    Heartbeat processess
server_id = None
server_secret = None
server_mode = None
server_name = None
server_slug = None

while True:
    # -- Check if were in test mode 'TEST_MODE'
    if os.environ['TEST_MODE'].lower() == 'true':
        log('CORE', 'Running in test mode, skipping server authentication', 'DEBUG')
        break

    announcement = announce.announce()

    if announcement[0] == False:
        log('CORE', 'Failed to announce to master server, retrying...', 'ERROR')
        time.sleep(int(os.environ['ANNOUNCE_RETRY_TIME']))

    else:
        server_id = announcement[1]['id']
        server_secret = announcement[1]['secret']
        server_mode = announcement[1]['mode']
        server_name = announcement[1]['name']
        server_slug = announcement[1]['slug']

        # -- OS Set the secret
        os.environ['SERVER_SECRET'] = server_secret

        log('CORE', 'Announced to master server successfully', 'DEBUG')
        log(server_slug, f'We are Node: "{server_id}", Named: "{server_name}", runing in: "{server_mode}" mode', 'info')
        
        # -- Break out of the loop
        break



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
    time.sleep(5)
    