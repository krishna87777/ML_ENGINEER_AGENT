"""Generates the animated SVGs used in README.md.

GitHub renders SVG files referenced with <img>, including CSS keyframe and SMIL
animation, but strips JavaScript. Every diagram here is pure CSS/SMIL.
Run:  python3 assets/make_svgs.py
"""
from pathlib import Path

OUT = Path(__file__).parent

# Palette: light values, then dark overrides via prefers-color-scheme.
BASE_CSS = """
.bg{fill:#f6f8fa}.card{fill:#ffffff;stroke:#d0d7de}
.ink{fill:#1f2328}.mut{fill:#656d76}.line{stroke:#8c959f}
.teal{fill:#0f766e}.tealS{stroke:#0f766e}.tealBg{fill:#d1f4ef}
.amber{fill:#b45309}.amberS{stroke:#b45309}.amberBg{fill:#fdecc8}
.red{fill:#cf222e}.redS{stroke:#cf222e}.redBg{fill:#ffe1e1}
.green{fill:#1a7f37}.greenS{stroke:#1a7f37}.greenBg{fill:#dafbe1}
.blue{fill:#0969da}.blueS{stroke:#0969da}.blueBg{fill:#ddf4ff}
.grey{fill:#afb8c1}.greyBg{fill:#eaeef2}
text{font-family:ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
.mono{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;white-space:pre}
.sx{transform-box:fill-box;transform-origin:0 50%}
@media (prefers-color-scheme: dark){
.bg{fill:#0d1117}.card{fill:#161b22;stroke:#30363d}
.ink{fill:#e6edf3}.mut{fill:#8b949e}.line{stroke:#6e7681}
.teal{fill:#2dd4bf}.tealS{stroke:#2dd4bf}.tealBg{fill:#0b3b36}
.amber{fill:#f5a524}.amberS{stroke:#f5a524}.amberBg{fill:#3d2a0a}
.red{fill:#ff7b72}.redS{stroke:#ff7b72}.redBg{fill:#4a1717}
.green{fill:#3fb950}.greenS{stroke:#3fb950}.greenBg{fill:#12361d}
.blue{fill:#58a6ff}.blueS{stroke:#58a6ff}.blueBg{fill:#0c2d4a}
.grey{fill:#484f58}.greyBg{fill:#21262d}
}
"""


def svg(w, h, body, css="", title=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-label="{title}"><title>{title}</title><style>{BASE_CSS}{css}</style>'
            f'<rect class="bg" width="{w}" height="{h}" rx="14"/>{body}</svg>')


def appear(name, a, gone=None, T=None):
    """Keyframes: hidden until fraction a, visible until `gone` (or ~end of cycle)."""
    a = round(a * 100, 2)
    b = round(min(a + 2.5, 99), 2)
    if gone is None:
        return (f"@keyframes {name}{{0%,{a}%{{opacity:0}}{b}%,93%{{opacity:1}}"
                f"98%,100%{{opacity:0}}}}")
    g = round(gone * 100, 2)
    g0 = round(max(g - 2, b), 2)
    return (f"@keyframes {name}{{0%,{a}%{{opacity:0}}{b}%,{g0}%{{opacity:1}}"
            f"{g}%,100%{{opacity:0}}}}")


