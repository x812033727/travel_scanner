// Guarded A01 104 -> 105 source adoption. This module has no network, database,
// provider, or host command. A caller must supply a live, independently reviewed
// gate probe and an exact owner grant. It does not start the video worker.
import { createHash, randomUUID } from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { readStoryLexicon } from '../core/story-lexicon.mjs';

export const SLUG = 'story-rolling-suitcase-v2';
export const CHAPTERS = Object.freeze(['hook', 'origin', 'idea', 'engine', 'turn', 'now']);
const HASH = /^[0-9a-f]{64}$/u;
const EVENT = /^r23-existing-revision-[0-9a-f]{16}$/u;
const SAFE_OLD_EVENT = /^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$/u;
export const RELEASE_LOCKS = Object.freeze([
  '/var/lock/travel-scanner-deploy.lock',
  '/root/mokaair-deploy.lock',
  '/run/mokaair-manual-deploy.lock',
  '/run/travel-scanner-deployer/deploy.lock',
]);
export const PRODUCTION_104_PINS = Object.freeze({
  source_sha256: 'e1499cd695f2f414d9379a8917b6b5b36e50ea0d046de495938157d8ff97add7',
  tip_index_sha256: 'f2628d894d6907f64733325581e0116c1d7b297b45fec0d9d63c4aff82d09288',
  audit_inventory_sha256: '0e51a4fa51220ec0e92b1044cdb0887dfa8e33ef8c825ef5ffcef9034b619e53',
  audit_file_count: 222,
});
// The r23 manuscript failed independent historical/editorial review on
// 2026-10-19. A future r24 must get new source and review pins before adoption.
export const REJECTED_R23_MANIFEST_SHA256 =
  'a5978f8318c87e62f48d9e00330fcdc45ffaf50161601d99017922f4af888cf4';
const sha = (bytes) => createHash('sha256').update(bytes).digest('hex');
const json = (value) => Buffer.from(JSON.stringify(value, null, 2) + '\n');
const need = (condition, code) => { if (!condition) throw Error(code); };
const verifiedGuard = (handle, code) => need(handle.verify() === true, code);
const hash = (file) => sha(regular(file));
const exists = (file) => { try { fs.lstatSync(file); return true; } catch (error) {
  if (error.code === 'ENOENT') return false;
  throw error;
} };
function syncDirectory(dir) {
  // Windows cannot fsync directory handles. Host execution is Linux, where
  // every create and rename must durably sync its parent directory.
  if (process.platform === 'win32') return;
  const fd = fs.openSync(dir, 'r');
  try { fs.fsyncSync(fd); } finally { fs.closeSync(fd); }
}

function regular(file) {
  const stat = fs.lstatSync(file);
  need(stat.isFile() && !stat.isSymbolicLink(), 'REGULAR_FILE_REQUIRED');
  return fs.readFileSync(file);
}
function directory(file) {
  const stat = fs.lstatSync(file);
  need(stat.isDirectory() && !stat.isSymbolicLink(), 'REAL_DIRECTORY_REQUIRED');
}
function freshProjectLease(workdir, owner) {
  directory(workdir);
  const file = path.join(workdir, 'LEASE');
  need(!fs.readdirSync(workdir).some((name) => name === 'LEASE' || name.startsWith('LEASE.')),
    'PREEXISTING_PROJECT_LEASE_REFUSED');
  const record = { schema_version: 1, token: randomUUID(),
    owner, pid: process.pid, host: os.hostname(),
    boot_id: null, start_ticks: null, acquired_at: new Date().toISOString() };
  const bytes = json(record);
  const fd = fs.openSync(file, 'wx', 0o600); // Never take over an old lease.
  try { fs.writeFileSync(fd, bytes); fs.fsyncSync(fd); }
  finally { fs.closeSync(fd); }
  syncDirectory(workdir);
  let released = false;
  return { verify() {
    need(!released && regular(file).equals(bytes), 'PROJECT_LEASE_LOST');
  }, release() {
    if (released) return;
    this.verify();
    fs.unlinkSync(file);
    syncDirectory(workdir);
    released = true;
  } };
}
function safeRoots(roots) {
  for (const key of ['docs', 'work']) {
    need(path.isAbsolute(roots[key]), 'ABSOLUTE_ROOT_REQUIRED');
    need(roots[key] === path.resolve(roots[key]), 'CANONICAL_NORMALIZED_ROOT_REQUIRED');
    directory(roots[key]);
    need(fs.realpathSync(roots[key]) === path.resolve(roots[key]), 'LINKED_ROOT_REFUSED');
  }
  need(roots.docs !== roots.work, 'TWO_DISTINCT_MOUNTS_REQUIRED');
  // The host uses two mounts. Testing on one filesystem is allowed, but the
  // production driver must separately prove their mount identities.
}
function ensureParentSafe(file) {
  const parent = path.dirname(file);
  const chain = [];
  for (let dir = parent; dir !== path.dirname(dir); dir = path.dirname(dir))
    chain.push(dir);
  for (const dir of chain.reverse()) {
    if (!exists(dir)) {
      fs.mkdirSync(dir, { mode: 0o700 }); // Never follow a preexisting linked ancestor.
      syncDirectory(path.dirname(dir));
    }
    directory(dir);
    need(fs.realpathSync(dir) === path.resolve(dir), 'LINKED_ANCESTOR_REFUSED');
  }
}
export function changedPaths() {
  return [
    ...CHAPTERS.map((key) => `${SLUG}/story/chapters/${key}.json`),
    `docs/videos/${SLUG}/series.json`,
    `docs/videos/${SLUG}/video.json`,
    `${SLUG}/auto.json`,
  ];
}
function fileFor(roots, logical) {
  need(changedPaths().includes(logical), 'PATH_OUTSIDE_NINE_FILE_ALLOWLIST');
  const isDocs = logical.startsWith('docs/videos/');
  const root = isDocs ? roots.docs : roots.work;
  const relative = isDocs ? logical.slice('docs/videos/'.length) : logical;
  const file = path.join(root, ...relative.split('/'));
  need(file.startsWith(root + path.sep), 'PATH_ESCAPE');
  let parent = path.dirname(file);
  while (parent !== root) { directory(parent); parent = path.dirname(parent); }
  regular(file);
  return file;
}
function optional(file) {
  return exists(file) ? hash(file) : null;
}
export function sourceTuple(roots) {
  safeRoots(roots);
  const doc = path.join(roots.docs, SLUG);
  const work = path.join(roots.work, SLUG);
  const lexicon = readStoryLexicon({ slug: SLUG, storyDir: doc,
    sharedFile: path.join(roots.docs, 'lexicon.json') });
  need(lexicon.mode === 'snapshot' && HASH.test(lexicon.lexicon_sha256),
    'PINNED_A01_LEXICON_REQUIRED');
  const chapters = Object.fromEntries(CHAPTERS.map((key) =>
    [key, hash(path.join(work, 'story', 'chapters', `${key}.json`))]));
  return {
    auto: hash(path.join(work, 'auto.json')),
    video: hash(path.join(doc, 'video.json')),
    series: hash(path.join(doc, 'series.json')),
    claims: hash(path.join(doc, 'claims.md')),
    script: hash(path.join(doc, 'script.md')),
    lexicon: lexicon.lexicon_sha256,
    narrative: hash(path.join(work, 'review', 'narrative.json')),
    pilot: optional(path.join(work, 'story', 'reviews', 'script-review.json')),
    verify: optional(path.join(doc, 'verify-1.md')),
    chapters,
  };
}
export const sourceHash = (tuple) => sha(JSON.stringify(tuple));

