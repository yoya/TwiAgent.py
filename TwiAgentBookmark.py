from TwiAgent import TwiAgent
from selenium.common.exceptions import NoSuchElementException

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
        menu = self.readByCSSSelector(article, 'div[aria-label="Share Tweet"]')
        self.click(menu)
        xpath = '//span[contains(text(),"Remove Tweet from Bookmarks")]'
        remove = self.readByXPATH(menu, xpath, wait=True)
        self.click(remove)
    def loadArticle(self):
        self.scrollToBottom()
        self.waitCSSSelector('article')
