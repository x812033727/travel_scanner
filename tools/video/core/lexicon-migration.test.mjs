import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { existsSync, mkdirSync, mkdtempSync, readFileSync, readdirSync, realpathSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import test from "node:test";

import { main } from "../cli.mjs";
import { inspectStartedStoryMigration, MIGRATION_REASON, migrateStartedStoryLexicon } from "./lexicon-migration.mjs";
import { initializeStoryLexicon, recoverCommittedStoryLexicon, requireStorySpeechLexicon, videoLexicon } from "./lexicon-store.mjs";
import { loadProject } from "./state.mjs";

const SLUG = "story-adapt-lexicon-migration";
const NAMES = ["Seiko Astron", "服部金太郎", "GPT"];
const json = value => `${JSON.stringify(value)}\n`;
const sha = bytes => createHash("sha256").update(bytes).digest("hex");
const shared = { schema_version: 1, terms: { GPT: "G P T" } };
const error = code => err => err.code === code;

/** A repository root and a separate work base, so the CLI's "outside the repository" rule holds. */
function box(t, { slug = SLUG, started = true } = {}) {
  const top = mkdtempSync(path.join(tmpdir(), "lexicon-migration-"));
  t.after(() => { assert.equal(path.dirname(realpathSync(top)), realpathSync(tmpdir())); rmSync(top, { recursive: true, force: true }); });
  const root = path.join(top, "repo");
  const base = path.join(top, "work");
  const dir = path.join(root, "docs", "videos", slug);
  const workdir = path.join(base, slug);
  mkdirSync(dir, { recursive: true });
  mkdirSync(workdir, { recursive: true });
  writeFileSync(path.join(root, "docs", "videos", "lexicon.json"), json(shared));
  writeFileSync(path.join(dir, "series.json"), json({ kind: "story", names: NAMES }));
  const doc = { slug, format: "drama", voice: { name: "test" }, characters: [], scenes: [{ id: "one", lines: [{ id: "a", text: "GPT" }] }] };
  if (started) {
    mkdirSync(path.join(workdir, "story", "chapters"), { recursive: true });
    for (let n = 1; n <= 6; n++) writeFileSync(path.join(workdir, "story", "chapters", `${n}.json`), json({ chapter: n }));
    writeFileSync(path.join(workdir, "approvals.json"), JSON.stringify({ approvals: [{ gate: "outline", sha256: "a" }, { gate: "script", sha256: "b" }] }));
    writeFileSync(path.join(dir, "video.json"), json(doc));
  }
  return { root, base, dir, workdir, slug, doc };
}

/** Every file under a directory with its bytes' SHA-256, for "nothing changed" assertions. */
function tree(dir) {
  if (!existsSync(dir)) return {};
  const out = {};
  for (const entry of readdirSync(dir, { withFileTypes: true, recursive: true })) {
    if (!entry.isFile()) continue;
    const file = path.join(entry.parentPath ?? entry.path, entry.name);
    out[path.relative(dir, file)] = sha(readFileSync(file));
  }
  return out;
}
const snapshotFiles = b => tree(path.join(b.dir, "story-lexicon"));
const everything = b => ({ docs: tree(path.join(b.root, "docs")), work: tree(b.workdir) });
const cli = (b, ...args) => {
  let out = "";
  return main(["story-lexicon-migrate", "--slug", b.slug, "--workdir", b.base, ...args], {
    root: b.root, env: {}, stdout: { write: s => { out += s; } }, stderr: { write: s => { out += s; } }, now: () => new Date("2026-10-17T09:00:00Z"),
  }).then(code => ({ code, out }));
};

test("a started story with no narration: the dry run allows it and writes nothing; --apply pins it and paid speech passes", async t => {
  const b = box(t);
  assert.throws(() => initializeStoryLexicon({ root: b.root, slug: b.slug, workdir: b.workdir, names: NAMES }), error("STORY_LEXICON_MIGRATION_REQUIRED"));
  assert.throws(() => requireStorySpeechLexicon(loadProject({ root: b.root, slug: b.slug }), b.workdir), error("STORY_LEXICON_MIGRATION_REQUIRED"));
  const before = everything(b);
  const report = inspectStartedStoryMigration({ root: b.root, slug: b.slug, workdir: b.workdir });
  assert.equal(report.status, "allowed");
  assert.ok(report.checks.every(check => check.ok));
  assert.deepEqual(report.seeded_terms, ["Seiko", "Astron"]);

  const dry = await cli(b);
  assert.equal(dry.code, 0);
  assert.match(dry.out, /: allowed; snapshot sha256 [0-9a-f]{64}/);
  assert.match(dry.out, /dry run: nothing written/);
  assert.deepEqual(everything(b), before);

  const applied = await cli(b, "--apply");
  assert.equal(applied.code, 0, applied.out);
  assert.match(applied.out, new RegExp(`pinned ${b.slug}: lexicon ${report.lexicon_sha256}`));
  const pinned = videoLexicon({ root: b.root, slug: b.slug, workdir: b.workdir, requireSnapshot: true });
  assert.equal(pinned.lexicon_sha256, report.lexicon_sha256);
  assert.deepEqual(pinned.lexicon.terms, { GPT: "G P T", Seiko: null, Astron: null });
  requireStorySpeechLexicon(loadProject({ root: b.root, slug: b.slug }), b.workdir);
  // The worker's own genesis call now sees the pinned story and leaves it alone.
  assert.equal(initializeStoryLexicon({ root: b.root, slug: b.slug, workdir: b.workdir }).lexicon_sha256, report.lexicon_sha256);
  // The shared dictionary is untouched, and no intent is left behind.
  assert.deepEqual(JSON.parse(readFileSync(path.join(b.root, "docs", "videos", "lexicon.json"))), shared);
  assert.equal(existsSync(path.join(b.dir, "story-lexicon", "pending.json")), false);
  assert.deepEqual(readdirSync(path.join(b.workdir, "story", "lexicon-intents")), []);

  const record = JSON.parse(readFileSync(path.join(b.dir, "story-lexicon", "migrations", `${pinned.head_event_sha256}.json`)));
  assert.equal(record.reason, MIGRATION_REASON);
  assert.equal(record.shared_sha256, sha(readFileSync(path.join(b.root, "docs", "videos", "lexicon.json"))));
  assert.equal(record.lexicon_sha256, pinned.lexicon_sha256);
  const [receipt] = readdirSync(path.join(b.workdir, "story", "lexicon-transactions")).map(name => JSON.parse(readFileSync(path.join(b.workdir, "story", "lexicon-transactions", name))));
  assert.equal(receipt.status, "committed");
  assert.equal(receipt.migration, MIGRATION_REASON);

  // Idempotent: a second run, by function or CLI, changes nothing.
  const after = everything(b);
  assert.equal(migrateStartedStoryLexicon({ root: b.root, slug: b.slug, workdir: b.workdir }).migrated, false);
  const again = await cli(b, "--apply");
  assert.equal(again.code, 0);
  assert.match(again.out, /already_pinned/);
  assert.deepEqual(everything(b), after);
});

test("the migrated snapshot is byte-identical to the genesis initializeStoryLexicon writes for a new story", t => {
  const started = box(t);
  const fresh = box(t, { started: false });
  const genesis = initializeStoryLexicon({ root: fresh.root, slug: fresh.slug, workdir: fresh.workdir, names: NAMES });
  const migrated = migrateStartedStoryLexicon({ root: started.root, slug: started.slug, workdir: started.workdir });
  assert.equal(migrated.migrated, true);
  assert.equal(migrated.lexicon_sha256, genesis.lexicon_sha256);
  assert.equal(migrated.head_event_sha256, genesis.head_event_sha256);
  const { [path.join("migrations", `${migrated.head_event_sha256}.json`)]: record, ...rest } = snapshotFiles(started);
  assert.ok(record, "the migration leaves its sidecar record");
  assert.deepEqual(rest, snapshotFiles(fresh));
});

test("an unstarted story is left to the worker's normal genesis", async t => {
  const b = box(t, { started: false });
  assert.throws(() => migrateStartedStoryLexicon({ root: b.root, slug: b.slug, workdir: b.workdir }), error("STORY_LEXICON_MIGRATION_NOT_NEEDED"));
  assert.equal((await cli(b, "--apply")).code, 1);
  assert.equal(existsSync(path.join(b.dir, "story-lexicon")), false);
});

const refusals = [
  ["a narration timeline", "STORY_LEXICON_MIGRATION_TIMELINE_PRESENT", b => writeFileSync(path.join(b.workdir, "timeline.json"), json({ lines: [] }))],
  ["a narration take under audio/", "STORY_LEXICON_MIGRATION_AUDIO_PRESENT", b => { mkdirSync(path.join(b.workdir, "audio", "takes"), { recursive: true }); writeFileSync(path.join(b.workdir, "audio", "takes", "a.wav"), "RIFF"); }],
  ["narration.wav", "STORY_LEXICON_MIGRATION_AUDIO_PRESENT", b => writeFileSync(path.join(b.workdir, "narration.wav"), "RIFF")],
  ["an audio approval", "STORY_LEXICON_MIGRATION_APPROVAL_PRESENT", b => writeFileSync(path.join(b.workdir, "approvals.json"), JSON.stringify({ approvals: [{ gate: "script" }, { gate: "audio" }] }))],
  ["a storyboard approval", "STORY_LEXICON_MIGRATION_APPROVAL_PRESENT", b => writeFileSync(path.join(b.workdir, "approvals.json"), JSON.stringify({ approvals: [{ gate: "script" }, { gate: "storyboard" }] }))],
  ["an unreadable approvals file", "STORY_LEXICON_MIGRATION_APPROVAL_PRESENT", b => writeFileSync(path.join(b.workdir, "approvals.json"), "{")],
  ["a pending lexicon intent", "LEXICON_TRANSACTION_INCOMPLETE", b => { mkdirSync(path.join(b.workdir, "story", "lexicon-intents"), { recursive: true }); writeFileSync(path.join(b.workdir, "story", "lexicon-intents", "x.json"), "{}"); }],
  ["a STOP file", "LEXICON_STOPPED", b => writeFileSync(path.join(b.workdir, "STOP"), "")],
];
for (const [what, code, arrange] of refusals) {
  test(`a story with ${what} is refused with ${code} and no byte changes`, async t => {
    const b = box(t);
    arrange(b);
    const before = everything(b);
    const report = inspectStartedStoryMigration({ root: b.root, slug: b.slug, workdir: b.workdir });
    assert.equal(report.status, "refused");
    assert.ok(report.checks.some(check => !check.ok && check.code === code), JSON.stringify(report.checks));
    assert.throws(() => migrateStartedStoryLexicon({ root: b.root, slug: b.slug, workdir: b.workdir }), error(code));
    const run = await cli(b, "--apply");
    assert.equal(run.code, 1);
    assert.match(run.out, new RegExp(`FAIL .* -> ${code}`));
    assert.deepEqual(everything(b), before);
  });
}

test("A01: an audited story is refused, by audit and by slug, and its 80 historical links keep their bytes", async t => {
  for (const slug of [SLUG, "story-rolling-suitcase-v2"]) {
    const b = box(t, { slug });
    const audit = path.join(b.workdir, "story", "recheck-audit");
    mkdirSync(audit, { recursive: true });
    for (let i = 0; i < 80; i++) writeFileSync(path.join(audit, `${i}.json`), json({ index: i }));
    const before = everything(b);
    const code = slug === SLUG ? "STORY_LEXICON_MIGRATION_AUDIT_PRESENT" : "STORY_LEXICON_MIGRATION_EXCLUDED";
    assert.throws(() => migrateStartedStoryLexicon({ root: b.root, slug, workdir: b.workdir }), error(code));
    const run = await cli(b, "--apply");
    assert.equal(run.code, 1);
    assert.match(run.out, /FAIL {2}no_recheck_audit -> STORY_LEXICON_MIGRATION_AUDIT_PRESENT/);
    assert.deepEqual(everything(b), before);
    assert.equal(Object.keys(before.work).filter(file => file.startsWith(path.join("story", "recheck-audit"))).length, 80);
    assert.equal(existsSync(path.join(b.dir, "story-lexicon")), false);
  }
});

test("a migration that crashed after its receipt is recovered by the ordinary committed-receipt recovery", t => {
  const b = box(t);
  assert.throws(() => migrateStartedStoryLexicon({ root: b.root, slug: b.slug, workdir: b.workdir, checkpoint: at => { if (at === "work-receipt") throw new Error("simulated crash"); } }), /simulated crash/);
  assert.throws(() => videoLexicon({ root: b.root, slug: b.slug, workdir: b.workdir, requireSnapshot: true }), error("LEXICON_TRANSACTION_INCOMPLETE"));
  const id = readdirSync(path.join(b.workdir, "story", "lexicon-intents"))[0].replace(/\.json$/, "");
  assert.equal(recoverCommittedStoryLexicon({ root: b.root, slug: b.slug, workdir: b.workdir, transactionId: id }).mode, "snapshot");
  requireStorySpeechLexicon(loadProject({ root: b.root, slug: b.slug }), b.workdir);
});

test("a migration that crashed before its receipt stays held for review", t => {
  const b = box(t);
  assert.throws(() => migrateStartedStoryLexicon({ root: b.root, slug: b.slug, workdir: b.workdir, checkpoint: at => { if (at === "current-pointer") throw new Error("simulated crash"); } }), /simulated crash/);
  const id = readdirSync(path.join(b.workdir, "story", "lexicon-intents"))[0].replace(/\.json$/, "");
  assert.throws(() => recoverCommittedStoryLexicon({ root: b.root, slug: b.slug, workdir: b.workdir, transactionId: id }), error("LEXICON_PARTIAL_TRANSACTION_REQUIRES_REVIEW"));
  assert.throws(() => migrateStartedStoryLexicon({ root: b.root, slug: b.slug, workdir: b.workdir }), error("LEXICON_TRANSACTION_INCOMPLETE"));
});
