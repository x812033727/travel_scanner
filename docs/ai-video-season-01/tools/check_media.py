"""Verify every exported file decodes a frame and has non-silent audio."""
import json
import math
import re
import subprocess
from pathlib import Path
from PIL import Image,ImageOps,ImageDraw,ImageFont

root=Path(__file__).resolve().parents[1]
records=[]
frames=[]
for file in sorted((root/'media').rglob('review.mp4')):
    timing=json.loads((file.parent/'timing.json').read_text('utf-8'))
    frame=file.parent/'qa-decoded-frame.jpg'
    subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-threads','2','-ss',str(timing['duration']/2),'-i',str(file),'-frames:v','1',str(frame)],check=True)
    result=subprocess.run(['ffmpeg','-hide_banner','-threads','2','-i',str(file),'-vn','-af','volumedetect','-f','null','NUL'],capture_output=True,text=True,encoding='utf-8',errors='replace',check=True)
    match=re.search(r'max_volume:\s*(-?\d+(?:\.\d+)?) dB',result.stderr)
    assert match and float(match.group(1))>-50, f'Silent or unreadable audio: {file}'
    records.append({'file':file.relative_to(root).as_posix(),'decoded_frame':frame.relative_to(root).as_posix(),'audio_max_db':float(match.group(1)),'frame_decode':'passed'})
    if not file.parent.name.startswith('short-'): frames.append(frame)
assert len(records)==18
page=Image.new('RGB',(1440,math.ceil(len(frames)/2)*455),'#101725'); d=ImageDraw.Draw(page)
font=ImageFont.truetype('C:/Windows/Fonts/msjh.ttc',22)
for i,file in enumerate(frames):
    x,y=(i%2)*720,(i//2)*455
    page.paste(ImageOps.contain(Image.open(file),(704,396)),(x,y))
    d.text((x+10,y+407),file.parent.name,font=font,fill='white')
page.save(root/'assets'/'qa-long-video-frames.jpg')
(root/'media-checks.json').write_text(json.dumps({'status':'passed','checks':records,'limitations':'Frame decode and non-silent audio are technical checks, not a human listening review.'},ensure_ascii=False,indent=2),encoding='utf-8')
print(f'Passed frame decode and audio checks for {len(records)} videos.')
