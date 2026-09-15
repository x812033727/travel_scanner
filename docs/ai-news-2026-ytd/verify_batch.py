"""Validate this batch and exercise draft/publication/replay in SQLite memory only."""
from __future__ import annotations

import asyncio
import hashlib
import json
import os
from pathlib import Path
import re
import sys
from urllib.parse import urlparse
from uuid import uuid4

os.environ['PUBLIC_READ_RATE_LIMIT_MODE']='off'
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path[:0]=[str(ROOT/'apps/api'),str(ROOT/'apps/api/tests')]
from PIL import Image
from sqlalchemy import event
from sqlalchemy.ext.asyncio import async_sessionmaker,create_async_engine
from app.db import Base
from app.guides.content_pack import load_packs,plan_import,apply_import
from app.guides.models import GuideTopic
from app.guides.pack_ingest import lint_all,errors
from app.guides.taxonomy import SEED_TOPICS,LIFE_SEED_TOPICS,seed_names
from app.models import User
from test_guides import TABLES,make_app,client

research=[json.loads(p.read_text(encoding='utf-8')) for p in sorted((HERE/'research').glob('*.json'))]
slugs={r['slug'] for r in research}
locales={'zh-TW','zh-CN','en','ja','ko'}
assert len(slugs)==22
packs=load_packs()
new=[p for p in packs if p.slug in slugs]
assert len(new)==22
baseline=json.loads((HERE/'live-baseline.json').read_text(encoding='utf-8'))
live_slugs={a['slug'] for a in baseline['articles']}
assert not slugs.intersection(live_slugs),'New slug already published at baseline'
findings=lint_all(ROOT/'apps/api/app/guides/content',ROOT/'apps/web/public',kind='life',slugs=slugs)
bad={s:[str(p) for p in errors(v)] for s,v in findings.items() if errors(v)}
assert not bad,bad


def paragraphs(doc):
    return ''.join(b.text for b in doc.blocks if b.type=='paragraph')


def shingles(text):
    text=re.sub(r'[^a-z0-9\u3400-\u9fff]','',text.lower())
    return {text[i:i+5] for i in range(len(text)-4)}


checks=[]
hero_hashes=[]
all_docs={p.slug:p.locales['zh-TW'] for p in packs if 'zh-TW' in p.locales}
for pack in new:
    assert pack.kind=='life' and set(pack.locales)==locales and pack.destination_id is None
    doc=pack.locales['zh-TW']
    text=paragraphs(doc)
    assert 1800<=len(text)<=3000,(pack.slug,len(text))
    assert not re.search('[价单适发应实来体结条轮对构补现]',text)
    assert len(doc.title)<=60
    assert all(str(s.checked_on)=='2026-09-14' for s in doc.sources)
    assert sum(b.type=='heading' and b.level==2 for b in doc.blocks)>=3
    assert any(b.type=='table' for b in doc.blocks) and any(b.type=='callout' for b in doc.blocks)
    hero=ROOT/'apps/web/public'/doc.hero.src.lstrip('/')
    with Image.open(hero) as img: assert img.size==(1600,900)
    assert hero.stat().st_size<=300_000
    hero_hashes.append(hashlib.sha256(hero.read_bytes()).hexdigest())
    for b in doc.blocks:
        if b.type=='image':
            assert (ROOT/'apps/web/public'/b.src.lstrip('/')).stat().st_size<=300_000
        if b.type=='link' and urlparse(str(b.url)).netloc=='mokaair.com':
            assert urlparse(str(b.url)).path.rsplit('/',1)[-1] in live_slugs|slugs
    neighbours=[]
    a=shingles(text)
    for slug,other in all_docs.items():
        if slug==pack.slug: continue
        assert doc.title!=other.title and text!=paragraphs(other)
        b=shingles(paragraphs(other))
        neighbours.append((len(a&b)/max(1,len(a|b)),slug))
    score,nearest=max(neighbours)
    assert score<0.18,(pack.slug,nearest,score)
    checks.append({'slug':pack.slug,'paragraph_characters':len(text),'hero_bytes':hero.stat().st_size,'closest_article':nearest,'five_character_jaccard':round(score,4),'sources':len(doc.sources)})
assert len(set(hero_hashes))==22

