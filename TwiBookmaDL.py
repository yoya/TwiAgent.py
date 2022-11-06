# pip install selenium

import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# find_elements
from selenium.webdriver.common.by import By
# wait for page load
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TwiBookmaDL:
    def __init__(self):
        options = Options()
        self.driver = webdriver.Chrome(options=options)
    def openBrowser(self, url, cookieFile):
        self.driver.get(url)
        json_open = open(cookieFile, 'r')
        try:
            cookies = json.load(json_open)
            for cookie in cookies:
                tmp = {"name": cookie["name"], "value": cookie["value"]}
                self.driver.add_cookie(tmp)
        except json.decoder.JSONDecodeError as e:
            mesg = "Invalid Cookie JSON file({}) => {}".format(cookieFile, e)
            raise Exception(mesg)
    def readBookmarkArticles(self):
        locator = (By.CSS_SELECTOR, 'article')
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(locator)
        )
        articles = self.driver.find_elements(*locator)
        print("articles count:{}".format(len(articles)))
        return articles
