// The video-worker check in .agents/skills/deploy/scripts/host-verify.sh: which `auto` exits in the
// worker's log are an owner's switch (AI drama off, exit 4; the monthly draft cap, exit 3) and which
// fail the deploy. The script runs on the host over one SSH session, so its awk program is read out
// of the script here and run on sample logs.
import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { existsSync, readFileSync } from "node:fs";
import test from "node:test";

const SCRIPT = readFileSync(new URL("../.agents/skills/deploy/scripts/host-verify.sh", import.meta.url), "utf8");
const DRAMA_OFF = "漫劇已停用";
const DRAFT_CAP = "支草稿，達到上限";
const GIT_BASH = "C:/Program Files/Git/bin/bash.exe";
const BASH = process.env.BASH || (process.platform === "win32" && existsSync(GIT_BASH) ? GIT_BASH : "bash");
// gawk 5.4 refuses an empty "BEGIN{}", which skipped these tests wherever it is the awk.
const hasAwk = spawnSync("awk", ["BEGIN{exit 0}"]).status === 0;
const hasBash = spawnSync(BASH, ["-c", "exit 0"]).status === 0;

function rollbackPair(imageHead, databaseHead) {
  const match = SCRIPT.match(/reviewed_budget_rollback_pair\(\) \{\r?\n[\s\S]*?\r?\n\}/);
  assert.ok(match, "host verifier must declare the reviewed rollback pair predicate");
  const result = spawnSync(BASH, ["-c", `${match[0]}\nreviewed_budget_rollback_pair "$1" "$2"`, "pair", imageHead, databaseHead], { encoding: "utf8" });
  assert.equal(result.error, undefined, result.error?.message);
  return result.status === 0;
}

function octal(text) {
  return [...Buffer.from(text, "utf8")].map((byte) => `\\${byte.toString(8)}`).join("");
}

function program() {
  const match = SCRIPT.match(/awk -v off="\$drama_off" -v cap="\$draft_cap" '\n([\s\S]*?)'\)"/);
  assert.ok(match, "host-verify.sh still classifies the worker's exits with one awk program");
  return match[1];
}

/** [counted exits, exit 4 at AI drama off, exit 3 at the draft cap] for a log. */
function classify(log) {
  const result = spawnSync("awk", ["-v", `off=${DRAMA_OFF}`, "-v", `cap=${DRAFT_CAP}`, program()], { input: log, encoding: "utf8" });
  assert.equal(result.status, 0, result.stderr);
  return result.stdout.trim().split(/\s+/).map(Number);
}

test("the script's octal strings spell the two messages it looks for", () => {
  assert.ok(SCRIPT.includes(`drama_off=$(printf '${octal(DRAMA_OFF)}')`));
  assert.ok(SCRIPT.includes(`draft_cap=$(printf '${octal(DRAFT_CAP)}')`));
});

test("an exit 3 right after the monthly draft cap is counted apart, and the check still fails on anything else", { skip: !hasAwk && "no awk on this machine" }, () => {
  const capped = "video-worker: round 12\n本月已產生 40 支草稿，達到上限 40 支\nvideo-worker: auto exited with 3\n";
  assert.deepEqual(classify(capped), [0, 0, 1]);
  // A Shorts line between the message and the exit does not break the pair.
  assert.deepEqual(classify("本月已產生 40 支草稿，達到上限 40 支\nvideo-worker: shorts: nothing due\nvideo-worker: auto exited with 3\n"), [0, 0, 1]);
  // Nor do the Drive backup's lines, which run after a round that ended in an error (#1660, 2026-10-22's log).
  const backedUp = [
    "本月已產生 60 支草稿，達到上限 60 支",
    "backup: google-vids-omni-free-quota: 13 files, 0 MB, checked in Drive under ai-news/google-vids-omni-free-quota",
    "backup: google-vids-omni-free-quota: the site reads it partial, missing dubs/ja, final.mp4; the tidy keeps its files",
    "video-worker: auto exited with 3",
  ].join("\n");
  assert.deepEqual(classify(backedUp), [0, 0, 1]);
  // A backup line does not make another round's exit 3 look capped.
  assert.deepEqual(classify("the token was refused\nbackup: not copying: x; the tidy keeps every video on YouTube\nvideo-worker: auto exited with 3\n"), [1, 0, 0]);
  // An exit 3 after anything else is a failure, and so is another exit after the cap message.
  assert.deepEqual(classify("the token was refused\nvideo-worker: auto exited with 3\n"), [1, 0, 0]);
  assert.deepEqual(classify("本月已產生 40 支草稿，達到上限 40 支\nvideo-worker: auto exited with 4\n"), [1, 0, 0]);
  assert.deepEqual(classify("本月已產生 40 支草稿，達到上限 40 支\nvideo-worker: auto exited with 1\n"), [1, 0, 0]);
  // The month's token cap is a different message and stays counted.
  assert.deepEqual(classify("本月模型 token 已用 9,000,000，達到上限 9,000,000；\nvideo-worker: auto exited with 3\n"), [1, 0, 0]);
});

test("the AI-drama-off exit 4 is still counted apart, and a mixed log counts each exit once", { skip: !hasAwk && "no awk on this machine" }, () => {
  assert.deepEqual(classify("AI 漫劇已停用\nvideo-worker: auto exited with 4\n"), [0, 1, 0]);
  const mixed = [
    "AI 漫劇已停用",
    "video-worker: auto exited with 4",
    "本月已產生 40 支草稿，達到上限 40 支",
    "video-worker: auto exited with 3",
    "network unreachable",
    "video-worker: auto exited with 2",
  ].join("\n");
  assert.deepEqual(classify(mixed), [1, 1, 1]);
});

test("the verdict still requires no counted exit, and names the capped exits", () => {
  assert.match(SCRIPT, /\[ "\$exited" -eq 0 \]/);
  assert.match(SCRIPT, /auto_exit3_draft_cap=\$cap_exits/);
});

test("host verification permits only three reviewed budget rollback pairs", { skip: !hasBash && "no bash on this machine" }, () => {
  for (const [imageHead, databaseHead] of [
    ["0132_video_pilot_budget", "0133_story_followon_budget"],
    ["0137_video_manga_tier", "0138_story_everyday_budget"],
    ["0138_story_everyday_budget", "0139_c20_zippo_pilot_budget"],
  ]) {
    assert.equal(rollbackPair(imageHead, databaseHead), true, `${imageHead} -> ${databaseHead}`);
    assert.equal(rollbackPair(databaseHead, imageHead), false, `${databaseHead} -> ${imageHead}`);
  }
  for (const [imageHead, databaseHead] of [
    ["0138_story_everyday_budget", "0138_story_everyday_budget"],
    ["0138_story_everyday_budget", "0139_other_budget"],
    ["0137_video_manga_tier", "0139_c20_zippo_pilot_budget"],
    ["0132_video_pilot_budget", "0134_unreviewed"],
  ]) {
    assert.equal(rollbackPair(imageHead, databaseHead), false, `${imageHead} -> ${databaseHead}`);
  }
  assert.match(SCRIPT, /\[ "\$head_n" -eq 1 \] && \[ "\$guard_rc" -eq 0 \] && \[ "\$expected" = "\$alembic_head" \]/);
  assert.match(SCRIPT, /\[ "\$schema_state" = rollback-compatible \] \\\n+     && reviewed_budget_rollback_pair "\$alembic_head" "\$current"/);
});
