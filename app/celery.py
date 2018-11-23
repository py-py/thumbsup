import os
from celery import Celery

REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
REDIS_PORT = os.getenv('REDIS_PORT', 6379)
REDIS_DB = os.getenv('REDIS_DB', 0)

redis_broker = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}'
app = Celery('tasks', broker=redis_broker)


@app.task
def save_host(host, port):
    print(host, port)


@app.task
def behance_thumbs_up(url, likes):
    print(url, likes)
