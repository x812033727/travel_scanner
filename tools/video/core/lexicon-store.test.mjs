import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { existsSync, mkdirSync, mkdtempSync, readFileSync, readdirSync, realpathSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import test from "node:test";
import { initializeStoryLexicon, mergeSharedLexicon, proposeStoryLexicon, recoverCommittedStoryLexicon, requireStorySpeechLexicon, reviseStoryLexicon, videoLexicon, withLexiconWriter } from "./lexicon-store.mjs";
import { loadProject } from "./state.mjs";
import { speechHash } from "./timeline.mjs";

const slug = "story-lexicon-runtime";
const json = value => `${JSON.stringify(value)}\n`;
const sha = value => createHash("sha256").update(value).digest("hex");
const old = { schema_version: 1, terms: { GPT: "G P T" } };
function box(t) {
  const root = mkdtempSync(path.join(tmpdir(), "lexicon-store-"));
  t.after(() => { assert.equal(path.dirname(realpathSync(root)), realpathSync(tmpdir())); rmSync(root, { recursive: true, force: true }); });
  const dir = path.join(root, "docs", "videos", slug);
  const workdir = path.join(root, "work", slug);
  const shared = path.join(root, "docs", "videos", "lexicon.json");
  mkdirSync(dir, { recursive: true });
  mkdirSync(workdir, { recursive: true });
  writeFileSync(shared, json(old));
  const doc = { slug, format: "drama", voice: { name: "test" }, characters: [], scenes: [{ id: "one", lines: [{ id: "a", text: "GPT" }] }] };
  writeFileSync(path.join(dir, "series.json"), json({ kind: "story" }));
  return { root, slug, dir, workdir, shared, doc, writeProject: () => writeFileSync(path.join(dir, "video.json"), json(doc)) };
}
const error = code => err => err.code === code;

test("runtime project and paid checks retain pinned bytes after another film edits the shared lexicon", t => {
  const b = box(t);
  const first = initializeStoryLexicon(b);
  b.writeProject();
  const p1 = loadProject({ root: b.root, slug });
  const speech = speechHash(p1.doc, p1.lexicon);
  mergeSharedLexicon(b.root, { OtherFilm: null });
  writeFileSync(b.shared, json({ schema_version: 1, terms: { GPT: "changed shared reading" } }));
  const p2 = loadProject({ root: b.root, slug });
  assert.equal(speechHash(p2.doc, p2.lexicon), speech);
  assert.equal(videoLexicon(b).lexicon_sha256, first.lexicon_sha256);
  requireStorySpeechLexicon(p2, b.workdir);
});

test("the same filesystem writer admission refuses a second independent writer", t => {
  const b = box(t);
  // A simulated external holder has no local ownership registration to borrow.
  const lock = path.join(b.root, "docs", "videos", ".lexicon-writer");
  mkdirSync(lock, { recursive: true });
  writeFileSync(path.join(lock, "LEASE"), json({ pid: process.pid, hostname: "another-host", token: "external" }));
  assert.throws(() => withLexiconWriter(b.root, () => assert.fail("must not write")), error("video_project_leased"));
  assert.deepEqual(JSON.parse(readFileSync(b.shared)), old);
});

test("an audited legacy story cannot be initialized or paid for and retains all 80 historical links", t => {
  const b = box(t);
  const audit = path.join(b.workdir, "story", "recheck-audit");
  b.writeProject();
  mkdirSync(audit, { recursive: true });
  const hashes = [];
  for (let i = 0; i < 80; i++) { const file = path.join(audit, `${i}.json`); writeFileSync(file, json({ index: i })); hashes.push(sha(readFileSync(file))); }
  assert.throws(() => initializeStoryLexicon(b), error("STORY_LEXICON_MIGRATION_REQUIRED"));
  assert.throws(() => requireStorySpeechLexicon(loadProject({ root: b.root, slug }), b.workdir), error("STORY_LEXICON_MIGRATION_REQUIRED"));
  assert.deepEqual(hashes, Array.from({ length: 80 }, (_, i) => sha(readFileSync(path.join(audit, `${i}.json`)))));
  assert.equal(existsSync(path.join(b.dir, "story-lexicon")), false);
});

test("writer additions are saved as proposals and a separately reviewed revision invalidates the old speech hash", t => {
  const b = box(t);
  const first = initializeStoryLexicon(b);
  b.writeProject();
  const p1 = loadProject({ root: b.root, slug });
  assert.deepEqual(proposeStoryLexicon({ ...b, additions: { NewName: null } }), ["NewName"]);
  assert.equal(videoLexicon(b).lexicon_sha256, first.lexicon_sha256);
  assert.deepEqual(JSON.parse(readFileSync(b.shared)), old);
  assert.equal(readdirSync(path.join(b.workdir, "story", "lexicon-proposals")).length, 1);
  assert.throws(() => reviseStoryLexicon({ ...b, nextBytes: Buffer.from(json({ schema_version: 1, terms: { GPT: "new reading" } })) }), error("REVISION_REVIEW_HASH_REQUIRED"));
  const revised = reviseStoryLexicon({ ...b, nextBytes: Buffer.from(json({ schema_version: 1, terms: { GPT: "new reading" } })), reviewSha256: sha("independent review fixture") });
  assert.equal(revised.sequence, 2);
  assert.throws(() => requireStorySpeechLexicon(p1, b.workdir), error("LEXICON_PROJECT_STALE"));
  assert.notEqual(speechHash(b.doc, revised.lexicon), speechHash(b.doc, first.lexicon));
});

for (const point of ["work-intent", "docs-intent", "immutable-files", "current-pointer", "work-receipt", "docs-intent-cleared"]) {
  test(`crash at ${point} keeps both-volume readers held; only an exact committed receipt can recover`, t => {
    const b = box(t);
    assert.throws(() => initializeStoryLexicon({ ...b, checkpoint: at => { if (at === point) throw new Error("simulated crash"); } }), /simulated crash/);
    assert.throws(() => videoLexicon({ ...b, requireSnapshot: true }), error("LEXICON_TRANSACTION_INCOMPLETE"));
    const id = readdirSync(path.join(b.workdir, "story", "lexicon-intents"))[0].replace(/\.json$/, "");
    if (["work-receipt", "docs-intent-cleared"].includes(point)) {
      assert.equal(recoverCommittedStoryLexicon({ ...b, transactionId: id }).mode, "snapshot");
      assert.equal(videoLexicon(b).mode, "snapshot");
    } else {
      assert.throws(() => recoverCommittedStoryLexicon({ ...b, transactionId: id }), error("LEXICON_PARTIAL_TRANSACTION_REQUIRES_REVIEW"));
      assert.throws(() => initializeStoryLexicon(b), error("LEXICON_TRANSACTION_INCOMPLETE"));
    }
  });
}
