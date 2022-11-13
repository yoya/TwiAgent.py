# (c) 2022/05/22 yoya@awn.jp

import os, sys, time
import json
from urllib import parse
import shutil
from TwiAgentBookmark import TwiAgentBookmark

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

def main(agent, retry):
    articles = agent.readBookmarkArticleList()
    articlesLen = len(articles)
#    print("articles count:{}".format(articlesLen))
    if (articlesLen < 1):
        agent.loadArticle()
        return False  # soft error
    for article in articles:
        url, text, imgsrcs = agent.readBookmarkArticle(article)
        print(url, imgsrcs)
        logf.write("========\n{}\n{}\n{}\n\n".format(url, text, imgsrcs))
        imgsrcsLen = len(imgsrcs)
#        print("    imgsrcs count:{}".format(imgsrcsLen))
        for src in imgsrcs:
            imgurl, imgfile = url_to_origurl_filename(src)
            img = agent.downloadPhotoImage(imgurl)
            with open("media/{}".format(imgfile),'wb') as f:
                shutil.copyfileobj(img, f)
            agent.removeBookmarkArticle(article)
            time.sleep(3)
    return True

agent = TwiAgentBookmark()
agent.openBookmark(cookieFile)

retry = 0
while (retry < 3):  # 仏の顔も三度まで
    try:
        if main(agent, retry) == True:
            retry = 0
            time.sleep(3)
        else:
            retry = retry + 1
            time.sleep(5)
    except (agent.RetryException) as e:
        agent.refresh()
        time.sleep(10)
        retry = retry + 1  # soft error
        continue
    except (agent.FinishExceptions) as e:
        print("OK")
        break
    except Exception as e:
        print(sys.exception_info())
        print(e, file=sys.stderr)
        break
    except (agent.AbortExceptions) as e:
        print(sys.exception_info())
        print(e, file=sys.stderr)
        break
