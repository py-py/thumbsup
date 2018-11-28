from random import randint
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, ElementNotVisibleException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from app import celery, db
from app.models import Proxy, Job

__all__ = ('add_like', 'thumbs_up')

# sudo sudo apt install chromium-chromedriver
MIN_WAIT_SECONDS = 10
MAX_WAIT_SECONDS = 20
CSS_SELECTOR = '.project-block--buttons .thumb a'


def make_driver(proxy):
    user_agent = UserAgent()
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('--proxy-server=http://{}'.format(proxy.union))
    options.add_argument(user_agent.chrome)

    driver = webdriver.Chrome(
        chrome_options=options,
        executable_path='/usr/lib/chromium-browser/chromedriver'
    )
    driver.set_window_size(randint(800, 1400), randint(600, 1000))
    return driver


@celery.task(bind=True, name='thumbs_up:add_like')
def add_like(self, job_id, proxy_id):
    if self.request.retries > 0:
        # TODO: search a new proxy;
        pass
    job = Job.query.filter_by(id=job_id).first()
    proxy = Proxy.query.filter_by(id=proxy_id).first()

    driver = make_driver(proxy)
    driver.get(job.url)

    try:
        element = WebDriverWait(driver, randint(MIN_WAIT_SECONDS, MAX_WAIT_SECONDS)) \
            .until(EC.presence_of_element_located((By.CSS_SELECTOR, CSS_SELECTOR)))
        element.click()
    except (TimeoutException, ElementNotVisibleException) as e:
        raise e
    else:
        job.added_likes += 1
        db.session.add(job)
        db.session.commit()
    finally:
        proxy.count_used += 1
        db.session.add(proxy)
        db.session.commit()
        driver.quit()


@celery.task(bind=True, name='thumbs_up:main')
def thumbs_up(self, job_id):
    job = Job.query.get(job_id)

    if not job:
        raise Exception('Job {job_id} not found.'.format(job_id=job_id))

    proxies = [p for p in Proxy.query.order_by('count_used').all()[:job.ordered_likes]]
    for proxy in proxies:
        job.proxies.append(proxy)
        db.session.add(job)
        db.session.commit()
        # add_like.apply_async((job.id, proxy.id), countdown=randint(0, job.period))
