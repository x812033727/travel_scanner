import { createHash } from "node:crypto";
import { spawnSync } from "node:child_process";
import { copyFileSync, mkdtempSync, readFileSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { NARRATIVE_PANEL, PANEL_RULES_SHA256, mergePanelVerdicts, panelVerdict } from "../../../../../tools/video/core/narrative.mjs";

const here = dirname(fileURLToPath(import.meta.url));
const episode = join(here, "../..");
const repo = join(episode, "../../..");
const sha = (bytes) => createHash("sha256").update(bytes).digest("hex");
const fileHash = (file) => sha(readFileSync(file));
const json = (file) => JSON.parse(readFileSync(file, "utf8"));
const save = (name, value) => writeFileSync(join(here, name), `${JSON.stringify(value, null, 2)}\n`);

const expected = {
  "research.md": "d0077504f3dbe828363158a25c7e7dade955089f49dbb03a734893739e12467e",
  "brief.md": "9d68d7b4dad27f56b6dbc53f7890bc0db84590de3e445302f8f4836c286ac1e3",
  "claims.md": "e19a8aa75c7d61bbba54b4d747db3b7025ac34599964ac0c4c115fbacd8d8c0b",
  "video.json": "108db5d8ae5b540e396b1e9add3490c7ac8761e1aaa7dfd76b172edbadaba226",
  "script.md": "5b18eb40b5c3434599abbd939d3231fc30837e360bfaff0ea00d23cdca89cf48",
};
const creative = () => Object.fromEntries(Object.keys(expected).map((name) => [name, fileHash(join(episode, name))]));
const assertFrozen = (stage) => {
  const actual = creative();
  if (Object.keys(expected).some((name) => actual[name] !== expected[name])) throw new Error(`R4 creative SHA drift ${stage}: ${JSON.stringify(actual)}`);
  return actual;
};

const original = {
  a: {
    answers: join(here, "../r4-blind-a/narrative-answers.json"),
    answer_sha256: "62a38b963d75660afdc4a9c8c0bcb9e627f5a28dddad420bbea923d3639ee943",
    review: join(here, "../r4-blind-a/narrative.md"),
    review_sha256: "d5f1d9ff858ba0cbbfd0a26d9d52118652f8d0e7997e1b56ad025c0d4aa75a06",
    receipt: join(here, "../r4-blind-a/official-narrative-record.json"),
  },
  b: {
    answers: join(here, "../r4-blind-b.json"),
    answer_sha256: "e19b677fa2c06b5786177efd6e5b548e4224222711ae87888da7a014be826e8b",
    review: join(here, "../r4-blind-b.md"),
    review_sha256: "48acf90cc70c41cb13457708ae7d37c549caaaa534eb354b5aa19f46a2fbddb3",
    receipt: join(here, "../r4-blind-b-cli-receipt.json"),
  },
};
const sourceReview = join(here, "../r4-source-independent.md");
const sourceReviewHash = "6a90a86efe7553ee408f736fd814d44f87ff298eac71cdd288da057d154faef7";

const frozenBefore = assertFrozen("before merge");
if (fileHash(sourceReview) !== sourceReviewHash) throw new Error("independent source/written-visual review changed");
if (!readFileSync(sourceReview, "utf8").includes("**史料／逐句主張 PASS；書面畫面 HOLD（僅 `s59027` 一景）。**")) throw new Error("source or visual gate status changed");

const lines = new Map(json(join(episode, "video.json")).scenes.flatMap((scene) => (scene.lines ?? []).map((line) => [line.id, line.text])));
const readers = [];
const verdicts = [];
let binding = null;
for (const name of ["a", "b"]) {
  const input = original[name];
  if (fileHash(input.answers) !== input.answer_sha256 || fileHash(input.review) !== input.review_sha256) throw new Error(`reader ${name} frozen ballot changed`);
  const answer = json(input.answers);
  if (answer.answers.length !== NARRATIVE_PANEL.length) throw new Error(`reader ${name} answer count`);
  for (const [index, entry] of answer.answers.entries()) {
    if (entry.id !== NARRATIVE_PANEL[index].id) throw new Error(`reader ${name} panel order`);
    const match = /^\[([^\]]+)\] (.*)$/u.exec(entry.evidence);
    if (!match || lines.get(match[1]) !== match[2]) throw new Error(`reader ${name} quote mismatch: ${entry.id}`);
  }
  const verdict = panelVerdict(answer);
  if (verdict.answers.some((entry, index) => entry.yes !== answer.answers[index].yes)) throw new Error(`reader ${name} official verdict changed a vote`);
  const receipt = json(input.receipt);
  const currentBinding = [receipt.panel_rules_sha256, receipt.panel_narration_sha256, receipt.script_hash, receipt.narrative_hash];
  if (currentBinding[0] !== PANEL_RULES_SHA256 || !receipt.passed || receipt.failed.length || receipt.advisory.length) throw new Error(`reader ${name} receipt invalid`);
  if (binding && currentBinding.some((value, index) => value !== binding[index])) throw new Error("reader receipts differ in panel/script binding");
  binding = currentBinding;
  copyFileSync(input.answers, join(here, `raw-ballot-${name}.json`));
  copyFileSync(input.review, join(here, `raw-review-${name}.md`));
  readers.push({ reader: name, answers_sha256: input.answer_sha256, review_sha256: input.review_sha256, receipt_sha256: fileHash(input.receipt), yes: verdict.answers.filter((entry) => entry.yes).length, no: verdict.failed.map((entry) => entry.id), advisory_no: verdict.advisory.map((entry) => entry.id) });
  verdicts.push(verdict);
}

