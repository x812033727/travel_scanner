"""Contact sheets from normal, signed-out public browser captures."""
import json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent
items=json.loads((HERE/'manifest.json').read_text(encoding='utf8'))
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)
for locale in ['zh-TW','en','ja','ko','zh-CN']:
    for mode in ['desktop','mobile','table']:
        for start in range(0,len(items),5):
            frames=[]
            for item in items[start:start+5]:
                view='mobile' if mode=='table' else mode;suffix='table-clean' if mode=='table' else 'top'
                frame=Image.open(HERE/'browser'/f"{view}-{locale}-{item['slug']}-{suffix}.png").convert('RGB')
                if mode=='desktop':frame=frame.crop((280,88,1085,900))
                frame.thumbnail((320,1800 if mode=='table' else 700),Image.Resampling.LANCZOS);frames.append(frame)
            sheet=Image.new('RGB',(1672,max(f.height for f in frames)+54),'#e6e6e6');draw=ImageDraw.Draw(sheet)
            for i,frame in enumerate(frames):
                draw.text((12+i*332,10),f'{start+i+1:02d} | {locale} | {mode}',fill='#222',font=font);sheet.paste(frame,(12+i*332,38))
            sheet.save(HERE/f'public-{mode}-{locale}-{start//5+1}.jpg',quality=90,optimize=True)
print('Saved public layout and table review sheets')
