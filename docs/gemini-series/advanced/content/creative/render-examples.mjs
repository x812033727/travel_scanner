/** Render original vector sources locally; no Gemini/Flow browser sessions or model calls. */
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';
const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '../../../../..');
const require = createRequire(path.join(root, 'apps/web/package.json'));
const { chromium } = require('@playwright/test');
const files = [];
async function walk(dir) {
  for (const entry of await fs.readdir(dir, { withFileTypes: true })) {
    const file = path.join(dir, entry.name);
    if (entry.isDirectory() && entry.name !== '__pycache__') await walk(file);
    else if (entry.isFile() && entry.name.endsWith('.svg')) files.push(file);
  }
}
await walk(path.join(here, 'examples'));
const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1600, height: 900 }, javaScriptEnabled: false });
await page.route('**/*', r => r.abort());
const records = [];
try {
  for (const file of files) {
    const relative = path.relative(path.join(here, 'examples'), file);
    const out = path.join(here, 'verification/reference-renders', relative.replace(/\.svg$/, ''));
    await fs.mkdir(path.dirname(out), { recursive: true });
    await page.setViewportSize({ width: 1600, height: 900 });
    await page.setContent('<style>html,body{margin:0}svg{display:block;width:100vw;height:56.25vw}</style>' + await fs.readFile(file,'utf8'));
    await page.evaluate(async()=>await document.fonts.ready);
    const clipped = await page.locator('svg text').evaluateAll(nodes=>nodes.filter(n=>{const b=n.getBoundingClientRect();return b.right>1600||b.left<0||b.bottom>900||b.top<0;}).map(n=>n.textContent));
    if (clipped.length) throw Error(relative+': '+clipped.join(', '));
    await page.screenshot({ path: file.replace(/\.svg$/, '.png') });
    await page.screenshot({ path: out + '.png' });
    await page.setViewportSize({ width: 360, height: 203 });
    await page.screenshot({ path: out + '-mobile.png' });
    records.push({ file:path.relative(here,file).replaceAll('\\','/'), png:file.replace(/\.svg$/,'.png').split(path.sep).pop(), clippedLabels:[], origin:'author-vector-reference-not-model-output' });
  }
} finally { await browser.close(); }
await fs.writeFile(path.join(here,'verification/reference-rendering.json'),JSON.stringify({checkedOn:'2026-09-14',records,modelCalls:0,generatedVideos:0},null,2)+'\n');
console.log(JSON.stringify({originalReferences:records.length,previews:records.length*2}));
