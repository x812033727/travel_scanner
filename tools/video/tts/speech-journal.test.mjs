// The speech journal (speech-journal.mjs) with the real client (client.mjs) and an injected
// counting fetch: nothing here reaches a live, paid endpoint.
import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { createHash } from "node:crypto";
import fs, { copyFileSync, existsSync, mkdirSync, readdirSync, readFileSync, rmSync, symlinkSync, writeFileSync } from "node:fs";
import { syncBuiltinESMExports } from "node:module";
import path from "node:path";
import test from "node:test";

import { EXIT, main as cli } from "../cli.mjs";
import { fixture, sandbox, tempDir } from "../core/fixtures/load.mjs";
import { atomicWrite } from "../core/paths.mjs";
import { eachLine, textHash } from "../core/schema.mjs";
import { ARTIFACTS, loadProject } from "../core/state.mjs";
import { serverNarration, phraseBody } from "../shorts/speech.mjs";
import { SPEECH_UNCERTAIN, SpeechError, synthesize } from "./client.mjs";
import { planRequests } from "./requests.mjs";
import { JOURNAL_DIR, judgeBody, listSpeechJournal, main as journalCli, openSpeechJournal, requestSha256, SPEECH_TAKEN_OVER, transcribeBody } from "./speech-journal.mjs";
import { concatSamples, encodeWav, parseWav } from "./wav.mjs";

// The fixture videos run seconds; the eight-minute floor has tests of its own.
process.env.VIDEO_MIN_EPISODE_MINUTES ??= "0";

const TOKEN = `mkv_${"j".repeat(43)}`;
const SITE = "https://mokaair.test";
const tone = (samples, pitch = 7) => Int16Array.from({ length: samples }, (_, index) => Math.round(8000 * Math.sin(index / pitch)));
const body = { voice: "gemini:Sulafat", style: "說書人", segments: [{ parts: [{ text: "一張手寫的發票" }], break_after_ms: 0 }] };
const lost = () => Object.assign(new TypeError("fetch failed"), { cause: Object.assign(new Error("socket hang up"), { code: "ECONNRESET" }) });
const refused = () => Object.assign(new TypeError("fetch failed"), { cause: Object.assign(new Error("connect ECONNREFUSED"), { code: "ECONNREFUSED" }) });
const problem = (status, code) => new Response(JSON.stringify({ code, detail: code }), { status, headers: { "Content-Type": "application/json" } });

/** A narration server counting its paid POSTs; `answers` are used in turn, then a WAV per body. */
function speechServer(answers = []) {
  const posts = [];
  const fetchImpl = async (url, init) => {
    if (url.endsWith("/api/video/speech/status")) {
      return Response.json({ configured: true, voices: ["zh-TW-HsiaoChenNeural"], monthly_limit: 0, used: 0, remaining: 0, gemini_configured: true, gemini_monthly_limit: 300000, gemini_used: 0 });
    }
    // A site from before speech/align: tts asks it first for an Azure voice and is refused, unpaid.
    if (url.endsWith("/api/video/speech/align")) return new Response("not found", { status: 404 });
    posts.push(JSON.parse(init.body));
    const answer = answers.shift();
    if (typeof answer === "function") return answer();
    if (answer) return answer;
    const sent = JSON.parse(init.body);
    // 200 ms of tone a character (the pace at which the fixtures' chapters run the 10 s YouTube
    // needs), a pitch per post so two takes differ, then the requested break.
    const audio = concatSamples(sent.segments.flatMap((segment) => [tone(segment.parts.reduce((sum, part) => sum + part.text.length, 0) * 9600, 5 + posts.length), new Int16Array(segment.break_after_ms * 48)]));
    return new Response(encodeWav(audio), { status: 200, headers: { "Content-Type": "audio/wav", "X-Billable-Characters": "10" } });
  };
  return { posts, fetchImpl };
}

const options = (server) => ({ site: SITE, token: TOKEN, fetchImpl: server.fetchImpl, sleep: async () => {} });
const journalIn = () => path.join(tempDir("speech-journal-"), JOURNAL_DIR);
const sender = (dir, server) => {
  const journal = openSpeechJournal(dir, { now: () => new Date("2026-10-05T03:00:00Z") });
  return { journal, send: journal.wrap((sent) => synthesize({ ...options(server), body: sent })) };
};
const entry = (dir, sha) => JSON.parse(readFileSync(path.join(dir, `${sha}.json`), "utf8"));
const held = (pattern = /./) => (error) => error instanceof SpeechError && error.code === SPEECH_UNCERTAIN && error.who === "owner" && pattern.test(error.message) && error.message.includes(SPEECH_UNCERTAIN);

test("an answer that came back is taken from disk after a restart, bound to its exact body, until it is released", async (t) => {
  const dir = journalIn();
  const server = speechServer();
  const first = sender(dir, server);
  const answer = await first.send(body);
  assert.equal(server.posts.length, 1);
  const sha = requestSha256(body);
  const saved = entry(dir, sha);
  assert.equal(saved.status, "confirmed");
  assert.deepEqual(saved.request, body, "the entry keeps the body it was bought for");
  assert.equal(saved.billable, 10);
  assert.deepEqual(readFileSync(path.join(dir, `${sha}.wav`)), answer.wav);

  // The run stops before saving what it made of the answer: the next one reads it from disk.
  const restart = openSpeechJournal(dir);
  const again = await restart.wrap(async () => assert.fail("a confirmed answer is not bought again"))(body);
  assert.deepEqual(again.wav, answer.wav);
  assert.deepEqual([again.billable, again.reused, restart.reused, server.posts.length], [0, true, 1, 1]);

  // Once the caller has saved it, a retake of the same body buys a new take.
  restart.release();
  assert.deepEqual(readdirSync(dir), []);
  const retake = await sender(dir, server).send(body);
  assert.equal(server.posts.length, 2);
  assert.notDeepEqual(retake.wav, answer.wav);
});

test("a changed request never reuses another request's answer", async (t) => {
  const dir = journalIn();
  const server = speechServer();
  const { send } = sender(dir, server);
  const original = await send(body);
  const changes = {
    text: { ...body, segments: [{ parts: [{ text: "再扣掉三十元的折價券" }], break_after_ms: 0 }] },
    voice: { ...body, voice: "gemini:Kore" },
    model: { ...body, model: "gemini-2.5-pro-preview-tts" },
    style: { ...body, style: "Taiwan Mandarin, relaxed." },
    language: { ...body, language: "en" },
    pause: { ...body, segments: [{ parts: body.segments[0].parts, break_after_ms: 800 }] },
  };
  for (const [what, changed] of Object.entries(changes)) {
    const before = server.posts.length;
    const answer = await sender(dir, server).send(changed);
    assert.equal(server.posts.length, before + 1, `another ${what} is another request`);
    assert.notDeepEqual(answer.wav, original.wav, what);
  }
  const shas = new Set([body, ...Object.values(changes)].map(requestSha256));
  assert.equal(shas.size, 7);
  assert.deepEqual((await sender(dir, server).send(body)).wav, original.wav, "the original is still its own");
  assert.equal(server.posts.length, 7);
});

