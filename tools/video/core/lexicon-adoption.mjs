// A deliberately narrow bridge for X10, whose reviewed script was composed in docs rather than
// written by the story worker. It has no worker chapters or auto.json to migrate. The operator
// must identify the actual media workbase and review the exact script, plan and shared dictionary
// bytes before a first speech request. This never manufactures worker state.
import { createHash, randomUUID } from "node:crypto";
import { closeSync, existsSync, fsyncSync, lstatSync, mkdirSync, openSync, readFileSync, readdirSync, realpathSync, renameSync, unlinkSync, writeFileSync } from "node:fs";
import path from "node:path";

import { genesisBytes, storyPlanNames } from "./lexicon-migration.mjs";
import { videoLexicon, withLexiconWriter } from "./lexicon-store.mjs";
import { docDir, isInside, lexiconFile, stopRequested } from "./paths.mjs";
import { acquireProjectLease } from "./project-lease.mjs";
import { planInitialStoryLexicon, readStoryLexicon, STORY_LEXICON_DIRECTORY, StoryLexiconError } from "./story-lexicon.mjs";

export const ADOPTION_SLUG = "story-everyday-ebay-paypal-x10";
export const ADOPTION_REASON = "manual_story_before_speech";
const REVIEW_KIND = "manual_story_lexicon_adoption_review";
const REVIEW_KEYS = ["confirmed_no_prior_speech", "independent", "kind", "lexicon_sha256", "reviewed_at", "reviewer", "schema_version", "series_sha256", "shared_sha256", "slug", "video_sha256", "workbase"];
const HASH = /^[0-9a-f]{64}$/;
const hash = bytes => createHash("sha256").update(bytes).digest("hex");
const json = value => Buffer.from(`${JSON.stringify(value, null, 2)}\n`);
const fail = (code, detail = "") => { throw new StoryLexiconError(code, detail); };
const intentFile = dir => path.join(dir, STORY_LEXICON_DIRECTORY, "pending.json");
const intentsDir = workdir => path.join(workdir, "story", "lexicon-intents");
const regularFile = file => existsSync(file) && lstatSync(file).isFile() && !lstatSync(file).isSymbolicLink();

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

function docsProof(dir, slug) {
  const videoFile = path.join(dir, "video.json");
  const seriesFile = path.join(dir, "series.json");
  if (!regularFile(videoFile) || !regularFile(seriesFile)) return { error: "video.json and series.json must be regular files" };
  try {
    const videoBytes = readFileSync(videoFile);
    const seriesBytes = readFileSync(seriesFile);
    const video = JSON.parse(videoBytes);
    const series = JSON.parse(seriesBytes);
    if (video?.slug !== slug || series?.kind !== "story" || !Array.isArray(series.names)
        || JSON.stringify(series.names) !== JSON.stringify(["eBay", "PayPal"]))
      return { error: "video.json must name X10 and series.json must be the eBay/PayPal story plan" };
    return { video_sha256: hash(videoBytes), series_sha256: hash(seriesBytes) };
  } catch { return { error: "video.json or series.json is not readable JSON" }; }
}

function workbaseProof(root, workdir) {
  const base = path.dirname(workdir);
  if (isInside(workdir, root)) return "the media work directory is inside the repository";
  if (!existsSync(base) || !lstatSync(base).isDirectory() || lstatSync(base).isSymbolicLink()) return "the explicit media workbase must already be a real directory";
  if (realpathSync(base) !== path.resolve(base)) return "the media workbase must not pass through a symlink";
  const workdirStat = lstatSync(workdir, { throwIfNoEntry: false });
  if (workdirStat && (!workdirStat.isDirectory() || workdirStat.isSymbolicLink())) return "the story work directory is not a real directory";
  return null;
}

function workFiles(workdir, underOwnLease) {
  if (!existsSync(workdir) || !lstatSync(workdir).isDirectory()) return [];
  return readdirSync(workdir).filter(name => !(underOwnLease && name === "LEASE"));
}

