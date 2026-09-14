/** Only our local author-fixture service; never touches user browser sessions. */
import fs from 'node:fs/promises';
import path from 'node:path';
import net from 'node:net';
import { spawn, execFile } from 'node:child_process';
import { promisify } from 'node:util';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';
const run = promisify(execFile);
const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '../../../../..');
const require = createRequire(path.join(root, 'apps/web/package.json'));
const { chromium } = require('@playwright/test');
const python = path.join(here, '.venv/Scripts/python.exe');
const out = path.join(here, 'verification/browser');
await fs.mkdir(out, { recursive: true });
const probe = net.createServer();
await new Promise(resolve => probe.listen(0, '127.0.0.1', resolve));
const port = probe.address().port;
await new Promise(resolve => probe.close(resolve));
const env = { ...process.env, GEMINI_LAB_LIVE: '0', GEMINI_API_KEY: '', GOOGLE_API_KEY: '' };
const child = spawn(python, ['-m','uvicorn','app:app','--app-dir',path.join(here,'examples/86/document-service'),'--host','127.0.0.1','--port',String(port)], { cwd: here, env, windowsHide: true, stdio: 'ignore' });
let browser;
const records = [];
try {
  let ready = false;
  const url = `http://127.0.0.1:${port}`;
  for (let n=0;n<40;n++) {
    try { const r = await fetch(url+'/health'); ready = r.ok && (await r.json()).mode === 'author_fixture'; } catch {}
    if (ready) break;
    await new Promise(resolve=>setTimeout(resolve,250));
  }
  if (!ready) throw Error('Local fixture service did not start');
  browser = await chromium.launch({headless:true});
  const page = await browser.newPage();
  await page.route('**/*', route => new URL(route.request().url()).hostname === '127.0.0.1' ? route.continue() : route.abort());
  const errors=[];
  page.on('pageerror',error=>errors.push(error.message));
  for(const width of [1200,360]) {
    await page.setViewportSize({width,height:900});
    await page.goto(url);
    await page.locator('#mode').filter({hasText:'未呼叫 Google API'}).waitFor();
    await page.locator('#send').click();
    await page.locator('#status').filter({hasText:'找到引用'}).waitFor();
    if (!(await page.locator('#answer').textContent()).includes('260')) throw Error('Wrong known answer');
    const overflow = await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth);
    if (overflow) throw Error(`Overflow at ${width}`);
    await page.screenshot({path:path.join(out,`service-${width}-cited.png`),fullPage:true});
    await page.getByRole('link',{name:'S003／v1'}).click();
    if (!page.url().endsWith('/sources/S003') || !(await page.locator('body').textContent()).includes('容量：260 毫升')) throw Error('Source navigation failed');
    await page.goBack();
    await page.locator('#question').fill('S011 的容量是多少？');
    await page.locator('#send').click();
    await page.locator('#status').filter({hasText:'缺少可核對'}).waitFor();
    if (await page.locator('#citations a').count()) throw Error('Invented citation');
    await page.screenshot({path:path.join(out,`service-${width}-missing.png`),fullPage:true});
    records.push({width,knownAnswer:'260',sourceNavigation:'same-tab verified',missing:'no citation',overflow:false});
  }
  const evaluation = await run(python,['examples/86/document-service/evaluate.py','--url',url,'--output',path.join(out,'service-evaluation.json')],{cwd:here,env,windowsHide:true});
  await run(python,['examples/82/grounding-demo/main.py','--fixture','examples/82/response-fixtures/cited.json'],{cwd:here,env,windowsHide:true});
  const html = await fs.readFile(path.join(here,'citation-view.html'),'utf8');
  // Move only our generated temporary artifact, inside the author task scope.
  await fs.rename(path.join(here,'citation-view.html'),path.join(out,'grounding-author-fixture.html'));
  const fixturePage=await browser.newPage({javaScriptEnabled:false});
  await fixturePage.route('**/*',r=>r.abort());
  for(const width of [1200,360]) {
    await fixturePage.setViewportSize({width,height:900});
    await fixturePage.setContent(html);
    await fixturePage.evaluate(async()=>await document.fonts.ready);
    if(await fixturePage.evaluate(()=>document.documentElement.scrollWidth>innerWidth)) throw Error('Grounding fixture overflow');
    await fixturePage.screenshot({path:path.join(out,`grounding-${width}.png`),fullPage:true});
  }
  if(errors.length) throw Error(errors.join('\n'));
  await fs.writeFile(path.join(out,'receipt.json'),JSON.stringify({checkedOn:'2026-09-14',browser:browser.version(),records,evaluation:JSON.parse(evaluation.stdout),pageErrors:errors,googleCalls:0,scope:'own loopback fixture service and authored HTML only',visualReview:'awaiting inspection'},null,2)+'\n');
  console.log(evaluation.stdout.trim());
} finally {
  if(browser) await browser.close();
  child.kill();
}
