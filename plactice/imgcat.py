import os, sys
import base64

def imgcat(filename, height):
    with open(filename, mode="rb") as f:
        imgdata = f.read()
        size = len(imgdata)
        name = base64.b64encode(filename.encode()).decode()
        data = base64.b64encode(imgdata).decode()
        print(";File=name={};size={};inline=1;height={}:".format(name, size, height), end = "")
        print(data, end = "")
        print("\007", end = "")

print("\033]1337", end = "")

for arg in sys.argv[1:]:
    imgcat(arg, 7)

print("")
