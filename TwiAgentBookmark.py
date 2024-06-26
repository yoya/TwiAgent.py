from TwiAgent import TwiAgent
from selenium.common.exceptions import NoSuchElementException

class TwiAgentBookmark(TwiAgent):
    BOOKMARK_URL = "https://twitter.com/i/bookmarks"
    def openBookmark(self, profileName):
        url = self.BOOKMARK_URL
        self.openBrowser(url, profileName)
    # ブックマーク一覧を取得する
    def readBookmarkArticleList(self):
        return self.readByCSSSelectorAll(self.driver, 'article', wait=True)
    #
    # ブックマーク情報の１つから文字と画像を収集する
    #
    def readBookmarkArticle(self, article):
#        user = self.readByCSSSelector(article, 'div[data-testid="User-Names"]')
        user = self.readByCSSSelector(article, 'div[data-testid="User-Name"]')
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
        try:
            self.readByCSSSelector(article, 'div[aria-label="Embedded video"]')
            video = True
        except NoSuchElementException:
            video = False
        return href, text, imgsrcs, video
    #
    # 共有メニューのブックマーク削除メニューを選択する
    #
    def removeBookmarkArticle(self, article):
        remove = self.readByCSSSelector(article, 'button[data-testid="removeBookmark"]')
        self.click(remove)
    def loadArticle(self):
        self.scrollToBottom()
        self.waitCSSSelector('article')
