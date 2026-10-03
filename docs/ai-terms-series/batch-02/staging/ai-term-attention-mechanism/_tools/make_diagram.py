from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FONT = "'Noto Sans TC','Noto Sans JP','PingFang TC','Microsoft JhengHei','Hiragino Sans',system-ui,sans-serif"
INK, MUTED = "#102A2B", "#5C6B6B"
TEAL, TEAL_BG = "#0D6B68", "#E3F0EF"
BLUE, BLUE_BG = "#2F6F9F", "#E6F0F7"
ORANGE = "#D97A2B"

out = []
add = out.append
add(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900" width="1600" height="900" role="img" aria-labelledby="title desc" font-family="{FONT}">')
add('<title id="title">注意力：比對、加權、混合 / Attention: match, weigh, mix</title>')
add('<desc id="desc">以「它」為 query，與小雅、行李箱、後車廂和其餘詞的 key 比對，經 softmax 轉成權重，示例權重依序為 0.10、0.55、0.25、0.10，總和為 1；再依權重混合各位置的 value，得到「它」的新表示，其中行李箱的內容占最多。權重是教學示例，不是實測。</desc>')
add('<rect width="1600" height="900" fill="#F7F1E8"/>')
add('<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#0D6B68"/></marker></defs>')
add(f'<text x="60" y="52" font-size="30" font-weight="700" fill="{INK}">注意力：比對、加權、混合</text>')
add(f'<text x="60" y="84" font-size="18" fill="{MUTED}">Attention: match, weigh, mix（權重為教學示例，非實測）</text>')

# column headers
for x, label in [(60, "要處理的位置"), (380, "被比對的位置"), (740, "softmax 後的權重"), (1250, "輸出")]:
    add(f'<text x="{x}" y="158" font-size="22" font-weight="700" fill="{INK}">{label}</text>')

rows = [
    ("小雅", 0.10, False),
    ("行李箱", 0.55, True),
    ("後車廂", 0.25, False),
    ("其餘詞", 0.10, False),
]
centers = [250, 378, 506, 634]
TOP, BOT = 194, 690

# query banner
add(f'<rect x="60" y="{TOP}" width="240" height="{BOT-TOP}" rx="14" fill="#FFFFFF" stroke="{ORANGE}" stroke-width="4"/>')
add(f'<text x="180" y="420" font-size="36" font-weight="700" fill="{INK}" text-anchor="middle">「它」</text>')
add(f'<text x="180" y="468" font-size="26" fill="{INK}" text-anchor="middle">query</text>')
add(f'<text x="180" y="506" font-size="22" fill="{MUTED}" text-anchor="middle">我要找什麼</text>')

# output box
add(f'<rect x="1250" y="{TOP}" width="290" height="{BOT-TOP}" rx="14" fill="{TEAL_BG}" stroke="{TEAL}" stroke-width="4"/>')
add(f'<text x="1395" y="384" font-size="28" font-weight="700" fill="{INK}" text-anchor="middle">「它」的新表示</text>')
add(f'<text x="1395" y="436" font-size="24" fill="{INK}" text-anchor="middle">＝各位置 value</text>')
add(f'<text x="1395" y="472" font-size="24" fill="{INK}" text-anchor="middle">依權重加權平均</text>')
add(f'<text x="1395" y="540" font-size="24" font-weight="700" fill="{TEAL}" text-anchor="middle">行李箱的內容</text>')
add(f'<text x="1395" y="576" font-size="24" font-weight="700" fill="{TEAL}" text-anchor="middle">占最多</text>')

for (token, w, hot), c in zip(rows, centers):
    stroke, fill = (TEAL, TEAL_BG) if hot else (BLUE, BLUE_BG)
    bar = TEAL if hot else BLUE
    # arrows
    add(f'<path d="M 300 {c} L 376 {c}" fill="none" stroke="{TEAL}" stroke-width="4" marker-end="url(#arrow)"/>')
    add(f'<path d="M 660 {c} L 736 {c}" fill="none" stroke="{TEAL}" stroke-width="4" marker-end="url(#arrow)"/>')
    add(f'<path d="M 1140 {c} L 1246 {c}" fill="none" stroke="{TEAL}" stroke-width="4" marker-end="url(#arrow)"/>')
    # key box
    add(f'<rect x="380" y="{c-56}" width="280" height="112" rx="14" fill="{fill}" stroke="{stroke}" stroke-width="4"/>')
    weight = "700" if hot else "400"
    add(f'<text x="520" y="{c-6}" font-size="30" font-weight="{weight}" fill="{INK}" text-anchor="middle">{token}</text>')
    add(f'<text x="520" y="{c+32}" font-size="20" fill="{MUTED}" text-anchor="middle">key、value</text>')
    # weight track + bar
    add(f'<rect x="740" y="{c-22}" width="400" height="44" rx="8" fill="#FFFFFF" stroke="{MUTED}" stroke-width="2"/>')
    bw = round(w * 400)
    add(f'<rect x="740" y="{c-22}" width="{bw}" height="44" rx="8" fill="{bar}"/>')
    add(f'<text x="{740+bw+16}" y="{c+9}" font-size="26" font-weight="700" fill="{INK}">{w:.2f}</text>')

# step strip
steps = [
    (60, "01", "query 與各 key 比對打分"),
    (560, "02", "softmax 轉成總和為 1 的權重"),
    (1060, "03", "依權重混合各 value"),
]
for x, badge, label in steps:
    add(f'<rect x="{x}" y="724" width="480" height="88" rx="14" fill="#FFFFFF" stroke="{TEAL}" stroke-width="4"/>')
    add(f'<circle cx="{x+50}" cy="768" r="26" fill="{TEAL}"/>')
    add(f'<text x="{x+50}" y="776" font-size="22" font-weight="700" fill="#FFFFFF" text-anchor="middle">{badge}</text>')
    add(f'<text x="{x+92}" y="777" font-size="24" fill="{INK}">{label}</text>')

add(f'<text x="1540" y="870" text-anchor="end" font-size="15" fill="{MUTED}">© Mokaair 製圖 2026</text>')
add('</svg>')
(ROOT / "diagram-1.svg").write_text("\n".join(out) + "\n", encoding="utf-8")
print("ok")
