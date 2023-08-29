import sys, os
import re, requests, shutil

prog, indir = sys.argv
files = os.listdir(indir)
for f in files:
    inpath = "{}/{}".format(indir, f)
    s = re.split('[/.]', f)
    id = s[-2]
    ext = s[-1]
    if ext != "webp":
        continue
    outpath = "{}/{}.{}".format(indir, id, "png")
    url = "https://pbs.twimg.com/media/{}?format=png&name=4096x4096".format(id);
    print(inpath, outpath, url)
    res = requests.get(url, stream = True)
    if res.status_code == 200:
        res.raw.decode_content = True  #  mime encode は解く
        with open(outpath, 'wb') as f:
            shutil.copyfileobj(res.raw, f)
            print("{} got".format(outpath))
            os.remove(inpath)
    else:
        print("res.status_code:{} url:{}".format(res.status_code, url))
