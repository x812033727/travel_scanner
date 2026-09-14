"""Build ten original SVG illustrations, diagrams and review contact sheets.

Run with the repository API Python environment. CHROMIUM_BIN may override Edge.
Only writes this batch's exact image directories and this evidence directory.
"""
from __future__ import annotations

import html
import json
import os
from pathlib import Path
import subprocess
import tempfile
import time
import sys

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CONTENT = ROOT / "apps/api/app/guides/content"
PUBLIC = ROOT / "apps/web/public"
CREAM, INK, TEAL, PALE, BLUE, ORANGE = "#F7F1E8", "#102A2B", "#0D6B68", "#E3F0EF", "#2F6F9F", "#D97A2B"
CACHED = sorted((Path(os.environ.get("LOCALAPPDATA", "."))/"ms-playwright").glob("chromium_headless_shell-*/chrome-headless-shell-win64/chrome-headless-shell.exe"))
CHROME = os.environ.get("CHROMIUM_BIN") or (str(CACHED[-1]) if CACHED else r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")


def rect(x, y, w, h, fill="#FFFFFF", stroke=TEAL, rx=24):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="6"/>'


def line(x1, y1, x2, y2, color=TEAL, width=12):
    return f'<path d="M{x1} {y1} L{x2} {y2}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round"/>'


def circle(x, y, r, fill=PALE, stroke=TEAL):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="6"/>'


def label(x, y, value, size=40, fill=INK, anchor="middle", max_width=None):
    if max_width:
        units=sum(1 if ord(c)>255 else 0.58 for c in value)
        size=min(size,round(max_width/max(units,1),1))
    return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="600" fill="{fill}" text-anchor="{anchor}">{html.escape(value)}</text>'


def document(x, y, w=220, h=270):
    return rect(x, y, w, h) + "".join(line(x+35, y+55+i*44, x+w-35-(i%2)*30, y+55+i*44, "#92BDB7", 12) for i in range(4))


def check(x, y):
    return circle(x, y, 66, PALE) + f'<path d="M{x-30} {y} l22 24 l43 -51" stroke="{TEAL}" fill="none" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/>'


def envelope(x, y, w=250, h=170):
    return rect(x,y,w,h) + f'<path d="M{x+10} {y+12} L{x+w/2} {y+h*.57} L{x+w-10} {y+12}" fill="none" stroke="{TEAL}" stroke-width="8"/>'


def calendar(x, y, w=240, h=230):
    return rect(x,y,w,h) + rect(x+4,y+4,w-8,54,PALE,"none",18) + line(x+65,y-18,x+65,y+22) + line(x+w-65,y-18,x+w-65,y+22) + "".join(circle(x+55+c*65,y+107+r*61,10,TEAL,"none") for c in range(3) for r in range(2))


def svg(title, desc, body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900" width="1600" height="900" role="img" aria-labelledby="title desc" font-family="'Microsoft JhengHei','Noto Sans TC',sans-serif">
<title id="title">{html.escape(title)}</title><desc id="desc">{html.escape(desc)}</desc>
<rect width="1600" height="900" fill="{CREAM}"/>{body}</svg>'''


def hero(index, title, alt, hero_label=None):
    b = circle(800,440,305,PALE,"none") + circle(225,675,72,"#F0DBC4","none") + circle(1360,220,55,"#DBE8F2","none")
    if index == 0:
        b += document(335,270,280,340)+document(920,245,270,330)+line(650,440,875,440)+check(1135,590)
        b += circle(715,370,72,"#FFFFFF",BLUE)+line(765,425,825,485,BLUE,24)
    elif index == 1:
        b += rect(370,485,175,165,TEAL,"none")+rect(580,400,175,250,BLUE,"none")+rect(790,305,175,345,ORANGE,"none")
        b += document(1070,325,220,310)+line(320,685,1310,685,INK,8)
        b += circle(1145,590,60,"#F0DBC4",ORANGE)+circle(1220,605,46,"#F0DBC4",ORANGE)
    elif index == 2:
        b += rect(365,260,550,365)+rect(410,320,330,70,PALE,"none")+line(420,445,850,445,"#92BDB7")+line(420,510,785,510,"#92BDB7")
        b += rect(1010,300,250,205,"#E6F0F7",BLUE)+line(1050,555,1210,555,BLUE)+check(930,610)
        b += ''.join(line(1040+i*23,340,1040+i*23,460,BLUE,5+(i%3)*3) for i in range(9))
    elif index == 3:
        b += rect(325,360,320,210)+line(650,465,820,310)+line(650,465,820,620)
        b += circle(930,310,110,"#FFFFFF",BLUE)+circle(930,620,110,"#FFFFFF",ORANGE)
        b += line(880,310,980,310,BLUE,16)+line(930,260,930,360,BLUE,16)
        b += ''.join(circle(875+c*55,620,10,ORANGE,"none") for c in range(3))+check(1240,465)
    elif index == 4:
        b += rect(640,235,275,420,"#FFFFFF",INK,42)+rect(675,290,205,230,PALE,"none")
        b += envelope(260,330)+calendar(1050,380)+line(520,410,615,410)+line(940,465,1020,465)
        b += ''.join(line(705+i*32,400-abs(3-i)*14,705+i*32,430+abs(3-i)*14,TEAL,10) for i in range(5))
        b += circle(777,590,18,TEAL,"none")
    elif index == 5:
        b += circle(800,435,120,"#FFFFFF")+circle(800,435,60,TEAL,"none")+line(650,435,465,435)+line(945,435,1110,435)
        b += document(230,300,235,300)+rect(1110,290,255,315,"#E6F0F7",BLUE)
        b += rect(1180,410,115,100,"#FFFFFF",BLUE)+f'<path d="M1200 410 V375 a38 38 0 0 1 76 0 v35" fill="none" stroke="{BLUE}" stroke-width="10"/>'
    elif index == 6:
        b += rect(285,255,430,220)+rect(910,340,380,300)+line(720,390,880,465)
        b += circle(340,315,18,BLUE,"none")+line(385,315,660,315,BLUE,10)+line(335,390,630,390,"#92BDB7")
        b += ''.join(line(940,410+i*65,1255,410+i*65,"#92BDB7",7) for i in range(3))+''.join(line(1000+i*83,380,1000+i*83,605,"#92BDB7",7) for i in range(3))
        b += check(745,630)
    elif index == 7:
        b += rect(370,245,740,400,"#FFFFFF",INK)+rect(405,285,670,310,PALE,"none")+line(740,650,740,715,INK,18)+line(610,730,870,730,INK,18)
        b += document(490,335,175,210)+calendar(730,330,235,210)+document(1145,410,175,225)
        b += f'<path d="M965 515 l0 165 l48 -46 l40 80 l35 -17 l-41 -80 l70 -8 Z" fill="{ORANGE}" stroke="{CREAM}" stroke-width="6"/>'
    elif index == 8:
        b += rect(300,260,990,375)+''.join(line(350,350+i*58,1240,350+i*58,"#B1CCC6",5) for i in range(4))
        b += '<path d="M380 480 C440 210 485 710 550 440 S660 320 725 450 S840 635 910 395 S1050 560 1200 420" fill="none" stroke="#0D6B68" stroke-width="13"/>'
        b += circle(585,580,29,ORANGE,"none")+line(612,575,612,365,ORANGE,10)+line(612,365,700,343,ORANGE,16)
    else:
        b += rect(340,255,860,390)+f'<path d="M385 595 L580 400 L750 540 L900 365 L1155 595 Z" fill="{PALE}"/>'+circle(1050,350,44,"#F0DBC4","none")
        b += '<rect x="500" y="350" width="315" height="225" rx="12" fill="none" stroke="#2F6F9F" stroke-width="8" stroke-dasharray="20 14"/>'
        b += line(1130,665,1295,425,ORANGE,40)+circle(1295,425,24,ORANGE,"none")+rect(920,605,175,85,"#E6F0F7",BLUE)
    hero_labels=["工作交接","用量與帳單","清楚標示來源","回答之前先想清楚","用語音整理一天","能力與存取資格","模型到日常工具","交付電腦工作","把想法變成音樂","保留重點再修改"]
    b += label(800,805,hero_label or hero_labels[index],52,max_width=1400)
    return svg(title,alt,b)


def diagram(data,locale='zh-TW'):
    b = label(800,102,data['title'],46,max_width=1440)
    positions=[(110,180),(850,180),(110,500),(850,500)]
    for i,((x,y),(heading,detail)) in enumerate(zip(positions,data['nodes'])):
        b += rect(x,y,640,245, "#FFFFFF", TEAL if i%2==0 else BLUE)
        b += circle(x+63,y+66,23,TEAL if i%2==0 else BLUE,"none")
        b += label(x+360,y+91,heading,44,max_width=510)+label(x+320,y+168,detail,32,"#5C6B6B",max_width=580)
    credits={'zh-TW':'© Mokaair 製圖 2026','zh-CN':'© Mokaair 制图 2026','en':'© Mokaair Illustration 2026','ja':'© Mokaair 作図 2026','ko':'© Mokaair 제작 2026'}
    b += label(1540,865,credits[locale],20,"#5C6B6B","end")
    return svg(data['title'],data['caption'],b)


def render(svg_file, png):
    png.unlink(missing_ok=True)
    with tempfile.TemporaryDirectory(prefix="mokaair-news-render-",ignore_cleanup_errors=True) as temp:
        page=Path(temp)/"render.html"
        page.write_text('<!doctype html><meta charset="utf-8"><style>html,body{margin:0}svg{display:block;width:1600px;height:900px}</style>'+svg_file.read_text(encoding="utf-8"),encoding="utf-8")
        command=[CHROME,"--headless","--disable-gpu","--no-first-run","--hide-scrollbars","--force-device-scale-factor=1","--window-size=1600,900",f"--user-data-dir={temp}/profile",f"--screenshot={png}",page.as_uri()]
        p=subprocess.run(command,capture_output=True,encoding="utf-8",errors="replace",timeout=60,creationflags=getattr(subprocess,"CREATE_NO_WINDOW",0))
        # Some Windows browser launchers return before their rendering child finishes.
        for _ in range(40):
            if png.exists():
                break
            time.sleep(0.25)
        if not png.exists():
            raise RuntimeError(f"render failed {svg_file.name}: {p.stderr[-800:]}")


def main():
    (HERE/"renders").mkdir(exist_ok=True)
    manifest=[]
    jobs=[]
    for research_file in sorted((HERE/"research").glob("*.json")):
        research=json.loads(research_file.read_text(encoding="utf-8"))
        slug=research['slug']
        pack=json.loads((CONTENT/f"{slug}.json").read_text(encoding="utf-8"))
        target=PUBLIC/"guides"/slug
        target.mkdir(parents=True,exist_ok=True)
        for locale,doc in pack['locales'].items():
            suffix='' if locale=='zh-TW' else '-'+locale.lower()
            localized=research.get('translations',{}).get(locale,{})
            if '--finalize' not in sys.argv:
                (target/f"hero{suffix}.svg").write_text(hero(research['hero_style'],doc['title'],doc['hero']['alt'],localized.get('hero_label')),encoding="utf-8")
                (target/f"diagram-1{suffix}.svg").write_text(diagram(localized.get('diagram',research['diagram']),locale),encoding="utf-8")
            for kind in ['hero','diagram-1']:
                png=(HERE/"renders"/f"{slug}-{locale}-{kind}.png").resolve()
                jobs.append({'svg':str((target/f'{kind}{suffix}.svg').resolve()),'png':str(png)})
                if '--svg-only' in sys.argv:continue
                if '--finalize' not in sys.argv:render(target/f"{kind}{suffix}.svg",png)
                if kind=='hero':
                    with Image.open(png) as picture:
                        assert picture.size==(1600,900),picture.size
                        picture.convert('RGB').save(target/f"hero{suffix}.jpg",quality=88,optimize=True,progressive=True)
        doc=pack['locales']['zh-TW']
        manifest.append({'slug':slug,'title':doc['title'],'event_date':research['event_date'],'url':f'https://mokaair.com/zh-TW/life/{slug}',
            'locales':{locale:{'title':doc['title'],'url':f'https://mokaair.com/{locale}/life/{slug}'} for locale,doc in pack['locales'].items()}})
        print(f"prepared {slug}",flush=True)
    manifest.sort(key=lambda v:v['event_date'])
    (HERE/"manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (HERE/'renders/jobs.json').write_text(json.dumps(jobs),encoding='utf-8')
    if '--svg-only' in sys.argv:return
    for kind in ['hero','diagram-1']:
        for locale in pack['locales']:
            for start in range(0,len(manifest),4):
                sheet=Image.new('RGB',(1600,960),CREAM)
                draw=ImageDraw.Draw(sheet)
                for j,item in enumerate(manifest[start:start+4]):
                    with Image.open(HERE/"renders"/f"{item['slug']}-{locale}-{kind}.png") as picture:
                        sheet.paste(picture.resize((800,450)),((j%2)*800,(j//2)*480))
                    draw.text(((j%2)*800+20,(j//2)*480+455),item['slug']+' '+locale,fill=INK)
                suffix='' if locale=='zh-TW' else '-'+locale
                sheet.save(HERE/f"{kind}-sheet-{start//4+1}{suffix}.jpg",quality=92)


if __name__=='__main__':
    main()
