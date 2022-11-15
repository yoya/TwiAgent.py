from TwiAgent import TwiAgent
from util import htmldump

class TwiAgentInterests(TwiAgent):
    INTERESTS_URL = "https://twitter.com/settings/your_twitter_data/twitter_interests"
    def __init__(self):
        pass
        # ブックマークを開く
    def openInterests(self, cookieFile):
        url = self.INTERESTS_URL
        self.openBrowser(url, cookieFile)
    def readSettingsInterestList(self):
#        detail = self.readByCSSSelectorAll(self.driver, 'section[aria-label="Section details"', wait = True)
        checkboxes = self.readByCSSSelectorAll(self.driver, 'input[type="checkbox"]', wait = True)
        interests = []
        for cb in checkboxes:
            elem = self.readByXPATH(cb, "../..")
            interests.append(elem)
        return interests
    def readSettingsInterest(self, interest):
#        htmldump(interest)
        text = interest.text
        checkbox = self.readByCSSSelector(interest, 'input[type="checkbox"]')
        if checkbox.get_attribute("checked") == "true":
            checked = True
        else:
            checked = False
        return { 'text':text, 'checked':checked }
    def toggleSettingsInterest(self, interest):
        checkbox = self.readByCSSSelector(interest, 'input[type="checkbox"]')
        self.click(checkbox)
