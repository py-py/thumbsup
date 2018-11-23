from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def thumb(url):
    pass


URL = 'https://www.behance.net/gallery/71966493/Halloween-Cartoon'

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('--proxy-server=http://{}'.format('77.252.133.48:25772'))

driver = webdriver.Chrome(
    chrome_options=options,
    executable_path='/usr/lib/chromium-browser/chromedriver'
)
driver.set_window_size(1495, 977)
driver.get(URL)

try:
    element = WebDriverWait(driver, 10) \
        .until(EC.presence_of_element_located((By.CSS_SELECTOR, '.project-block--buttons .thumb a')))
    element.click()
finally:
    driver.quit()
