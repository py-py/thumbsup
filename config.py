import os

from dotenv import load_dotenv

load_dotenv()
_CELERY_BROKER_HOST = os.getenv('CELERY_BROKER_HOST')
_CELERY_BROKER_PORT = os.getenv('CELERY_BROKER_PORT')
_CELERY_BROKER_DB = os.getenv('CELERY_BROKER_DB')

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY') or 'secret_key'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CELERY_BROKER_URL = f'redis://{_CELERY_BROKER_HOST}:{_CELERY_BROKER_PORT}/{_CELERY_BROKER_DB}'
    CELERY_RESULT_BACKEND = f'redis://{_CELERY_BROKER_HOST}:{_CELERY_BROKER_PORT}/{_CELERY_BROKER_DB}'


class Production(Config):
    DEBUG = False
