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
  "research.md": "27bebfb771aa8a901cf69528fb23401d351dcc35bdf584ab5e70c2163bfa0ea7",
  "brief.md": "49a1bd7cf68e2db074cc128bd08f60739da9ce85f63aa1ba4f7abab9f044e0d4",
  "claims.md": "73dcedbcbf30d5abd2db92fd34b789718e61938e8b4a86fe528d109851d332ec",
  "video.json": "7283ea2a7e444e2e58e83bb52a40da9548a1dddc1c2d74740971100f33936c48",
  "script.md": "6fd7c0585ebb1a47f518d70d769a1094deb54dc90404362df0ce0ed821ef1816",
};
const creative = () => Object.fromEntries(Object.keys(expected).map((name) => [name, sha(join(episode, name))]));
const before = creative();
if (Object.entries(expected).some(([name, value]) => before[name] !== value)) throw new Error("R3 creative SHA drift before CLI");
const ballots = { a: sha(join(here, "raw-ballot-a.md")), b: sha(join(here, "raw-ballot-b.md")) };
if (ballots.a !== "568b28a0e0501f02420d5d83c1a00c93c6019a66858ab10e4629dfd7fba3ee9a" || ballots.b !== "91c1f5019202cb827291bf1522764a455c8a57defae3011de64ee5041693efbc") throw new Error("R3 frozen ballots drift");
const workdir = mkdtempSync(join(tmpdir(), "curio-s58-r3-merge-formal-"));
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
  round: "R3",
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
if (!receipt.creative_unchanged || run.status !== 1 || stdout.passed !== false || !Array.isArray(stdout.failed) || stdout.failed.map((answer) => answer.id).join(",") !== "no_recap,no_detour" || !Array.isArray(stdout.advisory) || stdout.advisory.length !== 0 || record.passed !== false) throw new Error("unexpected formal R3 CLI result; inspect archived output");
process.stdout.write(`${JSON.stringify(receipt, null, 2)}\n`);
