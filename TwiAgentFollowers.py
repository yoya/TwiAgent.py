from TwiAgent import TwiAgent
import time
from selenium.common.exceptions import StaleElementReferenceException

class TwiAgentFollowers(TwiAgent):
    FOLLOWERS_URL = "https://twitter.com/followers"
    def openFollowers(self, profileName):
        url = self.FOLLOWERS_URL
        self.openBrowser(url, profileName)
    def readFollowers(self):
#        followers = self.readByCSSSelectorAll(self.driver, 'div[data-testid="cellInnerDiv"]', wait=True)
        followersUsername = []
        done = False
        while not done:
            followers = self.readByCSSSelectorAll(self.driver, 'div[data-testid="UserCell"]', wait=True)
            print(len(followers))
            try:
                done = True
                for f in followers:
                    xpath = './/a/div/div/span[contains(text(),"@")]';
                    users = self.readByXPATHAll(f, xpath, wait=True)
                    for u in users:
                        print(u.text)
                        if u.text not in followersUsername:
                            followersUsername.append(u.text)
                            done = False
                if not done:
                    print("scroll")
                    self.scrollToBottom()
            except StaleElementReferenceException as e:
                print("stale element")
                done = False
                time.sleep(1)
                break
            time.sleep(3)
        return followersUsername
