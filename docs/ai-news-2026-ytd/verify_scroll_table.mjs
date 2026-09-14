/** Capture a wide mobile table by using its existing horizontal scrollbar. */
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {chromium, devices} from '@playwright/test';
const here=path.dirname(fileURLToPath(import.meta.url));
const manifest=JSON.parse(await fs.readFile(path.join(here,'manifest.json'),'utf8'));
const browser=await chromium.launch({headless:true});
try {
  const context=await browser.newContext({...devices['iPhone 13'],locale:'zh-TW'});
  const page=await context.newPage();
  for(const stem of process.argv.slice(2)) {
    const target=manifest.flatMap(i=>Object.entries(i.locales).map(([locale,doc])=>({stem:`mobile-${locale}-${i.slug}`,url:doc.url}))).find(i=>i.stem===stem);
    assert(target,'Stem must belong to the publication whitelist');
    const response=await page.goto(target.url,{waitUntil:'domcontentloaded'});
    assert.equal(response.status(),200);
    const table=page.locator('main article table');
    await table.waitFor();
    await page.evaluate(()=>document.fonts.ready);
    for(const img of await page.locator('main article img').all()) {await img.scrollIntoViewIfNeeded();await img.evaluate(i=>i.decode());}
    const captures=[];
    for(const side of ['left','right']) {
      // Let the sticky header finish reacting to the return from image loading.
      // Measuring during smooth scrolling can give a stale document offset.
      await page.evaluate(()=>scrollTo({top:0,behavior:'instant'}));
      await page.waitForFunction(()=>scrollY===0);
      await page.evaluate(()=>document.fonts.ready);
      await page.waitForTimeout(750);
      const geometry=await table.evaluate((table,side)=>{
        const box=table.parentElement;
        box.scrollLeft=side==='left'?0:box.scrollWidth;
        const tr=table.getBoundingClientRect(),br=box.getBoundingClientRect();
        return {left:br.left,top:tr.top+scrollY,visibleWidth:box.clientWidth,width:tr.width,height:tr.height,scrollLeft:box.scrollLeft,dpr:devicePixelRatio,overflow:getComputedStyle(box).overflowX};
      },side);
      assert.equal(geometry.overflow,'auto');
      const name=`${stem}-scroll-${side}.png`;
      await page.screenshot({path:path.join(here,'browser',name),fullPage:true});
      const after=await table.evaluate(t=>({top:t.getBoundingClientRect().top+scrollY,height:t.getBoundingClientRect().height}));
      assert(Math.abs(after.top-geometry.top)<.1 && Math.abs(after.height-geometry.height)<.1,'Layout changed while capturing the table');
      captures.push({side,source:`browser/${name}`,...geometry});
    }
    assert.equal(captures[0].scrollLeft,0);
    assert(captures[1].scrollLeft>0);
    assert(Math.abs(captures[1].scrollLeft+captures[1].visibleWidth-captures[1].width)<=1);
    await fs.writeFile(path.join(here,'browser',`${stem}-scroll.json`),JSON.stringify({url:target.url,checked_at:new Date().toISOString(),authenticated:false,captures,native_horizontal_scroll_verified:true},null,2)+'\n');
    console.log(stem+' native horizontal scrolling passed');
  }
} finally {await browser.close();}
