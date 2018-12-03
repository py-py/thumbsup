from flask import Flask
from flask_login import LoginManager

from app.celery import make_celery
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


def register_blueprints(app):
    from app.proxy import proxy_bp
    app.register_blueprint(proxy_bp, url_prefix='/proxy')

    from app.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    from app.job import job_bp
    app.register_blueprint(job_bp, url_prefix='/job')


app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'auth.login'

register_blueprints(app)
celery = make_celery(app)

celery.conf.beat_schedule = {
    'download_proxy': {
        'task': 'proxy:main',
        'schedule': 60 * 10,
    },
}

from .tasks import *
from .signals import *
from . import routes, models
