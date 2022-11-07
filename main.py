# (c) 2022/05/22 yoya@awn.jp

import os, sys, time
from TwiBookmaDL import TwiBookmaDL
import json
from urllib import parse
import shutil

prog, cookieFile = sys.argv;

BOOKMARK_URL = "https://twitter.com/i/bookmarks"

def url_to_origurl_filename(src):
    up = parse.urlparse(src)
    qs = parse.parse_qs(up.query)
    fmt = qs['format'][0]
    url = "{}://{}{}?format={}&name=orig".format(up.scheme, up.netloc, up.path, fmt)
    filename = "{}.{}".format(up.path.split('/')[-1], fmt);
    return [url, filename]

# setup

os.makedirs("media", exist_ok=True)
logf = open("tweet.txt", 'a')

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
            logf.write("========\n{}\n{}\n{}".format(url, text, imgsrcs))
            for src in imgsrcs:
                imgurl, imgfile = url_to_origurl_filename(src)
                print(imgurl, imgfile)
                img = dl.downloadPhotoImage(imgurl)
                with open("media/{}".format(imgfile),'wb') as f:
                    shutil.copyfileobj(img, f)
            #dl.clickBookmarkShareButton(article)
            time.sleep(10)
            break
        break
        
except Exception as e:
    print(e, file=sys.stderr)
    exit (1)
