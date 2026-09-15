import { mkdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import sharp from 'sharp';

const here = path.dirname(fileURLToPath(import.meta.url));
const source = path.join(here, 'output/apps/web/public/guides/notebooklm-conflicting-sources/diagram-1.svg');
const destination = path.join(here, 'visual');
mkdirSync(destination, { recursive: true });
for (const [name, width] of [['diagram-desktop.png', 1600], ['diagram-mobile.png', 360]]) {
  await sharp(source).resize({ width }).png().toFile(path.join(destination, name));
}
console.log('Rendered the revised SVG at 1600 and 360 pixels; no browser or model calls.');
