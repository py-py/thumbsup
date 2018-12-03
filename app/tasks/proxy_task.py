from json import JSONDecodeError

import requests
from celery import group

from app import celery
from app.models import Proxy, get_or_create

__all__ = ('download_proxy', )

URL = 'http://pubproxy.com/api/proxy'


@celery.task(name='proxy:save')
def save_proxy(host, port):
    get_or_create(Proxy, host=host, port=port)


@celery.task(name='proxy:parse')
def parse_json(data):
    group(save_proxy.s(item['ip'], item['port']) for item in data['data'])()


@celery.task(name='proxy:fetch')
def fetch_proxy(limit):
    payload = {
        'limit': limit,
    }
    with requests.get(URL, params=payload) as response:
        if response.status_code == 200:
            try:
                response.json()
            except JSONDecodeError:
                pass
        raise Exception('Can not to get proxies')


@celery.task(name='proxy:main')
def download_proxy(limit=20):
    (fetch_proxy.s(limit) | parse_json.s())()
