# (c) 2022/11/28 yoya@awn.jp

import os, sys, time
from TwiAgentFollowers import TwiAgentFollowers

prog, cookieFile = sys.argv;

def main(agent):
    followers = agent.readFollowers()
    print(followers)
    
agent = TwiAgentFollowers()
agent.openFollowers(cookieFile)
main(agent)


