// The video-worker check in .agents/skills/deploy/scripts/host-verify.sh: which `auto` exits in the
// worker's log are an owner's switch (AI drama off, exit 4; the monthly draft cap, exit 3) and which
// fail the deploy. The script runs on the host over one SSH session, so its awk program is read out
// of the script here and run on sample logs.
import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { readFileSync } from "node:fs";
import test from "node:test";

const SCRIPT = readFileSync(new URL("../.agents/skills/deploy/scripts/host-verify.sh", import.meta.url), "utf8");
const DRAMA_OFF = "漫劇已停用";
const DRAFT_CAP = "支草稿，達到上限";
const hasAwk = spawnSync("awk", ["BEGIN{}"]).status === 0;

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
