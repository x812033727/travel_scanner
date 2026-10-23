// Runtime admission for shared writes and immutable story dictionaries. No live migration CLI.
import { createHash, randomUUID } from "node:crypto";
import { closeSync, existsSync, fsyncSync, mkdirSync, openSync, readFileSync, readdirSync, renameSync, unlinkSync, writeFileSync } from "node:fs";
import path from "node:path";
import { emptyLexicon, isProposableTerm } from "./lexicon.mjs";
import { docDir, lexiconFile, readJson, stopRequested, videosDir } from "./paths.mjs";
import { acquireProjectLease } from "./project-lease.mjs";
import { planInitialStoryLexicon, planStoryLexiconRevision, readStoryLexicon, STORY_LEXICON_DIRECTORY, StoryLexiconError } from "./story-lexicon.mjs";

const hash = bytes => createHash("sha256").update(bytes).digest("hex");
const json = value => Buffer.from(`${JSON.stringify(value, null, 2)}\n`);
const fail = code => { throw new StoryLexiconError(code); };
const pendingFile = dir => path.join(dir, STORY_LEXICON_DIRECTORY, "pending.json");
const intentsDir = workdir => path.join(workdir, "story", "lexicon-intents");

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
  // POSIX requires the directory entry to reach disk too. Windows rejects opening a directory.
  if (process.platform !== "win32") {
    const directory = openSync(path.dirname(file), "r");
    try { fsyncSync(directory); } finally { closeSync(directory); }
  }
}

function pending(dir, workdir) {
  if (existsSync(pendingFile(dir))) fail("LEXICON_TRANSACTION_INCOMPLETE");
  if (workdir && existsSync(intentsDir(workdir)) && readdirSync(intentsDir(workdir)).some(name => name.endsWith(".json")))
    fail("LEXICON_TRANSACTION_INCOMPLETE");
}

/** All shared dictionary writers use this same filesystem lease, including other videos. */
export function withLexiconWriter(root, operation) {
  const lease = acquireProjectLease(path.join(videosDir(root), ".lexicon-writer"), { owner: "lexicon-writer" });
  try {
    const value = operation();
    if (value?.then) fail("LEXICON_WRITER_MUST_BE_SYNCHRONOUS");
    return value;
  } finally { lease.release(); }
}

function additionsTo(lexicon, additions) {
  const next = structuredClone(lexicon);
  const added = [];
  for (const [term, spoken] of Object.entries(additions ?? {})) {
    if (!isProposableTerm(term) || Object.hasOwn(next.terms, term)) continue;
    if (spoken !== null && (typeof spoken !== "string" || !spoken.trim() || spoken.length > 80)) continue;
    next.terms[term] = spoken === null ? null : spoken.trim();
    added.push(term);
  }
  return { next, added };
}

export function mergeSharedLexicon(root, additions) {
  return withLexiconWriter(root, () => {
    const file = lexiconFile(root);
    const { next, added } = additionsTo(readJson(file, emptyLexicon()), additions);
    if (added.length) durable(file, json(next));
    return added;
  });
}

/** Read-only legacy compatibility; a pending transaction never falls back. */
export function videoLexicon({ root, slug, dir = docDir(slug, root), workdir, requireSnapshot = false }) {
  pending(dir, workdir);
  const value = readStoryLexicon({ slug, storyDir: dir, sharedFile: path.join(path.dirname(dir), "lexicon.json") });
  if (requireSnapshot && value.mode !== "snapshot") fail("STORY_LEXICON_MIGRATION_REQUIRED");
  return value;
}

/** Paid callers check under their project lease, including an intent left only on the work volume. */
export function requireStorySpeechLexicon(project, workdir) {
  if (project.series?.kind !== "story" && project.doc.category !== "story"
      && !existsSync(path.join(project.dir, STORY_LEXICON_DIRECTORY))) return;
  const current = videoLexicon({ slug: project.doc.slug, dir: project.dir, workdir, requireSnapshot: true });
  if (JSON.stringify(current.lexicon) !== JSON.stringify(project.shelfLexicon)) fail("LEXICON_PROJECT_STALE");
}

function safeToInitialize(workdir, dir) {
  const story = path.join(workdir, "story");
  const state = readJson(path.join(workdir, "auto.json"), null);
  return !existsSync(path.join(story, "recheck-audit"))
    && !existsSync(path.join(story, "chapters"))
    && !existsSync(path.join(dir, "video.json"))
    && !existsSync(path.join(workdir, "approvals.json"))
    && !existsSync(path.join(workdir, "timeline.json"))
    && !Object.values(state?.story?.chapters ?? {}).some(entry => entry?.written || entry?.checked || entry?.listened);
}

