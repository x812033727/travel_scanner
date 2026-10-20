// Pin a reviewed, manually composed story before any media or worker state exists.
// This is deliberately separate from both worker genesis and the migration of old
// worker chapters: neither path can prove the provenance of a manual video.json.
import { createHash, randomUUID } from "node:crypto";
import { closeSync, existsSync, fsyncSync, lstatSync, mkdirSync, openSync, readFileSync, readdirSync, realpathSync, renameSync, unlinkSync, writeFileSync } from "node:fs";
import path from "node:path";

import { genesisBytes } from "./lexicon-migration.mjs";
import { recoverCommittedStoryLexicon, videoLexicon, withLexiconWriter } from "./lexicon-store.mjs";
import { docDir, isInside, lexiconFile, stopRequested } from "./paths.mjs";
import { acquireProjectLease } from "./project-lease.mjs";
import { planInitialStoryLexicon, readStoryLexicon, STORY_LEXICON_DIRECTORY, StoryLexiconError } from "./story-lexicon.mjs";

export const MANUAL_BOOTSTRAP_REASON = "reviewed_unspoken_manual_draft";
const HASH = /^[0-9a-f]{64}$/;
const UUID = /^[0-9a-f-]{36}$/;
const ROLES = new Set(["source", "narrative_a", "narrative_b"]);
const digest = bytes => createHash("sha256").update(bytes).digest("hex");
const json = value => Buffer.from(`${JSON.stringify(value, null, 2)}\n`);
const fail = (code, detail = "") => { throw new StoryLexiconError(code, detail); };
const pendingFile = dir => path.join(dir, STORY_LEXICON_DIRECTORY, "pending.json");
const intentsDir = workdir => path.join(workdir, "story", "lexicon-intents");
const sidecarRelative = eventSha => path.join("manual-bootstraps", `${eventSha}.json`);

function durable(file, bytes, { immutable = false } = {}) {
  mkdirSync(path.dirname(file), { recursive: true });
  if (immutable && existsSync(file)) {
    if (!readFileSync(file).equals(bytes)) fail("LEXICON_IMMUTABLE_COLLISION");
    return;
  }
  const temporary = immutable ? file : `${file}.${randomUUID()}.tmp`;
  const fd = openSync(temporary, "wx");
  try { writeFileSync(fd, bytes); fsyncSync(fd); } finally { closeSync(fd); }
  if (!immutable) renameSync(temporary, file);
  if (process.platform !== "win32") {
    const directory = openSync(path.dirname(file), "r");
    try { fsyncSync(directory); } finally { closeSync(directory); }
  }
}

function regularBytes(file, code) {
  let stat;
  try { stat = lstatSync(file); } catch { fail(code, file); }
  if (!stat.isFile() || stat.isSymbolicLink()) fail(code, file);
  return readFileSync(file);
}

function parsed(bytes, code) {
  try { return JSON.parse(bytes.toString("utf8")); } catch { fail(code); }
}

function pathSafetyProblem(workdir, root) {
  if (isInside(workdir, root)) return "the media work directory is inside the repository";
  // Resolve the nearest existing ancestor before writing the project LEASE. A symlinked
  // media base can point back into docs/ even when its lexical path looks external.
  let nearest = path.resolve(workdir);
  const missing = [];
  while (true) {
    try {
      const stat = lstatSync(nearest);
      if (stat.isSymbolicLink()) return `a media path ancestor is a symlink: ${nearest}`;
      break;
    } catch (error) {
      if (error.code !== "ENOENT") throw error;
      const parent = path.dirname(nearest);
      if (parent === nearest) return "the media path has no existing ancestor";
      missing.unshift(path.basename(nearest));
      nearest = parent;
    }
  }
  for (let ancestor = path.dirname(nearest); ; ancestor = path.dirname(ancestor)) {
    if (lstatSync(ancestor).isSymbolicLink()) return `a media path ancestor is a symlink: ${ancestor}`;
    if (path.dirname(ancestor) === ancestor) break;
  }
  const physical = path.resolve(realpathSync(nearest), ...missing);
  if (isInside(physical, realpathSync(root))) return "the resolved media work directory is inside the repository";
  return null;
}