/** Every admission check is run before a lease and again under both leases. */
export function adoptionChecks({ root, slug, workdir, underOwnLease = false }) {
  const dir = docDir(slug, root);
  const docs = docsProof(dir, slug);
  const baseError = workbaseProof(root, workdir);
  const entries = workFiles(workdir, underOwnLease);
  const pendingWork = existsSync(intentsDir(workdir));
  const check = (id, ok, code, detail = "") => ({ id, ok, code, detail });
  return {
    docs,
    checks: [
      check("x10_only", slug === ADOPTION_SLUG, "STORY_LEXICON_ADOPTION_SLUG_UNSUPPORTED"),
      check("explicit_real_workbase", !baseError, "STORY_LEXICON_ADOPTION_WORKBASE_UNPROVEN", baseError ?? ""),
      check("manual_story_docs", !docs.error, "STORY_LEXICON_ADOPTION_DOCS_UNPROVEN", docs.error ?? ""),
      check("no_pending_transaction", !existsSync(intentFile(dir)) && !pendingWork, "LEXICON_TRANSACTION_INCOMPLETE"),
      check("no_stop", !stopRequested(workdir), "LEXICON_STOPPED"),
      check("no_worker_state", !existsSync(path.join(workdir, "auto.json")) && !existsSync(path.join(workdir, "story", "chapters")), "STORY_LEXICON_ADOPTION_WORKER_STATE_PRESENT"),
      check("no_recheck_audit", !existsSync(path.join(workdir, "story", "recheck-audit")), "STORY_LEXICON_ADOPTION_AUDIT_PRESENT"),
      check("no_timeline", !existsSync(path.join(workdir, "timeline.json")), "STORY_LEXICON_ADOPTION_TIMELINE_PRESENT"),
      check("no_audio", !existsSync(path.join(workdir, "audio")) && !existsSync(path.join(workdir, "narration.wav")), "STORY_LEXICON_ADOPTION_AUDIO_PRESENT"),
      check("no_approvals", !existsSync(path.join(workdir, "approvals.json")), "STORY_LEXICON_ADOPTION_APPROVAL_PRESENT"),
      check("no_other_work_artifacts", entries.length === 0, "STORY_LEXICON_ADOPTION_WORKDIR_NOT_EMPTY", entries.join(", ")),
    ],
  };
}

function reviewTemplate({ slug, workdir, docs, genesis, snapshot }) {
  return {
    schema_version: 1, kind: REVIEW_KIND, slug, workbase: path.dirname(workdir),
    video_sha256: docs.video_sha256, series_sha256: docs.series_sha256,
    shared_sha256: genesis.shared_sha256, lexicon_sha256: snapshot.lexicon_sha256,
    confirmed_no_prior_speech: false, independent: false, reviewer: "", reviewed_at: "",
  };
}

function reviewProblem(bytes, template, now) {
  let review;
  try { review = JSON.parse(bytes); } catch { return "review is not JSON"; }
  if (!review || typeof review !== "object" || Array.isArray(review)
      || JSON.stringify(Object.keys(review).sort()) !== JSON.stringify(REVIEW_KEYS)) return "review fields do not match the template";
  for (const field of ["schema_version", "kind", "slug", "workbase", "video_sha256", "series_sha256", "shared_sha256", "lexicon_sha256"])
    if (review[field] !== template[field]) return `${field} differs from the current dry-run template`;
  if (review.confirmed_no_prior_speech !== true || review.independent !== true) return "confirm no prior speech and an independent review explicitly";
  if (typeof review.reviewer !== "string" || !review.reviewer.trim() || review.reviewer.length > 100
      || /worker|writer|listener|checker|automation|auto|self|system|pipeline|bot/i.test(review.reviewer)) return "reviewer must identify an independent person or agent";
  if (typeof review.reviewed_at !== "string" || !/^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?(?:Z|[+-]\d\d:\d\d)$/.test(review.reviewed_at)
      || !Number.isFinite(Date.parse(review.reviewed_at)) || Date.parse(review.reviewed_at) > now().getTime()) return "reviewed_at must be a past ISO 8601 time with timezone";
  return null;
}

