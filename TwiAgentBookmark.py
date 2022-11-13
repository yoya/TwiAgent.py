# find_elements
from selenium.webdriver.common.by import By
# wait for page load
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchWindowException, TimeoutException

from TwiAgent import TwiAgent

class TwiAgentBookmark(TwiAgent):
    BOOKMARK_URL = "https://twitter.com/i/bookmarks"
    def openBookmark(self, cookieFile):
        url = self.BOOKMARK_URL
        self.openBrowser(url, cookieFile)
    # ブックマーク一覧を取得する
    def readBookmarkArticleList(self):
        return self.readByCSSSelectorAll(self.driver, 'article', wait=True)
    #
    # ブックマーク情報の１つから文字と画像を収集する
    #
    def readBookmarkArticle(self, article):
        user = self.readByCSSSelector(article, 'div[data-testid="User-Names"]')
        a = self.readByCSSSelector(article, 'a[href*="/status/"]')
        href = a.get_attribute("href")
        try:
            textElem = self.readByCSSSelector(article, 'div[data-testid="tweetText"]')
            text = textElem.text
        except NoSuchElementException:
            text = ""
        imgsrcs = []
        try:
            photos = self.readByCSSSelectorAll(article, 'div[data-testid="tweetPhoto"]')
        except NoSuchElementException:
            photos = []
        for photo in photos:
            imgs = self.readByCSSSelectorAll(photo, 'img')
            for img in imgs:
                src = img.get_attribute("src")
                imgsrcs.append(src)
        return href, text, imgsrcs
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