test("a lost POST is sent once, and a later run does not send it again until a person forgets it", async (t) => {
  const dir = journalIn();
  const server = speechServer([() => { throw lost(); }]);
  const sha = requestSha256(body);
  const firstRun = sender(dir, server);
  await assert.rejects(firstRun.send(body), (error) => held(/no usable answer came back/)(error) && error.requestSha256 === sha && error.message.includes(`forget --dir "${dir}" --sha ${sha}`));
  assert.equal(server.posts.length, 1, "the client did not resend it");
  assert.equal(entry(dir, sha).status, "held");

  // The client names the same request: its sha256 is the journal's key.
  await assert.rejects(synthesize({ ...options({ fetchImpl: async () => { throw lost(); } }), body }), (error) => error.code === SPEECH_UNCERTAIN && error.requestSha256 === sha);

  const restart = sender(dir, server);
  await assert.rejects(restart.send(body), held(/is held in the speech journal since 2026-10-05T03:00:00.000Z/));
  assert.equal(server.posts.length, 1, "a restart sends nothing");

  const out = { stdout: "", stderr: "" };
  const io = { stdout: { write: (text) => (out.stdout += text) }, stderr: { write: (text) => (out.stderr += text) } };
  assert.equal(journalCli(["list", "--dir", dir], io), 0);
  assert.match(out.stdout, new RegExp(`^${sha} held .* gemini:Sulafat "一張手寫的發票"`, "m"));
  assert.match(out.stdout, /1 held: check the provider's usage/);
  assert.match(out.stdout, /rerun the original native command to validate retained complete answers first/);
  assert.ok(out.stdout.indexOf("retained complete answers first") < out.stdout.indexOf("1 held: check"), "validate a retained answer before deciding whether to clear its hold");
  assert.equal(journalCli(["forget", "--dir", dir, "--sha", "0".repeat(64)], io), 2, "an unknown entry is a usage error");
  assert.equal(journalCli(["forget", "--dir", dir], io), 2);
  assert.equal(journalCli(["list"], io), 2);
  assert.equal(journalCli(["list", "--dir", dir, sha], io), 2);
  assert.equal(journalCli(["forget", "--dir", dir, "--sha", sha], io), 0);
  assert.match(out.stdout, /forgot .* \(held\)/);

  await sender(dir, server).send(body);
  assert.equal(server.posts.length, 2, "after forget it is sent once more");
});

test("an answer lost, broken or unusable on the way is held and not bought again", async (t) => {
  const stereo = () => {
    const wav = encodeWav(tone(4800));
    wav.writeUInt16LE(2, 22);
    return new Response(wav, { status: 200, headers: { "Content-Type": "audio/wav" } });
  };
  const cases = {
    "a body that breaks off": () => new Response(new ReadableStream({ start(controller) { controller.error(new Error("terminated")); } }), { status: 200 }),
    "a body that is not audio": () => new Response("not audio", { status: 200, headers: { "Content-Type": "audio/wav" } }),
    "audio the timeline cannot use": stereo,
    "the web route's lost answer": () => problem(504, "video_speech_answer_lost"),
    "a server error with no code": () => problem(500, ""),
  };
  for (const [what, answer] of Object.entries(cases)) {
    await t.test(what, async (t) => {
      const dir = journalIn();
      const server = speechServer([answer]);
      await assert.rejects(sender(dir, server).send(body), held());
      assert.equal(server.posts.length, 1);
      assert.equal(entry(dir, requestSha256(body)).status, "held");
      await assert.rejects(sender(dir, server).send(body), held(/held in the speech journal/));
      assert.equal(server.posts.length, 1);
    });
  }
});

test("a run that stopped after sending leaves a hold the next run respects", async (t) => {
  const dir = journalIn();
  const sha = requestSha256(body);
  let recorded = null;
  // The process dies while the request is out: the answer never comes.
  openSpeechJournal(dir).wrap(async () => {
    recorded = entry(dir, sha);
    return new Promise(() => {});
  })(body);
  await new Promise((resolve) => setImmediate(resolve));
  assert.deepEqual([recorded?.status, recorded?.request], ["sent", body], "recorded before it went out");
  const server = speechServer();
  await assert.rejects(sender(dir, server).send(body), held(/by a run that recorded no answer/));
  assert.equal(server.posts.length, 0);

  // Nor does a second run send it while the first is still waiting for its answer.
  const other = journalIn();
  let answer;
  const slow = openSpeechJournal(other).wrap(() => new Promise((resolve) => (answer = resolve)))(body);
  await assert.rejects(sender(other, server).send(body), held(/may still be running/));
  answer({ wav: encodeWav(tone(4800)), billable: 3 });
  assert.equal((await slow).billable, 3);
  assert.equal(entry(other, sha).status, "confirmed");
  assert.equal(server.posts.length, 0);
});

test("a saved answer changed on disk, or an entry that cannot be read, holds instead of being trusted or bought again", async (t) => {
  const dir = journalIn();
  const server = speechServer();
  await sender(dir, server).send(body);
  const sha = requestSha256(body);
  const wav = path.join(dir, `${sha}.wav`);
  writeFileSync(wav, Buffer.concat([readFileSync(wav), Buffer.alloc(2)]));
  await assert.rejects(sender(dir, server).send(body), held(/missing or changed on disk/));
  assert.equal(entry(dir, sha).status, "held");
  assert.equal(server.posts.length, 1);

  const other = { ...body, voice: "gemini:Kore" };
  writeFileSync(path.join(dir, `${requestSha256(other)}.json`), "{\"status\":");
  await assert.rejects(sender(dir, server).send(other), held(/cannot be read/));
  assert.equal(server.posts.length, 1);
  assert.deepEqual(listSpeechJournal(dir).map((item) => item.status).sort(), ["held", "unreadable"]);
});

test("a request the API settled leaves nothing behind, so the next run may send it", async (t) => {
  const cases = {
    "a voice not on the allowlist": { answers: [() => problem(403, "video_speech_voice_not_allowed")], posts: 1, who: "owner" },
    "a spent month": { answers: [() => problem(429, "video_speech_budget_exhausted")], posts: 1, who: "service" },
    // Jev's key not set (speech/judge's answer before any Jev call): a setting, nothing to hold.
    "Jev's key not set": { answers: [() => problem(503, "provider_unavailable")], posts: 1, who: "owner" },
    "a site that never answered": { answers: Array.from({ length: 5 }, () => () => { throw refused(); }), posts: 5, who: "service" },
  };
  for (const [what, { answers, posts, who }] of Object.entries(cases)) {
    await t.test(what, async (t) => {
      const dir = journalIn();
      const server = speechServer([...answers]);
      await assert.rejects(sender(dir, server).send(body), (error) => error instanceof SpeechError && error.code !== SPEECH_UNCERTAIN && error.who === who);
      assert.equal(server.posts.length, posts);
      assert.deepEqual(readdirSync(dir), []);
      await sender(dir, server).send(body);
      assert.equal(server.posts.length, posts + 1);
    });
  }
  // The API's own failure is retried by the client within the run, then confirmed once.
  const dir = journalIn();
  const server = speechServer([() => problem(502, "video_speech_upstream_failed")]);
  await sender(dir, server).send(body);
  assert.equal(server.posts.length, 2);
  assert.equal(entry(dir, requestSha256(body)).status, "confirmed");
});

// A run whose client sits in a wait between two tries until `wake()`; it never wakes if the run
// stopped there.
function sleeper(dir, server) {
  const waits = [];
  const journal = openSpeechJournal(dir, { now: () => new Date("2026-10-05T03:00:00Z") });
  const sleep = (ms) => new Promise((resolve) => waits.push({ ms, wake: resolve }));
  const send = journal.wrap((sent) => synthesize({ ...options(server), sleep, body: sent }));
  return { journal, send, waits };
}
const until = async (done) => {
  for (let turn = 0; turn < 100 && !done(); turn++) await new Promise((resolve) => setImmediate(resolve));
  assert.ok(done(), "the run got there");
};
const limited = () => problem(429, "rate_limit_exceeded");

test("a request whose run stopped while it waited to try again is sent by the next run, once", async (t) => {
  const cases = {
    "the routes' rate limit": { answer: limited, why: /^HTTP 429 rate_limit_exceeded; sent again in 61 s$/ },
    "a provider busy": { answer: () => problem(503, "video_speech_upstream_busy"), why: /^HTTP 503 video_speech_upstream_busy; sent again in 1 s$/ },
    "a site that was not reached": { answer: () => { throw refused(); }, why: /^the API was not reached; sent again in 1 s$/ },
  };
  for (const [what, { answer, why }] of Object.entries(cases)) {
    await t.test(what, async () => {
      const dir = journalIn();
      const sha = requestSha256(body);
      const server = speechServer([answer]);
      // A deploy restarts the worker during the wait: this run never wakes.
      const stopped = sleeper(dir, server);
      stopped.send(body);
      await until(() => stopped.waits.length === 1);
      const waiting = entry(dir, sha);
      assert.deepEqual([waiting.status, waiting.request], ["waiting", body]);
      assert.match(waiting.why, why);
      assert.match(waiting.wait_id, /^[0-9a-f-]{36}$/);

      const out = { stdout: "", stderr: "" };
      const io = { stdout: { write: (text) => (out.stdout += text) }, stderr: { write: (text) => (out.stderr += text) } };
      assert.equal(journalCli(["list", "--dir", dir], io), 0);
      assert.match(out.stdout, new RegExp(`^${sha} waiting 2026-10-05T03:00:00.000Z gemini:Sulafat`, "m"));
      assert.match(out.stdout, /1 waiting: nothing of it is out/);
      assert.doesNotMatch(out.stdout, /held/, "nothing for the owner to forget");

      const posts = server.posts.length;
      const answered = await sender(dir, server).send(body);
      assert.equal(server.posts.length, posts + 1, "sent once by the next run");
      assert.deepEqual(entry(dir, sha).status, "confirmed");
      assert.deepEqual(readFileSync(path.join(dir, `${sha}.wav`)), answered.wav);
      assert.deepEqual(readdirSync(dir).sort(), [`${sha}.json`, `${sha}.wav`], "no claim left behind");
    });
  }
});

test("a run that wakes after another run sent its request stops without sending it again", async () => {
  const dir = journalIn();
  const sha = requestSha256(body);
  const server = speechServer([limited, limited]);
  const first = sleeper(dir, server);
  const firstRun = first.send(body);
  await until(() => first.waits.length === 1);
  // A second run takes the waiting request over, and is refused and waits in its turn.
  const second = sleeper(dir, server);
  const secondRun = second.send(body);
  await until(() => second.waits.length === 1);
  assert.equal(server.posts.length, 2);
  const theirs = entry(dir, sha);
  assert.equal(theirs.status, "waiting");

  first.waits[0].wake();
  await assert.rejects(firstRun, (error) => {
    assert.ok(error instanceof SpeechError);
    // The service's, exit 4: the worker comes back to it, and nothing is held for the owner.
    assert.deepEqual([error.code, error.who, error.requestSha256], [SPEECH_TAKEN_OVER, "service", sha]);
    assert.match(error.message, /^POST \/api\/video\/speech was sent by another run while this one waited to send it again, so it is not sent twice/);
    assert.doesNotMatch(error.message, /\n/);
    return true;
  });
  assert.equal(server.posts.length, 2, "the first run sent nothing more");
  assert.deepEqual(entry(dir, sha), theirs, "and left the other run's entry as it was");

  second.waits[0].wake();
  const answer = await secondRun;
  assert.equal(server.posts.length, 3);
  assert.equal(entry(dir, sha).status, "confirmed");
  assert.deepEqual(readFileSync(path.join(dir, `${sha}.wav`)), answer.wav);
  // The run that took it over sent it, so a third run takes the answer from disk.
  const third = openSpeechJournal(dir);
  assert.deepEqual((await third.wrap(async () => assert.fail("not bought again"))(body)).wav, answer.wav);
});

test("a run that wakes after another run took its request over stops, whatever that run has done since", async (t) => {
  const cases = {
    "its POST still out": { second: () => new Promise(() => {}), after: async () => {} },
    "its answer saved": { second: undefined, after: async (run) => { await run; } },
    "its answer saved and released": { second: undefined, after: async (run, journal) => { await run; journal.release(); } },
  };
  for (const [what, { second, after }] of Object.entries(cases)) {
    await t.test(what, async () => {
      const dir = journalIn();
      const sha = requestSha256(body);
      const server = speechServer([limited, ...(second ? [second] : [])]);
      const first = sleeper(dir, server);
      const firstRun = first.send(body);
      await until(() => first.waits.length === 1);
      const other = sender(dir, server);
      const otherRun = other.send(body);
      await until(() => server.posts.length === 2);
      await after(otherRun, other.journal);
      const left = existsSync(path.join(dir, `${sha}.json`)) ? entry(dir, sha) : null;
      first.waits[0].wake();
      await assert.rejects(firstRun, (error) => error.code === SPEECH_TAKEN_OVER);
      assert.equal(server.posts.length, 2, "the woken run sent nothing");
      assert.deepEqual(existsSync(path.join(dir, `${sha}.json`)) ? entry(dir, sha) : null, left, "and left the other run's entry, or its absence, as it was");
    });
  }
});

test("a wait the journal could not record stops the request before the sleep, and it holds", async () => {
  const dir = journalIn();
  const sha = requestSha256(body);
  // The waiting entry is renamed into place and its fsync then fails: on disk it may say waiting.
  let failNext = false;
  const server = speechServer([() => { failNext = true; return limited(); }]);
  const saved = fs.fsyncSync;
  fs.fsyncSync = (fd) => {
    if (failNext) {
      failNext = false;
      throw Object.assign(new Error("EIO: i/o error, fsync"), { code: "EIO" });
    }
    return saved(fd);
  };
  syncBuiltinESMExports();
  const sleeps = [];
  const send = openSpeechJournal(dir).wrap((sent) => synthesize({ ...options(server), sleep: async (ms) => sleeps.push(ms), body: sent }));
  try {
    await assert.rejects(send(body), /the journal could not record its wait: EIO/);
  } finally {
    fs.fsyncSync = saved;
    syncBuiltinESMExports();
  }
  assert.deepEqual(sleeps, [], "no sleep, so no resend from this run");
  assert.equal(server.posts.length, 1);
  assert.equal(entry(dir, sha).status, "held");
  await assert.rejects(sender(dir, server).send(body), held(/held in the speech journal/));
  assert.equal(server.posts.length, 1, "nor from the next one");
});

test("a request sent again after its wait holds as any sent one does", async (t) => {
  // Lost on the way after the wait: held, as without one.
  const dir = journalIn();
  const sha = requestSha256(body);
  const server = speechServer([limited, () => { throw lost(); }]);
  await assert.rejects(sender(dir, server).send(body), held(/no usable answer came back/));
  assert.equal(server.posts.length, 2);
  assert.equal(entry(dir, sha).status, "held");
  await assert.rejects(sender(dir, server).send(body), held(/held in the speech journal/));
  assert.equal(server.posts.length, 2);

  // The run stops while the second POST is out: the entry says sent again, and holds.
  const other = journalIn();
  const out = speechServer([limited, () => new Promise(() => {})]);
  const stopped = sender(other, out);
  stopped.send(body);
  await until(() => out.posts.length === 2);
  assert.equal(entry(other, sha).status, "sent");
  await assert.rejects(sender(other, out).send(body), held(/by a run that recorded no answer/));
  assert.equal(out.posts.length, 2);
  assert.deepEqual(readdirSync(other), [`${sha}.json`]);
});

test("a waiting request another run is claiming is not sent by this one", async () => {
  const dir = journalIn();
  const sha = requestSha256(body);
  const server = speechServer([limited]);
  const stopped = sleeper(dir, server);
  stopped.send(body);
  await until(() => stopped.waits.length === 1);
  // Between its claim and its write: the claim file says another run is turning it into its own.
  const { wait_id: waitId } = entry(dir, sha);
  writeFileSync(path.join(dir, `${sha}.${waitId}.claim`), "");
  await assert.rejects(sender(dir, server).send(body), held(/another run keeps changing/));
  assert.equal(server.posts.length, 1);
  const waiting = entry(dir, sha);
  assert.equal(waiting.status, "waiting");
  // A claim left by a run that stopped while taking the entry back holds every run: `list` says
  // so, and `forget` clears the claim with the entry.
  const out = { stdout: "", stderr: "" };
  const io = { stdout: { write: (text) => (out.stdout += text) }, stderr: { write: (text) => (out.stderr += text) } };
  assert.equal(journalCli(["list", "--dir", dir], io), 0);
  assert.match(out.stdout, new RegExp(`^${sha} claimed `, "m"));
  assert.match(out.stdout, /1 claimed by a run that stopped while taking it back: nothing of it went out/);
  assert.doesNotMatch(out.stdout, /waiting: /);
  assert.equal(listSpeechJournal(dir)[0].claimed, true);
  assert.equal(journalCli(["forget", "--dir", dir, "--sha", sha], io), 0);
  assert.deepEqual(readdirSync(dir), []);
  await sender(dir, server).send(body);
  assert.equal(server.posts.length, 2, "sent once after forget");
  const posts = server.posts.length;
  // A waiting entry without a usable wait id is not one: it holds like an unreadable entry.
  const other = journalIn();
  mkdirSync(other, { recursive: true });
  writeFileSync(path.join(other, `${sha}.json`), JSON.stringify({ ...waiting, wait_id: "../../elsewhere" }));
  await assert.rejects(sender(other, server).send(body), held(/cannot be read/));
  assert.equal(server.posts.length, posts);
});

// --- the consumers -----------------------------------------------------------------------------

function capture(box, server, extra = {}) {
  const out = { stdout: "", stderr: "" };
  const ctx = {
    root: box.root,
    env: { VIDEO_WORKDIR: box.work, MOKAAIR_VIDEO_TOKEN: TOKEN, MOKAAIR_SITE: SITE },
    home: box.base,
    stdout: { write: (text) => (out.stdout += text) },
    stderr: { write: (text) => (out.stderr += text) },
    now: () => new Date("2026-10-05T03:00:00Z"),
    fetch: server.fetchImpl,
    sleep: async () => {},
    ...extra,
  };
  return { ctx, out };
}

const forgetFrom = (stderr) => {
  const [, dir, sha] = stderr.match(/forget --dir "([^"]+)" --sha ([0-9a-f]{64})/) ?? [];
  assert.ok(dir && sha, stderr);
  assert.equal(journalCli(["forget", "--dir", dir, "--sha", sha], { stdout: { write() {} }, stderr: { write() {} } }), 0);
  return dir;
};

