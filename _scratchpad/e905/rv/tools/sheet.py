import subprocess,sys,io
from PIL import Image,ImageDraw
# usage: sheet.py out.jpg width clip t1 t2 ... [clip2 t..]  (clip args end with .mp4)
out=sys.argv[1]; W=int(sys.argv[2]); items=[];clip=None
for a in sys.argv[3:]:
    if a.endswith('.mp4'): clip=a
    else: items.append((clip,float(a)))
tiles=[]
for c,t in items:
    b=subprocess.run(['ffmpeg','-v','error','-ss',str(t),'-i',c,'-frames:v','1','-vf',f'scale={W}:-2','-f','image2','-c:v','png','-'],capture_output=True).stdout
    im=Image.open(io.BytesIO(b)).convert('RGB'); d=ImageDraw.Draw(im); d.rectangle([0,0,200,16],fill='black'); d.text((3,2),c.split('/')[-1][:-4]+f' @{t}',fill='yellow'); tiles.append(im)
cols=min(len(tiles), max(1,1920//W)); rows=(len(tiles)+cols-1)//cols; h=tiles[0].height
S=Image.new('RGB',(cols*W,rows*h),'white')
for k,im in enumerate(tiles): S.paste(im,((k%cols)*W,(k//cols)*h))
S.save(out,quality=88)
