import { createHash } from "node:crypto";
import { copyFileSync, mkdtempSync, readFileSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const episode = join(here, "../..");
const repo = join(episode, "../../..");
const sha = (path) => createHash("sha256").update(readFileSync(path)).digest("hex");
const expected = {
  "research.md": "1f6adc58345a10655a0bfdf66c87d5337cbd87c8271f41cb4878204bf4e5d5d0",
  "brief.md": "fbffce22c2eff5052a4050b06b121e3fc8a62b7ab350ecfd6a150f5788214362",
  "claims.md": "67ed990038429d6186487e1f16504ebf3e982d2b8d7c591c75b7c58faf8cceef",
  "video.json": "1be17b85b1b41cb1f5e0f9fe21d18c758ef096447cb4c776c5dcba1ba79dda22",
  "script.md": "ce03aeae00241c3e178897ea35a4469c697abaddbb268061fd0574eed0dc35e0",
};
const creative = () => Object.fromEntries(Object.keys(expected).map((name) => [name, sha(join(episode, name))]));
const before = creative();
if (Object.entries(expected).some(([name, value]) => before[name] !== value)) throw new Error("R5 creative SHA drift before CLI");
const ballots = { a: sha(join(here, "raw-ballot-a.md")), b: sha(join(here, "raw-ballot-b.md")) };
if (ballots.a !== "19746ef5547ffb2de58f2ddb0ed522e5305b7b4fd8e976d43a95a2996361c097" || ballots.b !== "bd368236f51c2f4052c4eacd3598dae9f577dab474abfeca3971904cfc492c41") throw new Error("R5 frozen ballots drift");
const workdir = mkdtempSync(join(tmpdir(), "curio-s58-r5-merge-formal-"));
const args = [join(repo, "tools/video/cli.mjs"), "narrative", "--slug", "curio-s58", "--answers", join(here, "merged-answers.json"), "--workdir", workdir, "--json"];
const run = spawnSync(process.execPath, args, { cwd: repo, encoding: "utf8", env: { ...process.env, NODE_USE_ENV_PROXY: "1", NODE_NO_WARNINGS: "1" }, timeout: 300000 });
if (run.error) throw run.error;
writeFileSync(join(here, "cli.stdout.json"), run.stdout);
writeFileSync(join(here, "cli.stderr.txt"), run.stderr);
writeFileSync(join(here, "cli.exit-code.txt"), `${run.status}\n`);
const officialPath = join(workdir, "curio-s58/review/narrative.json");
copyFileSync(officialPath, join(here, "official-narrative-record.json"));
const after = creative();
const stdout = JSON.parse(run.stdout);
const record = JSON.parse(readFileSync(officialPath, "utf8"));
const receipt = {
  slug: "curio-s58",
  round: "R5",
  command: `${process.execPath} ${args.join(" ")}`,
  workdir,
  official_record_path: officialPath,
  creative_sha256_before: before,
  creative_sha256_after: after,
  creative_unchanged: Object.entries(expected).every(([name, value]) => after[name] === value),
  ballot_sha256: ballots,
  merged_answers_sha256: sha(join(here, "merged-answers.json")),
  stdout_sha256: sha(join(here, "cli.stdout.json")),
  stderr_sha256: sha(join(here, "cli.stderr.txt")),
  official_record_sha256: sha(officialPath),
  exit_code: run.status,
  cli_passed: stdout.passed,
  cli_failed: stdout.failed,
  cli_advisory: stdout.advisory,
  panel_rules_sha256: record.panel_rules_sha256,
  panel_narration_sha256: record.panel_narration_sha256,
  narrative_hash: record.narrative_hash,
  official_round: record.round,
};
writeFileSync(join(here, "cli-status.json"), `${JSON.stringify(receipt, null, 2)}\n`);
if (!receipt.creative_unchanged || run.status !== 0 || stdout.passed !== true || !Array.isArray(stdout.failed) || stdout.failed.length !== 0 || !Array.isArray(stdout.advisory) || stdout.advisory.length !== 0 || record.passed !== true) throw new Error("unexpected formal R5 CLI result; inspect archived output");
process.stdout.write(`${JSON.stringify(receipt, null, 2)}\n`);
