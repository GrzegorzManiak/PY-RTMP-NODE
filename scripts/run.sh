#!/bin/bash
set -e

# -- Nginx + RTMP Server install
/scripts/nginx.sh

# -- Python and its dependencies
/scripts/python.sh


# Start nginx
/usr/local/nginx/conf/sbin/nginx -g "daemon off;"