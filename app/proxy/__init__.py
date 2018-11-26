from flask import Blueprint

proxy = Blueprint('proxy', __name__, template_folder='proxy')

from . import routes
