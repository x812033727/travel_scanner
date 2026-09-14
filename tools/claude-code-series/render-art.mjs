import { chromium } from '@playwright/test';
import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const manifest = JSON.parse(await readFile(path.join(root, 'apps/api/app/guides/series_data/claude-code.json'), 'utf8'));
const slugs = [...manifest.entries.map(entry => entry.slug), manifest.hub];
const browser = await chromium.launch({ headless: true });
try {
  const page = await browser.newPage({ viewport: { width: 1600, height: 900 }, deviceScaleFactor: 1 });
  await page.route('**/*', route => route.abort());
  let count = 0;
  for (const slug of slugs) {
    const directory = path.join(root, 'apps/web/public/guides', slug);
    const hero = path.join(directory, 'hero.svg');
    if (!existsSync(hero)) continue;
    for (const name of ['hero', 'diagram-1']) {
      const source = await readFile(path.join(directory, `${name}.svg`), 'utf8');
      await page.setContent(`<meta charset="utf-8"><style>html,body{margin:0;padding:0}svg{display:block;width:1600px;height:900px}</style>${source}`);
      await page.evaluate(() => document.fonts.ready);
      const outside = await page.locator('svg text').evaluateAll(nodes => nodes.filter(node => {
        const box = node.getBoundingClientRect();
        return box.left < 0 || box.top < 0 || box.right > 1600 || box.bottom > 900;
      }).map(node => node.textContent));
      if (outside.length) throw new Error(`${slug}/${name} overflows: ${outside.join(', ')}`);
      if (name === 'hero') await page.screenshot({ path: path.join(directory, 'hero.jpg'), type: 'jpeg', quality: 87 });
    }
    count++;
  }
  const evidence = path.join(root, 'docs/claude-code-series/evidence');
  await mkdir(evidence, { recursive: true });
  await writeFile(path.join(evidence, 'art-validation.json'), JSON.stringify({ rendered: count, canvas: [1600, 900], svgTextBoundsChecked: true }, null, 2) + '\n');
  process.stdout.write(`Rendered and checked ${count} covers and diagrams.\n`);
} finally { await browser.close(); }