# ---------------------------------------------------------------- 1. hero
def hero():
    rows = [
        ("000", "", "draft", "good", "98.25", "baseline, GPU 2% busy"),
        ("002", "000", "improve", "good", "81.40", "remove sync stalls"),
        ("010", "002", "improve", "buggy", "65.31", "failed quality gate"),
        ("022", "020", "improve", "good", "41.97", "int8 experts"),
        ("024", "022", "improve", "good", "34.16", "CUDA graph"),
        ("031", "024", "improve", "good", "18.01", "fused Triton kernel"),
        ("036", "031", "improve", "good", "11.90", "8.26x, same output"),
    ]
    T = 14
    css = [f".r{{opacity:0;animation-duration:{T}s;animation-iteration-count:infinite}}"]
    body = []
    body.append('<text x="40" y="62" class="ink" font-size="30" font-weight="700">One Markdown file.</text>')
    body.append('<text x="40" y="100" class="teal" font-size="30" font-weight="700">228 experiments.</text>')
    body.append('<text x="40" y="136" class="mut" font-size="16">A coding agent that researches like a careful scientist:</text>')
    body.append('<text x="40" y="160" class="mut" font-size="16">one change at a time, every result written down.</text>')
    # pill badges
    for i, (t, c) in enumerate([("5 projects", "blue"), ("6 GB laptop GPU", "amber"), ("0 guessed numbers", "green")]):
        x = 40 + i * 150
        body.append(f'<rect x="{x}" y="186" width="{140}" height="30" rx="15" class="{c}Bg"/>'
                    f'<text x="{x+70}" y="206" text-anchor="middle" class="{c}" font-size="13" font-weight="600">{t}</text>')
    # journal card
    cx, cy, cw = 510, 30, 460
    body.append(f'<rect x="{cx}" y="{cy}" width="{cw}" height="{40+len(rows)*27+24}" rx="10" class="card"/>')
    body.append(f'<circle cx="{cx+18}" cy="{cy+18}" r="5" class="red"/><circle cx="{cx+34}" cy="{cy+18}" r="5" class="amber"/>'
                f'<circle cx="{cx+50}" cy="{cy+18}" r="5" class="green"/>'
                f'<text x="{cx+70}" y="{cy+22}" class="mut mono" font-size="12">journal.tsv  (DeepSeek-OCR, real rows)</text>')
    body.append(f'<text x="{cx+14}" y="{cy+48}" class="mut mono" font-size="11">id   parent stage    status  s/page  what changed</text>')
    for i, (id_, p, st, stat, m, d) in enumerate(rows):
        y = cy + 72 + i * 27
        a = 0.04 + i * 0.1
        css.append(appear(f"h{i}", a))
        col = "red" if stat == "buggy" else ("amber" if id_ == "036" else "ink")
        body.append(f'<g class="r" style="animation-name:h{i}">'
                    f'<text x="{cx+14}" y="{y}" class="{col} mono" font-size="12">{id_}  {p:>4}  {st:<8} {stat:<6} {m:>6}  {d}</text></g>')
    css.append(appear("hstar", 0.04 + 6 * 0.1 + 0.03))
    body.append(f'<g class="r" style="animation-name:hstar"><text x="{cx+cw-24}" y="{cy+72+6*27}" class="amber" font-size="16">★</text></g>')
    return svg(1000, 280, "".join(body), "".join(css), "One Markdown file, 228 experiments")


