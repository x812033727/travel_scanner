"""Original, unbranded editorial illustrations and large-type instructional figures."""
from __future__ import annotations

import html
import json
from pathlib import Path

DATA = json.loads(Path(__file__).with_name("artwork.json").read_text(encoding="utf-8"))
COLORS = {"A": "#176A66", "B": "#315F91", "C": "#87583B", "D": "#32765B", "E": "#415C8A", "F": "#795284", "G": "#AF5039", "H": "#286778"}
INK = "#163431"
PAPER = "#FBF7F0"
GOLD = "#EDB960"


def rect(x, y, width, height, color, radius=24, stroke="none", sw=0):
    return f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="{radius}" fill="{color}" stroke="{stroke}" stroke-width="{sw}"/>'


def circle(x, y, radius, color, stroke="none", sw=0):
    return f'<circle cx="{x}" cy="{y}" r="{radius}" fill="{color}" stroke="{stroke}" stroke-width="{sw}"/>'


def path(d, color="none", stroke=INK, sw=12):
    return f'<path d="{d}" fill="{color}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>'


def lines(x, y, color, count=3, width=260):
    return "".join(rect(x, y+i*55, width-i*30, 15, color, 7) for i in range(count))


def page(x, y, color, width=300, height=390):
    count = max(1, min(4, (height - 100) // 55 + 1))
    return rect(x+12,y+16,width,height,INK,24)+rect(x,y,width,height,PAPER,24,color,8)+lines(x+40,y+70,color,count,width-80)


def screen(color, terminal=False):
    value = rect(180,110,710,425,INK,32)+rect(205,135,660,345,color if terminal else PAPER,14)
    value += path("M120 570 H950 L1000 625 H70 Z",GOLD,INK,10)
    if terminal:
        value += path("M260 210 L310 250 L260 290 M350 292 H475",stroke=PAPER,sw=20)
        value += lines(260,350,"#B9D6C8",2,440)
    else:
        value += rect(235,165,600,45,"#DCE9E1",12)+circle(262,187,9,color)+circle(295,187,9,GOLD)
        value += rect(245,245,195,180,color,18)+lines(480,260,color,3,300)
    return value


def motif(name, color):
    if name in ("terminal", "browser", "laptop"):
        return screen(color, name=="terminal") + (page(820,330,color,210,250) if name=="browser" else "")
    if name == "phone":
        value=rect(315,65,330,555,INK,55)+rect(337,90,286,500,PAPER,38)
        value+=rect(415,111,130,18,INK,9)+rect(365,175,230,145,color,26)
        value+=path("M390 360 Q450 320 515 375 T590 360",stroke=GOLD,sw=18)+lines(370,435,color,2,200)
        return value+circle(820,350,108,GOLD)+path("M755 350 L800 395 L885 300",stroke=INK,sw=19)
    if name in ("files", "book", "library"):
        if name=="book":
            return path("M530 180 Q320 70 150 155 V560 Q330 480 530 585 Q750 480 930 560 V155 Q720 70 530 180 Z",PAPER,color,14)+path("M530 180 V585",stroke=color,sw=10)+lines(215,240,color,4,245)+lines(600,240,color,4,245)+path("M770 125 V340 L810 305 L850 342 V130",GOLD,GOLD,5)
        value=page(215,180,color)+page(430,115,color)+page(660,205,color)
        return value+(path("M110 630 H1070",stroke=INK,sw=30) if name=="library" else circle(860,505,82,GOLD)+path("M810 505 L847 544 L910 465",stroke=INK,sw=15))
    if name in ("chat", "history"):
        value=rect(160,115,590,235,PAPER,44,color,12)+path("M270 350 L265 405 L360 350",PAPER,color,10)+lines(220,175,color,2,430)
        value+=rect(510,390,490,185,color,38)+path("M830 575 L895 625 L895 570",color,color,8)+lines(570,445,PAPER,2,360)
        if name=="history": value+=circle(870,205,100,GOLD)+path("M870 142 V205 L920 245",stroke=INK,sw=14)
        else: value+=circle(850,210,18,GOLD)+circle(910,210,18,GOLD)+circle(970,210,18,GOLD)
        return value
    if name in ("pen", "recipe"):
        value=page(330,80,color,470,525)
        value+=path("M770 190 L850 245 L595 585 L515 620 L530 530 Z",GOLD,INK,10)
        if name=="recipe":
            for y in (180,300,420): value+=rect(185,y,95,80,color,18)+path(f"M205 {y+40} l18 18 l37 -40",stroke=PAPER,sw=10)
        return value
    if name in ("switch", "grid", "chart"):
        value=rect(145,115,800,455,PAPER,35,color,12)
        if name=="switch":
            for i,x in enumerate((330,550,770)):
                value+=path(f"M{x} 210 V495",stroke="#C7DDD2",sw=18)+rect(x-45,260+i%2*115,90,55,color,18)
        elif name=="grid":
            for y in (215,305,395,485): value+=path(f"M190 {y} H900",stroke="#C7DDD2",sw=6)
            for x in (380,560,740): value+=path(f"M{x} 160 V525",stroke="#C7DDD2",sw=6)
            value+=rect(567,312,166,76,GOLD,4)+rect(747,402,150,76,color,4)
        else:
            value+=path("M245 185 V485 H855",stroke=INK,sw=10)
            for x,h in ((330,120),(490,200),(650,290)):value+=rect(x,480-h,92,h,color,12)
            value+=path("M325 315 L490 245 L700 165",stroke=GOLD,sw=17)
        return value
    if name in ("research", "search"):
        value=page(190,125,color,420,455)
        value+=circle(710,290,150,PAPER,color,25)+path("M820 400 L990 580",stroke=INK,sw=65)
        value+=lines(635,260,color,2,150)
        if name=="research":value+=page(85,330,color,220,275)
        return value
    if name == "balance":
        return path("M570 135 V555 M400 590 H740 M290 215 H860",stroke=INK,sw=22)+circle(570,210,45,GOLD)+path("M300 235 L195 425 H405 Z",PAPER,color,10)+path("M850 235 L745 425 H955 Z",PAPER,color,10)+path("M190 430 Q300 580 410 430 Z",color,color,9)+path("M740 430 Q850 580 960 430 Z",color,color,9)
    if name == "shield":
        return path("M565 90 Q760 180 870 165 V355 Q850 515 565 645 Q280 515 260 355 V165 Q370 180 565 90 Z",color,INK,14)+path("M420 350 L525 455 L740 235",stroke=PAPER,sw=38)+circle(240,550,57,GOLD)
    if name == "key":
        return circle(360,270,145,color,INK,15)+circle(360,270,68,PAPER)+path("M480 360 L785 625 L865 555 L795 490 L735 535 L680 485 L725 440 L545 310 Z",GOLD,INK,12)
    if name == "clock":
        return circle(540,340,245,PAPER,color,22)+path("M540 170 V340 L690 435",stroke=INK,sw=28)+circle(540,340,22,GOLD)+rect(790,440,225,155,color,20)+lines(820,485,PAPER,2,150)+path("M320 110 L260 65 M760 105 L815 60",stroke=GOLD,sw=25)
    if name == "microphone":
        value=rect(420,100,210,330,color,100,INK,12)+path("M350 310 V350 Q350 490 525 500 Q700 490 700 350 V310 M525 505 V620 M430 625 H620",stroke=INK,sw=20)
        for i,h in enumerate((50,110,170,100)):value+=rect(800+i*48,340-h/2,19,h,GOLD,9)
        return value
    if name in ("team", "chain", "tree", "pipeline"):
        positions=[(240,335),(560,200),(890,370)] if name in ("team","chain") else [(240,190),(570,380),(910,195)]
        value=path("M240 335 Q530 20 890 370" if name in ("team","chain") else "M240 190 V380 H910 V195",stroke=GOLD,sw=26)
        for i,(x,y) in enumerate(positions):
            if name=="team":value+=circle(x,y-60,55,color)+path(f"M{x-100} {y+140} V{y+60} Q{x} {y-40} {x+100} {y+60} V{y+140} Z",PAPER,color,10)
            else:value+=rect(x-95,y-85,190,170,PAPER,28,color,12)+lines(x-56,y-35,color,2,115)
        if name=="tree":value+=page(80,450,color,210,200)
        return value
    if name in ("canvas", "palette", "film"):
        value=rect(170,90,790,500,PAPER,28,color,12)
        value+=path("M205 540 L410 325 L575 470 L735 240 L925 535 Z",color,color,5)+circle(380,230,63,GOLD)
        if name=="film":
            value+=rect(175,90,780,65,INK,5)+rect(175,535,780,55,INK,5)
            for x in range(210,930,90):value+=rect(x,105,40,30,PAPER,2)+rect(x,547,40,28,PAPER,2)
        elif name=="palette":value+=circle(900,485,140,GOLD)+circle(880,440,26,color)+circle(965,500,24,INK)+circle(830,530,24,PAPER)
        else:value+=path("M895 255 L1010 480 L925 465 L875 540 L835 510 L875 440 L820 395 Z",GOLD,INK,8)
        return value
    if name=="cards":
        return page(170,190,color,290,360)+page(470,120,color,290,360)+page(760,250,color,250,335)+circle(620,465,60,GOLD)+path("M590 465 L615 488 L655 440",stroke=INK,sw=12)
    if name=="map":
        return path("M150 180 L400 90 L700 200 L985 100 V550 L710 645 L420 530 L150 630 Z",PAPER,color,12)+path("M410 110 V520 M710 215 V625",stroke="#C7DDD2",sw=10)+path("M280 410 Q470 265 550 430 T860 310",stroke=GOLD,sw=18)+circle(285,400,27,color)+circle(860,310,30,color)
    if name=="tabs":
        return rect(170,105,670,400,"#C7DDD2",30,color,10)+rect(340,215,670,400,PAPER,30,color,12)+rect(375,250,200,45,GOLD,12)+lines(395,350,color,4,470)
    raise ValueError(f"No artwork for {name}")


def artwork(article: dict, blocks: list[dict], folder: Path) -> dict:
    number=article["number"]
    spec=DATA[str(number)]
    color=COLORS.get(article["group"],COLORS["A"])
    esc=html.escape
    base='<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900" role="img" aria-labelledby="title desc" font-family="Microsoft JhengHei,Noto Sans TC,sans-serif">'
    hero_desc=f'{spec["title"]}的原創插畫，以文件、裝置與流程等物件呼應{article["purpose"]}；非產品介面。'
    hero=base+f'<title id="title">{esc(article["title"])}</title><desc id="desc">{esc(hero_desc)}</desc>'
    hero+=rect(0,0,1600,900,"#F5EFE4",0)+circle(1300,220,360,"#E4EBDF")+circle(150,800,280,"#F2DEB8")
    hero+=f'<g transform="translate({170+(number%3)*20},170) scale(1.03)">{motif(spec["motif"],color)}</g>'
    hero+=f'<text x="90" y="115" font-size="54" font-weight="700" fill="{INK}">{esc(spec["title"])}</text></svg>'
    (folder/'hero.svg').write_text(hero,encoding='utf-8')
    desc="；".join(f'{title}：{detail}' for title,detail in spec['steps'])
    svg=base+f'<title id="title">{esc(spec["title"])}</title><desc id="desc">{esc(desc)}</desc>'+rect(0,0,1600,900,PAPER,0)
    svg+=f'<text x="65" y="110" font-size="78" font-weight="700" fill="{INK}">{esc(spec["title"])}</text>'
    for index,(title,detail) in enumerate(spec['steps']):
        # Large labels remain readable in a single-column 360px phone article.
        for text in (title,detail):
            if sum(1 if ord(c)>255 else .55 for c in text)>16:
                raise ValueError(f'Too wide for phone diagram {number}: {text}')
        y=165+index*225
        svg+=rect(60,y,1480,207,"#FFFFFF",24,color,4)+circle(150,y+101,53,color)
        svg+=f'<text x="150" y="{y+128}" text-anchor="middle" font-size="76" font-weight="700" fill="#FFFFFF">{"一二三"[index]}</text>'
        svg+=f'<text x="245" y="{y+82}" font-size="76" font-weight="700" fill="{INK}">{esc(title)}</text>'
        svg+=f'<text x="245" y="{y+168}" font-size="76" fill="{color}">{esc(detail)}</text>'
    svg+='<text x="1530" y="876" text-anchor="end" font-size="22" fill="#49615C">© Mokaair · 教學示意</text></svg>'
    (folder/'diagram-1.svg').write_text(svg,encoding='utf-8')
    return {'hero_alt':hero_desc,'diagram_alt':desc,'diagram_caption':spec['title']+'。此為原創教學圖解，並非產品畫面或實測輸出。'}
