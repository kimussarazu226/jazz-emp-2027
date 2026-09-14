#!/usr/bin/env python3
"""Canva取り込み用の静的版 canva.html を index.html から生成する。
動き（カウントダウン・ティッカー・フラップ）を静的な文字に置き換え、各セクションをCanvaのページとして印付けする。"""
import re, os
HERE = os.path.dirname(os.path.abspath(__file__))
s = open(os.path.join(HERE, "index.html"), encoding="utf-8").read()

# 1) scripts out
s = re.sub(r"<!-- ▼ ここから下は動きの仕組み。文章の修正では触らない -->\s*<script>.*?</script>\s*", "", s, flags=re.S)
s = s.replace('<meta name="robots" content="noindex"> <!-- 本公開時にこの行を削除（検索エンジンに載せる） -->\n', '')

# 2) nav clock out
s = s.replace('      <li class="keep"><span class="clock" id="clock">TOKYO --:--:--</span></li>\n', '')

# 3) countdown -> static opening line
s = re.sub(r'<div class="count" id="count">.*?</div>\s*</div>\s*</div>',
           '<div class="count"><span class="eyebrow">Opening</span><span class="static-open">2027.01.31 Sun 12:00</span></div>', s, count=1, flags=re.S)

# 4) ticker -> one static paragraph
items = re.findall(r'<div class="item"(?: lang="ja")?><i>([▲■])</i>(.*?)<em>(.*?)</em></div>', s)
line = "　".join(f"{m} {t} {e}" for m, t, e in items)
s = re.sub(r'<div class="ticker" aria-hidden="true">.*?</div>\s*</div>\s*</div>',
           f'<div class="ticker-static" lang="ja">{line}</div>\n  </div>', s, count=1, flags=re.S)

# 5) flap board -> plain text cells
s = re.sub(r'<div class="flap" data-text="([^"]*)"></div>', r'<div class="tt-time">\1</div>', s)
s = re.sub(r'<div class="flap wide" data-text="([^"]*)"></div>', r'<div class="tt-what">\1</div>', s)

# 6) mark pages for Canva (one per block)
pages = [
    ('<header class="nav">', '<header class="nav" data-document-role="page" data-label="Nav">'),
    ('<section class="hero" id="hero">', '<section class="hero" id="hero" data-document-role="page" data-label="Hero">'),
    ('<div class="band">', '<div class="band" data-document-role="page" data-label="Info band">'),
    ('<section class="section" id="about">', '<section class="section" id="about" data-document-role="page" data-label="About">'),
    ('<section class="section" id="lineup">', '<section class="section" id="lineup" data-document-role="page" data-label="Lineup">'),
    ('<section class="section" id="program">', '<section class="section" id="program" data-document-role="page" data-label="Program">'),
    ('<section class="section" id="ticket">', '<section class="section" id="ticket" data-document-role="page" data-label="Ticket">'),
    ('<section class="section" id="access">', '<section class="section" id="access" data-document-role="page" data-label="Access">'),
    ('<section class="section" id="notice">', '<section class="section" id="notice" data-document-role="page" data-label="Notice">'),
    ('<section class="section" id="news">', '<section class="section" id="news" data-document-role="page" data-label="News">'),
    ('<section class="section" id="credit">', '<section class="section" id="credit" data-document-role="page" data-label="Credit">'),
    ('<footer class="footer">', '<footer class="footer" data-document-role="page" data-label="Footer">'),
]
for a, b in pages:
    assert a in s, a
    s = s.replace(a, b, 1)

# 7) static styles for the replaced parts; fixed desktop width for a predictable conversion
s = s.replace("</style>", """
  /* —— Canva import edition —— */
  body { width: 1366px; margin: 0 auto; }
  .count .static-open { font-weight: 800; font-size: 26px; letter-spacing: -0.03em; }
  .ticker-static { font-family: var(--jp); font-size: 13px; font-weight: 700; letter-spacing: 0.04em; padding: 14px var(--pad); line-height: 1.8; }
  .tt-time { font-weight: 800; font-size: 22px; font-variant-numeric: tabular-nums; letter-spacing: -0.02em; }
  .tt-what { font-family: var(--jp); font-weight: 700; font-size: 20px; }
  .wordmark .l { font-variation-settings: normal; }
</style>""", 1)

open(os.path.join(HERE, "canva.html"), "w", encoding="utf-8").write(s)
print("canva.html", len(s), "pages", s.count('data-document-role="page"'))
