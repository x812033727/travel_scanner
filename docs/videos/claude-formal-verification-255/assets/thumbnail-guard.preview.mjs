import fs from 'node:fs';
import path from 'node:path';
import { createHash } from 'node:crypto';
import { renderPlan } from '../../../../tools/video/render/plan.mjs';
import { openRenderer } from '../../../../tools/video/render/browser.mjs';
import { THUMB_SIZE } from '../../../../tools/video/templates/templates.mjs';

const root = path.resolve(import.meta.dirname, '../../../..');
const episode = path.dirname(import.meta.dirname);
const asset = 'docs/videos/claude-formal-verification-255/assets/thumbnail-guard.png';
const sha = (p) => createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const source = { video: sha(path.join(episode, 'video.json')), claims: sha(path.join(episode, 'claims.md')) };
const doc = JSON.parse(fs.readFileSync(path.join(episode, 'video.json'), 'utf8'));

// Change an in-memory clone only. Root owns the actual metadata adoption.
doc.thumbnail.data.asset = asset;
doc.thumbnail.data.sub = '容量8，卻放行';
doc.assets.push({ path: asset, source: 'Mokaair原創縮圖主體', license: '原創；保留權利', author: 'Mokaair' });
const workdir = '/workspace/work/videos/claude-formal-verification-255';
const plan = renderPlan(doc, undefined, root, { workdir });
const renderer = await openRenderer({ root, workdir });
let captured;
try {
  captured = await renderer.capture(plan.thumbnail.key, plan.thumbnail.html, { size: THUMB_SIZE });
  fs.writeFileSync(path.join(import.meta.dirname, 'thumbnail-guard.preview.png'), captured.still);
} finally {
  await renderer.close();
}
if (sha(path.join(episode, 'video.json')) !== source.video || sha(path.join(episode, 'claims.md')) !== source.claims) throw new Error('Source changed during readonly preview; investigate concurrent writer.');
const proof = {
  kind: 'native_thumbnail_preview_on_cloned_document_not_adopted_metadata',
  source_sha256: source, in_memory_changes: { asset, sub: doc.thumbnail.data.sub },
  size: THUMB_SIZE, problems: captured.problems,
  preview_sha256: sha(path.join(import.meta.dirname, 'thumbnail-guard.preview.png')),
  actual_visual_review: 'pending; reviewer must open generated image',
};
fs.writeFileSync(path.join(import.meta.dirname, 'thumbnail-guard.preview-proof.json'), JSON.stringify(proof, null, 2) + '\n');
console.log(JSON.stringify(proof, null, 2));
