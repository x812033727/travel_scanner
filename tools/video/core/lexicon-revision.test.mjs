import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { existsSync, mkdirSync, mkdtempSync, readFileSync, readdirSync, realpathSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import test from "node:test";

import { main } from "../cli.mjs";
import { initializeStoryLexicon, proposeStoryLexicon, requireStorySpeechLexicon, videoLexicon } from "./lexicon-store.mjs";
import { applyStoryLexiconRevision, inspectStoryLexiconRevision, REVIEW_KIND } from "./lexicon-revision.mjs";
import { loadProject } from "./state.mjs";

const SLUG = "story-adapt-lexicon-revision";
const json = value => `${JSON.stringify(value)}\n`;
const sha = bytes => createHash("sha256").update(bytes).digest("hex");
const NOW = () => new Date("2026-10-17T12:00:00Z");
const error = code => err => err.code === code;

/** A pinned story that has written a chapter whose writer proposed Paul (as written) and Bocuse (博古斯). */
function box(t, { additions = { Paul: null, Bocuse: "博古斯" } } = {}) {
  const top = mkdtempSync(path.join(tmpdir(), "lexicon-revision-"));
  t.after(() => { assert.equal(path.dirname(realpathSync(top)), realpathSync(tmpdir())); rmSync(top, { recursive: true, force: true }); });
  const root = path.join(top, "repo");
  const base = path.join(top, "work");
  const dir = path.join(root, "docs", "videos", SLUG);
  const workdir = path.join(base, SLUG);
  mkdirSync(dir, { recursive: true });
  mkdirSync(workdir, { recursive: true });
  writeFileSync(path.join(root, "docs", "videos", "lexicon.json"), json({ schema_version: 1, terms: { GPT: "G P T" } }));
  writeFileSync(path.join(dir, "series.json"), json({ kind: "story" }));
  const b = { root, base, dir, workdir, slug: SLUG };
  initializeStoryLexicon(b);
  mkdirSync(path.join(workdir, "story", "chapters"), { recursive: true });
  writeFileSync(path.join(workdir, "story", "chapters", "1.json"), json({ chapter: 1 }));
  writeFileSync(path.join(workdir, "auto.json"), json({ slug: SLUG, story: { chapters: {}, lexicon_pending: Object.keys(additions) } }));
  const doc = { slug: SLUG, format: "drama", voice: { name: "test" }, characters: [], scenes: [{ id: "one", lines: [{ id: "a", text: "GPT" }] }] };
  writeFileSync(path.join(dir, "video.json"), json(doc));
  if (additions) assert.deepEqual(proposeStoryLexicon({ ...b, additions }), Object.keys(additions));
  return b;
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
const everything = b => ({ docs: tree(path.join(b.root, "docs")), work: tree(b.base) });

/** The template, filled in the way a reviewer would. */
function filled(b, decisions, overrides = {}) {
  const template = inspectStoryLexiconRevision(b).template;
  assert.ok(template, "a current proposal makes a template");
  for (const [term, decision] of Object.entries(decisions)) template.decisions[term] = { ...template.decisions[term], ...decision };
  return Buffer.from(`${JSON.stringify({ ...template, reviewer: "pei (owner)", reviewed_at: "2026-10-17T11:30:00Z", independent: true, ...overrides }, null, 2)}\n`);
}
const ACCEPT_BOTH = { Paul: { decision: "accept" }, Bocuse: { decision: "accept" } };
const run = (b, reviewBytes, apply = true) => applyStoryLexiconRevision({ ...b, reviewBytes, apply, now: NOW });

const cli = async (b, ...args) => {
  let out = "";
  const code = await main(["story-lexicon-revise", "--slug", b.slug, "--workdir", b.base, ...args], {
    root: b.root, env: {}, stdout: { write: s => { out += s; } }, stderr: { write: s => { out += s; } }, now: NOW,
  });
  return { code, out };
};

test("listing shows each proposal and a receipt template; it writes nothing", async t => {
  const b = box(t);
  const before = everything(b);
  const report = inspectStoryLexiconRevision(b);
  assert.deepEqual(report.refusals, []);
  assert.equal(report.proposals.length, 1);
  assert.equal(report.proposals[0].status, "current");
  assert.equal(report.proposals[0].before_sha256, report.lexicon_sha256);
  assert.deepEqual(report.proposals[0].pending, { Paul: null, Bocuse: "博古斯" });
  assert.deepEqual(report.template, {
    schema_version: 1, kind: REVIEW_KIND, slug: SLUG, lexicon_sha256: report.lexicon_sha256,
    proposals: [report.proposals[0].sha256],
    decisions: { Paul: { proposed: null, decision: null }, Bocuse: { proposed: "博古斯", decision: null } },
    reviewer: null, reviewed_at: null, independent: false,
  });
  const listed = await cli(b);
  assert.equal(listed.code, 0, listed.out);
  assert.match(listed.out, /current\s+[0-9a-f]{64}/);
  assert.match(listed.out, /Bocuse -> "博古斯"/);
  assert.match(listed.out, /"kind": "story_lexicon_revision_review"/);
  // The unfilled template itself is refused.
  const template = Buffer.from(JSON.stringify(report.template));
  assert.throws(() => run(b, template, false), error("STORY_LEXICON_REVIEWER_INVALID"));
  assert.deepEqual(everything(b), before);
});

test("a reviewed receipt: the dry run writes nothing; --apply publishes, keeps the receipt and paid speech passes", async t => {
  const b = box(t);
  const receipt = filled(b, { Paul: { decision: "accept" }, Bocuse: { decision: "accept_as", spoken: "保羅博古斯", reason: "full name" } });
  const file = path.join(b.root, "..", "receipt.json");
  writeFileSync(file, receipt);
  const before = everything(b);
  const dry = await cli(b, "--review", file);
  assert.equal(dry.code, 0, dry.out);
  assert.match(dry.out, /dry run: nothing written/);
  assert.deepEqual(everything(b), before);

  const old = videoLexicon(b);
  const applied = await cli(b, "--review", file, "--apply");
  assert.equal(applied.code, 0, applied.out);
  assert.match(applied.out, /published version 2/);
  assert.match(applied.out, /retry .* on \/admin\/videos/);
  const now = videoLexicon(b);
  assert.equal(now.mode, "snapshot");
  assert.equal(now.sequence, 2);
  assert.deepEqual(now.lexicon.terms, { ...old.lexicon.terms, Paul: null, Bocuse: "保羅博古斯" });
  // The event binds the exact receipt bytes, which are kept in the work directory.
  const event = JSON.parse(readFileSync(path.join(b.dir, "story-lexicon", "events", `${now.head_event_sha256}.json`)));
  assert.equal(event.review_sha256, sha(receipt));
  assert.equal(event.before_sha256, old.lexicon_sha256);
  assert.ok(readFileSync(path.join(b.workdir, "story", "lexicon-reviews", `${sha(receipt)}.json`)).equals(receipt));
  requireStorySpeechLexicon(loadProject({ root: b.root, slug: SLUG }), b.workdir);
  // Every lease and intent is gone.
  assert.ok(!existsSync(path.join(b.workdir, "LEASE")));
  assert.deepEqual(readdirSync(path.join(b.workdir, "story", "lexicon-intents")), []);
  // The proposal now reads as applied, and there is nothing left to template.
  const report = inspectStoryLexiconRevision(b);
  assert.equal(report.proposals[0].status, "applied");
  assert.equal(report.template, null);

  // Applying the same receipt again is a no-op that says so.
  const after = everything(b);
  const again = run(b, receipt);
  assert.equal(again.status, "already_applied");
  assert.equal(again.lexicon_sha256, now.lexicon_sha256);
  assert.deepEqual(everything(b), after);
});

test("a rejected term does not enter the dictionary; rejecting everything publishes nothing", t => {
  const b = box(t);
  const result = run(b, filled(b, { Paul: { decision: "accept" }, Bocuse: { decision: "reject", reason: "the chapter should not name him" } }));
  assert.equal(result.status, "applied");
  assert.deepEqual(result.rejected, ["Bocuse"]);
  const now = videoLexicon(b);
  assert.ok(Object.hasOwn(now.lexicon.terms, "Paul"));
  assert.ok(!Object.hasOwn(now.lexicon.terms, "Bocuse"));
  // The proposal still has a pending term against an older dictionary: stale, no template.
  const report = inspectStoryLexiconRevision(b);
  assert.equal(report.proposals[0].status, "stale");
  assert.deepEqual(report.proposals[0].pending, { Bocuse: "博古斯" });

  const c = box(t);
  const before = everything(c);
  assert.throws(() => run(c, filled(c, { Paul: { decision: "reject" }, Bocuse: { decision: "reject" } })), error("STORY_LEXICON_REVISION_NOTHING_ACCEPTED"));
  assert.deepEqual(everything(c), before);
});

test("a proposal made against an older dictionary is refused", t => {
  const b = box(t);
  const stale = filled(b, ACCEPT_BOTH);
  // A second chapter proposes another term against the same version; the first receipt publishes.
  assert.deepEqual(proposeStoryLexicon({ ...b, additions: { Lyon: null } }), ["Lyon"]);
  const first = inspectStoryLexiconRevision(b);
  assert.equal(first.template.proposals.length, 2);
  run(b, filled(b, { ...ACCEPT_BOTH, Lyon: { decision: "accept" } }));
  // A receipt written before that revision is refused, and writes nothing.
  const before = everything(b);
  assert.throws(() => run(b, stale), error("STORY_LEXICON_REVIEW_STALE"));
  assert.deepEqual(everything(b), before);
  // A fresh proposal after the revision, with a receipt naming the old (applied) proposal.
  assert.deepEqual(proposeStoryLexicon({ ...b, additions: { Rhone: null } }), ["Rhone"]);
  const report = inspectStoryLexiconRevision(b);
  const old = report.proposals.find(each => each.status === "applied").sha256;
  const receipt = filled(b, { Rhone: { decision: "accept" } }, { proposals: [...report.template.proposals, old] });
  assert.throws(() => run(b, receipt), error("STORY_LEXICON_PROPOSAL_APPLIED"));

  // A proposal whose terms were rejected stays pending against an older version: stale.
  const c = box(t);
  run(c, filled(c, { Paul: { decision: "accept" }, Bocuse: { decision: "reject" } }));
  const staleProposal = inspectStoryLexiconRevision(c).proposals[0].sha256;
  const current = videoLexicon(c).lexicon_sha256;
  const forced = Buffer.from(JSON.stringify({ schema_version: 1, kind: REVIEW_KIND, slug: SLUG, lexicon_sha256: current, proposals: [staleProposal],
    decisions: { Bocuse: { proposed: "博古斯", decision: "accept" } }, reviewer: "pei", reviewed_at: "2026-10-17T11:30:00Z", independent: true }));
  assert.throws(() => run(c, forced), error("STORY_LEXICON_PROPOSAL_STALE"));
});

test("a receipt with the wrong slug, proposal, reviewer, time, independence or decisions is refused before any write", async t => {
  const b = box(t);
  const cases = [
    [{ slug: "story-adapt-other" }, "STORY_LEXICON_REVIEW_SLUG_MISMATCH"],
    [{ lexicon_sha256: "0".repeat(64) }, "STORY_LEXICON_REVIEW_STALE"],
    [{ proposals: ["f".repeat(64)] }, "STORY_LEXICON_PROPOSAL_UNKNOWN"],
    [{ proposals: [] }, "STORY_LEXICON_REVIEW_INVALID"],
    [{ reviewer: "story worker" }, "STORY_LEXICON_REVIEWER_INVALID"],
    [{ reviewer: "writer" }, "STORY_LEXICON_REVIEWER_INVALID"],
    [{ reviewer: "listener-model" }, "STORY_LEXICON_REVIEWER_INVALID"],
    [{ reviewer: "automation" }, "STORY_LEXICON_REVIEWER_INVALID"],
    [{ reviewer: "self" }, "STORY_LEXICON_REVIEWER_INVALID"],
    [{ reviewer: "" }, "STORY_LEXICON_REVIEWER_INVALID"],
    [{ reviewed_at: "yesterday" }, "STORY_LEXICON_REVIEW_TIME_INVALID"],
    [{ reviewed_at: "2026-10-18T12:00:00Z" }, "STORY_LEXICON_REVIEW_TIME_INVALID"],
    [{ independent: false }, "STORY_LEXICON_REVIEW_NOT_INDEPENDENT"],
    [{ independent: "yes" }, "STORY_LEXICON_REVIEW_NOT_INDEPENDENT"],
    [{ kind: "something_else" }, "STORY_LEXICON_REVIEW_INVALID"],
    [{ extra: 1 }, "STORY_LEXICON_REVIEW_INVALID"],
  ];
  const before = everything(b);
  for (const [override, code] of cases) assert.throws(() => run(b, filled(b, ACCEPT_BOTH, override)), error(code), JSON.stringify(override));
  const decisionCases = [
    [{ Paul: { decision: "accept" } }, "STORY_LEXICON_REVIEW_DECISIONS_MISMATCH", { Bocuse: undefined }],
    [{ ...ACCEPT_BOTH, Lyon: { proposed: null, decision: "accept" } }, "STORY_LEXICON_REVIEW_DECISIONS_MISMATCH"],
    [{ Paul: { decision: "maybe" }, Bocuse: { decision: "accept" } }, "STORY_LEXICON_REVIEW_DECISION_INVALID"],
    [{ Paul: { decision: "accept_as" }, Bocuse: { decision: "accept" } }, "STORY_LEXICON_REVIEW_DECISION_INVALID"],
    [{ Paul: { decision: "accept", spoken: "保羅" }, Bocuse: { decision: "accept" } }, "STORY_LEXICON_REVIEW_DECISION_INVALID"],
    [{ Paul: { decision: "accept" }, Bocuse: { decision: "accept", proposed: "博古士" } }, "STORY_LEXICON_REVIEW_DECISION_INVALID"],
  ];
  for (const [decisions, code, drop = {}] of decisionCases) {
    const value = JSON.parse(filled(b, decisions));
    for (const term of Object.keys(drop)) delete value.decisions[term];
    for (const [term, entry] of Object.entries(decisions)) if (!value.decisions[term]) value.decisions[term] = entry;
    assert.throws(() => run(b, Buffer.from(JSON.stringify(value))), error(code), JSON.stringify(decisions));
  }
  assert.throws(() => run(b, Buffer.from("not json")), error("STORY_LEXICON_REVIEW_INVALID"));
  assert.deepEqual(everything(b), before);
  // The CLI reports a refusal with exit 1.
  const file = path.join(b.root, "..", "bad.json");
  writeFileSync(file, filled(b, ACCEPT_BOTH, { reviewer: "worker" }));
  const refused = await cli(b, "--review", file, "--apply");
  assert.equal(refused.code, 1);
  assert.match(refused.out, /refused: STORY_LEXICON_REVIEWER_INVALID/);
  assert.equal(videoLexicon(b).sequence, 1);
});

test("the wrong work directory is refused with zero writes", async t => {
  const b = box(t);
  const receipt = filled(b, ACCEPT_BOTH);
  const file = path.join(b.root, "..", "receipt.json");
  writeFileSync(file, receipt);
  const before = everything(b);
  // An empty work base (a forgotten VIDEO_WORKDIR): the story's directory does not exist there.
  const empty = path.join(b.root, "..", "empty-base");
  mkdirSync(empty);
  let out = "";
  const io = { root: b.root, env: {}, stdout: { write: s => { out += s; } }, stderr: { write: s => { out += s; } }, now: NOW };
  assert.equal(await main(["story-lexicon-revise", "--slug", SLUG, "--workdir", empty, "--review", file, "--apply"], io), 1);
  assert.match(out, /STORY_LEXICON_REVISION_WORKDIR_UNPROVEN/);
  // Another story's work directory under the right name.
  const other = { ...b, workdir: path.join(b.root, "..", "other", SLUG) };
  mkdirSync(path.join(other.workdir, "story", "chapters"), { recursive: true });
  writeFileSync(path.join(other.workdir, "story", "chapters", "1.json"), json({}));
  writeFileSync(path.join(other.workdir, "auto.json"), json({ slug: "story-adapt-someone-else", story: {} }));
  assert.throws(() => run(other, receipt), error("STORY_LEXICON_REVISION_WORKDIR_UNPROVEN"));
  // No story state at all.
  writeFileSync(path.join(other.workdir, "auto.json"), json({ slug: SLUG }));
  assert.throws(() => run(other, receipt), error("STORY_LEXICON_REVISION_WORKDIR_UNPROVEN"));
  assert.deepEqual(everything(b), before);
  assert.ok(!existsSync(path.join(other.workdir, "LEASE")));
  assert.ok(!existsSync(path.join(other.workdir, "story", "lexicon-reviews")));
  assert.ok(!existsSync(path.join(empty, SLUG)));
});

test("a STOP file or a held lease refuses without publishing", t => {
  const b = box(t);
  const receipt = filled(b, ACCEPT_BOTH);
  writeFileSync(path.join(b.workdir, "STOP"), "");
  const before = everything(b);
  assert.throws(() => run(b, receipt), error("LEXICON_STOPPED"));
  assert.deepEqual(everything(b), before);
  rmSync(path.join(b.workdir, "STOP"));
  writeFileSync(path.join(b.workdir, "LEASE"), json({ schema_version: 1, token: "worker", owner: "auto", pid: 1, host: "another-host" }));
  assert.throws(() => run(b, receipt), error("video_project_leased"));
  assert.equal(videoLexicon(b).sequence, 1);
  assert.ok(!existsSync(path.join(b.workdir, "story", "lexicon-reviews")));
});

test("--proposal narrows the template, and an unknown one is refused", async t => {
  const b = box(t);
  assert.deepEqual(proposeStoryLexicon({ ...b, additions: { Lyon: null } }), ["Lyon"]);
  const all = inspectStoryLexiconRevision(b);
  const lyon = all.proposals.find(each => Object.hasOwn(each.pending, "Lyon")).sha256;
  const one = inspectStoryLexiconRevision({ ...b, only: [lyon] });
  assert.deepEqual(Object.keys(one.template.decisions), ["Lyon"]);
  const listed = await cli(b, "--proposal", "a".repeat(64), "--json");
  assert.equal(listed.code, 1);
  assert.equal(JSON.parse(listed.out).refusals[0].code, "STORY_LEXICON_PROPOSAL_UNKNOWN");
});
