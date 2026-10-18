// Offline comparison only. Reads a caller-supplied immutable A01 capture and
// frozen r11 candidate; writes only this package's report with --write.
import fs from 'node:fs';
import path from 'node:path';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const pilot = path.resolve(here, '../..');
const r11 = path.resolve(here, '../A01-editorial-candidate-20261018-r11');
const readback = path.resolve(here, '../A01-pinned-lexicon-transition-candidate-20261017/actual-104-readback-20261017.json');
const storyModule = path.resolve(pilot, '../../../tools/video/automation/story.mjs');
const slug = 'story-rolling-suitcase-v2';
const keys = ['hook', 'origin', 'idea', 'engine', 'turn', 'now'];
const pins = {
  manifest: '39bcc9e69c4d89eea044e145abb592c587183796e92bb13646c83f82511d289a',
  r11_review: '2ed2f086af582ea75dde7abfdf43fb032d3fa7da2feb3917b249c7c890d774ac',
  r11_review_addendum: 'ed0c8932dbe71440cce9e7a3e6d55ec791ef2785010b53f282357c52ceddf1d7',
  verified_104: '29ddbe75e849f09fed508b3c1405fd533445aa8adee337539cb11ea9287460aa',
  readback_104: '70f7ea78a198c7ae593d3668c52f6ffea3ec7316072f0d35df04ffd63a7ae3d1',
  inventory_104: '827361fe4f8d89cbc3c211af5df91de1bbcb09ae8b4ffd6acf534b4465dfd6d3',
  source_104: 'e1499cd695f2f414d9379a8917b6b5b36e50ea0d046de495938157d8ff97add7',
};

