#!/usr/bin/env python3
"""Canva取り込み用 canva.html を index.html から生成する（動きと地図を保持する版）。
・フラップ表示とカウントダウンは初期状態を静的に書き出し、JSはその上で動かす（文字として編集可能にするため）
・ティッカーは1行の文字列に単純化（変換時の縦折れ防止）"""
import re, os, datetime
HERE = os.path.dirname(os.path.abspath(__file__))
s = open(os.path.join(HERE, "index.html"), encoding="utf-8").read()
s = s.replace('<meta name="robots" content="noindex"> <!-- 本公開時にこの行を削除（検索エンジンに載せる） -->\n', '')

# flap cells pre-rendered
def cells(txt):
    return "".join(f'<span class="c{" sp" if ch == " " else ""}">{"" if ch == " " else ch}</span>' for ch in txt)
s = re.sub(r'<div class="flap( wide)?" data-text="([^"]*)"></div>', lambda m: f'<div class="flap{m.group(1) or ""}" data-text="{m.group(2)}">{cells(m.group(2))}</div>', s)
s = s.replace("""  document.querySelectorAll('.flap').forEach(f => {
    f.innerHTML = [...f.dataset.text].map(ch => `<span class="c${ch === ' ' ? ' sp' : ''}">${ch === ' ' ? '' : ch}</span>`).join('');
  });
""", "")

# countdown pre-rendered with build-time values
T0 = datetime.datetime(2027, 1, 31, 3, 0, 0, tzinfo=datetime.timezone.utc)
diff = max(0, int((T0 - datetime.datetime.now(datetime.timezone.utc)).total_seconds()))
d, r = divmod(diff, 86400); h, r = divmod(r, 3600); m, sec = divmod(r, 60)
def digits(n, w): return "".join(f"<span>{c}</span>" for c in str(n).zfill(w))
s = re.sub(r'<div class="n" data-u="d">.*?</div>', f'<div class="n" data-u="d">{digits(d,3)}</div>', s, flags=re.S)
s = re.sub(r'<div class="n" data-u="h">.*?</div>', f'<div class="n" data-u="h">{digits(h,2)}</div>', s, flags=re.S)
s = re.sub(r'<div class="n" data-u="m">.*?</div>', f'<div class="n" data-u="m">{digits(m,2)}</div>', s, flags=re.S)
s = re.sub(r'<div class="n" data-u="s">.*?</div>', f'<div class="n" data-u="s">{digits(sec,2)}</div>', s, flags=re.S)

# ticker: one nowrap line, items inline
s = s.replace(".ticker .track { display: flex; width: max-content; animation: run 44s linear infinite; }",
              ".ticker .track { display: inline-block; white-space: nowrap; animation: run 44s linear infinite; }")
s = s.replace(".ticker .item { padding: 12px 32px 12px 0; font-size: 12px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; white-space: nowrap; display: flex; gap: 12px; align-items: center; }",
              ".ticker .item { display: inline-block; white-space: nowrap; padding: 12px 32px 12px 0; font-size: 12px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; }\n  .ticker .item i, .ticker .item em { margin-right: 12px; }")

open(os.path.join(HERE, "canva.html"), "w", encoding="utf-8").write(s)
print("canva.html", len(s), "flaps pre-rendered:", s.count('class="flap'), "countdown:", d, h, m, sec)
