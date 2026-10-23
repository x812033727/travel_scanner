// Experimental per-story lexicon format. This module plans immutable bytes and reads them;
// it deliberately has no publisher, worker integration, host command, or approval decision.
// A production writer must first establish an exclusive source/audit protocol and migrate
// existing story audits with an append-only transition. In particular, do not infer that an
// unpinned A01 story may be snapshotted merely because a shared dictionary is readable.
import { createHash } from "node:crypto";
import { lstatSync, readFileSync } from "node:fs";
import path from "node:path";

import { emptyLexicon, validateLexicon } from "./lexicon.mjs";
import { SLUG } from "./schema.mjs";

export const STORY_LEXICON_DIRECTORY = "story-lexicon";
const HASH = /^[0-9a-f]{64}$/;
const CURRENT_KEYS = ["head_event_sha256", "kind", "lexicon_sha256", "schema_version", "sequence", "slug"];
const EVENT_KEYS = ["after_sha256", "before_sha256", "kind", "previous_event_sha256", "reason", "review_sha256", "schema_version", "sequence", "slug"];
const CURRENT_KIND = "story_lexicon_current";
const EVENT_KIND = "story_lexicon_revision";

export class StoryLexiconError extends Error {
  constructor(code, detail = "") {
    super(`${code}${detail ? `: ${detail}` : ""}`);
    this.name = "StoryLexiconError";
    this.code = code;
  }
}

const fail = (code, detail) => { throw new StoryLexiconError(code, detail); };
const bytesOf = (value) => {
  if (Buffer.isBuffer(value)) return Buffer.from(value);
  if (typeof value === "string") return Buffer.from(value, "utf8");
  return fail("LEXICON_BYTES_REQUIRED");
};
const digest = (bytes) => createHash("sha256").update(bytes).digest("hex");
const jsonBytes = (value) => Buffer.from(`${JSON.stringify(value)}\n`, "utf8");
const keysAre = (value, keys) => value !== null && typeof value === "object" && !Array.isArray(value)
  && JSON.stringify(Object.keys(value).sort()) === JSON.stringify(keys);
const validHash = (value) => typeof value === "string" && HASH.test(value);
const validSlug = (slug) => typeof slug === "string" && SLUG.test(slug);

function parseJson(bytes, code) {
  try { return JSON.parse(bytes.toString("utf8").replace(/^\uFEFF/, "")); }
  catch { return fail(code); }
}

function parseLexicon(bytes) {
  const lexicon = parseJson(bytes, "LEXICON_JSON_INVALID");
  const problems = validateLexicon(lexicon);
  if (problems.length || !keysAre(lexicon, ["schema_version", "terms"])) {
    return fail("LEXICON_SCHEMA_INVALID", problems[0]?.path ?? "unexpected top-level field");
  }
  return lexicon;
}

function plan({ slug, lexiconBytes, previous = null, reviewSha256 = null }) {
  if (!validSlug(slug)) fail("STORY_SLUG_INVALID");
  const versionBytes = bytesOf(lexiconBytes);
  parseLexicon(versionBytes);
  const versionSha256 = digest(versionBytes);
  const initial = previous === null;
  if (!initial && (!previous || previous.mode !== "snapshot" || previous.slug !== slug
      || !validHash(previous.lexicon_sha256) || !validHash(previous.head_event_sha256)
      || !Number.isSafeInteger(previous.sequence) || previous.sequence < 1
      || previous.sequence === Number.MAX_SAFE_INTEGER || !Buffer.isBuffer(previous.bytes)
      || digest(previous.bytes) !== previous.lexicon_sha256)) fail("PREVIOUS_SNAPSHOT_INVALID");
  if (!initial && !validHash(reviewSha256)) fail("REVISION_REVIEW_HASH_REQUIRED");
  if (initial && reviewSha256 !== null) fail("INITIAL_REVIEW_HASH_UNEXPECTED");
  if (!initial && previous.lexicon_sha256 === versionSha256) fail("LEXICON_REVISION_UNCHANGED");
  const event = {
    schema_version: 1, kind: EVENT_KIND, slug, sequence: initial ? 1 : previous.sequence + 1,
    reason: initial ? "initial_snapshot" : "reviewed_revision",
    before_sha256: initial ? null : previous.lexicon_sha256,
    after_sha256: versionSha256,
    previous_event_sha256: initial ? null : previous.head_event_sha256,
    review_sha256: initial ? null : reviewSha256,
  };
  const eventBytes = jsonBytes(event);
  const eventSha256 = digest(eventBytes);
  const current = {
    schema_version: 1, kind: CURRENT_KIND, slug, sequence: event.sequence,
    lexicon_sha256: versionSha256, head_event_sha256: eventSha256,
  };
  // These relative names are derived only from checked SHA-256 digests. A future writer must
  // publish both immutable files before atomically selecting current.json under a shared lock.
  return {
    mode: "snapshot", slug, sequence: event.sequence, lexicon_sha256: versionSha256,
    head_event_sha256: eventSha256,
    files: [
      { relative: path.join("versions", `${versionSha256}.json`), bytes: versionBytes },
      { relative: path.join("events", `${eventSha256}.json`), bytes: eventBytes },
      { relative: "current.json", bytes: jsonBytes(current) },
    ],
  };
}

/** Pure plan for the first pinned version; this does not write or authorize a live story. */
export function planInitialStoryLexicon({ slug, sharedBytes }) {
  return plan({ slug, lexiconBytes: sharedBytes });
}

