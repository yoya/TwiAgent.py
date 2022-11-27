from TwiAgent import TwiAgent

class TwiAgentFollowers(TwiAgent):
    FOLLOWERS_URL = "https://twitter.com/followers"
    def openFollowers(self, cookieFile):
        url = self.FOLLOWERS_URL
        self.openBrowser(url, cookieFile)
    def readFollowers(self):
#        followers = self.readByCSSSelector(self.driver, 'div[aria-label="Timeline: Followers"]', wait=True)
        followers = self.readByCSSSelectorAll(self.driver, 'div[data-testid="cellInnerDiv"]', wait=True)
        print(followers)

        
        
