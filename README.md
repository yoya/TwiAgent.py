# TwiAgent.py

Twitter Agent powered by Python Selenium

- Bookmark Download
- Setting Interests

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

# Bookmark Image Download

```
% python bookmark.py cookie.json
```

## input

- cookie.json

## output

- tweet.txt
```
========
(URL)
(tweet text)
(img src list)
```

- media/*.(jpg|png)

# Setting Interests

```
% python interests.py cookie.json
```

## output

- interestsOK.txt
- interestsNG.txt

ファイルからキーワードを削除してから、

```
% python interests.py cookie.json
```

これを実行すると、キーワードに対応するチェックが反転する。

interestsOK.txt から消せば check が外れる
interestsNG.txt から消せば check がつく