function workdirProblem(workdir, allowLease) {
  let stat;
  try { stat = lstatSync(workdir); }
  catch (error) { if (error.code === "ENOENT") return null; throw error; }
  if (!stat.isDirectory() || stat.isSymbolicLink()) return "the media work directory is not a real directory";
  const entries = readdirSync(workdir).filter(name => !(allowLease && name === "LEASE"));
  return entries.length ? `the media work directory already has state: ${entries.join(", ")}` : null;
}

function reviewEvidence({ dir, slug, reviewFile, videoSha, seriesSha }) {
  const reviewsDir = path.join(dir, "reviews");
  let reviewsStat;
  try { reviewsStat = lstatSync(reviewsDir); } catch { fail("MANUAL_BOOTSTRAP_REVIEW_UNSAFE", reviewsDir); }
  if (!reviewsStat.isDirectory() || reviewsStat.isSymbolicLink()
      || !reviewFile || path.dirname(reviewFile) !== reviewsDir) fail("MANUAL_BOOTSTRAP_REVIEW_UNSAFE", String(reviewFile ?? "(missing)"));
  const bytes = regularBytes(reviewFile, "MANUAL_BOOTSTRAP_REVIEW_UNSAFE");
  const receipt = parsed(bytes, "MANUAL_BOOTSTRAP_REVIEW_INVALID");
  const keys = Object.keys(receipt).sort();
  const expected = ["decision", "evidence", "kind", "reviewer", "schema_version", "series_json_sha256", "slug", "video_json_sha256"];
  if (JSON.stringify(keys) !== JSON.stringify(expected) || receipt.schema_version !== 1
      || receipt.kind !== "manual_story_lexicon_bootstrap_review" || receipt.slug !== slug
      || receipt.decision !== "pin_unspoken_manual_draft" || typeof receipt.reviewer !== "string"
      || !receipt.reviewer.trim() || receipt.video_json_sha256 !== videoSha
      || receipt.series_json_sha256 !== seriesSha || !Array.isArray(receipt.evidence)
      || receipt.evidence.length !== ROLES.size) fail("MANUAL_BOOTSTRAP_REVIEW_INVALID");
  const seen = new Set();
  const seenFiles = new Set();
  const evidence = receipt.evidence.map(entry => {
    if (!entry || JSON.stringify(Object.keys(entry).sort()) !== JSON.stringify(["file", "role", "sha256"])
        || !ROLES.has(entry.role) || seen.has(entry.role) || typeof entry.file !== "string"
        || !HASH.test(entry.sha256)) fail("MANUAL_BOOTSTRAP_REVIEW_INVALID", "evidence fields or roles");
    seen.add(entry.role);
    const file = path.resolve(dir, entry.file);
    if (path.dirname(file) !== reviewsDir || file === reviewFile) fail("MANUAL_BOOTSTRAP_REVIEW_UNSAFE", entry.file);
    if (seenFiles.has(file)) fail("MANUAL_BOOTSTRAP_REVIEW_INVALID", "evidence files must be distinct");
    seenFiles.add(file);
    const content = regularBytes(file, "MANUAL_BOOTSTRAP_EVIDENCE_MISSING");
    if (digest(content) !== entry.sha256 || !content.toString("utf8").includes(videoSha))
      fail("MANUAL_BOOTSTRAP_EVIDENCE_STALE", entry.file);
    return { role: entry.role, file: path.relative(dir, file).replaceAll(path.sep, "/"), sha256: entry.sha256 };
  });
  if (seen.size !== ROLES.size) fail("MANUAL_BOOTSTRAP_REVIEW_INVALID", "the three independent evidence roles are required");
  return { review_sha256: digest(bytes), evidence };
}

