import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { existsSync, mkdirSync, mkdtempSync, readFileSync, readdirSync, rmSync, symlinkSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import test from "node:test";

import { runManualBootstrapCli } from "../lexicon-manual-bootstrap.mjs";
import { bootstrapManualStoryLexicon, inspectManualStoryBootstrap, MANUAL_BOOTSTRAP_REASON, recoverCommittedManualBootstrap } from "./lexicon-manual-bootstrap.mjs";
import { videoLexicon } from "./lexicon-store.mjs";
import { planInitialStoryLexicon } from "./story-lexicon.mjs";

const SLUG = "story-reviewed-manual-draft";
const hash = bytes => createHash("sha256").update(bytes).digest("hex");
const json = value => `${JSON.stringify(value, null, 2)}\n`;
const error = code => value => value?.code === code;

function fixture(t) {
  const top = mkdtempSync(path.join(tmpdir(), "manual-lexicon-bootstrap-"));
  t.after(() => rmSync(top, { recursive: true, force: true }));
  const root = path.join(top, "repo");
  const base = path.join(top, "media");
  const workdir = path.join(base, SLUG);
  const dir = path.join(root, "docs", "videos", SLUG);
  const reviewDir = path.join(dir, "reviews");
  mkdirSync(reviewDir, { recursive: true });
  const shared = { schema_version: 1, terms: { DVD: "D V D" } };
  writeFileSync(path.join(root, "docs", "videos", "lexicon.json"), json(shared));
  const series = { kind: "story", slug: "brand-extra", episode: 3, names: ["Netflix", "DVD", "網飛", "Blockbuster"] };
  const video = { schema_version: 1, slug: SLUG, format: "drama", category: "explainer", series: { slug: series.slug, episode: 3 }, scenes: [{ id: "one", lines: [{ id: "a", text: "Netflix" }] }] };
  const videoFile = path.join(dir, "video.json");
  const seriesFile = path.join(dir, "series.json");
  writeFileSync(videoFile, json(video));
  writeFileSync(seriesFile, json(series));
  const videoSha = hash(readFileSync(videoFile));
  const evidence = [
    ["source", "source-review.md"], ["narrative_a", "blind-a.md"], ["narrative_b", "blind-b.md"],
  ].map(([role, name]) => {
    const file = path.join(reviewDir, name);
    writeFileSync(file, `# ${role}\nReview of video.json SHA-256 ${videoSha}: PASS.\n`);
    return { role, file: `reviews/${name}`, sha256: hash(readFileSync(file)) };
  });
  const reviewFile = path.join(reviewDir, "lexicon-bootstrap.json");
  writeFileSync(reviewFile, json({ schema_version: 1, kind: "manual_story_lexicon_bootstrap_review", slug: SLUG,
    video_json_sha256: videoSha, series_json_sha256: hash(readFileSync(seriesFile)),
    decision: "pin_unspoken_manual_draft", reviewer: "independent-reviewer", evidence }));
  return { top, root, base, dir, workdir, reviewFile, videoFile, seriesFile, videoSha, series, evidence };
}

function tree(dir) {
  if (!existsSync(dir)) return {};
  const result = {};
  function visit(parent) {
    for (const entry of readdirSync(parent, { withFileTypes: true })) {
      const file = path.join(parent, entry.name);
      if (entry.isDirectory()) visit(file);
      else if (entry.isFile()) result[path.relative(dir, file)] = hash(readFileSync(file));
    }
  }
  visit(dir);
  return result;
}

function cli(box, ...args) {
  let out = ""; let err = "";
  const code = runManualBootstrapCli(["--slug", SLUG, "--workdir", box.base, ...args], {
    root: box.root, stdout: { write: text => { out += text; } }, stderr: { write: text => { err += text; } },
    now: () => new Date("2026-10-20T13:00:00Z"),
  });
  return { code, out, err };
}

test("reviewed manual draft: dry run writes nothing, apply pins standard genesis and records immutable provenance", t => {
  const b = fixture(t);
  const before = tree(b.top);
  const report = inspectManualStoryBootstrap({ root: b.root, slug: SLUG, workdir: b.workdir, reviewFile: b.reviewFile });
  assert.equal(report.status, "allowed");
  assert.deepEqual(report.seeded_terms, ["Netflix", "Blockbuster"]);
  assert.equal(cli(b, "--review", b.reviewFile).code, 0);
  assert.deepEqual(tree(b.top), before);
  const applied = cli(b, "--review", b.reviewFile, "--apply", "--json");
  assert.equal(applied.code, 0, applied.err || applied.out);
  assert.equal(JSON.parse(applied.out).applied.bootstrapped, true);
  const current = videoLexicon({ root: b.root, slug: SLUG, workdir: b.workdir, requireSnapshot: true });
  assert.equal(current.lexicon_sha256, report.lexicon_sha256);
  assert.deepEqual(current.lexicon.terms, { DVD: "D V D", Netflix: null, Blockbuster: null });
  const planned = planInitialStoryLexicon({ slug: SLUG, sharedBytes: json(current.lexicon) });
  assert.equal(planned.lexicon_sha256, current.lexicon_sha256);
  const sidecar = JSON.parse(readFileSync(path.join(b.dir, "story-lexicon", "manual-bootstraps", `${current.head_event_sha256}.json`)));
  assert.equal(sidecar.reason, MANUAL_BOOTSTRAP_REASON);
  assert.equal(sidecar.video_json_sha256, b.videoSha);
  assert.equal(sidecar.review_receipt_sha256, hash(readFileSync(b.reviewFile)));
  assert.equal(sidecar.evidence.length, 3);
  const [receipt] = readdirSync(path.join(b.workdir, "story", "lexicon-transactions"))
    .map(name => JSON.parse(readFileSync(path.join(b.workdir, "story", "lexicon-transactions", name))));
  assert.equal(receipt.status, "committed");
  assert.equal(receipt.bootstrap, MANUAL_BOOTSTRAP_REASON);
  assert.equal(existsSync(path.join(b.dir, "story-lexicon", "pending.json")), false);
  assert.deepEqual(readdirSync(path.join(b.workdir, "story", "lexicon-intents")), []);
  const after = tree(b.top);
  const again = bootstrapManualStoryLexicon({ root: b.root, slug: SLUG, workdir: b.workdir, reviewFile: b.reviewFile });
  assert.equal(again.bootstrapped, false);
  assert.equal(cli(b, "--review", b.reviewFile, "--apply").code, 0);
  assert.deepEqual(tree(b.top), after);
});

test("stale script, series or evidence refuses before any workdir or lease is created", t => {
  for (const mutate of [
    b => writeFileSync(b.videoFile, `${readFileSync(b.videoFile, "utf8")} `),
    b => writeFileSync(b.seriesFile, `${readFileSync(b.seriesFile, "utf8")} `),
    b => writeFileSync(path.join(b.dir, b.evidence[0].file), "different evidence"),
  ]) {
    const b = fixture(t);
    mutate(b);
    const before = tree(b.top);
    const run = cli(b, "--review", b.reviewFile, "--apply");
    assert.equal(run.code, 1);
    assert.equal(existsSync(b.workdir), false);
    assert.deepEqual(tree(b.top), before);
  }
});

test("existing media, approvals, worker state, STOP or a pending transaction blocks manual bootstrap", t => {
  const states = [
    ["timeline.json", "{}"], ["audio/one.wav", "audio"], ["narration.wav", "audio"],
    ["approvals.json", "{}"], ["auto.json", "{}"], ["story/chapters/1.json", "{}"],
    ["media/ledger.json", "{}"], ["story/lexicon-intents/old.json", "{}"], ["STOP", ""],
  ];
  for (const [relative, data] of states) {
    const b = fixture(t);
    const file = path.join(b.workdir, relative);
    mkdirSync(path.dirname(file), { recursive: true });
    writeFileSync(file, data);
    const before = tree(b.top);
    const report = inspectManualStoryBootstrap({ root: b.root, slug: SLUG, workdir: b.workdir, reviewFile: b.reviewFile });
    assert.equal(report.status, "refused", relative);
    assert.equal(cli(b, "--review", b.reviewFile, "--apply").code, 1, relative);
    assert.deepEqual(tree(b.top), before);
  }
});

test("an unsafe or missing review, and a workdir inside the repository, refuse without writes", t => {
  const b = fixture(t);
  assert.equal(cli(b, "--review", path.join(b.top, "outside.json"), "--apply").code, 1);
  assert.equal(cli(b, "--review", b.reviewFile, "--workdir", path.join(b.root, "media"), "--apply").code, 2);
  assert.equal(existsSync(b.workdir), false);
});

test("a symlinked review directory cannot supply source evidence from outside the story", t => {
  const b = fixture(t);
  const reviewsDir = path.join(b.dir, "reviews");
  const outside = path.join(b.top, "outside-reviews");
  mkdirSync(outside);
  for (const name of readdirSync(reviewsDir)) writeFileSync(path.join(outside, name), readFileSync(path.join(reviewsDir, name)));
  rmSync(reviewsDir, { recursive: true });
  symlinkSync(outside, reviewsDir);
  const report = inspectManualStoryBootstrap({ root: b.root, slug: SLUG, workdir: b.workdir, reviewFile: b.reviewFile });
  assert.equal(report.status, "refused");
  assert.equal(report.checks.find(check => check.id === "review_receipt").code, "MANUAL_BOOTSTRAP_REVIEW_UNSAFE");
  assert.equal(existsSync(b.workdir), false);
});

test("one evidence file cannot be counted as two independent review roles", t => {
  const b = fixture(t);
  const receipt = JSON.parse(readFileSync(b.reviewFile));
  receipt.evidence[1].file = receipt.evidence[0].file;
  receipt.evidence[1].sha256 = receipt.evidence[0].sha256;
  writeFileSync(b.reviewFile, json(receipt));
  const report = inspectManualStoryBootstrap({ root: b.root, slug: SLUG, workdir: b.workdir, reviewFile: b.reviewFile });
  assert.equal(report.status, "refused");
  assert.equal(report.checks.find(check => check.id === "review_receipt").code, "MANUAL_BOOTSTRAP_REVIEW_INVALID");
  assert.equal(existsSync(b.workdir), false);
});

test("before a commit receipt, every crash point remains held and cannot be auto-recovered", t => {
  for (const point of ["work-intent", "docs-intent", "immutable-files", "current-pointer"]) {
    const b = fixture(t);
    assert.throws(() => bootstrapManualStoryLexicon({ root: b.root, slug: SLUG, workdir: b.workdir, reviewFile: b.reviewFile,
      checkpoint: at => { if (at === point) throw new Error(`crash ${point}`); } }), new RegExp(`crash ${point}`));
    const report = inspectManualStoryBootstrap({ root: b.root, slug: SLUG, workdir: b.workdir, reviewFile: b.reviewFile });
    assert.equal(report.status, "refused", point);
    assert.throws(() => videoLexicon({ root: b.root, slug: SLUG, workdir: b.workdir, requireSnapshot: true }),
      error("LEXICON_TRANSACTION_INCOMPLETE"), point);
    assert.equal(existsSync(path.join(b.workdir, "story", "lexicon-transactions")), false);
  }
});

test("a crash after the committed receipt is recovered only with matching immutable evidence", t => {
  for (const point of ["work-receipt", "docs-intent-cleared"]) {
    const b = fixture(t);
    assert.throws(() => bootstrapManualStoryLexicon({ root: b.root, slug: SLUG, workdir: b.workdir, reviewFile: b.reviewFile,
      checkpoint: at => { if (at === point) throw new Error(`crash ${point}`); } }), new RegExp(`crash ${point}`));
    const [name] = readdirSync(path.join(b.workdir, "story", "lexicon-transactions"));
    const transactionId = name.replace(/\.json$/, "");
    assert.equal(inspectManualStoryBootstrap({ root: b.root, slug: SLUG, workdir: b.workdir, reviewFile: b.reviewFile }).status, "refused");
    const recovered = recoverCommittedManualBootstrap({ root: b.root, slug: SLUG, workdir: b.workdir, transactionId });
    assert.equal(recovered.mode, "snapshot");
    assert.equal(videoLexicon({ root: b.root, slug: SLUG, workdir: b.workdir, requireSnapshot: true }).mode, "snapshot");
    assert.equal(existsSync(path.join(b.dir, "story-lexicon", "pending.json")), false);
    assert.deepEqual(readdirSync(path.join(b.workdir, "story", "lexicon-intents")), []);
  }
});

test("recovery refuses a changed provenance sidecar and preserves both intents", t => {
  const b = fixture(t);
  assert.throws(() => bootstrapManualStoryLexicon({ root: b.root, slug: SLUG, workdir: b.workdir, reviewFile: b.reviewFile,
    checkpoint: at => { if (at === "work-receipt") throw new Error("crash after receipt"); } }), /crash after receipt/);
  const [name] = readdirSync(path.join(b.workdir, "story", "lexicon-transactions"));
  const transactionId = name.replace(/\.json$/, "");
  const receipt = JSON.parse(readFileSync(path.join(b.workdir, "story", "lexicon-transactions", name)));
  const sidecar = path.join(b.dir, "story-lexicon", "manual-bootstraps", `${receipt.head_event_sha256}.json`);
  writeFileSync(sidecar, `${readFileSync(sidecar, "utf8")} `);
  assert.throws(() => recoverCommittedManualBootstrap({ root: b.root, slug: SLUG, workdir: b.workdir, transactionId }),
    error("MANUAL_BOOTSTRAP_SIDECAR_INVALID"));
  assert.equal(existsSync(path.join(b.dir, "story-lexicon", "pending.json")), true);
  assert.deepEqual(readdirSync(path.join(b.workdir, "story", "lexicon-intents")), [`${transactionId}.json`]);
});
