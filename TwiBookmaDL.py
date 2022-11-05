# pip install selenium

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class TwiBookmaDL:
    options = Options()
    driver = webdriver.Chrome(options=options)
    def __init__(self):
    def openBrowser(self, url, cookieFile):
        print('openBrowser', url, cookieFile)

