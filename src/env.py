from dotenv.main import load_dotenv
import os

load_dotenv('../.env')
NGINX_BIN = os.path.abspath(os.getenv("NGINX_BIN"))
NGINX_CONF = os.path.abspath(os.getenv("NGINX_CONF"))
NGINX_CONF_PARSED = os.path.abspath(os.getenv("NGINX_CONF_PARSED"))