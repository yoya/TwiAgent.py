# (c) 2022/11/13 yoya@awn.jp

import os, sys, time
import json
from urllib import parse
import shutil
from TwiAgent import TwiAgent
from TwiAgentBookmark import TwiAgentBookmark
from util import imgcat, youtubeDl

prog, profileName = sys.argv[:2];
listfile = sys.argv[2] if len(sys.argv) > 2 else None

def url_to_origurl_filename(src, fmt = None):
    up = parse.urlparse(src)
    qs = parse.parse_qs(up.query)
    if fmt is None:
        fmt = qs['format'][0]
    url = "{}://{}{}?format={}&name=orig".format(up.scheme, up.netloc, up.path, fmt)
    # url = "{}://{}{}?format={}&name=4096x4096".format(up.scheme, up.netloc, up.path, fmt)
    filename = "{}.{}".format(up.path.split('/')[-1], fmt);
    return [url, filename, fmt]

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
        url, text, imgsrcs, video = agent.readBookmarkArticle(article)
        print(url, "imgsrcs len:{}".format(len(imgsrcs)))
        logf.write("========\n{}\n{}\n{}\n\n".format(url, text, imgsrcs))
        imgsrcsLen = len(imgsrcs)
#        print("    imgsrcs count:{}".format(imgsrcsLen))
        found = False
        for src in imgsrcs:
            dlDone = False  # download したフラグ
            isFile = False
            for f in ["png", "jpg"]:
                imgurl, imgfile, fmt = url_to_origurl_filename(src, f)
                imgfile = "media/{}".format(imgfile)
                if os.path.isfile(imgfile):
                    isFile = True
                    break
            if isFile:
                print("already downloaded: {}".format(imgfile))
                continue  # already downloaded
            imgurl, imgfile, fmt = url_to_origurl_filename(src, None)
            fmtList = [fmt]
            if fmt == "webp":
                fmtList = ["png", "jpg"]
            for f in fmtList:
                imgurl, imgfile, fmt = url_to_origurl_filename(src, f)
                imgfile = "media/{}".format(imgfile)
                try:
                    img = agent.downloadPhotoImage(imgurl)
                    dlDone = True
                except Exception as e:
                    dlDone = False;  # D/L 失敗
                if dlDone is False:
                    print("download failed:{}".format(imgurl))
                    continue
                with open(imgfile, 'wb') as f:
                    shutil.copyfileobj(img, f)
                    if os.environ["TERM_PROGRAM"] == "iTerm.app":
                        imgcat(imgfile, 10)
                        time.sleep(2)
            if video:
                videoId = url.split("/")[-1]
                print("url, videoId:", url, videoId)
                youtubeDl(url, "media/{}.mp4".format(videoId))
        if True:  # found is True:
            agent.removeBookmarkArticle(article)
            time.sleep(2)
    return True

def mainAdd(agent, listfile):
    with open(listfile, 'r') as f:
        lines = []
        for line in f.readlines():
            lines.append(line.rstrip())
        f.close()
        for line in lines:
            retry = 0
            while (retry < 3):
                url = line
                print(url)
                try:
                    agent.driver.get(url)
                    add = agent.readByCSSSelector(agent.driver, 'div[data-testid="bookmark"]', wait=True)
                    agent.click(add)
                    retry = 3
                    time.sleep(3)
                except (agent.RetryException) as e:
                    # ネットワーク不調の時はここ
                    agent.refresh()
                    retry = retry + 1
                    time.sleep(10)
                except (agent.FinishExceptions) as e:
                    # 削除されてる時ここにくる
                    print("FinishExcepton:", e)
                    retry = 3
                    time.sleep(10)
                except Exception as e:
                    print("Exception:", e)
                    return
    return True

if listfile is not None:
    agent = TwiAgent()
    agent.openBrowser("https://awm.jp/", profileName)
    mainAdd(agent, listfile)
    exit(0)

agent = TwiAgentBookmark()
agent.openBookmark(profileName)

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
#        print(sys.exception_info())
        print(e, file=sys.stderr)
        print("Retry")
        agent.refresh()
        retry = retry + 1  # soft error
        time.sleep(10)
        continue
    except (agent.AbortExceptions) as e:
        print(sys.exception_info())
        print(e, file=sys.stderr)
        print("Abort")
        break