/** Read-only report and a template whose hash fields must survive until apply. */
export function inspectManualStoryAdoption({ root, slug, workdir, reviewBytes = null, now = () => new Date(), underOwnLease = false }) {
  const { docs, checks } = adoptionChecks({ root, slug, workdir, underOwnLease });
  let previous = null;
  try { previous = videoLexicon({ root, slug, workdir }); }
  catch (error) { checks.unshift({ id: "story_lexicon_readable", ok: false, code: error?.code ?? "STORY_LEXICON_UNREADABLE", detail: error.message }); }
  if (previous?.mode === "snapshot")
    return { slug, status: "already_pinned", allowed: false, checks: [], lexicon_sha256: previous.lexicon_sha256 };
  let genesis = null;
  let snapshot = null;
  try {
    if (!regularFile(lexiconFile(root))) fail("SHARED_LEXICON_UNSAFE");
    genesis = genesisBytes(root, storyPlanNames(docDir(slug, root)));
    snapshot = planInitialStoryLexicon({ slug, sharedBytes: genesis.bytes });
    if (!HASH.test(genesis.shared_sha256 ?? "")) fail("SHARED_LEXICON_UNSAFE");
  } catch (error) { checks.push({ id: "shared_lexicon_valid", ok: false, code: error?.code ?? "SHARED_LEXICON_INVALID", detail: error.message }); }
  const template = !docs.error && genesis && snapshot ? reviewTemplate({ slug, workdir, docs, genesis, snapshot }) : null;
  if (reviewBytes !== null && template) {
    const problem = reviewProblem(reviewBytes, template, now);
    checks.push({ id: "review_matches_current_bytes", ok: !problem, code: "STORY_LEXICON_ADOPTION_REVIEW_INVALID", detail: problem ?? "" });
  } else if (reviewBytes !== null) {
    checks.push({ id: "review_matches_current_bytes", ok: false, code: "STORY_LEXICON_ADOPTION_REVIEW_INVALID", detail: "cannot validate review until docs and dictionary are readable" });
  }
  const eligible = checks.every(check => check.ok);
  return {
    slug, status: eligible ? reviewBytes === null ? "needs_review" : "allowed" : "refused",
    allowed: eligible && reviewBytes !== null, checks, template,
    names: storyPlanNames(docDir(slug, root)), seeded_terms: genesis?.seeded ?? [],
    shared_sha256: genesis?.shared_sha256 ?? null, lexicon_sha256: snapshot?.lexicon_sha256 ?? null,
    head_event_sha256: snapshot?.head_event_sha256 ?? null,
  };
}

function admit(report) {
  const failed = report.checks.filter(check => !check.ok);
  if (failed.length) fail(failed[0].code, failed.map(check => `${check.id}${check.detail ? ` (${check.detail})` : ""}`).join("; "));
}

