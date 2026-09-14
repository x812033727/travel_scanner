"""Derive this fixed manifest's QA from the previously exercised publication checks."""
from pathlib import Path
HERE=Path(__file__).resolve().parent;OLD=HERE.parent/'ai-news-2026-09'
s=(OLD/'verify_batch.py').read_text(encoding='utf8')
for a,b in [('len(slugs)==10','len(slugs)==22'),('len(new)==10','len(new)==22'),('len(set(hero_hashes))==10','len(set(hero_hashes))==22'),('len(locale_checks)==50','len(locale_checks)==110'),('len(first.created)==50','len(first.created)==110'),('len(published.published)==50','len(published.published)==110'),('len(replay.unchanged)==50','len(replay.unchanged)==110'),("'new_articles':10","'new_articles':22"),("'locale_documents':50","'locale_documents':110"),("'draft_created':50","'draft_created':110"),("'draft_publicly_hidden':50","'draft_publicly_hidden':110"),("'published_in_test':50","'published_in_test':110"),("'idempotent_unchanged':50","'idempotent_unchanged':110"),("'public_reads':50","'public_reads':110"),('in live_slugs\n','in live_slugs|slugs\n')]:
    assert a in s,a
    s=s.replace(a,b)
(HERE/'verify_batch.py').write_text(s,encoding='utf8')
s=(OLD/'verify_public.mjs').read_text(encoding='utf8')
s=s.replace('manifest.length, 10','manifest.length, 22').replace('report.pages.length,100','report.pages.length,220').replace('report.sitemap_locale_articles=50','report.sitemap_locale_articles=110').replace('internal_links:2','internal_links:doc.blocks.filter(b=>b.type===\'link\').length')
s=s.replace("const response = await page.goto(item.url, {waitUntil:'domcontentloaded',timeout:60000});","await new Promise(r=>setTimeout(r,1800));\n      let response = await page.goto(item.url, {waitUntil:'domcontentloaded',timeout:60000});\n      if(response.status()===429){await new Promise(r=>setTimeout(r,35000));response=await page.goto(item.url,{waitUntil:'domcontentloaded',timeout:60000});}")
a="""  const listing = await api.request.get(`https://mokaair.com/api/travel/guides?locale=${locale}&kind=life&limit=50`);
  assert.equal(listing.status(),200);
  const inventory=await listing.json();
  assert(manifest.every(item=>inventory.articles.some(a=>a.slug===item.slug)));
  report.public_index_articles[locale]=inventory.articles.length;"""
b="""  let cursor=null;const articles=[];
  do {
    const query=new URLSearchParams({locale,kind:'life',limit:'50'});
    if(cursor)query.set('cursor',cursor);
    const listing=await api.request.get('https://mokaair.com/api/travel/guides?'+query);
    assert.equal(listing.status(),200);
    const inventory=await listing.json();articles.push(...inventory.articles);cursor=inventory.next_cursor;
  }while(cursor);
  assert(manifest.every(item=>articles.some(a=>a.slug===item.slug)));
  report.public_index_articles[locale]=articles.length;"""
assert a in s;s=s.replace(a,b)
s=s.replace('all ten','all new articles')
(HERE/'verify_public.mjs').write_text(s,encoding='utf8')
s=(OLD/'verify_assets_links.mjs').read_text(encoding='utf8').replace("const release='2123edbd2e1fc53adef0b89952ead60deef31feb';","const release=process.env.NEWS_RELEASE_SHA;\nassert(/^[a-f0-9]{40}$/.test(release),'Set exact NEWS_RELEASE_SHA');")
s=s.replace('pages.length,100','pages.length,220').replace('assets.size,100','assets.size,220')
(HERE/'verify_assets_links.mjs').write_text(s,encoding='utf8')
(HERE/'crop_public_tables.py').write_text((OLD/'crop_public_tables.py').read_text(encoding='utf8'),encoding='utf8')
print('Prepared batch-specific local and public checks')
