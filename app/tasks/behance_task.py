from random import randint

from celery import shared_task, group
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from app.models import Proxy, Job
from app import celery

__all__ = ('add_like', 'thumbs_up')

# proxy = '77.252.133.48:25772'
# url = 'https://www.behance.net/gallery/71966493/Halloween-Cartoon'
WAIT_SECONDS = 10
CSS_SELECTOR = '.project-block--buttons .thumb a'


@celery.task(name='thumbs_up:add_like')
def add_like(url, proxy):
    # TODO: remove?
    print('TEST MESSAGE for proxy:' + proxy)

    # options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    # options.add_argument('--proxy-server=http://{}'.format(proxy))
    #
    # driver = webdriver.Chrome(
    #     chrome_options=options,
    #     executable_path='/usr/lib/chromium-browser/chromedriver'
    # )
    # driver.set_window_size(1495, 977)
    # driver.get(url)
    #
    # try:
    #     element = WebDriverWait(driver, WAIT_SECONDS)\
    #         .until(EC.presence_of_element_located((By.CSS_SELECTOR, CSS_SELECTOR)))
    #     element.click()
    # finally:
    #     driver.quit()


@celery.task(name='thumbs_up:main')
def thumbs_up(job_id):
    job = Job.query.filter_by(id=job_id).first()

    proxies = [p.union for p in Proxy.query.order_by('count_used').all()[:job.like]]
    for proxy in proxies:
        add_like.apply_async((job.url, proxy), countdown=randint(0, job.period))
