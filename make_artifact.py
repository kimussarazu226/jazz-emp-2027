#!/usr/bin/env python3
"""Claude用プレビュー生成（通常の編集では不要）。index.html を読み、アーティファクト向けに変換する。"""
import base64, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
s = open(os.path.join(HERE, "index.html"), encoding="utf-8").read()
inner = s.split("<title>", 1)[1].rsplit("</body>", 1)[0]
inner = "<title>" + inner
b64 = base64.b64encode(open(os.path.join(HERE, "assets/keyvisual.webp"), "rb").read()).decode()
fb = f'<script>window.__KV_FALLBACK="data:image/webp;base64,{b64}";</script>\n'
inner = inner.replace('src="assets/keyvisual.webp"', 'src="/_blob/c2bc8141ea2c23399e286239a9ebfe83"').replace("<script>\n(() => {", fb + "<script>\n(() => {", 1)
open(sys.argv[1], "w", encoding="utf-8").write(inner)
print("artifact written", sys.argv[1])
