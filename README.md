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

「興味」設定のキーワードにチェックが入っているものを OK、外れているものを NG に入れます。(NG にした項目はすぐ消えるので、NG ファイルが空の事が結構あります)

- interestsOK.txt
- interestsNG.txt

## 2回目以降

interestsOK.txt、interestsNG.txt の中に並ぶ文字列の  OK/NG を入れ替えたいキーワードの頭に空白を追加して、以下のコマンドを実行して下さい。
interestsOK.txt で新規に追加されたキーワードは "+ " が頭につくので、OK に残したい場合は "+ " を削除。NG に移したい倍は "+" だけ消して空白を頭に残して下さい。

例えば、interestsOK.txt に以下の２つが追加された場合。

```
+ tameninarukoto
+ kudaranaikoto
```

以下のように編集して、再び interests.py コマンドを叩く事で、１つ目を残し、2つ目を NG ファイルに移動させて、それをツイッターの設定に反省させる事もできます。

```
tameninarukoto
 kudaranaikoto
```
