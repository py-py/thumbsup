import os

from dotenv import load_dotenv

load_dotenv()
env = os.getenv('FLASK_ENV')

CELERY_HOST = os.getenv('CELERY_HOST')
CELERY_PORT = os.getenv('CELERY_PORT')
CELERY_DB = os.getenv('CELERY_DB')

DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

basedir = os.path.abspath(os.path.dirname(__file__))
broker_path = 'redis://{}:{}/{}'.format(CELERY_HOST, CELERY_PORT, CELERY_DB)
db_path = 'mysql://{}:{}@{}:{}/{}'.format(DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)


class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY') or 'secret_key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CELERY_BROKER_URL = broker_path
    CELERY_RESULT_BACKEND = broker_path


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'thumbs.db')
    SQLALCHEMY_DATABASE_URI = db_path


class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = db_path


if env == 'production':
    Config = ProductionConfig
elif env == 'development':
    Config = DevelopmentConfig
else:
    raise Exception('environment ENVIRONMENT is not provided')
