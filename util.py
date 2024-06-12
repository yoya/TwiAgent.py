import os, base64, subprocess

#YouTubeDL = "youtube-dl"
YouTubeDL = "yt-dlp"
ImageMagick = "magick"

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

ProfileName = "Profile 8"  # XXX

def youtubeDl(url, filename):
    print("youtubeDl")
    try:
        result = subprocess.run([YouTubeDL, "-help"], capture_output=True)
    except FileNotFoundError as e:
        print(e)
        return
    result = subprocess.run([YouTubeDL, url, "-o", filename, "--cookies-from-browser", "chrome:{}".format(ProfileName)])
    print(result)

#url = "https://twitter.com/yoya/status/1636393346452291588"
#folder = "1636393346452291588.mp4"
#youtubeDl(url, folder)

def htmldump(element):
    print(element.get_attribute('outerHTML'))

def listProfile():
    with os.scandir(".") as it:
        for entry in it:
            if entry.is_dir():
                name = entry.name
                sessionsPath = "{}/Default/Sessions/".format(name);
                if os.path.isdir(sessionsPath):
                    print(name)

def isEqualImage(imgfile1, imgfile2):
    try:
        result = subprocess.run([ImageMagick, "compare", "-h"], capture_output=True)
    except FileNotFoundError as e:
        return
    result = subprocess.run([ImageMagick, "compare", "-metric", "PSNR", imgfile1, imgfile2, "NULL:"], capture_output=True)
    print(result)
