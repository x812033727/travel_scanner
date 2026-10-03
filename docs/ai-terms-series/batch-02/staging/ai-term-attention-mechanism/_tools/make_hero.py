from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FONT = "'Noto Sans TC','Noto Sans JP','PingFang TC','Microsoft JhengHei','Hiragino Sans',system-ui,sans-serif"
TEAL, TEAL_BG, BLUE, BLUE_BG, ORANGE = "#0D6B68", "#E3F0EF", "#2F6F9F", "#E6F0F7", "#D97A2B"

centers = [230, 420, 610, 800, 990, 1180, 1370]
TOP = 600
SIZE = 120
query = 6
# (target index, stroke width, colour)
arcs = [(0, 8, BLUE, 40), (1, 8, BLUE, 26), (3, 9, BLUE, -2), (5, 10, BLUE, -34), (4, 14, BLUE, -18), (2, 26, TEAL, 12)]

out = []
add = out.append
add(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900" width="1600" height="900" role="img" aria-labelledby="title desc" font-family="{FONT}">')
add('<title id="title">注意力機制（Attention）：模型怎麼決定要參考哪些 token</title>')
add('<desc id="desc">一排方塊代表序列中的詞，最右邊的方塊向左畫出粗細不同的弧線連到其他方塊，最粗的一條連到較遠的一個方塊，表示相隔很遠的位置也能直接連上。</desc>')
add('<rect width="1600" height="900" fill="#F7F1E8"/>')

x0 = centers[query]
for idx, width, colour, off in arcs:
    x1 = centers[idx]
    xs = x0 + off
    dist = xs - x1
    apex = min(0.42 * dist, 400)
    ctrl_y = TOP - 2 * apex
    mid = (xs + x1) / 2
    add(f'<path d="M {xs} {TOP} Q {mid:.0f} {ctrl_y:.0f} {x1} {TOP}" fill="none" stroke="{colour}" stroke-width="{width}" stroke-linecap="round"/>')

for i, cx in enumerate(centers):
    if i == query:
        stroke, fill, dot = ORANGE, "#FFFFFF", ORANGE
    elif i == 2:
        stroke, fill, dot = TEAL, TEAL_BG, TEAL
    else:
        stroke, fill, dot = BLUE, BLUE_BG, BLUE
    add(f'<rect x="{cx-SIZE//2}" y="{TOP}" width="{SIZE}" height="{SIZE}" rx="22" fill="{fill}" stroke="{stroke}" stroke-width="7"/>')
    add(f'<circle cx="{cx}" cy="{TOP+SIZE//2}" r="16" fill="{dot}"/>')

add('</svg>')
(ROOT / "hero.svg").write_text("\n".join(out) + "\n", encoding="utf-8")
print("ok")
