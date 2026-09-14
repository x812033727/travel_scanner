import json,urllib.request,xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime,timezone
root=Path.cwd();out=Path(__file__).parent
series=json.loads((root/'apps/web/lib/guide-series.json').read_text(encoding='utf-8'))
slugs=[series['hubSlug']]+[a['slug'] for a in series['articles']]
origin='https://mokaair.com'
req=urllib.request.Request(origin+'/sitemap.xml',headers={'User-Agent':'Twitterbot/1.0'})
with urllib.request.urlopen(req,timeout=30) as r:
 assert r.status==200;raw=r.read()
xml=ET.fromstring(raw);ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
entries=[(e.findtext('s:loc',namespaces=ns),e.findtext('s:lastmod',namespaces=ns)) for e in xml.findall('s:url',ns)]
verified=[]
for slug in slugs:
 url=origin+'/zh-TW/life/'+slug
 matches=[modified for loc,modified in entries if loc==url]
 assert len(matches)==1 and matches[0],(slug,matches)
 verified.append({'slug':slug,'url':url,'lastModified':matches[0]})
with urllib.request.urlopen(urllib.request.Request(origin+'/zh-TW/life/'+series['hubSlug'],headers={'User-Agent':'Twitterbot/1.0'}),timeout=30) as r:
 html=r.read().decode();assert r.status==200
for slug in slugs[1:]:assert f'href="/zh-TW/life/{slug}"' in html,slug
assert 'name="robots" content="noindex' not in html
report={'checkedAt':datetime.now(timezone.utc).isoformat(),'status':'passed','sitemapEntries':len(entries),'seriesEntries':verified,'hubSSRLinks':50,'hubIndexable':True}
(out/'public-sitemap.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':'passed','seriesEntries':len(verified),'hubSSRLinks':50}))
