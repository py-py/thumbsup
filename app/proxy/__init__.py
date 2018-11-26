from flask import Blueprint

proxy_bp = Blueprint('proxy', __name__, template_folder='proxy')

from . import routes