# ---------------------------------------------------------------- 2. tree search
def tree():
    W, H, T = 900, 470, 16
    nodes = {  # id: (x, y, kind, label, sub)
        "001": (150, 78, "draft", "001 · draft", "score 0.62"),
        "002": (450, 78, "draft", "002 · draft", "score 0.55"),
        "003": (750, 78, "draft", "003 · draft", "score 0.48"),
        "004": (150, 172, "good", "004 · improve", "0.71 ↑"),
        "005": (450, 172, "bug", "005 · improve", "💥 crashed"),
        "006": (450, 266, "good", "006 · debug", "fixed · 0.58"),
        "007": (150, 266, "good", "007 · improve", "0.79 ↑"),
        "008": (95, 360, "good", "008 · improve", "0.86 ↑"),
        "009": (265, 360, "dead", "009 · improve", "0.74 ↓ worse"),
    }
    edges = [("001", "004"), ("002", "005"), ("005", "006"), ("004", "007"), ("007", "008"), ("007", "009")]
    order = ["001", "002", "003", "004", "005", "006", "007", "008", "009"]
    captions = [
        "Start wide: write 3 simple, different ideas (drafts)",
        "",
        "",
        "Improve the BEST node — exactly one change",
        "A run crashed → it becomes a bug to fix",
        "Debug it (at most 3 tries, then give up on that branch)",
        "Back to the best node → one more change → new best",
        "Keep climbing from the best …",
        "Worse? Keep it in the log, never build on it",
    ]
    step = 0.095
    css = [f".a{{opacity:0;animation-duration:{T}s;animation-iteration-count:infinite;animation-fill-mode:both}}"]
    body = ['<text x="30" y="30" class="mut" font-size="13" font-weight="600">TREE SEARCH OVER EXPERIMENTS</text>']
    t = {n: 0.03 + i * step for i, n in enumerate(order)}
    for a, b in edges:
        x1, y1 = nodes[a][0], nodes[a][1] + 22
        x2, y2 = nodes[b][0], nodes[b][1] - 22
        nm = f"e{a}{b}"
        css.append(appear(nm, t[b] - 0.01))
        dash = ' stroke-dasharray="5 5"' if nodes[b][2] == "dead" else ""
        body.append(f'<path class="a line" style="animation-name:{nm}" d="M{x1},{y1} C{x1},{(y1+y2)/2} {x2},{(y1+y2)/2} {x2},{y2}" '
                    f'fill="none" stroke-width="2"{dash}/>')
    styles = {"draft": ("blueBg", "blueS", "blue"), "good": ("greenBg", "greenS", "green"),
              "bug": ("redBg", "redS", "red"), "dead": ("greyBg", "line", "mut")}
    for n in order:
        x, y, kind, lab, sub = nodes[n]
        bg, st, tx = styles[kind]
        nm = f"n{n}"
        css.append(appear(nm, t[n]))
        body.append(f'<g class="a" style="animation-name:{nm}">'
                    f'<rect x="{x-68}" y="{y-22}" width="136" height="44" rx="10" class="{bg} {st}" stroke-width="1.6"/>'
                    f'<text x="{x}" y="{y-3}" text-anchor="middle" class="{tx}" font-size="13" font-weight="700">{lab}</text>'
                    f'<text x="{x}" y="{y+14}" text-anchor="middle" class="{tx}" font-size="11.5">{sub}</text></g>')
    # "best" crown that moves 001 -> 004 -> 007 -> 008
    best = [("001", t["001"], t["004"]), ("004", t["004"], t["007"]), ("007", t["007"], t["008"]), ("008", t["008"], None)]
    for n, a, g in best:
        x, y = nodes[n][0], nodes[n][1]
        nm = f"b{n}"
        css.append(appear(nm, a + 0.01, g))
        body.append(f'<g class="a" style="animation-name:{nm}"><rect x="{x+42}" y="{y-34}" width="48" height="20" rx="10" class="amberBg"/>'
                    f'<text x="{x+66}" y="{y-20}" text-anchor="middle" class="amber" font-size="11" font-weight="700">★ best</text></g>')
    # abandoned X for 009
    css.append(appear("x009", t["009"] + 0.03))
    body.append(f'<g class="a" style="animation-name:x009"><text x="{nodes["009"][0]+78}" y="{nodes["009"][1]+6}" class="red" font-size="20" font-weight="700">✕</text></g>')
    # captions
    body.append(f'<rect x="30" y="410" width="{W-60}" height="42" rx="10" class="card"/>')
    for i, n in enumerate(order):
        cap = captions[i]
        if not cap:
            continue
        nxt = next((t[m] for m in order[i+1:] if captions[order.index(m)]), None)
        nm = f"c{n}"
        css.append(appear(nm, t[n], nxt))
        body.append(f'<g class="a" style="animation-name:{nm}"><text x="{W/2}" y="437" text-anchor="middle" class="ink" font-size="15" font-weight="600">{cap}</text></g>')
    # legend
    lg = [("blueBg", "blueS", "draft"), ("greenBg", "greenS", "works"), ("redBg", "redS", "bug"), ("greyBg", "line", "abandoned")]
    for i, (bg, st, lab) in enumerate(lg):
        x = 560 + i * 76
        body.append(f'<rect x="{x}" y="18" width="14" height="14" rx="3" class="{bg} {st}"/><text x="{x+19}" y="30" class="mut" font-size="11.5">{lab}</text>')
    return svg(W, H, "".join(body), "".join(css), "Tree search over experiments")


