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
  "research.md": "f3ab0acd1e0bbf4124b7897b07604897d38068095a72530a2e2071e4b968f566",
  "brief.md": "c03bd176667ff1ca5180f5f9591869f1e8e58ca7e7454fa8d723913c7a3ed133",
  "claims.md": "e221beb8befe971381ef306aa89433f37021cbb88e3692f6c51409568211083a",
  "video.json": "e780262318e4b6860637a173c07258d7b3019e0d077200aabc35d8b6b1fc0e54",
  "script.md": "c61844a2e079285b8ad98a150e7ac49fa03dca9939dab10a81748fabcf4336d5",
};
const creative = () => Object.fromEntries(Object.keys(expected).map((name) => [name, sha(join(episode, name))]));
const before = creative();
if (Object.entries(expected).some(([name, value]) => before[name] !== value)) throw new Error("R1 creative SHA drift before CLI");
const ballots = { a: sha(join(here, "raw-ballot-a.md")), b: sha(join(here, "raw-ballot-b.md")) };
if (ballots.a !== "9b8e1af4a52a29355ab248537a21963c9882cf32707543bdad0b98335e5c854b" || ballots.b !== "635aa75586d59e743e0c0490f384f60b66d3cdccb90f11fcbbbe4a8f38904280") throw new Error("R1 frozen ballot drift");
const workdir = mkdtempSync(join(tmpdir(), "curio-s59-r1-merge-formal-"));
const args = [join(repo, "tools/video/cli.mjs"), "narrative", "--slug", "curio-s59", "--answers", join(here, "merged-answers.json"), "--workdir", workdir, "--json"];
const run = spawnSync(process.execPath, args, { cwd: repo, encoding: "utf8", env: { ...process.env, NODE_USE_ENV_PROXY: "1", NODE_NO_WARNINGS: "1" }, timeout: 300000 });
if (run.error) throw run.error;
writeFileSync(join(here, "cli.stdout.json"), run.stdout);
writeFileSync(join(here, "cli.stderr.txt"), run.stderr);
writeFileSync(join(here, "cli.exit-code.txt"), `${run.status}\n`);
const officialPath = join(workdir, "curio-s59/review/narrative.json");
copyFileSync(officialPath, join(here, "official-narrative-record.json"));
const after = creative();
const stdout = JSON.parse(run.stdout);
const record = JSON.parse(readFileSync(officialPath, "utf8"));
const receipt = {
  slug: "curio-s59", round: "R1", command: `${process.execPath} ${args.join(" ")}`,
  workdir, official_record_path: officialPath,
  creative_sha256_before: before, creative_sha256_after: after,
  creative_unchanged: Object.entries(expected).every(([name, value]) => after[name] === value),
  ballot_sha256: ballots, merged_answers_sha256: sha(join(here, "merged-answers.json")),
  stdout_sha256: sha(join(here, "cli.stdout.json")), stderr_sha256: sha(join(here, "cli.stderr.txt")),
  official_record_sha256: sha(officialPath), exit_code: run.status,
  cli_passed: stdout.passed, cli_failed: stdout.failed, cli_advisory: stdout.advisory,
  panel_rules_sha256: record.panel_rules_sha256, panel_narration_sha256: record.panel_narration_sha256,
  narrative_hash: record.narrative_hash, official_round: record.round,
};
writeFileSync(join(here, "cli-status.json"), `${JSON.stringify(receipt, null, 2)}\n`);
if (!receipt.creative_unchanged || run.status !== 1 || stdout.passed !== false || !Array.isArray(stdout.failed) || stdout.failed.map((answer) => answer.id).join(",") !== "payoffs,no_recap" || !Array.isArray(stdout.advisory) || stdout.advisory.length !== 0 || record.passed !== false) throw new Error("unexpected formal R1 CLI result; inspect archived output");
process.stdout.write(`${JSON.stringify(receipt, null, 2)}\n`);
