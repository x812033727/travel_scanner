/** Read-only, signed-out checks of every published article on desktop and mobile. */
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {chromium, devices} from '@playwright/test';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '../..');
const manifest = JSON.parse(await fs.readFile(path.join(here, 'manifest.json'), 'utf8'));
assert.equal(manifest.length, 10);
const locales=['zh-TW','en','ja','ko','zh-CN'];
const output = path.join(here, 'browser');
await fs.mkdir(output, {recursive:true});
const browser = await chromium.launch({headless:true, ...(process.env.CHROMIUM_BIN ? {executablePath:process.env.CHROMIUM_BIN}: {})});
const report = {checked_at:new Date().toISOString(), authenticated:false, pages:[], listings:[]};
try {
  for (const viewport of ['desktop', 'mobile']) {
    const context = await browser.newContext(viewport === 'mobile'
      ? {...devices['iPhone 13'], locale:'zh-TW'}
      : {viewport:{width:1365,height:900},locale:'zh-TW'});
    const page = await context.newPage();
    for(const locale of locales) {
    for (const entry of manifest) {
      const item={...entry,url:entry.locales[locale].url};
      const pack = JSON.parse(await fs.readFile(path.join(root, 'apps/api/app/guides/content', item.slug+'.json'), 'utf8'));
      const doc = pack.locales[locale];
      const response = await page.goto(item.url, {waitUntil:'domcontentloaded',timeout:60000});
      assert.equal(response.status(),200,item.url);
      await page.locator('article h1').waitFor();
      assert.equal(await page.locator('article h1').textContent(),doc.title);
      const article = page.locator('main article').first();
      const text = await article.innerText();
      for(const block of doc.blocks) {
        if(block.type==='paragraph') assert(text.includes(block.text),item.slug+' missing paragraph');
        if(block.type==='heading') assert(await article.getByRole('heading',{name:block.text,exact:true}).count());
        if(block.type==='callout') assert(text.includes(block.text));
        if(block.type==='link') assert(await article.locator('a').evaluateAll((links,url)=>links.some(a=>a.href===url),block.url));
      }
      assert.equal(await article.locator('table').count(),1);
      for(const row of doc.blocks.find(b=>b.type==='table').rows) {
        for(const cell of row) assert((await article.locator('table').innerText()).includes(cell));
      }
      for(const source of doc.sources) assert(await article.locator('a').evaluateAll((links,url)=>links.some(a=>a.href===url),source.url));
      const images = [doc.hero,...doc.blocks.filter(b=>b.type==='image')];
      for(const image of images) {
        const element = article.locator(`img[alt=${JSON.stringify(image.alt)}]`);
        await element.scrollIntoViewIfNeeded();
        await element.evaluate(async img=>{if(!img.complete) await new Promise((resolve,reject)=>{img.onload=resolve;img.onerror=reject;});});
        assert(await element.evaluate(img=>img.naturalWidth>0 && img.naturalHeight>0),image.src);
      }
      assert.equal(await page.locator('link[rel="canonical"]').getAttribute('href'),item.url);
      assert.equal(await page.locator('meta[name="description"]').getAttribute('content'),doc.description);
      assert((await page.title()).includes(doc.title));
      assert.equal(await page.locator('meta[property="og:type"]').getAttribute('content'),'article');
      assert((await page.locator('meta[property="og:image"]').first().getAttribute('content')).endsWith(doc.hero.src));
      const robots = await page.locator('meta[name="robots"]').evaluateAll(nodes=>nodes.map(n=>n.content));
      assert(robots.every(content=>!content.includes('noindex')));
      const alternates = await page.locator('link[rel="alternate"][hreflang]').evaluateAll(nodes=>nodes.map(n=>n.getAttribute('hreflang')));
      assert.deepEqual(alternates.sort(),[...locales,'x-default'].sort());
      const structured = await page.locator('script[type="application/ld+json"]').evaluateAll(nodes=>nodes.flatMap(n=>JSON.parse(n.textContent)));
      assert(structured.some(data=>data['@type']==='Article' && data.headline===doc.title && data.inLanguage===locale));
      assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'horizontal page overflow');
      await page.evaluate(()=>scrollTo(0,0));
      await page.screenshot({path:path.join(output,`${viewport}-${locale}-${item.slug}.png`),fullPage:true});
      await page.screenshot({path:path.join(output,`${viewport}-${locale}-${item.slug}-top.png`)});
      await article.locator('table').screenshot({path:path.join(output,`${viewport}-${locale}-${item.slug}-table.png`)});
      report.pages.push({slug:item.slug,locale,viewport,status:response.status(),full_text:true,images:images.length,table:true,sources:doc.sources.length,internal_links:2,metadata:true,screenshot:`browser/${viewport}-${locale}-${item.slug}.png`});
      console.log(`${viewport} ${locale}: ${item.slug} passed`);
    }
    const listResponse = await page.goto(`https://mokaair.com/${locale}/life`,{waitUntil:'domcontentloaded',timeout:60000});
    assert.equal(listResponse.status(),200);
    // The first page may be paginated; the public API inventory separately covers all ten.
    const listed = await page.locator('main a[href*="/life/"]').evaluateAll(nodes=>nodes.map(n=>n.href));
    assert(listed.some(url=>manifest.some(item=>item.locales[locale].url===url)),'new articles absent from life listing');
    await page.screenshot({path:path.join(output,`${viewport}-${locale}-life-list.png`),fullPage:true});
    report.listings.push({viewport,locale,status:200,new_articles_shown:manifest.filter(item=>listed.includes(item.locales[locale].url)).length});
    }
    await context.close();
  }
  const api = await browser.newContext();
  report.public_index_articles={};
  for(const locale of locales) {
  const listing = await api.request.get(`https://mokaair.com/api/travel/guides?locale=${locale}&kind=life&limit=50`);
  assert.equal(listing.status(),200);
  const inventory=await listing.json();
  assert(manifest.every(item=>inventory.articles.some(a=>a.slug===item.slug)));
  report.public_index_articles[locale]=inventory.articles.length;
  }
  const sitemap=await api.request.get('https://mokaair.com/sitemap.xml');
  assert.equal(sitemap.status(),200);
  const xml=await sitemap.text();
  for(const item of manifest) for(const locale of locales) assert(xml.includes(`<loc>${item.locales[locale].url}</loc>`),item.slug+' '+locale+' sitemap missing');
  report.sitemap_locale_articles=50;
  assert.equal(report.pages.length,100);
  await api.close();
  await fs.writeFile(path.join(here,'public-verification.json'),JSON.stringify(report,null,2)+'\n');
} finally { await browser.close(); }
