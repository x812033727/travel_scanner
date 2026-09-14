/** Render this batch's authored SVGs in one isolated Chromium process. */
import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {chromium} from '@playwright/test';
const here=path.dirname(fileURLToPath(import.meta.url));
const jobs=JSON.parse(await fs.readFile(path.join(here,'renders/jobs.json'),'utf8'));
const browser=await chromium.launch({headless:true});
try {
 const page=await browser.newPage({viewport:{width:1600,height:900},deviceScaleFactor:1});
 for(const job of jobs){
   const svg=await fs.readFile(job.svg,'utf8');
   await page.setContent('<!doctype html><meta charset="utf-8"><style>html,body{margin:0}svg{display:block;width:1600px;height:900px}</style>'+svg);
   await page.evaluate(()=>document.fonts.ready);
   const overflow=await page.locator('svg text').evaluateAll(nodes=>nodes.filter(n=>{const b=n.getBBox();return b.x<0||b.x+b.width>1600;}).map(n=>n.textContent));
   if(overflow.length)throw Error(JSON.stringify(overflow));
   await page.screenshot({path:job.png});
 }
 console.log(`Rendered ${jobs.length} localized assets`);
}finally{await browser.close();}