test("tts holds a lost request across runs and takes an answer it already paid for from the journal", async () => {
  const box = sandbox();
  const server = speechServer([() => { throw lost(); }]);
  const lostRun = capture(box, server);
  assert.equal(await cli(["tts", "--slug", box.slug], lostRun.ctx), EXIT.owner);
  assert.match(lostRun.out.stderr.trim().split("\n").at(-1), new RegExp(SPEECH_UNCERTAIN), "the worker reads the code from the last line");
  assert.equal(server.posts.length, 1);
  const rerun = capture(box, server);
  assert.equal(await cli(["tts", "--slug", box.slug], rerun.ctx), EXIT.owner);
  assert.equal(server.posts.length, 1, "the rerun does not send it again");
  const dir = forgetFrom(rerun.out.stderr);
  assert.equal(dir, path.join(box.workdir, ARTIFACTS.audio, JOURNAL_DIR));

  // An answer bought by a run that stopped before saving it: the next tts uses it.
  const { doc, lexicon } = loadProject({ slug: box.slug, root: box.root });
  const [request] = planRequests(doc, lexicon).filter((item) => !item.audio_ref);
  const bought = await openSpeechJournal(dir).wrap((sent) => synthesize({ ...options(server), body: sent }))(request.body);
  const posts = server.posts.length;
  const run = capture(box, server);
  assert.equal(await cli(["tts", "--slug", box.slug], run.ctx), EXIT.ok, run.out.stderr);
  assert.equal(server.posts.length, posts + 2, "only the other two scenes are bought");
  assert.ok(!server.posts.slice(posts).some((sent) => requestSha256(sent) === requestSha256(request.body)));
  assert.match(run.out.stdout, /1 answers paid for by an earlier run came from the speech journal/);
  assert.deepEqual(readdirSync(dir), [], "released once cache.json holds the takes");
  const timeline = JSON.parse(readFileSync(path.join(box.workdir, "timeline.json"), "utf8"));
  assert.ok(timeline.lines.some((line) => line.id === request.lines[0].id));
  assert.ok(bought.wav.length > 44);
});

