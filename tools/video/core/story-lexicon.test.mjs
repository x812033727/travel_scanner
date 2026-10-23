import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { existsSync, mkdirSync, mkdtempSync, readFileSync, realpathSync, rmSync, unlinkSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import test from "node:test";

import { speechHash } from "./timeline.mjs";
import { planInitialStoryLexicon, planStoryLexiconRevision, readStoryLexicon, STORY_LEXICON_DIRECTORY } from "./story-lexicon.mjs";

const SLUG = "story-test-snapshot";
const oldLexicon = { schema_version: 1, terms: { GPT: "G P T", Claude: null } };
const nextLexicon = { schema_version: 1, terms: { GPT: "吉皮提", Claude: null } };
const bytes = (value) => Buffer.from(`${JSON.stringify(value)}\n`, "utf8");
const sha = (value) => createHash("sha256").update(value).digest("hex");

function fixture(t) {
  const base = mkdtempSync(path.join(tmpdir(), "story-lexicon-test-"));
  const storyDir = path.join(base, SLUG);
  const sharedFile = path.join(base, "lexicon.json");
  mkdirSync(storyDir);
  writeFileSync(sharedFile, bytes(oldLexicon));
  t.after(() => {
    // This exact, newly created directory must still be a direct child of OS Temp.
    if (!existsSync(base)) return;
    assert.equal(path.dirname(realpathSync(base)), realpathSync(tmpdir()));
    rmSync(base, { recursive: true, force: true });
  });
  return { base, storyDir, sharedFile, read: () => readStoryLexicon({ slug: SLUG, storyDir, sharedFile }) };
}

function publishFixture(storyDir, planned) {
  const root = path.join(storyDir, STORY_LEXICON_DIRECTORY);
  // The planner never writes. The test publishes immutable files first and selects the pointer
  // last, which also exercises a read after a process-style restart.
  for (const file of planned.files) {
    if (file.relative === "current.json") continue;
    const target = path.join(root, file.relative);
    mkdirSync(path.dirname(target), { recursive: true });
    if (existsSync(target)) assert.deepEqual(readFileSync(target), file.bytes);
    else writeFileSync(target, file.bytes, { flag: "wx" });
  }
  writeFileSync(path.join(root, "current.json"), planned.files.find((file) => file.relative === "current.json").bytes);
}

function initial(t) {
  const box = fixture(t);
  const planned = planInitialStoryLexicon({ slug: SLUG, sharedBytes: readFileSync(box.sharedFile) });
  publishFixture(box.storyDir, planned);
  return { ...box, planned };
}

test("legacy stories explicitly read the shared dictionary without creating a snapshot", (t) => {
  const box = fixture(t);
  const legacy = box.read();
  assert.equal(legacy.mode, "legacy_shared");
  assert.deepEqual(legacy.lexicon, oldLexicon);
  assert.equal(legacy.lexicon_sha256, sha(readFileSync(box.sharedFile)));
  assert.equal(existsSync(path.join(box.storyDir, STORY_LEXICON_DIRECTORY)), false);
  writeFileSync(box.sharedFile, bytes({ schema_version: 1, terms: { ...oldLexicon.terms, OtherStory: null } }));
  assert.notEqual(box.read().lexicon_sha256, legacy.lexicon_sha256, "legacy mode still observes shared edits");
});

test("a pinned story survives restart and unrelated shared edits with identical source and speech hashes", (t) => {
  const box = initial(t);
  const first = box.read();
  assert.equal(first.mode, "snapshot");
  assert.equal(first.sequence, 1);
  assert.equal(first.lexicon_sha256, box.planned.lexicon_sha256);
  assert.deepEqual(first.bytes, bytes(oldLexicon));
  const doc = { format: "drama", voice: { name: "test" }, characters: [], scenes: [{ id: "one", lines: [{ id: "a", text: "GPT 和 Claude" }] }] };
  const speech = speechHash(doc, first.lexicon);
  writeFileSync(box.sharedFile, bytes({ schema_version: 1, terms: { ...oldLexicon.terms, OtherStory: "別的唸法" } }));
  const restarted = readStoryLexicon({ slug: SLUG, storyDir: box.storyDir, sharedFile: box.sharedFile });
  assert.equal(restarted.lexicon_sha256, first.lexicon_sha256);
  assert.deepEqual(restarted.bytes, first.bytes);
  assert.equal(speechHash(doc, restarted.lexicon), speech);
});

test("a reviewed revision creates a second immutable version and a verifiable event chain", (t) => {
  const box = initial(t);
  const before = box.read();
  const reviewSha256 = sha("fixture external review bytes");
  const planned = planStoryLexiconRevision({ slug: SLUG, previous: before, nextBytes: bytes(nextLexicon), reviewSha256 });
  assert.equal(planned.sequence, 2);
  assert.notEqual(planned.lexicon_sha256, before.lexicon_sha256);
  const event = JSON.parse(planned.files.find((file) => path.dirname(file.relative) === "events").bytes);
  assert.equal(event.before_sha256, before.lexicon_sha256);
  assert.equal(event.previous_event_sha256, before.head_event_sha256);
  assert.equal(event.review_sha256, reviewSha256);
  publishFixture(box.storyDir, planned);
  const after = box.read();
  assert.deepEqual(after.lexicon, nextLexicon);
  assert.equal(after.head_event_sha256, planned.head_event_sha256);
  assert.deepEqual(readFileSync(path.join(box.storyDir, STORY_LEXICON_DIRECTORY, "versions", `${before.lexicon_sha256}.json`)), before.bytes);
  assert.ok(existsSync(path.join(box.storyDir, STORY_LEXICON_DIRECTORY, "events", `${before.head_event_sha256}.json`)));
  assert.throws(() => planStoryLexiconRevision({ slug: SLUG, previous: after, nextBytes: after.bytes, reviewSha256 }), /LEXICON_REVISION_UNCHANGED/);
  assert.throws(() => planStoryLexiconRevision({ slug: SLUG, previous: after, nextBytes: before.bytes }), /REVISION_REVIEW_HASH_REQUIRED/);
});

test("a partial snapshot never silently falls back to the shared dictionary", (t) => {
  const box = fixture(t);
  mkdirSync(path.join(box.storyDir, STORY_LEXICON_DIRECTORY));
  assert.throws(box.read, /LEXICON_CURRENT_MISSING_OR_UNSAFE/);
});

test("bad pointer, missing old version, and mutated current version all fail closed", (t) => {
  const box = initial(t);
  const root = path.join(box.storyDir, STORY_LEXICON_DIRECTORY);
  const currentFile = path.join(root, "current.json");
  const originalCurrent = readFileSync(currentFile);
  writeFileSync(currentFile, "{invalid");
  assert.throws(box.read, /LEXICON_CURRENT_JSON_INVALID/);
  writeFileSync(currentFile, JSON.stringify({ ...JSON.parse(originalCurrent), slug: "../escape" }));
  assert.throws(box.read, /LEXICON_CURRENT_SCHEMA_INVALID/);
  writeFileSync(currentFile, originalCurrent);
  const pinnedFile = path.join(root, "versions", `${box.planned.lexicon_sha256}.json`);
  writeFileSync(pinnedFile, bytes(nextLexicon));
  assert.throws(box.read, /LEXICON_VERSION_HASH_MISMATCH/);
  unlinkSync(pinnedFile);
  assert.throws(box.read, /LEXICON_VERSION_MISSING_OR_UNSAFE/);
});

test("an event chain cannot hide a changed old link or a corrupted event", (t) => {
  const box = initial(t);
  const old = box.read();
  const next = planStoryLexiconRevision({ slug: SLUG, previous: old, nextBytes: bytes(nextLexicon), reviewSha256: sha("review") });
  publishFixture(box.storyDir, next);
  const root = path.join(box.storyDir, STORY_LEXICON_DIRECTORY);
  const oldEvent = path.join(root, "events", `${old.head_event_sha256}.json`);
  const original = readFileSync(oldEvent);
  writeFileSync(oldEvent, Buffer.concat([original, Buffer.from(" ")]));
  assert.throws(box.read, /LEXICON_EVENT_HASH_MISMATCH/);
  writeFileSync(oldEvent, original);
  const current = path.join(root, "current.json");
  writeFileSync(current, JSON.stringify({ ...JSON.parse(readFileSync(current)), sequence: 1 }));
  assert.throws(box.read, /LEXICON_EVENT_CHAIN_MISMATCH/);
});

test("malformed inputs and unsafe names never produce a path to write", (t) => {
  const box = fixture(t);
  for (const slug of ["../outside", "A01", "story/slash", ""]) {
    assert.throws(() => planInitialStoryLexicon({ slug, sharedBytes: bytes(oldLexicon) }), /STORY_SLUG_INVALID/);
  }
  assert.throws(() => planInitialStoryLexicon({ slug: SLUG, sharedBytes: bytes({ schema_version: 1, terms: { "8B": null } }) }), /LEXICON_SCHEMA_INVALID/);
  assert.throws(() => planInitialStoryLexicon({ slug: SLUG, sharedBytes: "not json" }), /LEXICON_JSON_INVALID/);
  assert.throws(() => readStoryLexicon({ slug: "other-story", storyDir: box.storyDir, sharedFile: box.sharedFile }), /STORY_SLUG_INVALID/);
});

test("legacy missing shared file has the historical empty dictionary fallback", (t) => {
  const box = fixture(t);
  unlinkSync(box.sharedFile);
  const value = box.read();
  assert.equal(value.mode, "legacy_shared");
  assert.equal(value.lexicon_sha256, null);
  assert.deepEqual(value.lexicon, { schema_version: 1, terms: {} });
});
