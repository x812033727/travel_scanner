import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
import {pathToFileURL} from 'node:url';
import {chromium} from 'playwright';
const out=path.resolve(process.argv[2]);
assert.ok(!fs.existsSync(path.join(out,'targeted-browser-review.json')),'Existing targeted review is evidence; use a new output copy instead of overwriting it');
const hash=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
assert.equal(hash(path.join(out,'animatic.html')),'cee2fc9cbe89b879e8c899bccd3888a63ddfb9f6534e09163e27c6f2872324d1');
const started_at=new Date().toISOString();
const browser=await chromium.launch({headless:true,channel:'msedge'});
const rows=[], errors=[];
try {
  const page=await browser.newPage({viewport:{width:1440,height:1200}});
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto(pathToFileURL(path.join(out,'animatic.html')).href);
  for(const id of ['a03-s085','a03-s086','a03-s087','a04-s037','a04-s038','a04-s039']) {
    await page.getByLabel('跳至鏡號').selectOption({label:id});
    await page.evaluate(()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))));
    const text=await page.locator('#stage').innerText();
    assert.ok(text.includes(id));
    if(id==='a03-s086') {assert.ok(text.includes('without the crown'));assert.ok(!text.includes('complete crown'));}
    if(id==='a04-s038') {assert.ok(text.includes("Bao's open right palm"));assert.ok(!text.includes("Bao's open left palm"));}
    const screenshot=`targeted-${id}.png`;
    await page.screenshot({path:path.join(out,screenshot),fullPage:false});
    rows.push({id,observed_at:new Date().toISOString(),text,screenshot,screenshot_sha256:hash(path.join(out,screenshot))});
  }
  assert.equal(errors.length,0);
  fs.writeFileSync(path.join(out,'targeted-browser-review.json'),JSON.stringify({
    schema_version:1,method:'Local authored HTML regression test; Playwright headless Microsoft Edge, native UI selectOption; six paused cards',
    started_at,finished_at:new Date().toISOString(),video_sha256:hash(path.join(out,'video.json')),
    html_sha256:hash(path.join(out,'animatic.html')),prior_attempts:[{method:'CUA IAB',action:'six-card selection then existing-tab rebind',result:'both timed out and kernel reset; no observation claimed'}],
    independent_review:false,full_length_watch:false,visual_screenshot_review:'pending',errors,rows,
  },null,2)+'\n');
  console.log(JSON.stringify({cards:rows.length,errors,output:'targeted-browser-review.json'}));
} finally {await browser.close();}
