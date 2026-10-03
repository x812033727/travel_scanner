from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FONT = "'Noto Sans TC','Noto Sans JP','PingFang TC','Microsoft JhengHei','Hiragino Sans',system-ui,sans-serif"

INK = "#102A2B"
MUTED = "#5C6B6B"
TEAL = "#0D6B68"
BLUE = "#2F6F9F"
ORANGE = "#D97A2B"
WARN = "#B8442D"

names = ["牛肉湯", "虱目魚粥", "鍋燒意麵"]
panels = [
    (60, BLUE, "低溫 t=0.5", "領先者更突出", [91, 7, 2], "分數除以 0.5，差距被放大"),
    (570, TEAL, "原本 t=1", "模型給的機率", [70, 20, 10], "分數除以 1，維持原樣"),
    (1080, ORANGE, "高溫 t=2", "差距被拉平", [52, 28, 20], "分數除以 2，差距被拉近"),
]

out = []
a = out.append
a(
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900" width="1600" height="900" role="img" '
    f'aria-labelledby="title desc" font-family="{FONT}">'
)
a('<title id="title">溫度只改變怎麼抽，不改變候選清單 / How temperature reshapes next-token probabilities</title>')
a(
    '<desc id="desc">同一份假想機率：牛肉湯 70%、虱目魚粥 20%、鍋燒意麵 10%。溫度 0.5 時變成約 91%、7%、2%，'
    '溫度 1 維持原樣，溫度 2 時變成約 52%、28%、20%。下方示範 top-p 0.85：由高到低累加，'
    '牛肉湯加虱目魚粥累積 90%，已達 85%，所以前兩名入選並重新配比為約 78% 與 22%，鍋燒意麵被排除。數字皆為示例。</desc>'
)
a('<rect width="1600" height="900" fill="#F7F1E8"/>')
a(f'<text x="60" y="52" font-size="30" font-weight="700" fill="{INK}">溫度只改變怎麼抽，不改變候選清單</text>')
a(f'<text x="60" y="84" font-size="18" fill="{MUTED}">Temperature reshapes the next-token distribution</text>')

PW, PY, PH = 460, 120, 400
for px, color, head, sub, vals, cap in panels:
    cx = px + PW / 2
    a(f'<rect x="{px}" y="{PY}" width="{PW}" height="{PH}" rx="14" fill="#FFFFFF" stroke="{color}" stroke-width="4"/>')
    a(f'<text x="{cx}" y="170" font-size="28" font-weight="700" fill="{INK}" text-anchor="middle">{head}</text>')
    a(f'<text x="{cx}" y="206" font-size="20" fill="{MUTED}" text-anchor="middle">{sub}</text>')
    for i, (name, v) in enumerate(zip(names, vals)):
        cy = 268 + i * 80
        bx = px + 140
        w = max(v * 2.4, 6)
        a(f'<text x="{px + 30}" y="{cy + 7}" font-size="22" fill="{INK}">{name}</text>')
        a(f'<rect x="{bx}" y="{cy - 20}" width="{w:.1f}" height="40" rx="6" fill="{color}"/>')
        a(f'<text x="{bx + w + 12:.1f}" y="{cy + 7}" font-size="22" font-weight="700" fill="{INK}">{v}%</text>')
    a(f'<text x="{cx}" y="490" font-size="18" fill="{MUTED}" text-anchor="middle">{cap}</text>')

# bottom band: top-p
a(f'<rect x="60" y="550" width="1480" height="285" rx="14" fill="#FFFFFF" stroke="{TEAL}" stroke-width="4"/>')
a(
    f'<text x="800" y="596" font-size="24" font-weight="700" fill="{INK}" text-anchor="middle">'
    "再加 top-p=0.85：由高到低累加機率，累積達到 85% 就停</text>"
)
X0, S = 250, 11
y0, h = 640, 70
segs = [
    ("牛肉湯", 70, TEAL, "#FFFFFF", 22),
    ("虱目魚粥", 20, BLUE, "#FFFFFF", 20),
    ("鍋燒意麵", 10, "#D5DADA", MUTED, 18),
]
x = X0
for name, v, fill, tcol, fs in segs:
    w = v * S
    a(f'<rect x="{x}" y="{y0}" width="{w}" height="{h}" fill="{fill}"/>')
    a(f'<text x="{x + w / 2}" y="{y0 + 29}" font-size="{fs}" fill="{tcol}" text-anchor="middle">{name}</text>')
    a(f'<text x="{x + w / 2}" y="{y0 + 57}" font-size="{fs}" font-weight="700" fill="{tcol}" text-anchor="middle">{v}%</text>')
    x += w
a(f'<rect x="{X0}" y="{y0}" width="{100 * S}" height="{h}" fill="none" stroke="{INK}" stroke-width="3"/>')
mx = X0 + 85 * S
a(f'<path d="M {mx} 626 L {mx} 718" fill="none" stroke="{WARN}" stroke-width="4"/>')
a(f'<text x="{mx}" y="622" font-size="18" font-weight="700" fill="{WARN}" text-anchor="middle">85%</text>')
a(f'<text x="{X0 + 70 * S}" y="744" font-size="18" fill="{MUTED}" text-anchor="middle">累積 70%</text>')
a(f'<text x="{X0 + 90 * S}" y="744" font-size="18" fill="{MUTED}" text-anchor="middle">累積 90%</text>')
inc_end = X0 + 90 * S
a(f'<path d="M {X0} 766 L {inc_end} 766 M {X0} 756 L {X0} 776 M {inc_end} 756 L {inc_end} 776" fill="none" stroke="{TEAL}" stroke-width="4"/>')
a(
    f'<text x="{(X0 + inc_end) / 2}" y="812" font-size="22" fill="{INK}" text-anchor="middle">'
    "入選：重新配比後牛肉湯約 78%、虱目魚粥約 22%</text>"
)
ex0, ex1 = inc_end + 10, X0 + 100 * S
a(f'<path d="M {ex0} 766 L {ex1} 766 M {ex0} 756 L {ex0} 776 M {ex1} 756 L {ex1} 776" fill="none" stroke="{WARN}" stroke-width="4"/>')
a(f'<text x="{(ex0 + ex1) / 2}" y="812" font-size="22" fill="{WARN}" text-anchor="middle">排除</text>')

a(f'<text x="1540" y="870" text-anchor="end" font-size="15" fill="{MUTED}">© Mokaair 製圖 2026</text>')
a("</svg>")

(ROOT / "diagram-1.svg").write_text("\n".join(out) + "\n", encoding="utf-8")
print("ok")