export function auditInventory(root, omittedTopDirectory = null) {
  directory(root);
  const rows = [];
  function walk(dir, rel = '') {
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      if (!rel && entry.name === omittedTopDirectory) continue;
      need(!entry.isSymbolicLink(), 'AUDIT_LINK_REFUSED');
      const name = rel ? `${rel}/${entry.name}` : entry.name;
      const file = path.join(dir, entry.name);
      if (entry.isDirectory()) walk(file, name);
      else {
        need(entry.isFile(), 'AUDIT_SPECIAL_FILE_REFUSED');
        rows.push([name, hash(file)]);
      }
    }
  }
  walk(root);
  rows.sort((a, b) => a[0] < b[0] ? -1 : a[0] > b[0] ? 1 : 0);
  return { count: rows.length, sha256: sha(rows.map(([name, digest]) =>
    `${name}\0${digest}\n`).join('')) };
}
function auditRoot(roots) {
  return path.join(roots.work, SLUG, 'story', 'recheck-audit');
}
function assertOldAudit(roots, plan, { allowPendingEvent = false, grant = null } = {}) {
  const root = auditRoot(roots);
  const entries = fs.readdirSync(root, { withFileTypes: true });
  const pending = allowPendingEvent && entries.some((entry) => entry.name === plan.event_id);
  const oldEntries = entries.filter((entry) => !pending || entry.name !== plan.event_id);
  need(oldEntries.length === 104 && entries.length === 104 + Number(pending)
    && entries.every((entry) =>
    entry.isDirectory() && !entry.isSymbolicLink()), 'EXACT_104_EVENTS_REQUIRED');
  const old = auditInventory(root, pending ? plan.event_id : null);
  need(old.count === plan.old_audit_file_count
    && old.sha256 === plan.old_audit_inventory_sha256, 'OLD_AUDIT_DRIFT');
  const tip = path.join(root, plan.old_event_id, 'index.json');
  need(hash(tip) === plan.old_index_sha256, 'OLD_INDEX_DRIFT');
  const index = JSON.parse(regular(tip));
  need(index.after_source_sha256 === plan.before_source_sha256
    && sourceHash(index.after) === plan.before_source_sha256, 'OLD_TIP_DRIFT');
  if (pending) {
    const pendingDir = path.join(root, plan.event_id);
    const files = fs.readdirSync(pendingDir);
    need(files.length === 0 || (files.length === 1 && files[0] === 'manual-amendment.json'),
      'PENDING_EVENT_FOREIGN_FILE');
    if (files.length) {
      const expected = expectedEventArtifacts(plan, index.after, grant);
      need(hash(path.join(pendingDir, files[0])) === sha(expected.amendment),
        'PENDING_AMENDMENT_DRIFT');
    }
  }
  return index;
}
function selectedPins(syntheticTestPins) {
  if (syntheticTestPins === undefined) return PRODUCTION_104_PINS;
  need(process.env.NODE_TEST_CONTEXT === 'child-v8'
    && process.argv[1]?.replaceAll('\\', '/').endsWith('/a01-adoption/transaction.test.mjs'),
  'SYNTHETIC_PINS_ONLY_IN_OWN_TEST_RUNNER');
  need(HASH.test(syntheticTestPins?.source_sha256)
    && HASH.test(syntheticTestPins?.tip_index_sha256)
    && HASH.test(syntheticTestPins?.audit_inventory_sha256)
    && Number.isInteger(syntheticTestPins?.audit_file_count),
  'SYNTHETIC_PINS_INVALID');
  return syntheticTestPins;
}
function validateTarget(roots, plan, pins) {
  need(plan?.schema_version === 1 && plan.kind === 'a01_r23_105_install_plan'
    && plan.slug === SLUG && EVENT.test(plan.event_id), 'PLAN_ID_INVALID');
  need(!Object.hasOwn(plan, 'event_index_sha256'),
    'INDEX_SHA_DEPENDS_ON_OWNER_GRANT');
  need(plan.editorial_manifest_sha256 !== REJECTED_R23_MANIFEST_SHA256,
    'R23_EDITORIAL_REJECTED_AWAIT_R24');
  // An arbitrary replacement SHA does not prove that r24's exact nine bytes
  // passed independent claim, source, visual and narrative review. The future
  // receipt gate must bind those hashes before production pins may execute.
  need(pins !== PRODUCTION_104_PINS, 'R24_EDITORIAL_REVIEW_GATE_NOT_CONFIGURED');
  need(HASH.test(plan.before_source_sha256)
    && HASH.test(plan.after_source_sha256)
    && HASH.test(plan.old_index_sha256)
    && HASH.test(plan.old_audit_inventory_sha256), 'PLAN_HASH_INVALID');
  need(plan.before_source_sha256 === pins.source_sha256
    && plan.old_index_sha256 === pins.tip_index_sha256
    && plan.old_audit_inventory_sha256 === pins.audit_inventory_sha256
    && plan.old_audit_file_count === pins.audit_file_count
    && SAFE_OLD_EVENT.test(plan.old_event_id) && plan.old_event_id !== '..',
  'INDEPENDENT_104_PINS_REQUIRED');
  need(plan.changed_files_sha256
    && JSON.stringify(Object.keys(plan.changed_files_sha256).sort()) ===
      JSON.stringify(changedPaths().sort()), 'EXACT_NINE_TARGETS_REQUIRED');
  need(plan.before_files_sha256
    && JSON.stringify(Object.keys(plan.before_files_sha256).sort()) ===
      JSON.stringify(changedPaths().sort())
    && Object.values(plan.before_files_sha256).every((value) => HASH.test(value)),
  'EXACT_NINE_BEFORE_HASHES_REQUIRED');
  need(Object.values(plan.changed_files_sha256).every((value) => HASH.test(value)),
    'TARGET_HASH_INVALID');
  need(Array.isArray(plan.public_source_urls) && plan.public_source_urls.length === 18
    && new Set(plan.public_source_urls).size === 18
    && plan.public_source_urls.every((url) => /^https:\/\//u.test(url)),
  'EXACT_18_PUBLIC_SOURCES_REQUIRED');
  need(plan.worker_story_sha256 && HASH.test(plan.worker_story_sha256)
    && plan.capture_manifest_sha256 && HASH.test(plan.capture_manifest_sha256)
    && plan.independent_capture_receipt_sha256
    && HASH.test(plan.independent_capture_receipt_sha256)
    && plan.public_filter_sha256 && HASH.test(plan.public_filter_sha256)
    && /^[0-9a-f]{40}$/u.test(plan.tools_video_tree_sha)
    && HASH.test(plan.tools_video_runtime_inventory_sha256)
    && Number.isInteger(plan.tools_video_runtime_file_count)
    && plan.tools_video_runtime_file_count > 0
    && /^sha256:[0-9a-f]{64}$/u.test(plan.worker_image_id),
  'FRESH_RUNTIME_PIN_REQUIRED');
  const target = plan.target_bytes;
  need(target && Object.keys(target).length === 9, 'TARGET_BYTES_REQUIRED');
  for (const logical of changedPaths()) {
    const bytes = Buffer.from(target[logical], 'base64');
    need(bytes.length && bytes.toString('base64') === target[logical]
      && sha(bytes) === plan.changed_files_sha256[logical], 'TARGET_BYTE_DRIFT');
    fileFor(roots, logical);
  }
  const video = JSON.parse(Buffer.from(target[`docs/videos/${SLUG}/video.json`], 'base64'));
  need(JSON.stringify(video.target_minutes) === '[7,8]'
    && JSON.stringify(video.sources.map((item) => item.url)) ===
      JSON.stringify(plan.public_source_urls), 'FILTERED_VIDEO_REQUIRED');
  const series = JSON.parse(Buffer.from(target[`docs/videos/${SLUG}/series.json`], 'base64'));
  const internalUrls = series.plan?.sources?.map((source) => source?.url);
  need(Array.isArray(internalUrls) && internalUrls.length === 25
    && internalUrls.every((url) => typeof url === 'string' && /^https:\/\//u.test(url))
    && new Set(internalUrls).size === 25
    && plan.public_source_urls.every((url) => internalUrls.includes(url))
    && series.target_minutes === 10,
    'INTERNAL_25_SOURCE_PLAN_REQUIRED');
  const auto = JSON.parse(Buffer.from(target[`${SLUG}/auto.json`], 'base64'));
  need(auto.status === 'blocked' && auto.blocked_kind === 'pilot_script_review'
    && auto.verified === false && auto.listener_done === false
    && auto.story?.narrative === null, 'REVIEW_RESET_REQUIRED');
  for (const key of CHAPTERS) {
    const chapter = JSON.parse(Buffer.from(target[`${SLUG}/story/chapters/${key}.json`], 'base64'));
    need(chapter.claims.every((claim) => claim.verdict === 'UNCHECKED'
      && claim.fact === null), 'OLD_FACT_VERDICTS_NOT_TRANSFERABLE');
  }
}
export function afterTuple(before, plan) {
  const after = structuredClone(before);
  for (const [logical, digest] of Object.entries(plan.changed_files_sha256)) {
    if (logical.endsWith('/auto.json')) after.auto = digest;
    else if (logical.endsWith('/series.json')) after.series = digest;
    else if (logical.endsWith('/video.json')) after.video = digest;
    else {
      const key = path.basename(logical, '.json');
      after.chapters[key] = digest;
    }
  }
  return after;
}
export function expectedEventArtifacts(plan, before, grant) {
  const after = afterTuple(before, plan);
  need(sourceHash(before) === plan.before_source_sha256
    && sourceHash(after) === plan.after_source_sha256, 'EVENT_SOURCE_TUPLE_DRIFT');
  need(grant?.approved === true && grant.slug === SLUG
    && grant.event_id === plan.event_id && grant.plan_sha256 === planHash(plan)
    && typeof grant.owner_approval_ref === 'string' && grant.owner_approval_ref.length > 12,
  'EVENT_OWNER_GRANT_REQUIRED');
  const ownerGrantSha = sha(json(grant));
  const amendment = json({ schema_version: 1, slug: SLUG, kind: 'r23_existing_six_chapter_revision',
    event_id: plan.event_id, before_source_sha256: plan.before_source_sha256,
    after_source_sha256: plan.after_source_sha256, editorial_manifest_sha256: plan.editorial_manifest_sha256,
    plan_sha256: grant.plan_sha256, owner_grant_sha256: ownerGrantSha,
    owner_approval_ref: grant.owner_approval_ref,
    capture_manifest_sha256: plan.capture_manifest_sha256,
    worker_story_sha256: plan.worker_story_sha256,
    public_filter_sha256: plan.public_filter_sha256,
    changed_files_sha256: plan.changed_files_sha256,
    public_source_urls: plan.public_source_urls,
    formal_review_pending: true, paid_work_allowed: false });
  const receipt = json({ schema_version: 1, slug: SLUG, kind: 'a01_adoption_installation_receipt',
    event_id: plan.event_id, before_source_sha256: plan.before_source_sha256,
    after_source_sha256: plan.after_source_sha256,
    plan_sha256: grant.plan_sha256, owner_grant_sha256: ownerGrantSha,
    owner_approval_ref: grant.owner_approval_ref,
    manual_amendment_sha256: sha(amendment),
    status: 'HOLD_PENDING_INDEPENDENT_READBACK' });
  const index = json({ schema_version: 1, slug: SLUG, result_kind: 'manual_revision',
    before_source_sha256: plan.before_source_sha256,
    after_source_sha256: plan.after_source_sha256, before, after, journals: [],
    manual_amendment_sha256: sha(amendment), revision_receipt_sha256: sha(receipt),
    previous_index_sha256: plan.old_index_sha256,
    old_audit_inventory_sha256: plan.old_audit_inventory_sha256,
    changed_paths: changedPaths(), formal_review_pending: true });
  return { amendment, receipt, index };
}
/** Candidate for independent review; intentionally not an approved verifier input. */
export function draftReadbackExpectation(plan, before, grant) {
  const { amendment, receipt, index } = expectedEventArtifacts(plan, before, grant);
  const prefix = `${SLUG}/story/recheck-audit/${plan.event_id}/`;
  return {
    schema_version: 1,
    kind: 'a01_r23_105_readback_expectation_draft',
    approval_required: true,
    slug: SLUG,
    event_id: plan.event_id,
    before_source_sha256: plan.before_source_sha256,
    after_source_sha256: plan.after_source_sha256,
    changed_files_sha256: plan.changed_files_sha256,
    event_files_sha256: {
      [`${prefix}index.json`]: sha(index),
      [`${prefix}manual-amendment.json`]: sha(amendment),
    },
    revision_receipt_sha256: sha(receipt),
    plan_sha256: grant.plan_sha256,
    owner_grant_sha256: sha(json(grant)),
    owner_approval_ref: grant.owner_approval_ref,
    public_source_urls: plan.public_source_urls,
  };
}
function safeCreate(file, bytes, lease) {
  lease.verify();
  need(!exists(file), 'CREATE_ONLY_COLLISION');
  ensureParentSafe(file);
  lease.verify();
  need(!exists(file), 'CREATE_ONLY_COLLISION');
  const fd = fs.openSync(file, 'wx', 0o600);
  try { fs.writeFileSync(fd, bytes); fs.fsyncSync(fd); }
  finally { fs.closeSync(fd); }
  syncDirectory(path.dirname(file));
}
function atomicReplace(file, bytes, lease, suffix) {
  lease.verify();
  regular(file);
  ensureParentSafe(file);
  const temporary = `${file}.a01-${suffix}.new`;
  safeCreate(temporary, bytes, lease);
  lease.verify();
  ensureParentSafe(file);
  regular(file);
  fs.renameSync(temporary, file);
  syncDirectory(path.dirname(file));
}
function paths(roots, id) {
  // Journals are on BOTH mounts but outside the A01 capture subtree. The
  // independent source verifier permits only nine replacements plus 105
  // event/receipt in the captured story directories.
  const doc = path.join(roots.docs, '.a01-adoption', SLUG, id);
  const work = path.join(roots.work, '.a01-adoption', SLUG, id);
  const event = path.join(auditRoot(roots), id);
  const receipt = path.join(roots.work, SLUG, 'manual-revisions', id, 'installation-receipt.json');
  return { doc, work, event, receipt };
}
export function plannedWritePaths(roots, plan) {
  const where = paths(roots, plan.event_id);
  const targets = changedPaths().map((logical) => fileFor(roots, logical));
  const auxiliary = [
    ...[where.doc, where.work].flatMap((dir) => [
      path.join(dir, 'intent.json'),
      ...changedPaths().map((logical) => path.join(dir, 'before', logical)),
    ]),
    path.join(where.event, 'manual-amendment.json'), where.receipt,
    path.join(where.event, `index.json.a01-${plan.event_id}.new`),
    path.join(where.event, 'index.json'),
  ];
  const auxiliaryDirectories = new Set();
  for (const file of auxiliary) {
    const root = file.startsWith(roots.docs + path.sep) ? roots.docs : roots.work;
    for (let dir = path.dirname(file); dir !== root; dir = path.dirname(dir))
      auxiliaryDirectories.add(dir);
  }
  return [
    path.join(roots.work, SLUG, 'LEASE'),
    ...targets,
    ...targets.map((file) => `${file}.a01-${plan.event_id}.new`),
    ...auxiliary,
    ...auxiliaryDirectories,
  ].sort();
}
function ownerGrant(grant, roots, plan, planSha) {
  need(grant?.schema_version === 1 && grant.slug === SLUG
    && grant.event_id === plan.event_id && grant.approved === true
    && grant.plan_sha256 === planSha && typeof grant.owner_approval_ref === 'string'
    && grant.owner_approval_ref.length > 12, 'EXACT_OWNER_GRANT_REQUIRED');
  need(JSON.stringify([...grant.write_paths].sort()) ===
    JSON.stringify(plannedWritePaths(roots, plan)), 'OWNER_PATH_SCOPE_DRIFT');
}
function stopBytes(roots, gate) {
  const file = path.join(roots.work, SLUG, 'STOP');
  const bytes = regular(file);
  need(sha(bytes) === gate.a01_stop_sha256, 'SCOPED_STOP_DRIFT');
  need(sha(regular(path.join(roots.work, 'STOP'))) === gate.global_stop_sha256,
    'GLOBAL_STOP_FENCE_DRIFT');
  return bytes;
}
async function checkGate(probe, roots, plan, stopSha, globalStopSha, releaseGuard,
  admissionFence) {
  const gate = await probe();
  verifiedGuard(releaseGuard, 'SELF_OWNED_RELEASE_GUARD_LOST');
  verifiedGuard(admissionFence, 'A01_DB_ADMISSION_FENCE_LOST');
  need(gate?.schema_version === 1 && gate.slug === SLUG
    && gate.release_sha === plan.release_sha
    && gate.capture_manifest_sha256 === plan.capture_manifest_sha256
    && gate.worker_story_sha256 === plan.worker_story_sha256
    && gate.public_filter_sha256 === plan.public_filter_sha256
    && gate.tools_video_tree_sha === plan.tools_video_tree_sha
    && gate.tools_video_runtime_inventory_sha256 === plan.tools_video_runtime_inventory_sha256
    && gate.tools_video_runtime_file_count === plan.tools_video_runtime_file_count
    && gate.worker_image_id === plan.worker_image_id
    && gate.independent_capture_receipt_sha256 === plan.independent_capture_receipt_sha256
    && gate.a01_stop_sha256 === stopSha
    && gate.global_stop_sha256 === globalStopSha
    && gate.release_hold?.owner === 'self'
    && gate.release_hold?.target_sha === plan.release_sha
    && gate.release_hold?.release_dir === releaseGuard.release_dir
    && gate.release_hold?.sha256 === releaseGuard.hold_sha256
    && JSON.stringify(gate.release_locks_owned_exactly) === JSON.stringify(RELEASE_LOCKS)
    && gate.a01_admission_fence?.kind === 'durable_db_row_guard'
    && gate.a01_admission_fence?.owner === 'self'
    && gate.a01_admission_fence?.token === admissionFence.token
    && gate.a01_admission_fence?.reserve_rejected === true
    && gate.a01_admission_fence?.text_stage_dispatch_rejected === true
    && gate.staged_release === false && gate.global_stop === true
    && gate.foreign_intent === false, 'HOST_GATE_DRIFT');
  need(Array.isArray(gate.global_nonterminal_stage_jobs)
    && gate.global_nonterminal_stage_jobs.length === 0
    && Array.isArray(gate.global_nonterminal_media_jobs)
    && gate.global_nonterminal_media_jobs.length === 0
    && Array.isArray(gate.a01_unsettled_journals)
    && gate.a01_unsettled_journals.length === 0, 'PAID_OR_UNSETTLED_WORK_PRESENT');
  need(gate.budget?.limit_usd === 25 && gate.budget?.spent_usd === 0
    && gate.budget?.reserved_usd === 0
    && gate.budget?.unsettled_operations === 0
    && gate.a01_media_assets === 0, 'A01_BUDGET_OR_MEDIA_DRIFT');
  need(stopBytes(roots, gate).length > 0, 'SCOPED_STOP_REQUIRED');
  return gate;
}
function planHash(plan) {
  return sha(json(plan));
}
function validateFreshSource(roots, plan) {
  const before = sourceTuple(roots);
  need(sourceHash(before) === plan.before_source_sha256, 'SOURCE_104_DRIFT');
  for (const logical of changedPaths())
    need(beforeHashFor(logical, before) === plan.before_files_sha256[logical],
      'BEFORE_FILE_PIN_DRIFT');
  const old = assertOldAudit(roots, plan);
  need(JSON.stringify(old.after) === JSON.stringify(before), 'OLD_TIP_SOURCE_DRIFT');
  const after = afterTuple(before, plan);
  need(sourceHash(after) === plan.after_source_sha256, 'PLAN_AFTER_TUPLE_DRIFT');
  return { before, after };
}

/**
 * The caller's probe must read live DB/jobs/budget/host locks on EVERY call.
 * This is a transaction core, not a CLI: no default probe or grant is provided.
 * A thrown error leaves A01 STOP and both journals in HOLD for reconciliation.
 */
export async function applyAdoption({ roots, plan, grant, probe, globalFence, releaseGuard,
  admissionFence, syntheticTestPins,
  fault = () => {} }) {
  safeRoots(roots);
  validateTarget(roots, plan, selectedPins(syntheticTestPins));
  need(!exists(path.join(auditRoot(roots), plan.event_id)), 'EVENT_ALREADY_EXISTS');
  const planSha = planHash(plan);
  ownerGrant(grant, roots, plan, planSha);
  need(typeof probe === 'function', 'LIVE_PROBE_REQUIRED');
  need(globalFence?.kind === 'reviewed_global_queue_worker_fence'
    && typeof globalFence.verify === 'function'
    && HASH.test(globalFence.global_stop_sha256), 'GLOBAL_QUEUE_FENCE_REQUIRED');
  need(releaseGuard?.kind === 'reviewed_self_owned_release_hold_and_four_locks'
    && typeof releaseGuard.verify === 'function'
    && HASH.test(releaseGuard.hold_sha256)
    && path.isAbsolute(releaseGuard.release_dir), 'SELF_OWNED_RELEASE_GUARD_REQUIRED');
  need(admissionFence?.kind === 'reviewed_durable_a01_db_admission_fence'
    && HASH.test(admissionFence.token)
    && typeof admissionFence.verify === 'function',
  'DURABLE_A01_DB_ADMISSION_FENCE_REQUIRED');
  verifiedGuard(releaseGuard, 'SELF_OWNED_RELEASE_GUARD_LOST');
  verifiedGuard(globalFence, 'GLOBAL_QUEUE_FENCE_LOST');
  const first = await checkGate(probe, roots, plan, plan.a01_stop_sha256,
    globalFence.global_stop_sha256, releaseGuard, admissionFence);
  const stopSha = first.a01_stop_sha256;
  const globalStopSha = first.global_stop_sha256;
  const lease = freshProjectLease(path.join(roots.work, SLUG),
    'a01-r23-104-to-105-adoption');
  const where = paths(roots, plan.event_id);
  try {
    lease.verify();
    verifiedGuard(globalFence, 'GLOBAL_QUEUE_FENCE_LOST');
    const writer = { verify() {
      verifiedGuard(globalFence, 'GLOBAL_QUEUE_FENCE_LOST');
      verifiedGuard(releaseGuard, 'SELF_OWNED_RELEASE_GUARD_LOST');
      verifiedGuard(admissionFence, 'A01_DB_ADMISSION_FENCE_LOST');
      lease.verify();
      need(sha(regular(path.join(roots.work, SLUG, 'STOP'))) === stopSha,
        'SCOPED_STOP_CHANGED_DURING_WRITE');
      need(sha(regular(path.join(roots.work, 'STOP'))) === globalStopSha,
        'GLOBAL_STOP_CHANGED_DURING_WRITE');
    } };
    const { before, after } = validateFreshSource(roots, plan);
    const { amendment, receipt, index } = expectedEventArtifacts(plan, before, grant);
    const indexSha = sha(index);
    await checkGate(probe, roots, plan, stopSha, globalStopSha, releaseGuard,
      admissionFence);
    need(!exists(where.doc) && !exists(where.work)
      && !exists(where.event) && !exists(where.receipt), 'FOREIGN_OR_OLD_INTENT_PRESENT');
    const intent = json({ schema_version: 1, slug: SLUG, event_id: plan.event_id,
      kind: 'a01_adoption_intent', plan_sha256: planSha, owner_approval_ref: grant.owner_approval_ref,
      owner_grant_sha256: sha(json(grant)), before_source_sha256: plan.before_source_sha256,
      after_source_sha256: plan.after_source_sha256, event_index_sha256: indexSha,
      scoped_stop_sha256: stopSha,
      status: 'HOLD_UNTIL_INDEPENDENT_READBACK' });
    safeCreate(path.join(where.doc, 'intent.json'), intent, writer);
    fault('docs-intent');
    safeCreate(path.join(where.work, 'intent.json'), intent, writer);
    fault('work-intent');
    for (const logical of changedPaths()) {
      const bytes = regular(fileFor(roots, logical));
      need(sha(bytes) === plan.before_files_sha256[logical], 'SOURCE_DRIFT_BEFORE_BACKUP');
      for (const dir of [where.doc, where.work]) {
        verifiedGuard(globalFence, 'GLOBAL_QUEUE_FENCE_LOST');
        safeCreate(path.join(dir, 'before', logical), bytes, writer);
        fault(`backup:${dir === where.doc ? 'docs' : 'work'}:${logical}`);
      }
    }
    // No canonical source was touched until both complete backup copies exist.
    for (const logical of changedPaths()) {
      const docCopy = regular(path.join(where.doc, 'before', logical));
      const workCopy = regular(path.join(where.work, 'before', logical));
      need(sha(docCopy) === plan.before_files_sha256[logical]
        && workCopy.equals(docCopy), 'DUAL_BACKUP_READBACK_DRIFT');
    }
    await checkGate(probe, roots, plan, stopSha, globalStopSha, releaseGuard,
      admissionFence);
    lease.verify();
    need(sourceHash(sourceTuple(roots)) === plan.before_source_sha256, 'SOURCE_DRIFT_BEFORE_REPLACE');
    fault('before-replace');
    for (const logical of changedPaths()) {
      verifiedGuard(globalFence, 'GLOBAL_QUEUE_FENCE_LOST');
      await checkGate(probe, roots, plan, stopSha, globalStopSha, releaseGuard,
        admissionFence);
      lease.verify();
      const file = fileFor(roots, logical);
      const now = hash(file);
      need(now === beforeHashFor(logical, before), 'SOURCE_DRIFT_DURING_REPLACE');
      atomicReplace(file, Buffer.from(plan.target_bytes[logical], 'base64'), writer, plan.event_id);
      fault(`replace:${logical}`);
    }
    need(sourceHash(sourceTuple(roots)) === plan.after_source_sha256, 'AFTER_SOURCE_DRIFT');
    await checkGate(probe, roots, plan, stopSha, globalStopSha, releaseGuard,
      admissionFence);
    safeCreate(path.join(where.event, 'manual-amendment.json'), amendment, writer);
    fault('amendment');
    safeCreate(where.receipt, receipt, writer);
    fault('receipt');
    lease.verify();
    verifiedGuard(globalFence, 'GLOBAL_QUEUE_FENCE_LOST');
    await checkGate(probe, roots, plan, stopSha, globalStopSha, releaseGuard,
      admissionFence);
    need(sourceHash(sourceTuple(roots)) === plan.after_source_sha256, 'PRECOMMIT_SOURCE_DRIFT');
    const indexFile = path.join(where.event, 'index.json');
    const indexTemp = path.join(where.event, `index.json.a01-${plan.event_id}.new`);
    need(!exists(indexFile), 'INDEX_ALREADY_EXISTS');
    safeCreate(indexTemp, index, writer);
    fault('index-temp');
    writer.verify();
    need(!exists(indexFile), 'INDEX_ALREADY_EXISTS');
    fs.renameSync(indexTemp, indexFile); // 105 tip is atomically published LAST.
    syncDirectory(where.event);
    fault('index');
    need(hash(path.join(where.event, 'index.json')) === indexSha
      && sourceHash(sourceTuple(roots)) === plan.after_source_sha256
      && hash(path.join(where.doc, 'intent.json')) === sha(intent)
      && hash(path.join(where.work, 'intent.json')) === sha(intent)
      && sha(stopBytes(roots, { a01_stop_sha256: stopSha,
        global_stop_sha256: globalStopSha })) === stopSha,
    'POSTCOMMIT_READBACK_DRIFT');
    return { status: 'HOLD_PENDING_INDEPENDENT_READBACK', event_id: plan.event_id,
      index_sha256: indexSha, after_source_sha256: plan.after_source_sha256 };
  } finally {
    lease.release(); // STOP and journals intentionally retained.
  }
}
function beforeHashFor(logical, before) {
  if (logical.endsWith('/auto.json')) return before.auto;
  if (logical.endsWith('/series.json')) return before.series;
  if (logical.endsWith('/video.json')) return before.video;
  return before.chapters[path.basename(logical, '.json')];
}

/** Read-only decision. Never infers a retry from a partial write. */
export function inspectRecovery({ roots, plan, grant, syntheticTestPins }) {
  safeRoots(roots);
  validateTarget(roots, plan, selectedPins(syntheticTestPins));
  ownerGrant(grant, roots, plan, planHash(plan));
  const where = paths(roots, plan.event_id);
  const eventIndex = path.join(where.event, 'index.json');
  const present = { docs_intent: exists(path.join(where.doc, 'intent.json')),
    work_intent: exists(path.join(where.work, 'intent.json')),
    index: exists(eventIndex) };
  const oldIndex = path.join(auditRoot(roots), plan.old_event_id, 'index.json');
  need(hash(oldIndex) === plan.old_index_sha256, 'OLD_INDEX_DRIFT');
  const expectedIndex = sha(expectedEventArtifacts(plan, JSON.parse(regular(oldIndex)).after,
    grant).index);
  const indexMatches = present.index && hash(eventIndex) === expectedIndex;
  const files = Object.fromEntries(changedPaths().map((logical) =>
    [logical, hash(fileFor(roots, logical))]));
  const old = plan.before_files_sha256;
  const allBefore = changedPaths().every((logical) => files[logical] === old[logical]);
  const allAfter = changedPaths().every((logical) =>
    files[logical] === plan.changed_files_sha256[logical]);
  const mixedButKnown = changedPaths().every((logical) =>
    [old[logical], plan.changed_files_sha256[logical]].includes(files[logical]));
  return { status: present.index && indexMatches && allAfter ? 'INDEX_PRESENT_VERIFY_INDEPENDENTLY'
    : present.index ? 'HOLD_INDEX_OR_SOURCE_MISMATCH'
      : allBefore ? 'HOLD_NO_SOURCE_CHANGE'
        : mixedButKnown ? 'HOLD_PARTIAL_REQUIRES_EXPLICIT_RECOVERY'
          : 'HOLD_UNKNOWN_DRIFT',
    present, index_matches: indexMatches, all_before: allBefore,
    all_after: allAfter, mixed_but_known: mixedButKnown,
    expected_index_sha256: expectedIndex,
    file_sha256: files };
}

/**
 * Exact-byte rollback of a PRE-INDEX partial write only. Requires a fresh
 * separately scoped recovery grant; keeps both intents, backups and STOP.
 * It never replays the forward install or removes an audit file.
 */
export async function recoverBefore({ roots, plan, grant, probe, globalFence, releaseGuard,
  admissionFence, adoptionGrant, syntheticTestPins,
  fault = () => {} }) {
  safeRoots(roots);
  validateTarget(roots, plan, selectedPins(syntheticTestPins));
  ownerGrant(adoptionGrant, roots, plan, planHash(plan));
  need(grant?.approved === true && grant.kind === 'a01_explicit_preindex_recovery'
    && grant.event_id === plan.event_id
    && grant.plan_sha256 === planHash(plan)
    && JSON.stringify([...grant.write_paths].sort()) ===
      JSON.stringify([
        ...changedPaths().flatMap((logical) => {
          const file = fileFor(roots, logical);
          return [file, `${file}.a01-${plan.event_id}-restore.new`];
        }),
        ...[paths(roots, plan.event_id).doc, paths(roots, plan.event_id).work]
          .map((dir) => path.join(dir, 'recovery.json')),
        path.join(roots.work, SLUG, 'LEASE'),
      ].sort()),
  'EXACT_RECOVERY_GRANT_REQUIRED');
  const where = paths(roots, plan.event_id);
  need(!exists(path.join(where.event, 'index.json')), 'INDEX_PRESENT_NO_ROLLBACK');
  need(globalFence?.kind === 'reviewed_global_queue_worker_fence'
    && typeof globalFence.verify === 'function'
    && HASH.test(globalFence.global_stop_sha256), 'GLOBAL_QUEUE_FENCE_REQUIRED');
  need(releaseGuard?.kind === 'reviewed_self_owned_release_hold_and_four_locks'
    && typeof releaseGuard.verify === 'function'
    && HASH.test(releaseGuard.hold_sha256)
    && path.isAbsolute(releaseGuard.release_dir), 'SELF_OWNED_RELEASE_GUARD_REQUIRED');
  need(admissionFence?.kind === 'reviewed_durable_a01_db_admission_fence'
    && HASH.test(admissionFence.token)
    && typeof admissionFence.verify === 'function',
  'DURABLE_A01_DB_ADMISSION_FENCE_REQUIRED');
  verifiedGuard(releaseGuard, 'SELF_OWNED_RELEASE_GUARD_LOST');
  verifiedGuard(globalFence, 'GLOBAL_QUEUE_FENCE_LOST');
  const lease = freshProjectLease(path.join(roots.work, SLUG),
    'a01-r23-preindex-recovery');
  try {
    const writer = { verify() {
      verifiedGuard(globalFence, 'GLOBAL_QUEUE_FENCE_LOST');
      verifiedGuard(releaseGuard, 'SELF_OWNED_RELEASE_GUARD_LOST');
      verifiedGuard(admissionFence, 'A01_DB_ADMISSION_FENCE_LOST');
      lease.verify();
      need(!exists(path.join(where.event, 'index.json')), 'INDEX_PRESENT_NO_ROLLBACK');
      need(sha(regular(path.join(roots.work, SLUG, 'STOP'))) === plan.a01_stop_sha256,
        'SCOPED_STOP_CHANGED_DURING_RECOVERY');
      need(sha(regular(path.join(roots.work, 'STOP'))) === globalFence.global_stop_sha256,
        'GLOBAL_STOP_CHANGED_DURING_RECOVERY');
    } };
    await checkGate(probe, roots, plan, plan.a01_stop_sha256,
      globalFence.global_stop_sha256, releaseGuard, admissionFence);
    assertOldAudit(roots, plan, { allowPendingEvent: true, grant: adoptionGrant });
    const state = inspectRecovery({ roots, plan, grant: adoptionGrant, syntheticTestPins });
    need(!state.present.index, 'INDEX_PRESENT_NO_ROLLBACK');
    need(state.mixed_but_known && state.present.docs_intent && state.present.work_intent,
      'UNKNOWN_OR_MISSING_INTENT_REFUSED');
    const first = regular(path.join(where.doc, 'intent.json'));
    need(first.equals(regular(path.join(where.work, 'intent.json'))), 'DUAL_INTENT_DRIFT');
    const intent = JSON.parse(first);
    need(intent.schema_version === 1 && intent.kind === 'a01_adoption_intent'
      && intent.slug === SLUG && intent.event_id === plan.event_id
      && intent.plan_sha256 === planHash(plan)
      && intent.owner_grant_sha256 === sha(json(adoptionGrant))
      && intent.owner_approval_ref === adoptionGrant.owner_approval_ref
      && intent.before_source_sha256 === plan.before_source_sha256
      && intent.after_source_sha256 === plan.after_source_sha256
      && intent.event_index_sha256 === state.expected_index_sha256,
    'INTENT_NOT_THIS_PLAN');
    for (const logical of changedPaths()) {
      const expected = plan.before_files_sha256[logical];
      const docsCopy = regular(path.join(where.doc, 'before', logical));
      const workCopy = regular(path.join(where.work, 'before', logical));
      need(sha(docsCopy) === expected && workCopy.equals(docsCopy), 'DUAL_BACKUP_DRIFT');
    }
    for (const logical of changedPaths()) {
      verifiedGuard(globalFence, 'GLOBAL_QUEUE_FENCE_LOST');
      lease.verify();
      need(!exists(path.join(where.event, 'index.json')), 'INDEX_PRESENT_NO_ROLLBACK');
      await checkGate(probe, roots, plan, plan.a01_stop_sha256,
        globalFence.global_stop_sha256, releaseGuard, admissionFence);
      need(!exists(path.join(where.event, 'index.json')), 'INDEX_PRESENT_NO_ROLLBACK');
      const file = fileFor(roots, logical);
      if (hash(file) !== plan.before_files_sha256[logical]) {
        atomicReplace(file, regular(path.join(where.work, 'before', logical)), writer,
          `${plan.event_id}-restore`);
        fault(`restore:${logical}`);
      }
    }
    need(sourceHash(sourceTuple(roots)) === plan.before_source_sha256,
      'RECOVERY_READBACK_DRIFT');
    assertOldAudit(roots, plan, { allowPendingEvent: true, grant: adoptionGrant });
    need(!exists(path.join(where.event, 'index.json')), 'INDEX_PRESENT_NO_ROLLBACK');
    const receipt = json({ schema_version: 1, kind: 'a01_preindex_recovery',
      slug: SLUG, event_id: plan.event_id, plan_sha256: planHash(plan),
      before_source_sha256: plan.before_source_sha256,
      retained_intents: true, retained_stop: true, requires_new_plan: true });
    for (const dir of [where.doc, where.work]) {
      safeCreate(path.join(dir, 'recovery.json'), receipt, writer);
    }
    return { status: 'HOLD_RECOVERED_BEFORE_104', source_sha256: plan.before_source_sha256 };
  } finally { lease.release(); }
}
