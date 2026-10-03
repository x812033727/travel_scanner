import json,re,sys
p='/home/user/travel_scanner/docs/ai-terms-series/batch-02/staging/ai-term-chain-of-thought/pack.json'
d=json.load(open(p))
z=d['locales']['zh-TW']
tot=0
per=[]
for i,b in enumerate(z['blocks']):
    t=b['type']; parts=[]
    if t=='paragraph': parts=[b['text']]
    elif t=='rich_paragraph': parts=[''.join(n['text'] for n in b['inlines'])]
    elif t=='list': parts=b['items']
    elif t=='table':
        parts=list(b['header'])
        for r in b['rows']: parts+=r
    elif t=='callout': parts=[b['title'],b['text']]
    n=sum(len(re.sub(r'\s+','',x)) for x in parts)
    # link text excluded by the brief
    if t=='rich_paragraph':
        link=sum(len(re.sub(r'\s+','',n_['text'])) for n_ in b['inlines'] if n_['type']!='text')
        per.append((i,t,n,n-link))
        tot_ex=n-link
        tot+=n   # tool's count includes link text
    else:
        per.append((i,t,n,n)); tot+=n
    
print('tool-style total (includes link text):',tot)
ex=sum(p_[3] for p_ in per)
print('excluding link text:',ex)
for x in per:
    if x[2]: print(x)
print('title',len(z['title']),'desc',len(z['description']))
