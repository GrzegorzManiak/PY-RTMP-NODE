from dotenv.main import load_dotenv
import os

load_dotenv('../.env')
NGINX_BIN = os.path.abspath(os.getenv("NGINX_BIN"))
NGINX_CONF = os.path.abspath(os.getenv("NGINX_CONF"))
NGINX_CONF_PARSED = os.path.abspath(os.getenv("NGINX_CONF_PARSED"))

CORE_API = os.getenv("CORE_URL"
).replace(
    '$CORE_HOST', os.getenv("CORE_HOST")
).replace(
    '$CORE_PORT', os.getenv("CORE_PORT")
)

# -- Set the env 'CORE_API' to the API URL
os.environ['CORE_API'] = CORE_API