const sha = (bytes) => createHash('sha256').update(bytes).digest('hex');
const json = (value) => Buffer.from(JSON.stringify(value, null, 2) + '\n');
function gate(ok, code) { if (!ok) throw new Error(code); }
function readFile(file, code) {
  gate(fs.existsSync(file) && fs.lstatSync(file).isFile() && !fs.lstatSync(file).isSymbolicLink(), code);
  try { return fs.readFileSync(file); } catch { throw new Error(code); }
}
function parse(bytes, code) {
  try { return JSON.parse(bytes); } catch { throw new Error(code); }
}
function inventory(root) {
  gate(path.isAbsolute(root) && fs.existsSync(root) && fs.lstatSync(root).isDirectory(), 'LOCAL_SNAPSHOT_REQUIRED');
  const entries = [];
  function walk(dir, relative = '') {
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      const rel = relative ? `${relative}/${entry.name}` : entry.name;
      const full = path.join(dir, entry.name);
      const stat = fs.lstatSync(full);
      gate(!stat.isSymbolicLink(), 'SNAPSHOT_SYMLINK_REFUSED');
      if (stat.isDirectory()) walk(full, rel);
      else {
        gate(stat.isFile(), 'SNAPSHOT_NONFILE_REFUSED');
        entries.push([rel, sha(fs.readFileSync(full))]);
      }
    }
  }
  walk(root);
  entries.sort((a, b) => a[0] < b[0] ? -1 : a[0] > b[0] ? 1 : 0);
  return { files: entries.length, sha256: sha(Buffer.from(entries.map(([rel, hash]) => `${rel}\0${hash}\n`).join(''))) };
}
function sceneSet(scenes, code) {
  const map = new Map();
  for (const scene of scenes) {
    gate(typeof scene?.id === 'string' && !map.has(scene.id), code);
    map.set(scene.id, scene);
  }
  return map;
}
function lineSet(scenes, code) {
  const map = new Map();
  for (const scene of scenes) for (const line of scene.lines ?? []) {
    gate(typeof line?.id === 'string' && !map.has(line.id), code);
    map.set(line.id, line);
  }
  return map;
}
function ids(scenes, field) {
  return [...new Set(scenes.flatMap((scene) => scene[field] ?? []))].sort();
}
function diff(before, after, changed = () => false) {
  const oldIds = new Set(before.keys()), newIds = new Set(after.keys());
  return {
    retained: [...oldIds].filter((id) => newIds.has(id)).sort(),
    added: [...newIds].filter((id) => !oldIds.has(id)).sort(),
    removed: [...oldIds].filter((id) => !newIds.has(id)).sort(),
    changed: [...oldIds].filter((id) => newIds.has(id) && changed(before.get(id), after.get(id))).sort(),
  };
}
function urls(rows, code) {
  gate(Array.isArray(rows), code);
  const map = new Map();
  for (const row of rows) {
    gate(typeof row?.url === 'string' && row.url.startsWith('https://') && !map.has(row.url), code);
    map.set(row.url, row);
  }
  return map;
}
function claimsMarkdown(bytes, code, { requireSource = true } = {}) {
  const rows = new Map();
  for (const [index, line] of bytes.toString('utf8').split(/\r?\n/).entries()) {
    if (!line.includes('｜')) continue;
    const parts = line.split('｜');
    gate(parts.length === 6, `${code}_LINE_${index + 1}`);
    const [id, claim, url, checked, scene, verdict] = parts;
    const sourceShape = (url.startsWith('https://') && /^\d{4}-\d{2}-\d{2}$/.test(checked)) || (!requireSource && url === '' && checked === '');
    gate(/^[a-z][a-z0-9]*$/.test(id) && claim && sourceShape && scene && verdict && !rows.has(id), `${code}_LINE_${index + 1}`);
    rows.set(id, { claim, url, checked, scene, verdict });
  }
  gate(rows.size > 0, code);
  return rows;
}
const displayCell = (value) => String(value).replace(/[|｜\n]/g, '／');
function claimChangeDetails(before, after) {
  const both = [...before.keys()].filter((id) => after.has(id)).sort();
  const fields = ['claim', 'url', 'checked', 'scene', 'verdict'];
  const differences = Object.fromEntries(fields.map((field) => [field, both.filter((id) => before.get(id)[field] !== after.get(id)[field])]));
  return {
    text_changed: differences.claim,
    source_url_changed: differences.url,
    source_checked_date_changed: differences.checked,
    scene_changed: differences.scene,
    verdict_changed: differences.verdict,
    semantic_or_source_changed: both.filter((id) => fields.slice(0, 4).some((field) => before.get(id)[field] !== after.get(id)[field])),
    old_source_missing_requires_reverification: both.filter((id) => !before.get(id).url),
  };
}
function lineLocations(scenes, code) {
  const lines = new Map();
  for (const scene of scenes) {
    const chapter = keys.find((key) => scene.id.startsWith(`${key}-`));
    gate(chapter, code);
    for (const line of scene.lines ?? []) {
      gate(typeof line?.id === 'string' && !lines.has(line.id), code);
      lines.set(line.id, { chapter, scene: scene.id, text: line.text });
    }
  }
  return lines;
}
function compare(snapshot, verifiedFile) {
  const inv = inventory(snapshot);
  gate(inv.files === 254, 'SNAPSHOT_FILE_COUNT_DRIFT');
  gate(inv.sha256 === pins.inventory_104, `SNAPSHOT_INVENTORY_DRIFT:${inv.sha256}`);

  const verifiedBytes = readFile(verifiedFile, 'VERIFIED_RECEIPT_MISSING');
  gate(sha(verifiedBytes) === pins.verified_104, 'VERIFIED_RECEIPT_DRIFT');
  const verified = parse(verifiedBytes, 'VERIFIED_RECEIPT_INVALID');
  const readbackBytes = readFile(readback, 'READBACK_RECEIPT_MISSING');
  gate(sha(readbackBytes) === pins.readback_104, 'READBACK_RECEIPT_DRIFT');
  const actual = parse(readbackBytes, 'READBACK_RECEIPT_INVALID');
  gate(verified.integrity === 'ACTUAL_REVIEW_PROGRESS_CHAIN_PASS' && verified.links === 104 && verified.source_sha256 === pins.source_104, 'VERIFIED_104_MISMATCH');
  gate(actual.integrity === verified.integrity && actual.links === verified.links && actual.source_sha256 === verified.source_sha256 && actual.production_status === 'HOLD', 'READBACK_104_MISMATCH');

  const manifestBytes = readFile(path.join(r11, 'manifest.json'), 'R11_MANIFEST_MISSING');
  gate(sha(manifestBytes) === pins.manifest, 'R11_MANIFEST_DRIFT');
  const manifest = parse(manifestBytes, 'R11_MANIFEST_INVALID');
  gate(manifest.slug === slug && manifest.authorizes_host_install_or_paid_media === false, 'R11_MANIFEST_SCOPE');
  for (const [rel, expected] of Object.entries(manifest.outputs_sha256)) {
    gate(sha(readFile(path.join(r11, rel), 'R11_OUTPUT_MISSING')) === expected, 'R11_OUTPUT_DRIFT');
  }
  const reviewBytes = readFile(path.join(r11, 'independent-full-review-20261018.md'), 'R11_REVIEW_MISSING');
  gate(sha(reviewBytes) === pins.r11_review, 'R11_REVIEW_DRIFT');
  gate(reviewBytes.toString('utf8').includes('PASS_OFFLINE_WITH_P2_NOTES'), 'R11_REVIEW_STATUS_DRIFT');
  const addendumBytes = readFile(path.join(r11, 'independent-full-review-addendum-20261018.md'), 'R11_REVIEW_ADDENDUM_MISSING');
  gate(sha(addendumBytes) === pins.r11_review_addendum, 'R11_REVIEW_ADDENDUM_DRIFT');
  gate(addendumBytes.toString('utf8').includes('HOLD_P1_N14') && addendumBytes.toString('utf8').includes('PASS_OFFLINE_WITH_P2_NOTES'), 'R11_REVIEW_ADDENDUM_STATUS_DRIFT');

  const fromCapture = (rel) => readFile(path.join(snapshot, ...rel.split('/')), 'SNAPSHOT_SOURCE_MISSING');
  const oldVideo = parse(fromCapture(`docs/videos/${slug}/video.json`), 'SNAPSHOT_VIDEO_INVALID');
  const oldSeries = parse(fromCapture(`docs/videos/${slug}/series.json`), 'SNAPSHOT_SERIES_INVALID');
  const auto = parse(fromCapture(`${slug}/auto.json`), 'SNAPSHOT_AUTO_INVALID');
  const newVideo = parse(readFile(path.join(r11, 'candidate/video.json'), 'R11_VIDEO_MISSING'), 'R11_VIDEO_INVALID');
  const newSeries = parse(readFile(path.join(r11, 'candidate/series.json'), 'R11_SERIES_MISSING'), 'R11_SERIES_INVALID');
  const sourceMap = parse(readFile(path.join(r11, 'source-map.json'), 'R11_SOURCE_MAP_MISSING'), 'R11_SOURCE_MAP_INVALID');
  gate(oldVideo.slug === slug && newVideo.slug === slug && oldSeries.slug === 'brand-stories-curio-pilot-v2' && newSeries.slug === oldSeries.slug, 'A01_IDENTITY_MISMATCH');
  gate(JSON.stringify(oldVideo.target_minutes) === '[9,11]' && JSON.stringify(newVideo.target_minutes) === '[7,8]', 'DURATION_DECISION_DRIFT');
  gate(oldSeries.target_minutes === 10 && newSeries.target_minutes === 10 && auto.target_minutes === 10, 'SERIES_DURATION_DRIFT');
  gate(oldVideo.look?.preset === 'cute-mystery' && newVideo.look?.preset === 'cute-mystery', 'LOOK_DRIFT');

  const oldScenes = sceneSet(oldVideo.scenes, 'OLD_SCENE_ID_INVALID');
  const newScenes = sceneSet(newVideo.scenes, 'NEW_SCENE_ID_INVALID');
  const beforeChapters = {};
  for (const key of keys) {
    const chapter = parse(fromCapture(`${slug}/story/chapters/${key}.json`), 'SNAPSHOT_CHAPTER_INVALID');
    gate(chapter.key === key && Array.isArray(chapter.scenes), 'SNAPSHOT_CHAPTER_SHAPE');
    beforeChapters[key] = chapter;
  }
  const oldChapterIds = keys.flatMap((key) => beforeChapters[key].scenes.map((scene) => scene.id));
  gate(oldChapterIds.length === oldScenes.size && new Set(oldChapterIds).size === oldScenes.size && oldChapterIds.every((id) => oldScenes.has(id)), 'OLD_CHAPTER_VIDEO_SCENES_MISMATCH');
  const oldChapterSceneMap = sceneSet(keys.flatMap((key) => beforeChapters[key].scenes), 'OLD_CHAPTER_SCENE_ID_DUPLICATE');
  // composeStory enriches each persisted chapter scene with chapter/claim metadata.
  // Compare the underlying chapter content, not those expected derived fields.
  const oldMergedSceneDifference = diff(oldChapterSceneMap, oldScenes, (a, b) => {
    const { chapter, claims, ...originalScene } = b;
    return JSON.stringify(a) !== JSON.stringify(originalScene);
  });
  gate([...newScenes.keys()].every((id) => keys.some((key) => id.startsWith(`${key}-`))), 'NEW_CHAPTER_SCENE_ID_UNKNOWN');

  const oldClaimRows = claimsMarkdown(fromCapture(`docs/videos/${slug}/claims.md`), 'SNAPSHOT_CLAIMS_MARKDOWN_INVALID', { requireSource: false });
  const oldDeclaredClaims = new Map();
  for (const key of keys) for (const row of beforeChapters[key].claims ?? []) {
    const hasSource = Number.isInteger(row.source);
    const source = hasSource ? oldVideo.sources?.[row.source] : null;
    const planSource = hasSource ? oldSeries.plan?.sources?.[row.source] : null;
    gate(typeof row.id === 'string' && !oldDeclaredClaims.has(row.id) && (!hasSource || (source?.url && source?.checked_on && planSource?.url === source.url && planSource?.checked === source.checked_on)), 'SNAPSHOT_CLAIM_SOURCE_UNVERIFIABLE');
    oldDeclaredClaims.set(row.id, {
      claim: displayCell(row.claim), url: source?.url ?? '', checked: source?.checked_on ?? '',
      scene: row.scene, verdict: row.verdict ?? '待查',
    });
  }
  gate(oldClaimRows.size === oldDeclaredClaims.size, 'SNAPSHOT_CLAIM_ROW_GAP');
  for (const [id, row] of oldDeclaredClaims) gate(JSON.stringify(oldClaimRows.get(id)) === JSON.stringify(row), 'SNAPSHOT_CLAIM_ROW_DRIFT');

  const newClaimRows = claimsMarkdown(readFile(path.join(r11, 'candidate/claims.md'), 'R11_CLAIMS_MISSING'), 'R11_CLAIMS_MARKDOWN_INVALID', { requireSource: false });
  const newClaimRefs = new Map();
  for (const scene of newVideo.scenes) for (const id of scene.claims ?? []) {
    gate(typeof id === 'string' && !newClaimRefs.has(id), 'R11_CLAIM_REF_DUPLICATE');
    newClaimRefs.set(id, scene.id);
  }
  gate(newClaimRows.size === newClaimRefs.size, 'R11_CLAIM_ROW_GAP');
  for (const [id, scene] of newClaimRefs) {
    const row = newClaimRows.get(id);
    gate(row?.scene === scene && row.verdict === 'PENDING', 'R11_CLAIM_UNVERIFIABLE');
  }
  const newUnsourcedClaimIds = [...newClaimRows].filter(([, row]) => !row.url).map(([id]) => id).sort();
  gate(JSON.stringify(newUnsourcedClaimIds) === '["n14"]', 'R11_UNSOURCED_CLAIMS_DRIFT');

  const chapters = keys.map((key) => {
    const before = beforeChapters[key];
    const afterScenes = newVideo.scenes.filter((scene) => scene.id.startsWith(`${key}-`));
    const oldMap = sceneSet(before.scenes, 'OLD_CHAPTER_SCENE_DUPLICATE');
    const newMap = sceneSet(afterScenes, 'NEW_CHAPTER_SCENE_DUPLICATE');
    const oldLines = lineSet(before.scenes, 'OLD_CHAPTER_LINE_DUPLICATE');
    const newLines = lineSet(afterScenes, 'NEW_CHAPTER_LINE_DUPLICATE');
    const oldClaims = new Map((before.claims ?? []).map((row) => [row.id, oldClaimRows.get(row.id)]));
    gate(oldClaims.size === (before.claims ?? []).length && [...oldClaims.values()].every(Boolean), 'OLD_CLAIM_ID_DUPLICATE');
    const newClaims = new Map(ids(afterScenes, 'claims').map((id) => [id, newClaimRows.get(id)]));
    gate([...newClaims.values()].every(Boolean), 'R11_CHAPTER_CLAIM_ROW_GAP');
    const sceneContentChanged = (a, b) => {
      const { chapter, claims, ...candidateScene } = b;
      return JSON.stringify(a) !== JSON.stringify(candidateScene);
    };
    return {
      key,
      before: { scenes: before.scenes.length, lines: oldLines.size, declared_claims: oldClaims.size, chapter_sha256: sha(fromCapture(`${slug}/story/chapters/${key}.json`)) },
      r11: { scenes: afterScenes.length, lines: newLines.size, scene_claim_refs: newClaims.size },
      scene_ids: diff(oldMap, newMap, sceneContentChanged),
      line_ids: diff(oldLines, newLines, (a, b) => a.text !== b.text),
      claim_ids: diff(oldClaims, newClaims, (a, b) => JSON.stringify(a) !== JSON.stringify(b)),
      claim_change_details: claimChangeDetails(oldClaims, newClaims),
    };
  });
  const oldLineLocations = lineLocations(oldVideo.scenes, 'OLD_GLOBAL_LINE_DUPLICATE');
  const newLineLocations = lineLocations(newVideo.scenes, 'R11_GLOBAL_LINE_DUPLICATE');
  const retainedLineIds = [...oldLineLocations.keys()].filter((id) => newLineLocations.has(id)).sort();
  const globalLineContinuity = {
    retained_ids: retainedLineIds,
    moved_chapter: retainedLineIds.filter((id) => oldLineLocations.get(id).chapter !== newLineLocations.get(id).chapter).map((id) => ({ id, from: { chapter: oldLineLocations.get(id).chapter, scene: oldLineLocations.get(id).scene }, to: { chapter: newLineLocations.get(id).chapter, scene: newLineLocations.get(id).scene } })),
    moved_scene: retainedLineIds.filter((id) => oldLineLocations.get(id).scene !== newLineLocations.get(id).scene).map((id) => ({ id, from: { chapter: oldLineLocations.get(id).chapter, scene: oldLineLocations.get(id).scene }, to: { chapter: newLineLocations.get(id).chapter, scene: newLineLocations.get(id).scene } })),
    text_changed: retainedLineIds.filter((id) => oldLineLocations.get(id).text !== newLineLocations.get(id).text),
  };
  const globalClaimContinuity = {
    claim_ids: diff(oldClaimRows, newClaimRows, (a, b) => JSON.stringify(a) !== JSON.stringify(b)),
    claim_change_details: claimChangeDetails(oldClaimRows, newClaimRows),
  };

  const oldSources = urls(oldVideo.sources, 'OLD_PUBLIC_SOURCE_INVALID');
  const newSources = urls(newVideo.sources, 'R11_PUBLIC_SOURCE_INVALID');
  const planSources = urls(newSeries.plan?.sources, 'R11_PLAN_SOURCE_INVALID');
  const citedSources = urls(sourceMap.source_index, 'R11_CITED_SOURCE_INVALID');
  gate(newSources.size === citedSources.size && [...newSources.keys()].every((url) => citedSources.has(url)), 'R11_CITED_PUBLIC_SOURCE_DRIFT');
  const citedClaims = new Map();
  for (const [url, row] of citedSources) for (const id of row.claim_ids ?? []) {
    gate(typeof id === 'string' && !citedClaims.has(id), 'R11_SOURCE_MAP_CLAIM_DUPLICATE');
    citedClaims.set(id, url);
  }
  gate(citedClaims.size === newClaimRows.size - newUnsourcedClaimIds.length, 'R11_SOURCE_MAP_CLAIM_GAP');
  for (const [id, row] of newClaimRows) {
    if (!row.url) gate(!citedClaims.has(id), 'R11_UNSOURCED_CLAIM_MAPPED');
    else gate(citedClaims.get(id) === row.url && /^\d{4}-\d{2}-\d{2}$/.test(newSources.get(row.url)?.checked_on ?? '') && newSources.get(row.url).checked_on >= row.checked, `R11_CLAIM_SOURCE_UNVERIFIABLE_${id}`);
  }
  const sourceDiff = diff(oldSources, newSources, (a, b) => a.title !== b.title || a.checked_on !== b.checked_on);
  const publicMissingFromPlan = [...newSources.keys()].filter((url) => !planSources.has(url)).sort();
  const planExtra = [...planSources.keys()].filter((url) => !newSources.has(url)).sort();
  const moduleBytes = readFile(storyModule, 'LOCAL_STORY_MODULE_MISSING');
  const remergeCurrent = moduleBytes.toString('utf8').includes('sources: plan.sources.map((source) =>');

  return {
    schema_version: 1,
    status: 'OFFLINE_DIFF_ONLY_HOLD',
    snapshot_proof: { links: 104, source_sha256: pins.source_104, file_count: inv.files, inventory_sha256: inv.sha256, verified_report_sha256: pins.verified_104, readback_sha256: pins.readback_104 },
    candidate_proof: { r11_manifest_sha256: pins.manifest, independent_review_sha256: pins.r11_review, independent_review_addendum_sha256: pins.r11_review_addendum, original_offline_review_result: 'PASS_OFFLINE_WITH_P2_NOTES', formal_factual_gate: 'HOLD_P1_N14', local_story_module_sha256: sha(moduleBytes) },
    identity: { slug, series: oldSeries.slug, episode: auto.series?.episode, look: newVideo.look?.preset },
    duration: { before_body_target_minutes: oldVideo.target_minutes, r11_body_target_minutes: newVideo.target_minutes, series_target_minutes: newSeries.target_minutes, saved_auto_target_minutes: auto.target_minutes, intro_and_outro_not_body_seconds: [5, 21] },
    totals: { before_scenes: oldScenes.size, r11_scenes: newScenes.size, before_lines: lineSet(oldVideo.scenes, 'OLD_LINE_ID_DUPLICATE').size, r11_lines: lineSet(newVideo.scenes, 'NEW_LINE_ID_DUPLICATE').size, before_claim_rows: oldClaimRows.size, r11_claim_rows: newClaimRows.size },
    capture_chapter_to_merged_scene_difference: oldMergedSceneDifference,
    global_line_continuity: globalLineContinuity,
    global_claim_continuity: globalClaimContinuity,
    chapters,
    sources: { before_public_count: oldSources.size, r11_public_count: newSources.size, r11_cited_count: citedSources.size, r11_plan_count: planSources.size, public_url_difference: sourceDiff, r11_public_missing_from_plan: publicMissingFromPlan, plan_would_remerge_extra_urls: planExtra, r11_unsourced_pending_claim_ids: newUnsourcedClaimIds, current_local_compose_maps_all_plan_sources: remergeCurrent },
    adoption: { r11_has_six_chapter_files: keys.every((key) => fs.existsSync(path.join(r11, `candidate/chapters/${key}.json`))), formal_factual_gate: 'HOLD_P1_N14', direct_install_allowed: false, formal_script_review_allowed: false, paid_media_allowed: false, required_next: ['Create a new hash-bound editorial candidate that resolves active n14 source and wording, then obtain a fresh independent factual-claims review; r11 original offline PASS cannot serve as a formal factual PASS.', 'Obtain a fresh authenticated host capture and complete jobs, budget, STOP and lease readback.', 'Reconcile the six persisted chapter JSON files and their audit history against this exact r11 scene, line, claim and source delta.', 'Make the A01-only duration gate and public source remerge safe, then independently review the proposed on-host transition.', 'Run real verifier, listener and narrative gates on the resulting source before any formal script-review receipt.'] },
  };
}

try {
  const args = process.argv.slice(2);
  gate(args.length === 5 && ['--check', '--write'].includes(args[0]) && args[1] === '--snapshot' && args[3] === '--verified', 'ARGS_REQUIRED');
  const report = compare(args[2], args[4]);
  const reportFile = path.join(here, 'report.json');
  if (args[0] === '--write') fs.writeFileSync(reportFile, json(report));
  else gate(readFile(reportFile, 'REPORT_MISSING').equals(json(report)), 'REPORT_DRIFT');
  console.log(JSON.stringify({ status: report.status, snapshot_links: report.snapshot_proof.links, before_scenes: report.totals.before_scenes, r11_scenes: report.totals.r11_scenes, before_sources: report.sources.before_public_count, r11_sources: report.sources.r11_public_count, six_chapters_available: report.adoption.r11_has_six_chapter_files, paid_media_allowed: false }));
} catch (error) {
  console.error(`HOLD:${String(error.message).toUpperCase().replace(/[^A-Z0-9_:-]/g, '') || 'INPUT_FAILED'}`);
  process.exitCode = 2;
}