locale_checks=[]
for pack in new:
    original=pack.locales['zh-TW']
    for locale,doc in pack.locales.items():
        assert [b.type for b in doc.blocks]==[b.type for b in original.blocks]
        assert [(str(s.url),str(s.checked_on)) for s in doc.sources]==[(str(s.url),str(s.checked_on)) for s in original.sources]
        assert len(doc.title)<=200 and len(doc.description)<=500
        body=paragraphs(doc)
        assert len(body)>=len(paragraphs(original))*0.7,(pack.slug,locale,'translation too short')
        if locale=='en':assert not re.search(r'[\u3400-\u9fff]{4}',body)
        for block,source in zip(doc.blocks,original.blocks):
            if block.type=='table':
                assert len(block.rows)==len(source.rows) and len(block.header)==len(source.header)
            if block.type=='link':
                url=urlparse(str(block.url))
                assert url.path.rsplit('/',1)[-1] in live_slugs|slugs
                if locale!='zh-TW':assert url.path.startswith('/'+locale+'/')
        assets=[doc.hero,*[b for b in doc.blocks if b.type=='image']]
        for asset in assets:
            file=ROOT/'apps/web/public'/asset.src.lstrip('/')
            assert file.exists() and file.stat().st_size<=300_000
            if locale!='zh-TW':assert '-'+locale.lower()+'.' in file.name
        locale_checks.append({'slug':pack.slug,'locale':locale,'paragraph_characters':len(body),'complete_block_structure':True,'sources_preserved':True,'localized_assets':len(assets)})
assert len(locale_checks)==110


async def verify_import():
    engine=create_async_engine('sqlite+aiosqlite:///:memory:')
    @event.listens_for(engine.sync_engine,'connect')
    def foreign_keys(connection,_): connection.execute('PRAGMA foreign_keys=ON')
    try:
        async with engine.begin() as conn:
            await conn.run_sync(lambda c:Base.metadata.create_all(c,tables=TABLES))
        factory=async_sessionmaker(engine,expire_on_commit=False)
        actor=User(id=uuid4(),email='ai-news-local-qa@example.com',password_hash='test-only',is_admin=True,is_active=True)
        async with factory() as session:
            for section,topics in [('travel',SEED_TOPICS),('life',LIFE_SEED_TOPICS)]:
                for order,(slug,labels) in enumerate(topics):
                    session.add(GuideTopic(slug=slug,names_json=seed_names(labels),display_order=order*10,section=section,source='seed'))
            session.add(actor)
            await session.commit()
            first=await apply_import(session,actor,await plan_import(session,new),publish=False)
            assert first.failed is None and len(first.created)==110 and not first.published
        async with client(make_app(factory)) as api:
            for locale in locales:
                assert not (await api.get('/guides',params={'locale':locale,'kind':'life'})).json()['articles']
        async with factory() as session:
            published=await apply_import(session,actor,await plan_import(session,new),publish=True)
            assert published.failed is None and len(published.published)==110
            replay=await apply_import(session,actor,await plan_import(session,new),publish=True)
            assert replay.failed is None and len(replay.unchanged)==110
            assert not replay.created and not replay.updated and not replay.published
        async with client(make_app(factory)) as api:
            for locale in locales:
                for pack in new:
                    r=await api.get(f'/guides/life/{pack.slug}',params={'locale':locale})
                    assert r.status_code==200 and r.json()['status']=='published'
                    assert set(r.json()['published_locales'])==locales
                    body=r.json()['document']
                    assert body['title']==pack.locales[locale].title
                    assert len(body['blocks'])==len(pack.locales[locale].blocks)
                listed=(await api.get('/guides',params={'locale':locale,'kind':'life','limit':50})).json()
                assert {a['slug'] for a in listed['articles']}==slugs
        return {'database':'SQLite memory only','draft_created':110,'draft_publicly_hidden':110,'published_in_test':110,'idempotent_unchanged':110,'public_reads':110,'production_writes':0}
    finally:
        await engine.dispose()


result={'checked_on':'2026-09-14','articles':checks,'locale_checks':locale_checks,'local_import':asyncio.run(verify_import()),'new_articles':22,'locale_documents':110,'duplicate_titles':0,'duplicate_bodies':0,'duplicate_hero_hashes':0,'existing_public_life_articles':len(live_slugs),'all_repository_packs_validated':len(packs),'lint_warnings':{s:[str(p) for p in ps] for s,ps in findings.items() if ps}}
(HERE/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
