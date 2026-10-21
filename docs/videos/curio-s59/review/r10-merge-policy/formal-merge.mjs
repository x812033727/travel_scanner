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
  "claims.md": "5f3066ba0baaaf78404600f38e5e9eda4a93c2eece14bbc296eff274dc618cb7",
  "video.json": "70487214ddbb2cc45f4af58d28ab894de9235ab811c4250b5bf16dbd638f5ffa",
  "script.md": "94acc30b9822e77e26dae56625b179ec17e8af8ce3879d8b35289a3c60824b42",
};
function assertFrozen(stage) {
  const actual = Object.fromEntries(Object.keys(frozen).map((name) => [name, sha(join(episode, name))]));
  if (Object.keys(frozen).some((name) => actual[name] !== frozen[name])) throw new Error(`${stage}: creative drift ${JSON.stringify(actual)}`);
  return actual;
}

const sourceReview = join(here, "../r10-source-independent.md");
const sourceSha = "bede994e1d5ef357367b59b6ce2f68e27e0a2fba383cb9071f35d209535fba3d";
const inputs = {
  A: {
    answers: join(here, "../r10-blind-a/answers.json"),
    answersSha: "6f19e2d8bad4138fb538e8f47ae28cabaf9ce3c2ca39808fc42480e488bba448",
    review: join(here, "../r10-blind-a.md"),
    reviewSha: "063f7e989978208459a577733ab86600926df94189c802e92eb5deafdec39198",
    official: join(here, "../r10-blind-a/official-narrative-record.json"),
    officialSha: "cdcbd160ac2b8c93ca5cc0aa7bc82edd9070634a162d02652363de92e01c382b",
    stdout: join(here, "../r10-blind-a/cli-stdout.json"),
    stdoutSha: "85c4161fc1001efe5d2c897eb191b2c7a1ac76549c6b42639d5b157c47b7ad94",
    stderr: join(here, "../r10-blind-a/cli-stderr.txt"),
    stderrSha: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    exit: join(here, "../r10-blind-a/cli-exit-code.txt"),
    exitSha: "9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa",
  },
  B: {
    answers: join(here, "../r10-blind-b/answers.json"),
    answersSha: "3a8983aa4a77a3d87a6bbcc2d0571821867c6f10a9157b4c1561c795f568bd8d",
    review: join(here, "../r10-blind-b.md"),
    reviewSha: "8fd6631ea716534c342544dae5540d9aa7ad730fb3e92b0d38473acd1a4aa6a3",
    official: join(here, "../r10-blind-b/official-narrative-record.json"),
    officialSha: "aec705c26d4aef6f8317ca86f8cace09ef6902808d3651b164377748733a6ca3",
    stdout: join(here, "../r10-blind-b/cli-stdout.json"),
    stdoutSha: "e69e8960eda051666c398f5565a25b38e40b34661c9eb81adbc6b6f22fadb0f2",
    stderr: join(here, "../r10-blind-b/cli-stderr.txt"),
    stderrSha: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    exit: join(here, "../r10-blind-b/cli-exit-code.txt"),
    exitSha: "9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa",
  },
};
const before = assertFrozen("before merge");
if (sha(sourceReview) !== sourceSha || !readFileSync(sourceReview, "utf8").includes("**本輪來源、逐句引註與書面畫面 PASS。**")) throw new Error("R10 independent source review drift");
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
if (!merged.passed || merged.answers.filter((entry) => entry.yes).length !== 13 || merged.failed.length || merged.advisory.length) throw new Error("unexpected R10 fixed OR result");
save("merge-audit.json", {
  slug: "curio-s59", round: "R10", rule: "fixed OR: a cited yes from either independent reader passes a question", creative_sha256: before,
  panel_rules_sha256: PANEL_RULES_SHA256, panel_narration_sha256: binding[1], readers, merged_answers_sha256: sha(join(here, "merged-answers.json")),
  result: { passed: merged.passed, yes: 13, failed: [], advisory: [], answers: merged.answers.map(({ id, required, yes, evidence, yes_readers }) => ({ id, required, yes, evidence, yes_readers })) },
});

const workdir = mkdtempSync(join(tmpdir(), "s59-r10-formal-merge-"));
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
if (run.status !== 0 || !stdout.passed || !official.passed || stdout.failed.length || official.failed.length || official.panel_rules_sha256 !== binding[0] || official.panel_narration_sha256 !== binding[1]) throw new Error("unexpected R10 official CLI verdict");
save("cli-status.json", { command: [process.execPath, ...args], workdir, exit_code: run.status, stdout_sha256: sha(join(here, "cli-stdout.json")), stderr_sha256: sha(join(here, "cli-stderr.txt")), official_sha256: sha(officialPath), creative_sha256_before: before, creative_sha256_after: after, passed: true, failed: [], narrative_hash: official.narrative_hash, panel_rules_sha256: official.panel_rules_sha256, panel_narration_sha256: official.panel_narration_sha256 });
save("policy-gate.json", { slug: "curio-s59", round: "R10", creative_sha256: after, narrative: { status: "PASS", two_reader_or_yes: 13, required_failed: [], official_record_sha256: sha(officialPath) }, source_and_claims: { status: "PASS for 110 spoken rows and 124 direct citations", independent_review_sha256: sourceSha, blockers: [] }, written_visual: { status: "PASS for 100 shots and 10 big cards", independent_review_sha256: sourceSha, blockers: [] }, pre_media_policy: { status: "READY_FOR_OWNER_GATES", paid_media_allowed: false, pending: ["outline/script approval", "bounded TTS estimate", "audio review", "generated visual review"] } });
process.stdout.write(`${JSON.stringify({ readers, fixed_or_yes: 13, required_failed: [], official_exit: run.status, workdir }, null, 2)}\n`);
