#!/usr/bin/env node
// Metadata-only correction: the approved v4 canvas is clear at +5 s, after its CTA transition.
// Never invokes ffmpeg or writes media. Run after rendering: node .../endscreen-timing.mjs --require-all
import { createHash, randomUUID } from 'node:crypto';
import { createReadStream, existsSync, mkdirSync, readFileSync, renameSync, statSync, writeFileSync } from 'node:fs';
import { homedir } from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';
import { parseArgs } from 'node:util';

const { values } = parseArgs({ options: { 'output-root': { type: 'string' }, 'probe-evidence': { type: 'string' }, 'brand-dir': { type: 'string' }, slug: { type: 'string' }, 'require-all': { type: 'boolean' }, 'dry-run': { type: 'boolean' }, 'no-index': { type: 'boolean' } } });
const root = path.resolve(values['output-root'] ?? path.join(homedir(), 'mokaair-work/curio-five-recuts-20261012'));
const evidenceFile = path.resolve(values['probe-evidence'] ?? path.join(root, 'outro-timing-probe/evidence.json'));
const brand = path.resolve(values['brand-dir'] ?? path.join(homedir(), 'mokaair-work/channel-outro-20261012/package-v4/channel'));
const ALLOWED = ['curio-h02', 'curio-u02', 'curio-h03', 'curio-l08', 'curio-h01'];
const OUTRO_SHA = '00eb9ccc8449fa8b47de0aab290b8aa7d55b09962c12a127e0f0c9c5f7834396';
const PROBE_SHA = 'cb93aa6b4384a7a41341bc697f51ec3869584f29362874a2e3dc243ae6e3d6d2';
const CODE = fileURLToPath(import.meta.url);
const read = (p) => JSON.parse(readFileSync(p, 'utf8').replace(/^\uFEFF/, ''));
const bytes = (v) => Buffer.from(`${JSON.stringify(v, null, 2)}\n`);
const hash = (v) => createHash('sha256').update(v).digest('hex');
const need = (ok, message) => { if (!ok) throw new Error(message); };
const inside = (file, dir) => { const r = path.relative(dir, file); return r === '' || (!r.startsWith('..') && !path.isAbsolute(r)); };
async function sha(file) {
  const before = statSync(file), h = createHash('sha256');
  for await (const chunk of createReadStream(file)) h.update(chunk);
  const after = statSync(file);
  need(before.size === after.size && before.mtimeMs === after.mtimeMs, `File changed while hashing: ${file}`);
  return h.digest('hex');
}
function atomic(file, content) {
  const temporary = `${file}.${randomUUID()}.tmp`;
  writeFileSync(temporary, content); renameSync(temporary, file);
}
const evidenceBytes = readFileSync(evidenceFile), evidence = JSON.parse(evidenceBytes);
need(hash(evidenceBytes) === PROBE_SHA, 'Timing evidence changed; review it before changing the explicit expected SHA');
need(evidence.sha256 === OUTRO_SHA && evidence.recommended_start_outro_frame === 150 && evidence.recommended_last_seconds === 16 && evidence.media_changed === false, 'Timing evidence does not identify the accepted v4 +5 second boundary');
const manifest = read(path.join(brand, 'manifest.json'));
need(manifest.package_id === 'mokaair-brand-package-v4-endscreen' && manifest.assets.find((a) => a.role === 'outro')?.sha256 === OUTRO_SHA, 'Wrong branding package');
need(await sha(path.join(brand, 'outro.mp4')) === OUTRO_SHA, 'Approved outro bytes changed');
const probed = spawnSync('ffprobe', ['-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=nb_frames,r_frame_rate,width,height', '-of', 'json', path.join(brand, 'outro.mp4')], { encoding: 'utf8', windowsHide: true });
need(probed.status === 0, `Cannot verify approved outro: ${probed.stderr}`);
const video = JSON.parse(probed.stdout).streams[0];
need(Number(video.nb_frames) === 630 && video.r_frame_rate === '30/1' && video.width === 1920 && video.height === 1080, 'Approved outro format changed');
const selected = values.slug ? [values.slug] : ALLOWED;
need(selected.every((s) => ALLOWED.includes(s)), 'Unknown recut slug');
need(!values['require-all'] || selected.length === 5, '--require-all must select all five episodes');
const plans = [], skipped = [];
for (const slug of selected) {
  const base = path.join(root, slug), upload = path.join(base, 'upload');
  const files = { qa: path.join(base, 'qa.json'), metadata: path.join(upload, 'metadata.json'), setup: path.join(upload, 'endscreen-setup.json'), checksums: path.join(upload, 'checksums.json') };
  if (!existsSync(files.qa) || !read(files.qa).ok) { skipped.push(slug); continue; }
  const beforeBytes = Object.fromEntries(Object.entries(files).map(([k, p]) => [k, readFileSync(p)]));
  const input = Object.fromEntries(Object.entries(beforeBytes).map(([k, data]) => [k, JSON.parse(data)]));
  const { qa, metadata, setup, checksums } = input, total = qa.total_frames;
  need(qa.ok && qa.fps === 30 && qa.outro_frames === 630 && qa.decoded_frames === total && qa.full_av_decode === 'passed', `${slug}: incomplete final QA`);
  need(qa.final_sha256 === metadata.final_sha256 && metadata.video_id === null && metadata.uploaded === false && metadata.published === false, `${slug}: final identity/publication fields changed`);
  need(setup.template_video_id === 'oxEtlA8GWas' && setup.end_frame === total && setup.end_seconds === total / 30 && setup.configured === false && setup.setup_in_youtube_studio_required === true, `${slug}: unexpected endscreen identity/status`);
  need([total - 510, total - 480].includes(setup.start_frame), `${slug}: unexpected earlier endscreen interval`);
  need(JSON.stringify(setup.slots) === JSON.stringify(manifest.outro_source.end_screen_slots), `${slug}: endscreen geometry changed`);
  const media = ['final.mp4', 'dubs/en.wav', 'dubs/ja.wav', 'dubs/ko.wav', 'captions/zh-TW.srt', 'captions/en.srt', 'captions/ja.srt', 'captions/ko.srt'];
  const mediaBefore = {};
  for (const relative of media) {
    const file = path.join(upload, relative), actual = await sha(file);
    need(checksums[relative] === actual, `${slug}: media differs from sealed checksum: ${relative}`);
    mediaBefore[relative] = actual;
  }
  need(mediaBefore['final.mp4'] === qa.final_sha256, `${slug}: final SHA differs from QA`);
  for (const [relative, expected] of Object.entries(checksums)) {
    const file = path.resolve(upload, relative);
    need(inside(file, upload), 'Unsafe checksum path');
    need((mediaBefore[relative] ?? await sha(file)) === expected, `${slug}: package checksum changed: ${relative}`);
  }
  const receiptDir = path.join(base, 'postprocess/endscreen-timing-20261012'), receiptFile = path.join(receiptDir, 'receipt.json');
  const setupNew = {
    ...setup, start_frame: total - 480, start_seconds: total / 30 - 16, duration_seconds: 16,
    outro_start_frame: total - 630, canvas_clear_outro_frame: 150,
    timing_basis: 'Reviewed approved-v4 pixels: CTA transition at +4 seconds; clear slot canvas at +5 seconds.',
    approved_outro_sha256: OUTRO_SHA, timing_probe_sha256: PROBE_SHA,
  };
  const setupBytes = bytes(setupNew), setupSha = hash(setupBytes);
  if (setup.start_frame === total - 480 && metadata.endscreen_setup?.sha256 === hash(beforeBytes.setup) && qa.endscreen_timing?.setup_sha256 === hash(beforeBytes.setup) && existsSync(receiptFile)) {
    const receipt = read(receiptFile);
    need(receipt.ok && receipt.final_sha256 === qa.final_sha256 && receipt.probe_evidence_sha256 === PROBE_SHA && receipt.after.setup === hash(beforeBytes.setup), `${slug}: prior correction receipt does not match`);
    plans.push({ slug, status: 'already-corrected', final_sha256: qa.final_sha256, start_seconds: setup.start_seconds, end_seconds: setup.end_seconds, receipt: receiptFile });
    continue;
  }
  const bound = { file: 'endscreen-setup.json', sha256: setupSha, start_frame: setupNew.start_frame, end_frame: total, start_seconds: setupNew.start_seconds, end_seconds: setupNew.end_seconds, duration_seconds: 16, configured: false };
  const metadataNew = { ...metadata, endscreen_setup: bound };
  const qaNew = { ...qa, endscreen_interval_valid: true, endscreen_timing: { ...bound, setup_sha256: setupSha, approved_outro_sha256: OUTRO_SHA, probe_evidence_sha256: PROBE_SHA, canvas_clear_outro_frame: 150, previous_start_frame: setup.start_frame, previous_start_seconds: setup.start_seconds, metadata_only: true, receipt_file: receiptFile, media_reencoded: false, final_sha256: qa.final_sha256 } };
  const metadataBytes = bytes(metadataNew), qaBytes = bytes(qaNew);
  const checksumsBytes = bytes({ ...checksums, 'metadata.json': hash(metadataBytes), 'endscreen-setup.json': setupSha });
  plans.push({ slug, status: 'planned', final_sha256: qa.final_sha256, start_seconds: setupNew.start_seconds, end_seconds: setupNew.end_seconds, files, beforeBytes, afterBytes: { qa: qaBytes, metadata: metadataBytes, setup: setupBytes, checksums: checksumsBytes }, mediaBefore, upload, receiptDir, receiptFile });
}
need(!values['require-all'] || skipped.length === 0, `Not all five final QAs passed yet: ${skipped.join(', ')}`);
const results = [];
for (const plan of plans) {
  if (plan.status === 'already-corrected' || values['dry-run']) {
    results.push({ slug: plan.slug, status: values['dry-run'] && plan.status === 'planned' ? 'dry-run' : plan.status, final_sha256: plan.final_sha256, start_seconds: plan.start_seconds, end_seconds: plan.end_seconds, duration_seconds: 16 }); continue;
  }
  mkdirSync(path.join(plan.receiptDir, 'before'), { recursive: true });
  const before = Object.fromEntries(Object.entries(plan.beforeBytes).map(([key, data]) => [key, hash(data)]));
  for (const [key, file] of Object.entries(plan.files)) {
    need(hash(readFileSync(file)) === before[key], `${plan.slug}: metadata changed during planning: ${key}`);
    const backup = path.join(plan.receiptDir, 'before', `${key}.json`);
    if (!existsSync(backup)) writeFileSync(backup, plan.beforeBytes[key]);
    else need(hash(readFileSync(backup)) === before[key], `${plan.slug}: an earlier different correction attempt exists`);
  }
  const changed = [];
  try {
    for (const key of ['setup', 'metadata', 'qa', 'checksums']) { atomic(plan.files[key], plan.afterBytes[key]); changed.push(key); }
    const mediaAfter = {};
    for (const [relative, expected] of Object.entries(plan.mediaBefore)) {
      const actual = await sha(path.join(plan.upload, relative));
      need(actual === expected, `${plan.slug}: media changed during metadata-only correction: ${relative}`);
      mediaAfter[relative] = actual;
    }
    const after = Object.fromEntries(Object.entries(plan.files).map(([key, file]) => [key, hash(readFileSync(file))]));
    const receipt = { schema_version: 1, kind: 'curio-endscreen-metadata-only-correction', ok: true, corrected_at: new Date().toISOString(), slug: plan.slug, final_sha256: plan.final_sha256, approved_outro_sha256: OUTRO_SHA, probe_evidence: evidenceFile, probe_evidence_sha256: PROBE_SHA, script_sha256: await sha(CODE), before, after, media_sha256_before: plan.mediaBefore, media_sha256_after: mediaAfter, media_unchanged: true, media_reencoded: false, duration_seconds: 16, start_seconds: plan.start_seconds, end_seconds: plan.end_seconds, youtube_studio_configured: false, uploaded: false, published: false };
    atomic(plan.receiptFile, bytes(receipt));
    results.push({ slug: plan.slug, status: 'corrected', final_sha256: plan.final_sha256, start_seconds: plan.start_seconds, end_seconds: plan.end_seconds, duration_seconds: 16, receipt: plan.receiptFile, media_unchanged: true });
  } catch (error) {
    for (const key of changed.reverse()) atomic(plan.files[key], plan.beforeBytes[key]);
    throw error;
  }
}
console.log(JSON.stringify({ dry_run: !!values['dry-run'], corrections: results, skipped_pending_qa: skipped }, null, 2));
if (!values['dry-run'] && !values['no-index'] && plans.length) {
  const index = spawnSync(process.execPath, [path.join(path.dirname(CODE), 'delivery-index.mjs'), '--output-root', root], { encoding: 'utf8', windowsHide: true });
  process.stdout.write(index.stdout ?? ''); process.stderr.write(index.stderr ?? '');
  need(index.status === 0, 'Metadata correction succeeded but delivery index refresh failed');
}
