"""Prepare owned series metadata and immutable source snapshots; never publish."""
import argparse
import hashlib
import html
import importlib.util
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path
import tempfile
ROOT=Path(__file__).resolve().parents[3]
PLAN=ROOT/'docs/claude-code-series/advanced/curriculum.json'
EVIDENCE=ROOT/'docs/claude-code-series/advanced/evidence'
def write(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--sources',action='store_true');args=parser.parse_args()
    plan=json.loads(PLAN.read_text(encoding='utf-8'))
    manifest_path=ROOT/'apps/api/app/guides/series_data/claude-code.json'
    manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
    manifest['entries']=[e for e in manifest['entries'] if e['number']<=60]
    manifest['groups']=[g for g in manifest['groups'] if g['id']<'K']
    manifest['paths']=[p for p in manifest['paths'] if not p['id'].startswith('advanced-')]
    urls={s['id']:s['url'] for s in plan['sources']}
    for entry in plan['entries']:
        fields=['slug','title','outcome','number','group','level','platforms','aliases','prerequisites','related']
        lesson={key:entry[key] for key in fields}
        lesson['sources']=[urls[key] for key in entry['source_ids']]
        if entry['group']=='N':
            lesson['sources']+=['https://modelcontextprotocol.io/docs/develop/build-server','https://github.com/modelcontextprotocol/typescript-sdk']
        if entry['number']==94:
            lesson['sources']+=['https://code.claude.com/docs/en/agent-sdk/sessions']
        if entry['number']==72:
            lesson['sources']+=['https://code.claude.com/docs/en/plugins-reference']
        manifest['entries'].append(lesson)
    manifest['groups'] += [{'id':g['id'],'title':g['title']} for g in plan['groups']]
    slugs={e['number']:e['slug'] for e in manifest['entries']}
    manifest['paths'] += [{'id':p['id'],'title':p['title'],'slugs':[slugs[n] for n in p['numbers']]} for p in plan['paths']]
    write(manifest_path,manifest)
    source_path=ROOT/'docs/claude-code-series/source-checks.json'
    if args.sources:
        import httpx
        cache=Path(tempfile.gettempdir())/'mokaair-claude-advanced-sources';cache.mkdir(exist_ok=True)
        def fetch(url):
            fetch_url=url+'.md' if url.startswith('https://code.claude.com/') else url
            response=httpx.get(fetch_url,follow_redirects=True,timeout=45)
            body=response.text
            filename=hashlib.sha256(url.encode()).hexdigest()[:16]+'.txt'
            (cache/filename).write_text(body,encoding='utf-8')
            title=next((line.lstrip('# ') for line in body.splitlines() if line.startswith('# ')),'')
            if not title:
                m=re.search(r'<title[^>]*>(.*?)</title>',body,re.S)
                title=html.unescape(m.group(1).strip()) if m else ''
            return {'url':url,'fetched_url':str(response.url),'status':response.status_code,'checked_on':date.today().isoformat(),'title':title,'sha256':hashlib.sha256(response.content).hexdigest(),'bytes':len(response.content),'verification':'official-documentation','product_operation_tested':False,'cache_file':filename}
        all_urls=sorted({u for e in manifest['entries'] if e['number']>=61 for u in e['sources']})
        with ThreadPoolExecutor(max_workers=5) as pool: checks=list(pool.map(fetch,all_urls))
        write(EVIDENCE/'source-checks.json',checks)
        failures=[c for c in checks if c['status']!=200 or not c['title']]
        if failures: print(json.dumps(failures,ensure_ascii=False));return 1
        prior={c['url']:c for c in json.loads(source_path.read_text(encoding='utf-8'))}
        prior.update({c['url']:{k:v for k,v in c.items() if k!='cache_file'} for c in checks})
        write(source_path,list(prior.values()))
        print(json.dumps({'sources':len(checks),'cache':str(cache)}))
    print(json.dumps({'entries':len(manifest['entries']),'groups':len(manifest['groups']),'paths':len(manifest['paths'])}))
    return 0
if __name__=='__main__':sys.exit(main())
