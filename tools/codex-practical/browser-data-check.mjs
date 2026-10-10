#!/usr/bin/env node
// Observe the learner website. This does not record the native Codex App.
import assert from 'node:assert/strict';
import { createServer } from 'node:http';
import { mkdirSync, readFileSync, writeFileSync, existsSync } from 'node:fs';
import path from 'node:path';
import { parseArgs } from 'node:util';
import { chromium } from '@playwright/test';
import { createHash } from 'node:crypto';
import { pathToFileURL } from 'node:url';

const { values } = parseArgs({ options: { lesson:{type:'string'}, output:{type:'string'} } });
if (!values.lesson || !values.output) throw new Error('Use --lesson expanded lesson directory --output NEW_DIRECTORY');
const source = path.resolve(values.lesson, 'reference'), output = path.resolve(values.output);
if (existsSync(output)) throw new Error('Preserve existing receipts; choose a new output directory.');
mkdirSync(output, {recursive:true});
const server = createServer((req,res) => {
  try {
    const suffix = decodeURIComponent(new URL(req.url,'http://localhost').pathname);
    const file = path.resolve(source, '.' + (suffix === '/' ? '/index.html' : suffix));
    if (!file.startsWith(source + path.sep)) throw new Error('outside source');
    res.setHeader('Content-Type', ({'.html':'text/html','.mjs':'text/javascript','.css':'text/css'})[path.extname(file)] ?? 'application/octet-stream');
    res.end(readFileSync(file));
  } catch { res.writeHead(404); res.end('Not found'); }
});
await new Promise(resolve => server.listen(0,'127.0.0.1',resolve));
const browser = await chromium.launch({channel:'msedge',headless:true});
const checks = [], errors = [], key = 'mokaair-codex-practical-v2';
const context = await browser.newContext({viewport:{width:390,height:844},acceptDownloads:true});
const page = await context.newPage();
page.on('pageerror', error => errors.push(error.message));
const store = () => page.evaluate(key => JSON.parse(localStorage.getItem(key)),key);
const mark = name => checks.push({name,status:'pass'});
try {
  await page.goto(`http://127.0.0.1:${server.address().port}`);
  await page.locator('#import-file').setInputFiles(path.join(source,'fixtures/tasks.json'));
  await page.waitForFunction(() => document.querySelector('#message').textContent === '整批匯入完成。');
  assert.equal(await page.locator('#tasks li').count(),5);
  await page.locator('#report-form button').click();
  const truth = JSON.parse(readFileSync(path.join(source,'fixtures/truth.json'),'utf8'));
  assert.deepEqual(JSON.parse(await page.locator('#report').textContent()),truth);
  mark('import-five-fixture-tasks-and-verify-Taipei-weekly-report');
  const before = await store();
  const downloadEvent = page.waitForEvent('download');
  await page.locator('#export-csv').click();
  const csvDownload = await downloadEvent;
  await csvDownload.saveAs(path.join(output,'exported.csv'));
  const { decodeCsv } = await import(pathToFileURL(path.join(source,'core.mjs')).href);
  assert.deepEqual(decodeCsv(readFileSync(path.join(output,'exported.csv'),'utf8')),before.tasks);
  mark('actual-CSV-download-roundtrip-preserves-identities-and-times');
  await page.locator('#import-file').setInputFiles({name:'damaged.json',mimeType:'application/json',buffer:Buffer.from('{bad')});
  await page.waitForFunction(() => document.querySelector('#message').textContent.includes('整批匯入拒絕'));
  assert.deepEqual(await store(),before);
  mark('damaged-import-rejected-atomically-without-data-loss');
  await page.locator('#search').fill('nothing-matches');
  assert.equal(await page.locator('#tasks li').count(),0);
  assert.equal(await page.locator('#empty').isVisible(),true);
  assert.equal((await store()).tasks.length,5);
  await page.locator('#search').fill('');
  mark('empty-search-result-preserves-hidden-data');
  const pending = page.locator('#tasks input[data-id="pending"]');
  await pending.check();
  assert.match((await store()).tasks.find(task=>task.id==='pending').completedAt,/Z$/);
  assert.equal(await page.evaluate(() => document.activeElement.dataset.id),'pending');
  await pending.uncheck();
  assert.equal((await store()).tasks.find(task=>task.id==='pending').completedAt,null);
  await page.reload();
  assert.equal((await store()).tasks.find(task=>task.id==='unknown').completedAt,null);
  mark('completion-time-toggle-focus-and-unknown-date-survive-reload');
  const add = async title => { await page.locator('#task-title').fill(title); await page.locator('#task-form button').click(); };
  await add('同名'); await add('同名');
  const duplicateIds = (await store()).tasks.filter(task=>task.title==='同名').map(task=>task.id);
  await page.locator(`#tasks button[data-id="${duplicateIds[1]}"]`).click();
  assert.equal((await store()).tasks.some(task=>task.id===duplicateIds[0]),true);
  assert.equal((await store()).tasks.some(task=>task.id===duplicateIds[1]),false);
  assert.equal(await page.evaluate(() => document.activeElement.id),'task-title');
  mark('same-title-delete-removes-only-selected-ID-and-restores-focus');
  assert.equal(await page.evaluate(() => document.documentElement.scrollWidth<=innerWidth),true);
  await page.screenshot({path:path.join(output,'390px.png'),fullPage:true});
  await page.setViewportSize({width:1280,height:900});
  assert.equal(await page.evaluate(() => document.documentElement.scrollWidth<=innerWidth),true);
  mark('390px-and-1280px-have-no-horizontal-overflow');
  await page.evaluate(key => {
    localStorage.removeItem(key);
    localStorage.setItem('mokaair-codex-practical-v1',JSON.stringify({version:1,tasks:[{id:'legacy',title:'舊完成',completed:true}]}));
    localStorage.setItem('other-example','preserve');
  },key);
  await page.reload();
  assert.match(await page.locator('#message').textContent(),/舊資料/);
  assert.equal(await page.locator('#tasks li').count(),1);
  assert.equal(await page.locator('#tasks input').isChecked(),true);
  assert.equal(await store(),null); // Migration is read-only until the first mutation.
  await add('遷移後新增');
  const migrated = await store();
  assert.equal(migrated.version,2);
  assert.equal(migrated.tasks[0].completedAt,null);
  const legacyRaw = await page.evaluate(() => localStorage.getItem('mokaair-codex-practical-v1'));
  await page.locator('details summary').click();
  await page.locator('#reset').click();
  await page.reload();
  assert.equal(await page.locator('#tasks li').count(),0);
  assert.equal(await page.evaluate(() => localStorage.getItem('mokaair-codex-practical-v1')),legacyRaw);
  assert.equal(await page.evaluate(() => localStorage.getItem('other-example')),'preserve');
  mark('v1-migration-preserves-unknown-and-original; reset-stays-empty-after-reload');
  assert.deepEqual(errors,[]);
  const hashFile = file => createHash('sha256').update(readFileSync(file)).digest('hex');
  const receipt = {schema_version:1,checked_on:new Date().toISOString(),node_version:process.version,
    browser_version:browser.version(),evidence_kind:'actual-Edge-learner-website; not-native-Codex-App',
    source_directory:source,source_hashes:Object.fromEntries(['core.mjs','storage.mjs','app.mjs','index.html','style.css'].map(file=>[file,hashFile(path.join(source,file))])),checks};
  writeFileSync(path.join(output,'receipt.json'),JSON.stringify(receipt,null,2)+'\n');
  console.log(JSON.stringify({checks:checks.length,status:'pass'}));
} catch(error) {
  writeFileSync(path.join(output,'failure.json'),JSON.stringify({checked_on:new Date().toISOString(),checks,error:error.message},null,2)+'\n');
  throw error;
} finally { await context.close(); await browser.close(); await new Promise(resolve=>server.close(resolve)); }
