import math, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
T = (300, 585); tip = (905, 585); C = (1100, 450)
dx, dy = tip[0]-T[0], tip[1]-T[1]; L = math.hypot(dx, dy); d = (dx/L, dy/L); pp = (-d[1], d[0])
r1 = lambda v: round(v, 1)
def pt(a, b): return (r1(T[0]+a*d[0]+b*pp[0]), r1(T[1]+a*d[1]+b*pp[1]))
def poly(points, fill, stroke="#102A2B", sw=3): return '<polygon points="' + ' '.join(f'{x},{y}' for x,y in points) + f'" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"/>'
fl = poly([pt(12,0), pt(-18,36), pt(42,36), pt(78,0)], "#2F6F9F") + poly([pt(12,0), pt(-18,-36), pt(42,-36), pt(78,0)], "#2F6F9F")
base = (tip[0]-56*d[0], tip[1]-56*d[1])
head = poly([tip, (r1(base[0]+24*pp[0]), r1(base[1]+24*pp[1])), (r1(base[0]-24*pp[0]), r1(base[1]-24*pp[1]))], "#102A2B")
u = (C[0]-tip[0], C[1]-tip[1]); ul = math.hypot(*u); u = (u[0]/ul, u[1]/ul); q = (-u[1], u[0])
tipd = (C[0]-64*u[0], C[1]-64*u[1])            # dashed arrow ends just outside the bullseye
bd = (tipd[0]-34*u[0], tipd[1]-34*u[1])
dhead = poly([(r1(tipd[0]), r1(tipd[1])), (r1(bd[0]+17*q[0]), r1(bd[1]+17*q[1])), (r1(bd[0]-17*q[0]), r1(bd[1]-17*q[1]))], "#B8442D", "#B8442D", 2)
start = (r1(tip[0]+34*u[0]), r1(tip[1]+34*u[1])); lend = (r1(bd[0]), r1(bd[1]))
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900" width="1600" height="900" role="img" aria-labelledby="title desc" font-family="'Noto Sans TC','Noto Sans JP','PingFang TC','Microsoft JhengHei','Hiragino Sans',system-ui,sans-serif"><title id="title">AI 對齊（Alignment）：對到誰的什麼，先問清楚</title><desc id="desc">左側的對話框代表一句請求，一支箭從它下方射向右側的靶，箭落在偏離靶心的位置，一條虛線箭頭指向原本想射中的靶心。</desc><rect width="1600" height="900" fill="#F7F1E8"/><rect x="120" y="235" width="440" height="200" rx="36" fill="#FFFFFF" stroke="#0D6B68" stroke-width="7"/><polygon points="219,430 297,430 236,497" fill="#FFFFFF"/><rect x="223" y="430" width="71" height="10" fill="#FFFFFF"/><path d="M 218 435 L 236 499 L 298 435" fill="none" stroke="#0D6B68" stroke-width="7" stroke-linejoin="round" stroke-linecap="butt"/><rect x="175" y="285" width="330" height="22" rx="11" fill="#9FB1B0"/><rect x="175" y="333" width="240" height="22" rx="11" fill="#9FB1B0"/><rect x="175" y="381" width="290" height="22" rx="11" fill="#9FB1B0"/><circle cx="{C[0]}" cy="{C[1]}" r="300" fill="#E3F0EF" stroke="#0D6B68" stroke-width="8"/><circle cx="{C[0]}" cy="{C[1]}" r="215" fill="#FFFFFF" stroke="#0D6B68" stroke-width="6"/><circle cx="{C[0]}" cy="{C[1]}" r="130" fill="#E6F0F7" stroke="#2F6F9F" stroke-width="6"/><circle cx="{C[0]}" cy="{C[1]}" r="52" fill="#D97A2B" stroke="#B8442D" stroke-width="6"/><line x1="{start[0]}" y1="{start[1]}" x2="{lend[0]}" y2="{lend[1]}" stroke="#B8442D" stroke-width="10" stroke-linecap="round" stroke-dasharray="1 22"/>{dhead}<line x1="{T[0]}" y1="{T[1]}" x2="{r1(base[0])}" y2="{r1(base[1])}" stroke="#102A2B" stroke-width="10" stroke-linecap="round"/>{fl}{head}</svg>'''
(root/"hero.svg").write_text(svg+"\n", encoding="utf-8")
