"""Reserve exact batch paths before authoring content or assets."""
import datetime,json,urllib.request,urllib.parse
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
items=json.loads((HERE/'manifest.json').read_text(encoding='utf8'))
slugs=[i['slug'] for i in items]+['ai-news-2026-january-september-index']
assert len(slugs)==len(set(slugs))==22
for slug in slugs:
    assert not (ROOT/'apps/api/app/guides/content'/f'{slug}.json').exists()
    assert not (ROOT/'apps/web/public/guides'/slug).exists()
articles=[]
cursor=None
while True:
    query={'locale':'zh-TW','kind':'life','limit':50}
    if cursor:query['cursor']=cursor
    with urllib.request.urlopen('https://mokaair.com/api/travel/guides?'+urllib.parse.urlencode(query)) as r:
        data=json.load(r)
    articles.extend({'slug':a['slug'],'title':a['title']} for a in data['articles'])
    cursor=data.get('next_cursor')
    if not cursor:break
assert not set(slugs)&{a['slug'] for a in articles}
(HERE/'live-baseline.json').write_text(json.dumps({'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'articles':articles,'next_cursor':None},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
task=ROOT/'tasks/open/2026-09-14-ai-news-2026-year-to-date.md'
text=task.read_text(encoding='utf8')
extra=''.join(f'  - apps/api/app/guides/content/{s}.json\n  - apps/web/public/guides/{s}\n' for s in slugs)
text=text.replace('  - docs/ai-news-2026-ytd\n','  - docs/ai-news-2026-ytd\n'+extra)
task.write_text(text,encoding='utf8')
(HERE/'slugs.json').write_text(json.dumps(slugs,indent=2)+'\n',encoding='utf8')
print(f'Reserved {len(slugs)} unique paths; inspected {len(articles)} live life articles')
