// Render reviewed local SVG assets with one browser. No network requests.
import { chromium } from '@playwright/test';
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const out = path.join(here, 'renders');
fs.mkdirSync(out, { recursive: true });
const manifestFile = path.join(out, 'manifest.json');
const manifest = fs.existsSync(manifestFile) ? JSON.parse(fs.readFileSync(manifestFile, 'utf8')) : {};
const slugs = JSON.parse(fs.readFileSync(path.join(here, 'catalogue.json'), 'utf8')).terms.map(t => t.slug);
slugs.push('ai-terms-index');
const browser = await chromium.launch({ executablePath: process.env.CHROMIUM_BIN || 'C:/Program Files/Google/Chrome/Application/chrome.exe', headless: true });
let rendered = 0, unchanged = 0;
try {
  const page = await browser.newPage({ viewport: { width: 1600, height: 900 }, deviceScaleFactor: 1 });
  await page.route('**/*', route => route.abort());
  for (const slug of slugs) {
    const folder = path.join(here, 'staging', slug);
    if (!fs.existsSync(path.join(folder, 'research.json'))) continue;
    for (const name of ['hero', 'diagram-1']) {
      const src = path.join(folder, `${name}.svg`);
      if (!fs.existsSync(src)) continue;
      const svg = fs.readFileSync(src, 'utf8');
      const key = `${slug}-${name}`;
      const hash = createHash('sha256').update(svg).digest('hex');
      const png = path.join(out, `${key}.png`);
      if (manifest[key]?.sha256 === hash && fs.existsSync(png)) { unchanged++; continue; }
      await page.setContent(`<!doctype html><meta charset="utf-8"><style>html,body{margin:0;padding:0}svg{display:block;width:1600px;height:900px}</style>${svg}`);
      await page.evaluate(() => document.fonts.ready);
      await page.screenshot({ path: png });
      manifest[key] = { sha256: hash, png: `${key}.png`, width: 1600, height: 900 };
      rendered++;
    }
  }
} finally {
  await browser.close();
  fs.writeFileSync(manifestFile, JSON.stringify(manifest, null, 2) + '\n');
}
console.log(JSON.stringify({ rendered, unchanged, total: Object.keys(manifest).length }));
