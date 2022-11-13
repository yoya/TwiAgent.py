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

def main(dl, retry):
    articles = dl.readBookmarkArticleList()
    articlesLen = len(articles)
#    print("articles count:{}".format(articlesLen))
    if (articlesLen < 1):
        dl.loadArticle()
        return False  # soft error
    for article in articles:
        url, text, imgsrcs = dl.readBookmarkArticle(article)
        print(url, imgsrcs)
        logf.write("========\n{}\n{}\n{}\n\n".format(url, text, imgsrcs))
        imgsrcsLen = len(imgsrcs)
#        print("    imgsrcs count:{}".format(imgsrcsLen))
        for src in imgsrcs:
            imgurl, imgfile = url_to_origurl_filename(src)
            img = dl.downloadPhotoImage(imgurl)
            with open("media/{}".format(imgfile),'wb') as f:
                shutil.copyfileobj(img, f)
            dl.removeBookmarkArticle(article)
            time.sleep(3)
    return True

dl = TwiBookmaDL()
dl.openBrowser(BOOKMARK_URL, cookieFile)

retry = 0
while (retry < 3):  # 仏の顔も三度まで
    try:
        if main(dl, retry) == True:
            retry = 0
            time.sleep(3)
        else:
            retry = retry + 1
            time.sleep(5)
    except (dl.RetryException) as e:
        dl.refresh()
        time.sleep(10)
        retry = retry + 1  # soft error
        continue
    except (dl.FinishExceptions) as e:
        print("OK")
        break
    except Exception as e:
        print(sys.exception_info())
        print(e, file=sys.stderr)
        break
    except (dl.AbortExceptions) as e:
        print(sys.exception_info())
        print(e, file=sys.stderr)
        break