test("tts sends a request its last run left waiting out the rate limit, instead of holding it", async () => {
  const box = sandbox();
  const server = speechServer([() => problem(429, "rate_limit_exceeded")]);
  const dir = path.join(box.workdir, ARTIFACTS.audio, JOURNAL_DIR);
  // The worker is restarted while the first request waits for the routes' window to open.
  const waits = [];
  const stopped = capture(box, server, { sleep: (ms) => new Promise(() => waits.push(ms)) });
  cli(["tts", "--slug", box.slug], stopped.ctx);
  await until(() => waits.length === 1);
  assert.deepEqual(waits, [61_000]);
  assert.deepEqual(listSpeechJournal(dir).map((item) => item.status), ["waiting"]);
  const [waiting] = listSpeechJournal(dir);

  const run = capture(box, server);
  assert.equal(await cli(["tts", "--slug", box.slug], run.ctx), EXIT.ok, run.out.stderr);
  assert.equal(server.posts.filter((sent) => requestSha256(sent) === waiting.sha).length, 2, "refused once, then sent once");
  assert.doesNotMatch(run.out.stdout, /came from the speech journal/, "an answer of this run's, not an earlier one's");
  assert.deepEqual(readdirSync(dir), [], "released once cache.json holds the takes");
});

/** ffmpeg as the dub sees it: a measurement, a shortened copy for atempo, a plain copy otherwise. */
function fakeFfmpeg() {
  return {
    locate: async () => ({ ffmpeg: "ffmpeg", ffprobe: "ffprobe", version: "fake ffmpeg" }),
    run: async (_file, args) => {
      const input = args[args.indexOf("-i") + 1];
      if (args.includes("null")) return { stdout: "", stderr: 'Parsed_loudnorm {"input_i":"-20.0","input_tp":"-3.0","input_lra":"5.0","input_thresh":"-30.0","target_offset":"0.5"}\n' };
      const tempo = args.find((arg) => String(arg).startsWith("atempo="));
      if (tempo) {
        const wav = parseWav(readFileSync(input));
        writeFileSync(args.at(-1), encodeWav(wav.samples.slice(0, Math.round(wav.samples.length / Number(tempo.slice(7))))));
      } else {
        copyFileSync(input, args.at(-1));
      }
      return { stdout: "", stderr: "" };
    },
  };
}

test("a dub's lost request holds across runs until a person forgets it", async () => {
  const box = sandbox();
  const doc = { ...fixture(), voice: { provider: "gemini", name: "Sulafat", style: "Taiwan Mandarin, relaxed." } };
  writeFileSync(path.join(box.dir, "video.json"), JSON.stringify(doc));
  const lines = {};
  for (const { line } of eachLine(doc)) lines[line.id] = { source_hash: textHash(line.text), text: `EN ${line.id}` };
  mkdirSync(path.join(box.dir, "i18n"), { recursive: true });
  writeFileSync(path.join(box.dir, "i18n", "en.json"), JSON.stringify({ title: "T", description: "D", tags: [], chapters: {}, source_hashes: {}, lines }));
  const server = speechServer();
  const ffmpeg = fakeFfmpeg();
  const narrated = capture(box, server, { ffmpeg });
  const code = await cli(["tts", "--slug", box.slug], narrated.ctx);
  assert.ok(code === EXIT.ok || code === EXIT.lint, narrated.out.stderr);

  const posts = server.posts.length;
  server.fetchImpl = ((healthy) => {
    let first = true;
    return async (url, init) => {
      if (first && url.endsWith("/api/video/speech")) {
        first = false;
        server.posts.push(JSON.parse(init.body));
        throw lost();
      }
      return healthy(url, init);
    };
  })(server.fetchImpl);
  const dub = () => capture(box, server, { ffmpeg });
  const lostRun = dub();
  assert.equal(await cli(["dub", "--slug", box.slug, "--locale", "en"], lostRun.ctx), EXIT.owner);
  assert.match(lostRun.out.stderr, new RegExp(SPEECH_UNCERTAIN));
  assert.equal(server.posts.length, posts + 1);
  const rerun = dub();
  assert.equal(await cli(["dub", "--slug", box.slug, "--locale", "en"], rerun.ctx), EXIT.owner);
  assert.equal(server.posts.length, posts + 1, "the rerun does not send it again");
  assert.equal(forgetFrom(rerun.out.stderr), path.join(box.workdir, ARTIFACTS.audio, JOURNAL_DIR));
  const done = dub();
  assert.equal(await cli(["dub", "--slug", box.slug, "--locale", "en"], done.ctx), EXIT.ok, done.out.stdout + done.out.stderr);
  assert.ok(server.posts.length > posts + 1);
  assert.deepEqual(readdirSync(path.join(box.workdir, ARTIFACTS.audio, JOURNAL_DIR)), []);
});

