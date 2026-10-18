// A01 offline bridge only. This command reads pinned inputs and checks generated files;
// it has no write mode, host connection, review signer, or media-provider call.
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const parent = path.dirname(here);
const r12 = path.join(parent, 'A01-editorial-candidate-20261018-r12');
const prior = path.join(parent, 'A01-r11-snapshot104-diff-20261018');
const readback = path.join(parent, 'A01-pinned-lexicon-transition-candidate-20261017', 'actual-104-readback-20261017.json');
const slug = 'story-rolling-suitcase-v2';
const keys = ['hook', 'origin', 'idea', 'engine', 'turn', 'now'];
const pins = {
  r12_manifest: '17cc760b8573f97d189db7c476d57c61eddd4050f79e54a0460eee5c15b7a9d3',
  r12_review: '123f4650eaa55197ddcc955c9dd6bcf6f9bf3f1137c8ff0adb7c16ef30bceb4e',
  snapshot_diff: 'f861df7ea97bcf33a280d1ba3cb68280b2c9f030ecfceecd54cfff0cc302006c',
  current_inventory: '7807ee9daf03bd747d6de45ffa9903469fa8309f1611944de879df8293966c9e',
  current_lexicon: 'ecc784b12066a64f847629753bb17d03814c61c349664c17b6c15237d01cd5a2',
  old_lexicon: 'e24382a54e9d8fe4570ddc176fa39081a7e3a4a728b481caae5f12cc81ad2903',
  current_archive_reported: '13fedb2bcdb44bd2dd1bf484ea5557c2d217a0ddf71e6c1b57e33b2ba46912ed',
};
const hash = (bytes) => createHash('sha256').update(bytes).digest('hex');
const json = (value) => Buffer.from(JSON.stringify(value, null, 2) + '\n');
const same = (left, right, code) => assert.deepEqual(left, right, code);
function file(name) {
  const stat = fs.lstatSync(name);
  assert.ok(stat.isFile() && !stat.isSymbolicLink(), `regular file required: ${name}`);
  return fs.readFileSync(name);
}
function pinned(name, digest, code) {
  const bytes = file(name);
  assert.equal(hash(bytes), digest, code);
  return bytes;
}
const parse = (bytes) => JSON.parse(bytes.toString('utf8'));
function inventory(root) {
  assert.ok(path.isAbsolute(root) && fs.lstatSync(root).isDirectory(), 'absolute snapshot directory required');
  const rows = [];
  function visit(dir, prefix = '') {
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      const rel = prefix ? `${prefix}/${entry.name}` : entry.name;
      const full = path.join(dir, entry.name);
      const stat = fs.lstatSync(full);
      assert.ok(!stat.isSymbolicLink(), 'snapshot symlink refused');
      if (stat.isDirectory()) visit(full, rel);
      else {
        assert.ok(stat.isFile(), 'snapshot nonfile refused');
        rows.push([rel, hash(fs.readFileSync(full))]);
      }
    }
  }
  visit(root);
  rows.sort((a, b) => a[0].localeCompare(b[0], 'en'));
  // Match the bytewise path ordering used by the independent r11/104 report.
  rows.sort((a, b) => a[0] < b[0] ? -1 : a[0] > b[0] ? 1 : 0);
  return { file_count: rows.length, sha256: hash(Buffer.from(rows.map(([rel, digest]) => `${rel}\0${digest}\n`).join(''))), rows };
}
function uniqueMap(rows, key, code) {
  const out = new Map();
  for (const row of rows) {
    const id = key(row);
    assert.ok(typeof id === 'string' && id && !out.has(id), `${code}: ${id}`);
    out.set(id, row);
  }
  return out;
}
function claimsMarkdown(bytes) {
  const rows = [];
  let chapter = null;
  for (const line of bytes.toString('utf8').split(/\r?\n/)) {
    const heading = /^## .*（(hook|origin|idea|engine|turn|now)）$/.exec(line);
    if (heading) { chapter = heading[1]; continue; }
    if (!/^[a-z]\d+[a-z]?｜/.test(line)) continue;
    const cells = line.split('｜');
    assert.equal(cells.length, 6, 'claim row shape');
    const [id, claim, url, checked, scene, verdict] = cells;
    assert.ok(chapter && claim && /^https:\/\//.test(url) && /^\d{4}-\d{2}-\d{2}$/.test(checked));
    assert.equal(verdict, 'PENDING', `r12 claim ${id} is not pending`);
    rows.push({ id, claim, url, checked, scene, verdict, chapter });
  }
  uniqueMap(rows, (row) => row.id, 'duplicate r12 claim');
  return rows;
}
function itemLocation(chapters, field, keyOf) {
  const rows = [];
  for (const key of keys) for (const [index, scene] of chapters[key].scenes.entries()) {
    if (field === 'scene') rows.push({ id: scene.id, chapter: key, index, item: scene });
    if (field === 'line') for (const [line_index, item] of (scene.lines ?? []).entries()) rows.push({ id: item.id, chapter: key, scene: scene.id, index: line_index, item });
  }
  if (field === 'claim') for (const key of keys) for (const [index, item] of (chapters[key].claims ?? []).entries()) rows.push({ id: item.id, chapter: key, scene: item.scene, index, item });
  return uniqueMap(rows, keyOf ?? ((row) => row.id), `duplicate ${field}`);
}
function orderDiff(before, after) {
  return {
    retired: [...before.keys()].filter((id) => !after.has(id)).sort(),
    added: [...after.keys()].filter((id) => !before.has(id)).sort(),
    retained: [...after.keys()].filter((id) => before.has(id)).sort(),
  };
}

export function buildArtifacts(snapshot, verifiedFile, current) {
  const diff = parse(pinned(path.join(prior, 'report.json'), pins.snapshot_diff, 'r11/104 report drift'));
  assert.equal(diff.status, 'OFFLINE_DIFF_ONLY_HOLD');
  const manifest = parse(pinned(path.join(r12, 'manifest.json'), pins.r12_manifest, 'r12 manifest drift'));
  assert.equal(manifest.status, 'HOLD_UNREVIEWED_OFFLINE_EDITORIAL_CANDIDATE');
  const review = pinned(path.join(r12, 'independent-full-review-20261018.md'), pins.r12_review, 'r12 review drift').toString('utf8');
  assert.ok(review.includes(pins.r12_manifest.toUpperCase()) && review.includes('P1 = 0') && review.includes('HOLD'), 'r12 review conclusion drift');
  assert.equal(hash(file(path.join(r12, 'build.mjs'))), manifest.build_sha256, 'r12 builder drift');
  assert.equal(hash(file(path.join(r12, 'README.md'))), manifest.readme_sha256, 'r12 README drift');
  for (const [rel, digest] of Object.entries(manifest.outputs_sha256)) pinned(path.join(r12, rel), digest, `r12 output drift ${rel}`);
  const inv = inventory(snapshot);
  same({ file_count: inv.file_count, sha256: inv.sha256 }, { file_count: diff.snapshot_proof.file_count, sha256: diff.snapshot_proof.inventory_sha256 }, 'snapshot inventory drift');
  const fresh = inventory(current);
  assert.equal(fresh.file_count, 254, 'current capture file count drift');
  assert.equal(fresh.sha256, pins.current_inventory, 'current capture inventory drift');
  const oldInventory = new Map(inv.rows);
  const currentInventory = new Map(fresh.rows);
  const changedFiles = [...new Set([...oldInventory.keys(), ...currentInventory.keys()])].sort()
    .filter((rel) => oldInventory.get(rel) !== currentInventory.get(rel))
    .map((rel) => ({ path: rel, old_sha256: oldInventory.get(rel) ?? null, current_sha256: currentInventory.get(rel) ?? null }));
  same(changedFiles, [{ path: 'docs/videos/lexicon.json', old_sha256: pins.old_lexicon, current_sha256: pins.current_lexicon }], 'current versus 104 file drift');
  const verified = parse(pinned(verifiedFile, diff.snapshot_proof.verified_report_sha256, '104 verification drift'));
  const actual = parse(pinned(readback, diff.snapshot_proof.readback_sha256, '104 readback drift'));
  assert.equal(verified.integrity, 'ACTUAL_REVIEW_PROGRESS_CHAIN_PASS');
  assert.equal(verified.links, 104);
  assert.equal(verified.source_sha256, diff.snapshot_proof.source_sha256);
  assert.equal(actual.integrity, verified.integrity);
  assert.equal(actual.links, verified.links);
  assert.equal(actual.source_sha256, verified.source_sha256);
  assert.equal(actual.production_status, 'HOLD');
  const capture = (rel) => file(path.join(snapshot, ...rel.split('/')));
  const oldVideo = parse(capture(`docs/videos/${slug}/video.json`));
  const oldSeries = parse(capture(`docs/videos/${slug}/series.json`));
  const oldAuto = parse(capture(`${slug}/auto.json`));
  assert.equal(oldVideo.slug, slug);
  assert.equal(oldSeries.slug, 'brand-stories-curio-pilot-v2');
  assert.equal(oldAuto.target_minutes, 10);
  same(oldVideo.target_minutes, [9, 11], 'saved body duration drift');
  const oldChapters = Object.fromEntries(keys.map((key) => {
    const bytes = capture(`${slug}/story/chapters/${key}.json`);
    const expected = diff.chapters.find((row) => row.key === key)?.before?.chapter_sha256;
    assert.equal(hash(bytes), expected, `snapshot ${key} chapter drift`);
    const chapter = parse(bytes);
    assert.equal(chapter.key, key);
    return [key, chapter];
  }));
  const oldScenes = itemLocation(oldChapters, 'scene');
  const oldLines = itemLocation(oldChapters, 'line');
  const oldClaims = itemLocation(oldChapters, 'claim');
  assert.equal(oldScenes.size, 79);
  assert.equal(oldLines.size, 108);
  assert.equal(oldClaims.size, 85);

  const video = parse(file(path.join(r12, 'candidate/video.json')));
  const originalSeries = parse(file(path.join(r12, 'candidate/series.json')));
  const sourceMap = parse(file(path.join(r12, 'source-map.json')));
  const sourceAddition = parse(file(path.join(r12, 'plan-source-addition.json')));
  const claimRows = claimsMarkdown(file(path.join(r12, 'candidate/claims.md')));
  const noncanonicalClaimIds = claimRows.filter((row) => !/^[a-z]\d+$/.test(row.id)).map((row) => row.id);
  same(noncanonicalClaimIds, ['t7b'], 'r12 noncanonical claim IDs drift');
  assert.equal(video.slug, slug);
  same(video.target_minutes, [7, 8], 'r12 owner duration drift');
  assert.equal(video.scenes.length, 65);
  assert.equal(video.sources.length, 18);
  assert.equal(claimRows.length, 78);
  assert.equal(originalSeries.plan.sources.length, 23);
  assert.equal(originalSeries.target_minutes, 10);
  const publicSources = uniqueMap(video.sources, (row) => row.url, 'r12 public source');
  const r12ClaimById = uniqueMap(claimRows, (row) => row.id, 'r12 claim');
  const sourceClaimMap = new Map();
  for (const row of sourceMap.source_index) {
    assert.ok(publicSources.has(row.url), 'source-map URL not public');
    for (const id of row.claim_ids) {
      assert.ok(!sourceClaimMap.has(id), `source-map duplicate claim ${id}`);
      sourceClaimMap.set(id, row.url);
    }
  }
  assert.equal(sourceClaimMap.size, claimRows.length);
  for (const row of claimRows) {
    assert.equal(sourceClaimMap.get(row.id), row.url, `source-map claim ${row.id}`);
    assert.ok(publicSources.get(row.url).checked_on >= row.checked, `source date ${row.id}`);
  }

  const proposedSeries = structuredClone(originalSeries);
  const originalPlanSources = originalSeries.plan.sources;
  const planMap = uniqueMap(proposedSeries.plan.sources.map((source, index) => ({ ...source, index })), (row) => row.url, 'plan source');
  const missing = video.sources.filter((source) => !planMap.has(source.url));
  assert.equal(missing.length, 2, 'source-plan missing-source count drift');
  assert.ok(missing.some((row) => row.url.includes('Chinook_2024_5-3-24_FINAL.pdf')), 'Plath first-person source missing');
  assert.ok(missing.some((row) => row.url === sourceAddition.source.url), 'n14 source missing');
  for (const source of missing) {
    const firstClaim = claimRows.find((row) => row.url === source.url);
    proposedSeries.plan.sources.push({
      url: source.url,
      publisher: source.url === sourceAddition.source.url ? sourceAddition.source.publisher : source.title,
      kind: source.url === sourceAddition.source.url ? sourceAddition.source.kind : 'archive',
      supports: source.url === sourceAddition.source.url ? sourceAddition.source.supports : firstClaim.claim,
      checked: source.checked_on,
    });
  }
  const dateChanges = [];
  const proposedIndex = uniqueMap(proposedSeries.plan.sources.map((source, index) => ({ ...source, index })), (row) => row.url, 'proposed source');
  const titleDifferences = [];
  for (const source of video.sources) {
    const row = proposedIndex.get(source.url);
    assert.ok(row, `unmapped source ${source.url}`);
    if (row.publisher !== source.title) titleDifferences.push({ url: source.url, proposed_index: row.index, r12_public_title: source.title, proposed_publisher: row.publisher });
    if (row.checked !== source.checked_on) {
      assert.ok(row.checked < source.checked_on, `candidate check date would go backward ${source.url}`);
      dateChanges.push({ url: source.url, from: row.checked, to: source.checked_on, index: row.index });
      proposedSeries.plan.sources[row.index].checked = source.checked_on;
    }
  }
  const uncitedPlan = originalPlanSources.map((source, index) => ({ url: source.url, index })).filter((row) => !publicSources.has(row.url));
  assert.equal(uncitedPlan.length, 7, 'uncited plan source count drift');
  for (const fact of proposedSeries.plan.must_verify) for (const index of fact.sources) assert.ok(Number.isInteger(index) && index >= 0 && index < originalPlanSources.length, 'must_verify index drift');

  const r12Chapters = {};
  const r12SceneMap = new Map();
  const r12LineMap = new Map();
  for (const key of keys) {
    const scenes = video.scenes.filter((scene) => scene.id.startsWith(`${key}-`));
    assert.ok(scenes.length > 0 && typeof scenes[0].chapter === 'string', `${key} title missing`);
    const claimIds = scenes.flatMap((scene) => scene.claims ?? []);
    const claims = claimRows.filter((row) => row.chapter === key);
    same([...claimIds].sort(), claims.map((row) => row.id).sort(), `${key} claim references drift`);
    for (const scene of scenes) {
      assert.ok(!r12SceneMap.has(scene.id), `duplicate r12 scene ${scene.id}`);
      r12SceneMap.set(scene.id, { chapter: key, item: scene });
      for (const line of scene.lines ?? []) {
        assert.ok(!r12LineMap.has(line.id), `duplicate r12 line ${line.id}`);
        r12LineMap.set(line.id, { chapter: key, scene: scene.id, item: line });
      }
    }
    const plainScenes = scenes.map(({ chapter: _chapter, claims: _claims, ...scene }) => scene);
    r12Chapters[key] = {
      key,
      title: scenes[0].chapter,
      scenes: plainScenes,
      claims: claims.map((row) => ({ id: row.id, claim: row.claim, scene: row.scene, source: proposedIndex.get(row.url).index, fact: null, verdict: 'UNCHECKED' })),
      loops: [],
      ...(key === 'hook' ? { thumbnail_shot: video.thumbnail?.data?.shot } : {}),
      report: 'OFFLINE_BRIDGE_ONLY: all claims reset to UNCHECKED; no verifier, listener, narrative panel, or formal review has run on these six chapters.',
    };
  }
  assert.equal(r12SceneMap.size, 65);
  assert.equal(r12LineMap.size, 77);
  const loopKeys = new Set();
  for (const loop of video.loops ?? []) {
    const setup = r12LineMap.get(loop.setup);
    const payoff = r12LineMap.get(loop.payoff);
    assert.ok(setup && payoff && !loopKeys.has(loop.setup), `unresolved loop ${loop.setup}`);
    loopKeys.add(loop.setup);
    if (setup.chapter !== payoff.chapter) r12Chapters[setup.chapter].loops.push({ setup: loop.setup, what: loop.what });
    r12Chapters[payoff.chapter].loops.push({ setup: loop.setup, payoff: loop.payoff, what: loop.what });
  }
  assert.equal(loopKeys.size, 11);
  assert.ok(r12Chapters.hook.scenes.some((scene) => scene.id === r12Chapters.hook.thumbnail_shot));
  const r12EmptyClaimArrays = video.scenes.filter((scene) => Array.isArray(scene.claims) && scene.claims.length === 0).map((scene) => scene.id);
  const chapterComposeLoopOrder = keys.flatMap((key) => r12Chapters[key].loops.filter((loop) => loop.payoff).map((loop) => loop.setup));
  assert.equal(r12EmptyClaimArrays.length, 3, 'r12 empty claim arrays drift');
  same([...chapterComposeLoopOrder].sort(), video.loops.map((loop) => loop.setup).sort(), 'chapter loop set drift');
  assert.notDeepEqual(chapterComposeLoopOrder, video.loops.map((loop) => loop.setup), 'r12 loop ordering unexpectedly reproduced');

  const sceneIds = orderDiff(oldScenes, r12SceneMap);
  const lineIds = orderDiff(oldLines, r12LineMap);
  const claimIds = orderDiff(oldClaims, r12ClaimById);
  const chapterMapping = keys.map((key) => {
    const chapter = r12Chapters[key];
    const old = oldChapters[key];
    return {
      key,
      old_chapter_sha256: diff.chapters.find((row) => row.key === key).before.chapter_sha256,
      old_counts: { scenes: old.scenes.length, lines: old.scenes.flatMap((scene) => scene.lines ?? []).length, claims: old.claims.length },
      candidate_counts: { scenes: chapter.scenes.length, lines: chapter.scenes.flatMap((scene) => scene.lines ?? []).length, claims: chapter.claims.length },
      scenes: chapter.scenes.map((scene, index) => {
        const original = oldScenes.get(scene.id);
        const merged = r12SceneMap.get(scene.id).item;
        return {
          id: scene.id,
          index,
          candidate_scene_sha256: hash(json(scene)),
          r12_merged_scene_sha256: hash(json(merged)),
          old: original ? { chapter: original.chapter, index: original.index, scene_sha256: hash(json(original.item)), changed: hash(json(original.item)) !== hash(json(scene)) } : null,
          lines: scene.lines.map((line, lineIndex) => {
            const before = oldLines.get(line.id);
            return { id: line.id, index: lineIndex, text_sha256: hash(Buffer.from(line.text)), old: before ? { chapter: before.chapter, scene: before.scene, index: before.index, text_sha256: hash(Buffer.from(before.item.text)), changed: before.item.text !== line.text } : null };
          }),
          claims: chapter.claims.filter((row) => row.scene === scene.id).map((row) => {
            const current = r12ClaimById.get(row.id);
            const before = oldClaims.get(row.id);
            const beforeSource = Number.isInteger(before?.item?.source) ? oldVideo.sources[before.item.source] : null;
            return {
              id: row.id,
              claim_sha256: hash(Buffer.from(row.claim)),
              source_url: current.url,
              source_checked: current.checked,
              proposed_plan_source_index: row.source,
              reset_verdict: row.verdict,
              old: before ? { chapter: before.chapter, scene: before.scene, index: before.index, claim_sha256: hash(Buffer.from(before.item.claim)), source_url: beforeSource?.url ?? null, verdict: before.item.verdict ?? null } : null,
            };
          }),
        };
      }),
    };
  });
  const mapping = {
    schema_version: 1,
    status: 'OFFLINE_SNAPSHOT104_TO_R12_MAP_HOLD',
    source_basis: { snapshot_links: 104, snapshot_tip_sha256: diff.snapshot_proof.source_sha256, r12_manifest_sha256: pins.r12_manifest, r12_review_sha256: pins.r12_review, r11_snapshot_diff_sha256: pins.snapshot_diff },
    global_ids: { scenes: sceneIds, lines: lineIds, claims: claimIds },
    chapters: chapterMapping,
  };
  const sourcePlan = {
    schema_version: 1,
    status: 'PROPOSED_ONLY_SOURCE_REMERGE_REQUIRED',
    old_plan_sources: originalPlanSources.length,
    proposed_plan_sources: proposedSeries.plan.sources.length,
    r12_cited_public_sources: video.sources.length,
    missing_from_old_plan: missing.map((row) => ({ url: row.url, proposed_index: proposedIndex.get(row.url).index, checked: row.checked_on })),
    old_plan_uncited_by_r12: uncitedPlan,
    existing_source_checked_date_changes: dateChanges,
    public_title_differences: titleDifferences,
    source_index_basis: 'candidate/series.json plan.sources, old 0..22 retained and two sources appended at 23..24',
    claim_source_rows: claimRows.map((row) => ({ id: row.id, chapter: row.chapter, scene: row.scene, url: row.url, checked: row.checked, proposed_plan_index: proposedIndex.get(row.url).index, r12_public_index: video.sources.findIndex((source) => source.url === row.url) })),
    old_must_verify_indices_preserved: true,
    compose_with_proposed_plan_would_publish_uncited_sources: uncitedPlan.length,
    r12_exact_public_source_set_reproduced_by_current_worker: false,
    r12_exact_public_source_metadata_reproduced_by_current_worker: false,
    direct_host_adoption_allowed: false,
  };
  const reset = {
    schema_version: 1,
    status: 'ALL_FORMAL_GATES_RESET_REQUIRED_HOLD',
    snapshot: { links: 104, tip_sha256: diff.snapshot_proof.source_sha256, production_status: actual.production_status, old_capture_date: '2026-10-17', current_capture_inventory_sha256: fresh.sha256, current_capture_a01_story_bytes_equal_old: true, current_capture_provenance_independently_verified_here: false },
    candidate: { r12_manifest_sha256: pins.r12_manifest, independent_offline_review_sha256: pins.r12_review, scenes: 65, lines: 77, claims: 78, source_urls: 18 },
    chapter_bytes_changed_from_snapshot: keys.map((key) => ({ key, old_sha256: diff.chapters.find((row) => row.key === key).before.chapter_sha256, candidate_sha256: hash(json(r12Chapters[key])) })),
    claim_id_renumbering_blocker: {
      severity: 'P2_FORMAL_ADOPTION_BLOCKER',
      noncanonical_r12_claim_ids: noncanonicalClaimIds,
      location: 'turn-09 claim t7b',
      worker_rule: 'story.mjs numberClaims accepts only a chapter prefix followed by digits; verifier cleanup reassigns nonnumeric IDs',
      post_verifier_id: 'UNKNOWN_UNTIL_THE_EXACT_FORMAL_VERIFIER_RESULT',
      required_action: 'Rebuild the scene/line/claim/source mapping, chapter and merged-script hashes, and any formal review receipt from the actual verifier-saved chapter bytes; do not reuse t7b-bound offline hashes.',
    },
    compose_byte_differences_even_with_proposed_chapters: {
      r12_explicit_empty_claim_array_scene_ids: r12EmptyClaimArrays,
      worker_omits_empty_claim_arrays: true,
      r12_loop_setup_order: video.loops.map((loop) => loop.setup),
      chapter_compose_loop_setup_order: chapterComposeLoopOrder,
      loop_membership_preserved_but_order_changes: true,
      r12_exact_video_bytes_reproduced: false,
    },
    new_or_changed_line_ids: [...r12LineMap].filter(([id, row]) => oldLines.get(id)?.item?.text !== row.item.text).map(([id]) => id),
    changed_or_new_claim_ids: [...r12ClaimById].filter(([id, row]) => {
      const old = oldClaims.get(id)?.item;
      const oldUrl = Number.isInteger(old?.source) ? oldVideo.sources[old.source]?.url : null;
      return !old || old.claim !== row.claim || oldUrl !== row.url || old.scene !== row.scene;
    }).map(([id]) => id),
    persisted_six_chapters: 'DO_NOT_OVERWRITE_FROM_THIS_PACKAGE',
    chapter_verifier: 'REQUIRED_NEW_RUN_ON_FRESH_HOST_CHAPTER_BYTES',
    listener: 'REQUIRED_NEW_RUN_ON_FRESH_HOST_CHAPTER_BYTES',
    narrative_panel: 'REQUIRED_NEW_RUN_ON_FRESH_HOST_CHAPTER_BYTES',
    formal_script_review_receipt: 'NOT_ISSUED_AND_OLD_RECEIPTS_NOT_TRANSFERABLE',
    source_plan_merge: 'REQUIRED_BEFORE_COMPOSE_OR_PUBLIC_METADATA',
    saved_duration: { snapshot_video: oldVideo.target_minutes, snapshot_auto_minutes: oldAuto.target_minutes, r12_body: video.target_minutes, old_series_minutes: oldSeries.target_minutes, r12_series_minutes: originalSeries.target_minutes, action: 'A01-only persisted duration and worker gate reconciliation required; this package does not mutate either' },
    tts_and_real_duration: 'NOT_RUN',
    image_contact_sheet_and_final_review: 'NOT_RUN',
    fresh_host_audit_jobs_budget_stop_lease: 'REQUIRED',
    current_capture_global_lexicon_rebaseline_before_tts: 'REQUIRED',
    paid_media_allowed: false,
  };
  assert.ok(reset.chapter_bytes_changed_from_snapshot.every((row) => row.old_sha256 !== row.candidate_sha256));
  const currentAssessment = {
    schema_version: 1,
    status: 'CURRENT_CAPTURE_FILE_COMPARISON_ONLY_HOLD',
    reported_archive_sha256_not_recomputed_here: pins.current_archive_reported,
    old_snapshot_inventory_sha256: inv.sha256,
    current_capture_inventory_sha256: fresh.sha256,
    file_count: fresh.file_count,
    exact_relative_file_differences: changedFiles,
    a01_six_chapters_and_other_capture_files_byte_identical_to_snapshot104: true,
    global_lexicon_difference_is_outside_a01_story_chapters: true,
    independent_current_host_provenance_and_live_stop_lease_job_budget: 'NOT_ESTABLISHED_BY_FILE_COMPARISON',
    formal_gates_or_paid_media_allowed: false,
  };
  const outputs = new Map([
    ...keys.map((key) => [`candidate/chapters/${key}.json`, json(r12Chapters[key])]),
    ['candidate/series.json', json(proposedSeries)],
    ['mapping.json', json(mapping)],
    ['source-plan-assessment.json', json(sourcePlan)],
    ['reset-assessment.json', json(reset)],
    ['current-capture-assessment.json', json(currentAssessment)],
  ]);
  const ownManifest = {
    schema_version: 1,
    status: 'OFFLINE_BRIDGE_HOLD_NO_HOST_OR_PAID_ACTION',
    input_sha256: { r12_manifest: pins.r12_manifest, r12_independent_review: pins.r12_review, r11_snapshot104_diff: pins.snapshot_diff, snapshot_inventory: inv.sha256, snapshot_verified_receipt: diff.snapshot_proof.verified_report_sha256, current_capture_inventory: fresh.sha256 },
    check_sha256: hash(file(path.join(here, 'check.mjs'))),
    readme_sha256: hash(file(path.join(here, 'README.md'))),
    outputs_sha256: Object.fromEntries([...outputs].map(([name, bytes]) => [name, hash(bytes)])),
    direct_host_adoption_allowed: false,
    formal_receipt_issued: false,
    paid_media_allowed: false,
  };
  outputs.set('manifest.json', json(ownManifest));
  return outputs;
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try {
    const args = process.argv.slice(2);
    assert.ok(args.length === 7 && args[0] === '--check' && args[1] === '--snapshot' && args[3] === '--verified' && args[5] === '--current', 'use --check --snapshot ABSOLUTE_DIR --verified ABSOLUTE_FILE --current ABSOLUTE_DIR');
    assert.ok(path.isAbsolute(args[2]) && path.isAbsolute(args[4]) && path.isAbsolute(args[6]), 'absolute local evidence paths required');
    const outputs = buildArtifacts(args[2], args[4], args[6]);
    for (const [rel, bytes] of outputs) {
      const target = path.join(here, rel);
      assert.ok(target.startsWith(here + path.sep), 'output path escaped candidate directory');
      assert.ok(file(target).equals(bytes), `generated file drift: ${rel}`);
    }
    console.log(JSON.stringify({ status: 'OFFLINE_BRIDGE_HOLD', chapters: 6, scenes: 65, lines: 77, claims: 78, r12_sources: 18, proposed_plan_sources: 25, current_files: 254, files_checked: outputs.size, writes: 0 }));
  } catch (error) {
    console.error(`HOLD: ${error.message}`);
    process.exitCode = 2;
  }
}
