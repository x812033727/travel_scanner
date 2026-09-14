"""Execute inside the released API container. Uses the existing scoped CLI only."""
import asyncio, datetime, hashlib, json, os, subprocess, sys
from pathlib import Path
from sqlalchemy import select, text
from app.db import SessionFactory, engine
from app.config import get_settings
from app.models import User
from app.guides.content_pack import load_packs
SLUGS = ["ai-news-claude-opus-5-20260724","ai-news-gpt-56-price-cut-20260730","ai-news-eu-transparency-20260802","ai-news-chatgpt-free-thinking-20260806","ai-news-gemini-live-20260826","ai-news-claude-fable-51-20260901","ai-news-gemini-38-flash-20260902","ai-news-gpt-6-astra-20260903","ai-news-lyria-35-gemini-20260904","ai-news-chatgpt-images-25-20260908"]
assert len(SLUGS)==len(set(SLUGS))==10
LOCALES = ['zh-TW', 'en', 'ja', 'ko', 'zh-CN']
KEYS = sorted(s+':'+locale for s in SLUGS for locale in LOCALES)
packs=load_packs(slugs=set(SLUGS))
assert len(packs)==10 and all(p.kind=='life' and set(p.locales)==set(LOCALES) for p in packs)
STORE=Path('/tmp/mokaair-ai-news-20260914')
os.umask(0o077)
STORE.mkdir(exist_ok=True)
args=[sys.executable,'-m','app.cli','guides-import']
for locale in LOCALES: args+=['--locale',locale]
for slug in SLUGS: args+=['--slug',slug]
def cli(*extra):
    r=subprocess.run(args+list(extra),capture_output=True,text=True,check=True)
    return json.loads(r.stdout)
async def fingerprint():
    condition="a.slug != ALL(:slugs)"
    specs={
      'guide_articles':f'SELECT a.* FROM guide_articles a WHERE {condition}',
      'guide_article_locales':f'SELECT l.* FROM guide_article_locales l JOIN guide_articles a ON a.id=l.article_id WHERE {condition}',
      'guide_article_topics':f'SELECT t.* FROM guide_article_topics t JOIN guide_articles a ON a.id=t.article_id WHERE {condition}',
      'guide_article_revisions':f'SELECT r.* FROM guide_article_revisions r JOIN guide_article_locales l ON l.id=r.article_locale_id JOIN guide_articles a ON a.id=l.article_id WHERE {condition}',
      'guide_topics':'SELECT * FROM guide_topics',
      'site_pages':'SELECT * FROM site_pages',
      'provider_configs':'SELECT * FROM provider_configs'
    }
    out={}
    async with SessionFactory() as session:
      for name,sql in specs.items():
        rows=list(await session.scalars(text('SELECT row_to_json(t)::text FROM ('+sql+') t ORDER BY row_to_json(t)::text'),{'slugs':SLUGS} if ':slugs' in sql else {}))
        out[name]={'rows':len(rows),'sha256':hashlib.sha256('\n'.join(rows).encode()).hexdigest()}
    return out
async def actor():
    owners=sorted(get_settings().admin_email_set)
    async with SessionFactory() as session:
      users=list(await session.scalars(select(User).where(User.email.in_(owners),User.is_active.is_(True))))
      assert len(users)==1, 'Expected exactly one existing active configured owner'
      return users[0].email
async def main():
    try:
        mode=sys.argv[1]
        if mode=='dry-run':
            assert not (STORE/'published.json').exists()
            plan=cli('--dry-run')
            assert plan['dry_run'] is True and len(plan['articles'])==10
            assert sorted(a['slug'] for a in plan['articles'])==sorted(SLUGS)
            assert all(a['taxonomy']=='create' and a['locales']==[{'locale':locale,'action':'create','publish':True} for locale in LOCALES] for a in plan['articles'])
            baseline={'plan':plan,'protected':await fingerprint(),'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
            (STORE/'baseline.json').write_text(json.dumps(baseline))
            print(json.dumps(baseline))
        elif mode=='publish':
            baseline=json.loads((STORE/'baseline.json').read_text())
            assert await fingerprint()==baseline['protected'], 'Other editorial state changed since dry-run'
            assert cli('--dry-run')==baseline['plan'], 'Import plan changed since dry-run'
            email=await actor()
            result=cli('--actor-email',email,'--publish')
            (STORE/'published.json').write_text(json.dumps(result))
            assert result['failed'] is None and sorted(result['created'])==KEYS and sorted(result['published'])==KEYS,result
            assert not result['updated'] and not result['taxonomy_updated']
            after=await fingerprint()
            assert after==baseline['protected'], 'Existing editorial data changed'
            replay=cli('--actor-email',email,'--publish')
            assert replay['failed'] is None and sorted(replay['unchanged'])==KEYS,replay
            assert not any(replay[k] for k in ['created','updated','published','taxonomy_updated'])
            output={'published_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result':result,'replay':replay,'protected_before':baseline['protected'],'protected_after':after,'existing_editorial_data_unchanged':True}
            (STORE/'verified.json').write_text(json.dumps(output))
            print(json.dumps(output))
        else:
            raise SystemExit('Use dry-run or publish')
    finally:
        await engine.dispose()

asyncio.run(main())
