# (c) 2022/11/13 yoya@awn.jp

import os, sys, time
from operator import xor
from TwiAgentInterests import TwiAgentInterests
import shutil

prog, cookieFile = sys.argv;

INTERESTS_URL = "https://twitter.com/settings/your_twitter_data/twitter_interests"

OK_FILE = "interestsOK.txt"
NG_FILE = "interestsNG.txt"
OK_FILE_NEW = "interestsOK.new"
NG_FILE_NEW = "interestsNG.new"

exist_ok = os.path.isfile(OK_FILE)
exist_ng = os.path.isfile(NG_FILE)

if xor(exist_ok , exist_ng) == True:
    print("exist_ok:{} exist_ng:{}".format(exist_ok , exist_ng))
    exit (1)
exist_okng = exist_ok

os.makedirs("media", exist_ok=True)

okngTable = {}
if exist_okng:
    okf = open(OK_FILE, 'r')
    ngf = open(NG_FILE, 'r')
    for text in okf.read().split('\n'):
        okngTable[text] = True
    for text in ngf.read().split('\n'):
        okngTable[text] = False
    oknewf = open(OK_FILE_NEW, 'w')
    ngnewf = open(NG_FILE_NEW, 'w')
else:
    okf = open(OK_FILE, 'w')
    ngf = open(NG_FILE, 'w')

def main(agent):
    interests = agent.readSettingsInterestList()
    interestsLen = len(interests)
    print(" interests count:{}".format(interestsLen))
    if ( interestsLen < 1):
        return False  # soft error
    for interest in interests:
        info = agent.readSettingsInterest(interest)
        text = info["text"]
        checked = info["checked"]
        checkedNew = okngTable.get(text)
        if checkedNew is None:
            checkedNew = not checked  # OK にも NG にも存在しない時は逆にする
        if exist_okng:  # OK/NG が存在する場合は Twitter 設定に反映する
            if xor(checked, checkedNew) == True:
                print("text:{} checked:{} checkedNew:{}".format(text, checked, checkedNew))
                agent.toggleSettingsInterest(interest)
            if checkedNew:
                oknewf.write(text)
                oknewf.write("\n")
            else:
                ngnewf.write(text)
                ngnewf.write("\n")
        else:  # OK/NG が新規ファイルの場合は書き込むだけ
            if checked == True:
                okf.write(text)
                okf.write("\n")
            else:
                ngf.write(text)
                ngf.write("\n")
    return True

agent = TwiAgentInterests()
agent.openInterests(cookieFile)

main(agent)
