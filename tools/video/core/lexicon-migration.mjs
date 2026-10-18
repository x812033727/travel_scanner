// One-time pinning of a story that started before per-story lexicon snapshots existed (#1548).
//
// `initializeStoryLexicon` only pins a story that has not started, so a story that wrote its
// chapters before #1548 was deployed holds with STORY_LEXICON_MIGRATION_REQUIRED. When such a story
// has synthesized no narration yet, nothing has been spoken with the shared dictionary, and pinning
// it now is the same decision genesis would have made: the shared dictionary plus the plan's names.
// This module does exactly that and nothing more (docs/videos/story-lexicon-migration.md).
//
// It never touches a story with a narration timeline, narration audio, an audio-or-later approval or
// a recheck audit. A01 (80 audit events) needs its own reviewed append-only transition.
//
// The transaction mirrors lexicon-store.mjs's `publish` (both leases, durable intents on both
// volumes, immutable files, current pointer, strict read-back, receipt, then clear the intents), so
// `recoverCommittedStoryLexicon` recovers a crashed migration unchanged. The genesis bytes are the
// ones `initializeStoryLexicon` writes (the strict reader accepts no other genesis); the migration
// itself is recorded in an immutable sidecar the reader ignores and in the intent and receipt.
import { createHash, randomUUID } from "node:crypto";
import { closeSync, existsSync, fsyncSync, lstatSync, mkdirSync, openSync, readFileSync, readdirSync, renameSync, unlinkSync, writeFileSync } from "node:fs";
import path from "node:path";

import { emptyLexicon, isProposableTerm } from "./lexicon.mjs";
import { videoLexicon, withLexiconWriter } from "./lexicon-store.mjs";
import { docDir, lexiconFile, readJson, stopRequested } from "./paths.mjs";
import { acquireProjectLease } from "./project-lease.mjs";
import { planInitialStoryLexicon, readStoryLexicon, STORY_LEXICON_DIRECTORY, StoryLexiconError } from "./story-lexicon.mjs";

export const MIGRATION_REASON = "started_before_pinning";
/** Gates that come before any narration is synthesized. Anything else (audio, storyboard, final, publish, dubs, languages, or an unknown gate) refuses. */
export const PRE_NARRATION_GATES = new Set(["outline", "script", "look"]);
/** A01 is never migrated here, whatever its work directory looks like. */
export const EXCLUDED_SLUGS = new Set(["story-rolling-suitcase-v2"]);

const hash = bytes => createHash("sha256").update(bytes).digest("hex");
const json = value => Buffer.from(`${JSON.stringify(value, null, 2)}\n`);
const fail = (code, detail) => { throw new StoryLexiconError(code, detail); };
const pendingFile = dir => path.join(dir, STORY_LEXICON_DIRECTORY, "pending.json");
const intentsDir = workdir => path.join(workdir, "story", "lexicon-intents");
const migrationRelative = eventSha256 => path.join("migrations", `${eventSha256}.json`);

// Same durability rules as lexicon-store.mjs: immutable files are created once and must match.
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

function anyFile(dir) {
  if (!existsSync(dir)) return false;
  if (!lstatSync(dir).isDirectory()) return true;
  return readdirSync(dir, { withFileTypes: true }).some(entry => entry.isDirectory() ? anyFile(path.join(dir, entry.name)) : true);
}

