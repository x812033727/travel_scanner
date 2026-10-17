#!/usr/bin/env node
// Static readability preview only; this does not render or approve the B18 episode.
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import sharp from 'sharp';
import { openRenderer } from '../../../../../tools/video/render/browser.mjs';
import { sceneProblems, slideHtml } from '../../../../../tools/video/templates/templates.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '../../../../..');
const mode = process.argv[2];
assert(['--write', '--check'].includes(mode), 'use --write or --check');
const sha = (bytes) => crypto.createHash('sha256').update(bytes).digest('hex');
const engineBytes = fs.readFileSync(path.join(here, 'remapped-chapters/engine.json'));
const manifest = JSON.parse(fs.readFileSync(path.join(here, 'sha256.json'), 'utf8'));
assert.equal(sha(engineBytes), manifest.files['remapped-chapters/engine.json'], 'engine changed after candidate build');
const themeBytes = fs.readFileSync(path.join(root, 'tools/video/templates/theme.css'));
assert.equal(sha(themeBytes), 'ae26b5b6c920b2d2cfffa45bdc0c181a996c7cd3689cc9769d6186875df360c5', 'theme drift');
const chapter = JSON.parse(engineBytes);
const scene = chapter.scenes.find((item) => item.id === 'engine-s041');
assert.equal(scene?.template, 'title');
assert.deepEqual(scene.data, { title: '1958.04 · 約 20 坪', subtitle: '布施首店', tag: 'J-Net21／發明協會' });
assert.deepEqual(sceneProblems(scene), [], 'card schema');
const state = { reveal: 0, previousReveal: 0, first: true, totalReveals: 0,
  chapter: null, chapterNumber: 0, chapterCount: 0 };
const renderer = await openRenderer({ root, channel: process.env.VIDEO_BROWSER_CHANNEL || 'msedge' });
let full;
try {
  const frame = await renderer.capture('b18e041', slideHtml(scene, state));
  assert.deepEqual(frame.problems, [], 'card renderer');
  full = frame.still;
} finally { await renderer.close(); }
const mobile = await sharp(full).resize(320, 180).png().toBuffer();
const outputs = new Map([
  ['engine-s041-1920x1080.png', full],
  ['engine-s041-320x180.png', mobile],
]);
const report = {
  schema_version: 1, status: 'STATIC_CARD_RENDER_ONLY_NOT_EPISODE_APPROVAL',
  scene_id: scene.id, engine_sha256: sha(engineBytes), theme_sha256: sha(themeBytes),
  render_channel: process.env.VIDEO_BROWSER_CHANNEL || 'msedge',
  full_png_sha256: sha(full), mobile_png_sha256: sha(mobile),
  renderer_problems: [], tag: scene.data.tag,
};
outputs.set('card-preview.json', Buffer.from(JSON.stringify(report, null, 2) + '\n'));
for (const [name, bytes] of outputs) {
  const target = path.join(here, name);
  if (mode === '--write') fs.writeFileSync(target, bytes);
  else assert.equal(sha(fs.readFileSync(target)), sha(bytes), `render output drift: ${name}`);
}
console.log(JSON.stringify({ status: 'PASS_STATIC_CARD_ONLY', mode, full_png_sha256: sha(full), mobile_png_sha256: sha(mobile) }));
