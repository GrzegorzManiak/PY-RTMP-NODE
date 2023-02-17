from flask import app, Blueprint
from . import private_blueprint

# Path: src/api/private/publish.py
@private_blueprint.route('/publish', methods=['POST'])
def publish():
    print('Publishing...')
    # ...
    return 'OK'