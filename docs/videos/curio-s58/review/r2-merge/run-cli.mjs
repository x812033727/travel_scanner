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
  "research.md": "8a1db1dc2a9441a7b16683c70067203ddc7be6c0070560f32c02d91b5e32de34",
  "brief.md": "7b44818f6b681a4ee786c00a32359b4181772aeaa1b5cd897bcd13871b1ad016",
  "claims.md": "73f9ea7122ec728357b7eb3c8487b9657b4bbe0e6d140c4b0514a7deddc2d471",
  "video.json": "d69ce07f441aeabddc231d4d98fe4437ffea4e7c763198d2a61be1161bebe0cb",
  "script.md": "9d590c8c3e6f93628d87d4618276ee967364aa36e0b54c7008c9266b6daae0ac",
};
const creative = () => Object.fromEntries(Object.keys(expected).map((name) => [name, sha(join(episode, name))]));
const before = creative();
if (Object.entries(expected).some(([name, value]) => before[name] !== value)) throw new Error("R2 creative SHA drift before CLI");
const ballots = { a: sha(join(here, "raw-ballot-a.md")), b: sha(join(here, "raw-ballot-b.md")) };
if (ballots.a !== "9ad26823d4360c49212f14d5b2f05c7ba7783269dd03ab6f893e43a209d29bc9" || ballots.b !== "9ed2f8a7d5d2f35def56aedf04da388c9fdf1c02f4555c59d7c710e541ab18a4") throw new Error("R2 frozen ballots drift");
const workdir = mkdtempSync(join(tmpdir(), "curio-s58-r2-merge-formal-"));
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
  round: "R2",
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
if (!receipt.creative_unchanged || run.status !== 1 || stdout.passed !== false || !Array.isArray(stdout.failed) || stdout.failed.map((answer) => answer.id).join(",") !== "no_spoiler,one_line,payoffs,no_recap,no_detour" || !Array.isArray(stdout.advisory) || stdout.advisory.length !== 0 || record.passed !== false) throw new Error("unexpected formal R2 CLI result; inspect archived output");
process.stdout.write(`${JSON.stringify(receipt, null, 2)}\n`);
