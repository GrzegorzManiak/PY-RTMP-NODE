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

from logger import log
from env import NGINX_HTTP_PORT


"""
    :name: get_nginx_stats
    :description: Get the nginx statistics as a dictionary
                  from the nginx server
    :return: dict or None if failed
"""
def get_nginx_stats() -> dict:
    try:
        r = requests.get(f"http://127.0.0.1:{NGINX_HTTP_PORT}/statistics")
        if r.status_code == 200:
            try: return xmltodict.parse(r.text)
            except: log('NGINX', 'Failed to parse nginx statistics', 'error')
        else: log('NGINX', 'Failed to get nginx statistics', 'error')
    except: log('NGINX', 'Failed to get nginx statistics', 'error')
    
    return None



"""
    :name: stats_refresh_thread
    :description: A thread that refreshes the nginx
                  statistics every x seconds
    :param: seconds: int
    :return: None
"""
statistics_thread = None
statistics_cache = None
force_refresh_callbacks = []

def stats_refresh_thread(threads: list, seconds: int):    
    # -- This is what will be run in the thread
    def func():
        global statistics_cache
        global force_refresh
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
                statistics_cache = get_nginx_stats()
                last_refresh = time.time() * 1000
                force_refresh = False

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