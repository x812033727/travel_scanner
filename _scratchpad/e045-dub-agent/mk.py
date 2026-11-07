# usage: mk.py <locale> <tsv file>: lines "id<TAB>text[<TAB>say[<TAB>emotion]]"
import json,sys
R='/home/user/travel_scanner/docs/videos/zhong-tian-qu-qi-e045/'
loc,src=sys.argv[1],sys.argv[2]
v=json.load(open(R+'video.json'))
L={l['id']:l for s in v['scenes'] for l in s['lines']}
out={}
for row in open(src,encoding='utf8'):
    row=row.rstrip('\n')
    if not row.strip(): continue
    p=row.split('\t')
    i=p[0]; e={'text':p[1],'emotion':L[i]['emotion']}
    if len(p)>3 and p[3]: e['emotion']=p[3]
    if len(p)>2 and p[2] and p[2]!=p[1]: e['say']=p[2]
    out[i]=e
missing=[i for i in L if i not in out]
assert not missing, missing
out={i:out[i] for i in L}
open(R+f'dub.{loc}.json','w',encoding='utf8').write(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print('wrote e045',loc,len(out))
