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
  "brief.md": "f2086e64ffd56c5c2d8ea072d7122ffd7d7a2c2290c3413cf54a8ea2a8e35b4f",
  "claims.md": "75f3c81a1cfba0250c8fe2d291765acdeb098dd6f37e8fc34bb17632e62356e9",
  "video.json": "542c5d17330d2344fd588bfe839b636642f37da80c97a9f34d29ace013c75ec5",
  "script.md": "86d6b9883dc24ba55b2c4c66ad390755610999a84dd354e1c02aa8c0f8cbc1f3",
};
const creative = () => Object.fromEntries(Object.keys(expected).map((name) => [name, sha(join(episode, name))]));
const before = creative();
if (Object.entries(expected).some(([name, value]) => before[name] !== value)) throw new Error("R3 creative SHA drift before CLI");
const ballots = { a: sha(join(here, "raw-ballot-a.md")), b: sha(join(here, "raw-ballot-b.md")) };
if (ballots.a !== "5ab3e4a99ca0df9ec139e352a19b147ca1a2d8040aaf14734090450ce9744e36" || ballots.b !== "958183170d8470b0c8d9302c040d5ebec187bb6ae05bb7b78a42a9c11e45b23e") throw new Error("R3 frozen ballot drift");
const workdir = mkdtempSync(join(tmpdir(), "curio-s59-r3-merge-formal-"));
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
  slug: "curio-s59", round: "R3", command: `${process.execPath} ${args.join(" ")}`,
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
if (!receipt.creative_unchanged || run.status !== 1 || stdout.passed !== false || !Array.isArray(stdout.failed) || stdout.failed.map((answer) => answer.id).join(",") !== "no_recap" || !Array.isArray(stdout.advisory) || stdout.advisory.length !== 0 || record.passed !== false) throw new Error("unexpected formal R3 CLI result; inspect archived output");
process.stdout.write(`${JSON.stringify(receipt, null, 2)}\n`);
