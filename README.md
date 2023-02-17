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

### Terminology
- Node: A node is a server that is running the RTMP Node software, it can be a root node, edge
        node, root relay node or relay node.
- Root Relay Node: A node that can take in a stream from the Ingest node, and relay it to other nodes,
                   This not can NOT output a stream to the end user, only to other nodes.
- Relay Node: A node that can take in a stream from a Root Relay Node, and relay it to other nodes or
              the end user, this is the only node capable of transcoding the stream.
- Ingest Node: A node that can take in a stream from a broadcaster, and ONLY relay it to Root Level
               Relay Nodes.


### Relaying
The relaying decisions are made the the master server, there is one master relay table that is 
distributed to all the nodes, and its updated by the master server.

The node will than check its streams against the relay table, if it has a stream that is in the
relay table, it will relay it to the node that is in the relay table.

Each relay table entry has its own Security Key, this is used to authenticate the stream, so that
the node can be sure that the stream is coming from the correct node, and or not from a malicious
node or just a randomer.

- Root Relay: If this relay is designated as a root relay, the node will only relay the stream to
              other nodes, it will not relay the stream to the end user, if the nodes pourpose 
              is updated, it will drop any streams that are currently being relayed to it from
              normal nodes, and any streams being broadcasted to users.

```JSON
[
    "steam_id":  [
        {
            "node_id": "node_id",
            "node_url": "rtmp://node_url:1935/relay",
            "node_key": "node_key"
        }
    ]
]
```

#### User relaying (Only for Normal Relay Nodes)
If the node is a normal relay node, it will also relay the stream to the end user, this is done
by the NGINX-RTMP server, it will take the stream and relay it to the end user, with the user
of FFMPEG DASH and HLS transcoding.

When a user connects to the node, it will check its incoming streams to check if a stream is 
being broadcasted to this node, if it is, it will begin the process of transcoding the stream
and relaying it to the user (If it has not already started transcoding the stream for other
users).

If the stream is not being broadcasted to this node, it will request the master to route the
stream to this node, and then begin the transcoding process.

### Ingest
The ingest is done by the NGINX-RTMP server, it will accept the RTMP stream and relay it to the
other nodes.

The node will know which streams to relay to which nodes, because of the ingest relay table.
This table differs from the normal relay table as this one dose not point twoards edge nodes,
it only points to root level relay nodes.

```JSON
[
    "steam_id":  [
        {
            "node_id": "node_id",
            "node_url": "rtmp://node_url:1935/relay",
            "node_key": "node_key"
        }
    ]
]
```


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
