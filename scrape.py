# This script should be open in terminal, as in the example below:
# $ python scrape.py https://www.website-address.com

import sys
import logging
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import re

options = Options()
options.add_argument('headless')
options.add_experimental_option('excludeSwitches', ['enable-logging'])

logging.getLogger('WDM').setLevel(logging.CRITICAL)
os.environ['WDM_LOG_LEVEL'] = "0"

adres = sys.argv[1]
if adres[-1]=='/':
    adres = adres[:-1]

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

names = ['/kontakt', '/o-firmie', '/o-nas', '/ueber-uns', '/contact']


def phone_by_href(page):
    try:
        driver.get(page)

        number = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='tel:']")))
        num_by_href = number.get_attribute('text')
        return num_by_href
        
    except:
        pass


def phone_by_regex(page):
    try:
        driver.get(page)
        source = driver.page_source
        rgx_phone = re.compile(r"(?:\(?\+?\d{1,3}?\)?\s?)?\d{2,4}\s\d{2,3}\s\d{2,3}\s?\d{2,4}?|\(?\+\d{1,3}?\)?\d{9,11}|\d{3}\s\d{3}\s\d{3}|\+\d{2}\D\d{2,3}\D\d{3,4}\D{1,3}\d{1}")
        num_by_regex = re.findall(rgx_phone, source)[0]

        return num_by_regex
    except:
        pass

while True:
    checking = phone_by_href(adres)
    if checking is not None:
        break

    checking = phone_by_regex(adres)
    if checking is not None:
        break

    for name in names:
        code = adres + name
        checking = phone_by_href(code)
        checking = phone_by_regex(code)
        if checking is not None:
            break

    if checking is not None:
        break
    
    checking = 'Could not find a phone number'
    break

print(checking.strip())

driver.quit()
