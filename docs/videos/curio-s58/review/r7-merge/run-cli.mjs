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
  "claims.md": "fbb902e05bede6a4a88b108aae725667b41058c979ff7a69dea339a188c19e87",
  "video.json": "ad330abbe8f0919987c01de2c3227e025af8d1d93cc7f2e3557875d5d7b629ec",
  "script.md": "d32bea9d5cc33125cf9b41f1288a8faf78765d96dcd3ed2002abe4ad97f20957",
};
const creative = () => Object.fromEntries(Object.keys(expected).map((name) => [name, sha(join(episode, name))]));
const before = creative();
if (Object.entries(expected).some(([name, value]) => before[name] !== value)) throw new Error("R7 creative SHA drift before CLI");
const ballots = { a: sha(join(here, "raw-ballot-a.md")), b: sha(join(here, "raw-ballot-b.md")) };
if (ballots.a !== "ec1a47dda76f6606c0fce4fc2b49861ed9254a6015587f84b15633f562c015cc" || ballots.b !== "37a697113f8e29558498e4b6e41e5019254668b7f05eb739f697db9d618cb610") throw new Error("R7 frozen ballots drift");
const workdir = mkdtempSync(join(tmpdir(), "curio-s58-r7-merge-formal-"));
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
  round: "R7",
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
if (!receipt.creative_unchanged || run.status !== 1 || stdout.passed !== false || !Array.isArray(stdout.failed) || stdout.failed.map((entry) => typeof entry === "string" ? entry : entry.id).join(",") !== "no_recap" || !Array.isArray(stdout.advisory) || stdout.advisory.length !== 0 || record.passed !== false) throw new Error("unexpected formal R7 CLI result; inspect archived output");
process.stdout.write(`${JSON.stringify(receipt, null, 2)}\n`);