/** The only write path: refuse before any lease, recheck under both, then publish and read back. */
export function adoptManualStoryLexicon({ root, slug, workdir, reviewFile, now = () => new Date(), checkpoint = () => {} }) {
  if (!reviewFile) fail("STORY_LEXICON_ADOPTION_REVIEW_REQUIRED");
  const reviewed = readFileSync(reviewFile);
  const before = inspectManualStoryAdoption({ root, slug, workdir, reviewBytes: reviewed, now });
  if (before.status === "already_pinned") return { ...videoLexicon({ root, slug, workdir, requireSnapshot: true }), adopted: false };
  admit(before);
  const lease = acquireProjectLease(workdir, { owner: "story-lexicon-adoption" });
  try {
    return withLexiconWriter(root, () => {
      lease.verify();
      const dir = docDir(slug, root);
      const currentReview = readFileSync(reviewFile);
      if (!currentReview.equals(reviewed)) fail("STORY_LEXICON_ADOPTION_REVIEW_CHANGED");
      const report = inspectManualStoryAdoption({ root, slug, workdir, reviewBytes: currentReview, now, underOwnLease: true });
      admit(report);
      if (report.status === "already_pinned") return { ...videoLexicon({ root, slug, dir, workdir, requireSnapshot: true }), adopted: false };
      const genesis = genesisBytes(root, report.names);
      const snapshot = planInitialStoryLexicon({ slug, sharedBytes: genesis.bytes });
      if (snapshot.lexicon_sha256 !== report.lexicon_sha256) fail("STORY_LEXICON_ADOPTION_SOURCE_CHANGED");
      const reviewSha256 = hash(currentReview);
      const record = json({
        schema_version: 1, kind: "story_lexicon_adoption", reason: ADOPTION_REASON, slug,
        event_sha256: snapshot.head_event_sha256, lexicon_sha256: snapshot.lexicon_sha256,
        video_sha256: report.template.video_sha256, series_sha256: report.template.series_sha256,
        shared_sha256: genesis.shared_sha256, seeded_terms: genesis.seeded,
        workbase: report.template.workbase, review_sha256: reviewSha256,
        preconditions: report.checks.map(check => check.id), adopted_at: now().toISOString(),
      });
      const id = randomUUID();
      const intent = { schema_version: 1, id, slug, before_sha256: genesis.shared_sha256,
        after_sha256: snapshot.lexicon_sha256, head_event_sha256: snapshot.head_event_sha256, sequence: snapshot.sequence,
        adoption: ADOPTION_REASON, adoption_sha256: hash(record), review_sha256: reviewSha256,
        video_sha256: report.template.video_sha256, series_sha256: report.template.series_sha256 };
      const workIntent = path.join(intentsDir(workdir), `${id}.json`);
      durable(workIntent, json(intent), { immutable: true });
      checkpoint("work-intent");
      durable(intentFile(dir), json(intent), { immutable: true });
      checkpoint("docs-intent");
      const base = path.join(dir, STORY_LEXICON_DIRECTORY);
      for (const file of snapshot.files.filter(file => file.relative !== "current.json"))
        durable(path.join(base, file.relative), file.bytes, { immutable: true });
      const adoptionFile = path.join(base, "adoptions", `${snapshot.head_event_sha256}.json`);
      const reviewCopy = path.join(base, "adoptions", "reviews", `${reviewSha256}.json`);
      durable(reviewCopy, currentReview, { immutable: true });
      durable(adoptionFile, record, { immutable: true });
      checkpoint("immutable-files");
      const pointer = snapshot.files.find(file => file.relative === "current.json");
      durable(path.join(base, "current.json"), pointer.bytes);
      checkpoint("current-pointer");
      const pinned = readCommitted({ root, slug, dir, snapshot, adoptionFile, reviewCopy, intent });
      durable(path.join(workdir, "story", "lexicon-transactions", `${id}.json`),
        json({ ...intent, status: "committed", current_sha256: hash(pointer.bytes) }), { immutable: true });
      checkpoint("work-receipt");
      unlinkSync(intentFile(dir));
      checkpoint("docs-intent-cleared");
      unlinkSync(workIntent);
      return { ...pinned, adopted: true, transaction_id: id, adoption_sha256: hash(record) };
    });
  } finally { lease.release(); }
}

function readCommitted({ root, slug, dir, snapshot, adoptionFile, reviewCopy, intent }) {
  const current = readStoryLexicon({ slug, storyDir: dir, sharedFile: lexiconFile(root) });
  const docs = docsProof(dir, slug);
  if (current.lexicon_sha256 !== snapshot.lexicon_sha256 || current.head_event_sha256 !== snapshot.head_event_sha256
      || docs.video_sha256 !== intent.video_sha256 || docs.series_sha256 !== intent.series_sha256
      || hash(readFileSync(adoptionFile)) !== intent.adoption_sha256
      || hash(readFileSync(reviewCopy)) !== intent.review_sha256)
    fail("LEXICON_COMMIT_READBACK_FAILED");
  return current;
}
