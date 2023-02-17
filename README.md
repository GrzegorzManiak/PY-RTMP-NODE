# PY-RTMP-NODE
A RTMP Ingest/Relay/Edge Node using FFMPEG, Python and NGINX-RTMP

## What is this?
This is a RTMP Ingest/Relay/Edge Node using FFMPEG, Python and NGINX-RTMP. Personally I will use this in my 2nd Year Project at TUDublin, but feel free to use it for your own projects.

## How does it work?
Theres a few parts to this project, but the main parts are:
- Heartbeat: This heartbeats to a server to let it know that the node is still alive.
- Core: This is the core of the project, it handles the Auth of broadcasters and Viewers, It is
        Responsible for relaying certain streams to other nodes.
- NGINX: This is the RTMP server that will accept the RTMP stream and relay it to the other nodes.
- FFMPEG: This is the encoder that will encode the RTMP stream to HLS and DASH.
- Master: This is the server that sits in the middle of the mesh, it is responsible for directing
          the streams to the correct nodes, load balancing the streams, keeping track of the
          nodes, keeping track of the streams, authentication of broadcasters, viewers and nodes.

          In general, this is the brains of the operation, I will open source this in the future,
          as I am still working on it.

## How do I use it?
### .env
```
# NGINX
NGINX_PORT = 1935
NGINX_CONF = ../nginx.conf
NGINX_BIN  = /usr/local/nginx/sbin/nginx

# FFMPEG (TBC)

# MASTER 
MASTER_SERVER = https://master.streamstage.co
HEARTBEAT_ENDPOINT = /heartbeat
ANNOUNCE_ENDPOINT = /announce
STREAMS_ENDPOINT = /streams
AUTH_ENDPOINT = /auth

# SECURITY
MASTER_KEY = 1234567890-SUPER-STRONG-KEY
```

## Docker 
### Build
```
docker build -t py-rtmp-node .
```

### Run
```
docker run -d -p 1935:1935 -p 8080:8080 py-rtmp-node
```
