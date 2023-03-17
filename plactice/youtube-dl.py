import subprocess

YouTubeDL = "youtube-dl"

#  youtube-dl https://twitter.com/pedori3/status/1578342845748252673  -o ../media/1578342845748252673.mp4
def youtubeDl(url, filename):
    try:
        result = subprocess.run([YouTubeDL, "-help"], capture_output=True)
    except FileNotFoundError as e:
        return 
    result = subprocess.run([YouTubeDL, url, "-o", filename])

url = "https://twitter.com/yoya/status/1636393346452291588"
folder = "1636393346452291588.mp4"
youtubeDl(url, folder)