test("a Short's server phrase holds when lost, and is taken from the journal when it came back unsaved", async () => {
  const cacheDir = path.join(tempDir("shorts-journal-"), ".speech-server");
  const voice = { provider: "gemini", name: "Sulafat", style: "說書人" };
  const phrases = ["一張手寫的發票", "再扣掉三十元的折價券"];
  const server = speechServer([() => { throw lost(); }]);
  const client = { site: SITE, token: TOKEN, fetch: server.fetchImpl, sleep: async () => {} };
  // No karaoke here (a build asks the aligner only for --captions karaoke), and this server has
  // no align route: every phrase POST it counts is a synthesis.
  await assert.rejects(serverNarration({ phrases, voice, cacheDir, client, align: false }), held());
  assert.equal(server.posts.length, 1);
  await assert.rejects(serverNarration({ phrases, voice, cacheDir, client, align: false }), held(/held in the speech journal/));
  assert.equal(server.posts.length, 1, "the next build or lab round does not send it again");
  const [held1] = listSpeechJournal(path.join(cacheDir, JOURNAL_DIR));
  assert.equal(held1.sha, requestSha256(phraseBody(voice, phrases[0])));
  assert.equal(journalCli(["forget", "--dir", path.join(cacheDir, JOURNAL_DIR), "--sha", held1.sha], { stdout: { write() {} }, stderr: { write() {} } }), 0);

  // The second phrase was bought by a build that stopped before caching it.
  const bought = await openSpeechJournal(path.join(cacheDir, JOURNAL_DIR)).wrap((sent) => synthesize({ ...options(server), body: sent }))(phraseBody(voice, phrases[1]));
  const posts = server.posts.length;
  const built = await serverNarration({ phrases, voice, cacheDir, client, align: false });
  assert.equal(server.posts.length, posts + 1, "only the first phrase is bought");
  assert.deepEqual([built.calls, built.characters], [1, 10], "the reused phrase is not counted as this build's");
  assert.deepEqual(built.clips[1], bought.wav);
  assert.deepEqual(readdirSync(path.join(cacheDir, JOURNAL_DIR)), []);
  assert.ok(existsSync(cacheDir));
});

// --- complete answers whose canonical confirmation could not be promoted -----------------------
// These fixtures inject only local I/O failures. A restarted journal gets an explicitly dead
// producer probe; no production PID, media directory, or paid endpoint is involved.
const fullSha = (bytes) => createHash("sha256").update(bytes).digest("hex");
const pretty = (value) => `${JSON.stringify(value, null, 2)}\n`;
const fixedRecoveryTime = () => new Date("2026-10-08T00:00:00Z");
const quietJournalIO = { stdout: { write() {} }, stderr: { write() {} } };
const recoveryAudio = encodeWav(tone(4800));
const recoveryTranscription = { wav: recoveryAudio, terms: ["Mokaair"], language: "ja" };
const recoveryJudgement = {
  lines: [{ id: "one", expected: "Hello", heard: "Hello" }, { id: "two", expected: "World", heard: "Word" }],
  language: "en",
};
const recoveryRoutes = [
  {
    name: "full WAV", sha: requestSha256(body), answer: { wav: recoveryAudio, billable: 37 },
    invoke: (journal, send) => journal.wrap(send)(body),
    check: (answer) => {
      assert.deepEqual(answer.wav, recoveryAudio);
      assert.deepEqual([answer.billable, answer.reused], [0, true]);
    },
  },
  {
    name: "ASR text", sha: requestSha256(transcribeBody(recoveryTranscription)), answer: "Mokaair の字幕です。",
    invoke: (journal, send) => journal.wrapTranscribe(send)(recoveryTranscription),
    check: (answer) => assert.equal(answer, "Mokaair の字幕です。"),
  },
  {
    name: "Jev results", sha: requestSha256(judgeBody(recoveryJudgement)), answer: new Map([["one", 0.97], ["two", NaN]]),
    invoke: (journal, send) => journal.wrapJudge(send)(recoveryJudgement),
    check: (answer) => assert.deepEqual(answer, new Map([["one", 0.97], ["two", NaN]])),
  },
];

async function failedConfirmation(spec = recoveryRoutes[0]) {
  const dir = journalIn();
  const canonical = path.join(dir, `${spec.sha}.json`);
  const staged = path.join(dir, `${spec.sha}.answer.json`);
  const temporary = `${canonical}.${process.pid}.tmp`;
  let calls = 0;
  let confirmed;
  const write = (file, data) => {
    if (file === canonical && JSON.parse(String(data)).status === "confirmed") {
      confirmed = Buffer.from(data);
      writeFileSync(temporary, confirmed);
      throw Object.assign(new Error("injected confirmed receipt EPERM"), { code: "EPERM" });
    }
    atomicWrite(file, data);
  };
  const first = openSpeechJournal(dir, { now: fixedRecoveryTime, write, processAlive: () => false });
  const send = async () => { calls += 1; return spec.answer; };
  await assert.rejects(spec.invoke(first, send), (error) => error.code === "EPERM");
  assert.equal(calls, 1);
  assert.equal(entry(dir, spec.sha).status, "sent");
  assert.ok(existsSync(staged), "the complete staged confirmation survives the failed rename");
  const sent = readFileSync(canonical);
  const envelope = JSON.parse(readFileSync(staged, "utf8"));
  assert.equal(envelope.sent_sha256, fullSha(sent));
  assert.equal(envelope.sent_bytes, sent.length);
  assert.equal(envelope.confirmed_sha256, fullSha(confirmed));
  assert.equal(envelope.confirmed_bytes, confirmed.length);
  assert.deepEqual(Buffer.from(envelope.confirmed_base64, "base64"), confirmed);
  return { dir, canonical, staged, temporary, sent, confirmed, spec, send, calls: () => calls };
}

function archiveSnapshot(dir) {
  const archive = path.join(dir, "recovery");
  const files = new Map();
  function walk(directory) {
    if (!existsSync(directory)) return;
    for (const item of readdirSync(directory, { withFileTypes: true })) {
      const file = path.join(directory, item.name);
      if (item.isDirectory()) walk(file);
      else if (item.isFile()) files.set(path.relative(archive, file), readFileSync(file));
    }
  }
  walk(archive);
  return files;
}

function replaceCandidates(failed, confirmed) {
  const raw = Buffer.from(pretty(confirmed));
  const envelope = JSON.parse(readFileSync(failed.staged, "utf8"));
  writeFileSync(failed.staged, pretty({ ...envelope, confirmed_sha256: fullSha(raw), confirmed_bytes: raw.length, confirmed_base64: raw.toString("base64") }));
  writeFileSync(failed.temporary, raw);
}

test("a failed confirmed promotion preserves and reuses complete WAV, ASR and Jev answers after restart", async (t) => {
  for (const spec of recoveryRoutes) {
    await t.test(spec.name, async () => {
      const failed = await failedConfirmation(spec);
      const restarted = openSpeechJournal(failed.dir, { processAlive: () => false });
      spec.check(await spec.invoke(restarted, failed.send));
      assert.equal(failed.calls(), 1, "recovery never resends the paid request");
      assert.equal(restarted.reused, 1);
      assert.deepEqual(readFileSync(failed.canonical), failed.sent, "recovery does not promote or rewrite sent");
      const archived = archiveSnapshot(failed.dir);
      assert.ok([...archived.values()].some((bytes) => bytes.equals(failed.sent)), "original full sent bytes are archived");
      assert.ok([...archived.values()].some((bytes) => bytes.equals(failed.confirmed)), "original full confirmation bytes are archived");
      if (spec.name === "full WAV") assert.ok([...archived.values()].some((bytes) => bytes.equals(recoveryAudio)), "the full WAV is archived");
      assert.ok([...archived.keys()].some((file) => path.basename(file) === "proof.json"));
      const again = openSpeechJournal(failed.dir, { processAlive: () => false });
      spec.check(await spec.invoke(again, failed.send));
      assert.deepEqual(archiveSnapshot(failed.dir), archived, "repeated recovery keeps every archived byte unchanged");
      assert.equal(failed.calls(), 1);
      restarted.release();
      assert.ok(!existsSync(failed.canonical));
      assert.ok(!existsSync(failed.staged));
      assert.deepEqual(archiveSnapshot(failed.dir), archived, "cache release preserves recovery evidence");
    });
  }
});

test("a staged confirmation alone survives a restart without relying on the failed rename temporary", async () => {
  const failed = await failedConfirmation();
  rmSync(failed.temporary);
  const restarted = openSpeechJournal(failed.dir, { processAlive: () => false });
  failed.spec.check(await failed.spec.invoke(restarted, failed.send));
  assert.equal(failed.calls(), 1);
});

