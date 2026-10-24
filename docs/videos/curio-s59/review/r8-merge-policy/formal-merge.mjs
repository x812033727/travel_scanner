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
const sha = (file) => createHash("sha256").update(readFileSync(file)).digest("hex");
const json = (file) => JSON.parse(readFileSync(file, "utf8"));
const save = (name, value) => writeFileSync(join(here, name), `${JSON.stringify(value, null, 2)}\n`);

const frozen = {
  "research.md": "39a48f08ca01dfa18009e9c1819684d03b92c52656952affd3266a574d88067d",
  "brief.md": "9d68d7b4dad27f56b6dbc53f7890bc0db84590de3e445302f8f4836c286ac1e3",
  "claims.md": "aeb0cd64b8ddeb992e70c3daa813f42d475718e707e82e62f0da4a7684d95f95",
  "video.json": "f29d9f55dbea7ee52a19e6c885ed36f26f51b30fc7fe0fa4caa87b7ea9d3a33b",
  "script.md": "f0fd2a6069844fe99e994367f3fa8d27b36928231dc0695fd816762c18faf07b",
};
function assertFrozen(stage) {
  const actual = Object.fromEntries(Object.keys(frozen).map((name) => [name, sha(join(episode, name))]));
  if (Object.keys(frozen).some((name) => actual[name] !== frozen[name])) throw new Error(`${stage}: creative drift ${JSON.stringify(actual)}`);
  return actual;
}

const sourceReview = join(here, "../r8-source-independent.md");
const sourceSha = "e846ae6277bb3ecaedf52c01d3ee169a411b3de5375ec580c157aa642abafa87";
const inputs = {
  A: {
    answers: join(here, "../r8-blind-a/answers.json"),
    answersSha: "3d6f382a8fa806337f03044da5b6f34d6abac1810c29826e45b1fb9b6a863f74",
    review: join(here, "../r8-blind-a.md"),
    reviewSha: "971524fe74b0a0112edc208ee5504be206b04a48af9679c4edefdd8c8f4380f6",
    official: join(here, "../r8-blind-a/official-narrative-record.json"),
    officialSha: "2f51ec8673baee73146883b40c547fcbb2fd90d1fd6ec827e35f5eb8dd411504",
    stdout: join(here, "../r8-blind-a/cli-stdout.json"),
    stdoutSha: "265396daa5c48467bbc8d50444c915029f5b3229c1a647866c73ade14c44d676",
    stderr: join(here, "../r8-blind-a/cli-stderr.txt"),
    stderrSha: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    exit: join(here, "../r8-blind-a/cli-exit-code.txt"),
    exitSha: "4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865",
  },
  B: {
    answers: join(here, "../r8-blind-b/answers.json"),
    answersSha: "62f2cec3480e3650778dbb9ba57eb791b391211fceed72a725440c7fb90c54f0",
    review: join(here, "../r8-blind-b.md"),
    reviewSha: "c1333ad2f4b37cb439f0b7d1d3168384f3d7080daf1d60f282946cb3b49dd2b0",
    official: join(here, "../r8-blind-b/official-narrative-record.json"),
    officialSha: "d0ed013ba9c0c0f658ee51219ae2252331bf50b0f1ec8304c77dc92e17c1b903",
    stdout: join(here, "../r8-blind-b/cli-stdout.json"),
    stdoutSha: "9ba1a7de6c855fa50c20a46804cc7fb430546cf2eefe308cbf2f846227d0eff3",
    stderr: join(here, "../r8-blind-b/cli-stderr.txt"),
    stderrSha: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    exit: join(here, "../r8-blind-b/cli-exit-code.txt"),
    exitSha: "4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865",
  },
};
const before = assertFrozen("before merge");
if (sha(sourceReview) !== sourceSha || !readFileSync(sourceReview, "utf8").includes("書面畫面 PASS")) throw new Error("R8 independent source review drift");
const lines = new Map(json(join(episode, "video.json")).scenes.flatMap((scene) => (scene.lines ?? []).map((line) => [line.id, line.text])));
const verdicts = [];
const readers = [];
let binding = null;
for (const label of ["A", "B"]) {
  const input = inputs[label];
  for (const [name, path, expected] of [["answers", input.answers, input.answersSha], ["review", input.review, input.reviewSha], ["official", input.official, input.officialSha], ["stdout", input.stdout, input.stdoutSha], ["stderr", input.stderr, input.stderrSha], ["exit", input.exit, input.exitSha]]) {
    if (sha(path) !== expected) throw new Error(`reader ${label} ${name} drift`);
  }
  const answer = json(input.answers);
  if (answer.answers.length !== NARRATIVE_PANEL.length) throw new Error(`reader ${label} answer count`);
  for (const [i, entry] of answer.answers.entries()) {
    if (entry.id !== NARRATIVE_PANEL[i].id) throw new Error(`reader ${label} panel order`);
    const match = /^\[([^\]]+)\] (.*)$/u.exec(entry.evidence);
    if (!match || lines.get(match[1]) !== match[2]) throw new Error(`reader ${label} citation mismatch ${entry.id}`);
  }
  const verdict = panelVerdict(answer);
  const receipt = json(input.official);
  const currentBinding = [receipt.panel_rules_sha256, receipt.panel_narration_sha256, receipt.script_hash, receipt.narrative_hash];
  if (currentBinding[0] !== PANEL_RULES_SHA256 || receipt.round !== 1 || receipt.passed !== verdict.passed || JSON.stringify(receipt.advisory) !== JSON.stringify(verdict.advisory.map((entry) => entry.id))) throw new Error(`reader ${label} official receipt invalid`);
  if (binding && currentBinding.some((value, i) => value !== binding[i])) throw new Error("reader receipts bind different input");
  binding = currentBinding;
  if (JSON.stringify(receipt.failed) !== JSON.stringify(verdict.failed.map((entry) => entry.id))) throw new Error(`reader ${label} official votes differ`);
  if (receipt.answers.some((entry, i) => entry.yes !== answer.answers[i].yes || entry.evidence !== answer.answers[i].evidence)) throw new Error(`reader ${label} receipt altered vote or citation`);
  copyFileSync(input.answers, join(here, `raw-ballot-${label.toLowerCase()}.json`));
  copyFileSync(input.review, join(here, `raw-review-${label.toLowerCase()}.md`));
  copyFileSync(input.official, join(here, `reader-${label.toLowerCase()}-official.json`));
  copyFileSync(input.stdout, join(here, `reader-${label.toLowerCase()}-stdout.json`));
  copyFileSync(input.stderr, join(here, `reader-${label.toLowerCase()}-stderr.txt`));
  copyFileSync(input.exit, join(here, `reader-${label.toLowerCase()}-exit-code.txt`));
  readers.push({ label, answers_sha256: input.answersSha, review_sha256: input.reviewSha, official_sha256: input.officialSha, stdout_sha256: input.stdoutSha, stderr_sha256: input.stderrSha, exit_sha256: input.exitSha, yes: verdict.answers.filter((entry) => entry.yes).length, failed: verdict.failed.map((entry) => entry.id) });
  verdicts.push(verdict);
}

