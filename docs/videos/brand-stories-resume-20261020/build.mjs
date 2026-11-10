// Offline production exports only. Never calls a provider, imports work or writes approvals.
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { readFileSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '../../..');
const base = 'docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016';
const editorial = `${base}/A01-editorial-candidate-20261019-r47`;
const canonical = `${base}/A01-worker-handoff-r47-canonical-20261019`;
const bytes = p => readFileSync(path.join(root, p));
const hash = b => createHash('sha256').update(b).digest('hex');
const json = p => JSON.parse(bytes(p));
const pinned = {
  [`${editorial}/manifest.json`]: '323dc77c5ec678ef38c35204eb7865d46c8ca612b5e82f0a6083ddf70c59a24e',
  [`${canonical}/manifest.json`]: '3edb9c375bcef6b01adc4e7bd14eec3757dd907d16a175247f8468a063465fb2',
};
for (const [p, expected] of Object.entries(pinned)) assert.equal(hash(bytes(p)), expected, p);
const video = json(`${canonical}/worker-composed-video.json`);
const manifest = json(`${canonical}/manifest.json`);
const metadata = json(`${canonical}/metadata-delta.json`);
const keys = ['hook', 'origin', 'idea', 'engine', 'turn', 'now'];
const chapters = keys.map(key => json(`${canonical}/story/chapters/${key}.json`));
assert.equal(video.slug, 'story-rolling-suitcase-v2');
assert.deepEqual(video.look, { preset: 'cute-mystery' });
assert.equal(video.scenes.length, 50);
assert.equal(video.scenes.flatMap(s => s.lines ?? []).length, 52);
const claims = chapters.flatMap(c => c.claims ?? []);
assert.equal(claims.length, 54);
assert.ok(claims.every(c => c.verdict === 'PENDING'));
assert.equal(manifest.duration_gate_passed, false);
const inputs = [...Object.keys(pinned), `${canonical}/worker-composed-video.json`,
  `${canonical}/lexicon.json`, `${canonical}/claim-map.json`, `${canonical}/metadata-delta.json`,
  `${canonical}/independent-handoff-review.md`, `${editorial}/independent-reader-a.md`,
  `${editorial}/independent-reader-b.md`, `${editorial}/REVIEW-STATUS.md`,
  ...keys.map(key => `${canonical}/story/chapters/${key}.json`)];
const tsv = rows => rows.map(row => row.map(v => String(v ?? '').replaceAll('\t', ' ').replaceAll('\n', ' ')).join('\t')).join('\n') + '\n';
const cueRows = [['chapter_key', 'chapter_title', 'scene_id', 'line_id', 'pending_claim_ids', 'narration_verbatim']];
const shotRows = [['chapter_key', 'scene_id', 'template', 'visual', 'camera', 'pending_claim_ids', 'prompt_verbatim']];
const composedScenes = new Map(video.scenes.map(scene => [scene.id, scene]));
assert.equal(composedScenes.size, 50);
const exportedClaims = new Set();
for (const chapter of chapters) for (const scene of chapter.scenes) {
  const composed = composedScenes.get(scene.id);
  assert.ok(composed, `missing composed scene ${scene.id}`);
  assert.deepEqual(composed.lines, scene.lines, `narration mismatch ${scene.id}`);
  assert.deepEqual(composed.data, scene.data, `visual mismatch ${scene.id}`);
  for (const id of composed.claims ?? []) exportedClaims.add(id);
  const ids = (composed.claims ?? []).join(',');
  for (const line of scene.lines ?? []) cueRows.push([chapter.key, chapter.title, scene.id, line.id, ids, line.text]);
  shotRows.push([chapter.key, scene.id, scene.template, scene.data?.visual, scene.data?.camera, ids, scene.data?.prompt]);
}
assert.equal(cueRows.length, 53);
assert.equal(shotRows.length, 51);
assert.equal(exportedClaims.size, 54);
assert.deepEqual([...exportedClaims].sort(), claims.map(c => c.id).sort());
const summary = {
  schema_version: 1,
  status: 'OFFLINE_EXPORT_ONLY_PRODUCTION_HOLD',
  slug: video.slug,
  upstream_sha256: Object.fromEntries(inputs.map(p => [p, hash(bytes(p))])),
  authorization: { host_write: false, paid_generation: false, upload: false },
  existing_review_scope: 'r47 offline narrative PASS and canonical conversion PASS; not historical verification or a worker approval receipt',
  chapter_summary: chapters.map(c => ({ key: c.key, title: c.title, scenes: c.scenes.length,
    lines: c.scenes.flatMap(s => s.lines ?? []).length,
    narration_unicode_codepoints: c.scenes.flatMap(s => s.lines ?? []).reduce((n, l) => n + [...l.text].length, 0),
    pending_claims: c.claims.length })),
  scene_summary: {
    total: video.scenes.length,
    still_shot_scenes: video.scenes.filter(s => s.template === 'shot' && s.data?.visual === 'still').length,
    other_scenes: video.scenes.filter(s => !(s.template === 'shot' && s.data?.visual === 'still')).length,
    // A scene count is not a billable request count: existing assets, retakes, settings and QA must be read back.
    paid_request_count: null,
    paid_request_count_reason: 'Host asset inventory, reuse and bounded retry allowance are not available in this cloud checkout.',
  },
  claims: { pending: 54, plan_linked: 15, passage_only: 39, newly_verified: 0 },
  duration: { actual_body_seconds: null, required_actual_body_seconds: [420, 480],
    gate_passed: false, model_estimates_seconds: { cpm250: 450.4, cpm275: 414.1, cpm300: 383 },
    note: 'A01 compact exception only. Estimates are not TTS, include model assumptions, and must not be labeled actual speech. Do not pad or slow the voice to pass.' },
  budget: { currency: 'USD', all_in_cap: 25, actual_spend: null, remaining: null,
    next_batch_total: null, approved_batch: false,
    required: ['fresh ledger and outstanding reservations', 'provider balance', 'exact model routing and unit prices',
      'bounded text, TTS, images, judges, transcription, music and retries'] },
  publication_metadata_differences: { status: 'DECISION_PENDING',
    count: metadata.metadata_differences.length,
    paths: metadata.metadata_differences.map(d => d.path),
    source: `${canonical}/metadata-delta.json` },
  gates: ['fresh live release, worker, series, slug, locks and asset inventory readback',
    '54 actual claims verified and exact-script independent receipts',
    'guarded canonical chapter adoption without rewriting reviewed narration',
    'whole-batch count and all-in cost approved within remaining USD25 budget',
    'actual narration body 420–480 seconds and audio QA',
    'pictures, final media QA and owner playback', 'owner-selected languages and upload approval'],
};
const outputs = { 'production-status.json': JSON.stringify(summary, null, 2) + '\n',
  'A01-narration-cues.tsv': tsv(cueRows), 'A01-shot-list.tsv': tsv(shotRows) };
const check = process.argv.includes('--check');
for (const [name, value] of Object.entries(outputs)) {
  if (check) assert.equal(readFileSync(path.join(here, name), 'utf8'), value, `stale ${name}`);
  else writeFileSync(path.join(here, name), value);
}
console.log(JSON.stringify({ check, status: summary.status, scenes: shotRows.length - 1,
  narration_lines: cueRows.length - 1, still_shot_scenes: summary.scene_summary.still_shot_scenes,
  pending_claims: claims.length, paid_calls: 0 }));
