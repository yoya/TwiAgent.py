import base64

# https://iterm2.com/documentation-one-page.html#documentation-images.html
# ESC]1337;File=name={};size={};inline=1;height={}:   .. ^G\n
# ESC = 0x1B = 033
# ^G  = 0x07 = 007

def imgcat(filename, height):
    with open(filename, mode="rb") as f:
        imgdata = f.read()
        size = len(imgdata)
        name = base64.b64encode(filename.encode()).decode()
        data = base64.b64encode(imgdata).decode()
        print("\033]1337;File=name={};size={};inline=1;height={}:".format(name, size, height), end = "")
        print(data, end = "")
        print("\007")

# import os, sys
#if os.environ["TERM_PROGRAM"] == "iTerm.app":
#    imgcat(sys.argv[1], 7)

def htmldump(element):
    print(element.get_attribute('outerHTML'))
