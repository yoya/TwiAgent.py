import sys, os, time
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from TwiAgent import TwiAgent

url = "https://pwiki.awm.jp/~yoya/"
cookieFile = "pwiki.cookie"
agent = TwiAgent()
agent.openBrowser(url, cookieFile)
time.sleep(10)
