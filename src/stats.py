"""
    For somereason, NGINX-RTMP outputs its statistics as a
    XML file. So we need to parse the XML file and convert
    it to a dictionary.

    We have to get the XML file from the nginx server, 
    http://$NGINX_HTTP_API/statistics
"""

import requests
import xmltodict
import json

from logger import log
from env import NGINX_HTTP_API

def get_nginx_stats() -> dict:
    try:
        log('NGINX', 'Getting nginx statistics', 'debug')
        r = requests.get(f"http://{NGINX_HTTP_API}/statistics")

        if r.status_code == 200:
            log('NGINX', 'Got nginx statistics successfully')
            return xmltodict.parse(r.text)
        else:
            log('NGINX', 'Failed to get nginx statistics', 'error')
            return {}
    except:
        log('NGINX', 'Failed to get nginx statistics', 'error')
        return {}