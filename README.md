# JAZZ EMP vol.9 Official Website

公開URL: https://kimussarazu226.github.io/jazz-emp-2027/

## 編集のしかた
- 直すファイルは **`index.html` だけ**。GitHub上で鉛筆アイコンを押して編集 → 「Commit changes」で保存すると、1分ほどで公開ページに反映されます
- ファイル内に `<!-- ▼ ... -->` の目印があり、出演者・時間割・チケット・お知らせなど、直す場所が分かるようになっています
- 画像は `assets/` に入れて、`index.html` から `assets/ファイル名` で参照します
- 本公開のときは `<meta name="robots" content="noindex">` の行を削除します

## ローカルで確認したいとき
```
python3 -m http.server 8787
```
→ http://localhost:8787

## その他
- `make_artifact.py` は Claude のプレビュー生成用。通常は使いません
