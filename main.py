# (c) 2022/05/22 yoya@awn.jp

import sys, time
from TwiBookmaDL import TwiBookmaDL
import json

prog, cookieFile = sys.argv;

BOOKMARK_URL = "https://twitter.com/i/bookmarks"

dl = TwiBookmaDL()
try:
    dl.openBrowser(BOOKMARK_URL, cookieFile)
except Exception as e:
    print(e)
    exit (1)
    
time.sleep(5)
