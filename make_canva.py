#!/usr/bin/env python3
"""Canva取り込み用 canva.html を index.html から生成する。
方針: 動きと地図は残しつつ、文字は「1要素＝1つの文字列」に単純化して、Canva上で編集しやすくする。"""
import re, os, datetime
HERE = os.path.dirname(os.path.abspath(__file__))
s = open(os.path.join(HERE, "index.html"), encoding="utf-8").read()
s = s.replace('<meta name="robots" content="noindex"> <!-- 本公開時にこの行を削除（検索エンジンに載せる） -->\n', '')

# --- Wordmark: plain text, no per-letter spans (drops the cursor width effect) ---
s = re.sub(r'<h1 class="wordmark h" id="wordmark" aria-label="JAZZ EMP vol.9">.*?</h1>',
           '<h1 class="wordmark h" id="wordmark"><span class="line">Jazz</span><span class="line">Emp</span></h1>', s, flags=re.S)
s = re.sub(r"  // Wordmark: width follows the cursor.*?\n  if \(!RM\) \{\n.*?\n  \}\n", "", s, flags=re.S)

# --- Hero date: two separate lines ---
s = s.replace('<div class="d h"><span>January 31, 2027</span><span>Sun 12:00 – 18:00</span></div>',
              '<div class="d h">January 31, 2027</div><div class="d h">Sun 12:00 – 18:00</div>')

# --- Countdown: one text per unit, pre-rendered ---
T0 = datetime.datetime(2027, 1, 31, 3, 0, 0, tzinfo=datetime.timezone.utc)
diff = max(0, int((T0 - datetime.datetime.now(datetime.timezone.utc)).total_seconds()))
d, r = divmod(diff, 86400); h, r = divmod(r, 3600); m, sec = divmod(r, 60)
for k, v, w in (("d", d, 3), ("h", h, 2), ("m", m, 2), ("s", sec, 2)):
    s = re.sub(rf'<div class="n" data-u="{k}">.*?</div>', f'<div class="n" data-u="{k}">{str(v).zfill(w)}</div>', s, flags=re.S)
s = s.replace("""  function setDigits(el, str) {
    const sp = el.children;
    for (let i = 0; i < sp.length; i++) if (sp[i].textContent !== str[i]) {
      sp[i].textContent = str[i];
      if (!RM) { sp[i].classList.remove('flip'); void sp[i].offsetWidth; sp[i].classList.add('flip'); }
    }
  }""", """  function setDigits(el, str) { if (el.textContent !== str) el.textContent = str; }""")

# --- Ticker: plain text items ---
s = re.sub(r'<div class="item"(?: lang="ja")?><i>([▲■])</i>(.*?)<em>(.*?)</em></div>', r'<div class="item" lang="ja">\1 \2　\3</div>', s)
s = s.replace(".ticker .track { display: flex; width: max-content; animation: run 44s linear infinite; }",
              ".ticker .track { display: inline-block; white-space: nowrap; animation: run 44s linear infinite; }")
s = s.replace(".ticker .item { padding: 12px 32px 12px 0; font-size: 12px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; white-space: nowrap; display: flex; gap: 12px; align-items: center; }",
              ".ticker .item { display: inline-block; white-space: nowrap; padding: 12px 32px 12px 0; font-size: 12px; font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase; }")

# --- Lineup members: leader on its own line, the rest as one run (no inline bold) ---
def members(m):
    inner = m.group(1)
    parts = re.split(r'\s*／\s*', re.sub(r'</?b>', '', inner))
    return f'<div class="act-members" lang="ja"><div class="lead">{parts[0]}</div><div>{" ／ ".join(parts[1:])}</div></div>' if len(parts) > 1 else m.group(0)
s = re.sub(r'<div class="act-members" lang="ja">(.*?)</div>', members, s)
s = s.replace(".act-members b { color: var(--ink); font-weight: 700; }", ".act-members .lead { color: var(--ink); font-weight: 700; }")

