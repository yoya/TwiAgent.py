# TwiAgent.py

Twitter Agent powered by Python Selenium

- Bookmark Download
- Setting Interests

Twitter API を使わず Chrome を Selenium で操作して自動化するツールです。
今のところブックマークの画像をダウンロードする機能が便利だと思います。

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

## login.py

以下のコマンドで起動するブラウザ上で、Twitter にログインして下さい。
ウィンドウをその後で閉じて大丈夫です。

```
% python login.py <profile_name>
```

<profile_name> はログイン状態を記憶する場所で任意の文字列を使えます。
拘りが無ければ、ログイン名にすると良いでしょう。

自分は以下のようにしてます。

```
% python login.py yoya
```

引数無しの実行で、今までに指定した Profile 名を表示出来ます。
Profile名を思い出せない時にお使い下さい。

```
% python login.py
yoya
```

# Bookmark Image Download

ブックマーク画像を D/L する機能です。

```
% python bookmark.py <profile_name>
```

## input

ログイン済みの Profile名が必要です。

- <profile_name>

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

興味(Interests) の設定をテキスト編集で変更できます。
まずは以下のコマンドを実行します。

```
% python interests.py <profile_name>
```
## input

ログイン済みの Profile名が必要です。

- <profile_name>

## output

- interestsOK.txt
- interestsNG.txt

## setting process

ファイルからキーワードを削除してから、

```
% python interests.py <profile_name>
```

これを実行すると、キーワードに対応するチェックが反転する。

- interestsOK.txt から消せば check が外れる
- interestsNG.txt から消せば check がつく

interestsOK.txt を空ファイルにすれば、全ての check が外れます
その状態から、interestsNG.txt から興味のあるキーワードを消して
check をつけると良いでしょう。
