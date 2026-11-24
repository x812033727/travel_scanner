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
  "research.md": "b26201dd469744fe10c8d259beb93ebcda23609fdb6bc989a6f1d784d9f9779e",
  "brief.md": "5afefc8547bc4fb4a597bcfc99e4e93bcec7631ad237085af78b596aa269a21f",
  "claims.md": "4dc0fdf5c0ee1ce70d78e77e125a83afaf2b3f52fb5d474bb5e3594aa887b503",
  "video.json": "f5ffe0868a570ab86b993cbdbe69014922b7447f078626e2c7294d531c21bbef",
  "script.md": "37dbc104268814e5cc9db7ac72f13a537b2007e9e71c4c219c1252c4a2d7d3f0",
};
const creative = () => Object.fromEntries(Object.keys(expected).map((name) => [name, sha(join(episode, name))]));
const before = creative();
if (Object.entries(expected).some(([name, value]) => before[name] !== value)) throw new Error("R10 creative SHA drift before CLI");
const ballots = { a: sha(join(here, "raw-ballot-a.md")), b: sha(join(here, "raw-ballot-b.md")) };
if (ballots.a !== "f1468b81333b1605a0b37f53f13936ab6f0a12863f4eba95ff88730393d3754f" || ballots.b !== "fe89c2808e611069e6d7ea5adcc039a7f964964234c76b471daffa1b52cd4592") throw new Error("R10 frozen ballots drift");
const workdir = mkdtempSync(join(tmpdir(), "curio-s58-r10-merge-formal-"));
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
  round: "R10",
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
if (!receipt.creative_unchanged || run.status !== 1 || stdout.passed !== false || !Array.isArray(stdout.failed) || stdout.failed.map((entry) => typeof entry === "string" ? entry : entry.id).join(",") !== "no_recap" || !Array.isArray(stdout.advisory) || stdout.advisory.length !== 0 || record.passed !== false) throw new Error("unexpected formal R10 CLI result; inspect archived output");
process.stdout.write(`${JSON.stringify(receipt, null, 2)}\n`);