/** Publish under both leases. A crash leaves durable intents and readers HOLD until recovery. */
function publish({ root, slug, workdir, makePlan, initialize = false, checkpoint = () => {} }) {
  const lease = acquireProjectLease(workdir, { owner: "story-lexicon" });
  try {
    return withLexiconWriter(root, () => {
      const dir = docDir(slug, root);
      pending(dir, workdir);
      if (stopRequested(workdir) || stopRequested(path.dirname(workdir))) fail("LEXICON_STOPPED");
      const previous = videoLexicon({ root, slug, dir, workdir });
      if (initialize && previous.mode === "snapshot") return previous;
      if (initialize && !safeToInitialize(workdir, dir)) fail("STORY_LEXICON_MIGRATION_REQUIRED");
      const plan = makePlan(previous);
      const id = randomUUID();
      const workIntent = path.join(intentsDir(workdir), `${id}.json`);
      const receiptFile = path.join(workdir, "story", "lexicon-transactions", `${id}.json`);
      const intent = { schema_version: 1, id, slug, before_sha256: previous.lexicon_sha256,
        after_sha256: plan.lexicon_sha256, head_event_sha256: plan.head_event_sha256, sequence: plan.sequence };
      durable(workIntent, json(intent), { immutable: true });
      checkpoint("work-intent");
      durable(pendingFile(dir), json(intent), { immutable: true });
      checkpoint("docs-intent");
      const base = path.join(dir, STORY_LEXICON_DIRECTORY);
      for (const file of plan.files.filter(file => file.relative !== "current.json"))
        durable(path.join(base, file.relative), file.bytes, { immutable: true });
      checkpoint("immutable-files");
      const current = plan.files.find(file => file.relative === "current.json");
      durable(path.join(base, "current.json"), current.bytes);
      checkpoint("current-pointer");
      // Read the strict complete chain before recording commit. Pending markers fence readers.
      const result = readStoryLexicon({ slug, storyDir: dir, sharedFile: lexiconFile(root) });
      if (result.lexicon_sha256 !== plan.lexicon_sha256 || result.head_event_sha256 !== plan.head_event_sha256)
        fail("LEXICON_COMMIT_READBACK_FAILED");
      durable(receiptFile, json({ ...intent, status: "committed", current_sha256: hash(current.bytes) }), { immutable: true });
      checkpoint("work-receipt");
      unlinkSync(pendingFile(dir));
      checkpoint("docs-intent-cleared");
      unlinkSync(workIntent);
      return result;
    });
  } finally { lease.release(); }
}

/** Only a genuinely unstarted story is automatically pinned; A01's old audit is never migrated here. */
export function initializeStoryLexicon({ root, slug, workdir, checkpoint, names = [] }) {
  const current = videoLexicon({ root, slug, workdir });
  if (current.mode === "snapshot") return current;
  return publish({ root, slug, workdir, initialize: true, checkpoint,
    makePlan: () => {
      const shared = existsSync(lexiconFile(root)) ? readFileSync(lexiconFile(root)) : json(emptyLexicon());
      const terms = Object.fromEntries(names.flatMap(name => String(name).match(/[A-Za-z][A-Za-z0-9'.+#-]*/g) ?? []).map(term => [term, null]));
      const { next, added } = additionsTo(JSON.parse(shared), terms);
      return planInitialStoryLexicon({ slug, sharedBytes: added.length ? json(next) : shared });
    } });
}

/** Explicit reviewed revision. The review hash binds evidence; it is not owner authentication. */
export function reviseStoryLexicon({ root, slug, workdir, nextBytes, reviewSha256, checkpoint }) {
  return publish({ root, slug, workdir, checkpoint,
    makePlan: previous => planStoryLexiconRevision({ slug, previous, nextBytes, reviewSha256 }) });
}

/** Explicit recovery only for a fully committed, byte-matching transaction; partial commits HOLD. */
export function recoverCommittedStoryLexicon({ root, slug, workdir, transactionId }) {
  if (!/^[0-9a-f-]{36}$/.test(transactionId)) fail("LEXICON_TRANSACTION_ID_INVALID");
  const lease = acquireProjectLease(workdir, { owner: "story-lexicon-recovery" });
  try {
    return withLexiconWriter(root, () => {
      if (stopRequested(workdir) || stopRequested(path.dirname(workdir))) fail("LEXICON_STOPPED");
      const dir = docDir(slug, root);
      const workIntent = path.join(intentsDir(workdir), `${transactionId}.json`);
      const receipt = readJson(path.join(workdir, "story", "lexicon-transactions", `${transactionId}.json`), null);
      if (!receipt || receipt.status !== "committed" || receipt.slug !== slug || receipt.id !== transactionId)
        fail("LEXICON_PARTIAL_TRANSACTION_REQUIRES_REVIEW");
      const { status, current_sha256, ...intent } = receipt;
      const expected = json(intent);
      for (const file of [workIntent, pendingFile(dir)])
        if (existsSync(file) && !readFileSync(file).equals(expected)) fail("LEXICON_RECOVERY_INTENT_MISMATCH");
      const currentFile = path.join(dir, STORY_LEXICON_DIRECTORY, "current.json");
      if (hash(readFileSync(currentFile)) !== current_sha256) fail("LEXICON_RECOVERY_CURRENT_MISMATCH");
      const value = readStoryLexicon({ slug, storyDir: dir, sharedFile: lexiconFile(root) });
      if (value.lexicon_sha256 !== intent.after_sha256 || value.head_event_sha256 !== intent.head_event_sha256
          || value.sequence !== intent.sequence) fail("LEXICON_RECOVERY_CURRENT_MISMATCH");
      if (existsSync(pendingFile(dir))) unlinkSync(pendingFile(dir));
      if (existsSync(workIntent)) unlinkSync(workIntent);
      return value;
    });
  } finally { lease.release(); }
}

/** Save proposed additions without silently changing a story's pronunciation or shared source. */
export function proposeStoryLexicon({ root, slug, workdir, additions }) {
  const current = videoLexicon({ root, slug, workdir, requireSnapshot: true });
  const { next, added } = additionsTo(current.lexicon, additions);
  if (!added.length) return [];
  const bytes = json({ schema_version: 1, slug, before_sha256: current.lexicon_sha256, additions, next });
  durable(path.join(workdir, "story", "lexicon-proposals", `${hash(bytes)}.json`), bytes, { immutable: true });
  return added;
}