/** Read-only admission report. Apply repeats every check under both filesystem leases. */
export function inspectManualStoryBootstrap({ root, slug, workdir, reviewFile, allowLease = false }) {
  const dir = docDir(slug, root);
  let current;
  try { current = videoLexicon({ root, slug, dir, workdir }); }
  catch (error) { return { slug, status: "refused", allowed: false, checks: [{ id: "lexicon_readable", ok: false, code: error.code ?? "LEXICON_UNREADABLE", detail: error.message }] }; }
  if (current.mode === "snapshot") return { slug, status: "already_pinned", allowed: false, checks: [], lexicon_sha256: current.lexicon_sha256 };
  const checks = [];
  const check = (id, code, action) => {
    try { const value = action(); checks.push({ id, ok: true }); return value; }
    catch (error) { checks.push({ id, ok: false, code: error.code ?? code, detail: error.message }); return null; }
  };
  check("no_stop", "LEXICON_STOPPED", () => {
    if (stopRequested(workdir) || stopRequested(path.dirname(workdir))) fail("LEXICON_STOPPED");
  });
  check("safe_workdir_path", "MANUAL_BOOTSTRAP_WORKDIR_UNSAFE", () => {
    const unsafe = pathSafetyProblem(workdir, root);
    if (unsafe) fail("MANUAL_BOOTSTRAP_WORKDIR_UNSAFE", unsafe);
  });
  check("empty_workdir", "MANUAL_BOOTSTRAP_WORKDIR_NOT_EMPTY", () => {
    const problem = workdirProblem(workdir, allowLease);
    if (problem) fail("MANUAL_BOOTSTRAP_WORKDIR_NOT_EMPTY", problem);
  });
  const seriesBytes = check("series", "MANUAL_BOOTSTRAP_SERIES_INVALID", () => {
    const bytes = regularBytes(path.join(dir, "series.json"), "MANUAL_BOOTSTRAP_SERIES_INVALID");
    const series = parsed(bytes, "MANUAL_BOOTSTRAP_SERIES_INVALID");
    if (series.kind !== "story" || !Array.isArray(series.names)) fail("MANUAL_BOOTSTRAP_SERIES_INVALID");
    return { bytes, series };
  });
  const videoBytes = check("manual_video", "MANUAL_BOOTSTRAP_VIDEO_INVALID", () => {
    const bytes = regularBytes(path.join(dir, "video.json"), "MANUAL_BOOTSTRAP_VIDEO_INVALID");
    const doc = parsed(bytes, "MANUAL_BOOTSTRAP_VIDEO_INVALID");
    if (doc.slug !== slug || doc.format !== "drama" || doc.series?.slug !== seriesBytes?.series?.slug
        || doc.series?.episode !== seriesBytes?.series?.episode || !Array.isArray(doc.scenes) || !doc.scenes.length)
      fail("MANUAL_BOOTSTRAP_VIDEO_INVALID", "video.json does not match this story plan");
    return bytes;
  });
  const videoSha = videoBytes ? digest(videoBytes) : null;
  const seriesSha = seriesBytes ? digest(seriesBytes.bytes) : null;
  const review = check("review_receipt", "MANUAL_BOOTSTRAP_REVIEW_INVALID", () => {
    if (!videoSha || !seriesSha) fail("MANUAL_BOOTSTRAP_REVIEW_INVALID", "the script and series must be valid first");
    return reviewEvidence({ dir, slug, reviewFile, videoSha, seriesSha });
  });
  const planned = check("genesis_plan", "MANUAL_BOOTSTRAP_GENESIS_INVALID", () => {
    if (!seriesBytes) fail("MANUAL_BOOTSTRAP_GENESIS_INVALID", "series.json is required");
    const genesis = genesisBytes(root, seriesBytes.series.names);
    const snapshot = planInitialStoryLexicon({ slug, sharedBytes: genesis.bytes });
    return { genesis, snapshot };
  });
  return {
    slug, status: checks.every(item => item.ok) ? "allowed" : "refused", allowed: checks.every(item => item.ok), checks,
    video_json_sha256: videoSha, series_json_sha256: seriesSha, review_receipt_sha256: review?.review_sha256 ?? null,
    evidence: review?.evidence ?? [], shared_sha256: planned?.genesis.shared_sha256 ?? null,
    seeded_terms: planned?.genesis.seeded ?? [], lexicon_sha256: planned?.snapshot.lexicon_sha256 ?? null,
    head_event_sha256: planned?.snapshot.head_event_sha256 ?? null,
  };
}

function admit(report) {
  if (!report.allowed) {
    const failed = report.checks.filter(item => !item.ok);
    fail(failed[0]?.code ?? "MANUAL_BOOTSTRAP_REFUSED", failed.map(item => `${item.id}: ${item.detail}`).join("; "));
  }
}