# ---------------------------------------------------------------- 3. the loop
def loop():
    W, H, T = 900, 410, 10
    cx, cy, r = 450, 225, 130
    import math
    stages = [("1. Pick", "follow the 4 rules"), ("2. Change ONE thing", "write sol_023.py"),
              ("3. Run", "log → file, not screen"), ("4. Read the score", "grep, tail -50 if crash"),
              ("5. Write it down", "journal.tsv + git commit")]
    css = [f".s{{animation-duration:{T}s;animation-iteration-count:infinite}}"]
    body = ['<text x="30" y="30" class="mut" font-size="13" font-weight="600">THE LOOP — IT NEVER STOPS UNTIL THE BUDGET RUNS OUT</text>']
    body.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" class="line" stroke-width="2" stroke-dasharray="4 7"/>')
    pts = []
    for i, (a, b) in enumerate(stages):
        ang = -math.pi / 2 + i * 2 * math.pi / len(stages)
        x, y = cx + r * math.cos(ang), cy + r * math.sin(ang)
        pts.append((x, y))
        lo, hi = i / 5 * 100, (i + 1) / 5 * 100
        css.append(f"@keyframes g{i}{{0%,{max(lo-0.1,0):.1f}%{{opacity:.35}}{lo+3:.1f}%,{hi-3:.1f}%{{opacity:1}}{hi:.1f}%,100%{{opacity:.35}}}}")
        bx = x + (105 if math.cos(ang) > 0.3 else (-105 if math.cos(ang) < -0.3 else 0))
        by = y + (-4 if abs(math.cos(ang)) > 0.3 else (-34 if math.sin(ang) < 0 else 36))
        body.append(f'<g class="s" style="animation-name:g{i}">'
                    f'<circle cx="{x:.1f}" cy="{y:.1f}" r="13" class="teal"/>'
                    f'<text x="{x:.1f}" y="{y+4.5:.1f}" text-anchor="middle" fill="#fff" font-size="12" font-weight="700">{i+1}</text>'
                    f'<text x="{bx:.1f}" y="{by:.1f}" text-anchor="middle" class="ink" font-size="15" font-weight="700">{a[3:]}</text>'
                    f'<text x="{bx:.1f}" y="{by+18:.1f}" text-anchor="middle" class="mut mono" font-size="11.5">{b}</text></g>')
    # moving dot along the circle (SMIL)
    body.append(f'<circle r="7" class="amber"><animateMotion dur="{T}s" repeatCount="indefinite" '
                f'path="M{cx},{cy-r} a{r},{r} 0 1,1 -0.01,0"/></circle>')
    body.append(f'<text x="{cx}" y="{cy-6}" text-anchor="middle" class="ink" font-size="20" font-weight="800">no</text>'
                f'<text x="{cx}" y="{cy+18}" text-anchor="middle" class="ink" font-size="20" font-weight="800">"may I continue?"</text>')
    return svg(W, H, "".join(body), "".join(css), "The experiment loop")


