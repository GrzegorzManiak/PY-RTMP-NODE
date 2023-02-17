from flask import Blueprint

private_blueprint = Blueprint(
    'private', 
    __name__,
    url_prefix='/private'
)

# -- Import all the routes
from .publish import publish