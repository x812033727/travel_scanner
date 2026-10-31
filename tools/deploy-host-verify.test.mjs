// The video-worker check in .agents/skills/deploy/scripts/host-verify.sh: which `auto` exits in the
// worker's log are an owner's switch (AI drama off, exit 4; the monthly draft cap, exit 3) and which
// fail the deploy. The script runs on the host over one SSH session, so its awk program is read out
// of the script here and run on sample logs.
import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { existsSync, readFileSync, mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
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

const START = "2026-10-30T00:45:00.000000000Z";
function classifier() {
  const match = SCRIPT.match(/video_log_classify\(\) \{\r?\n[\s\S]*?\r?\n\}/);
  assert.ok(match, "host verifier must expose its actual log classifier");
  return match[0];
}

function timestamped(log) {
  return log.trimEnd().split("\n").map((line, i) => {
    const time = new Date(Date.parse(START) + i * 1000).toISOString().replace(".000Z", ".000000000Z");
    return `${time} ${line}`;
  }).join("\n") + "\n";
}

/** Execute the production Bash/awk function; no JavaScript reimplementation or skip. */
function inspect(log, { raw = false, first = 1, since = START } = {}) {
  const result = spawnSync(BASH, ["-c", `drama_off=$1; draft_cap=$2\n${classifier()}\nvideo_log_classify "$3" "$4"`, "classify", DRAMA_OFF, DRAFT_CAP, since, String(first)], { input: raw ? log : timestamped(log), encoding: "utf8" });
  assert.equal(result.error, undefined, result.error?.message);
  assert.equal(result.status, 0, result.stderr);
  assert.equal(result.stderr, "");
  const counts = result.stdout.trim().split(/\s+/).map(Number);
  assert.equal(counts.length, 4, result.stdout);
  assert.ok(counts.every(Number.isInteger), result.stdout);
  return counts;
}

function classify(log) { return inspect(log).slice(0, 3); }

test("real Bash and awk are required; missing tools fail instead of skipping", () => {
  assert.equal(hasAwk, true, "install awk or run the tests in the documented POSIX environment");
  assert.equal(hasBash, true, "install Bash or run the tests in the documented POSIX environment");
});

test("the script's octal strings spell the two messages it looks for", () => {
  assert.ok(SCRIPT.includes(`drama_off=$(printf '${octal(DRAMA_OFF)}')`));
  assert.ok(SCRIPT.includes(`draft_cap=$(printf '${octal(DRAFT_CAP)}')`));
});

test("an exit 3 right after the monthly draft cap is counted apart, and the check still fails on anything else", () => {
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

test("the AI-drama-off exit 4 is still counted apart, and a mixed log counts each exit once", () => {
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

test("host verification permits only five reviewed budget rollback pairs", () => {
  for (const [imageHead, databaseHead] of [
    ["0132_video_pilot_budget", "0133_story_followon_budget"],
    ["0137_video_manga_tier", "0138_story_everyday_budget"],
    ["0138_story_everyday_budget", "0139_c20_zippo_pilot_budget"],
    ["0139_c20_zippo_pilot_budget", "0140_c11_ucc_remake_budget"],
    ["0140_c11_ucc_remake_budget", "0141_story_remake_budgets"],
  ]) {
    assert.equal(rollbackPair(imageHead, databaseHead), true, `${imageHead} -> ${databaseHead}`);
    assert.equal(rollbackPair(databaseHead, imageHead), false, `${databaseHead} -> ${imageHead}`);
  }
  for (const [imageHead, databaseHead] of [
    ["0138_story_everyday_budget", "0138_story_everyday_budget"],
    ["0138_story_everyday_budget", "0139_other_budget"],
    ["0137_video_manga_tier", "0139_c20_zippo_pilot_budget"],
    ["0139_c20_zippo_pilot_budget", "0140_other_budget"],
    ["0138_story_everyday_budget", "0140_c11_ucc_remake_budget"],
    ["0140_c11_ucc_remake_budget", "0141_other_budget"],
    ["0139_c20_zippo_pilot_budget", "0141_story_remake_budgets"],
    ["0132_video_pilot_budget", "0134_unreviewed"],
  ]) {
    assert.equal(rollbackPair(imageHead, databaseHead), false, `${imageHead} -> ${databaseHead}`);
  }
  assert.match(SCRIPT, /\[ "\$head_n" -eq 1 \] && \[ "\$guard_rc" -eq 0 \] && \[ "\$expected" = "\$alembic_head" \]/);
  assert.match(SCRIPT, /\[ "\$schema_state" = rollback-compatible \] \\\n+     && reviewed_budget_rollback_pair "\$alembic_head" "\$current"/);
});

// Actual 2026-10-30 Docker timestamps/order/counts retained; only the project slug is sanitized.
const ACTUAL_INTERLEAVED = [
  "2026-10-30T00:45:30.303110720Z video-worker: shorts: the knock failed",
  "2026-10-30T00:45:30.310609975Z video-worker: shorts: API 服務目前無法回應",
  "2026-10-30T00:45:40.732729217Z 本月已產生 60 支草稿，達到上限 60 支",
  "2026-10-30T00:45:41.067104278Z video-worker: auto exited with 3",
  "2026-10-30T00:50:43.394780160Z 本月已產生 60 支草稿，達到上限 60 支",
  "2026-10-30T00:50:43.591233066Z video-worker: auto exited with 3",
  "2026-10-30T00:55:46.863277669Z 本月已產生 60 支草稿，達到上限 60 支",
  "2026-10-30T00:55:47.061467774Z video-worker: auto exited with 3",
  "2026-10-30T01:02:58.111770401Z   planner: claude-opus-5-5, 205678 tokens; month 0/100000000",
  "2026-10-30T01:02:58.856792042Z daily: sample-daily-20261029 planned from the 12 articles of 2026-10-29; Jev picked outline A; outline sent to /admin/videos",
  "2026-10-30T01:03:00.591795670Z sample-daily-20261029: Jev chose outline A (Jev 挑了 A（0.76）：符合立場 0.72、有示範：不適用（解說）、建議 0.02，依設定自動核准)",
  "2026-10-30T01:03:40.430845018Z sample-daily-20261029: writer is still running; its saved receipt will be checked next round",
  "2026-10-30T01:03:42.155006193Z 本月已產生 60 支草稿，達到上限 60 支",
  "2026-10-30T01:03:42.347580323Z video-worker: auto exited with 3",
  "2026-10-30T01:09:05.261034695Z 本月已產生 60 支草稿，達到上限 60 支",
  "2026-10-30T01:09:22.557725482Z [lane 2] sample-daily-20261029: writer is still running; its saved receipt will be checked next round",
  "2026-10-30T01:09:23.740778359Z video-worker: auto exited with 3",
  "2026-10-30T01:14:26.754197475Z 本月已產生 60 支草稿，達到上限 60 支",
  "2026-10-30T01:14:38.381205964Z   writer: claude-opus-5-5, 162797 tokens; month 0/100000000",
  "2026-10-30T01:14:38.739205622Z [lane 2] sample-daily-20261029: script drafted and passes lint",
  "2026-10-30T01:17:55.548286443Z   verifier: claude-opus-5-5, 95911 tokens; month 0/100000000",
  "2026-10-30T01:17:55.725427314Z [lane 2] sample-daily-20261029: fact-check round 1, 4 facts changed; another round follows",
  "2026-10-30T01:20:19.529502964Z   verifier: claude-opus-5-5, 85266 tokens; month 0/100000000",
  "2026-10-30T01:20:19.530561482Z [lane 2] sample-daily-20261029: fact-check round 2, 0 facts changed",
  "2026-10-30T01:21:09.882773236Z   listener: claude-opus-5-5, 56582 tokens; month 0/100000000",
  "2026-10-30T01:21:10.001395054Z [lane 2] sample-daily-20261029: listener edit, 7 changes",
  "2026-10-30T01:23:33.575996710Z   verifier: claude-opus-5-5, 86641 tokens; month 0/100000000",
  "2026-10-30T01:23:33.578449497Z [lane 2] sample-daily-20261029: fact-check round 3, 0 facts changed",
  "2026-10-30T01:23:59.791499905Z   verifier: claude-opus-5-5, 8853 tokens; month 0/100000000",
  "2026-10-30T01:24:24.960130608Z [lane 2] sample-daily-20261029: writer is still running; its saved receipt will be checked next round",
  "2026-10-30T01:24:26.056427597Z video-worker: auto exited with 3",
  "2026-10-30T01:29:28.625583022Z 本月已產生 60 支草稿，達到上限 60 支",
  "2026-10-30T01:29:52.450750528Z   verifier: claude-opus-5-5, 9021 tokens; month 0/100000000",
  "2026-10-30T01:29:52.636346760Z   writer: claude-opus-5-5, 90792 tokens; month 0/100000000",
  "2026-10-30T01:29:52.809752711Z [lane 2] sample-daily-20261029: screenplay rewritten after the storytelling panel's note (round 1); it is checked again",
  "2026-10-30T01:32:07.882172753Z   verifier: claude-opus-5-5, 84282 tokens; month 0/100000000",
  "2026-10-30T01:32:07.884983136Z [lane 2] sample-daily-20261029: fact-check round 4, 0 facts changed",
  "2026-10-30T01:32:41.424205548Z   listener: claude-opus-5-5, 56491 tokens; month 0/100000000",
  "2026-10-30T01:32:41.575414870Z [lane 2] sample-daily-20261029: listener edit, 6 changes",
  "2026-10-30T01:35:51.414756472Z   verifier: claude-opus-5-5, 94929 tokens; month 0/100000000",
  "2026-10-30T01:35:51.584037680Z [lane 2] sample-daily-20261029: fact-check round 5, 1 facts changed",
  "2026-10-30T01:36:16.367440789Z   verifier: claude-opus-5-5, 8797 tokens; month 0/100000000",
  "2026-10-30T01:36:41.528468851Z [lane 2] sample-daily-20261029: writer is still running; its saved receipt will be checked next round",
  "2026-10-30T01:36:42.506770206Z video-worker: auto exited with 3",
  "2026-10-30T01:41:45.124378271Z 本月已產生 60 支草稿，達到上限 60 支",
  "2026-10-30T01:42:09.206501415Z   verifier: claude-opus-5-5, 8847 tokens; month 0/100000000",
  "2026-10-30T01:42:34.437694527Z [lane 2] sample-daily-20261029: writer is still running; its saved receipt will be checked next round",
  "2026-10-30T01:42:35.384268219Z video-worker: auto exited with 3",
  "2026-10-30T01:48:45.142570005Z 本月已產生 60 支草稿，達到上限 60 支",
  "2026-10-30T01:49:07.013479201Z   verifier: claude-opus-5-5, 8816 tokens; month 0/100000000",
  "2026-10-30T01:49:32.264067539Z [lane 2] sample-daily-20261029: writer is still running; its saved receipt will be checked next round",
  "2026-10-30T01:49:33.353409092Z video-worker: auto exited with 3",
  "2026-10-30T01:54:35.741601292Z 本月已產生 60 支草稿，達到上限 60 支",
  "2026-10-30T01:55:03.720494139Z   verifier: claude-opus-5-5, 9526 tokens; month 0/100000000",
  "2026-10-30T01:55:29.014432512Z [lane 2] sample-daily-20261029: writer is still running; its saved receipt will be checked next round",
  "2026-10-30T01:55:30.417765807Z video-worker: auto exited with 3",
  "2026-10-30T02:00:33.895987776Z 本月已產生 60 支草稿，達到上限 60 支",
  "2026-10-30T02:01:03.908968762Z   verifier: claude-opus-5-5, 9637 tokens; month 0/100000000",
  "2026-10-30T02:01:29.203475864Z [lane 2] sample-daily-20261029: writer is still running; its saved receipt will be checked next round",
  "2026-10-30T02:01:31.060667599Z video-worker: auto exited with 3"
].join("\n") + "\n";

const CAP = "本月已產生 60 支草稿，達到上限 60 支";
const EXIT3 = "video-worker: auto exited with 3";
const TOKEN = "  verifier: claude-opus-5-5, 9637 tokens; month 0/100000000";
const WAITING = "[lane 2] sample-daily-20261029: writer is still running; its saved receipt will be checked next round";

test("the exact sanitized actual sequence classifies all eleven single-use cap exits", () => {
  assert.equal(ACTUAL_INTERLEAVED.trimEnd().split("\n").length, 60);
  assert.deepEqual(inspect(ACTUAL_INTERLEAVED, { raw: true }), [0, 0, 11, 0]);
  const recent = inspect(ACTUAL_INTERLEAVED, { raw: true, first: 31 });
  assert.equal(recent[0], 0);
  assert.equal(recent[1], 0);
  assert.ok(recent[2] > 0);
  assert.equal(recent[3], 0);
});

test("a reason is consumed once by every exit and cannot cross an explicit round boundary", () => {
  assert.deepEqual(inspect([CAP, EXIT3, EXIT3].join("\n")), [1, 0, 1, 0]);
  assert.deepEqual(inspect([CAP, "video-worker: auto exited with 2", EXIT3].join("\n")), [2, 0, 0, 0]);
  assert.deepEqual(inspect(["AI 漫劇已停用", "video-worker: auto exited with 4", "video-worker: auto exited with 4"].join("\n")), [1, 1, 0, 0]);
  const crossRound = inspect([CAP, "video-worker: round 2", EXIT3].join("\n"));
  assert.equal(crossRound[0], 1);
  assert.ok(crossRound[3] > 0);
  const duplicate = inspect([CAP, TOKEN, CAP, EXIT3].join("\n"));
  assert.equal(duplicate[0], 1);
  assert.ok(duplicate[3] > 0);
});

test("known progress is exact; an error or unknown lane/stage/backup/shorts line keeps the exit failing", () => {
  for (const unknown of [
    "[lane 2] sample-daily-20261029: writer failed: connection reset",
    "[lane 2] sample-daily-20261029: writer is still running; its saved receipt will be checked next round; ERROR",
    "[lane 2] sample-daily-20261029: an unfamiliar result",
    "[lane 3] sample-daily-20261029: writer is still running; its saved receipt will be checked next round",
    "  verifier: token was refused",
    "  verifier: claude-opus-5-5, x tokens; month 0/100000000",
    "backup: failed: permission denied",
    "backup: unknown response",
    "tidy: could not remove a file",
    "video-worker: shorts: unexpected response",
    "Traceback (most recent call last):",
    "the token was refused",
    "unrecognized message",
  ]) {
    const result = inspect([CAP, TOKEN, unknown, WAITING, EXIT3].join("\n"));
    assert.equal(result[0], 1, unknown);
    assert.equal(result[2], 0, unknown);
    assert.ok(result[3] > 0, unknown);
  }
  const earlierError = inspect(["network unreachable", CAP, EXIT3].join("\n"));
  assert.equal(earlierError[0], 1);
  assert.ok(earlierError[3] > 0);
});

test("malformed exits and policy-lookalike messages never become exemptions", () => {
  for (const exit of ["video-worker: auto exited", "video-worker: auto exited with x", "video-worker: auto exited with 03", "video-worker: auto exited with 3 extra", "video-worker: auto exited with 0", "  video-worker: auto exited with 2", "auto exited with 2", "video-worker: AUTO EXITED with 3", "video-worker: auto\texited with 3"]) {
    assert.equal(inspect([CAP, exit].join("\n"))[0], 1, exit);
    assert.equal(inspect(exit)[0], 1, "without a pending reason: " + exit);
  }
  for (const reason of ["error: " + CAP, CAP + "; unknown error", "someone quoted AI 漫劇已停用", "本月模型 token 已用 9,000,000，達到上限 9,000,000；"]) {
    assert.equal(inspect([reason, EXIT3].join("\n"))[0], 1, reason);
  }
});

test("a brief moving from approval to upload while the draft cap holds is not an error", () => {
  const lane = (message) => `[lane 2] daily-ai-20261029: ${message}`;
  // The worker's log on 2026-10-30, after the deploy of c58d79510.
  const result = inspect([
    "video-worker: shorts: the knock failed",
    "video-worker: shorts: API 服務目前無法回應",
    lane("the final is approved (自動品管 11 項全過，依設定自動核准)"),
    CAP,
    lane("upload package written"),
    lane("publish confirmation sent to /admin/videos"),
    lane("the upload is confirmed (上傳包 4 項齊全，依設定自動核准); the owner uploads it in YouTube Studio and pastes the address on /admin/videos"),
    lane("translator is still running; its saved receipt will be checked next round"),
    lane("caption_reviewer is still running; its saved receipt will be checked next round"),
    "  translator: claude-sonnet-5-5, 20389 tokens; month 0/100000000",
    "  caption_reviewer: claude-sonnet-5-5, 812 tokens; month 0/100000000",
    EXIT3,
  ].join("\n"));
  assert.deepEqual(result, [0, 0, 1, 0]);
  for (const unknown of [
    lane("verifier is still running; its saved receipt will be checked next round"),
    lane("the final is approved (the owner wrote anything here)"),
    lane("upload package written; ERROR"),
    lane("publish confirmation sent to /admin/elsewhere"),
    lane("the upload is confirmed (上傳失敗); the owner uploads it in YouTube Studio and pastes the address on /admin/videos"),
  ]) {
    const refused = inspect([CAP, unknown, EXIT3].join("\n"));
    assert.equal(refused[0], 1, unknown);
    assert.ok(refused[3] > 0, unknown);
  }
});

test("exact benign grammar permits error words in identifiers and paths without permitting error suffixes", () => {
  for (const progress of [
    "[lane 2] api-error-guide: writer is still running; its saved receipt will be checked next round",
    "[lane 2] why-model-failed: script drafted and passes lint",
    "[lane 2] error: fact-check round 2, 0 facts changed",
    "[lane 2] failed: listener edit, 7 changes",
    "  verifier: model-error, 100 tokens; month 0/100000000",
    "backup: error-guide: 13 files, 0 MB, checked in Drive under ai-news/failed/example",
    "backup: failed-guide: the site reads it partial, missing dubs/error, failed.mp4; the tidy keeps its files",
  ]) {
    assert.deepEqual(inspect([CAP, progress, EXIT3].join("\n")), [0, 0, 1, 0], progress);
    const invalidSuffix = inspect([CAP, progress + "; ERROR: upstream outage", EXIT3].join("\n"));
    assert.equal(invalidSuffix[0], 1, progress);
    assert.ok(invalidSuffix[3] > 0, progress);
  }
});

test("free-text errors of any case before a policy reason cannot be hidden by the later reason", () => {
  for (const error of ["ERROR: upstream outage", "eRrOr: upstream outage", "EXCEPTION: connection dropped", "FATAL: aborted", "PANIC: stopped", "REQUEST REFUSED", "NETWORK UNREACHABLE", "WRITER FAILED"]) {
    const result = inspect([error, CAP, EXIT3].join("\n"));
    assert.equal(result[0], 1, error);
    assert.equal(result[2], 0, error);
    assert.ok(result[3] > 0, error);
  }
});

test("context warms the last30 window, without hiding a recent orphan or failing solely on saturation", () => {
  const oldFailure = ["network unreachable", "video-worker: auto exited with 2", ...Array(35).fill("video-worker: shorts: nothing due"), CAP, TOKEN, WAITING, EXIT3];
  assert.deepEqual(inspect(oldFailure.join("\n"), { first: oldFailure.length - 29 }), [0, 0, 1, 0]);
  const capOutsideWindow = [CAP, ...Array(35).fill(TOKEN), EXIT3];
  assert.deepEqual(inspect(capOutsideWindow.join("\n"), { first: capOutsideWindow.length - 29 }), [0, 0, 1, 0]);
  const orphan = [EXIT3, ...Array(29).fill(TOKEN)];
  assert.deepEqual(inspect(orphan.join("\n")), [1, 0, 0, 0]);
  const saturated = [...Array(1962).fill("video-worker: shorts: nothing due"), ...capOutsideWindow];
  assert.equal(saturated.length, 1999);
  saturated.unshift("video-worker: shorts: nothing due");
  assert.deepEqual(inspect(saturated.join("\n"), { first: 1971 }), [0, 0, 1, 0]);
  const lostReason = [...Array(1970).fill(TOKEN), EXIT3, ...Array(29).fill(TOKEN)];
  assert.equal(lostReason.length, 2000);
  assert.deepEqual(inspect(lostReason.join("\n"), { first: 1971 }), [1, 0, 0, 0]);
  const oldUnknownInterleaving = [CAP, "opaque unrecognized response", ...Array(35).fill(TOKEN), EXIT3];
  assert.equal(inspect(oldUnknownInterleaving.join("\n"), { first: oldUnknownInterleaving.length - 29 })[0], 1);
});

test("missing, malformed, out-of-order, or stale timestamps cannot supply policy context", () => {
  for (const log of [
    `${CAP}\n${START} ${EXIT3}\n`,
    `not-a-time ${CAP}\n${START} ${EXIT3}\n`,
    `2026-10-30T99:45:00.000000000Z ${CAP}\n${START} ${EXIT3}\n`,
    `2026-10-29T00:45:00.000000000Z ${CAP}\n${START} ${EXIT3}\n`,
    `2026-10-30T00:45:02.000000000Z ${CAP}\n${START} ${EXIT3}\n`,
  ]) {
    const result = inspect(log, { raw: true });
    assert.equal(result[2], 0);
    assert.ok(result[3] > 0);
  }
  assert.ok(inspect([CAP, EXIT3].join("\n"), { since: "" })[3] > 0);
  assert.deepEqual(inspect(`${START.replace(".000000000Z", "Z")} ${CAP}\n${START} ${EXIT3}\n`, { raw: true }), [0, 0, 1, 0]);
});

test("timestamped blank payloads preserve policy context and raw30 positions", () => {
  for (const blank of ["", "   ", "\t\t"]) {
    assert.deepEqual(inspect([CAP, blank, EXIT3].join("\n")), [0, 0, 1, 0]);
  }
  const reasonBeforeWindow = [CAP, ...Array(29).fill(""), EXIT3];
  assert.equal(reasonBeforeWindow.length, 31);
  assert.deepEqual(inspect(reasonBeforeWindow.join("\n"), { first: 2 }), [0, 0, 1, 0]);
  const oldOrphan = [EXIT3, ...Array(30).fill("")];
  const rawOldOrphan = oldOrphan.map((line, i) => `${new Date(Date.parse(START) + i * 1000).toISOString()} ${line}`).join("\n") + "\n";
  assert.deepEqual(inspect(rawOldOrphan, { raw: true, first: 2 }), [0, 0, 0, 0]);
  const recentOrphan = ["", EXIT3, ...Array(29).fill("")];
  const rawRecentOrphan = recentOrphan.map((line, i) => `${new Date(Date.parse(START) + i * 1000).toISOString()} ${line}`).join("\n") + "\n";
  assert.deepEqual(inspect(rawRecentOrphan, { raw: true, first: 2 }), [1, 0, 0, 0]);
  for (const blankRecord of ["", " \t", "not-a-timestamp ", "2026-10-29T00:45:00.000000000Z \t"]) {
    const raw = `${START} ${CAP}\n${blankRecord}\n2026-10-30T00:45:02.000000000Z ${EXIT3}\n`;
    const result = inspect(raw, { raw: true });
    assert.equal(result[2], 0);
    assert.ok(result[3] > 0);
  }
});

/** Execute only the production video section, with a local shell-function Docker fixture. */
function videoSection(log, { dockerExit = 0, changed = false, secondInspectExit = 0 } = {}) {
  const match = SCRIPT.match(/section video-worker-started\r?\n[\s\S]*?(?=\r?\n# ----------------------------------------------------------------)/);
  assert.ok(match);
  const dir = mkdtempSync(join(tmpdir(), "host-verify-test-"));
  const marker = join(dir, "inspect-count").replaceAll("\\", "/");
  const logFile = join(dir, "docker-log.txt").replaceAll("\\", "/");
  writeFileSync(logFile, log);
  const stub = `
section() { :; }
epoch() { echo 100; }
count() { grep -c -- "$1" || true; }
verdict() { printf 'TEST_VERDICT %s %s %s\\n' "$1" "$2" "$3"; [ "$2" -eq 1 ]; }
head_ct=1
docker() {
  if [ "$1" = inspect ]; then
    if [ -e "$TEST_MARKER" ]; then
      [ "$TEST_SECOND_INSPECT_EXIT" -eq 0 ] || return "$TEST_SECOND_INSPECT_EXIT"
      [ "$TEST_CHANGED" = yes ] && { echo "replacement running 0 $TEST_START"; return 0; }
    fi
    printf x > "$TEST_MARKER"
    echo "container-one running 0 $TEST_START"
  elif [ "$1" = logs ]; then
    [ "$*" = "logs --timestamps --since $TEST_START --tail 2000 container-one" ] || return 98
    cat "$TEST_LOG_FILE"
    return "$TEST_DOCKER_EXIT"
  else
    return 99
  fi
}
`;
  try {
    const result = spawnSync(BASH, ["-c", stub + "\n" + match[0]], { encoding: "utf8", env: { ...process.env, TEST_START: START, TEST_MARKER: marker, TEST_LOG_FILE: logFile, TEST_DOCKER_EXIT: String(dockerExit), TEST_CHANGED: changed ? "yes" : "no", TEST_SECOND_INSPECT_EXIT: String(secondInspectExit) } });
    assert.equal(result.error, undefined, result.error?.message);
    assert.match(result.stdout, /TEST_VERDICT video-worker-started [01] /);
    return result;
  } finally { rmSync(dir, { recursive: true, force: true }); }
}

test("the native video section checks log-read status and current-container identity", () => {
  const log = timestamped([CAP, TOKEN, WAITING, EXIT3].join("\n"));
  const healthy = videoSection(log);
  assert.equal(healthy.status, 0, healthy.stdout + healthy.stderr);
  assert.equal(healthy.stderr, "");
  assert.match(healthy.stdout, /TEST_VERDICT video-worker-started 1 state=running restarts=0 started_after_head=1 knock_failed=0 auto_exited=0 auto_exit4_drama_off=0 auto_exit3_draft_cap=1 not_paired=0 /);
  const failedRead = videoSection(log, { dockerExit: 17 });
  assert.equal(failedRead.status, 1);
  assert.match(failedRead.stdout, /log_read_exit=17/);
  assert.equal(videoSection(log, { changed: true }).status, 1);
  assert.equal(videoSection(log, { secondInspectExit: 9 }).status, 1);
  assert.equal(videoSection(timestamped(EXIT3)).status, 1);
  assert.equal(videoSection(timestamped("  video-worker: auto exited with 2")).status, 1);
  assert.equal(videoSection(timestamped("auto exited with 2")).status, 1);
  assert.equal(videoSection(timestamped(["ERROR: upstream outage", CAP, EXIT3].join("\n"))).status, 1);
  const identifier = videoSection(timestamped([CAP, "[lane 2] api-error-guide: writer is still running; its saved receipt will be checked next round", EXIT3].join("\n")));
  assert.equal(identifier.status, 0, identifier.stdout + identifier.stderr);
  assert.equal(videoSection("").status, 1);
});

test("the native section sorts Docker timestamps, then applies the recent window", () => {
  const shuffled = ACTUAL_INTERLEAVED.trimEnd().split("\n").reverse().join("\n");
  const result = videoSection(shuffled);
  assert.equal(result.status, 0, result.stdout + result.stderr);
  assert.match(result.stdout, /auto_exited=0/);
  const longLived = [...Array(1962).fill("video-worker: shorts: nothing due"), CAP, ...Array(35).fill(TOKEN), EXIT3];
  longLived.unshift("video-worker: shorts: nothing due");
  assert.equal(longLived.length, 2000);
  const saturated = videoSection(timestamped(longLived.join("\n")));
  assert.equal(saturated.status, 0, saturated.stdout + saturated.stderr);
  assert.match(saturated.stdout, /log_lines=2000/);
});

test("the native section ignores only timestamped blank payloads without moving the raw30 boundary", () => {
  for (const blank of ["", "   ", "\t\t"]) {
    const result = videoSection(timestamped([CAP, blank, EXIT3].join("\n")));
    assert.equal(result.status, 0, result.stdout + result.stderr);
  }
  const capBeforeWindow = videoSection(timestamped([CAP, ...Array(29).fill(""), EXIT3].join("\n")));
  assert.equal(capBeforeWindow.status, 0, capBeforeWindow.stdout + capBeforeWindow.stderr);
  for (const blankRecord of ["", " \t", "not-a-timestamp ", "2026-10-29T00:45:00.000000000Z \t"]) {
    const raw = `${START} ${CAP}\n${blankRecord}\n2026-10-30T00:45:02.000000000Z ${EXIT3}\n`;
    assert.equal(videoSection(raw).status, 1, JSON.stringify(blankRecord));
  }
});
