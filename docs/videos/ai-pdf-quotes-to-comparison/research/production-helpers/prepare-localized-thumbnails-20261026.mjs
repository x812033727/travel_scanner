// ROOT REVIEW FIRST; preparation helper only until its exact hash is approved.
// Native render --thumbnails-only in a NEW scratch. Never touches the active producer's lease.
import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { isDeepStrictEqual } from 'node:util';

const ROOT = '/workspace/travel_scanner_pdf';
const HOME = '/workspace/work/ai-pdf-01';
const SLUG = 'ai-pdf-quotes-to-comparison';
const ORIGINAL = path.join(HOME, 'media', SLUG);
const PREPARATION = path.join(HOME, 'localized-thumbnail-preparation-20261026');
const BASE = path.join(PREPARATION, 'media');
const WORK = path.join(BASE, SLUG);
const DOC = path.join(ROOT, 'docs/videos', SLUG);
const LOCALES = ['en', 'ja', 'ko', 'es', 'pt', 'id', 'vi', 'th'];
const ART = 'stock/be673375c05932dd665ca14b79030c1fa69b5705c1d582348b31b0eb89a5c7a2.png';
const EXPECTED_SOURCE = 'eac88936fbcb0324208d639b75ddad8f045c6bcc3cc8c4f60d89ebc6c65f3e04';
const EXPECTED_FINAL = '346a5bbd4b47884f301a9dfc9b67fe81e1a504232a0f4746e60ddead54d94e3f';
const SOURCE_PINS = {
  'video.json': EXPECTED_SOURCE,
  'i18n/en.json': '844c953f4842dcb741bc5a5a96db904729f77e3312a41b373f8bcf5a1b44acbc',
  'i18n/ja.json': '4669d500de015f641c9edecb572a300a753e6322e91f80fa3fec68cd26f63351',
  'i18n/ko.json': '5feb043679df63d869b6e884be6e88edf6c263073770ac7976ec94f557fe392e',
  'i18n/es.json': '7ee642cf0a288ce8be2010b68f4b048d8a7becb7f2743401230325d37f3446ea',
  'i18n/pt.json': 'db80b73e876d581d65675139ab96e8d354b0689b1727630ab4546d87fa3c6bd8',
  'i18n/id.json': '78302c5a486dcb63d026a439b1d354846ebdcfa71766a8ff2624435f5288ac05',
  'i18n/vi.json': '938bbba0ac851c8a1d78bb7ce91138afe17d2c057da78b9293451b84def6dd73',
  'i18n/th.json': '8b60ef2931b5eb1308d0e486a8d441239af64fb54c4975d8d17911c1d66cd116',
  'diagrams/pdf-quotes-hero.svg': 'e21e0b90a84b24bbd93985ccd964a224a16645a3daa519a0849af389891e6d4f',
};
const INPUT_PINS = {
  'frames/manifest.json': 'cc1d6a69a57abe7de24111c42c7f8de495906c8a843a441b361a10eea9af4d8d',
  'languages.json': '96a63b6f2ff7f1513b76613f45e7e86d38069fba6cf214c6cc0ad506251462d3',
  [ART]: 'be673375c05932dd665ca14b79030c1fa69b5705c1d582348b31b0eb89a5c7a2',
  'thumbnail.jpg': 'd6a9da0ebf714d71c9adbfd1e99ed0d102121d11acf3e6a6e2e196858399c30c',
  'timeline.json': '226cafffe6e8b6df7d71d2be6ec3a121cff6481bdac2aa16e57cea6d206e9433',
  'final.mp4': EXPECTED_FINAL,
};
const sha = bytes => createHash('sha256').update(bytes).digest('hex');
const digest = file => sha(fs.readFileSync(file));
const read = file => JSON.parse(fs.readFileSync(file, 'utf8'));
const json = value => `${JSON.stringify(value, null, 2)}\n`;
const ensure = (ok, message) => { if (!ok) throw new Error(message); };
const self = path.resolve(process.argv[1]);
if (process.argv.length !== 3 || process.argv[2] !== '--execute') {
  console.log(`ROOT REVIEW FIRST. Native eight-thumbnail preparation only.\nOutput: ${WORK}\nNo original LEASE, body render, paid image, TTS, ASR, model, approval, package, push or upload.`);
  process.exit(process.argv.length === 2 || process.argv[2] === '--help' ? 0 : 2);
}

