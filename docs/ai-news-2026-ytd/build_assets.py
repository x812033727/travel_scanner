"""Original topic-specific SVG illustrations using Mokaair's established palette."""
import importlib.util,json,sys
from pathlib import Path
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
spec=importlib.util.spec_from_file_location('news_art',HERE.parent/'ai-news-2026-09/build_assets.py')
art=importlib.util.module_from_spec(spec);spec.loader.exec_module(art)
rect,line,circle,label,document,check,envelope,calendar=art.rect,art.line,art.circle,art.label,art.document,art.check,art.envelope,art.calendar
CREAM,INK,TEAL,PALE,BLUE,ORANGE=art.CREAM,art.INK,art.TEAL,art.PALE,art.BLUE,art.ORANGE
LOCALES=['zh-TW','en','ja','ko','zh-CN']

def chip(x,y,w=240,h=200):
    b=rect(x,y,w,h,PALE)+rect(x+35,y+35,w-70,h-70,'#FFFFFF',BLUE,12)
    for i in range(4):
        b+=line(x-25,y+30+i*45,x,y+30+i*45,TEAL,7)+line(x+w,y+30+i*45,x+w+25,y+30+i*45,TEAL,7)
    return b

def monitor(x=510,y=280,w=580,h=330):
    return rect(x,y,w,h,'#FFFFFF',INK)+rect(x+25,y+25,w-50,h-65,PALE,'none')+line(x+w/2,y+h,x+w/2,y+h+60,INK,12)+line(x+w/2-85,y+h+65,x+w/2+85,y+h+65,INK,12)

def lock(x,y):
    return rect(x,y,140,120,'#FFFFFF',BLUE)+f'<path d="M{x+28} {y} V{y-48} a42 42 0 0 1 84 0 V{y}" fill="none" stroke="{BLUE}" stroke-width="10"/>'+circle(x+70,y+48,12,BLUE,'none')+line(x+70,y+52,x+70,y+85,BLUE,9)

def play(x,y,color=ORANGE):
    return circle(x,y,70,'#FFFFFF',color)+f'<path d="M{x-18} {y-33} l55 33 l-55 33 Z" fill="{color}"/>'

def music(x,y):
    return circle(x,y,32,ORANGE,'none')+line(x+28,y,x+28,y-160,ORANGE,13)+line(x+28,y-160,x+140,y-183,ORANGE,20)+line(x+140,y-183,x+140,y-23,ORANGE,13)+circle(x+110,y-20,32,ORANGE,'none')

