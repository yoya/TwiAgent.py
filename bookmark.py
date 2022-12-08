# (c) 2022/11/13 yoya@awn.jp

import os, sys, time
import json
from urllib import parse
import shutil
from TwiAgentBookmark import TwiAgentBookmark
from util import imgcat

prog, cookieFile = sys.argv;

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
        print(url, "imgsrcs len:{}".format(len(imgsrcs)))
        logf.write("========\n{}\n{}\n{}\n\n".format(url, text, imgsrcs))
        imgsrcsLen = len(imgsrcs)
#        print("    imgsrcs count:{}".format(imgsrcsLen))
        for src in imgsrcs:
            imgurl, imgfile = url_to_origurl_filename(src)
            img = agent.downloadPhotoImage(imgurl)
            imgfile = "media/{}".format(imgfile)
            with open(imgfile, 'wb') as f:
                shutil.copyfileobj(img, f)
                print(imgurl)
                if os.environ["TERM_PROGRAM"] == "iTerm.app":
                    imgcat(imgfile, 8)
            time.sleep(3)
        agent.removeBookmarkArticle(article)
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
        time.sleep(5)
        retry = retry + 1  # soft error
        continue
    except (agent.FinishExceptions) as e:
#        print(sys.exception_info())
#        print(e, file=sys.stderr)
        print("OK")
        break
    except Exception as e:
        print(sys.exception_info())
        print(e, file=sys.stderr)
        print("Retry")
        time.sleep(10)
        break
    except (agent.AbortExceptions) as e:
        print(sys.exception_info())
        print(e, file=sys.stderr)
        print("Abort")
        break