// Native Chromium routes its fake https://video.local origin to local bytes and
// reports every refused outside request as a layout problem. Do not replace that
// mechanism with a real web page or block Playwright's native local IPC.
const nodeNetworkAttempts = [];
globalThis.fetch = (...args) => { nodeNetworkAttempts.push({ argument_type: typeof args[0] }); throw new Error('Thumbnail preparation forbids Node fetch/provider requests.'); };
process.env.PLAYWRIGHT_BROWSERS_PATH ??= '/workspace/work/ai-animation-01/browsers';
const { main } = await import(`${ROOT}/tools/video/cli.mjs`);
const { openRenderer } = await import(`${ROOT}/tools/video/render/browser.mjs`);
const { localizedThumbnails } = await import(`${ROOT}/tools/video/render/cli.mjs`);
const { renderPlan, renderProblems, sceneAssets, themeHash } = await import(`${ROOT}/tools/video/render/plan.mjs`);
const { fontDir, pageFonts } = await import(`${ROOT}/tools/video/render/fonts.mjs`);
const { acquireProjectLease } = await import(`${ROOT}/tools/video/core/project-lease.mjs`);
const { stopRequested } = await import(`${ROOT}/tools/video/core/paths.mjs`);
const { lintProject, loadProject } = await import(`${ROOT}/tools/video/core/state.mjs`);
const { visualHash } = await import(`${ROOT}/tools/video/core/timeline.mjs`);
const { localizedThumbnailHash, thumbnailSourceHash, thumbnailStatus } = await import(`${ROOT}/tools/video/core/translations.mjs`);
const { THUMB_SIZE } = await import(`${ROOT}/tools/video/templates/templates.mjs`);

function fileRecord(file) {
  const st = fs.lstatSync(file); ensure(st.isFile() && !st.isSymbolicLink(), `Not a regular immutable file: ${file}`);
  return { sha256: digest(file), size: st.size };
}
function tree(dir) {
  const out = {};
  const visit = (at, prefix = '') => {
    for (const e of fs.readdirSync(at, { withFileTypes: true }).sort((a, b) => a.name.localeCompare(b.name))) {
      const rel = prefix ? `${prefix}/${e.name}` : e.name, f = path.join(at, e.name);
      ensure(!e.isSymbolicLink(), `Symlink in protected input tree: ${f}`);
      if (e.isDirectory()) visit(f, rel); else out[rel] = fileRecord(f);
    }
  };
  visit(dir); return out;
}
function verifyPins() {
  for (const [rel, h] of Object.entries(SOURCE_PINS)) ensure(digest(path.join(DOC, rel)) === h, `Source changed: ${rel}; stop rather than render mixed versions.`);
  for (const [rel, h] of Object.entries(INPUT_PINS)) ensure(digest(path.join(ORIGINAL, rel)) === h, `Immutable original input changed: ${rel}`);
}
function jpegShape(bytes) {
  ensure(bytes[0] === 0xff && bytes[1] === 0xd8, 'Native capture is not a JPEG.');
  let i = 2;
  while (i + 8 < bytes.length) {
    ensure(bytes[i++] === 0xff, 'Invalid JPEG marker.');
    while (bytes[i] === 0xff) i++;
    const marker = bytes[i++];
    if (marker === 0xd9 || marker === 0xda) break;
    if (marker === 0x01 || marker >= 0xd0 && marker <= 0xd7) continue;
    const length = bytes.readUInt16BE(i); ensure(length >= 2 && i + length <= bytes.length, 'Invalid JPEG segment.');
    if ([0xc0, 0xc1, 0xc2, 0xc3, 0xc5, 0xc6, 0xc7, 0xc9, 0xca, 0xcb, 0xcd, 0xce, 0xcf].includes(marker))
      return { width: bytes.readUInt16BE(i + 5), height: bytes.readUInt16BE(i + 3), components: bytes[i + 7] };
    i += length;
  }
  throw new Error('JPEG has no supported frame dimensions.');
}

