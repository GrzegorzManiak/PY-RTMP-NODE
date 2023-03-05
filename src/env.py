from dotenv.main import load_dotenv
from logger import log
import socket
import os

load_dotenv('../.env')
NGINX_BIN = os.path.abspath(os.getenv("NGINX_BIN"))
NGINX_CONF = os.path.abspath(os.getenv("NGINX_CONF"))
NGINX_CONF_PARSED = os.path.abspath(os.getenv("NGINX_CONF_PARSED"))
NGINX_HTTP_PORT = int(os.getenv("NGINX_HTTP_PORT"))

SECRET = os.getenv("MASTER_KEY")

# -- CORE_HOST
if os.getenv("CORE_HOST") == None:
    os.environ['CORE_HOST'] = socket.gethostbyname(socket.gethostname())


# -- CORE ENDPOINTS's
CORE_API = os.getenv("CORE_URL"
).replace(
    '$CORE_HOST', os.getenv("CORE_HOST")
).replace(
    '$CORE_PORT', os.getenv("CORE_PORT")
)

NGINX_HTTP_API = os.getenv("CORE_URL"
).replace(
    '$CORE_HOST', os.getenv("CORE_HOST")
).replace(
    '$CORE_PORT', os.getenv("NGINX_HTTP_PORT")
)

NGINX_RTMP_API = os.getenv("CORE_URL"
).replace(
    '$CORE_HOST', os.getenv("CORE_HOST")
).replace(
    '$CORE_PORT', os.getenv("NGINX_RTMP_PORT")
)

# -- Set the env 'CORE_API' to the API URL
os.environ['CORE_API'] = CORE_API
os.environ['NGINX_HTTP_API'] = NGINX_HTTP_API

# -- Local
local = os.getenv("LOCAL_ONLY").lower() == 'true'
if local: os.environ['LOCAL_ONLY'] = 'deny all;'
else: os.environ['LOCAL_ONLY'] = ''

# -- Add 'logs' folder as static folder, logs is in the root of the project
LOG_FOLDER = os.path.abspath('./logs')

log('OS', f'Log Folder: {LOG_FOLDER}')
log('ENV', 'Environment variables loaded successfully')
