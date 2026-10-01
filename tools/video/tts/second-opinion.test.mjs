import assert from "node:assert/strict";
import test from "node:test";

import {
  SECOND_OPINION_TIMEOUT_ENV,
  secondOpinionTimeout,
  secondTranscripts,
  TIMEOUT_BASE_MS,
  TIMEOUT_PER_CLIP_MS,
} from "./second-opinion.mjs";

const clips = (count) => Array.from({ length: count }, (_, i) => `/audio/line-${i + 1}.wav`);

test("the default time limit grows with the number of clips", () => {
  assert.equal(secondOpinionTimeout(1), TIMEOUT_BASE_MS + TIMEOUT_PER_CLIP_MS);
  assert.equal(secondOpinionTimeout(30), TIMEOUT_BASE_MS + 30 * TIMEOUT_PER_CLIP_MS);
  // 30 clips at about a minute each, the case the old fixed 30 minutes could not hold.
  assert.ok(secondOpinionTimeout(30) > 30 * 60 * 1000);
});

test("the environment sets the whole time limit, and a bad value says what is wrong", () => {
  assert.equal(secondOpinionTimeout(30, { [SECOND_OPINION_TIMEOUT_ENV]: "5400000" }), 5_400_000);
  assert.equal(secondOpinionTimeout(2, { [SECOND_OPINION_TIMEOUT_ENV]: "  " }), TIMEOUT_BASE_MS + 2 * TIMEOUT_PER_CLIP_MS);
  for (const bad of ["0", "-1", "90m", "1.5"]) {
    assert.throws(() => secondOpinionTimeout(2, { [SECOND_OPINION_TIMEOUT_ENV]: bad }), new RegExp(`${SECOND_OPINION_TIMEOUT_ENV} must be a positive whole number`));
  }
});

test("the runner gets the limit for this batch and the transcripts come back by clip", async () => {
  const calls = [];
  const run = async (program, args, options) => {
    calls.push({ program, args, options });
    return { stdout: "line-1.wav hello there\r\nline-2.wav second line\nnoise\n" };
  };
  const heard = await secondTranscripts(["python", "whisper.py"], "ja", clips(2), { run, env: {} });
  assert.deepEqual([...heard], [["line-1.wav", "hello there"], ["line-2.wav", "second line"]]);
  assert.equal(calls[0].options.timeout, TIMEOUT_BASE_MS + 2 * TIMEOUT_PER_CLIP_MS);
  assert.deepEqual(calls[0].args, ["whisper.py", "ja", ...clips(2)]);

  await secondTranscripts(["python", "whisper.py"], "ja", clips(2), { run, env: { [SECOND_OPINION_TIMEOUT_ENV]: "60000" } });
  assert.equal(calls[1].options.timeout, 60_000);
});

test("a run killed by its time limit says it timed out, with the clip count and the limit", async () => {
  const run = async () => {
    throw Object.assign(new Error("Command failed: python whisper.py ja ..."), { killed: true, signal: "SIGTERM", code: null });
  };
  await assert.rejects(
    secondTranscripts(["python", "whisper.py"], "ja", clips(30), { run, env: {} }),
    (error) => {
      assert.match(error.message, /^timed out after 70 min on 30 clips;/);
      assert.match(error.message, new RegExp(SECOND_OPINION_TIMEOUT_ENV));
      assert.doesNotMatch(error.message.split("\n")[0], /Command failed/);
      return true;
    },
  );
  await assert.rejects(
    secondTranscripts(["python", "whisper.py"], "ja", clips(1), { run, env: { [SECOND_OPINION_TIMEOUT_ENV]: "90000" } }),
    /^Error: timed out after 1\.5 min on 1 clip;/,
  );
});

test("other failures keep their own message", async () => {
  const crashed = Object.assign(new Error("Command failed: python whisper.py\nTraceback ..."), { killed: false, code: 1 });
  await assert.rejects(secondTranscripts(["python", "whisper.py"], "ja", clips(3), { run: async () => { throw crashed; }, env: {} }), (error) => error === crashed);
  const flooded = Object.assign(new Error("stdout maxBuffer length exceeded"), { killed: true, code: "ERR_CHILD_PROCESS_STDIO_MAXBUFFER" });
  await assert.rejects(secondTranscripts(["python", "whisper.py"], "ja", clips(3), { run: async () => { throw flooded; }, env: {} }), (error) => error === flooded);
});

test("a real program that outlives its limit is reported as timed out", async () => {
  const command = [process.execPath, "-e", "setTimeout(() => {}, 60000)", "--"];
  await assert.rejects(
    secondTranscripts(command, "ja", clips(2), { env: { ...process.env, [SECOND_OPINION_TIMEOUT_ENV]: "300" } }),
    /^Error: timed out after 0\.3 s on 2 clips;/,
  );
});
