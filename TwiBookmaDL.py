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
import requests

class TwiBookmaDL:
    def __init__(self):
        pass
    # ブラウザを開く
    def openBrowser(self, url, cookieFile):
        json_open = open(cookieFile, 'r')
        try:
            cookies = json.load(json_open)
            options = Options()
            #options.add_argument('--headless')
            prefs = {"intl.accept_languages": "en-us"}
            options.add_experimental_option("prefs",prefs)
            self.driver = webdriver.Chrome(options=options)
            self.driver.get(url)
            for cookie in cookies:
                tmp = {"name": cookie["name"], "value": cookie["value"]}
                self.driver.add_cookie(tmp)
        except json.decoder.JSONDecodeError as e:
            mesg = "Invalid Cookie JSON file({}) => {}".format(cookieFile, e)
            raise Exception(mesg)
    # ブックマーク一覧を取得する
    def readBookmarkArticleList(self):
        locator = (By.CSS_SELECTOR, 'article')
        wait = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(locator)
        )
        articles = self.driver.find_elements(*locator)
        return articles
    #
    # ブックマーク情報の１つから文字と画像を収集する
    #
    def readBookmarkArticle(self, article):
        user = article.find_element(By.CSS_SELECTOR, 'div[data-testid="User-Names"]')
        a = user.find_element(By.CSS_SELECTOR, 'a[href*="/status/"]')
        href = a.get_attribute("href")
        try:
            textElem = article.find_element(By.CSS_SELECTOR, 'div[data-testid="tweetText"]')
            text = textElem.text
        except NoSuchElementException:
            text = ""
        imgsrcs = []
        try:
            photos = article.find_elements(By.CSS_SELECTOR, 'div[data-testid="tweetPhoto"]')
        except NoSuchElementException:
            photos = []
        for photo in photos:
            imgs = photo.find_elements(By.CSS_SELECTOR, 'img')
            for img in imgs:
                src = img.get_attribute("src")
                imgsrcs.append(src)
        return href, text, imgsrcs
    #
    # 画像のダウンロードストリームを取得する
    #
    def downloadPhotoImage(self, src):
        r = requests.get(src, stream = True)
        if r.status_code == 200:
            r.raw.decode_content = True  #  mime encode は解く
            return r.raw  # filestream
        raise Exception("Can't get image:{}".format(src))
    #
    # 共有メニューのブックマーク削除メニューを選択する
    #
    def removeBookmarkArticle(self, article):
        locator = (By.CSS_SELECTOR, 'div[aria-label="Share Tweet"]')
        menu = article.find_element(*locator)
        self.driver.execute_script('arguments[0].click();', menu)
        locator = (By.XPATH, '//span[contains(text(),"Remove Tweet from Bookmarks")]')
        wait = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(locator)
        )
        remove = menu.find_element(*locator)
        self.driver.execute_script('arguments[0].click();', remove)
    def loadArticle(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight+1)")
        locator = (By.CSS_SELECTOR, 'article')
        wait = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(locator)
        )
    #
    # 画面リフレッシュ
    def refresh(self):
        self.driver.refresh()
