import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { existsSync, mkdirSync, mkdtempSync, readFileSync, readdirSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import test from "node:test";

import { main } from "../cli.mjs";
import { adoptManualStoryLexicon, ADOPTION_SLUG, inspectManualStoryAdoption } from "./lexicon-adoption.mjs";
import { initializeStoryLexicon, recoverCommittedStoryLexicon, requireStorySpeechLexicon, videoLexicon } from "./lexicon-store.mjs";
import { loadProject } from "./state.mjs";

const sha = bytes => createHash("sha256").update(bytes).digest("hex");
const error = code => caught => caught.code === code;
const NOW = new Date("2026-10-20T20:00:00Z");

function box(t) {
  const top = mkdtempSync(path.join(tmpdir(), "manual-lexicon-adoption-"));
  t.after(() => rmSync(top, { recursive: true, force: true }));
  const root = path.join(top, "repo");
  const base = path.join(top, "media");
  const dir = path.join(root, "docs", "videos", ADOPTION_SLUG);
  const workdir = path.join(base, ADOPTION_SLUG);
  mkdirSync(dir, { recursive: true });
  mkdirSync(base);
  writeFileSync(path.join(root, "docs", "videos", "lexicon.json"), '{"schema_version":1,"terms":{"GPT":"G P T"}}\n');
  writeFileSync(path.join(dir, "series.json"), '{"kind":"story","slug":"brand-stories-everyday-reversals-extra","names":["eBay","PayPal"]}\n');
  writeFileSync(path.join(dir, "video.json"), JSON.stringify({
    slug: ADOPTION_SLUG, category: "explainer", format: "drama", voice: { name: "test" },
    characters: [], scenes: [{ id: "one", lines: [{ id: "a", text: "eBay and PayPal" }] }],
  }) + "\n");
  return { top, root, base, dir, workdir, slug: ADOPTION_SLUG, reviewFile: path.join(top, "review.json") };
}

function review(b) {
  const report = inspectManualStoryAdoption({ ...b, now: () => NOW });
  assert.equal(report.status, "needs_review", JSON.stringify(report.checks));
  const record = { ...report.template, confirmed_no_prior_speech: true, independent: true, reviewer: "independent operator", reviewed_at: "2026-10-20T19:00:00Z" };
  writeFileSync(b.reviewFile, JSON.stringify(record, null, 2) + "\n");
  return { report, record };
}

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

function cli(b, ...args) {
  let stdout = "";
  let stderr = "";
  return main(["story-lexicon-adopt", "--slug", b.slug, "--workdir", b.base, ...args], {
    root: b.root, env: {}, now: () => NOW,
    stdout: { write: text => { stdout += text; } }, stderr: { write: text => { stderr += text; } },
  }).then(code => ({ code, stdout, stderr }));
}

test("X10 docs-only story: dry run writes nothing; reviewed adoption pins genesis and permits the ordinary speech guard", async t => {
  const b = box(t);
  assert.throws(() => initializeStoryLexicon(b), error("STORY_LEXICON_MIGRATION_REQUIRED"));
  assert.throws(() => requireStorySpeechLexicon(loadProject({ root: b.root, slug: b.slug }), b.workdir), error("STORY_LEXICON_MIGRATION_REQUIRED"));
  const before = tree(b.top);
  const dry = await cli(b);
  assert.equal(dry.code, 0, dry.stderr);
  assert.match(dry.stdout, /needs_review/);
  assert.match(dry.stdout, /"confirmed_no_prior_speech": false/);
  assert.deepEqual(tree(b.top), before);
  const { report } = review(b);
  const reviewed = await cli(b, "--review", b.reviewFile);
  assert.equal(reviewed.code, 0, reviewed.stderr);
  assert.match(reviewed.stdout, /: allowed/);
  const applied = await cli(b, "--review", b.reviewFile, "--apply");
  assert.equal(applied.code, 0, applied.stdout + applied.stderr);
  assert.match(applied.stdout, /pinned story-everyday-ebay-paypal-x10/);
  const pinned = videoLexicon({ root: b.root, slug: b.slug, workdir: b.workdir, requireSnapshot: true });
  assert.equal(pinned.lexicon_sha256, report.lexicon_sha256);
  assert.deepEqual(pinned.lexicon.terms, { GPT: "G P T", eBay: null, PayPal: null });
  requireStorySpeechLexicon(loadProject({ root: b.root, slug: b.slug }), b.workdir);
  const adoption = JSON.parse(readFileSync(path.join(b.dir, "story-lexicon", "adoptions", `${pinned.head_event_sha256}.json`)));
  assert.equal(adoption.video_sha256, report.template.video_sha256);
  assert.equal(adoption.series_sha256, report.template.series_sha256);
  assert.equal(adoption.review_sha256, sha(readFileSync(b.reviewFile)));
  assert.equal(existsSync(path.join(b.workdir, "auto.json")), false);
  assert.equal(existsSync(path.join(b.workdir, "story", "chapters")), false);
  assert.equal(existsSync(path.join(b.dir, "story-lexicon", "pending.json")), false);
  assert.deepEqual(readdirSync(path.join(b.workdir, "story", "lexicon-intents")), []);
  const after = tree(b.top);
  const again = await cli(b, "--review", b.reviewFile, "--apply");
  assert.equal(again.code, 0);
  assert.match(again.stdout, /already_pinned/);
  assert.deepEqual(tree(b.top), after);
});

test("adoption requires an explicit media workbase and a review for apply", async t => {
  const b = box(t);
  const before = tree(b.top);
  let output = "";
  assert.equal(await main(["story-lexicon-adopt", "--slug", b.slug], { root: b.root, env: {}, stderr: { write: text => { output += text; } } }), 2);
  assert.match(output, /explicit --workdir/);
  const noReview = await cli(b, "--apply");
  assert.equal(noReview.code, 2);
  assert.match(noReview.stderr, /needs --review/);
  assert.deepEqual(tree(b.top), before);
});

const refusals = [
  ["missing explicit workbase", "STORY_LEXICON_ADOPTION_WORKBASE_UNPROVEN", b => rmSync(b.base, { recursive: true })],
  ["worker auto.json", "STORY_LEXICON_ADOPTION_WORKER_STATE_PRESENT", b => { mkdirSync(b.workdir); writeFileSync(path.join(b.workdir, "auto.json"), "{}"); }],
  ["worker chapters", "STORY_LEXICON_ADOPTION_WORKER_STATE_PRESENT", b => mkdirSync(path.join(b.workdir, "story", "chapters"), { recursive: true })],
  ["audit", "STORY_LEXICON_ADOPTION_AUDIT_PRESENT", b => mkdirSync(path.join(b.workdir, "story", "recheck-audit"), { recursive: true })],
  ["timeline", "STORY_LEXICON_ADOPTION_TIMELINE_PRESENT", b => { mkdirSync(b.workdir); writeFileSync(path.join(b.workdir, "timeline.json"), "{}"); }],
  ["audio directory", "STORY_LEXICON_ADOPTION_AUDIO_PRESENT", b => mkdirSync(path.join(b.workdir, "audio"), { recursive: true })],
  ["narration", "STORY_LEXICON_ADOPTION_AUDIO_PRESENT", b => { mkdirSync(b.workdir); writeFileSync(path.join(b.workdir, "narration.wav"), "RIFF"); }],
  ["approvals", "STORY_LEXICON_ADOPTION_APPROVAL_PRESENT", b => { mkdirSync(b.workdir); writeFileSync(path.join(b.workdir, "approvals.json"), "{}"); }],
  ["base STOP", "LEXICON_STOPPED", b => writeFileSync(path.join(b.base, "STOP"), "")],
  ["docs intent", "LEXICON_TRANSACTION_INCOMPLETE", b => { mkdirSync(path.join(b.dir, "story-lexicon")); writeFileSync(path.join(b.dir, "story-lexicon", "pending.json"), "{}"); }],
  ["other media file", "STORY_LEXICON_ADOPTION_WORKDIR_NOT_EMPTY", b => { mkdirSync(b.workdir); writeFileSync(path.join(b.workdir, "final.mp4"), "movie"); }],
];
for (const [name, code, arrange] of refusals) {
  test(`adoption refuses ${name} without changing bytes`, async t => {
    const b = box(t);
    review(b);
    arrange(b);
    const before = tree(b.top);
    const run = await cli(b, "--review", b.reviewFile, "--apply");
    assert.equal(run.code, 1, run.stdout + run.stderr);
    assert.match(run.stdout, new RegExp(code));
    assert.deepEqual(tree(b.top), before);
    assert.equal(existsSync(path.join(b.workdir, "LEASE")), false);
  });
}

test("adoption rejects a stale exact-byte review before a lease", async t => {
  const b = box(t);
  review(b);
  writeFileSync(path.join(b.dir, "video.json"), readFileSync(path.join(b.dir, "video.json"), "utf8") + " ");
  const before = tree(b.top);
  const run = await cli(b, "--review", b.reviewFile, "--apply");
  assert.equal(run.code, 1);
  assert.match(run.stdout, /STORY_LEXICON_ADOPTION_REVIEW_INVALID/);
  assert.deepEqual(tree(b.top), before);
});

test("adoption rejects a review after shared pronunciation bytes change", async t => {
  const b = box(t);
  review(b);
  writeFileSync(path.join(b.root, "docs", "videos", "lexicon.json"), '{"schema_version":1,"terms":{"GPT":"G P T","new":null}}\n');
  const before = tree(b.top);
  const run = await cli(b, "--review", b.reviewFile, "--apply");
  assert.equal(run.code, 1);
  assert.match(run.stdout, /STORY_LEXICON_ADOPTION_REVIEW_INVALID/);
  assert.deepEqual(tree(b.top), before);
});

test("adoption rejects another slug and a false no-prior-speech attestation", async t => {
  const b = box(t);
  const { record } = review(b);
  writeFileSync(b.reviewFile, JSON.stringify({ ...record, confirmed_no_prior_speech: false }));
  assert.match((await cli(b, "--review", b.reviewFile, "--apply")).stdout, /STORY_LEXICON_ADOPTION_REVIEW_INVALID/);
  const other = await cli({ ...b, slug: "story-adapt-other" }, "--review", b.reviewFile, "--apply");
  assert.equal(other.code, 1);
  assert.match(other.stdout, /STORY_LEXICON_ADOPTION_SLUG_UNSUPPORTED/);
});

test("a committed adoption crash recovers through the existing receipt protocol", t => {
  const b = box(t);
  review(b);
  assert.throws(() => adoptManualStoryLexicon({ ...b, now: () => NOW, checkpoint: at => { if (at === "work-receipt") throw new Error("simulated crash"); } }), /simulated crash/);
  assert.throws(() => videoLexicon({ root: b.root, slug: b.slug, workdir: b.workdir, requireSnapshot: true }), error("LEXICON_TRANSACTION_INCOMPLETE"));
  const id = readdirSync(path.join(b.workdir, "story", "lexicon-intents"))[0].replace(/\.json$/, "");
  assert.equal(recoverCommittedStoryLexicon({ root: b.root, slug: b.slug, workdir: b.workdir, transactionId: id }).mode, "snapshot");
  requireStorySpeechLexicon(loadProject({ root: b.root, slug: b.slug }), b.workdir);
});

test("an adoption interrupted before its committed receipt holds the strict reader", t => {
  const b = box(t);
  review(b);
  assert.throws(() => adoptManualStoryLexicon({ ...b, now: () => NOW, checkpoint: at => { if (at === "current-pointer") throw new Error("simulated crash"); } }), /simulated crash/);
  const id = readdirSync(path.join(b.workdir, "story", "lexicon-intents"))[0].replace(/\.json$/, "");
  assert.throws(() => recoverCommittedStoryLexicon({ root: b.root, slug: b.slug, workdir: b.workdir, transactionId: id }), error("LEXICON_PARTIAL_TRANSACTION_REQUIRES_REVIEW"));
  assert.throws(() => requireStorySpeechLexicon(loadProject({ root: b.root, slug: b.slug }), b.workdir), error("LEXICON_TRANSACTION_INCOMPLETE"));
});
