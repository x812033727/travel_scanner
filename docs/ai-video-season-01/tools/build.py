"""Build an editable, source-backed Chinese video season and local narrated review cuts.

No network requests, paid APIs, uploads, model tests or repository-wide edits.
Requires Python/Pillow, Windows System.Speech, ffmpeg and ffprobe.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import html
import json
import math
import re
import subprocess
import wave
from datetime import date, timedelta
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
FONT = Path('C:/Windows/Fonts/msjh.ttc')
BOLD = Path('C:/Windows/Fonts/msjhbd.ttc')
W, H = 1920, 1080
INK, MUTED, BG = '#F4F7FB', '#A6B2C8', '#101725'
KINDS = {'sourced_fact':'來源解說', 'fictional_example':'情境示意', 'editorial_guidance':'編輯分析／建議'}
SOURCES = {s['id']: s for s in json.loads((ROOT/'sources.json').read_text('utf-8'))['sources']}

def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')

def save_json(path, value):
    write(path, json.dumps(value, ensure_ascii=False, indent=2))

def run(args, **kwargs):
    return subprocess.run([str(a) for a in args], check=True, **kwargs)

def font(size, bold=False):
    return ImageFont.truetype(str(BOLD if bold else FONT), size)

def wrap(text, f, width):
    lines, current = [], ''
    for ch in text:
        if ch == '\n':
            lines.append(current); current = ''; continue
        if f.getlength(current + ch) > width and current and ch not in '，。！？；：、）』」':
            lines.append(current); current = ch
        else:
            current += ch
    if current: lines.append(current)
    return lines

def label(draw, text, xy, size=40, fill=INK, width=1600, bold=False, spacing=1.4):
    f = font(size, bold)
    lines = wrap(text, f, width)
    for i, line in enumerate(lines): draw.text((xy[0], xy[1]+i*size*spacing), line, font=f, fill=fill)
    return len(lines)*size*spacing

def chunks(text):
    # Clause-level synthesis makes subtitle timestamps correspond to actual audio,
    # rather than distributing estimated timings across an entire paragraph.
    parts = re.findall(r'[^，。！？；：、]+[，。！？；：、]?', text)
    out, buf = [], ''
    for part in parts:
        if len(buf + part) > 34 and buf:
            out.append(buf); buf = ''
        while len(part) > 40:
            out.append(part[:28]); part = part[28:]
        buf += part
        if buf.endswith(('。','！','？')):
            out.append(buf); buf = ''
    if buf: out.append(buf)
    return out

def stamp(seconds, ass=False):
    units = 100 if ass else 1000
    n = round(seconds * units)
    hours, n = divmod(n, 3600*units)
    minutes, n = divmod(n, 60*units)
    secs, sub = divmod(n, units)
    return f'{hours}:{minutes:02}:{secs:02}.{sub:02}' if ass else f'{hours:02}:{minutes:02}:{secs:02},{sub:03}'

def mmss(sec):
    return f'{int(sec)//60:02}:{int(sec)%60:02}'

def board(ep, scene, phase, dest, vertical=False):
    # Original code-native information graphics, separate from generated thumbnails.
    width, height = (1080,1920) if vertical else (W,H)
    im = Image.new('RGB',(width,height),BG); d = ImageDraw.Draw(im)
    accent = ep['accent']
    for y in range(height):
        blend = y/height
        d.line((0,y,width,y),fill=(16+int(blend*5),23+int(blend*8),37+int(blend*11)))
    margin = 72 if vertical else 100
    d.rounded_rectangle((margin,62,margin+116,106),radius=12,fill=accent)
    label(d,f"EP {ep['number']:02}",(margin+14,67),26,BG,bold=True)
    label(d,'AI 與真實世界',(margin+144,67),28,MUTED)
    label(d,KINDS[scene.get('kind','editorial_guidance')],(margin,135),28,accent)
    title_y = 204 if vertical else 200
    title_h = label(d,scene['heading'],(margin,title_y),64 if vertical else 72,width=width-margin*2,bold=True)
    cards = scene['cards']
    if vertical:
        for i,card in enumerate(cards):
            y=540+i*225
            d.rounded_rectangle((margin,y,width-margin,y+172),radius=25,fill='#243248',outline=accent if i==phase else '#37475C',width=4)
            label(d,f'0{i+1}',(margin+25,y+20),28,accent)
            label(d,card,(margin+100,y+40),44,width=width-margin*2-125,bold=True)
    else:
        cardw = (width-margin*2-64)//3
        for i,card in enumerate(cards):
            x=margin+i*(cardw+32); y=410
            selected=i==phase
            d.rounded_rectangle((x,y,x+cardw,y+240),radius=28,fill='#243248' if selected else '#182234',outline=accent if selected else '#344256',width=4 if selected else 2)
            label(d,f'0{i+1}',(x+30,y+24),32,accent if selected else MUTED)
            label(d,card,(x+30,y+97),42,width=cardw-60,bold=True,fill=INK if selected else MUTED)
            if i<2:
                cx=x+cardw+16
                d.line((cx-8,y+115,cx+8,y+115),fill=accent,width=3)
    refs=scene.get('refs',[])
    refline=' · '.join(f"{r} {SOURCES[r]['publisher'].split('/')[0].strip()}" for r in refs) or '原創概念示意／編輯建議；非實測紀錄'
    label(d,refline,(margin,height-(610 if vertical else 325)),24,MUTED,width=width-margin*2)
    label(d,'資料查核 2026-09-28 · 合成旁白 · 圖解審片版',(margin,height-63),23,MUTED,width=width-margin*2)
    im.save(dest)

def subtitle_files(units, dest, vertical=False):
    style_size = 54 if vertical else 48
    playx,playy=(1080,1920) if vertical else (1920,1080)
    ass=f'''[Script Info]
ScriptType: v4.00+
PlayResX: {playx}
PlayResY: {playy}
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Microsoft JhengHei,{style_size},&H00FFFFFF,&H000000FF,&H00201810,&H00201810,0,0,0,0,100,100,0,0,3,10,0,2,90,90,{300 if vertical else 108},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
    srt=[]
    for i,u in enumerate(units):
        text=u['text'].replace('{','').replace('}','')
        lines=wrap(text,font(style_size),playx-210)
        sub='\\N'.join(lines)
        ass+=f"Dialogue: 0,{stamp(u['start'],True)},{stamp(u['end'],True)},Default,,0,0,0,,{sub}\n"
        srt.append(f"{i+1}\n{stamp(u['start'])} --> {stamp(u['end'])}\n"+'\n'.join(lines)+'\n')
    write(dest/'captions.ass',ass); write(dest/'captions.srt','\n'.join(srt))

def prepare_units(ep, dest, rate):
    units=[]
    for si,scene in enumerate(ep['scenes']):
        for text in chunks(scene['narration']):
            digest=hashlib.sha256(f'HanhanDesktop|{rate}|{text}'.encode()).hexdigest()[:20]
            path=ROOT/'media'/'voice-cache'/f'{digest}.wav'
            path.parent.mkdir(parents=True,exist_ok=True)
            units.append({'scene':si,'text':text,'path':str(path.resolve())})
    save_json(dest/'speech-input.json',units)
    run(['powershell','-NoProfile','-ExecutionPolicy','Bypass','-File',ROOT/'tools'/'synthesize.ps1','-Manifest',dest/'speech-input.json','-Rate',rate])
    return units

def combine_audio(units,dest):
    time=0; params=None
    with wave.open(str(dest/'narration.wav'),'wb') as output:
        for u in units:
            with wave.open(u['path'],'rb') as source:
                current=source.getparams()
                if params is None:
                    params=current; output.setparams(current)
                assert current[:3]==params[:3], 'Inconsistent voice format'
                data=source.readframes(source.getnframes())
                duration=source.getnframes()/source.getframerate()
            u['start']=time
            output.writeframes(data)
            pause=0.08
            output.writeframes(b'\0'*round(pause*params.framerate)*params.sampwidth*params.nchannels)
            time+=duration+pause
            u['end']=time
    return time

def render_video(ep, dest, units, duration, vertical=False):
    subtitle_files(units,dest,vertical)
    scene_times=[]; concat=[]
    for si,scene in enumerate(ep['scenes']):
        relevant=[u for u in units if u['scene']==si]
        start,end=relevant[0]['start'],relevant[-1]['end']
        scene_times.append({'heading':scene['heading'],'start':start,'end':end})
        for phase in range(3):
            name=f'scene-{si+1:02}-{phase}.png'
            board(ep,scene,phase,dest/name,vertical)
            concat += [f"file '{name}'",f'duration {(end-start)/3:.6f}']
    concat.append(f"file '{name}'")
    write(dest/'frames.txt','\n'.join(concat)+'\n')
    vf="fps=24,subtitles=captions.ass"
    output='review.mp4'
    with (dest/'ffmpeg.log').open('w',encoding='utf-8') as log:
        run(['ffmpeg','-y','-hide_banner','-loglevel','warning','-f','concat','-safe','1','-i','frames.txt','-i','narration.wav','-vf',vf,'-af','loudnorm=I=-16:TP=-1.5:LRA=11','-c:v','libx264','-preset','ultrafast','-crf','23','-threads','4','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-t',f'{duration:.6f}','-movflags','+faststart',output],cwd=dest,stdout=log,stderr=log)
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(dest/output)],encoding='utf-8'))
    save_json(dest/'probe.json',probe)
    save_json(dest/'timing.json',{'duration':duration,'scenes':scene_times,'units':[{k:v for k,v in u.items() if k!='path'} for u in units]})
    return scene_times,probe

def docs(ep,dest,timing=None):
    md=f"# {ep['title_a']}\n\n編號：{ep['id']}｜形式：中文資料型解說｜無真人出鏡｜非實測\n\n"
    md+='## 完整旁白與分鏡\n\n'
    for i,s in enumerate(ep['scenes']):
        ts=f"{mmss(timing[i]['start'])} " if timing else ''
        md+=f"### {ts}{i+1:02}｜{s['heading']}\n\n**畫面：** {s['visual']}\n\n**性質：** {KINDS[s['kind']]}。**來源：** {', '.join(s['refs']) or '原創示意或編輯建議，無外部事實主張'}。\n\n{s['narration']}\n\n"
    md+='## 資料與界線\n\n'
    for rid in ep['sources']:
        r=SOURCES[rid]; md+=f"- {rid} [{r['title']}]({r['url']}) — {r['publisher']}，{r['date'] or '持續更新頁面'}。限制：{r['limits']}\n"
    write(dest/'script-storyboard.md',md)
    write(dest/'narration.txt','\n\n'.join(s['narration'] for s in ep['scenes']))
    shorts='# 兩支衍生 Shorts\n\n'
    for i,s in enumerate(ep['shorts']):
        shorts+=f"## {i+1}. {s['title']}\n\n{s['text']}\n\n畫面重點：{' → '.join(s['cards'])}\n\n來源：{', '.join(s['refs']) or '原創示意／編輯建議'}\n\n"
    write(dest/'shorts.md',shorts.rstrip()+'\n')
    description=ep['description']+'\n\n本片使用合成旁白與原創示意圖解；非現場紀錄、非產品實測。資料查核日：2026-09-28。\n\n'
    if timing:
        description+='章節\n'+'\n'.join(f"{mmss(s['start'])} {s['heading']}" for s in timing)+'\n\n'
    description+='資料來源\n'+'\n'.join(f"{rid}｜{SOURCES[rid]['title']}\n{SOURCES[rid]['url']}" for rid in ep['sources'])
    write(dest/'youtube-description.txt',description)
    save_json(dest/'upload-draft.json',{'status':'local_draft_not_uploaded','title_a':ep['title_a'],'title_b':ep['title_b'],'description':description,'pinned_comment':ep['pinned_comment'],'language':'zh-TW','audience':'general_audience_not_made_for_kids','privacy':'private_if_uploaded','ai_disclosure':'Disclose realistic generated illustration when used; re-check current Studio requirements','thumbnail_a':f"../../assets/{ep['number']:02}-thumbnail-a.png",'thumbnail_b':f"../../assets/{ep['number']:02}-thumbnail-b.png",'publication_requires':'Final audiovisual review and explicit channel/upload destination; no public upload performed'})

def gallery(episodes):
    cards=[]
    for ep in episodes:
        path=f"media/{ep['id']}"
        timingfile=ROOT/path/'timing.json'
        duration=json.loads(timingfile.read_text('utf-8'))['duration'] if timingfile.exists() else None
        dur=mmss(duration) if duration else '尚未輸出'
        cards.append(f'''<article id="{ep['id']}"><div class="eyebrow">EP {ep['number']:02} / {html.escape(ep['theme'])} / {dur}</div>
<h2>{html.escape(ep['title_a'])}</h2>
<div class="thumbs"><figure><img src="assets/{ep['number']:02}-thumbnail-a.png" alt="縮圖 A"><figcaption>A｜{html.escape(ep['title_a'])}</figcaption></figure><figure><img src="assets/{ep['number']:02}-thumbnail-b.png" alt="縮圖 B"><figcaption>B｜{html.escape(ep['title_b'])}</figcaption></figure></div>
<video controls preload="none" poster="assets/{ep['number']:02}-thumbnail-a.png" src="{path}/review.mp4"></video>
<p>{html.escape(ep['description'])}</p><nav><a href="{path}/script-storyboard.md">旁白與分鏡</a><a href="{path}/captions.srt">字幕</a><a href="{path}/youtube-description.txt">發布文案</a><a href="{path}/shorts.md">Shorts 腳本</a><a href="{path}/short-1/review.mp4">Short 1</a><a href="{path}/short-2/review.mp4">Short 2</a></nav></article>''')
    page='''<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>AI 與真實世界｜第一季審片室</title><style>
*{box-sizing:border-box}body{background:#101725;color:#eef3fa;font:17px/1.7 system-ui,"Microsoft JhengHei",sans-serif;margin:0}main{max-width:1160px;margin:auto;padding:64px 24px}header{border-bottom:1px solid #354053;padding-bottom:36px}.eyebrow{color:#71dbed;font-size:14px;letter-spacing:.09em}h1{font-size:clamp(36px,6vw,64px);line-height:1.2;max-width:900px;margin:20px 0}h2{font-size:30px;line-height:1.4}p{color:#bac7d9}.badge{display:inline-block;border:1px solid #647188;border-radius:20px;padding:4px 14px;font-size:13px;margin-right:10px}article{padding:44px 0;border-bottom:1px solid #354053}.thumbs{display:grid;grid-template-columns:1fr 1fr;gap:20px}figure{margin:0}img{width:100%;border-radius:14px}figcaption{font-size:13px;color:#afbed1;margin:8px 0 20px}video{width:100%;max-height:630px;background:#080c13;border-radius:12px}a{color:#77deef;text-underline-offset:5px}nav{display:flex;gap:22px;flex-wrap:wrap;margin:18px 0}aside{padding:20px;background:#1c293b;border-radius:12px;margin:26px 0} @media(max-width:650px){.thumbs{grid-template-columns:1fr}h2{font-size:24px}main{padding:30px 18px}}
</style><main><aside>Git checkout 不含 MP4 / WAV / ZIP；播放與下載需先重建或還原本機交付包。腳本、縮圖與歷史驗證紀錄已收錄。</aside><header><div class="eyebrow">AI & THE REAL WORLD / SEASON 01</div><h1>把 AI 的大問題，<br>講回真實世界。</h1><p>六支中文資料型解說。完整旁白、來源界線、原創縮圖與可播放圖解審片版。</p><span class="badge">本機檔案</span><span class="badge">未上傳 YouTube</span><span class="badge">資料查核 2026-09-28</span></header>
<aside>目前影片為 Windows 中文合成旁白＋原創圖解的審片版。腳本已完成，不代表已通過人耳配音審查、最終節奏剪輯或發布驗收；百萬觀看是目標，不是已取得的結果。縮圖與影片內的圖解為不同素材。</aside><nav><a href="README.md">交付說明</a><a href="sources.json">來源登錄</a><a href="operations.md">90 天操作表</a><a href="analytics.csv">成效紀錄</a><a href="validation.json">驗證結果</a></nav>'''+''.join(cards)+'</main></html>'
    page=page.replace('<nav><a href="README.md">','<nav><a href="review-videos.zip">18 支審片影片打包</a><a href="scripts-and-thumbnails.zip">腳本與縮圖打包</a><a href="README.md">')
    write(ROOT/'index.html',page)

def validate(episodes):
    report={'checked_on':'2026-09-28','status':'technical_checks_only','not_verified':['Human listening/pronunciation review','Audience retention','YouTube account/upload','Final cinematic edit','One million views'],'episodes':[]}
    for ep in episodes:
        assert len(ep['scenes'])==10 and len(ep['shorts'])==2
        assert len(ep['sources'])>=3
        for scene in ep['scenes']:
            assert len(scene['cards'])==3 and scene['kind'] in KINDS
            assert all(r in SOURCES for r in scene['refs'])
            assert not any(x in scene['narration'] for x in ['TODO','待補','填入此處'])
        dest=ROOT/'media'/ep['id']; timing=json.loads((dest/'timing.json').read_text('utf-8')) if (dest/'timing.json').exists() else None
        item={'id':ep['id'],'script_characters':sum(len(s['narration']) for s in ep['scenes']),'long_video_exists':(dest/'review.mp4').exists(),'duration_seconds':timing['duration'] if timing else None,'duration_8_to_12_minutes':bool(timing and 480<=timing['duration']<=720),'thumbnails':[{'variant':v,'exists':(ROOT/'assets'/f"{ep['number']:02}-thumbnail-{v}.png").exists()} for v in ['a','b']]}
        if timing:
            assert ''.join(u['text'] for u in timing['units'])==''.join(s['narration'] for s in ep['scenes']), 'Audio transcript no longer matches source script'
            assert 480<=timing['duration']<=720, 'Long video outside the agreed 8-12 minute range'
            assert timing['units'][0]['start']==0
            for a,b in zip(timing['units'],timing['units'][1:]): assert abs(a['end']-b['start'])<0.001
            probe=json.loads((dest/'probe.json').read_text('utf-8'))
            assert any(s['codec_type']=='audio' for s in probe['streams'])
            video=next(s for s in probe['streams'] if s['codec_type']=='video')
            assert (video['width'],video['height'])==(1920,1080)
            assert abs(float(probe['format']['duration'])-timing['duration'])<0.3
            item['subtitle_units']=len(timing['units'])
            item['shorts']=[{'exists':(dest/f'short-{i}'/'review.mp4').exists(),'duration':json.loads((dest/f'short-{i}'/'timing.json').read_text('utf-8'))['duration'] if (dest/f'short-{i}'/'timing.json').exists() else None} for i in [1,2]]
            for i,short in enumerate(ep['shorts'],1):
                sp=dest/f'short-{i}'
                st=json.loads((sp/'timing.json').read_text('utf-8'))
                assert ''.join(u['text'] for u in st['units'])==short['text']
                assert 15<=st['duration']<=60
                spr=json.loads((sp/'probe.json').read_text('utf-8'))
                sv=next(s for s in spr['streams'] if s['codec_type']=='video')
                assert (sv['width'],sv['height'])==(1080,1920)
                assert any(s['codec_type']=='audio' for s in spr['streams'])
                assert abs(float(spr['format']['duration'])-st['duration'])<0.3
        for variant in ['a','b']:
            imagepath=ROOT/'assets'/f"{ep['number']:02}-thumbnail-{variant}.png"
            with Image.open(imagepath) as img:
                assert img.width>=1280 and abs(img.width/img.height-16/9)<0.01
        assert item['long_video_exists'], 'Long video missing'
        report['episodes'].append(item)
    save_json(ROOT/'validation.json',report)
    print(json.dumps(report,ensure_ascii=False,indent=2))

def main():
    p=argparse.ArgumentParser(); p.add_argument('--episode'); p.add_argument('--rate',type=int,default=0); p.add_argument('--docs-only',action='store_true'); p.add_argument('--shorts-only',action='store_true'); p.add_argument('--validate',action='store_true'); args=p.parse_args()
    episodes=[json.loads(f.read_text('utf-8')) for f in sorted((ROOT/'episodes').glob('*.json'))]
    if args.validate: validate(episodes); gallery(episodes); return
    for ep in episodes:
        if args.episode and not ep['id'].startswith(tuple(args.episode.split(','))): continue
        dest=ROOT/'media'/ep['id']; dest.mkdir(parents=True,exist_ok=True)
        existing_timing=dest/'timing.json'
        docs(ep,dest,json.loads(existing_timing.read_text('utf-8'))['scenes'] if existing_timing.exists() else None)
        if args.docs_only: continue
        if not args.shorts_only:
            units=prepare_units(ep,dest,args.rate)
            duration=combine_audio(units,dest)
            print(f"{ep['id']} narration {duration:.1f}s",flush=True)
            timing,probe=render_video(ep,dest,units,duration)
            docs(ep,dest,timing)
        for i,short in enumerate(ep['shorts'],1):
            sd=dest/f'short-{i}'; sd.mkdir(exist_ok=True)
            shortep={**ep,'scenes':[{'heading':short['title'],'narration':short['text'],'cards':short['cards'],'refs':short['refs'],'kind':'sourced_fact' if short['refs'] else 'editorial_guidance'}]}
            sunits=prepare_units(shortep,sd,args.rate); st=combine_audio(sunits,sd)
            render_video(shortep,sd,sunits,st,True)
            print(f"{ep['id']} short {i}: {st:.1f}s",flush=True)
        if not args.shorts_only:
            save_json(dest/'render-receipt.json',{'voice':'Microsoft Hanhan Desktop / Windows System.Speech','voice_rate':args.rate,'status':'local_narrated_graphic_review_cut','duration_seconds':duration,'not_a_final_edit':True,'uploaded':False})
    gallery(episodes)

if __name__=='__main__': main()