def drawing(slug):
    if 'nvidia-rubin' in slug:
        b=''.join(rect(230+i*365,240,260,400,'#FFFFFF',TEAL if i%2==0 else BLUE) for i in range(3))
        for c in range(3):
            for r in range(3):b+=rect(260+c*365,285+r*108,200,70,PALE,'none',12)+circle(290+c*365,320+r*108,10,ORANGE,'none')+line(330+c*365,320+r*108,430+c*365,320+r*108,TEAL,7)
        return b+line(355,665,355,715)+line(720,665,720,715)+line(1085,665,1085,715)+line(355,715,1085,715)
    if 'chatgpt-health' in slug:
        return document(260,285,290,350)+line(365,240,365,325,ORANGE,18)+line(322,282,408,282,ORANGE,18)+calendar(680,285,280,260)+line(560,460,655,460)+line(975,460,1085,460)+lock(1130,390)
    if 'personal-intelligence' in slug:
        return envelope(240,260)+rect(260,520,220,160,PALE,BLUE)+circle(415,560,20,ORANGE,'none')+chip(685,350)+line(505,355,665,430)+line(495,590,665,490)+line(950,450,1100,450)+lock(1130,405)
    if 'gpt-53-codex' in slug:
        return document(240,315,230,310)+monitor(590,270,620,350)+label(900,440,'{  }',120)+line(470,460,565,460)+check(1230,620)
    if 'opus-46' in slug:
        return document(230,255,220,320)+document(470,340,220,320)+document(740,260,220,320)+circle(1175,420,112,'#FFFFFF',BLUE)+line(1255,500,1360,620,BLUE,28)+line(1120,415,1230,415,BLUE,10)+line(1175,365,1175,470,BLUE,10)
    if 'qwen-35' in slug:
        return chip(620,250,320,250)+line(780,515,780,625,ORANGE,14)+f'<path d="M725 580 L780 635 L835 580" fill="none" stroke="{ORANGE}" stroke-width="14"/>'+document(250,330,230,300)+monitor(1100,335,280,195)+line(505,480,595,400)+line(965,400,1070,420)
    if 'gemini-31-pro' in slug:
        return chip(680,330)+document(245,245,250,320)+line(510,400,650,425)+rect(1060,280,275,320,'#FFFFFF',BLUE)+line(1100,540,1100,450,BLUE,22)+line(1170,540,1170,390,TEAL,22)+line(1240,540,1240,345,ORANGE,22)+line(945,425,1030,425)
    if 'gpt-54' in slug:
        return monitor(465,240,640,360)+document(210,340,195,265)+rect(1170,330,210,240,'#FFFFFF',BLUE)+line(1200,395,1350,395,BLUE,7)+line(1200,460,1350,460,BLUE,7)+check(785,460)+line(405,480,450,480)+line(1115,475,1160,475)
    if 'interactive-visuals' in slug:
        return rect(300,250,980,390)+rect(345,290,345,310,PALE,'none')+circle(520,440,102,'#FFFFFF',BLUE)+f'<path d="M520 440 L520 338 A102 102 0 0 1 608 491 Z" fill="{ORANGE}"/>'+line(770,380,1190,380,BLUE,10)+circle(880,380,24,'#FFFFFF',BLUE)+line(770,490,1190,490)+circle(1080,490,24,'#FFFFFF')
    if 'lyria-3-pro' in slug:
        return rect(245,250,1110,390)+''.join(line(300,330+i*55,1300,330+i*55,'#B1CCC6',5) for i in range(5))+music(450,545)+music(800,490)+rect(1120,295,185,65,PALE,'none')+label(1212,340,'3:00',36)
    if 'glasswing' in slug:
        return f'<path d="M780 240 L1000 315 V460 Q1000 625 780 720 Q560 625 560 460 V315 Z" fill="{PALE}" stroke="{TEAL}" stroke-width="10"/>'+lock(710,400)+document(220,335,235,280)+document(1100,335,235,280)+line(465,460,530,460)+line(1030,460,1090,460)
    if 'muse-spark' in slug:
        return rect(270,280,300,270,PALE)+rect(1020,400,310,240,'#FFFFFF',BLUE)+circle(800,440,115,'#FFFFFF')+circle(800,440,48,ORANGE,'none')+line(580,405,665,425)+line(935,480,1000,510)+circle(345,360,23,TEAL,'none')+line(405,360,510,360)+line(330,445,510,445)+line(1080,490,1270,490,BLUE,10)+line(1080,560,1200,560,BLUE,10)
    if 'images-20' in slug:
        return rect(300,245,910,420)+f'<path d="M340 610 L530 400 L710 560 L950 345 L1170 610 Z" fill="{PALE}"/>'+circle(1070,350,40,ORANGE,'none')+rect(380,300,260,65,'#FFFFFF',BLUE,10)+line(420,333,600,333,BLUE,8)+line(1170,640,1330,365,ORANGE,32)
    if 'gpt-55' in slug:
        return document(230,260,235,310)+document(515,360,235,310)+monitor(875,260,470,300)+line(470,430,500,490)+line(765,485,850,420)+check(1110,410)
    if 'gemini-omni' in slug:
        return rect(235,250,1130,400,'#FFFFFF',INK)+''.join(rect(265+i*365,290,325,310,PALE if i!=1 else '#E6F0F7','none',12) for i in range(3))+play(790,445)+circle(410,410,48,ORANGE,'none')+line(1100,380,1220,510,BLUE,16)+line(1085,510,1240,365,BLUE,16)
    if 'gemini-spark' in slug:
        return calendar(260,275,330,330)+circle(890,435,145,'#FFFFFF',BLUE)+line(890,435,890,335,BLUE,12)+line(890,435,975,465,BLUE,12)+envelope(1160,475,230,160)+line(615,440,705,440)+line(1050,470,1140,540)
    if 'fable-5-access' in slug:
        return document(210,285,235,310)+line(465,440,620,440)+rect(655,280,310,320,PALE)+line(750,370,750,510,ORANGE,30)+line(865,370,865,510,ORANGE,30)+line(985,440,1130,440)+check(1260,440)
    if 'gpt-56-sol' in slug:
        return chip(645,300,320,250)+document(250,345,235,300)+line(500,470,610,430)+line(995,430,1100,470)+lock(1140,420)+''.join(circle(705+i*100,650,20,TEAL if i!=1 else ORANGE,'none') for i in range(3))
    if 'sonnet-5' in slug:
        return document(280,265,320,370)+rect(755,255,545,395,'#FFFFFF',BLUE)+line(815,340,1235,340,BLUE,8)+line(815,420,1235,420,BLUE,8)+line(815,500,1110,500,BLUE,8)+circle(1115,610,75,PALE)+label(1115,633,'$',65)+line(630,440,715,440)
    if 'chatgpt-work' in slug:
        return document(190,280,255,320)+rect(570,345,385,275,PALE)+''.join(line(600,410+i*60,920,410+i*60,'#92BDB7',7) for i in range(3))+monitor(1080,245,330,235)+line(460,425,550,460)+line(975,460,1070,400)+check(1235,625)
    if 'gemini-36' in slug:
        return chip(630,350)+document(220,280,240,330)+line(490,425,590,425)+line(910,420,1100,300,BLUE)+line(910,490,1100,615,ORANGE)+rect(1130,240,210,170,'#FFFFFF',BLUE)+check(1235,620)+line(1180,300,1290,300,BLUE,8)+line(1180,350,1260,350,BLUE,8)
    return ''.join(rect(270+c*370,215+r*165,310,130,'#FFFFFF',TEAL if (r+c)%2==0 else BLUE,18)+label(425+c*370,300+r*165,f'{r*3+c+1:02d}',64) for r in range(3) for c in range(3))+line(360,720,1220,720,ORANGE,8)

