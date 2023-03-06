"""
    For somereason, NGINX-RTMP outputs its statistics as a
    XML file. So we need to parse the XML file and convert
    it to a dictionary.

    We have to get the XML file from the nginx server, 
    http://$NGINX_HTTP_API/statistics
"""


# -- Example of parsed XML
"""
    EXAMPLE OF ONE BROADCASTER CONNECTED TO NGINX-RTMP

{
   "rtmp":{
      "nginx_version":"1.23.3",
      "nginx_rtmp_version":"1.2.x-dev",
      "compiler":"gcc 12.2.1 20221121 (Red Hat 12.2.1-4) (GCC)",
      "pid":"33632",
      "uptime":"81",
      "naccepted":"2",
      "bw_in":"11177392",
      "bytes_in":"101306963",
      "bw_out":"0",
      "bytes_out":"517",
      "server":{
         "application":{
            "name":"live",
            "live":{
               "stream":{
                  "name":"test",
                  "time":"79662",
                  "bw_in":"11167384",
                  "bytes_in":"101215705",
                  "bw_out":"0",
                  "bytes_out":"0",
                  "bw_audio":"178856",
                  "bw_video":"10988528",
                  "bw_data":"0",
                  "client":{
                     "id":"1",
                     "address":"192.168.0.227",
                     "port":"57594",
                     "time":"79829",
                     "flashver":"FMLE/3.0 (compatible; FMSc/1.0)",
                     "swfurl":"rtmp://192.168.0.227/live",
                     "bytes_in":"101306963",
                     "bytes_out":"517",
                     "dropped":"0",
                     "avsync":"2",
                     "timestamp":"79435",
                     "publishing":"None",
                     "active":"None"
                  },
                  "meta":{
                     "video":{
                        "width":"1920",
                        "height":"1080",
                        "frame_rate":"60.000",
                        "data_rate":"10000",
                        "codec":"H264",
                        "profile":"High",
                        "compat":"0",
                        "level":"4.2"
                     },
                     "audio":{
                        "codec":"AAC",
                        "profile":"LC",
                        "channels":"2",
                        "sample_rate":"48000",
                        "data_rate":"160"
                     }
                  },
                  "nclients":"1",
                  "publishing":"None",
                  "active":"None"
               },
               "nclients":"1"
            },
            "play":{
               "nclients":"0"
            }
         }
      }
   }
}
"""

# -- Imports
import time
import requests
import xmltodict
import threading
import psutil
import warnings

from logger import log
from env import NGINX_HTTP_PORT


kb = float(1024)
mb = float(kb ** 2)
gb = float(kb ** 3)

"""
    :name: get_nginx_stats
    :description: Get the nginx statistics as a dictionary
                  from the nginx server
    :return: dict or None if failed
"""
def get_nginx_stats() -> dict:
    try:
        warnings.filterwarnings('ignore', message='Unverified HTTPS request')
        r = requests.get(f"https://127.0.0.1:{NGINX_HTTP_PORT}/statistics", verify=False)
        if r.status_code == 200:
            try: return xmltodict.parse(r.text)
            except: log('NGINX', 'Failed to parse nginx statistics E1', 'error')
        else: log('NGINX', 'Failed to get nginx statistics E2', 'error')
    except Exception as e: log('NGINX', f'Failed to get nginx statistics E3: {e}', 'error')
    
    return None



"""
    :name: stats_refresh_thread
    :description: A thread that refreshes the nginx
                  statistics every x seconds
    :param: seconds: int
    :return: None
"""
statistics_thread = None
statistics_cache = {}
force_refresh_callbacks = []
server_statistics_cache = {
    'datasets': [
        { 'name': 'CPU%', 'type': 'line', 'values': [] },
        { 'name': 'RAM%', 'type': 'line', 'values': [] },
        { 'name': 'NET RX (Mbps)', 'type': 'line', 'values': [] },
        { 'name': 'NET TX (Mbps)', 'type': 'line', 'values': [] },
    ],
    'labels': []
}

