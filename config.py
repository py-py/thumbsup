import os

from dotenv import load_dotenv

load_dotenv()
env = os.getenv('FLASK_ENV')

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')
REDIS_DB = os.getenv('REDIS_DB')

DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

basedir_path = os.path.abspath(os.path.dirname(__file__))
broker_path = 'redis://{}:{}/{}'.format(REDIS_HOST, REDIS_PORT, REDIS_DB)
mysql_path = 'mysql://{}:{}@{}:{}/{}'.format(DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)


class Config:
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY') or 'secret_key'

    CELERY_BROKER_URL = broker_path
    CELERY_RESULT_BACKEND = broker_path

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = mysql_path
