#!/bin/bash
set -e

# Install dependencies
apt-get update
apt-get install -y git build-essential wget libpcre3 libpcre3-dev libssl-dev zlib1g-dev libpcre3-dev

cd /tmp

# Clone the nginx-rtmp-module repository
git clone https://github.com/sergey-dryabzhinsky/nginx-rtmp-module.git
wget https://nginx.org/download/nginx-1.23.3.tar.gz
tar -zxvf nginx-1.23.3.tar.gz

# Configure and build nginx with nginx-rtmp-module
cd nginx-1.23.3
./configure --with-http_ssl_module --add-module=../nginx-rtmp-module
make
make install

# Add nginx binary to PATH
echo 'export PATH=$PATH:/usr/local/nginx/sbin' >> ~/.bashrc
source ~/.bashrc

# Clean up
rm -rf /tmp/nginx-rtmp-module
rm -rf /tmp/nginx.tar.gz
rm -rf /tmp/nginx

# -- Copy over the nginx.conf file from /scripts/nginx.conf
cp /scripts/nginx.conf /usr/local/nginx/conf/nginx.conf

echo "nginx installed"