# --- Program: flap cells become single text per cell; the settle animation scrambles the whole string ---
s = re.sub(r'<div class="flap( wide)?" data-text="([^"]*)"></div>', lambda m: f'<div class="flap{m.group(1) or ""}" data-text="{m.group(2)}">{m.group(2)}</div>', s)
s = s.replace("""  document.querySelectorAll('.flap').forEach(f => {
    f.innerHTML = [...f.dataset.text].map(ch => `<span class="c${ch === ' ' ? ' sp' : ''}">${ch === ' ' ? '' : ch}</span>`).join('');
  });
  function settle(f, delay) {
    if (RM) return;
    const cells = [...f.querySelectorAll('.c')], target = [...f.dataset.text], t0 = performance.now() + delay;
    (function step(now) {
      let done = true;
      cells.forEach((c, i) => {
        if (target[i] === ' ') return;
        const at = t0 + 350 + i * 45;
        if (now < at) { done = false; if (now > t0 && Math.random() < 0.5) c.textContent = CH[(Math.random() * CH.length) | 0]; }
        else c.textContent = target[i];
      });
      if (!done) requestAnimationFrame(step);
    })(performance.now());
  }""", """  function settle(f, delay) {
    if (RM) return;
    const target = [...(f.dataset.text || f.textContent)], t0 = performance.now() + delay;
    (function step(now) {
      let done = true, out = '';
      target.forEach((ch, i) => {
        if (ch === ' ') { out += ' '; return; }
        const at = t0 + 350 + i * 45;
        if (now < at) { done = false; out += (now > t0 && Math.random() < 0.5) ? CH[(Math.random() * CH.length) | 0] : ch; }
        else out += ch;
      });
      f.textContent = out;
      if (!done) requestAnimationFrame(step);
    })(performance.now());
  }""")
s = s.replace("""  .flap { display: inline-flex; gap: 2px; }
  .flap .c { display: inline-grid; place-items: center; width: 1.05em; height: 1.45em; background: #e6e3da; font-weight: 700; font-size: clamp(16px, 2vw, 24px); line-height: 1; position: relative; font-variant-numeric: tabular-nums; font-family: var(--display), var(--jp); color: var(--ink); }
  .flap .c.sp { background: transparent; width: .45em; }
  .flap .c::after { content: ""; position: absolute; left: 0; right: 0; top: 50%; height: 1px; background: var(--cream); }
  .flap.wide .c { width: auto; min-width: 1.05em; padding: 0 .12em; }""",
"""  .flap { display: inline-block; background: #e6e3da; padding: .3em .5em; font-weight: 700; font-size: clamp(16px, 2vw, 24px); line-height: 1; letter-spacing: .12em; font-variant-numeric: tabular-nums; font-family: var(--display), var(--jp); color: var(--ink); white-space: nowrap; }""")

# --- Ticket steps: Free tag out of the bold heading ---
s = s.replace('<b lang="ja">teketで「オンライン視聴チケット」を申し込む<span class="free">Free</span></b>', '<b lang="ja">teketで「オンライン視聴チケット」を申し込む</b><span class="free">Free</span>')
s = s.replace('<b lang="ja">STOCKVOICEにユーザー登録する<span class="free">Free</span></b>', '<b lang="ja">STOCKVOICEにユーザー登録する</b><span class="free">Free</span>')
s = s.replace(".step .free { display: inline-block;", ".step .free { display: inline-block; margin-top: 6px;")

# --- News: bold headline as its own line ---
s = s.replace('<p lang="ja"><b>Music Cities Awards 受賞のお知らせ</b>　', '<p lang="ja"><b style="display:block">Music Cities Awards 受賞のお知らせ</b>')

# --- Footer: giant wordmark fully visible ---
s = s.replace(".footer .giant { font-size: clamp(64px, 16.5vw, 300px); line-height: .74; margin-bottom: -0.16em; white-space: nowrap; letter-spacing: -0.05em; color: var(--red); padding-left: var(--pad); }",
              ".footer .giant { font-size: clamp(64px, 16.5vw, 300px); line-height: 1; margin: 0; padding: 0 var(--pad) 24px; white-space: nowrap; letter-spacing: -0.05em; color: var(--red); }")

open(os.path.join(HERE, "canva.html"), "w", encoding="utf-8").write(s)
print("canva.html", len(s), "| per-letter spans:", s.count('class="l"'), "| flap cells:", s.count('class="c"'), "| inline b in members:", len(re.findall(r'act-members[^<]*<b', s)))
