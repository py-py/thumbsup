from json import JSONDecodeError

import requests

from app import celery
from app.models import Proxy, get_or_create

__all__ = ('download_proxy',)

URL = 'https://proxy.l337.tech/txt'


@celery.task(name='proxy:parse_and_save')
def parse_and_save(data):
    for proxy in data:
        host, port = proxy.split(':')
        get_or_create(Proxy, host=host, port=port)


@celery.task(name='proxy:fetch')
def fetch_proxy():
    with requests.get(URL, verify=False) as response:
        if response.status_code == 200:
            try:
                content = response.content.decode()
                return content.splitlines()
            except JSONDecodeError:
                raise Exception(response.content)
        raise Exception('Can not to get proxies')


@celery.task(name='proxy:main')
def download_proxy():
    (fetch_proxy.s() | parse_and_save.s())()