const merged = mergePanelVerdicts(verdicts);
const mergedAnswers = { answers: merged.answers.map(({ id, yes, evidence }) => ({ id, yes, evidence })) };
save("merged-answers.json", mergedAnswers);
if (merged.passed || merged.answers.filter((entry) => entry.yes).length !== 12 || JSON.stringify(merged.failed.map((entry) => entry.id)) !== JSON.stringify(["payoffs"])) throw new Error("unexpected R8 fixed OR result");
save("merge-audit.json", {
  slug: "curio-s59", round: "R8", rule: "fixed OR: a cited yes from either independent reader passes a question", creative_sha256: before,
  panel_rules_sha256: PANEL_RULES_SHA256, panel_narration_sha256: binding[1], readers, merged_answers_sha256: sha(join(here, "merged-answers.json")),
  result: { passed: merged.passed, yes: 12, failed: ["payoffs"], advisory: [], answers: merged.answers.map(({ id, required, yes, evidence, yes_readers }) => ({ id, required, yes, evidence, yes_readers })) },
});

const workdir = mkdtempSync(join(tmpdir(), "s59-r8-formal-merge-"));
const args = [join(repo, "tools/video/cli.mjs"), "narrative", "--slug", "curio-s59", "--answers", join(here, "merged-answers.json"), "--workdir", workdir, "--json"];
const run = spawnSync(process.execPath, args, { cwd: repo, encoding: "utf8", timeout: 300000 });
if (run.error) throw run.error;
writeFileSync(join(here, "cli-stdout.json"), run.stdout);
writeFileSync(join(here, "cli-stderr.txt"), run.stderr);
writeFileSync(join(here, "cli-exit-code.txt"), `${run.status}\n`);
const officialPath = join(workdir, "curio-s59/review/narrative.json");
copyFileSync(officialPath, join(here, "official-narrative-record.json"));
const stdout = JSON.parse(run.stdout);
const official = json(officialPath);
const after = assertFrozen("after official CLI");
if (run.status !== 1 || stdout.passed || official.passed || JSON.stringify(stdout.failed.map((entry) => entry.id)) !== JSON.stringify(["payoffs"]) || JSON.stringify(official.failed) !== JSON.stringify(["payoffs"]) || official.panel_rules_sha256 !== binding[0] || official.panel_narration_sha256 !== binding[1]) throw new Error("unexpected R8 official CLI verdict");
save("cli-status.json", { command: [process.execPath, ...args], workdir, exit_code: run.status, stdout_sha256: sha(join(here, "cli-stdout.json")), stderr_sha256: sha(join(here, "cli-stderr.txt")), official_sha256: sha(officialPath), creative_sha256_before: before, creative_sha256_after: after, passed: false, failed: ["payoffs"], narrative_hash: official.narrative_hash, panel_rules_sha256: official.panel_rules_sha256, panel_narration_sha256: official.panel_narration_sha256 });
save("policy-gate.json", { slug: "curio-s59", round: "R8", creative_sha256: after, narrative: { status: "HOLD", two_reader_or_yes: 12, required_failed: ["payoffs"], official_record_sha256: sha(officialPath) }, source_and_claims: { status: "PASS for spoken 110/110", independent_review_sha256: sourceSha }, written_visual: { status: "PASS for 100 shots and 10 big cards", independent_review_sha256: sourceSha, blockers: [] }, pre_media_policy: { status: "HOLD", paid_media_allowed: false } });
process.stdout.write(`${JSON.stringify({ readers, fixed_or_yes: 12, required_failed: ["payoffs"], official_exit: run.status, workdir }, null, 2)}\n`);
