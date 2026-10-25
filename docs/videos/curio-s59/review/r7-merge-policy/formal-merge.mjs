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
  "claims.md": "73711de13ce73791e409118b923eceb9d35425a84a63b6fc8b20ddba816e1c58",
  "video.json": "c78a0329f901d05450440ac7244345e5a375ebbacf361c187cec1036bfcc767e",
  "script.md": "d024ba3a7fed6c94b90320097de6289273278b65c7e1ebaef727b86ec861e57f",
};
function assertFrozen(stage) {
  const actual = Object.fromEntries(Object.keys(frozen).map((name) => [name, sha(join(episode, name))]));
  if (Object.keys(frozen).some((name) => actual[name] !== frozen[name])) throw new Error(`${stage}: creative drift ${JSON.stringify(actual)}`);
  return actual;
}

const sourceReview = join(here, "../r7-source-independent.md");
const sourceSha = "8c431f0b0455d3f83b71489fbb41f0645d4d3d9357d6e3c8c0aa0698cfd52d14";
const inputs = {
  A: {
    answers: join(here, "../r7-blind-a/answers.json"),
    answersSha: "ad5f94534dba4be428b4b609fb132ec0700300ef75f9a1bc2f70bc1e672ad68b",
    review: join(here, "../r7-blind-a.md"),
    reviewSha: "bab1b2ac8058910fa82caef1a7d647aef6bc46a9de5c5a510c7fc0ab3cfc766d",
    official: join(here, "../r7-blind-a/official-narrative-record.json"),
    officialSha: "279b1dadb01c0aa2f81b2fe736091597e61dd9822289a91a991dd0572024e488",
    stdout: join(here, "../r7-blind-a/cli-stdout.json"),
    stdoutSha: "2ee08cbcc0a60e8b7ddc87d9da98698907f1450f254dfb53686413441cefc2b0",
    stderr: join(here, "../r7-blind-a/cli-stderr.txt"),
    stderrSha: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    exit: join(here, "../r7-blind-a/cli-exit-code.txt"),
    exitSha: "4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865",
  },
  B: {
    answers: join(here, "../r7-blind-b/answers.json"),
    answersSha: "b33d080fa1e7d6c110bc57012404c36d63dce055496fd9c45bf0a9dd1051c3f0",
    review: join(here, "../r7-blind-b.md"),
    reviewSha: "b931d1036132b34b3c3c2e7d17aa459856fa9959b68c323950c1fe6b8172e510",
    official: join(here, "../r7-blind-b/official-narrative-record.json"),
    officialSha: "31183160c081994d7864853ffcac400e813b6611501665895b3ddc8d5c564ed0",
    stdout: join(here, "../r7-blind-b/cli-stdout.json"),
    stdoutSha: "8b08d336f3851cb18a040b478d6e8a6687a7d79a615684e762f350307e5f4007",
    stderr: join(here, "../r7-blind-b/cli-stderr.txt"),
    stderrSha: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    exit: join(here, "../r7-blind-b/cli-exit-code.txt"),
    exitSha: "4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865",
  },
};
const before = assertFrozen("before merge");
if (sha(sourceReview) !== sourceSha || !readFileSync(sourceReview, "utf8").includes("書面畫面 PASS")) throw new Error("R7 independent source review drift");
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
if (merged.passed || merged.answers.filter((entry) => entry.yes).length !== 12 || JSON.stringify(merged.failed.map((entry) => entry.id)) !== JSON.stringify(["no_recap"])) throw new Error("unexpected R7 fixed OR result");
save("merge-audit.json", {
  slug: "curio-s59", round: "R7", rule: "fixed OR: a cited yes from either independent reader passes a question", creative_sha256: before,
  panel_rules_sha256: PANEL_RULES_SHA256, panel_narration_sha256: binding[1], readers, merged_answers_sha256: sha(join(here, "merged-answers.json")),
  result: { passed: merged.passed, yes: 12, failed: ["no_recap"], advisory: [], answers: merged.answers.map(({ id, required, yes, evidence, yes_readers }) => ({ id, required, yes, evidence, yes_readers })) },
});

const workdir = mkdtempSync(join(tmpdir(), "s59-r7-formal-merge-"));
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
if (run.status !== 1 || stdout.passed || official.passed || JSON.stringify(stdout.failed.map((entry) => entry.id)) !== JSON.stringify(["no_recap"]) || JSON.stringify(official.failed) !== JSON.stringify(["no_recap"]) || official.panel_rules_sha256 !== binding[0] || official.panel_narration_sha256 !== binding[1]) throw new Error("unexpected R7 official CLI verdict");
save("cli-status.json", { command: [process.execPath, ...args], workdir, exit_code: run.status, stdout_sha256: sha(join(here, "cli-stdout.json")), stderr_sha256: sha(join(here, "cli-stderr.txt")), official_sha256: sha(officialPath), creative_sha256_before: before, creative_sha256_after: after, passed: false, failed: ["no_recap"], narrative_hash: official.narrative_hash, panel_rules_sha256: official.panel_rules_sha256, panel_narration_sha256: official.panel_narration_sha256 });
save("policy-gate.json", { slug: "curio-s59", round: "R7", creative_sha256: after, narrative: { status: "HOLD", two_reader_or_yes: 12, required_failed: ["no_recap"], official_record_sha256: sha(officialPath) }, source_and_claims: { status: "PASS for spoken 110/110", independent_review_sha256: sourceSha }, written_visual: { status: "PASS for 100 shots and 10 big cards", independent_review_sha256: sourceSha, blockers: [] }, pre_media_policy: { status: "HOLD", paid_media_allowed: false } });
process.stdout.write(`${JSON.stringify({ readers, fixed_or_yes: 12, required_failed: ["no_recap"], official_exit: run.status, workdir }, null, 2)}\n`);
