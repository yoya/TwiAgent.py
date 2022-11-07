# TwiBookmaDL.py

Twitter Bookmark Downloader powered by Python Selenium

# require

- Apple macOS Monterey 以降

- Google Chrome 最近のバージョン

- Python 3.10.8
  - https://www.python.org/

- Chrome driver (実行ファイル)
  - https://chromedriver.chromium.org/downloads

# setup

- Python をインストールする
- Chrome driver を実行パスに設置する
  - バージョン更新が多いので $HOME/bin/ だと楽かも。

## pip install

```
% pip install -r requirements.txt
```

## cookie.json

- EditThisCookie
  - https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg/

- usage
   - Chrome で twitter.com を開いて対象ユーザでログインします
   - Chrome 拡張の EditThisCookie を開きます
      - cookie export (タブの右から３番目) をクリックします。
   - cookie.json を作って clipboard 内のテキストを保存します。

```
% python main.py cookie.json
```

# input

- cookie.json

# output

- tweet.txt
```
====
(URL)
(tweet text)
(img src)
```

- media/*.(jpeg|png)
