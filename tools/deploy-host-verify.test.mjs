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
const hasAwk = spawnSync("awk", ["BEGIN { exit 0 }"]).status === 0;
const hasSh = spawnSync("sh", ["-c", ":"]).status === 0;

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

function schemaVerdict({ head, current, expected = head, state = "rollback-compatible", guard = 0, heads = 1 }) {
  const section = SCRIPT.split("section alembic-head\n", 2)[1];
  assert.ok(section, "host verifier still has an alembic-head section");
  const condition = section.split("\nok=0\n", 2)[1]?.split("\nverdict alembic-head", 1)[0];
  assert.ok(condition, "host verifier still has one schema verdict condition");
  const run = spawnSync("sh", ["-c", `ok=0\n${condition}\nprintf '%s' "$ok"`], {
    env: {
      ...process.env,
      head_n: String(heads), guard_rc: String(guard), expected,
      alembic_head: head, schema_state: state, current,
    },
    encoding: "utf8",
  });
  assert.equal(run.status, 0, run.stderr);
  return run.stdout;
}

test("schema verdict accepts only the two reviewed rollback pairs with a passing guard", { skip: !hasSh && "no sh on this machine" }, () => {
  const old = "0132_video_pilot_budget";
  const middle = "0133_story_followon_budget";
  const next = "0134_a01_admission_fence";
  assert.equal(schemaVerdict({ head: old, current: middle }), "1");
  assert.equal(schemaVerdict({ head: middle, current: next }), "1");
  assert.equal(schemaVerdict({ head: middle, current: middle, state: "exact" }), "1");
  assert.equal(schemaVerdict({ head: old, current: next }), "0");
  assert.equal(schemaVerdict({ head: middle, current: "0134_other" }), "0");
  assert.equal(schemaVerdict({ head: middle, current: next, guard: 1 }), "0");
  assert.equal(schemaVerdict({ head: middle, current: next, heads: 2 }), "0");
  assert.equal(schemaVerdict({ head: middle, current: next, expected: old }), "0");
});
