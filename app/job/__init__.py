from flask import Blueprint

job_bp = Blueprint('job', __name__, template_folder='job')

from . import routes