# ---------------------------------------------------------------- 4. MoE offload
def moe():
    W, H, T = 940, 470, 14
    css = [f".m{{animation-duration:{T}s;animation-iteration-count:infinite;animation-timing-function:ease-in-out}}"]
    body = ['<text x="30" y="30" class="mut" font-size="13" font-weight="600">MOE EXPERT OFFLOAD — HOW AN 18 GB MODEL RUNS IN AN 8 GB SLICE</text>']
    gx, gy, gw, gh = 40, 50, 380, 300
    kx, ky = 520, 60
    body.append(f'<rect x="{gx}" y="{gy}" width="{gw}" height="{gh}" rx="12" class="card" stroke-width="1.5"/>'
                f'<text x="{gx+16}" y="{gy+26}" class="ink" font-size="15" font-weight="700">GPU  (our cap: 8 GB)</text>')
    body.append(f'<rect x="{kx}" y="{ky}" width="{gw}" height="{gh}" rx="12" class="card" stroke-width="1.5"/>'
                f'<text x="{kx+16}" y="{ky+26}" class="ink" font-size="15" font-weight="700">CPU RAM  (125 GB, slower)</text>')
    # always-on-GPU blocks
    body.append(f'<rect x="{gx+16}" y="{gy+40}" width="170" height="34" rx="7" class="tealBg tealS" stroke-width="1.3"/>'
                f'<text x="{gx+101}" y="{gy+62}" text-anchor="middle" class="teal" font-size="12" font-weight="700">attention + router</text>')
    body.append(f'<rect x="{gx+194}" y="{gy+40}" width="170" height="34" rx="7" class="tealBg tealS" stroke-width="1.3"/>'
                f'<text x="{gx+279}" y="{gy+62}" text-anchor="middle" class="teal" font-size="12" font-weight="700">vision encoder 1.1 GB</text>')
    # 48 expert layers: 8 cols x 6 rows
    cols, tw, th, gap = 8, 38, 22, 6
    ox, oy = gx + 16, gy + 90
    kox, koy = kx + 16, ky + 50
    keep = 14
    p1, p2, p3 = 0.22, 0.42, 0.62  # phases: overflow, move all out, bring 14 back
    for i in range(48):
        c, rr = i % cols, i // cols
        x0, y0 = ox + c * (tw + gap), oy + rr * (th + gap)
        xk, yk = kox + c * (tw + gap), koy + rr * (th + gap)
        dx, dy = xk - x0, yk - y0
        nm = f"t{i}"
        stay = i < keep
        if stay:
            css.append(f"@keyframes {nm}{{0%,{p1*100}%{{transform:translate(0,0)}}"
                       f"{p2*100}%,{p2*100+4}%{{transform:translate({dx}px,{dy}px)}}"
                       f"{p3*100}%,94%{{transform:translate(0,0)}}100%{{transform:translate(0,0)}}}}")
        else:
            css.append(f"@keyframes {nm}{{0%,{p1*100}%{{transform:translate(0,0)}}"
                       f"{p2*100}%,94%{{transform:translate({dx}px,{dy}px)}}100%{{transform:translate(0,0)}}}}")
        cl = "amberBg amberS"
        body.append(f'<g class="m" style="animation-name:{nm}"><rect x="{x0}" y="{y0}" width="{tw}" height="{th}" rx="4" class="{cl}" stroke-width="1"/>'
                    f'<text x="{x0+tw/2}" y="{y0+15}" text-anchor="middle" class="amber" font-size="9.5" font-weight="600">L{i}</text></g>')
    body.append(f'<text x="{gx+16}" y="{gy+gh-12}" class="mut" font-size="11.5">amber = expert FFN layer (big, but each token uses only a few)</text>')
    # VRAM bar
    bx, by, bw = 40, 390, 860
    body.append(f'<text x="{bx}" y="{by-8}" class="ink" font-size="13" font-weight="700">VRAM used</text>')
    body.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="22" rx="11" class="greyBg"/>')
    scale = bw / 20.0  # 20 GB full width
    capx = bx + 8 * scale
    w18, w14, w764 = 18.0 * scale, 1.4 * scale, 7.64 * scale
    k14, k764 = 1.4/18, 7.64/18
    css.append(f"@keyframes vb{{0%,{p1*100}%{{transform:scaleX(1)}}{p2*100}%,{p2*100+4}%{{transform:scaleX({k14:.4f})}}{p3*100}%,94%{{transform:scaleX({k764:.4f})}}100%{{transform:scaleX(1)}}}}")
    css.append(f"@keyframes vc{{0%,{p1*100}%{{fill:#cf222e}}{p2*100}%,94%{{fill:#1a7f37}}100%{{fill:#cf222e}}}}")
    body.append(f'<rect class="m sx" x="{bx}" y="{by}" height="22" rx="11" width="{w18}" style="animation-name:vb,vc"/>')
    body.append(f'<line x1="{capx}" y1="{by-6}" x2="{capx}" y2="{by+28}" class="redS" stroke-width="2.5" stroke-dasharray="4 3"/>'
                f'<text x="{capx+6}" y="{by+42}" class="red" font-size="12" font-weight="700">8 GB cap</text>')
    labels = [("Whole 30B model on GPU = 18 GB → does NOT fit ✕", 0, p1 + 0.04, "red"),
              ("Move ALL experts to CPU → only 1.4 GB, always loads (8.6 tok/s)", p1 + 0.04, p2 + 0.08, "blue"),
              ("Bring the first 14 of 48 back → 7.64 GB, just under the cap, 2× faster", p2 + 0.08, 0.95, "green")]
    for j, (txt, a, g, c) in enumerate(labels):
        nm = f"ml{j}"
        a0, g0 = round(a * 100, 1), round(g * 100, 1)
        css.append(f"@keyframes {nm}{{0%,{a0}%{{opacity:0}}{a0+2}%,{g0-2}%{{opacity:1}}{g0}%,100%{{opacity:0}}}}")
        body.append(f'<g class="m" style="animation-name:{nm};opacity:0"><text x="{W/2}" y="455" text-anchor="middle" class="{c}" font-size="15" font-weight="700">{txt}</text></g>')
    return svg(W, H, "".join(body), "".join(css), "MoE expert offload")


