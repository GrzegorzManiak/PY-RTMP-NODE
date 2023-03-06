import threading
import logging
import os

from flask import Flask
from logger import log

# -- Blueprints
from .private import private_blueprint
from .public import public_blueprint

# -- Create the app
app = Flask(__name__)


# -- Register blueprints
app.register_blueprint(private_blueprint)
app.register_blueprint(public_blueprint)

def start_api(threads: list):
    # -- Suppress the flask debug messages
    # https://stackoverflow.com/a/70025182
    logging.getLogger('werkzeug').setLevel(logging.CRITICAL)

    # -- Start the API on a different thread
    log('API', f'Starting API on {os.getenv("CORE_HOST")}:{os.getenv("CORE_PORT")}', 'DEBUG')

    thread = threading.Thread(
        target = lambda: app.run(
            host=f'{os.getenv("CORE_HOST")}', 
            port=f'{os.getenv("CORE_PORT")}'
        )
    )
    
    thread.setName('API')
    thread.start()  

    # -- Add the thread to the list of threads
    threads.append(thread)

    log('API', f'API started successfully on {os.getenv("CORE_HOST")}:{os.getenv("CORE_PORT")}')