ensure(!fs.existsSync(PREPARATION), 'One-use preparation already exists; inspect it, NEVER overwrite or replay.');
ensure(fs.realpathSync(HOME) === HOME && fs.realpathSync(ORIGINAL) === ORIGINAL, 'Unsafe original/base path.');
verifyPins();
const project = loadProject({ slug: SLUG, root: ROOT }), lint = lintProject(project);
ensure(lint.errors.length === 0, 'Actual current source does not pass lint.');
ensure(project.doc.thumbnail?.data?.asset === ART && project.doc.scenes.every(s => sceneAssets(s).length === 0)
  && !project.doc.thumbnail.data.capture && !project.doc.thumbnail.data.shot && !project.doc.thumbnail.variants,
  'Unexpected scene/capture/keyframe/variant dependency; review its actual inputs first.');
const oldManifest = read(path.join(ORIGINAL, 'frames/manifest.json'));
ensure(oldManifest.visual_hash === visualHash(project.doc), 'Primary frames manifest is stale.');
const languages = read(path.join(ORIGINAL, 'languages.json'));
assert.deepEqual(Object.keys(languages.locales).sort(), [...LOCALES].sort());
ensure(LOCALES.every(l => ['metadata', 'captions', 'dub'].every(p => languages.locales[l][p] === true)), 'Actual eight-language choice differs.');
ensure(thumbnailSourceHash(project.doc) === '12bdfb50a92a' && LOCALES.every(l => thumbnailStatus(project.doc, project.translations[l]) === 'current'), 'Thumbnail source words are stale or absent.');
const fontRoots = Object.fromEntries([...new Set(LOCALES.flatMap(pageFonts))].map(name => [name, fs.realpathSync(fontDir(name))]));
const immutable = () => ({
  original_frames: tree(path.join(ORIGINAL, 'frames')), original_stock: tree(path.join(ORIGINAL, 'stock')),
  source_files: Object.fromEntries(Object.keys(SOURCE_PINS).map(rel => [rel, fileRecord(path.join(DOC, rel))])),
  original_inputs: Object.fromEntries(Object.keys(INPUT_PINS).map(rel => [rel, fileRecord(path.join(ORIGINAL, rel))])),
  native_renderer: tree(path.join(ROOT, 'tools/video/render')), native_templates: tree(path.join(ROOT, 'tools/video/templates')),
  native_core: tree(path.join(ROOT, 'tools/video/core')), native_cli: fileRecord(path.join(ROOT, 'tools/video/cli.mjs')),
  shelf_lexicon: fileRecord(path.join(ROOT, 'docs/videos/lexicon.json')),
  font_packages: Object.fromEntries(Object.entries(fontRoots).map(([name, dir]) => [name, { directory: dir, files: tree(dir) }])),
  helper: fileRecord(self),
});
const before = immutable(), started = new Date().toISOString();
let lease = null;
const captures = [], nativeLog = [];
try {
  fs.mkdirSync(PREPARATION); // Exclusive one-use root; never removed on failure.
  fs.mkdirSync(WORK, { recursive: true });
  lease = acquireProjectLease(WORK, { owner: 'localized-thumbnail-preparation-only' });
  const verify = () => { lease.verify(); ensure(!stopRequested(PREPARATION) && !stopRequested(WORK), 'STOP holds thumbnail preparation.'); };
  const write = (rel, bytes) => { verify(); const f = path.join(PREPARATION, rel); ensure(!path.relative(PREPARATION, f).startsWith('..'), 'Output escapes preparation.'); fs.mkdirSync(path.dirname(f), { recursive: true }); fs.writeFileSync(f, bytes, { flag: 'wx', mode: 0o600 }); };
  write('ONE_USE_ADMISSION.NOT_ADOPTED.json', json({ started_at_utc: started, pid: process.pid, helper_sha256: digest(self), workdir: WORK,
    status: 'LOCAL THUMBNAIL PREPARATION ONLY / NOT ADOPTED', original_project_lease_acquired: false,
    original_auto_audio_checks_expected_to_change_legitimately: true, original_project_tree_unchanged_claimed: false }));
  write('immutable-inputs.before.json', json(before));
  for (const rel of ['frames/manifest.json', 'languages.json', ART]) {
    verify(); const to = path.join(WORK, rel); fs.mkdirSync(path.dirname(to), { recursive: true });
    fs.copyFileSync(path.join(ORIGINAL, rel), to, fs.constants.COPYFILE_EXCL);
    ensure(digest(to) === INPUT_PINS[rel], `Copied input differs: ${rel}`);
  }
  const dataProblems = renderProblems(project.doc, ROOT, { workdir: WORK });
  ensure(dataProblems.length === 0, 'Native renderProblems rejected current thumbnail/source/assets.');
  const plan = renderPlan(project.doc, themeHash(), ROOT, { translations: project.translations, workdir: WORK });
  const localized = localizedThumbnails(plan);
  ensure(localized.drawable.length === 8 && Object.keys(localized.gaps).length === 0
    && isDeepStrictEqual(localized.drawable.map(p => p.locale).sort(), [...LOCALES].sort()), 'Native coverage/translation check did not accept all eight current thumbnails.');
  const ownByKey = new Map(localized.drawable.map(p => [p.key, p]));
  const observedRenderer = async options => {
    verify(); ensure(options.root === ROOT && options.workdir === WORK, 'Native renderer points outside scratch.');
    const renderer = await openRenderer(options);
    return { ...renderer, capture: async (key, html, options) => {
      verify(); const own = ownByKey.get(key);
      ensure(own && own.html === html && options.type === 'jpeg' && isDeepStrictEqual(options.size, THUMB_SIZE), 'Native renderer tried a body/primary/unknown capture.');
      const actual = await renderer.capture(key, html, options); verify();
      const shape = jpegShape(actual.still);
      captures.push({ locale: own.locale, native_key: key, native_thumbnail_hash: own.hash, html_sha256: sha(html),
        source_thumbnail_hash: thumbnailSourceHash(project.doc), translation_sha256: SOURCE_PINS[`i18n/${own.locale}.json`],
        native_layout_font_image_and_brand_problems: [...actual.problems], jpeg_shape: shape, jpeg_sha256: sha(actual.still), bytes: actual.still.length });
      return actual; // Return the genuine native result unchanged; failed fits stay failed.
    }, close: async () => { await renderer.close(); } };
  };
  const out = { write(text) { nativeLog.push(String(text)); process.stdout.write(text); } };
  verify(); verifyPins();
  const code = await main(['render', '--slug', SLUG, '--thumbnails-only'], {
    root: ROOT, here: path.join(ROOT, 'tools/video'), env: { ...process.env, VIDEO_WORKDIR: BASE },
    stdout: out, stderr: out, openRenderer: observedRenderer,
  });
  verify(); write('native-render.log', nativeLog.join('')); write('actual-captures.json', json(captures));
  ensure(code === 0, `Native render genuinely failed with exit${code}; preserve this one-use scratch.`);
  const updated = read(path.join(WORK, 'frames/manifest.json'));
  const kept = m => { const x = { ...m }; delete x.thumbnail_locales; delete x.thumbnail_locale_gaps; return x; };
  ensure(isDeepStrictEqual(kept(updated), kept(oldManifest)), 'Native render changed a primary frame/body manifest field.');
  ensure(Object.keys(updated.thumbnail_locale_gaps ?? {}).length === 0
    && isDeepStrictEqual(Object.keys(updated.thumbnail_locales ?? {}).sort(), [...LOCALES].sort()), 'Native result is missing/failed at least one language.');
  ensure(captures.length === 8 && new Set(captures.map(c => c.locale)).size === 8, 'Actual renderer did not capture exactly eight foreign thumbnails.');
  for (const locale of LOCALES) {
    const row = captures.find(c => c.locale === locale), recorded = updated.thumbnail_locales[locale], f = path.join(WORK, recorded.file);
    ensure(row.native_layout_font_image_and_brand_problems.length === 0 && row.jpeg_shape.width === 1280 && row.jpeg_shape.height === 720
      && row.bytes <= 2 * 1024 * 1024 && digest(f) === row.jpeg_sha256 && recorded.file === `thumbnails/${locale}.jpg`
      && recorded.hash === localizedThumbnailHash(project.doc, project.translations[locale]), `${locale} actual native thumbnail proof failed.`);
  }
  ensure(fs.readdirSync(path.join(WORK, 'frames')).join(',') === 'manifest.json' && !fs.existsSync(path.join(WORK, 'thumbnail.jpg'))
    && !fs.existsSync(path.join(WORK, 'final.mp4')) && !fs.existsSync(path.join(WORK, 'auto.json')) && !fs.existsSync(path.join(WORK, 'approvals.json')),
    'An unexpected primary/body/approval artifact was created in scratch.');
  verifyPins(); const after = immutable();
  ensure(isDeepStrictEqual(after, before), 'An immutable source/frame/art/font/native input changed; preparation is not adoptable.');
  ensure(nodeNetworkAttempts.length === 0, 'Node attempted an outside/provider fetch.');
  write('immutable-inputs.after.json', json(after));
  write('result.NOT_ADOPTED.json', json({ schema_version: 1, started_at_utc: started, finished_at_utc: new Date().toISOString(),
    status: 'EIGHT LOCALIZED THUMBNAILS PREPARED / NOT ADOPTED', native_command: 'render --thumbnails-only', native_exit_code: code,
    workdir: WORK, source_sha256: EXPECTED_SOURCE, approved_primary_final_sha256: EXPECTED_FINAL,
    actual_captures: captures, native_thumbnail_gaps: updated.thumbnail_locale_gaps ?? {}, primary_manifest_fields_preserved: true,
    immutable_input_manifests_equal: true, original_project_lease_acquired: false, original_project_written_by_this_helper: false,
    original_auto_audio_check_files_not_frozen_or_claimed_unchanged: true, copied_inputs: ['frames/manifest.json', 'languages.json', ART],
    body_PNGs_copied_or_redrawn: 0, primary_thumbnail_redrawn: false, synthesized_images: 0, TTS_ASR_model_requests: 0,
    original_final_or_audio_approval_changed: false, owner_action_or_upload_or_publication: false, node_network_attempts: nodeNetworkAttempts,
    browser_asset_policy: 'Unmodified native openRenderer routes fake video.local pages/fonts/theme/stock from disk; refused requests are genuine capture problems and fail this helper.',
    mobile_legibility_and_visual_review_pending: true, native_geometry_scope: '1280x720 settled JPEG fit/overflow/font/image/brand mechanics; no automated claim of mobile legibility.',
    next: 'Root independently view the actual eight JPEGs at full and mobile display size. Preserve NOT ADOPTED; only at a safe normal producer boundary consider native adoption of the exact thumbnails after current source/hash revalidation. No source, lease, paid unit, voice gate, package, owner choice, upload or publication is completed by this preparation.' }));
  verify();
  console.log(json({ result: path.join(PREPARATION, 'result.NOT_ADOPTED.json'), result_sha256: digest(path.join(PREPARATION, 'result.NOT_ADOPTED.json')),
    thumbnails: captures.map(c => ({ locale: c.locale, sha256: c.jpeg_sha256, shape: c.jpeg_shape })), immutable_inputs_unchanged: true, original_project_written: false, adopted: false }));
} catch (error) {
  console.error(`Thumbnail preparation stopped: ${error.message}. Keep the one-use directory; never overwrite or blindly replay it.`);
  process.exitCode = 1;
} finally { lease?.release(); }