/** Same genesis rule as initializeStoryLexicon: shared bytes, plus each plan name's Latin tokens as `null` when absent. */
export function genesisBytes(root, names) {
  const sharedFile = lexiconFile(root);
  const shared = existsSync(sharedFile) ? readFileSync(sharedFile) : null;
  const base = shared ?? json(emptyLexicon());
  const next = structuredClone(JSON.parse(base));
  const seeded = [];
  const terms = Object.fromEntries(names.flatMap(name => String(name).match(/[A-Za-z][A-Za-z0-9'.+#-]*/g) ?? []).map(term => [term, null]));
  for (const term of Object.keys(terms)) {
    if (!isProposableTerm(term) || Object.hasOwn(next.terms, term)) continue;
    next.terms[term] = null;
    seeded.push(term);
  }
  return { bytes: seeded.length ? json(next) : base, shared_sha256: shared ? hash(shared) : null, seeded };
}

function isStory(dir) {
  return readJson(path.join(dir, "series.json"), null)?.kind === "story"
    || readJson(path.join(dir, "video.json"), null)?.category === "story";
}

/** The names genesis would have seeded: the reviewed story plan's names in series.json. */
export function storyPlanNames(dir) {
  const names = readJson(path.join(dir, "series.json"), null)?.names;
  return Array.isArray(names) ? names.filter(name => typeof name === "string" && name.trim()) : [];
}

/**
 * Positive proof that `workdir` is this story's own work directory, and that the story started there.
 * Every other check reads the work directory and passes on an empty one, so a forgotten
 * VIDEO_WORKDIR or a wrong --workdir must refuse here instead of pinning a story with audio elsewhere.
 */
export function workdirProof(workdir, slug) {
  if (!existsSync(workdir) || !lstatSync(workdir).isDirectory()) return "the work directory does not exist";
  let state;
  try { state = JSON.parse(readFileSync(path.join(workdir, "auto.json"), "utf8")); } catch { return "auto.json is missing or unreadable"; }
  if (state?.slug !== slug) return `auto.json belongs to ${JSON.stringify(state?.slug ?? null)}`;
  if (!state.story || typeof state.story !== "object") return "auto.json has no story state";
  const chapters = path.join(workdir, "story", "chapters");
  if (!existsSync(chapters) || !readdirSync(chapters).some(name => name.endsWith(".json")))
    return "story/chapters has no chapter file (an unstarted story is pinned by the worker's normal genesis)";
  return null;
}

function lateApprovals(workdir) {
  const file = path.join(workdir, "approvals.json");
  if (!existsSync(file)) return [];
  let record;
  try { record = JSON.parse(readFileSync(file, "utf8")); } catch { return ["(approvals.json unreadable)"]; }
  if (!Array.isArray(record?.approvals)) return ["(approvals.json has no approvals list)"];
  return [...new Set(record.approvals.map(entry => String(entry?.gate)).filter(gate => !PRE_NARRATION_GATES.has(gate)))];
}

/**
 * Every precondition, in the order they are enforced, each with the error code it raises.
 * `already_pinned` is not a refusal: a pinned story is returned unchanged.
 */
export function migrationChecks({ root, slug, workdir, dir = docDir(slug, root) }) {
  const pendingIntents = existsSync(intentsDir(workdir)) ? readdirSync(intentsDir(workdir)).filter(name => name.endsWith(".json")) : [];
  const late = lateApprovals(workdir);
  const proof = workdirProof(workdir, slug);
  const audio = [anyFile(path.join(workdir, "audio")) && "audio/", existsSync(path.join(workdir, "narration.wav")) && "narration.wav"].filter(Boolean);
  return [
    { id: "not_excluded", ok: !EXCLUDED_SLUGS.has(slug), code: "STORY_LEXICON_MIGRATION_EXCLUDED", detail: "A01 needs its own reviewed transition" },
    { id: "no_pending_transaction", ok: !existsSync(pendingFile(dir)) && !pendingIntents.length, code: "LEXICON_TRANSACTION_INCOMPLETE", detail: pendingIntents.join(", ") },
    { id: "no_stop", ok: !stopRequested(workdir) && !stopRequested(path.dirname(workdir)), code: "LEXICON_STOPPED" },
    { id: "is_story", ok: isStory(dir), code: "STORY_LEXICON_MIGRATION_NOT_A_STORY" },
    { id: "workdir_is_this_story", ok: !proof, code: "STORY_LEXICON_MIGRATION_WORKDIR_UNPROVEN", detail: proof ?? "" },
    { id: "no_recheck_audit", ok: !existsSync(path.join(workdir, "story", "recheck-audit")), code: "STORY_LEXICON_MIGRATION_AUDIT_PRESENT" },
    { id: "no_timeline", ok: !existsSync(path.join(workdir, "timeline.json")), code: "STORY_LEXICON_MIGRATION_TIMELINE_PRESENT" },
    { id: "no_narration_audio", ok: !audio.length, code: "STORY_LEXICON_MIGRATION_AUDIO_PRESENT", detail: audio.join(", ") },
    { id: "no_audio_or_later_approval", ok: !late.length, code: "STORY_LEXICON_MIGRATION_APPROVAL_PRESENT", detail: late.join(", ") },
  ];
}

function plan({ root, slug, names, now, checks }) {
  const genesis = genesisBytes(root, names);
  const snapshot = planInitialStoryLexicon({ slug, sharedBytes: genesis.bytes });
  const record = json({
    schema_version: 1, kind: "story_lexicon_migration", reason: MIGRATION_REASON, slug,
    event_sha256: snapshot.head_event_sha256, lexicon_sha256: snapshot.lexicon_sha256,
    shared_sha256: genesis.shared_sha256, seeded_terms: genesis.seeded,
    preconditions: checks.map(check => check.id),
    migrated_at: now().toISOString(),
  });
  return { genesis, snapshot, record };
}

/**
 * What a migration would do, without writing: the checks, whether it is allowed, and the snapshot
 * SHA-256 it would pin (null when the shared dictionary cannot be read).
 */
export function inspectStartedStoryMigration({ root, slug, workdir, names }) {
  const dir = docDir(slug, root);
  const current = (() => { try { return readStoryLexicon({ slug, storyDir: dir, sharedFile: lexiconFile(root) }); } catch (error) { return { mode: "unreadable", error }; } })();
  const seeds = names ?? storyPlanNames(dir);
  if (current.mode === "snapshot") return { slug, status: "already_pinned", allowed: false, checks: [], lexicon_sha256: current.lexicon_sha256, names: seeds };
  const checks = migrationChecks({ root, slug, workdir, dir });
  if (current.mode === "unreadable") checks.unshift({ id: "story_lexicon_readable", ok: false, code: current.error?.code ?? "STORY_LEXICON_UNREADABLE", detail: current.error?.message });
  let snapshot = null;
  let genesis = null;
  try { genesis = genesisBytes(root, seeds); snapshot = planInitialStoryLexicon({ slug, sharedBytes: genesis.bytes }); }
  catch (error) { checks.push({ id: "shared_lexicon_valid", ok: false, code: error?.code ?? "SHARED_LEXICON_INVALID", detail: error?.message }); }
  const allowed = checks.every(check => check.ok);
  return {
    slug, status: allowed ? "allowed" : "refused", allowed, checks, names: seeds,
    lexicon_sha256: snapshot?.lexicon_sha256 ?? null, head_event_sha256: snapshot?.head_event_sha256 ?? null,
    shared_sha256: genesis?.shared_sha256 ?? null, seeded_terms: genesis?.seeded ?? [],
  };
}

function admit(checks) {
  const failed = checks.filter(check => !check.ok);
  if (failed.length) fail(failed[0].code, failed.map(check => `${check.id}${check.detail ? ` (${check.detail})` : ""}`).join("; "));
}

/**
 * Pin a started story that has spoken nothing yet. Idempotent: a pinned story is returned as is.
 * Every precondition is re-checked under both leases before anything is written.
 */
export function migrateStartedStoryLexicon({ root, slug, workdir, names, checkpoint = () => {}, now = () => new Date() }) {
  const dir = docDir(slug, root);
  const seeds = names ?? storyPlanNames(dir);
  // Refuse before the leases: acquiring one writes a LEASE file into the work directory.
  if (EXCLUDED_SLUGS.has(slug)) fail("STORY_LEXICON_MIGRATION_EXCLUDED");
  const pinned = (() => { try { return readStoryLexicon({ slug, storyDir: dir, sharedFile: lexiconFile(root) }); } catch { return null; } })();
  // A pinned story is read, never written: this also holds on a pending intent on either volume.
  if (pinned?.mode === "snapshot") return { ...videoLexicon({ root, slug, dir, workdir }), migrated: false };
  admit(migrationChecks({ root, slug, workdir, dir }));
  const lease = acquireProjectLease(workdir, { owner: "story-lexicon-migration" });
  try {
    return withLexiconWriter(root, () => {
      if (EXCLUDED_SLUGS.has(slug)) fail("STORY_LEXICON_MIGRATION_EXCLUDED");
      if (existsSync(pendingFile(dir))) fail("LEXICON_TRANSACTION_INCOMPLETE");
      const previous = videoLexicon({ root, slug, dir, workdir });
      if (previous.mode === "snapshot") return { ...previous, migrated: false };
      const checks = migrationChecks({ root, slug, workdir, dir });
      admit(checks);
      const { snapshot, record, genesis } = plan({ root, slug, names: seeds, now, checks });
      const id = randomUUID();
      const workIntent = path.join(intentsDir(workdir), `${id}.json`);
      const receiptFile = path.join(workdir, "story", "lexicon-transactions", `${id}.json`);
      const intent = { schema_version: 1, id, slug, before_sha256: previous.lexicon_sha256,
        after_sha256: snapshot.lexicon_sha256, head_event_sha256: snapshot.head_event_sha256, sequence: snapshot.sequence,
        migration: MIGRATION_REASON, migration_sha256: hash(record) };
      durable(workIntent, json(intent), { immutable: true });
      checkpoint("work-intent");
      durable(pendingFile(dir), json(intent), { immutable: true });
      checkpoint("docs-intent");
      const base = path.join(dir, STORY_LEXICON_DIRECTORY);
      for (const file of snapshot.files.filter(file => file.relative !== "current.json"))
        durable(path.join(base, file.relative), file.bytes, { immutable: true });
      durable(path.join(base, migrationRelative(snapshot.head_event_sha256)), record, { immutable: true });
      checkpoint("immutable-files");
      const current = snapshot.files.find(file => file.relative === "current.json");
      durable(path.join(base, "current.json"), current.bytes);
      checkpoint("current-pointer");
      const result = readStoryLexicon({ slug, storyDir: dir, sharedFile: lexiconFile(root) });
      if (result.lexicon_sha256 !== snapshot.lexicon_sha256 || result.head_event_sha256 !== snapshot.head_event_sha256
          || hash(readFileSync(path.join(base, migrationRelative(snapshot.head_event_sha256)))) !== intent.migration_sha256)
        fail("LEXICON_COMMIT_READBACK_FAILED");
      durable(receiptFile, json({ ...intent, status: "committed", current_sha256: hash(current.bytes) }), { immutable: true });
      checkpoint("work-receipt");
      unlinkSync(pendingFile(dir));
      checkpoint("docs-intent-cleared");
      unlinkSync(workIntent);
      return { ...result, migrated: true, transaction_id: id, shared_sha256: genesis.shared_sha256, seeded_terms: genesis.seeded };
    });
  } finally { lease.release(); }
}