const merged = mergePanelVerdicts(verdicts);
const answers = { answers: merged.answers.map(({ id, yes, evidence }) => ({ id, yes, evidence })) };
save("merged-answers.json", answers);
const mergeAudit = {
  slug: "curio-s59",
  round: "R4",
  rule: "fixed OR: a question passes when at least one reader has a cited yes",
  creative_sha256: frozenBefore,
  panel_rules_sha256: PANEL_RULES_SHA256,
  panel_narration_sha256: binding[1],
  readers,
  merged_answers_sha256: fileHash(join(here, "merged-answers.json")),
  merged: { passed: merged.passed, yes: merged.answers.filter((entry) => entry.yes).length, failed: merged.failed.map((entry) => entry.id), advisory: merged.advisory.map((entry) => entry.id), answers: merged.answers.map(({ id, required, yes, evidence, yes_readers }) => ({ id, required, yes, evidence, yes_readers })) },
};
save("merge-audit.json", mergeAudit);
if (!merged.passed || mergeAudit.merged.yes !== 13 || merged.answers.some((entry) => entry.yes_readers !== 2)) throw new Error("unexpected R4 fixed OR result");

const workdir = mkdtempSync(join(tmpdir(), "s59-r4-formal-merge-"));
const args = [join(repo, "tools/video/cli.mjs"), "narrative", "--slug", "curio-s59", "--answers", join(here, "merged-answers.json"), "--workdir", workdir, "--json"];
const run = spawnSync(process.execPath, args, { cwd: repo, encoding: "utf8", timeout: 300000 });
if (run.error) throw run.error;
writeFileSync(join(here, "cli-stdout.json"), run.stdout);
writeFileSync(join(here, "cli-stderr.txt"), run.stderr);
writeFileSync(join(here, "cli-exit-code.txt"), `${run.status}\n`);
const officialPath = join(workdir, "curio-s59/review/narrative.json");
copyFileSync(officialPath, join(here, "official-narrative-record.json"));
const official = json(officialPath);
const stdout = JSON.parse(run.stdout);
const frozenAfter = assertFrozen("after CLI");
const cliStatus = {
  command: `${process.execPath} ${args.join(" ")}`,
  workdir,
  exit_code: run.status,
  stdout_sha256: fileHash(join(here, "cli-stdout.json")),
  stderr_sha256: fileHash(join(here, "cli-stderr.txt")),
  official_record_sha256: fileHash(officialPath),
  creative_sha256_before: frozenBefore,
  creative_sha256_after: frozenAfter,
  creative_unchanged: true,
  passed: stdout.passed,
  failed: stdout.failed.map((entry) => entry.id),
  advisory: stdout.advisory.map((entry) => entry.id),
  official_round: official.round,
  panel_rules_sha256: official.panel_rules_sha256,
  panel_narration_sha256: official.panel_narration_sha256,
  narrative_hash: official.narrative_hash,
};
save("cli-status.json", cliStatus);
if (run.status !== 0 || !stdout.passed || !official.passed || stdout.failed.length || stdout.advisory.length || official.panel_rules_sha256 !== binding[0] || official.panel_narration_sha256 !== binding[1]) throw new Error("unexpected formal R4 CLI result");

// The independent written-visual audit is a pre-media gate. This is not the later Jev QA call.
const policy = {
  slug: "curio-s59",
  round: "R4",
  creative_sha256: frozenAfter,
  narrative: { status: "PASS", readers: 2, fixed_or_yes: 13, required_failed: [], official_record_sha256: cliStatus.official_record_sha256 },
  source_and_claims: { status: "PASS", independent_review_sha256: sourceReviewHash },
  written_visual: { status: "HOLD", independent_review_sha256: sourceReviewHash, blocker: { scene: "s59027", detail: "Prompt directs a finger along the groove where the spoken mechanism calls for a needle/contact reading the trace." } },
  pre_media_policy: { status: "HOLD", paid_media_allowed: false, reason: "s59027 written-visual contradiction requires prompt-only repair and fresh visual review on the new video.json hash" },
};
save("policy-gate.json", policy);
process.stdout.write(`${JSON.stringify({ merged: mergeAudit.merged.yes, readers: readers.map(({ reader, yes }) => ({ reader, yes })), cli: cliStatus.passed, pre_media_policy: policy.pre_media_policy.status, workdir }, null, 2)}\n`);