/** Manual source files do not share the media lease, so pin their exact bytes again at each commit boundary. */
function requireSourcesUnchanged({ root, slug, workdir, reviewFile, report }) {
  if (stopRequested(workdir) || stopRequested(path.dirname(workdir))) fail("LEXICON_STOPPED");
  const dir = docDir(slug, root);
  const sources = [
    ["video.json", path.join(dir, "video.json"), report.video_json_sha256],
    ["series.json", path.join(dir, "series.json"), report.series_json_sha256],
    ["review receipt", reviewFile, report.review_receipt_sha256],
    ...report.evidence.map(entry => [entry.role, path.join(dir, entry.file), entry.sha256]),
  ];
  for (const [label, file, expected] of sources) {
    let bytes;
    try { bytes = regularBytes(file, "MANUAL_BOOTSTRAP_SOURCE_CHANGED"); }
    catch (error) { fail("MANUAL_BOOTSTRAP_SOURCE_CHANGED", `${label}: ${error.message}`); }
    if (digest(bytes) !== expected) fail("MANUAL_BOOTSTRAP_SOURCE_CHANGED", label);
  }
  // Also re-check the reviewed relationship and reject a symlinked reviews/ directory.
  let review;
  try { review = reviewEvidence({ dir, slug, reviewFile, videoSha: report.video_json_sha256, seriesSha: report.series_json_sha256 }); }
  catch (error) { fail("MANUAL_BOOTSTRAP_SOURCE_CHANGED", `review evidence: ${error.message}`); }
  if (review.review_sha256 !== report.review_receipt_sha256
      || JSON.stringify(review.evidence) !== JSON.stringify(report.evidence)) fail("MANUAL_BOOTSTRAP_SOURCE_CHANGED", "review evidence");
}

/** Publish standard genesis bytes with an immutable manual-provenance sidecar. */
export function bootstrapManualStoryLexicon({ root, slug, workdir, reviewFile, checkpoint = () => {}, now = () => new Date() }) {
  const before = inspectManualStoryBootstrap({ root, slug, workdir, reviewFile });
  if (before.status === "already_pinned") return { ...videoLexicon({ root, slug, workdir }), bootstrapped: false };
  admit(before);
  const lease = acquireProjectLease(workdir, { owner: "manual-story-lexicon-bootstrap" });
  try {
    return withLexiconWriter(root, () => {
      lease.verify();
      const report = inspectManualStoryBootstrap({ root, slug, workdir, reviewFile, allowLease: true });
      if (report.status === "already_pinned") return { ...videoLexicon({ root, slug, workdir }), bootstrapped: false };
      admit(report);
      const dir = docDir(slug, root);
      const previous = videoLexicon({ root, slug, dir, workdir });
      const series = parsed(regularBytes(path.join(dir, "series.json"), "MANUAL_BOOTSTRAP_SERIES_INVALID"), "MANUAL_BOOTSTRAP_SERIES_INVALID");
      const genesis = genesisBytes(root, series.names);
      const snapshot = planInitialStoryLexicon({ slug, sharedBytes: genesis.bytes });
      if (snapshot.lexicon_sha256 !== report.lexicon_sha256 || snapshot.head_event_sha256 !== report.head_event_sha256)
        fail("MANUAL_BOOTSTRAP_SOURCE_CHANGED");
      const record = json({
        schema_version: 1, kind: "story_lexicon_manual_bootstrap", reason: MANUAL_BOOTSTRAP_REASON, slug,
        event_sha256: snapshot.head_event_sha256, lexicon_sha256: snapshot.lexicon_sha256,
        shared_sha256: genesis.shared_sha256, seeded_terms: genesis.seeded,
        video_json_sha256: report.video_json_sha256, series_json_sha256: report.series_json_sha256,
        review_receipt_sha256: report.review_receipt_sha256, evidence: report.evidence,
        bootstrapped_at: now().toISOString(),
      });
      lease.verify();
      requireSourcesUnchanged({ root, slug, workdir, reviewFile, report });
      const id = randomUUID();
      const workIntent = path.join(intentsDir(workdir), `${id}.json`);
      const receiptFile = path.join(workdir, "story", "lexicon-transactions", `${id}.json`);
      const intent = { schema_version: 1, id, slug, before_sha256: previous.lexicon_sha256,
        after_sha256: snapshot.lexicon_sha256, head_event_sha256: snapshot.head_event_sha256, sequence: snapshot.sequence,
        bootstrap: MANUAL_BOOTSTRAP_REASON, bootstrap_sha256: digest(record) };
      durable(workIntent, json(intent), { immutable: true });
      checkpoint("work-intent");
      durable(pendingFile(dir), json(intent), { immutable: true });
      checkpoint("docs-intent");
      const base = path.join(dir, STORY_LEXICON_DIRECTORY);
      for (const file of snapshot.files.filter(file => file.relative !== "current.json"))
        durable(path.join(base, file.relative), file.bytes, { immutable: true });
      durable(path.join(base, sidecarRelative(snapshot.head_event_sha256)), record, { immutable: true });
      checkpoint("immutable-files");
      const current = snapshot.files.find(file => file.relative === "current.json");
      durable(path.join(base, "current.json"), current.bytes);
      checkpoint("current-pointer");
      const result = readStoryLexicon({ slug, storyDir: dir, sharedFile: lexiconFile(root) });
      if (result.lexicon_sha256 !== snapshot.lexicon_sha256 || result.head_event_sha256 !== snapshot.head_event_sha256
          || digest(readFileSync(path.join(base, sidecarRelative(snapshot.head_event_sha256)))) !== intent.bootstrap_sha256)
        fail("LEXICON_COMMIT_READBACK_FAILED");
      lease.verify();
      requireSourcesUnchanged({ root, slug, workdir, reviewFile, report });
      durable(receiptFile, json({ ...intent, status: "committed", current_sha256: digest(current.bytes) }), { immutable: true });
      checkpoint("work-receipt");
      unlinkSync(pendingFile(dir));
      checkpoint("docs-intent-cleared");
      unlinkSync(workIntent);
      return { ...result, bootstrapped: true, transaction_id: id, review_receipt_sha256: report.review_receipt_sha256 };
    });
  } finally { lease.release(); }
}

