import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import {fileURLToPath, pathToFileURL} from 'node:url';
import {createHash} from 'node:crypto';
import {chromium} from '@playwright/test';

const dir=path.dirname(fileURLToPath(import.meta.url)), poolDir=path.resolve(dir,'../..');
const sha=file=>createHash('sha256').update(fs.readFileSync(file)).digest('hex');
const context=vm.createContext({});vm.runInContext(fs.readFileSync(path.join(dir,'demo.js'),'utf8'),context);
const m=context.losslessDemo, plain=value=>JSON.parse(JSON.stringify(value));
const vectors=[{input:[6,2],encoded:{mid:4,side:4}},{input:[6,3],encoded:{mid:4,side:3}},{input:[-6,-3],encoded:{mid:-5,side:-3}},{input:[-32768,32767],encoded:{mid:-1,side:-65535}}];
for(const v of vectors){const encoded=m.encodeStereo(...v.input);assert.deepEqual(plain(encoded),v.encoded);const out=m.decodeStereo(encoded.mid,encoded.side);assert.deepEqual([out.left,out.right],v.input);}
let pairs=0;
for(let l=-128;l<=127;l++)for(let r=-128;r<=127;r++){const e=m.encodeStereo(l,r),d=m.decodeStereo(e.mid,e.side);assert.equal(d.left,l);assert.equal(d.right,r);pairs++;}
let seed=9639;const next=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return (seed&65535)-32768;};
const edge=[-32768,-32767,-1,0,1,32766,32767];let boundary=0;
for(const l of edge)for(const r of edge){const e=m.encodeStereo(l,r),d=m.decodeStereo(e.mid,e.side);assert.equal(d.left,l);assert.equal(d.right,r);boundary++;}
let sequences=0;
for(let i=0;i<128;i++){const samples=Array.from({length:64},next);assert.deepEqual(plain(m.decode(m.encode(samples))),samples);sequences++;}
assert.deepEqual(plain(m.encode(m.presets.smooth)),{first:100,residuals:[1,2,-1,2,1]});
const bad=m.encode(m.presets.smooth);bad.residuals[0]=0;assert.deepEqual(plain(m.decode(bad)),[100,100,102,101,103,104]);
assert.deepEqual(plain(m.decodeStereo(4,3,false)),{left:5,right:2,restoredSum:8,odd:1});
assert.deepEqual(plain(m.decodeStereo(-5,-3,false)),{left:-7,right:-4,restoredSum:-10,odd:1});
const browser=await chromium.launch({headless:true});
try{
 const page=await browser.newPage({viewport:{width:1440,height:1000}}),errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto(pathToFileURL(path.join(dir,'demo.html')).href);
 await page.locator('#restore').click();assert.match(await page.locator('#prediction-result').textContent(),/每一點都回來/);
 await page.locator('#damage').click();assert.match(await page.locator('#prediction-result').textContent(),/已經不同/);
 await page.locator('#signal').selectOption('jump');await page.locator('#restore').click();assert.match(await page.locator('#prediction-result').textContent(),/每一點都回來/);
 for(const id of ['even','odd','negative','edge']){await page.locator('#stereo-case').selectOption(id);assert.match(await page.locator('#stereo-result').textContent(),/原樣還原/);await page.locator('#parity').click();assert.match(await page.locator('#stereo-result').textContent(),id==='even'?/原樣還原/:/錯誤版本/);await page.locator('#parity').click();}
 await page.locator('#signal').selectOption('smooth');await page.locator('#restore').click();await page.locator('#stereo-case').selectOption('odd');
 await page.screenshot({path:path.join(poolDir,'.cache/wave6-g59-desktop.png'),fullPage:true});
 await page.setViewportSize({width:390,height:844});assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);
 assert.ok(await page.locator('.table-wrap').evaluate(el=>{el.scrollLeft=el.scrollWidth;return el.scrollLeft>0}));
 assert.equal(await page.locator('#prediction-table tr').last().locator('td').last().textContent(),'105');
 await page.locator('.table-wrap').evaluate(el=>{el.scrollLeft=0});
 await page.screenshot({path:path.join(poolDir,'.cache/wave6-g59-mobile.png'),fullPage:true});assert.deepEqual(errors,[]);
 const receipt={status:'PASS_ARITHMETIC_AND_UI_NOT_CODEC_OR_AUDIENCE_TEST',tested_on:new Date().toISOString(),node:process.version,browser:await browser.version(),files:['demo.js','demo.html','verify-demo.mjs'].map(file=>({file,sha256:sha(path.join(dir,file))})),checks:{fixed_vectors:vectors,exhaustive_signed_8bit_stereo_pairs:pairs,signed_16bit_boundary_pairs:boundary,seeded_prediction_sequences:sequences,samples_per_sequence:64,seed:9639,explicit_corrupted_residual_counterexample:true,positive_and_negative_odd_parity_counterexamples:true,presets_and_buttons:true,mobile_document_horizontal_overflow:false,page_errors:errors},scope:'Original first-order predictor and mid/side integer arithmetic only; not a FLAC bitstream implementation. No filesize, Rice-code, CRC, subjective hearing or performance claims. Browser and arithmetic exercised; no narration or audience test.',screenshots:['.cache/wave6-g59-desktop.png','.cache/wave6-g59-mobile.png'],visual_inspection:'PENDING_ROOT_VIEW',production_ready:false};
 fs.writeFileSync(path.join(poolDir,'reviews/wave6-g59-demo.json'),JSON.stringify(receipt,null,2)+'\n');console.log(JSON.stringify(receipt));
}finally{await browser.close();}
