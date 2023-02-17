from flask import Flask
import threading
import os


# -- Blueprints
from .private import private_blueprint
from .public import public_blueprint

# -- Create the app
app = Flask(__name__)

# -- Register blueprints
app.register_blueprint(private_blueprint)
app.register_blueprint(public_blueprint)

print(app.url_map)

def start_api():
    # -- Start the API on a different thread
    threading.Thread(
        target = lambda: app.run(
            host=f'{os.getenv("CORE_HOST")}', 
            port=f'{os.getenv("CORE_PORT")}'
        )
    ).start()