/** Pure plan for a reviewed revision; a review hash is data, not human authentication. */
export function planStoryLexiconRevision({ slug, previous, nextBytes, reviewSha256 }) {
  return plan({ slug, lexiconBytes: nextBytes, previous, reviewSha256 });
}

function nodeStat(file) {
  try { return lstatSync(file); }
  catch (error) {
    if (error?.code === "ENOENT") return null;
    throw error;
  }
}

function safeDirectory(dir, code) {
  const stat = nodeStat(dir);
  if (!stat || !stat.isDirectory() || stat.isSymbolicLink()) fail(code, dir);
}

function regularFile(file, code) {
  const stat = nodeStat(file);
  if (!stat || !stat.isFile() || stat.isSymbolicLink()) fail(code, file);
  return readFileSync(file);
}

function versionBytes(root, sha256) {
  const bytes = regularFile(path.join(root, "versions", `${sha256}.json`), "LEXICON_VERSION_MISSING_OR_UNSAFE");
  if (digest(bytes) !== sha256) fail("LEXICON_VERSION_HASH_MISMATCH");
  return { bytes, lexicon: parseLexicon(bytes) };
}

function eventValue(root, sha256) {
  const bytes = regularFile(path.join(root, "events", `${sha256}.json`), "LEXICON_EVENT_MISSING_OR_UNSAFE");
  if (digest(bytes) !== sha256) fail("LEXICON_EVENT_HASH_MISMATCH");
  const event = parseJson(bytes, "LEXICON_EVENT_JSON_INVALID");
  if (!keysAre(event, EVENT_KEYS) || event.schema_version !== 1 || event.kind !== EVENT_KIND
      || !validSlug(event.slug) || !Number.isSafeInteger(event.sequence) || event.sequence < 1
      || !validHash(event.after_sha256)) fail("LEXICON_EVENT_SCHEMA_INVALID");
  return event;
}

/**
 * Read a pinned story and its entire event chain. A legacy story with no snapshot directory
 * explicitly falls back to the shared dictionary; that is compatibility, not migration.
 */
export function readStoryLexicon({ slug, storyDir, sharedFile }) {
  if (!validSlug(slug) || typeof storyDir !== "string" || path.basename(path.resolve(storyDir)) !== slug) fail("STORY_SLUG_INVALID");
  safeDirectory(storyDir, "STORY_DIRECTORY_UNSAFE");
  const root = path.join(storyDir, STORY_LEXICON_DIRECTORY);
  const rootStat = nodeStat(root);
  if (!rootStat) {
    let bytes = null;
    let lexicon = emptyLexicon();
    if (sharedFile && nodeStat(sharedFile)) {
      bytes = regularFile(sharedFile, "SHARED_LEXICON_UNSAFE");
      lexicon = parseLexicon(bytes);
    }
    return { mode: "legacy_shared", slug, lexicon, bytes, lexicon_sha256: bytes === null ? null : digest(bytes) };
  }
  if (!rootStat.isDirectory() || rootStat.isSymbolicLink()) fail("LEXICON_SNAPSHOT_DIRECTORY_UNSAFE");
  const current = parseJson(regularFile(path.join(root, "current.json"), "LEXICON_CURRENT_MISSING_OR_UNSAFE"), "LEXICON_CURRENT_JSON_INVALID");
  if (!keysAre(current, CURRENT_KEYS) || current.schema_version !== 1 || current.kind !== CURRENT_KIND
      || current.slug !== slug || !Number.isSafeInteger(current.sequence) || current.sequence < 1
      || !validHash(current.lexicon_sha256) || !validHash(current.head_event_sha256)) fail("LEXICON_CURRENT_SCHEMA_INVALID");
  safeDirectory(path.join(root, "versions"), "LEXICON_VERSIONS_DIRECTORY_UNSAFE");
  safeDirectory(path.join(root, "events"), "LEXICON_EVENTS_DIRECTORY_UNSAFE");

  const seen = new Set();
  let eventHash = current.head_event_sha256;
  let afterHash = current.lexicon_sha256;
  let newest = null;
  for (let sequence = current.sequence; sequence >= 1; sequence--) {
    if (seen.has(eventHash)) fail("LEXICON_EVENT_CYCLE");
    seen.add(eventHash);
    const event = eventValue(root, eventHash);
    if (event.slug !== slug || event.sequence !== sequence || event.after_sha256 !== afterHash) fail("LEXICON_EVENT_CHAIN_MISMATCH");
    if (sequence === 1) {
      if (event.reason !== "initial_snapshot" || event.before_sha256 !== null
          || event.previous_event_sha256 !== null || event.review_sha256 !== null) fail("LEXICON_GENESIS_INVALID");
    } else if (event.reason !== "reviewed_revision" || !validHash(event.before_sha256)
        || !validHash(event.previous_event_sha256) || !validHash(event.review_sha256)
        || event.before_sha256 === event.after_sha256) fail("LEXICON_REVISION_INVALID");
    const version = versionBytes(root, afterHash);
    if (!newest) newest = version;
    eventHash = event.previous_event_sha256;
    afterHash = event.before_sha256;
  }
  return {
    mode: "snapshot", slug, sequence: current.sequence,
    lexicon_sha256: current.lexicon_sha256, head_event_sha256: current.head_event_sha256,
    lexicon: newest.lexicon, bytes: newest.bytes,
  };
}
