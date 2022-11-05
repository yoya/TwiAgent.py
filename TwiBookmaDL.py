# pip install selenium

import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

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
