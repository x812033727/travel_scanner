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
  "research.md": "ad5baec33ae786da9d103eecadca9f16c9f23f00d4041bde158e1e2697958efb",
  "brief.md": "90024cd567cb540e92fe9d58815cb36a0d05ade7a6739ec6851a54d6d5d10b80",
  "claims.md": "b84f891c58a937cd9fd2cfffc2aab0f14c0c652fee838f6a79bfca2b40e99bc5",
  "video.json": "26844c8610bd399077be2f349b3c548168c5021d6c143a88610ca8138d16a435",
  "script.md": "c74ea14ea53d7442b59d2232fd867b1ce7794aae4b2878337b693fe25a3e78a3",
};
const creative = () => Object.fromEntries(Object.keys(expected).map((name) => [name, sha(join(episode, name))]));
const before = creative();
if (Object.entries(expected).some(([name, value]) => before[name] !== value)) throw new Error("R2 creative SHA drift before CLI");
const ballots = { a: sha(join(here, "raw-ballot-a.md")), b: sha(join(here, "raw-ballot-b.md")) };
if (ballots.a !== "5dcb6fc982e4658d52f0105dd2c1230c6f6ea0c291d0075be843b2521c1e5e02" || ballots.b !== "e9d86cef82821b11e8a1830614efabc7428eedf562190cc627800b2dd9212bd1") throw new Error("R2 frozen ballot drift");
const workdir = mkdtempSync(join(tmpdir(), "curio-s59-r2-merge-formal-"));
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
  slug: "curio-s59", round: "R2", command: `${process.execPath} ${args.join(" ")}`,
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
if (!receipt.creative_unchanged || run.status !== 1 || stdout.passed !== false || !Array.isArray(stdout.failed) || stdout.failed.map((answer) => answer.id).join(",") !== "no_recap" || !Array.isArray(stdout.advisory) || stdout.advisory.length !== 0 || record.passed !== false) throw new Error("unexpected formal R2 CLI result; inspect archived output");
process.stdout.write(`${JSON.stringify(receipt, null, 2)}\n`);
