#!/usr/bin/env python3
"""Original editable dice explainer. Uses only Pillow + system ffmpeg.

Rendered facts are derived from lesson.json; no AI service is called at render time.
"""
import argparse
import json
import math
import pathlib
import subprocess
import sys
from functools import lru_cache

from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent
W, H, FPS, DURATION = 1280, 720, 24, 54
SCENE_TIMES = [(0, 7), (7, 16), (16, 26), (26, 34), (34, 43), (43, 54)]
CJK = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
CJK_BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
LATIN = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
LATIN_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
CJK_INDEX, CJK_BOLD_INDEX, LATIN_INDEX, LATIN_BOLD_INDEX = 3, 3, 0, 0


def discover_cjk(explicit=None, bold=False, explicit_index=None):
    """Prefer the tested Linux fonts; accept local Noto files and system TC fonts."""
    if explicit:
        chosen = pathlib.Path(explicit).expanduser()
        if not chosen.is_file():
            raise ValueError(f"Font file not found: {chosen}")
        result = (str(chosen), 0 if explicit_index is None else explicit_index)
        ImageFont.truetype(result[0], 24, index=result[1])
        return result
    weight = 'Bold' if bold else 'Regular'
    candidates = [
        (f'/usr/share/fonts/opentype/noto/NotoSansCJK-{weight}.ttc', 3),
        (str(ROOT/'fonts'/f'NotoSansCJKtc-{weight}.otf'), 0),
        ('C:/Windows/Fonts/msjhbd.ttc' if bold else 'C:/Windows/Fonts/msjh.ttc', 0),
    ]
    for candidate,index in candidates:
        if pathlib.Path(candidate).is_file():
            return candidate, index if explicit_index is None else explicit_index
    # macOS PingFang is a collection: select its Traditional Chinese face by name.
    mac_font = pathlib.Path('/System/Library/Fonts/PingFang.ttc')
    if mac_font.is_file():
        options=[]
        for index in range(32):
            try:
                family,style=ImageFont.truetype(str(mac_font),24,index=index).getname()
            except OSError:
                break
            if 'TC' in family:
                score=int(('semibold' if bold else 'regular') in style.lower())
                options.append((score,index))
        if options:
            return str(mac_font), max(options)[1] if explicit_index is None else explicit_index
    if bold:
        return discover_cjk(None,False,explicit_index)
    raise ValueError('No Traditional Chinese font found. Install Noto Sans CJK TC, or pass --font /path/to/NotoSansCJKtc-Regular.otf (and optionally --font-bold). For a TTC collection also pass --font-index if needed.')


def configure_fonts(args):
    global CJK,CJK_BOLD,LATIN,LATIN_BOLD
    global CJK_INDEX,CJK_BOLD_INDEX,LATIN_INDEX,LATIN_BOLD_INDEX
    CJK,CJK_INDEX=discover_cjk(args.font,False,args.font_index)
    try:
        CJK_BOLD,CJK_BOLD_INDEX=discover_cjk(args.font_bold,True,args.font_index)
    except (ValueError,OSError):
        if args.font and not args.font_bold:
            CJK_BOLD,CJK_BOLD_INDEX=CJK,CJK_INDEX
        else:
            raise
    if not pathlib.Path(LATIN).is_file():
        LATIN,LATIN_INDEX=CJK,CJK_INDEX
    if not pathlib.Path(LATIN_BOLD).is_file():
        LATIN_BOLD,LATIN_BOLD_INDEX=CJK_BOLD,CJK_BOLD_INDEX
    font.cache_clear()
    if not args.summary:
        print(json.dumps({'fonts':{'regular':CJK,'regular_index':CJK_INDEX,'bold':CJK_BOLD,'bold_index':CJK_BOLD_INDEX}},ensure_ascii=False))


@lru_cache(maxsize=60)
def font(size, bold=False, latin=False):
    path = (LATIN_BOLD if bold else LATIN) if latin else (CJK_BOLD if bold else CJK)
    index=(LATIN_BOLD_INDEX if bold else LATIN_INDEX) if latin else (CJK_BOLD_INDEX if bold else CJK_INDEX)
    return ImageFont.truetype(path, size, index=index)


def ease(x):
    x = max(0, min(1, x))
    return 1 - (1 - x) ** 3


