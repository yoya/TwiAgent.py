# TwiBookmaDL.py

Twitter Bookmark Downloader powered by Python Selenium

# require

- Apple macOS modern version

- Google Chrome latest version

- Python 3.10.8
  - https://www.python.org/

- Chrome driver (execution file)
  - https://chromedriver.chromium.org/downloads

# setup

- python をインストールする
- chrome driver を実行パスに設置する
  - バージョン更新が多いので $HOME/bin/ だと楽かも。

## pip install

```
% pip install -r requirements.txt
```

## cookie.json

- EditThisCookie
  - https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg/

- usage
   - Chrome, open twitter.com & login by target account
   - EditThisCookie, open chrome extension
      - click cookie export (third tab from the right)
   - From clipboard, save to cookie.txt


# input

- cookie.json

# output

- tweet.txt
====
(URL)
(tweet text)

- media/*.(jpeg|png)
