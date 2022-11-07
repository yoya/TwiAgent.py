# pip install selenium

#import time
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
        print("wait", wait)
        articles = self.driver.find_elements(*locator)
        print("articles count:{}".format(len(articles)))
        return articles
    # ブックマーク情報の１つから文字と画像を収集する
    def readBookmarkArticle(self, article):
        user = article.find_element(By.CSS_SELECTOR, 'div[data-testid="User-Names"]')
        a = user.find_element(By.CSS_SELECTOR, 'a[href*="/status/"]')
        href = a.get_attribute("href")
        text = article.find_element(By.CSS_SELECTOR, 'div[data-testid="tweetText"]')
        imgsrcs = []
        photos = article.find_elements(By.CSS_SELECTOR, 'div[data-testid="tweetPhoto"]')
        for photo in photos:
            imgs = photo.find_elements(By.CSS_SELECTOR, 'img')
            print("imgs len:{}".format(len(imgs)))
            for img in imgs:
#            print("img", img, img.get_attribute('outerHTML'))
                src = img.get_attribute("src")
                imgsrcs.append(src)
        return href, text.text, imgsrcs
    #
    def downloadPhotoImage(self, imgsrcs):
        pass
    # 共有ボタンをクリックして、ポップアップめんニューを出す
    def clickBookmarkShareButton(self, article):
        print("clickBookmarkShareButton", article.get_attribute('outerHTML'))
        locator = (By.CSS_SELECTOR, 'div[aria-label="Share Tweet"]')
#        menus = article.find_elements(*locator)
        menu = article.find_element(*locator)
        print(menu)
        self.driver.execute_script('arguments[0].click();', menu)
