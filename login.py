# (c) 2023/01/29 yoya@awn.jp

import sys
import util
from TwiAgent import TwiAgent

TWITTER_URL = "https://twitter.com/"

if len(sys.argv) < 2:
    util.listProfile()
    exit(0)

prog, profileName = sys.argv;

agent = TwiAgent()
agent.openBrowser(TWITTER_URL, profileName)

# ログイン後の画面が出るのを確認
agent.waitCSSSelector(agent.driver, 'article', 60*10)
