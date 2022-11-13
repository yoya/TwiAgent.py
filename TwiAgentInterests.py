import TwiAgent

class TwiAgentInterests(TwiAgent):
    INTERESTS_URL = "https://twitter.com/settings/your_twitter_data/twitter_interests"
    def __init__(self):
        pass
        # ブックマークを開く
    def openInterests(self, cookieFile):
        url = self.INTERESTS_URL
        self.openBrowser(url, cookieFile)
