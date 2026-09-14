"""Read-only content checks plus import/public-read checks in disposable SQLite memory.

Run with apps/api/.venv/Scripts/python.exe docs/article-batch-5/verify_batch.py.
Never connects to configured production databases; no credentials required.
"""
from pathlib import Path
import asyncio
from collections import Counter
import hashlib
import json
import re
import sys
from urllib.parse import urlparse
from uuid import uuid4
import xml.etree.ElementTree as ET
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path[:0] = [str(ROOT / 'apps/api'), str(ROOT / 'apps/api/tests')]
from app.guides.content_pack import load_packs, plan_import, apply_import
from app.guides.models import GuideTopic
from app.guides.taxonomy import SEED_TOPICS, LIFE_SEED_TOPICS, seed_names
from app.db import Base
from app.models import User
from sqlalchemy import event
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from test_guides import TABLES, make_app, client

rows = json.loads((HERE / 'manifest.json').read_text(encoding='utf-8'))
slugs = {row['slug'] for row in rows}
assert len(rows) == len(slugs) == 30
live=json.loads((HERE/'live-baseline.json').read_text(encoding='utf-8'))
assert len(set(live['life_slugs']))==40
assert not slugs.intersection(live['life_slugs'])
packs = load_packs()
by_slug = {p.slug:p for p in packs}
new = [by_slug[r['slug']] for r in rows]
old = [p for p in packs if p.slug not in slugs]
assert Counter(p.kind for p in new) == {'howto':15, 'life':15}

def body(doc):
    values=[]
    for b in doc.model_dump(mode='json')['blocks']:
        if b['type'] in {'image','link','offer'}: continue
        for key in ['text','title','caption']:
            if b.get(key): values.append(b[key])
        values += b.get('items', []) + b.get('header', [])
        values += [cell for row in b.get('rows', []) for cell in row]
    return ''.join(values)

def normalized(s): return re.sub(r'[^a-z0-9\u3400-\u9fff]', '', s.casefold())
def shingles(s):
    s=normalized(s)
    return {s[i:i+5] for i in range(len(s)-4)}

all_docs={p.slug:p.locales.get('zh-TW', next(iter(p.locales.values()))) for p in packs}
titles=[normalized(doc.title) for doc in all_docs.values()]
assert len(titles)==len(set(titles)), 'Duplicate normalized title'
bodies={slug:normalized(body(doc)) for slug,doc in all_docs.items()}
assert len(set(bodies.values()))==len(bodies), 'Duplicate full article'
grams={slug:shingles(text) for slug,text in bodies.items()}
checks=[]
images=[]
for pack in new:
    doc=pack.locales['zh-TW']
    raw=doc.model_dump(mode='json')
    text=body(doc)
    assert len(text) >= (1800 if pack.kind=='howto' else 900), (pack.slug, len(text))
    assert len(text)<=3200
    assert sum(b['type']=='heading' and b['level']==2 for b in raw['blocks'])>=3
    assert any(b['type']=='table' for b in raw['blocks'])
    assert any(b['type']=='callout' for b in raw['blocks'])
    assert doc.sources and all(str(s.checked_on)=='2026-09-14' for s in doc.sources)
    hero=ROOT/'apps/web/public'/doc.hero.src.lstrip('/')
    assert hero.stat().st_size<=200_000
    with Image.open(hero) as img: assert img.size==(1600,900)
    images.append(hashlib.sha256(hero.read_bytes()).hexdigest())
    assert 'AI 生成' in doc.hero.credit.license
    assert '非實拍' in doc.hero.alt
    for block in raw['blocks']:
        if block['type']=='image':
            path=ROOT/'apps/web/public'/block['src'].lstrip('/')
            assert path.is_file()
            svg=ET.parse(path).getroot()
            assert svg.attrib['viewBox']=='0 0 1600 900'
            for el in svg.iter():
                if 'font-size' in el.attrib: assert float(el.attrib['font-size'])>=15
        if block['type']=='link' and urlparse(block['url']).netloc=='mokaair.com':
            bits=urlparse(block['url']).path.strip('/').split('/')
            if len(bits)==4 and bits[1]=='guides' or len(bits)==3 and bits[1]=='life':
                target=by_slug.get(bits[-1])
                assert target, (pack.slug,'missing internal target',bits[-1])
                assert (bits[-2]=='life' and target.kind=='life') or bits[-2]==target.kind
            else:
                route='/'.join(bits[1:])
                allowed={'guides','guides/howto','foods','destinations/tokyo','destinations/singapore','destinations/chiang-mai','destinations/hanoi'}
                assert route in allowed, (pack.slug,route)
    nearest=[]
    for other in packs:
        if other.slug==pack.slug: continue
        a,b=grams[pack.slug],grams[other.slug]
        score=len(a&b)/len(a|b)
        nearest.append((score,other.slug))
    score,nearest_slug=max(nearest)
    assert score<0.16,(pack.slug,nearest_slug,score)
    checks.append({'slug':pack.slug,'kind':pack.kind,'title':doc.title,'body_characters':len(text),
        'hero_bytes':hero.stat().st_size,'nearest_article':nearest_slug,'five_character_jaccard':round(score,4)})
assert len(set(images))==30, 'Repeated hero image'

async def verify_import():
    engine=create_async_engine('sqlite+aiosqlite:///:memory:')
    @event.listens_for(engine.sync_engine,'connect')
    def foreign_keys(connection,_): connection.execute('PRAGMA foreign_keys=ON')
    try:
        async with engine.begin() as conn:
            await conn.run_sync(lambda c:Base.metadata.create_all(c,tables=TABLES))
        factory=async_sessionmaker(engine,expire_on_commit=False)
        actor=User(id=uuid4(),email='editorial-qa@example.com',password_hash='local-test-only',is_admin=True,is_active=True)
        async with factory() as session:
            for section,topics in [('travel',SEED_TOPICS),('life',LIFE_SEED_TOPICS)]:
                for order,(slug,labels) in enumerate(topics):
                    session.add(GuideTopic(slug=slug,names_json=seed_names(labels),display_order=order*10,section=section,source='seed'))
            session.add(actor)
            await session.commit()
            plan=await plan_import(session,new)
            first=await apply_import(session,actor,plan,publish=True)
            assert first.failed is None,first.failed
            assert len(first.created)==len(first.published)==30
            again=await apply_import(session,actor,await plan_import(session,new),publish=True)
            assert again.failed is None and len(again.unchanged)==30
            assert not again.created and not again.published and not again.updated
        async with client(make_app(factory)) as api:
            for pack in new:
                response=await api.get(f'/guides/{pack.kind}/{pack.slug}',params={'locale':'zh-TW'})
                assert response.status_code==200,(pack.slug,response.status_code,response.text[:300])
                assert pack.locales['zh-TW'].title in response.text
        return {'database':'disposable SQLite memory only','created':30,'published_in_test':30,'idempotent_unchanged':30,'public_api_reads':30,'production_writes':0}
    finally: await engine.dispose()

result={'baseline_pack_count':len(old),'total_valid_packs':len(packs),'new_pack_count':30,
    'duplicate_titles':0,'duplicate_full_articles':0,'duplicate_hero_hashes':0,
    'live_lifestyle_index_compared':40,
    'deduplication_scope':'Repository content at the branch base plus this batch; manual topic review of the dated public indexes documented in live-baseline.json. Unpublished database drafts were not accessed; lexical similarity is a review aid, not proof of semantic novelty.',
    'local_import':asyncio.run(verify_import()),'articles':checks}
(HERE/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='articles'},ensure_ascii=False,indent=2))
