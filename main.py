# (c) 2022/05/22 yoya@awn.jp

import os, sys, time
from TwiBookmaDL import TwiBookmaDL
import json

prog, cookieFile = sys.argv;

BOOKMARK_URL = "https://twitter.com/i/bookmarks"

# setup

os.makedirs("media", exist_ok=True)

dl = TwiBookmaDL()
try:
    dl.openBrowser(BOOKMARK_URL, cookieFile)
    while (True):
        articles = dl.readBookmarkArticleList()
        articlesLen = len(articles)
        print("articles count:{}".format(articlesLen))
        if (articlesLen < 1):
            time.sleep(10)
            continue
        for article in articles:
            url, text, imgsrcs = dl.readBookmarkArticle(article)
            print(url)
            print("   ", text)
            print("   ", imgsrcs)
             dl.downloadPhotoImage(imgsrcs)
            #dl.clickBookmarkShareButton(article)
            time.sleep(10)
            break
        break
        
except Exception as e:
    print(e, file=sys.stderr)
    exit (1)
