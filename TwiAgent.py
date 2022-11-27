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
    def openBrowser(self, url, cookieFile):
        json_open = open(cookieFile, 'r')
        try:
            cookies = json.load(json_open)
            options = Options()
            #options.add_argument('--headless')
            prefs = {"intl.accept_languages": "en-us"}  # 英語言語設定
            options.add_experimental_option("prefs",prefs)
            self.driver = webdriver.Chrome(options=options)
            self.driver.get(url)  # 初来訪サイトだと cookie をセット出来ない
            for cookie in cookies:
                tmp = {"name": cookie["name"], "value": cookie["value"]}
                self.driver.add_cookie(tmp)
            self.driver.get(url)  # cookie セットした状態でアクセスし直し
        except json.decoder.JSONDecodeError as e:
            mesg = "Invalid Cookie JSON file({}) => {}".format(cookieFile, e)
            raise Exception(mesg)
    # 画面リフレッシュ
    def refresh(self):
        self.driver.refresh()
    def click(self, element):
        self.driver.execute_script('arguments[0].click();', element)
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
    def readByXPATH(self, element, xpath, wait=False):
        locator = (By.XPATH, xpath)
        if wait:
            w = WebDriverWait(element, 10).until(
                EC.presence_of_element_located(locator)
            )
        return element.find_element(*locator)
