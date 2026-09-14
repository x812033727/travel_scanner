const fs = require('node:fs');
const path = require('node:path');
const { createRequire } = require('node:module');
const requireRepo = createRequire(path.join(process.cwd(), 'package.json'));
const { chromium, expect } = requireRepo('@playwright/test');
const series = JSON.parse(fs.readFileSync('apps/web/lib/guide-series.json','utf8'));
const out = __dirname;
const origin = 'https://mokaair.com';
const hub = '/zh-TW/life/' + series.hubSlug;
const result = {checkedAt:new Date().toISOString(),origin,pages:[],searches:[],status:'running'};
const save = () => fs.writeFileSync(path.join(out,'public-browser.json'),JSON.stringify(result,null,2));
async function layout(page) {
 await page.evaluate(()=>document.fonts.ready);
 const size=await page.evaluate(()=>({w:innerWidth,scroll:document.documentElement.scrollWidth}));
 expect(size.scroll,JSON.stringify(size)).toBeLessThanOrEqual(size.w+1);
}
(async()=>{
 const browser=await chromium.launch();
 try {
  for(const [name,viewport] of [['desktop',{width:1440,height:1000}],['mobile',{width:390,height:844}]]){
   const context=await browser.newContext({viewport,permissions:['clipboard-read','clipboard-write']});
   // All product HTML, APIs, JS and images remain live. Advertising/analytics are irrelevant to verification.
   await context.route(/googleads|googlesyndication|doubleclick|google-analytics|googletagmanager|stay22\.com/,r=>r.abort());
   const page=await context.newPage();page.setDefaultTimeout(20000);page.on('pageerror',e=>{result.pageErrors??=[];result.pageErrors.push(String(e));});
   await page.goto(origin+'/zh-TW/life');
   await expect(page.locator(`a[href="${hub}"]`).first()).toBeVisible();
   await page.locator(`a[href="${hub}"]`).first().click();
   await page.waitForLoadState('load');
   const lessons=page.getByTestId('series-lessons');
   await expect(lessons.locator('li > a')).toHaveCount(50);
   expect(await lessons.locator('li > a').evaluateAll(xs=>xs.map(x=>x.getAttribute('href')))).toEqual(series.articles.map(x=>'/zh-TW/life/'+x.slug));
   const search=page.getByRole('searchbox',{name:'搜尋教學或指令'});
   for(const [q,slug] of [['MD','gemini-markdown-basics'],['GEMINI.md','gemini-cli-gemini-md'],['手機','gemini-ios-app-guide'],['CLI','gemini-cli-getting-started'],['/memory','gemini-cli-memory-hierarchy'],['NotebookLM','notebooklm-guide']]){
    await search.fill(q);await expect(lessons.locator(`a[href="/zh-TW/life/${slug}"]`)).toBeVisible();await expect.poll(()=>lessons.locator('li > a').count()).toBeLessThan(50);result.searches.push({device:name,query:q,passed:true});
   }
   await page.getByRole('button',{name:'清除篩選'}).click();
   for(const group of series.groups){await page.getByRole('combobox',{name:'主題分類',exact:true}).selectOption(group.id);await expect(lessons.locator('li > a')).toHaveCount(series.articles.filter(a=>a.group===group.id).length);}
   await page.getByRole('button',{name:'清除篩選'}).click();
   for(const route of series.paths){await page.getByRole('combobox',{name:'學習路線',exact:true}).selectOption(route.id);await expect(lessons.locator('li > a')).toHaveCount(route.articles.length);}
   await page.getByRole('button',{name:'清除篩選'}).click();await layout(page);await search.scrollIntoViewIfNeeded();await page.screenshot({path:path.join(out,`${name}-hub.png`)});
   for(const a of series.articles){
    const response=await page.goto(origin+'/zh-TW/life/'+a.slug);expect(response.status()).toBe(200);
    await expect(page.locator('h1')).toHaveText(a.title);
    await expect(page.getByRole('navigation',{name:'Gemini 系列導覽',exact:true}).getByRole('link',{name:'返回 Gemini 教學總目錄'})).toHaveAttribute('href',hub);
    const bottom=page.getByRole('navigation',{name:'繼續閱讀 Gemini 系列'});
    await expect(bottom.locator('a[rel="prev"]')).toHaveCount(a.number>1?1:0);
    await expect(bottom.locator('a[rel="next"]')).toHaveCount(a.number<50?1:0);
    if(a.number>1)await expect(bottom.locator('a[rel="prev"]')).toHaveAttribute('href','/zh-TW/life/'+series.articles[a.number-2].slug);
    if(a.number<50)await expect(bottom.locator('a[rel="next"]')).toHaveAttribute('href','/zh-TW/life/'+series.articles[a.number].slug);
    for(const c of series.commands.filter(c=>c.article===a.number))await expect(page.locator('#'+c.anchor)).toHaveCount(1);
    await layout(page);
    const diagram=page.locator('img[src$="diagram-1.svg"]');await diagram.scrollIntoViewIfNeeded();
    await expect.poll(()=>diagram.evaluate(img=>img.complete&&img.naturalWidth>0)).toBeTruthy();
    if([18,36,47,50].includes(a.number)){
     const figure=page.locator('figure').filter({has:page.locator('pre')}).first();
     const code=await figure.locator('code').textContent();await figure.getByRole('button').click();
     expect((await page.evaluate(()=>navigator.clipboard.readText())).replace(/\r\n/g,'\n')).toBe(code);
     await figure.screenshot({path:path.join(out,`${name}-${a.number}-code.png`)});
    }
    result.pages.push({device:name,slug:a.slug,status:200,overflow:false,diagram:true});save();
    console.log(name,a.number,a.slug,'passed');
   }
   await context.close();
  }
  const context=await browser.newContext({javaScriptEnabled:false,viewport:{width:360,height:800}});const page=await context.newPage();
  await page.goto(origin+hub);await expect(page.getByTestId('series-lessons').locator('li > a')).toHaveCount(50);await layout(page);
  await page.getByTestId('series-lessons').locator('li > a').nth(35).click();await expect(page.locator('h1')).toHaveText(series.articles[35].title);await layout(page);
  await page.locator('img[src$="diagram-1.svg"]').scrollIntoViewIfNeeded();await page.screenshot({path:path.join(out,'no-js-360.png')});await context.close();
  result.noJavaScript='passed';result.status='passed';result.completedAt=new Date().toISOString();save();
 }catch(e){result.status='failed';result.error=String(e);save();throw e;}finally{await browser.close();}
})();
