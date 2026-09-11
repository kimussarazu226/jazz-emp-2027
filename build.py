#!/usr/bin/env python3
"""Build index.html (public site) and jazz-emp.html (Claude artifact preview) from template.html.

template.html is the single source of truth. __KV__ is replaced with the key-visual reference.
"""
import base64, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
tpl = open(os.path.join(HERE, "template.html"), encoding="utf-8").read()

# Public site: relative file reference, full HTML document.
body = tpl.replace("__KV__", "assets/keyvisual.webp")
head, rest = body.split("</style>", 1)
doc = ('<!doctype html>\n<html lang="ja">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n'
       + head + "</style>\n</head>\n<body>" + rest + "\n</body>\n</html>\n")
open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(doc)

# Artifact preview (optional): blob URL with an inline fallback.
out = sys.argv[1] if len(sys.argv) > 1 else None
if out:
    b64 = base64.b64encode(open(os.path.join(HERE, "assets/keyvisual.webp"), "rb").read()).decode()
    fb = f'<script>window.__KV_FALLBACK="data:image/webp;base64,{b64}";</script>\n'
    art = tpl.replace("__KV__", "/_blob/c2bc8141ea2c23399e286239a9ebfe83").replace("<script>\n(() => {", fb + "<script>\n(() => {", 1)
    open(out, "w", encoding="utf-8").write(art)
print("built index.html", os.path.getsize(os.path.join(HERE, "index.html")))