class Renderer:
    def __init__(self, cfg):
        self.cfg = cfg
        self.colors = cfg["colors"]
        self.bg = self.colors["background"]
        self.ink = self.colors["ink"]
        self.red = self.colors["coral"]
        self.green = self.colors["accent"]
        self.muted = "#6B787A"
        self.line = "#D7DCD6"
        self.target = cfg["target_sum"]
        self.matches = [(a, b) for a in range(1, 7) for b in range(1, 7) if a+b == self.target]
        self.frames = {}

    def txt(self, draw, xy, s, size=28, fill=None, bold=False, latin=False, anchor=None):
        draw.text(xy, str(s), font=font(size, bold, latin), fill=fill or self.ink, anchor=anchor)

    def pill(self, draw, box, s, color=None):
        draw.rounded_rectangle(box, 13, fill=color or self.ink)
        self.txt(draw, (box[0]+15, box[1]+7), s, 19, self.bg, True)

    def base(self, step, title, subtitle=""):
        im = Image.new("RGB", (W, H), self.bg)
        d = ImageDraw.Draw(im)
        self.pill(d, (60, 37, 267, 80), "可修改的解說動畫")
        self.txt(d, (1220, 49), f"0{step+1} / 06", 19, self.muted, latin=True, anchor="ra")
        self.txt(d, (60, 106), title, 45, bold=True)
        if subtitle:
            self.txt(d, (63, 170), subtitle, 23, self.muted)
        d.line((60, 661, 1220, 661), fill=self.line, width=2)
        self.txt(d, (60, 679), "原創練習範例 · 兩顆公平、獨立的六面骰子", 17, self.muted)
        self.txt(d, (1220, 679), "資料 → 動畫 → 驗證", 17, self.muted, anchor="ra")
        return im

    def die(self, d, xy, number, size=142, color=None):
        x, y = xy
        d.rounded_rectangle((x+4, y+7, x+size+4, y+size+7), 23, fill="#E0DFD7")
        d.rounded_rectangle((x, y, x+size, y+size), 23, fill="#FFFFFF", outline=self.line, width=2)
        patterns = {1:[(1,1)], 2:[(0,0),(2,2)],3:[(0,0),(1,1),(2,2)],4:[(0,0),(0,2),(2,0),(2,2)],5:[(0,0),(0,2),(1,1),(2,0),(2,2)],6:[(0,0),(0,1),(0,2),(2,0),(2,1),(2,2)]}
        for px, py in patterns[number]:
            cx,cy=x+size*(.25+px*.25),y+size*(.25+py*.25)
            radius=size*.065
            d.ellipse((cx-radius,cy-radius,cx+radius,cy+radius), fill=color or self.ink)

    def grid(self, d, active=None, reveal=36, color=None):
        active = set(active or [])
        x0, y0, cell, gap = 116, 263, 55, 7
        self.txt(d, (300, 198), "第二顆 →", 22, self.muted, anchor="ma")
        self.txt(d, (60, 228), "第一顆", 17, self.muted)
        for n in range(1,7):
            self.txt(d, (x0+(n-1)*(cell+gap)+cell/2, y0-35), n, 22, self.muted, True, True, "ma")
            self.txt(d, (x0-30,y0+(n-1)*(cell+gap)+cell/2), n, 22, self.muted, True, True, "mm")
        for a in range(1,7):
            for b in range(1,7):
                i=(a-1)*6+b
                if i > reveal:
                    continue
                x,y=x0+(b-1)*(cell+gap),y0+(a-1)*(cell+gap)
                on=(a,b) in active
                d.rounded_rectangle((x,y,x+cell,y+cell), 10, fill=(color or self.red) if on else "#E9EBE4", outline=None if on else "#E0E4DC", width=1)
                self.txt(d, (x+cell/2,y+cell/2), a+b, 22, "#FFFFFF" if on else self.ink, on, True, "mm")

    def panel(self, d, numerator, denominator=36, caption="有利組合 / 全部組合", color=None):
        color=color or self.red
        d.rounded_rectangle((659, 250, 1210, 599), 26, fill="#FFFFFF", outline=self.line, width=1)
        self.txt(d, (702, 279), caption, 23, self.muted)
        self.txt(d, (701, 340), numerator, 112, color, True, True)
        self.txt(d, (821, 372), f"/ {denominator}", 64, self.ink, True, True)
        percentage=100*numerator/denominator
        self.txt(d, (705, 502), f"約 {percentage:.1f}%", 40, color, True)

    def scene0(self, p):
        im=self.base(0,self.cfg["title"],"先用一張圖，把每種結果攤開。")
        d=ImageDraw.Draw(im)
        # A gentle bob keeps the opening alive while all text remains fixed.
        shift=int(math.sin(p*math.pi*2)*5)
        first_die,second_die=self.matches[0]
        self.die(d,(177,302+shift),first_die,166,self.red)
        self.txt(d,(390,346),"+",70,self.muted,True,True)
        self.die(d,(475,302-shift),second_die,166,self.green)
        self.txt(d,(732,315),"總和",34,self.muted)
        opening_question=f"{self.target} 或 12？" if self.target!=12 else "12 最容易？"
        self.txt(d,(730,366),opening_question,70,self.ink,True)
        self.pill(d,(733,500,1147,546),"不是每個總和都一樣容易出現",self.red)
        return im

    def scene1(self,p):
        count=min(36,int(ease(p/.64)*36))
        key=(1,count)
        if key in self.frames:return self.frames[key].copy()
        im=self.base(1,"36 種組合，每格一樣可能","一列代表第一顆，一欄代表第二顆。")
        d=ImageDraw.Draw(im);self.grid(d,reveal=count)
        self.txt(d,(704,271),"每格都是一種結果",29,bold=True)
        self.txt(d,(700,344),f"{count:02d}",125,self.green,True,True)
        self.txt(d,(702,509),"6 × 6 = 36",40,bold=True,latin=True)
        self.frames[key]=im.copy();return im

    def scene2(self,p):
        count=min(len(self.matches),int(ease(p/.7)*len(self.matches)+.1))
        key=(2,count)
        if key in self.frames:return self.frames[key].copy()
        im=self.base(2,f"總和 {self.target}：有 {len(self.matches)} 種組合","亮色格子的兩顆骰子，加起來都相同。")
        d=ImageDraw.Draw(im);self.grid(d,self.matches[:count]);self.panel(d,count)
        self.frames[key]=im.copy();return im

    def scene3(self,p):
        im=self.base(3,"總和 12：只有 1 種組合","只有 6 + 6，會落在右下角這一格。")
        d=ImageDraw.Draw(im);self.grid(d,[(6,6)] if p>.13 else []);self.panel(d,1,color=self.green)
        return im

    def scene4(self,p):
        im=self.base(4,f"總和 {self.target} 的機率，是總和 12 的 {len(self.matches)} 倍","分母相同，直接比較有利組合的數量。")
        d=ImageDraw.Draw(im)
        factor=ease(p/.64)
        for i,(label,num,col) in enumerate([(f"總和 {self.target}",len(self.matches),self.red),("總和 12",1,self.green)]):
            y=298+i*145
            self.txt(d,(62,y+17),label,31,bold=True)
            d.rounded_rectangle((264,y,1004,y+78),18,fill="#E9EBE4")
            bw=max(2,int(740*num/6*factor))
            d.rounded_rectangle((264,y,264+bw,y+78),18,fill=col)
            self.txt(d,(1055,y+10),f"{num} 格",36,col,True)
        self.txt(d,(264,588),"每一格同樣可能，亮起幾格就是關鍵。",28,self.muted)
        return im

    def scene5(self,p):
        six=[(a,b) for a in range(1,7) for b in range(1,7) if a+b==6]
        count=min(5,int(ease(p/.60)*5+.1))
        key=(5,count)
        if key in self.frames:return self.frames[key].copy()
        im=self.base(5,"把目標改成 6，結果會跟著變","同一份程式，重新計算亮格，而不是手工塗色。")
        d=ImageDraw.Draw(im);self.grid(d,six[:count],color=self.green);self.panel(d,count,color=self.green)
        self.frames[key]=im.copy();return im

    def frame(self,t,transition=True):
        ix=next((i for i,(a,b) in enumerate(SCENE_TIMES) if a<=t<b),5)
        a,b=SCENE_TIMES[ix];p=(t-a)/(b-a)
        im=getattr(self,f"scene{ix}")(p)
        d=ImageDraw.Draw(im)
        d.rectangle((0,0,int(W*t/DURATION),4),fill=self.red)
        if transition:
            alpha=min(1,(t-a)/.3,(b-t)/.28)
            if alpha<1:
                im=Image.blend(Image.new("RGB",(W,H),self.bg),im,max(0,alpha))
        return im

    def export_frames(self,out):
        out.mkdir(parents=True,exist_ok=True)
        points={"opening":5,"grid-all":15,"grid-target":25,"sum-twelve":33,"comparison":42,"sum-six":53}
        for name,t in points.items():self.frame(t,False).save(out/f"{name}.png")
        sheet=Image.new("RGB",(1280,1080),self.bg)
        for n,name in enumerate(points):
            picture=Image.open(out/f"{name}.png").resize((640,360),Image.Resampling.LANCZOS)
            sheet.paste(picture,((n%2)*640,(n//2)*360))
        sheet.save(out/"contact-sheet.jpg",quality=93)

    def export_narration(self,output):
        """Export draft words/timings from the current config, without claiming audio sync."""
        names={1:'一',2:'二',3:'三',4:'四',5:'五',6:'六',7:'七',8:'八',9:'九',10:'十',11:'十一',12:'十二'}
        target,count=names[self.target],names[len(self.matches)]
        opening=f'總和{target}和十二一樣容易出現嗎？' if self.target!=12 else '總和十二容易出現嗎？'
        words=[
            '兩顆骰子的'+opening+'把結果排成表格，就看得出來。',
            '骰子公平、結果互不影響時，一共有三十六種同樣可能的組合。',
            f'總和{target}共有{count}種組合。沿著亮色格子逐一核對，機率就是三十六分之{count}。',
            '總和十二只有六加六。亮起一格，機率就是三十六分之一。',
            f'總和{target}和總和十二使用相同分母。有利組合是{count}格對一格，所以機率是{count}倍。',
            '最後固定練習總和六，就會亮起五格。每改一份資料，都要把相關文字和畫面一起核對。',
        ]
        def stamp(seconds):
            return f'{seconds//3600:02d}:{seconds//60%60:02d}:{seconds%60:02d},000'
        entries=[{'id':f'dice-{i+1}','start':a,'end':b,'text':words[i]} for i,(a,b) in enumerate(SCENE_TIMES)]
        output.with_suffix('.narration.txt').write_text('\n'.join(words)+'\n',encoding='utf-8')
        output.with_suffix('.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(a)} --> {stamp(b)}\n{words[i]}' for i,(a,b) in enumerate(SCENE_TIMES))+'\n',encoding='utf-8')
        output.with_suffix('.timeline.json').write_text(json.dumps({'locale':'zh-TW','target_sum':self.target,'timing':'planned scene windows; audio not generated or aligned','fixed_final_exercise_sum':6,'segments':entries},ensure_ascii=False,indent=2),encoding='utf-8')

    def render(self,path):
        command=["ffmpeg","-hide_banner","-loglevel","warning","-y","-f","rawvideo","-vcodec","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-an","-c:v","libx264","-preset","fast","-crf","20","-pix_fmt","yuv420p","-movflags","+faststart",str(path)]
        p=subprocess.Popen(command,stdin=subprocess.PIPE)
        try:
            for frame in range(DURATION*FPS):
                p.stdin.write(self.frame(frame/FPS).tobytes())
            p.stdin.close()
            if p.wait()!=0:raise RuntimeError("ffmpeg failed")
        except BaseException:
            p.kill();raise


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("lesson",nargs="?",type=pathlib.Path,default=ROOT/"lesson.json")
    parser.add_argument("--output",type=pathlib.Path,default=ROOT/"demo.mp4")
    parser.add_argument("--frames-dir",type=pathlib.Path,default=ROOT/"frames")
    parser.add_argument("--frames-only",action="store_true")
    parser.add_argument("--font",help="Traditional Chinese font file, e.g. NotoSansCJKtc-Regular.otf")
    parser.add_argument("--font-bold",help="Optional bold Traditional Chinese font file")
    parser.add_argument("--font-index",type=int,help="Font face index for a TTC collection; explicit OTF/TTF defaults to 0")
    parser.add_argument("--summary",action="store_true",help="Print a short human-readable result instead of JSON")
    args=parser.parse_args()
    try:
        configure_fonts(args)
    except (ValueError,OSError) as error:
        parser.error(str(error))
    # Independent checker is a precondition, and its output is kept in the run log.
    checked=subprocess.run([sys.executable,str(ROOT/"check_lesson.py"),str(args.lesson)],capture_output=args.summary,text=args.summary)
    if checked.returncode:
        if args.summary:
            print(checked.stdout.strip())
        raise SystemExit(checked.returncode)
    cfg=json.loads(args.lesson.read_text())
    renderer=Renderer(cfg)
    renderer.export_frames(args.frames_dir)
    renderer.export_narration(args.output)
    if not args.frames_only:renderer.render(args.output)
    if args.summary:
        print('OK: exported preview frames' if args.frames_only else f'OK: rendered {args.output.name}')
        print(f'{W}x{H} {FPS}fps duration={DURATION}s audio=none'+(' (planned; frames only)' if args.frames_only else ''))
        print(f'target_sum={cfg["target_sum"]} highlighted_count={len(renderer.matches)}')
    else:
        print(json.dumps({"output":str(args.output),"duration_seconds":DURATION,"fps":FPS,"width":W,"height":H,"target_sum":cfg["target_sum"],"highlight_count":len(renderer.matches),"audio":"none (intentional)"},ensure_ascii=False))


if __name__=="__main__":main()
