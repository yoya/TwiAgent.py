# (c) 2022/05/22 yoya@awn.jp

import sys
from TwiBookmaDL import TwiBookmaDL

prog, url, cookieFile = sys.argv;

dl = TwiBookmaDL()
dl.openBrowser(url, cookieFile)
