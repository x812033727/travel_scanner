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
  "claims.md": "54e6c2f1d8fb533161ed48980ef1043faf6716c70999576507de9d6a735da747",
  "video.json": "a0f986b5f1f578f6170b62ad24e17775b87ef4d3eb463104de9975a84928e4e6",
  "script.md": "6c28555d04104c676f76414479f038f426893f940a183e2518e3e9abac22cc09",
};
function assertFrozen(stage) {
  const actual = Object.fromEntries(Object.keys(frozen).map((name) => [name, sha(join(episode, name))]));
  if (Object.keys(frozen).some((name) => actual[name] !== frozen[name])) throw new Error(`${stage}: creative drift ${JSON.stringify(actual)}`);
  return actual;
}

const sourceReview = join(here, "../r9-source-independent.md");
const sourceSha = "20a0f368a288743f82d49ac6ade58771dd44e2d34207e591ab417e86b5a0ffee";
const inputs = {
  A: {
    answers: join(here, "../r9-blind-a/answers.json"),
    answersSha: "e5e5165beba5c59d59216df86229f7ebb2f732432ba9aa5f6cb8d7becad9820f",
    review: join(here, "../r9-blind-a.md"),
    reviewSha: "80b2bd1bad903c83e0a8d2094c1f5b80ec6374e4c5329709d09f80df3b8df1da",
    official: join(here, "../r9-blind-a/official-narrative-record.json"),
    officialSha: "0db961c6d83f02438f86b83c212bf345f2633b763f5742538907749b204dff2f",
    stdout: join(here, "../r9-blind-a/cli-stdout.json"),
    stdoutSha: "df815bfaae780a68359e283516fbc369d6802ae265f98fb9cd7b1c87a64fefda",
    stderr: join(here, "../r9-blind-a/cli-stderr.txt"),
    stderrSha: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    exit: join(here, "../r9-blind-a/cli-exit-code.txt"),
    exitSha: "4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865",
  },
  B: {
    answers: join(here, "../r9-blind-b/answers.json"),
    answersSha: "28b92dedaa860ae02490298fa9a345afd6091d004d2649c8b899e378cfba3b92",
    review: join(here, "../r9-blind-b.md"),
    reviewSha: "f7014f462ef7de0ec874d1ffe8dbfbac6b1baa6c1067b48221c8f4dcf0f4d011",
    official: join(here, "../r9-blind-b/official-narrative-record.json"),
    officialSha: "b905636301b9e8ba6c8738bf1938e96436c26cc36c1dd5776872f34186f468fe",
    stdout: join(here, "../r9-blind-b/cli-stdout.json"),
    stdoutSha: "ceaa5aa31fcb854d0a5714f1dab8706f5fc5e354f5902f45595c55bca5d61a46",
    stderr: join(here, "../r9-blind-b/cli-stderr.txt"),
    stderrSha: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    exit: join(here, "../r9-blind-b/cli-exit-code.txt"),
    exitSha: "9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa",
  },
};
const before = assertFrozen("before merge");
if (sha(sourceReview) !== sourceSha || !readFileSync(sourceReview, "utf8").includes("HOLD")) throw new Error("R9 independent source review drift");
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
if (!merged.passed || merged.answers.filter((entry) => entry.yes).length !== 13 || merged.failed.length || merged.advisory.length) throw new Error("unexpected R9 fixed OR result");
save("merge-audit.json", {
  slug: "curio-s59", round: "R9", rule: "fixed OR: a cited yes from either independent reader passes a question", creative_sha256: before,
  panel_rules_sha256: PANEL_RULES_SHA256, panel_narration_sha256: binding[1], readers, merged_answers_sha256: sha(join(here, "merged-answers.json")),
  result: { passed: merged.passed, yes: 13, failed: [], advisory: [], answers: merged.answers.map(({ id, required, yes, evidence, yes_readers }) => ({ id, required, yes, evidence, yes_readers })) },
});

const workdir = mkdtempSync(join(tmpdir(), "s59-r9-formal-merge-"));
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
if (run.status !== 0 || !stdout.passed || !official.passed || stdout.failed.length || official.failed.length || official.panel_rules_sha256 !== binding[0] || official.panel_narration_sha256 !== binding[1]) throw new Error("unexpected R9 official CLI verdict");
save("cli-status.json", { command: [process.execPath, ...args], workdir, exit_code: run.status, stdout_sha256: sha(join(here, "cli-stdout.json")), stderr_sha256: sha(join(here, "cli-stderr.txt")), official_sha256: sha(officialPath), creative_sha256_before: before, creative_sha256_after: after, passed: true, failed: [], narrative_hash: official.narrative_hash, panel_rules_sha256: official.panel_rules_sha256, panel_narration_sha256: official.panel_narration_sha256 });
save("policy-gate.json", { slug: "curio-s59", round: "R9", creative_sha256: after, narrative: { status: "PASS", two_reader_or_yes: 13, required_failed: [], official_record_sha256: sha(officialPath) }, source_and_claims: { status: "HOLD at s59059 attribution", independent_review_sha256: sourceSha, blockers: ["s59058 Edison attribution may carry into s59059 du Moncel observations"] }, written_visual: { status: "PASS for 100 shots and 10 big cards", independent_review_sha256: sourceSha, blockers: [] }, pre_media_policy: { status: "HOLD", paid_media_allowed: false } });
process.stdout.write(`${JSON.stringify({ readers, fixed_or_yes: 13, required_failed: [], official_exit: run.status, workdir }, null, 2)}\n`);
