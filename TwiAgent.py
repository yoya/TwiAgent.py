# pip install selenium requests

#import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# find_elements
from selenium.webdriver.common.by import By
# wait for page load
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchWindowException, TimeoutException
import requests

class TwiAgent:
    AbortExceptions = (NoSuchElementException)
    RetryException  = (StaleElementReferenceException)
    FinishExceptions = (NoSuchWindowException, TimeoutException)
    def __init__(self):
        pass
    # ブラウザを開く
    def openBrowser(self, url, profileName):
        options = Options()
        #options.add_argument('--headless')
        options.add_argument('--user-data-dir={}'.format(profileName))
        prefs = {"intl.accept_languages": "en-us"}  # 英語言語設定
        options.add_experimental_option("prefs",prefs)
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(url)
    # 画面リフレッシュ
    def refresh(self):
        self.driver.refresh()
    def click(self, element):
        self.driver.execute_script('arguments[0].click();', element)
    def scrollTo(self, offset):
        self.driver.execute_script("window.scrollTo(0, {})".format(offset))
    def scrollToBottom(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight+1)")
    #
    # 画像のダウンロードストリームを取得する
    #
    def downloadPhotoImage(self, src):
        r = requests.get(src, stream = True)
        if r.status_code == 200:
            r.raw.decode_content = True  #  mime encode は解く
            return r.raw  # filestream
        raise Exception("Can't get image:{}".format(src))
    def readByCSSSelectorAll(self, element, selector, wait=False):
        locator = (By.CSS_SELECTOR, selector)
        if wait:
            w = WebDriverWait(element, 10).until(
                EC.presence_of_element_located(locator)
            )
        return element.find_elements(*locator)
    def readByCSSSelector(self, element, selector, wait=False):
        locator = (By.CSS_SELECTOR, selector)
        if wait:
            w = WebDriverWait(element, 10).until(
                EC.presence_of_element_located(locator)
            )
        return element.find_element(*locator)
    def readByXPATHAll(self, element, xpath, wait=False):
        locator = (By.XPATH, xpath)
        if wait:
            w = WebDriverWait(element, 10).until(
                EC.presence_of_element_located(locator)
            )
        return element.find_elements(*locator)
    def readByXPATH(self, element, xpath, wait=False):
        locator = (By.XPATH, xpath)
        if wait:
            w = WebDriverWait(element, 10).until(
                EC.presence_of_element_located(locator)
            )
        return element.find_element(*locator)
    def wait(self, element, locator, timeout = None):
        if timeout is None:
            timeout = 10  # default timeout
        return WebDriverWait(element, timeout).until(
            EC.presence_of_element_located(locator)
        )
    def waitCSSSelector(self, element, selector, timeout = None):
        return self.wait(element,(By.CSS_SELECTOR, selector), timeout)
    def waitPATH(self, element, xpath, timeout = None):
        return self.wait(self, element, (By.XPATH, xpath), timeout)