test("a complete answer after a settled waiting resend survives local promotion failure bound to the final sent receipt", async (t) => {
  for (const takeover of [false, true]) {
    await t.test(takeover ? "another run resumes the waiting request" : "the original run wakes and resends", async () => {
      const dir = journalIn();
      const sha = requestSha256(body);
      const canonical = path.join(dir, `${sha}.json`);
      const server = speechServer([limited]);
      const fetch = server.fetchImpl;
      const sentAttempts = [];
      server.fetchImpl = async (url, init) => {
        if (url.endsWith("/api/video/speech")) sentAttempts.push(readFileSync(canonical));
        return fetch(url, init);
      };
      if (takeover) {
        const stopped = sleeper(dir, server);
        stopped.send(body);
        await until(() => stopped.waits.length === 1);
        assert.equal(entry(dir, sha).status, "waiting");
      }
      let clock = 0;
      let injected = 0;
      const journal = openSpeechJournal(dir, {
        now: () => new Date(Date.parse("2026-10-08T00:00:00Z") + clock++ * 1000),
        write(file, data) {
          if (file === canonical && JSON.parse(String(data)).status === "confirmed") {
            injected += 1;
            writeFileSync(`${file}.${process.pid}.tmp`, data);
            throw Object.assign(new Error("injected post-resume confirmed EPERM"), { code: "EPERM" });
          }
          // Keep the local fixture's waiting/resume writes deterministic; only the complete
          // confirmed receipt promotion is the injected failure this case exercises.
          writeFileSync(file, data);
        },
      });
      await assert.rejects(journal.wrap((sent) => synthesize({ ...options(server), body: sent }))(body), (error) => error.code === "EPERM");
      assert.equal(injected, 1);
      assert.equal(server.posts.length, 2, "one settled refusal followed by one successful answer");
      assert.equal(sentAttempts.length, 2);
      assert.notEqual(fullSha(sentAttempts[0]), fullSha(sentAttempts[1]), "the resumed POST has its own actual final sent bytes");
      const finalSent = readFileSync(canonical);
      assert.deepEqual(finalSent, sentAttempts[1]);
      assert.equal(JSON.parse(finalSent).status, "sent");
      assert.equal(JSON.parse(finalSent).producer_pid, process.pid);
      if (takeover) assert.notEqual(JSON.parse(sentAttempts[0]).generation, JSON.parse(finalSent).generation);
      else assert.equal(JSON.parse(sentAttempts[0]).generation, JSON.parse(finalSent).generation);
      const stage = JSON.parse(readFileSync(path.join(dir, `${sha}.answer.json`), "utf8"));
      assert.equal(stage.sent_sha256, fullSha(finalSent));
      assert.equal(stage.sent_bytes, finalSent.length);
      const confirmed = JSON.parse(Buffer.from(stage.confirmed_base64, "base64"));
      assert.equal(confirmed.sent_sha256, fullSha(finalSent));
      assert.equal(confirmed.generation, JSON.parse(finalSent).generation);
      const fullWav = readFileSync(path.join(dir, `${sha}.wav`));
      let recoveryCalls = 0;
      const restarted = openSpeechJournal(dir, { processAlive: () => false });
      const answer = await restarted.wrap(async () => { recoveryCalls += 1; assert.fail("a saved post-resume answer is not sent again"); })(body);
      assert.deepEqual(answer.wav, fullWav);
      assert.deepEqual([answer.billable, answer.reused, restarted.reused, recoveryCalls], [0, true, 1, 0]);
      assert.equal(server.posts.length, 2);
      assert.deepEqual(readFileSync(canonical), finalSent);
      assert.ok([...archiveSnapshot(dir).values()].some((bytes) => bytes.equals(finalSent)));
    });
  }
});

test("a real closed producer's complete answer is reused after restart using the default PID probe", async () => {
  const dir = journalIn();
  const journalURL = new URL("./speech-journal.mjs", import.meta.url).href;
  const pathsURL = new URL("../core/paths.mjs", import.meta.url).href;
  const script = `
    import assert from "node:assert/strict";
    import { existsSync, readFileSync, writeFileSync } from "node:fs";
    import path from "node:path";
    import { openSpeechJournal, requestSha256 } from ${JSON.stringify(journalURL)};
    import { atomicWrite } from ${JSON.stringify(pathsURL)};
    const [dir, base64, serializedBody] = process.argv.slice(1);
    const body = JSON.parse(serializedBody);
    const sha = requestSha256(body);
    const canonical = path.join(dir, sha + ".json");
    let calls = 0;
    let injected = 0;
    const journal = openSpeechJournal(dir, {
      write(file, data) {
        if (file === canonical && JSON.parse(String(data)).status === "confirmed") {
          injected += 1;
          writeFileSync(file + "." + process.pid + ".tmp", data);
          throw Object.assign(new Error("injected confirmed receipt EPERM"), { code: "EPERM" });
        }
        atomicWrite(file, data);
      },
    });
    await assert.rejects(journal.wrap(async () => {
      calls += 1;
      return { wav: Buffer.from(base64, "base64"), billable: 23 };
    })(body), (error) => error.code === "EPERM");
    assert.equal(calls, 1);
    assert.equal(injected, 1, "the observed failure is the injected confirmation promotion");
    assert.equal(JSON.parse(readFileSync(canonical, "utf8")).status, "sent");
    assert.ok(existsSync(path.join(dir, sha + ".answer.json")));
    console.log(JSON.stringify({ pid: process.pid, calls, injected }));
  `;
  const closed = spawnSync(process.execPath, ["--input-type=module", "--eval", script, dir, recoveryAudio.toString("base64"), JSON.stringify(body)], {
    encoding: "utf8", timeout: 20000, windowsHide: true,
  });
  assert.ifError(closed.error);
  assert.equal(closed.status, 0, `producer failed: ${closed.stderr || closed.stdout}`);
  assert.equal(closed.signal, null);
  const producer = JSON.parse(closed.stdout.trim());
  assert.ok(Number.isInteger(producer.pid) && producer.pid !== process.pid);
  assert.deepEqual([producer.calls, producer.injected], [1, 1]);
  assert.equal(entry(dir, requestSha256(body)).producer_pid, producer.pid);
  let parentCalls = 0;
  const restarted = openSpeechJournal(dir);
  const answer = await restarted.wrap(async () => { parentCalls += 1; assert.fail("a closed producer's complete answer is not bought again"); })(body);
  assert.deepEqual(answer.wav, recoveryAudio);
  assert.deepEqual([answer.billable, answer.reused, restarted.reused, parentCalls], [0, true, 1, 0]);
  assert.equal(entry(dir, requestSha256(body)).status, "sent", "default-probe recovery still leaves canonical unchanged");
  const archived = archiveSnapshot(dir);
  assert.ok([...archived.values()].some((bytes) => bytes.equals(recoveryAudio)));
  assert.equal([...archived.keys()].filter((file) => path.basename(file) === "proof.json").length, 1);
});

test("a live or unknown confirmed-answer producer remains held without altering evidence", async (t) => {
  for (const state of [true, null]) {
    await t.test(String(state), async () => {
      const failed = await failedConfirmation();
      const staged = readFileSync(failed.staged);
      const temporary = readFileSync(failed.temporary);
      await assert.rejects(failed.spec.invoke(openSpeechJournal(failed.dir, { processAlive: () => state }), failed.send), held());
      assert.equal(failed.calls(), 1);
      assert.deepEqual(readFileSync(failed.canonical), failed.sent);
      assert.deepEqual(readFileSync(failed.staged), staged);
      assert.deepEqual(readFileSync(failed.temporary), temporary);
      assert.equal(archiveSnapshot(failed.dir).size, 0);
    });
  }
});

test("missing, changed, truncated or wrong-format full WAVs hold despite complete confirmation JSON", async (t) => {
  const changes = {
    missing: (file) => rmSync(file),
    changed: (file) => { const bytes = readFileSync(file); bytes[bytes.length - 1] ^= 1; writeFileSync(file, bytes); },
    truncated: (file) => writeFileSync(file, readFileSync(file).subarray(0, 44)),
    "wrong format with matching hash": (file, failed) => {
      const bytes = readFileSync(file);
      bytes.writeUInt16LE(2, 22);
      writeFileSync(file, bytes);
      replaceCandidates(failed, { ...JSON.parse(failed.confirmed), wav_sha256: fullSha(bytes), wav_bytes: bytes.length });
    },
  };
  for (const [name, change] of Object.entries(changes)) {
    await t.test(name, async () => {
      const failed = await failedConfirmation();
      change(path.join(failed.dir, `${failed.spec.sha}.wav`), failed);
      const staged = readFileSync(failed.staged);
      await assert.rejects(failed.spec.invoke(openSpeechJournal(failed.dir, { processAlive: () => false }), failed.send), held());
      assert.equal(failed.calls(), 1);
      assert.deepEqual(readFileSync(failed.canonical), failed.sent);
      assert.deepEqual(readFileSync(failed.staged), staged);
    });
  }
});

