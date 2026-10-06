// check-audio's transcriptions and Jev judgements through the speech journal (speech-journal.mjs),
// with the real client (client.mjs) and an injected counting fetch: nothing here reaches a live,
// paid endpoint. check.test.mjs and batch-recovery.test.mjs keep the check's own behaviour.
import assert from "node:assert/strict";
import { mkdirSync, readdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { EXIT, main } from "../cli.mjs";
import { fixture, sandbox, tempDir } from "../core/fixtures/load.mjs";
import { eachLine } from "../core/schema.mjs";
import { ARTIFACTS } from "../core/state.mjs";
import { SAMPLE_RATE } from "../core/timeline.mjs";
import { judgeLines, SPEECH_UNCERTAIN, SpeechError, transcribeClip } from "./client.mjs";
import { JOURNAL_DIR, judgeBody, listSpeechJournal, main as journalCli, openSpeechJournal, requestSha256, transcribeBody } from "./speech-journal.mjs";
import { concatSamples, encodeWav } from "./wav.mjs";

// The fixture videos run seconds; the eight-minute floor has tests of its own.
process.env.VIDEO_MIN_EPISODE_MINUTES ??= "0";

const TOKEN = `mkv_${"c".repeat(43)}`;
const SITE = "https://mokaair.test";
const tone = (samples, pitch = 7) => Int16Array.from({ length: samples }, (_, index) => Math.round(8000 * Math.sin(index / pitch)));
const clip = (pitch = 7) => encodeWav(tone(8000, pitch), 16_000);
const lost = () => Object.assign(new TypeError("fetch failed"), { cause: Object.assign(new Error("socket hang up"), { code: "ECONNRESET" }) });
const problem = (status, code) => new Response(JSON.stringify({ code, detail: code }), { status, headers: { "Content-Type": "application/json" } });
const brokenJson = (text) => () => new Response(text, { status: 200, headers: { "Content-Type": "application/json" } });
const held = (pattern = /./) => (error) => error instanceof SpeechError && error.code === SPEECH_UNCERTAIN && error.who === "owner" && pattern.test(error.message) && error.message.includes(SPEECH_UNCERTAIN);
const QUESTIONS = [
  { id: "a1b2", intended: "一張手寫的發票", spoken_form: "一張手寫的發票", heard: "一張收寫的發票" },
  { id: "c3d4", intended: "再扣掉三十元的折價券", spoken_form: "再扣掉三十元的折價券", heard: "再扣掉三十元的這價券" },
];

/** The site's transcriber and Jev, counting their paid POSTs; `answers` are used in turn, then a fresh answer per body. */
function listener(answers = []) {
  const posts = { transcribe: [], judge: [] };
  const fetchImpl = async (url, init) => {
    const route = url.endsWith("/api/video/speech/transcribe") ? "transcribe" : url.endsWith("/api/video/speech/judge") ? "judge" : null;
    assert.ok(route, `unexpected request: ${url}`);
    const body = JSON.parse(init.body);
    posts[route].push(body);
    const answer = answers.shift();
    if (typeof answer === "function") return answer(body);
    if (answer) return answer;
    // A transcript per call, so a second purchase reads differently from the first.
    if (route === "transcribe") return Response.json({ text: `第 ${posts.transcribe.length} 次聽到的話` });
    return Response.json({ results: body.lines.map((line, index) => ({ id: line.id, noul: 0.5 + index / 10 + posts.judge.length / 100 })) });
  };
  return { posts, fetchImpl };
}

const options = (server) => ({ site: SITE, token: TOKEN, fetchImpl: server.fetchImpl, sleep: async () => {} });
const journalIn = () => path.join(tempDir("check-journal-"), JOURNAL_DIR);
const opened = (dir, server) => {
  const journal = openSpeechJournal(dir, { now: () => new Date("2026-10-06T01:00:00Z") });
  const transcribe = journal.wrapTranscribe(transcribeClip);
  const judge = journal.wrapJudge(judgeLines);
  return { journal, transcribe: (args) => transcribe({ ...options(server), ...args }), judge: (args) => judge({ ...options(server), ...args }) };
};
const entry = (dir, sha) => JSON.parse(readFileSync(path.join(dir, `${sha}.json`), "utf8"));
const silent = { stdout: { write() {} }, stderr: { write() {} } };

test("the journal names a transcription and a Jev call by the sha256 the client gives the same request", async () => {
  const never = { site: SITE, token: TOKEN, fetchImpl: async () => { throw lost(); }, sleep: async () => {} };
  const variants = [
    { wav: clip(), terms: [], language: "zh-TW" },
    { wav: clip(), terms: ["Go", "GPT-5.5"], language: "zh-TW" },
    { wav: clip(9), terms: ["API"], language: "en" },
    { wav: clip(), terms: [], language: "ja" },
  ];
  for (const variant of variants) {
    const error = await transcribeClip({ ...never, ...variant }).catch((caught) => caught);
    assert.equal(error.code, SPEECH_UNCERTAIN);
    assert.equal(error.requestSha256, requestSha256(transcribeBody(variant)), JSON.stringify(variant.terms));
    const journaled = await openSpeechJournal(journalIn()).wrapTranscribe(transcribeClip)({ ...never, ...variant }).catch((caught) => caught);
    assert.ok(held(/POST \/api\/video\/speech\/transcribe was sent/)(journaled), journaled.message);
    assert.equal(journaled.requestSha256, error.requestSha256);
    assert.equal(journaled.path, "speech/transcribe");
  }
  assert.deepEqual(Object.keys(transcribeBody({ wav: clip() })), ["audio"], "the narration's default language and no terms add no field");
  for (const language of ["zh-TW", "ko"]) {
    const error = await judgeLines({ ...never, lines: QUESTIONS, language }).catch((caught) => caught);
    assert.equal(error.requestSha256, requestSha256(judgeBody({ lines: QUESTIONS, language })), language);
    const journaled = await openSpeechJournal(journalIn()).wrapJudge(judgeLines)({ ...never, lines: QUESTIONS, language }).catch((caught) => caught);
    assert.ok(held(/POST \/api\/video\/speech\/judge was sent/)(journaled), journaled.message);
    assert.equal(journaled.requestSha256, error.requestSha256);
  }
});

test("a transcript or Jev answer that came back is taken from disk after a restart, bound to its exact body", async () => {
  const dir = journalIn();
  const server = listener([() => Response.json({ results: [{ id: "a1b2", noul: 0.25 }, { id: "c3d4" }] })]);
  const first = opened(dir, server);
  // The first POST is Jev's, whose second answer has no probability: the client reads NaN.
  const verdicts = await first.judge({ lines: QUESTIONS });
  assert.deepEqual([...verdicts], [["a1b2", 0.25], ["c3d4", NaN]]);
  const text = await first.transcribe({ wav: clip(), terms: ["Go"] });
  assert.deepEqual([server.posts.transcribe.length, server.posts.judge.length], [1, 1]);

  const saved = entry(dir, requestSha256(transcribeBody({ wav: clip(), terms: ["Go"] })));
  assert.equal(saved.status, "confirmed");
  assert.equal(saved.path, "speech/transcribe");
  assert.deepEqual(saved.answer, { text });
  assert.equal(saved.request.audio, undefined, "the entry keeps the clip's sha256, not its audio");
  assert.deepEqual([saved.request.audio_bytes, saved.request.terms, saved.request.language], [clip().length, ["Go"], undefined]);
  assert.match(saved.request.audio_sha256, /^[0-9a-f]{64}$/);
  assert.equal(entry(dir, requestSha256(judgeBody({ lines: QUESTIONS }))).request.lines.length, 2);

  // The run stops before saving what it made of the answers: the next one reads them from disk.
  const restart = openSpeechJournal(dir);
  assert.equal(await restart.wrapTranscribe(async () => assert.fail("a confirmed transcript is not bought again"))({ wav: clip(), terms: ["Go"] }), text);
  assert.deepEqual([...(await restart.wrapJudge(async () => assert.fail("a confirmed verdict is not bought again"))({ lines: QUESTIONS }))], [...verdicts]);
  assert.equal(restart.reused, 2);

  // Another clip, other terms, another language or other lines is another request.
  const changed = opened(dir, server);
  const answers = [
    await changed.transcribe({ wav: clip(9), terms: ["Go"] }),
    await changed.transcribe({ wav: clip(), terms: [] }),
    await changed.transcribe({ wav: clip(), terms: ["Go", "AI"] }),
    await changed.transcribe({ wav: clip(), terms: ["Go"], language: "en" }),
  ];
  assert.equal(server.posts.transcribe.length, 5);
  assert.ok(answers.every((answer) => answer !== text));
  await changed.judge({ lines: QUESTIONS.slice(0, 1) });
  await changed.judge({ lines: [{ ...QUESTIONS[0], heard: "一張手寫的發票" }, QUESTIONS[1]] });
  await changed.judge({ lines: QUESTIONS, language: "ja" });
  assert.equal(server.posts.judge.length, 4);
  assert.equal(changed.journal.reused, 0);

  // Once the caller has saved them, the same request is bought again.
  restart.release();
  changed.journal.release();
  assert.deepEqual(readdirSync(dir), []);
  assert.notEqual(await opened(dir, server).transcribe({ wav: clip(), terms: ["Go"] }), text);
  assert.equal(server.posts.transcribe.length, 6);
});

test("a transcription or Jev call whose answer was lost or broke is held, and not sent again until a person forgets it", async (t) => {
  const cases = {
    "a lost transcription": { route: "transcribe", answer: () => { throw lost(); } },
    "a transcript that breaks off": { route: "transcribe", answer: () => new Response(new ReadableStream({ start(controller) { controller.error(new Error("terminated")); } }), { status: 200 }) },
    "a transcript that is not JSON": { route: "transcribe", answer: brokenJson('{"text":') },
    "the web route's lost transcript": { route: "transcribe", answer: () => problem(504, "video_speech_answer_lost") },
    "a lost Jev call": { route: "judge", answer: () => { throw lost(); } },
    "a Jev answer that is not JSON": { route: "judge", answer: brokenJson('{"results":[') },
    "a Jev call the API could not settle": { route: "judge", answer: () => problem(500, "") },
  };
  for (const [what, { route, answer }] of Object.entries(cases)) {
    await t.test(what, async () => {
      const dir = journalIn();
      const server = listener([answer]);
      const ask = (journal) => (route === "transcribe" ? journal.transcribe({ wav: clip(), terms: ["Go"] }) : journal.judge({ lines: QUESTIONS }));
      const sha = requestSha256(route === "transcribe" ? transcribeBody({ wav: clip(), terms: ["Go"] }) : judgeBody({ lines: QUESTIONS }));
      await assert.rejects(ask(opened(dir, server)), (error) => held(new RegExp(`^POST /api/video/speech/${route} was sent and no usable answer came back`))(error) && error.requestSha256 === sha && error.message.includes(`forget --dir "${dir}" --sha ${sha}`));
      assert.equal(server.posts[route].length, 1, "the client did not resend it");
      assert.equal(entry(dir, sha).status, "held");
      await assert.rejects(ask(opened(dir, server)), held(/is held in the speech journal since 2026-10-06T01:00:00.000Z/));
      assert.equal(server.posts[route].length, 1, "a restart sends nothing");

      const out = { stdout: "", stderr: "" };
      assert.equal(journalCli(["list", "--dir", dir], { stdout: { write: (text) => (out.stdout += text) }, stderr: silent.stderr }), 0);
      const about = route === "transcribe" ? `speech/transcribe ${clip().length} bytes of audio, terms Go` : "speech/judge 2 lines a1b2, c3d4";
      assert.ok(out.stdout.startsWith(`${sha} held 2026-10-06T01:00:00.000Z ${about} (no usable answer came back`), out.stdout);
      assert.match(out.stdout, /1 held: check the provider's usage/);
      assert.equal(journalCli(["forget", "--dir", dir, "--sha", sha], silent), 0);
      await ask(opened(dir, server));
      assert.equal(server.posts[route].length, 2, "after forget it is sent once more");
    });
  }
});

test("a run that stopped while its transcription or Jev call was out leaves a hold the next run respects", async () => {
  const dir = journalIn();
  // The process dies while both requests are out: no answer is ever recorded.
  openSpeechJournal(dir).wrapTranscribe(() => new Promise(() => {}))({ wav: clip(), terms: ["Go"] });
  openSpeechJournal(dir).wrapJudge(() => new Promise(() => {}))({ lines: QUESTIONS });
  await new Promise((resolve) => setImmediate(resolve));
  assert.deepEqual(listSpeechJournal(dir).map((item) => [item.path, item.status]).sort(), [["speech/judge", "sent"], ["speech/transcribe", "sent"]]);
  const server = listener();
  const next = opened(dir, server);
  await assert.rejects(next.transcribe({ wav: clip(), terms: ["Go"] }), held(/^POST \/api\/video\/speech\/transcribe was sent at .* by a run that recorded no answer/));
  await assert.rejects(next.judge({ lines: QUESTIONS }), held(/^POST \/api\/video\/speech\/judge was sent at .* by a run that recorded no answer/));
  assert.deepEqual([server.posts.transcribe.length, server.posts.judge.length], [0, 0]);
});

test("a transcription or Jev call the API settled leaves nothing behind, so the next run may send it", async (t) => {
  const cases = {
    "a transcriber that stays busy": { route: "transcribe", answers: Array.from({ length: 5 }, () => () => problem(503, "video_speech_upstream_busy")), posts: 5, who: "service" },
    "a spent Jev day": { route: "judge", answers: [() => problem(429, "jev_budget_exhausted")], posts: 1, who: "service" },
    "a revoked token": { route: "transcribe", answers: [() => problem(401, "video_tool_token_invalid")], posts: 1, who: "owner" },
  };
  for (const [what, { route, answers, posts, who }] of Object.entries(cases)) {
    await t.test(what, async () => {
      const dir = journalIn();
      const server = listener([...answers]);
      const ask = (journal) => (route === "transcribe" ? journal.transcribe({ wav: clip() }) : journal.judge({ lines: QUESTIONS }));
      await assert.rejects(ask(opened(dir, server)), (error) => error instanceof SpeechError && error.code !== SPEECH_UNCERTAIN && error.who === who);
      assert.equal(server.posts[route].length, posts);
      assert.deepEqual(readdirSync(dir), []);
      await ask(opened(dir, server));
      assert.equal(server.posts[route].length, posts + 1);
    });
  }
});

test("a transcript or verdict changed on disk holds instead of being trusted or bought again", async () => {
  const dir = journalIn();
  const server = listener();
  const first = opened(dir, server);
  await first.transcribe({ wav: clip() });
  await first.judge({ lines: QUESTIONS });
  for (const body of [transcribeBody({ wav: clip() }), judgeBody({ lines: QUESTIONS })]) {
    const file = path.join(dir, `${requestSha256(body)}.json`);
    const edited = JSON.parse(readFileSync(file, "utf8"));
    edited.answer = body.lines ? { results: [{ id: "a1b2", noul: 0.99 }, { id: "c3d4", noul: 0.99 }] } : { text: "一張手寫的發票" };
    writeFileSync(file, JSON.stringify(edited));
  }
  const restart = opened(dir, server);
  await assert.rejects(restart.transcribe({ wav: clip() }), held(/missing or changed on disk/));
  await assert.rejects(restart.judge({ lines: QUESTIONS }), held(/missing or changed on disk/));
  assert.deepEqual([server.posts.transcribe.length, server.posts.judge.length], [1, 1]);
  assert.deepEqual(listSpeechJournal(dir).map((item) => [item.path, item.status]).sort(), [["speech/judge", "held"], ["speech/transcribe", "held"]]);
});

// --- check-audio -------------------------------------------------------------------------------

/**
 * A site that synthesizes tones, hears every clip as something the script does not say (so each
 * line goes to Jev, which passes it), and counts its paid POSTs. `transcribe` and `judge` answer
 * those routes in turn first; a function may throw.
 */
function site({ transcribe = [], judge = [] } = {}) {
  const posts = { speech: 0, transcribe: [], judge: [] };
  const fetchImpl = async (url, init) => {
    if (url.endsWith("/speech/status")) {
      return Response.json({ configured: true, region: "eastasia", voices: ["zh-TW-HsiaoChenNeural"], output_format: "riff-48khz-16bit-mono-pcm", max_request_characters: 1500, monthly_limit: 0, used: 0, remaining: null });
    }
    const body = JSON.parse(init.body);
    if (url.endsWith("/speech/transcribe")) {
      posts.transcribe.push(body);
      const answer = transcribe.shift();
      return answer ? answer(body) : Response.json({ text: `第 ${posts.transcribe.length} 次聽到的話` });
    }
    if (url.endsWith("/speech/judge")) {
      posts.judge.push(body);
      const answer = judge.shift();
      return answer ? answer(body) : Response.json({ results: body.lines.map((line) => ({ id: line.id, noul: 0.95 })) });
    }
    // A site from before speech/align: tts asks it first for an Azure voice and is refused, unpaid.
    if (url.endsWith("/speech/align")) return new Response("not found", { status: 404 });
    posts.speech += 1;
    // 200 ms a character, the voices' pace: the fixture's chapters then run the 10 s tts requires.
    const audio = concatSamples(body.segments.flatMap((segment) => [
      tone(Math.round(segment.parts.reduce((sum, part) => sum + part.text.length, 0) * 0.2 * SAMPLE_RATE)),
      new Int16Array(Math.round((segment.break_after_ms / 1000) * SAMPLE_RATE)),
    ]));
    return new Response(encodeWav(audio), { status: 200, headers: { "Content-Type": "audio/wav", "X-Billable-Characters": "10" } });
  };
  return { posts, fetchImpl, queue: { transcribe, judge } };
}

function context(box, fetchImpl) {
  const out = { stdout: "", stderr: "" };
  return {
    out,
    ctx: {
      root: box.root,
      env: { VIDEO_WORKDIR: box.work, MOKAAIR_VIDEO_TOKEN: TOKEN },
      home: box.base,
      fetch: fetchImpl,
      stdout: { write: (text) => (out.stdout += text) },
      stderr: { write: (text) => (out.stderr += text) },
      now: () => new Date("2026-10-06T01:00:00Z"),
      sleep: async () => {},
    },
  };
}

async function narrated(server) {
  const box = sandbox();
  const synth = context(box, server.fetchImpl);
  assert.equal(await main(["tts", "--slug", box.slug], synth.ctx), EXIT.ok, synth.out.stderr);
  const lines = [...eachLine(fixture())].map(({ line }) => line);
  assert.ok(lines.length >= 3 && lines.length <= 40, "the fixture's lines fit one Jev call");
  const check = async (...flags) => {
    const run = context(box, server.fetchImpl);
    return { code: await main(["check-audio", "--slug", box.slug, ...flags], run.ctx), ...run.out };
  };
  return { box, lines, check, journal: path.join(box.workdir, ARTIFACTS.audio, JOURNAL_DIR), cacheFile: path.join(box.workdir, "review", "check.json") };
}

const forgetFrom = (stderr) => {
  const [, dir, sha] = stderr.match(/forget --dir "([^"]+)" --sha ([0-9a-f]{64})/) ?? [];
  assert.ok(dir && sha, stderr);
  assert.equal(journalCli(["forget", "--dir", dir, "--sha", sha], silent), 0);
  return dir;
};
const readJsonFile = (file) => JSON.parse(readFileSync(file, "utf8"));
// atomicWrite's temporary file for `file` in this process: a directory there makes the write fail.
const blockWrite = (file) => mkdirSync(`${file}.${process.pid}.tmp`, { recursive: true });
const unblockWrite = (file) => rmSync(`${file}.${process.pid}.tmp`, { recursive: true, force: true });

test("check-audio holds a transcription whose answer was lost until a person forgets it, then finishes", async () => {
  const server = site({ transcribe: [() => { throw lost(); }] });
  const { lines, check, journal, cacheFile } = await narrated(server);

  const lostRun = await check();
  assert.equal(lostRun.code, EXIT.owner, lostRun.stderr);
  const last = lostRun.stderr.trim().split("\n").at(-1);
  assert.match(last, /^POST \/api\/video\/speech\/transcribe was sent and no usable answer came back \(socket hang up\)/);
  assert.ok(last.includes(SPEECH_UNCERTAIN), "the worker reads the code from the last line");
  assert.equal(server.posts.transcribe.length, 1);

  const rerun = await check();
  assert.equal(rerun.code, EXIT.owner);
  assert.match(rerun.stderr, /speech\/transcribe is held in the speech journal since 2026-10-06T01:00:00.000Z/);
  assert.equal(server.posts.transcribe.length, 1, "the rerun does not send it again");
  assert.equal(forgetFrom(rerun.stderr), journal);

  const done = await check();
  assert.equal(done.code, EXIT.ok, done.stdout + done.stderr);
  assert.equal(server.posts.transcribe.length, 1 + lines.length);
  assert.match(done.stdout, new RegExp(`${lines.length} clips transcribed now, 1 Jev calls`));
  assert.doesNotMatch(done.stdout, /came from the speech journal/);
  assert.deepEqual(readdirSync(journal), [], "released once check.json holds the transcripts and verdicts");

  // The cache answers as before: nothing is sent, and the journal stays empty.
  const cached = await check();
  assert.equal(cached.code, EXIT.ok);
  assert.deepEqual([server.posts.transcribe.length, server.posts.judge.length], [1 + lines.length, 1]);
  assert.deepEqual(readdirSync(journal), []);
  assert.ok(Object.values(readJsonFile(cacheFile).lines).every((line) => line.noul === 0.95));
});

test("check-audio takes a transcript that came back before check.json was written from the journal", async () => {
  const server = site();
  const { lines, check, journal, cacheFile } = await narrated(server);
  blockWrite(cacheFile);
  await assert.rejects(check(), "the first cache write fails after the first transcript was bought");
  unblockWrite(cacheFile);
  assert.equal(server.posts.transcribe.length, 1);
  const [kept] = listSpeechJournal(journal);
  assert.deepEqual([kept.path, kept.status], ["speech/transcribe", "confirmed"]);

  const resumed = await check();
  assert.equal(resumed.code, EXIT.ok, resumed.stdout + resumed.stderr);
  assert.equal(server.posts.transcribe.length, lines.length, "the kept transcript is not bought again");
  assert.match(resumed.stdout, new RegExp(`${lines.length - 1} clips transcribed now, 1 Jev calls`));
  assert.match(resumed.stdout, /1 answers paid for by an earlier run came from the speech journal, not bought again/);
  assert.equal(readJsonFile(cacheFile).lines[lines[0].id].heard, "第 1 次聽到的話");
  assert.deepEqual(readdirSync(journal), []);
});

test("check-audio holds a Jev call whose answer broke, and reuses one that came back before it was saved", async () => {
  const server = site({ judge: [brokenJson('{"results":[')] });
  const { lines, check, journal, cacheFile } = await narrated(server);
  const brokenRun = await check();
  assert.equal(brokenRun.code, EXIT.owner, brokenRun.stderr);
  assert.match(brokenRun.stderr.trim().split("\n").at(-1), new RegExp(`^POST /api/video/speech/judge was sent and no usable answer came back \\(the answer could not be read: .*${SPEECH_UNCERTAIN}`));
  assert.deepEqual([server.posts.transcribe.length, server.posts.judge.length], [lines.length, 1]);
  assert.ok(Object.values(readJsonFile(cacheFile).lines).every((line) => line.noul === null), "the transcripts are kept, no verdict is");

  const rerun = await check();
  assert.equal(rerun.code, EXIT.owner);
  assert.deepEqual([server.posts.transcribe.length, server.posts.judge.length], [lines.length, 1], "neither is sent again");
  forgetFrom(rerun.stderr);

  // Jev answers this time, doubting one line, and the run stops before writing the verdicts.
  const doubted = lines[1].id;
  server.queue.judge.push((body) => {
    blockWrite(cacheFile);
    return Response.json({ results: body.lines.map((line) => ({ id: line.id, noul: line.id === doubted ? 0.1 : 0.95 })) });
  });
  await assert.rejects(check(), "the cache write after the Jev call fails");
  unblockWrite(cacheFile);
  assert.equal(server.posts.judge.length, 2);
  assert.deepEqual(listSpeechJournal(journal).map((item) => [item.path, item.status]), [["speech/judge", "confirmed"]]);

  const resumed = await check();
  assert.equal(resumed.code, EXIT.lint, resumed.stdout + resumed.stderr);
  assert.deepEqual([server.posts.transcribe.length, server.posts.judge.length], [lines.length, 2], "the verdicts are not bought again");
  assert.match(resumed.stdout, /0 clips transcribed now, 0 Jev calls/);
  assert.match(resumed.stdout, /1 answers paid for by an earlier run came from the speech journal/);
  assert.deepEqual(readJsonFile(path.join(path.dirname(cacheFile), "check-flags.json")).flags, [doubted]);
  assert.deepEqual(readdirSync(journal), []);
});