# ---------------------------------------------------------------- 5. tiling
def tiling():
    W, H, T = 940, 360, 12
    css = [f".q{{animation-duration:{T}s;animation-iteration-count:infinite}}"]
    body = ['<text x="30" y="30" class="mut" font-size="13" font-weight="600">TILING — GIVE EVERY PACK ENOUGH PIXELS</text>']
    # shelf: 5 rows x 12 packs
    sx, sy, pw, ph = 40, 60, 30, 40
    brands = ["blue", "green", "amber", "red", "teal"]
    for r in range(5):
        body.append(f'<rect x="{sx-6}" y="{sy+r*(ph+10)+ph}" width="{12*(pw+4)+8}" height="4" class="grey"/>')
        for c in range(12):
            b = brands[(c // 3 + r) % 5]
            body.append(f'<rect x="{sx+c*(pw+4)}" y="{sy+r*(ph+10)}" width="{pw}" height="{ph}" rx="4" class="{b}Bg {b}S" stroke-width="1"/>')
    body.append(f'<text x="{sx}" y="{sy+5*(ph+10)+22}" class="mut" font-size="12">48 MP shelf photo · 150 packs · 17 brands</text>')
    # moving highlight over 12 tiles (5 boxes each approximated as 3x1 chunks of 4 cols)
    tiles = [(r, c) for r in range(5) for c in range(3)]
    n = len(tiles)
    vals_x = ";".join(str(sx - 3 + c * 4 * (pw + 4)) for r, c in tiles)
    vals_y = ";".join(str(sy - 3 + r * (ph + 10)) for r, c in tiles)
    body.append(f'<rect width="{4*(pw+4)+2}" height="{ph+6}" rx="6" fill="none" class="amberS" stroke-width="3">'
                f'<animate attributeName="x" values="{vals_x}" dur="{T}s" calcMode="discrete" repeatCount="indefinite"/>'
                f'<animate attributeName="y" values="{vals_y}" dur="{T}s" calcMode="discrete" repeatCount="indefinite"/></rect>')
    # arrow
    body.append('<path d="M470,160 L540,160" class="amberS" stroke-width="3" fill="none"/><path d="M540,152 L552,160 L540,168 Z" class="amber"/>')
    # zoom panel
    zx, zy = 570, 60
    body.append(f'<rect x="{zx}" y="{zy}" width="330" height="200" rx="12" class="card"/>'
                f'<text x="{zx+16}" y="{zy+24}" class="ink" font-size="14" font-weight="700">one tile, sent to the model</text>')
    for k in range(4):
        body.append(f'<rect x="{zx+20+k*76}" y="{zy+40}" width="66" height="96" rx="7" class="blueBg blueS" stroke-width="1.4"/>'
                    f'<circle cx="{zx+34+k*76}" cy="{zy+54}" r="10" class="red"/>'
                    f'<text x="{zx+34+k*76}" y="{zy+58}" text-anchor="middle" fill="#fff" font-size="10" font-weight="700">{12+k}</text>')
    body.append(f'<text x="{zx+16}" y="{zy+160}" class="mono ink" font-size="12">12 | Morning Fresh | lemon 750ml</text>'
                f'<text x="{zx+16}" y="{zy+178}" class="mono ink" font-size="12">13 | Morning Fresh | lemon 750ml</text>'
                f'<text x="{zx+16}" y="{zy+196}" class="mono mut" font-size="12">…Python does all the counting</text>')
    body.append(f'<text x="{zx}" y="300" class="red" font-size="13" font-weight="700">Whole photo → packs blur → "Ezee" × 37 ✕</text>'
                f'<text x="{zx}" y="322" class="green" font-size="13" font-weight="700">Tiles of 5 → 150/150 read · 0.98 · 31 s ✓</text>')
    return svg(W, H, "".join(body), "".join(css), "Tiling")


# ---------------------------------------------------------------- 6. before / after bars
def bars():
    rows = [
        ("Multilingual OCR (CPU)", 165, 2.0, "s/page", "68–165 s → ~2 s", "35–80×"),
        ("DeepSeek-OCR (6 GB GPU)", 98.25, 11.90, "s/page", "98.25 s → 11.90 s", "8.26×"),
        ("Face verification (phone)", 20.2, 1.75, "s", "20.2 s → 1.75 s", "11.5×"),
        ("Shelf audit under 8 GB", 217, 31.2, "s/shelf", "217 s (30B) → 31 s (7B)", "7×"),
    ]
    W, H, T = 940, 80 + len(rows) * 74, 8
    css = [f".w{{animation-duration:{T}s;animation-iteration-count:infinite;animation-timing-function:cubic-bezier(.6,0,.2,1)}}"]
    body = ['<text x="30" y="32" class="mut" font-size="13" font-weight="600">BEFORE → AFTER (time, shorter is better)</text>']
    full = 560
    for i, (name, b, a, u, lab, x) in enumerate(rows):
        y = 64 + i * 74
        wa = max(full * a / b, 8)
        body.append(f'<text x="30" y="{y+18}" class="ink" font-size="14" font-weight="700">{name}</text>'
                    f'<text x="30" y="{y+38}" class="mut" font-size="12">{lab}</text>')
        body.append(f'<rect x="260" y="{y+6}" width="{full}" height="30" rx="8" class="greyBg"/>')
        css.append(f"@keyframes w{i}{{0%,15%{{transform:scaleX(1)}}55%,92%{{transform:scaleX({wa/full:.4f})}}100%{{transform:scaleX(1)}}}}")
        css.append(f"@keyframes wc{i}{{0%,15%{{fill:#cf222e}}55%,92%{{fill:#1a7f37}}100%{{fill:#cf222e}}}}")
        body.append(f'<rect class="w sx" x="260" y="{y+6}" height="30" rx="8" width="{full}" style="animation-name:w{i},wc{i};animation-delay:{i*0.15}s"/>')
        css.append(f"@keyframes wx{i}{{0%,50%{{opacity:0}}58%,92%{{opacity:1}}100%{{opacity:0}}}}")
        body.append(f'<g class="w" style="animation-name:wx{i};animation-delay:{i*0.15}s;opacity:0"><text x="{840}" y="{y+28}" class="green" font-size="20" font-weight="800">{x}</text></g>')
    return svg(W, H, "".join(body), "".join(css), "Before and after")


# ---------------------------------------------------------------- 7. overfitting
def overfit():
    W, H, T = 940, 360, 10
    css = [f".o{{animation-duration:{T}s;animation-iteration-count:infinite;animation-timing-function:ease-out}}"]
    body = ['<text x="30" y="32" class="mut" font-size="13" font-weight="600">OVERFITTING — WHEN THE SEARCH MEMORISES THE TEST</text>']
    # left: student analogy
    body.append('<rect x="30" y="54" width="380" height="270" rx="12" class="card"/>')
    body.append('<text x="50" y="86" class="ink" font-size="16" font-weight="700">The student analogy</text>')
    lines = ["Practise 50 times on the SAME mock paper,",
             "keep whatever scored best, and you will ace",
             "that paper — maybe because you memorised it.",
             "",
             "Tree search does the same: 50 experiments,",
             "all scored on ONE dev set. The winner is",
             "partly \"best at this dev set\", not \"best\"."]
    for k, l in enumerate(lines):
        body.append(f'<text x="50" y="{116+k*22}" class="mut" font-size="13.5">{l}</text>')
    body.append('<text x="50" y="300" class="teal" font-size="13.5" font-weight="700">Fix: a sealed test set, opened once at the end.</text>')
    # right: bars
    bx, full = 470, 380
    items = [("Shelf preset, tuned on the dishwash photo", 0.98, "green", 0.0),
             ("Same preset, new photo (handwash)", 0.36, "red", 0.9),
             ("Real uploads, no brand list given", 0.765, "amber", 1.8)]
    for i, (lab, v, c, d) in enumerate(items):
        y = 70 + i * 66 + (22 if i >= 2 else 0)
        body.append(f'<text x="{bx}" y="{y}" class="ink" font-size="13" font-weight="600">{lab}</text>')
        body.append(f'<rect x="{bx}" y="{y+8}" width="{full}" height="24" rx="7" class="greyBg"/>')
        w = full * v
        css.append(f"@keyframes ob{i}{{0%,10%{{transform:scaleX(0)}}45%,90%{{transform:scaleX(1)}}100%{{transform:scaleX(0)}}}}")
        body.append(f'<rect class="o sx {c}" x="{bx}" y="{y+8}" height="24" rx="7" width="{w:.1f}" style="animation-name:ob{i};animation-delay:{d}s"/>')
        body.append(f'<text x="{bx+full-8}" y="{y+26}" text-anchor="end" class="ink" font-size="13" font-weight="800">{v:g}</text>')
    body.append(f'<text x="{bx}" y="178" class="red" font-size="12.5" font-weight="700">↑ overfit: 0.98 → 0.36 on a photo it never saw</text>')
    body.append(f'<text x="{bx}" y="266" class="amber" font-size="12.5" font-weight="700">↑ the brand list was quietly doing part of the work</text>'
                f'<text x="{bx}" y="306" class="teal" font-size="13" font-weight="700">Always score on photos the search never saw.</text>')
    return svg(W, H, "".join(body), "".join(css), "Overfitting")


# ---------------------------------------------------------------- 8. lineage
def lineage():
    W, H, T = 940, 330, 6
    css = [f".p{{animation-duration:{T}s;animation-iteration-count:infinite}}"
           "@keyframes flow{to{stroke-dashoffset:-24}}"
           ".f{stroke-dasharray:8 4;animation:flow 1s linear infinite}"
           "@keyframes pulse{0%,100%{opacity:1}50%{opacity:.75}}"]
    body = ['<text x="30" y="32" class="mut" font-size="13" font-weight="600">WHERE THE IDEAS COME FROM</text>']
    boxes = [(40, 70, "WecoAI/aideml", "AIDE", ["tree of solutions", "draft · improve · debug", "metric-guided search"], "blue"),
             (40, 200, "karpathy/autoresearch", "autoresearch", ["fixed 5-min budget", "log → grep → tail -50", "never-stop loop, git"], "amber")]
    for x, y, repo, name, feats, c in boxes:
        body.append(f'<rect x="{x}" y="{y}" width="300" height="106" rx="12" class="{c}Bg {c}S" stroke-width="1.5"/>'
                    f'<text x="{x+16}" y="{y+26}" class="{c}" font-size="15" font-weight="800">{name}</text>'
                    f'<text x="{x+16}" y="{y+44}" class="{c} mono" font-size="11.5">github.com/{repo}</text>')
        for k, fe in enumerate(feats):
            body.append(f'<text x="{x+16}" y="{y+66+k*16}" class="ink" font-size="12.5">• {fe}</text>')
    body.append('<path class="f blueS" d="M340,123 C440,123 460,170 560,170" fill="none" stroke-width="3"/>')
    body.append('<path class="f amberS" d="M340,253 C440,253 460,200 560,200" fill="none" stroke-width="3"/>')
    body.append('<rect x="560" y="120" width="340" height="130" rx="14" class="tealBg tealS" stroke-width="2"/>'
                '<text x="730" y="152" text-anchor="middle" class="teal" font-size="18" font-weight="800">ML_ENGINEER_AGENT.md</text>'
                '<text x="730" y="178" text-anchor="middle" class="ink" font-size="12.5">+ Phase-0 hardware interview &amp; table</text>'
                '<text x="730" y="197" text-anchor="middle" class="ink" font-size="12.5">+ journal.tsv with parent links</text>'
                '<text x="730" y="216" text-anchor="middle" class="ink" font-size="12.5">+ OOM ladder: batch → model → method</text>'
                '<text x="730" y="235" text-anchor="middle" class="ink" font-size="12.5">+ simplicity rule, REPORT.md from real rows</text>')
    return svg(W, H, "".join(body), "".join(css), "Lineage of ML_ENGINEER_AGENT.md")


if __name__ == "__main__":
    for name, fn in [("hero", hero), ("tree-search", tree), ("loop", loop), ("moe-offload", moe),
                     ("tiling", tiling), ("before-after", bars), ("overfitting", overfit), ("lineage", lineage)]:
        (OUT / f"{name}.svg").write_text(fn(), encoding="utf-8")
        print("wrote", name)
