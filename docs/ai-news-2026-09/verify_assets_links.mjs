/** Public asset integrity and internal-link checks; no authentication or writes. */
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';
import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {chromium} from '@playwright/test';

const here=path.dirname(fileURLToPath(import.meta.url));
const root=path.resolve(here,'../..');
const manifest=JSON.parse(await fs.readFile(path.join(here,'manifest.json'),'utf8'));
const release='2123edbd2e1fc53adef0b89952ead60deef31feb';
const publicReport=JSON.parse(await fs.readFile(path.join(here,'public-verification.json'),'utf8'));
assert.equal(publicReport.pages.length,100,'Complete desktop/mobile verification first');
const assets=new Set(), links=new Set();
for(const entry of manifest) {
  const pack=JSON.parse(await fs.readFile(path.join(root,'apps/api/app/guides/content',entry.slug+'.json'),'utf8'));
  for(const doc of Object.values(pack.locales)) {
    assets.add(doc.hero.src);
    for(const block of doc.blocks) {
      if(block.type==='image') assets.add(block.src);
      if(block.type==='link') links.add(block.url);
    }
  }
}
assert.equal(assets.size,100);
const report={checked_at:new Date().toISOString(),release_sha:release,authenticated:false,assets:[],internal_links:[]};
const knownTargets=new Map(manifest.flatMap(entry=>Object.entries(entry.locales).map(([locale,doc])=>[doc.url,{slug:entry.slug,locale,title:doc.title}])));
const browser=await chromium.launch({headless:true});
try {
  const context=await browser.newContext({userAgent:'Twitterbot/1.0'});
  const hash=data=>createHash('sha256').update(data).digest('hex');
  for(const src of assets) {
    const response=await context.request.get('https://mokaair.com'+src);
    assert.equal(response.status(),200,src);
    const body=await response.body();
    assert(body.length<300*1024,src+' exceeds image limit');
    // Compare the released Git blob, avoiding Windows checkout line-ending conversion.
    const expected=execFileSync('git',['show',`${release}:apps/web/public${src}`],{cwd:root});
    assert.equal(hash(body),hash(expected),src+' differs from released artwork');
    report.assets.push({src,bytes:body.length,sha256:hash(body),status:200});
  }
  const page=await context.newPage();
  for(const url of links) {
    const known=knownTargets.get(url);
    if(known) {
      const evidence=publicReport.pages.filter(p=>p.slug===known.slug && p.locale===known.locale);
      assert.deepEqual(evidence.map(p=>p.viewport).sort(),['desktop','mobile']);
      assert(evidence.every(p=>p.status===200 && p.full_text && p.metadata));
      report.internal_links.push({url,status:200,title:known.title,evidence:'public-verification.json desktop and mobile'});
      continue;
    }
    await new Promise(resolve=>setTimeout(resolve,5000));
    let response=await page.goto(url,{waitUntil:'domcontentloaded',timeout:60000});
    if(response.status()===429) {
      const requested=Number(response.headers()['retry-after']);
      const delay=Number.isFinite(requested) && requested>0 ? requested*1000 : 30000;
      console.log(`Rate limited; honoring retry delay for ${url}`);
      await new Promise(resolve=>setTimeout(resolve,Math.max(30000,delay)));
      response=await page.goto(url,{waitUntil:'domcontentloaded',timeout:60000});
    }
    assert.equal(response.status(),200,url);
    assert.equal(await page.locator('article h1').count(),1,url+' has no published article');
    assert.equal(await page.locator('link[rel="canonical"]').getAttribute('href'),url);
    report.internal_links.push({url,status:200,title:await page.locator('article h1').textContent(),evidence:'signed-out crawler page'});
  }
  await fs.writeFile(path.join(here,'asset-link-verification.json'),JSON.stringify(report,null,2)+'\n');
  console.log(JSON.stringify({assets:report.assets.length,internal_links:report.internal_links.length}));
} finally {await browser.close();}
