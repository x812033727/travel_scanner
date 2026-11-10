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
  "research.md": "d0077504f3dbe828363158a25c7e7dade955089f49dbb03a734893739e12467e",
  "brief.md": "9d68d7b4dad27f56b6dbc53f7890bc0db84590de3e445302f8f4836c286ac1e3",
  "claims.md": "96a84699644630305f3966de3f9c2d07a3eed501456a6e0a14587eaa99c59981",
  "video.json": "5a6293a9c93352f848b697625c97b21a8783b0fc49f14ce236bfc1513e154cf1",
  "script.md": "7a474081830f7bfe230a6a02a166dab3ec03b834f2e1c86df8727d70cab620c9",
};
function assertFrozen(stage) {
  const actual = Object.fromEntries(Object.keys(frozen).map((name) => [name, sha(join(episode, name))]));
  if (Object.keys(frozen).some((name) => actual[name] !== frozen[name])) throw new Error(`${stage}: creative drift ${JSON.stringify(actual)}`);
  return actual;
}

const sourceReview = join(here, "../r6-source-independent.md");
const sourceSha = "8ab8b4023dc1ef208cb67a534a58932b42cd2e9292f41c47bf3f0553bc519d3a";
const inputs = {
  A: {
    answers: "/tmp/curio-s59-r6-blind-a.jG34VE/answers.json",
    answersSha: "cd35f1ff14d9e0c87e969ddae975ddfffe6fb4cb397cfe3904182cb4fe076e2f",
    review: join(here, "../r6-blind-a.md"),
    reviewSha: "7964ce162a35a5f1653836fd4e6589e6a294d9cc1105324a6af150e106ed68d0",
    official: "/tmp/curio-s59-r6-blind-a.jG34VE/curio-s59/review/narrative.json",
    officialSha: "b71c27cef582cbcbdc29ff7fc40cdfbf9ee5025b64d1daf402a7db7d69c39dcf",
  },
  B: {
    answers: "/tmp/curio-s59-r6-blind-b.oNvjYX/answers.json",
    answersSha: "17361b97c7f831194e6ea2c4503aad7e8f2a7fe68f58acafe7c771ba93d9132f",
    review: join(here, "../r6-blind-b.md"),
    reviewSha: "9bab8eb7add4132a3f0a5dfb6eb34609b7be8ba7b6733cb11372e2001981cc90",
    official: "/tmp/curio-s59-r6-blind-b.oNvjYX/curio-s59/review/narrative.json",
    officialSha: "13c43d7bbbde19573a4123a8f454597f40661874a21883b12958d68e6e7f55ba",
  },
};

const before = assertFrozen("before merge");
if (sha(sourceReview) !== sourceSha || !readFileSync(sourceReview, "utf8").includes("書面畫面 HOLD")) throw new Error("R6 independent source review drift");
const lines = new Map(json(join(episode, "video.json")).scenes.flatMap((scene) => (scene.lines ?? []).map((line) => [line.id, line.text])));
const verdicts = [];
const readers = [];
let binding = null;
for (const label of ["A", "B"]) {
  const input = inputs[label];
  for (const [name, path, expected] of [["answers", input.answers, input.answersSha], ["review", input.review, input.reviewSha], ["official", input.official, input.officialSha]]) {
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
  if (currentBinding[0] !== PANEL_RULES_SHA256 || receipt.round !== 1 || receipt.passed || receipt.advisory.length) throw new Error(`reader ${label} official receipt invalid`);
  if (binding && currentBinding.some((value, i) => value !== binding[i])) throw new Error("reader receipts bind different input");
  binding = currentBinding;
  if (JSON.stringify(receipt.failed) !== JSON.stringify(verdict.failed.map((entry) => entry.id))) throw new Error(`reader ${label} official votes differ`);
  if (receipt.answers.some((entry, i) => entry.yes !== answer.answers[i].yes || entry.evidence !== answer.answers[i].evidence)) throw new Error(`reader ${label} receipt altered vote or citation`);
  copyFileSync(input.answers, join(here, `raw-ballot-${label.toLowerCase()}.json`));
  copyFileSync(input.review, join(here, `raw-review-${label.toLowerCase()}.md`));
  copyFileSync(input.official, join(here, `reader-${label.toLowerCase()}-official.json`));
  readers.push({ label, answers_sha256: input.answersSha, review_sha256: input.reviewSha, official_sha256: input.officialSha, yes: verdict.answers.filter((entry) => entry.yes).length, failed: verdict.failed.map((entry) => entry.id) });
  verdicts.push(verdict);
}

const merged = mergePanelVerdicts(verdicts);
const mergedAnswers = { answers: merged.answers.map(({ id, yes, evidence }) => ({ id, yes, evidence })) };
save("merged-answers.json", mergedAnswers);
if (merged.passed || merged.answers.filter((entry) => entry.yes).length !== 12 || JSON.stringify(merged.failed.map((entry) => entry.id)) !== JSON.stringify(["no_recap"])) throw new Error("unexpected R6 fixed OR result");
save("merge-audit.json", {
  slug: "curio-s59", round: "R6", rule: "fixed OR: a cited yes from either independent reader passes a question", creative_sha256: before,
  panel_rules_sha256: PANEL_RULES_SHA256, panel_narration_sha256: binding[1], readers, merged_answers_sha256: sha(join(here, "merged-answers.json")),
  result: { passed: merged.passed, yes: 12, failed: ["no_recap"], advisory: [], answers: merged.answers.map(({ id, required, yes, evidence, yes_readers }) => ({ id, required, yes, evidence, yes_readers })) },
});

const workdir = mkdtempSync(join(tmpdir(), "s59-r6-formal-merge-"));
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
if (run.status !== 1 || stdout.passed || official.passed || JSON.stringify(stdout.failed.map((entry) => entry.id)) !== JSON.stringify(["no_recap"]) || JSON.stringify(official.failed) !== JSON.stringify(["no_recap"]) || official.panel_rules_sha256 !== binding[0] || official.panel_narration_sha256 !== binding[1]) throw new Error("unexpected R6 official CLI verdict");
save("cli-status.json", { command: [process.execPath, ...args], workdir, exit_code: run.status, stdout_sha256: sha(join(here, "cli-stdout.json")), stderr_sha256: sha(join(here, "cli-stderr.txt")), official_sha256: sha(officialPath), creative_sha256_before: before, creative_sha256_after: after, passed: false, failed: ["no_recap"], narrative_hash: official.narrative_hash, panel_rules_sha256: official.panel_rules_sha256, panel_narration_sha256: official.panel_narration_sha256 });
save("policy-gate.json", { slug: "curio-s59", round: "R6", creative_sha256: after, narrative: { status: "HOLD", two_reader_or_yes: 12, required_failed: ["no_recap"], official_record_sha256: sha(officialPath) }, source_and_claims: { status: "PASS for spoken 110/110", independent_review_sha256: sourceSha }, written_visual: { status: "HOLD", independent_review_sha256: sourceSha, blockers: ["s59017 paper disc groove", "s59013 ambiguous paper-disc track", "research P06 implies direct needle/diaphragm contact"] }, pre_media_policy: { status: "HOLD", paid_media_allowed: false } });
process.stdout.write(`${JSON.stringify({ readers, fixed_or_yes: 12, required_failed: ["no_recap"], official_exit: run.status, workdir }, null, 2)}\n`);
