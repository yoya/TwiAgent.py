from TwiAgent import TwiAgent

class TwiAgentInterests(TwiAgent):
    # Privary and Safety > Ads preferences > Interests
    INTERESTS_URL = "https://twitter.com/settings/your_twitter_data/twitter_interests"
    def __init__(self):
        pass
        # ブックマークを開く
    def openInterests(self, profileName):
        url = self.INTERESTS_URL
        self.openBrowser(url, profileName)
    def readSettingsInterestList(self):
        checkboxes = self.readByCSSSelectorAll(self.driver, 'input[type="checkbox"]', wait = True)
        interests = []
        for cb in checkboxes:
            elem = self.readByXPATH(cb, "../..")
            interests.append(elem)
        return interests
    def readSettingsInterest(self, interest):
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
