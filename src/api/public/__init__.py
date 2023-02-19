from flask import Blueprint

public_blueprint = Blueprint(
    'public',
    __name__,
    url_prefix='/public'
)

# -- Import all the routes
from . statistics import statistic