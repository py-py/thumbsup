import logging
from random import randint
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, ElementNotVisibleException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pyvirtualdisplay import Display

from app import celery, db
from app.models import Proxy, Job, Association

__all__ = ('add_like', 'thumbs_up')

logger = logging.getLogger(__name__)

DRIVER_WAIT_SECONDS = 60
XPATH_SELECTOR = '//div[@id="project-canvas"]/following-sibling::div//div[@data-adobe-analytics="AppreciateClick"]'


def make_driver(proxy):
    user_agent = UserAgent()
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--proxy-server=http://{}'.format(proxy.union))
    options.add_argument(user_agent.chrome)

    # disable images;
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(
        chrome_options=options,
        executable_path='/usr/lib/chromium-browser/chromedriver'
    )
    # driver.set_window_size(randint(800, 1400), randint(600, 1000))
    return driver


@celery.task(bind=True, name='thumbs_up:add_like', default_retry_delay=0, max_retries=None)
def add_like(self, job_id, proxy_id):
    job = Job.query.get(job_id)
    proxy = Proxy.query.get(proxy_id)

    if self.request.retries > 0:
        try:
            proxy = job.get_free_proxy()
        except Exception as exc:
            logger.error('Job: {job.id} is stopped because free proxy for current job is not founded.'.format(job=job))
            raise exc

    association = Association(proxy=proxy)
    job.associations.append(association)
    db.session.add(job)
    db.session.commit()

    display = Display(visible=0)
    display.start()
    driver = make_driver(proxy)

    try:
        driver.get(job.url)
        element = WebDriverWait(driver, DRIVER_WAIT_SECONDS)\
            .until(EC.presence_of_element_located((By.XPATH, XPATH_SELECTOR)))
        element.click()
    except TimeoutException as exc:
        logger.error('Connect to job: {job.id} is not reachable with proxy: {proxy.id}'.format(proxy=proxy, job=job))
        self.retry()
    except ElementNotVisibleException as exc:
        logger.error('Proxy: {proxy.id} was used before for current job: {job.id}'.format(proxy=proxy, job=job))
        self.retry()
    except WebDriverException as exc:
        logger.error(exc)
        self.retry()
    else:
        association.is_success = True
        db.session.add(association)
        db.session.commit()
    finally:
        proxy.count_used += 1
        db.session.add(proxy)
        db.session.commit()
        driver.quit()
        display.stop()


@celery.task(bind=True, name='thumbs_up:main')
def thumbs_up(self, job_id):
    job = Job.query.get(job_id)

    if not job:
        raise Exception('Job {job_id} not found.'.format(job_id=job_id))

    proxies = sorted(job.get_free_proxies(), key=lambda p: p.count_used)[:job.ordered_likes]
    for proxy in proxies:
        # TODO: temporary for debugging;
        # add_like.apply_async((job.id, proxy.id), countdown=randint(0, job.period))
        add_like.apply_async((job.id, proxy.id), countdown=randint(0, 0))