test("corrupt hashes and malformed inline answers cannot become recovered ASR or Jev evidence", async (t) => {
  const cases = [
    ["ASR hash changed", recoveryRoutes[1], (saved) => ({ ...saved, answer_sha256: "0".repeat(64) })],
    ["ASR text is not a string", recoveryRoutes[1], (saved) => { const answer = { text: 123 }; return { ...saved, answer, answer_sha256: fullSha(JSON.stringify(answer)) }; }],
    ["Jev hash changed", recoveryRoutes[2], (saved) => ({ ...saved, answer_sha256: "0".repeat(64) })],
    ["Jev results is not an array", recoveryRoutes[2], (saved) => { const answer = { results: {} }; return { ...saved, answer, answer_sha256: fullSha(JSON.stringify(answer)) }; }],
  ];
  for (const [name, spec, change] of cases) {
    await t.test(name, async () => {
      const failed = await failedConfirmation(spec);
      replaceCandidates(failed, change(JSON.parse(failed.confirmed)));
      const staged = readFileSync(failed.staged);
      await assert.rejects(spec.invoke(openSpeechJournal(failed.dir, { processAlive: () => false }), failed.send), held());
      assert.equal(failed.calls(), 1);
      assert.deepEqual(readFileSync(failed.canonical), failed.sent);
      assert.deepEqual(readFileSync(failed.staged), staged);
    });
  }
});

test("missing confirmations, changed sent generation and held canonical receipts never recover or resend", async (t) => {
  const changes = {
    "no complete confirmation": (failed) => { rmSync(failed.staged); rmSync(failed.temporary); },
    "another sent generation": (failed) => writeFileSync(failed.canonical, pretty({ ...JSON.parse(failed.sent), generation: "another-generation" })),
    "canonical held": (failed) => writeFileSync(failed.canonical, pretty({ ...JSON.parse(failed.sent), status: "held", held_at: fixedRecoveryTime().toISOString(), why: "owner hold" })),
    "canonical unreadable": (failed) => writeFileSync(failed.canonical, '{"status":'),
  };
  for (const [name, change] of Object.entries(changes)) {
    await t.test(name, async () => {
      const failed = await failedConfirmation();
      change(failed);
      const canonical = readFileSync(failed.canonical);
      await assert.rejects(failed.spec.invoke(openSpeechJournal(failed.dir, { processAlive: () => false }), failed.send), held());
      assert.equal(failed.calls(), 1);
      assert.deepEqual(readFileSync(failed.canonical), canonical);
    });
  }
});

test("two different complete confirmations for the same sent generation hold instead of choosing an answer", async () => {
  const failed = await failedConfirmation(recoveryRoutes[1]);
  const original = readFileSync(failed.temporary);
  const saved = JSON.parse(failed.confirmed);
  const answer = { text: "A different complete transcript" };
  replaceCandidates(failed, { ...saved, answer, answer_sha256: fullSha(JSON.stringify(answer)) });
  writeFileSync(failed.temporary, original);
  await assert.rejects(failed.spec.invoke(openSpeechJournal(failed.dir, { processAlive: () => false }), failed.send), held());
  assert.equal(failed.calls(), 1);
  assert.deepEqual(readFileSync(failed.canonical), failed.sent);
  assert.equal(archiveSnapshot(failed.dir).size, 0);
});

test("a partial or inconsistent staged envelope holds when no complete legacy candidate exists", async (t) => {
  const changes = {
    "partial JSON": () => '{"schema_version":',
    "wrong confirmed size": (saved) => pretty({ ...saved, confirmed_bytes: saved.confirmed_bytes + 1 }),
    "wrong confirmed hash": (saved) => pretty({ ...saved, confirmed_sha256: "0".repeat(64) }),
    "wrong sent size": (saved) => pretty({ ...saved, sent_bytes: saved.sent_bytes + 1 }),
    "partial confirmed bytes": (saved) => pretty({ ...saved, confirmed_base64: Buffer.from(saved.confirmed_base64, "base64").subarray(0, 20).toString("base64") }),
  };
  for (const [name, change] of Object.entries(changes)) {
    await t.test(name, async () => {
      const failed = await failedConfirmation();
      rmSync(failed.temporary);
      writeFileSync(failed.staged, change(JSON.parse(readFileSync(failed.staged, "utf8"))));
      const staged = readFileSync(failed.staged);
      await assert.rejects(failed.spec.invoke(openSpeechJournal(failed.dir, { processAlive: () => false }), failed.send), held());
      assert.equal(failed.calls(), 1);
      assert.deepEqual(readFileSync(failed.canonical), failed.sent);
      assert.deepEqual(readFileSync(failed.staged), staged);
    });
  }
});

test("redacted ASR request identity must match the incoming clip, terms and language before recovery", async () => {
  const failed = await failedConfirmation(recoveryRoutes[1]);
  const changedSent = { ...JSON.parse(failed.sent), request: { ...JSON.parse(failed.sent).request, language: "ko" } };
  const rawSent = Buffer.from(pretty(changedSent));
  writeFileSync(failed.canonical, rawSent);
  const confirmed = { ...JSON.parse(failed.confirmed), request: changedSent.request, sent_sha256: fullSha(rawSent) };
  replaceCandidates(failed, confirmed);
  const staged = JSON.parse(readFileSync(failed.staged, "utf8"));
  writeFileSync(failed.staged, pretty({ ...staged, sent_sha256: fullSha(rawSent), sent_bytes: rawSent.length }));
  await assert.rejects(failed.spec.invoke(openSpeechJournal(failed.dir, { processAlive: () => false }), failed.send), held());
  assert.equal(failed.calls(), 1);
  assert.deepEqual(readFileSync(failed.canonical), rawSent);
  assert.equal(archiveSnapshot(failed.dir).size, 0);
});

test("archival I/O failure preserves the complete answer and a later recovery resumes without resending", async () => {
  const failed = await failedConfirmation();
  const staged = readFileSync(failed.staged);
  const temporary = readFileSync(failed.temporary);
  const interrupted = openSpeechJournal(failed.dir, {
    processAlive: () => false,
    create: (file) => {
      if (file.includes(`${path.sep}recovery${path.sep}`)) throw Object.assign(new Error("injected archive failure"), { code: "EPERM" });
      assert.ok(existsSync(file), "the canonical sent receipt already exists");
      return false;
    },
  });
  await assert.rejects(failed.spec.invoke(interrupted, failed.send));
  assert.equal(failed.calls(), 1);
  assert.deepEqual(readFileSync(failed.canonical), failed.sent);
  assert.deepEqual(readFileSync(failed.staged), staged);
  assert.deepEqual(readFileSync(failed.temporary), temporary);
  const restarted = openSpeechJournal(failed.dir, { processAlive: () => false });
  failed.spec.check(await failed.spec.invoke(restarted, failed.send));
  assert.equal(failed.calls(), 1);
});

test("recovery refuses archive directory junctions rather than writing evidence outside its journal", async (t) => {
  for (const level of ["recovery", "generation"]) {
    await t.test(level, async () => {
      const failed = await failedConfirmation();
      const outside = tempDir("speech-unrelated-archive-");
      const recovery = path.join(failed.dir, "recovery");
      const link = level === "recovery" ? recovery : path.join(recovery, fullSha(failed.sent));
      if (level === "generation") mkdirSync(recovery);
      symlinkSync(outside, link, "junction");
      const staged = readFileSync(failed.staged);
      await assert.rejects(failed.spec.invoke(openSpeechJournal(failed.dir, { processAlive: () => false }), failed.send), held());
      assert.deepEqual(readdirSync(outside), [], "no evidence is created through the archive directory link");
      assert.deepEqual(readFileSync(failed.canonical), failed.sent);
      assert.deepEqual(readFileSync(failed.staged), staged);
      assert.equal(failed.calls(), 1);
    });
  }
});

function fixtureCreateOnce(file, data) {
  try { writeFileSync(file, data, { flag: "wx" }); return true; }
  catch (error) { if (error.code === "EEXIST") return false; throw error; }
}