/** Recovery is only for a committed transaction whose provenance sidecar still matches. */
export function recoverCommittedManualBootstrap({ root, slug, workdir, transactionId }) {
  if (!UUID.test(transactionId)) fail("LEXICON_TRANSACTION_ID_INVALID");
  const unsafe = pathSafetyProblem(workdir, root);
  if (unsafe) fail("MANUAL_BOOTSTRAP_WORKDIR_UNSAFE", unsafe);
  const lease = acquireProjectLease(workdir, { owner: "manual-story-lexicon-recovery" });
  try {
    return withLexiconWriter(root, () => {
      const file = path.join(workdir, "story", "lexicon-transactions", `${transactionId}.json`);
      const receipt = parsed(regularBytes(file, "MANUAL_BOOTSTRAP_RECEIPT_MISSING"), "MANUAL_BOOTSTRAP_RECEIPT_INVALID");
      if (receipt.id !== transactionId || receipt.slug !== slug || receipt.status !== "committed"
          || receipt.bootstrap !== MANUAL_BOOTSTRAP_REASON || !HASH.test(receipt.bootstrap_sha256)
          || !HASH.test(receipt.head_event_sha256)) fail("MANUAL_BOOTSTRAP_RECEIPT_INVALID");
      const sidecar = path.join(docDir(slug, root), STORY_LEXICON_DIRECTORY, sidecarRelative(receipt.head_event_sha256));
      const record = regularBytes(sidecar, "MANUAL_BOOTSTRAP_SIDECAR_MISSING");
      const value = parsed(record, "MANUAL_BOOTSTRAP_SIDECAR_INVALID");
      if (digest(record) !== receipt.bootstrap_sha256 || value.kind !== "story_lexicon_manual_bootstrap"
          || value.reason !== MANUAL_BOOTSTRAP_REASON || value.slug !== slug
          || value.event_sha256 !== receipt.head_event_sha256 || value.lexicon_sha256 !== receipt.after_sha256)
        fail("MANUAL_BOOTSTRAP_SIDECAR_INVALID");
      return recoverCommittedStoryLexicon({ root, slug, workdir, transactionId });
    });
  } finally { lease.release(); }
}