def get_network_usage():
    """
    Returns the network traffic in Mbps for the past second.
    """
    net_io_counters1 = psutil.net_io_counters()
    time.sleep(1)
    net_io_counters2 = psutil.net_io_counters()
    
    bytes_sent = net_io_counters2.bytes_sent - net_io_counters1.bytes_sent
    bytes_recv = net_io_counters2.bytes_recv - net_io_counters1.bytes_recv
    bits_sent = bytes_sent * 8
    bits_recv = bytes_recv * 8
    
    mbps_sent = bits_sent / 1000000
    mbps_recv = bits_recv / 1000000
    
    # Make sure that the values are a bit more than 0
    if mbps_sent < 0.01: mbps_sent = 0.01
    if mbps_recv < 0.01: mbps_recv = 0.01

    # Format the values to 2 decimal places
    mbps_sent = round(mbps_sent, 2)
    mbps_recv = round(mbps_recv, 2)

    return (mbps_sent, mbps_recv)

def push_stats():
    global server_statistics_cache  

    mem_total = int(psutil.virtual_memory()[0]/gb)
    mem_used = int(psutil.virtual_memory()[3]/gb)
    mem_percent = int(mem_used/mem_total*100)

    cpu = server_statistics_cache['datasets'][0]['values']
    ram = server_statistics_cache['datasets'][1]['values']
    net_tx = server_statistics_cache['datasets'][2]['values']
    net_rx = server_statistics_cache['datasets'][3]['values']

    cpu.append(psutil.cpu_percent())
    ram.append(mem_percent)
    
    nu = get_network_usage()
    net_tx.append(nu[0])
    net_rx.append(nu[1])

    # -- Trim the data
    MAX_ENTRIES = 10

    server_statistics_cache['datasets'][0]['values'] = cpu[-MAX_ENTRIES:]
    server_statistics_cache['datasets'][1]['values'] = ram[-MAX_ENTRIES:]
    server_statistics_cache['datasets'][2]['values'] = net_tx[-MAX_ENTRIES:]
    server_statistics_cache['datasets'][3]['values'] = net_rx[-MAX_ENTRIES:]

    # -- mm:ss
    lable = time.strftime('%H:%M:%S', time.gmtime(time.time()))
    server_statistics_cache['labels'].append(lable)
    server_statistics_cache['labels'] = server_statistics_cache['labels'][-MAX_ENTRIES:]


def get_cache() -> dict:
    global statistics_cache
    return statistics_cache

def set_cache(new_cache: dict):
    global statistics_cache
    statistics_cache = new_cache

def stats_refresh_thread(threads: list, seconds: int):    


    # -- This is what will be run in the thread
    def func():
        last_refresh = time.time() * 1000 # -- In milliseconds

        # So, we don't really want to refresh every x seconds
        # because we might need to get the stats right away
        # so basically, instead of sleeping, we just wait for
        # a signal to refresh the stats, or just to wait out
        # the time until the next refresh
        while True:
            if (
                len(force_refresh_callbacks) > 0 or 
                (time.time() * 1000) - last_refresh >= seconds * 1000
            ):
                set_cache(get_nginx_stats())
                push_stats()
                last_refresh = time.time() * 1000

            if len(force_refresh_callbacks) > 0:
                log('NGINX', 'Forced to refresh the statistics', 'DEBUG')

                for callback in force_refresh_callbacks:
                    # -- Execute the callback
                    callback()

                    # -- Get rid of the callback
                    force_refresh_callbacks.remove(callback)

                

    # -- Create the thread
    global statistics_thread
    statistics_thread = threading.Thread(target=func, name='stats_refresh_thread')
    statistics_thread.start()
    statistics_thread.name = 'NGINX-RTMP Statistics Refresh Thread'
    threads.append(statistics_thread)

    log('NGINX', 'Started the statistics refresh thread', 'DEBUG')