def main():
    jobs=[];manifest=[]
    research=sorted((json.loads(p.read_text(encoding='utf8')) for p in (HERE/'research').glob('*.json')),key=lambda x:(x['event_date'],x['slug']))
    for item in research:
        slug=item['slug'];pack=json.loads((ROOT/'apps/api/app/guides/content'/f'{slug}.json').read_text(encoding='utf8'))
        target=ROOT/'apps/web/public/guides'/slug;target.mkdir(parents=True,exist_ok=True)
        for locale,doc in pack['locales'].items():
            suffix='' if locale=='zh-TW' else '-'+locale.lower()
            localized=item.get('translations',{}).get(locale,{})
            credits={'zh-TW':'© Mokaair 製圖 2026','zh-CN':'© Mokaair 制图 2026','en':'© Mokaair Illustration 2026','ja':'© Mokaair 作図 2026','ko':'© Mokaair 제작 2026'}
            if '--finalize' not in sys.argv:
                body=label(80,100,'MOKAAIR  /  AI NEWS',34,TEAL,'start')+label(1510,100,item['event_date'],28,BLUE,'end')
                body+=drawing(slug)+label(800,805,localized.get('hero_label',item['hero_label']),48,max_width=1400)+label(1535,868,credits[locale],20,'#5C6B6B','end')
                (target/f'hero{suffix}.svg').write_text(art.svg(doc['title'],doc['hero']['alt'],body),encoding='utf8')
                (target/f'diagram-1{suffix}.svg').write_text(art.diagram(localized.get('diagram',item['diagram']),locale),encoding='utf8')
            for kind in ['hero','diagram-1']:
                png=HERE/'renders'/f'{slug}-{locale}-{kind}.png'
                jobs.append({'svg':str(target/f'{kind}{suffix}.svg'),'png':str(png)})
                if '--finalize' in sys.argv and kind=='hero':
                    with Image.open(png) as im:
                        assert im.size==(1600,900)
                        im.convert('RGB').save(target/f'hero{suffix}.jpg',quality=88,optimize=True,progressive=True)
        manifest.append({'slug':slug,'title':item['title'],'event_date':item['event_date'],'url':f'https://mokaair.com/zh-TW/life/{slug}','locales':{l:{'title':d['title'],'url':f'https://mokaair.com/{l}/life/{slug}'} for l,d in pack['locales'].items()}})
    (HERE/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    (HERE/'renders/jobs.json').write_text(json.dumps(jobs),encoding='utf8')
    if '--finalize' in sys.argv:
        for kind in ['hero','diagram-1']:
            for locale in LOCALES:
                for start in range(0,len(manifest),4):
                    sheet=Image.new('RGB',(1600,960),CREAM);draw=ImageDraw.Draw(sheet)
                    for j,item in enumerate(manifest[start:start+4]):
                        with Image.open(HERE/'renders'/f"{item['slug']}-{locale}-{kind}.png") as im:sheet.paste(im.resize((800,450)),((j%2)*800,(j//2)*480))
                        draw.text(((j%2)*800+15,(j//2)*480+456),item['slug']+' '+locale,fill=INK)
                    sheet.save(HERE/f'{kind}-sheet-{start//4+1}-{locale}.jpg',quality=90)
    print('Prepared localized artwork jobs:',len(jobs))
if __name__=='__main__':main()