test("interrupted recovery after copying evidence resumes with the same immutable bytes and no new POST", async () => {
  const failed = await failedConfirmation();
  const interrupted = openSpeechJournal(failed.dir, {
    processAlive: () => false,
    create: (file, data) => {
      if (path.basename(file) === "proof.json") throw Object.assign(new Error("injected before proof commit"), { code: "EPERM" });
      return fixtureCreateOnce(file, data);
    },
  });
  await assert.rejects(failed.spec.invoke(interrupted, failed.send));
  const before = archiveSnapshot(failed.dir);
  assert.ok(before.size >= 3, "interruption happens after complete sent, confirmed and WAV evidence is copied");
  assert.ok(![...before.keys()].some((file) => path.basename(file) === "proof.json"));
  failed.spec.check(await failed.spec.invoke(openSpeechJournal(failed.dir, { processAlive: () => false }), failed.send));
  const after = archiveSnapshot(failed.dir);
  for (const [name, bytes] of before) assert.deepEqual(after.get(name), bytes, "resumption never changes earlier evidence");
  assert.equal([...after.keys()].filter((file) => path.basename(file) === "proof.json").length, 1);
  assert.equal(failed.calls(), 1);
});

test("a canonical hold created during archival prevents answer hand-out after recovery evidence is saved", async () => {
  const failed = await failedConfirmation();
  const heldBytes = Buffer.from(pretty({ ...JSON.parse(failed.sent), status: "held", held_at: fixedRecoveryTime().toISOString(), why: "owner hold while copying evidence" }));
  const restarted = openSpeechJournal(failed.dir, {
    processAlive: () => false,
    create: (file, data) => {
      if (path.basename(file) === "proof.json") writeFileSync(failed.canonical, heldBytes);
      return fixtureCreateOnce(file, data);
    },
  });
  await assert.rejects(failed.spec.invoke(restarted, failed.send), held());
  assert.deepEqual(readFileSync(failed.canonical), heldBytes, "recovery does not overwrite the newer hold");
  assert.equal(restarted.reused, 0);
  assert.equal(failed.calls(), 1);
  assert.ok(archiveSnapshot(failed.dir).size > 0, "preserved evidence cannot override canonical ownership");
});

test("recovery archive evidence does not authorize reuse after an explicit forget and new same-body retake", async () => {
  const failed = await failedConfirmation();
  const oldReader = openSpeechJournal(failed.dir, { processAlive: () => false });
  failed.spec.check(await failed.spec.invoke(oldReader, failed.send));
  const archived = archiveSnapshot(failed.dir);
  assert.equal(journalCli(["forget", "--dir", failed.dir, "--sha", failed.spec.sha], quietJournalIO), 0);
  let retakeCalls = 0;
  const different = encodeWav(tone(4800, 11));
  const retake = openSpeechJournal(failed.dir, { now: fixedRecoveryTime });
  const answer = await retake.wrap(async () => { retakeCalls += 1; return { wav: different, billable: 19 }; })(body);
  assert.deepEqual(answer.wav, different);
  assert.equal(retakeCalls, 1, "the requested retake buys its own answer despite matching body and timestamp");
  const newCanonical = readFileSync(failed.canonical);
  assert.ok(!existsSync(failed.staged), "successful canonical confirmation retires its staged receipt");
  oldReader.release();
  assert.deepEqual(readFileSync(failed.canonical), newCanonical, "the stale reader cannot release a newer generation");
  assert.deepEqual(readFileSync(path.join(failed.dir, `${failed.spec.sha}.wav`)), different, "the stale reader cannot delete the newer answer");
  assert.ok(!existsSync(failed.staged));
  assert.deepEqual(archiveSnapshot(failed.dir), archived, "old immutable evidence remains available");
  assert.equal(failed.calls(), 1);
});

test("successful confirmation cleanup cannot unlink a newer same-body generation's staged answer", async () => {
  const dir = journalIn();
  const sha = requestSha256(body);
  const canonical = path.join(dir, `${sha}.json`);
  const staged = path.join(dir, `${sha}.answer.json`);
  const wavFile = path.join(dir, `${sha}.wav`);
  const newerWav = encodeWav(tone(4800, 11));
  let newerSentBytes;
  let newerStageBytes;
  let calls = 0;
  const journal = openSpeechJournal(dir, {
    now: fixedRecoveryTime,
    write(file, data) {
      atomicWrite(file, data);
      if (file !== canonical || JSON.parse(String(data)).status !== "confirmed") return;
      // Model another owner's explicit same-body retake at the boundary between the old
      // canonical confirmation and its local staged-receipt cleanup. No second sender runs.
      const confirmed = JSON.parse(String(data));
      const newerSent = { ...confirmed, status: "sent", generation: "37eec85f-88b0-4b8b-9ce7-de5dfe017234", sent_at: "2026-10-08T00:00:01.000Z" };
      for (const field of ["confirmed_at", "sent_sha256", "wav_sha256", "wav_bytes", "billable"]) delete newerSent[field];
      newerSentBytes = Buffer.from(pretty(newerSent));
      const newerConfirmedBytes = Buffer.from(pretty({ ...newerSent, status: "confirmed", confirmed_at: "2026-10-08T00:00:02.000Z",
        sent_sha256: fullSha(newerSentBytes), wav_sha256: fullSha(newerWav), wav_bytes: newerWav.length, billable: 19 }));
      newerStageBytes = Buffer.from(pretty({ schema_version: 1, sent_sha256: fullSha(newerSentBytes), sent_bytes: newerSentBytes.length,
        confirmed_sha256: fullSha(newerConfirmedBytes), confirmed_bytes: newerConfirmedBytes.length, confirmed_base64: newerConfirmedBytes.toString("base64") }));
      writeFileSync(canonical, newerSentBytes);
      writeFileSync(staged, newerStageBytes);
      writeFileSync(wavFile, newerWav);
    },
  });
  const answer = await journal.wrap(async () => { calls += 1; return { wav: recoveryAudio, billable: 37 }; })(body);
  assert.deepEqual(answer.wav, recoveryAudio, "the old caller receives only its own answer");
  assert.equal(calls, 1);
  assert.deepEqual(readFileSync(canonical), newerSentBytes);
  assert.deepEqual(readFileSync(staged), newerStageBytes, "cleanup leaves the newer complete staged answer intact");
  assert.deepEqual(readFileSync(wavFile), newerWav);
  journal.release();
  assert.deepEqual(readFileSync(canonical), newerSentBytes, "the old caller cannot release the newer sent receipt");
  assert.deepEqual(readFileSync(staged), newerStageBytes);
  assert.deepEqual(readFileSync(wavFile), newerWav);
});

test("independent recovery readers share one immutable proof without issuing a provider request", async () => {
  const failed = await failedConfirmation();
  const readers = Array.from({ length: 4 }, () => openSpeechJournal(failed.dir, { processAlive: () => false }));
  const answers = await Promise.all(readers.map((reader) => failed.spec.invoke(reader, failed.send)));
  for (const answer of answers) failed.spec.check(answer);
  assert.deepEqual(readers.map((reader) => reader.reused), [1, 1, 1, 1]);
  assert.equal(failed.calls(), 1);
  const archived = archiveSnapshot(failed.dir);
  assert.equal([...archived.keys()].filter((file) => path.basename(file) === "proof.json").length, 1);
  assert.deepEqual(readFileSync(failed.canonical), failed.sent);
});

test("legacy confirmed temporary answers recover only with exact original sent bytes and a dead filename PID", async (t) => {
  for (const producer of [false, true, null]) {
    await t.test(String(producer), async () => {
      const dir = journalIn();
      mkdirSync(dir, { recursive: true });
      const sha = requestSha256(body);
      const sent = { schema_version: 1, path: "speech", request_sha256: sha, request: body, status: "sent", sent_at: "2026-10-05T03:00:00.000Z" };
      const canonical = path.join(dir, `${sha}.json`);
      const temporary = `${canonical}.987654.tmp`;
      writeFileSync(canonical, pretty(sent));
      writeFileSync(path.join(dir, `${sha}.wav`), recoveryAudio);
      writeFileSync(temporary, pretty({ ...sent, status: "confirmed", confirmed_at: "2026-10-05T03:00:01.000Z", wav_sha256: fullSha(recoveryAudio), wav_bytes: recoveryAudio.length, billable: 37 }));
      const originalSent = readFileSync(canonical);
      const originalTemp = readFileSync(temporary);
      let calls = 0;
      const restarted = openSpeechJournal(dir, { processAlive: (pid) => { assert.equal(pid, 987654); return producer; } });
      const invoke = () => restarted.wrap(async () => { calls += 1; assert.fail("legacy recovery never calls the provider"); })(body);
      if (producer === false) recoveryRoutes[0].check(await invoke());
      else await assert.rejects(invoke(), held());
      assert.equal(calls, 0);
      assert.deepEqual(readFileSync(canonical), originalSent);
      assert.deepEqual(readFileSync(temporary), originalTemp);
    });
  }
});
