// The speech journal (speech-journal.mjs) with the real client (client.mjs) and an injected
// counting fetch: nothing here reaches a live, paid endpoint.
import assert from "node:assert/strict";
import { copyFileSync, existsSync, mkdirSync, readdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { EXIT, main as cli } from "../cli.mjs";
import { fixture, sandbox, tempDir } from "../core/fixtures/load.mjs";
import { eachLine, textHash } from "../core/schema.mjs";
import { ARTIFACTS, loadProject } from "../core/state.mjs";
import { serverNarration, phraseBody } from "../shorts/speech.mjs";
import { SPEECH_UNCERTAIN, SpeechError, synthesize } from "./client.mjs";
import { planRequests } from "./requests.mjs";
import { JOURNAL_DIR, listSpeechJournal, main as journalCli, openSpeechJournal, requestSha256 } from "./speech-journal.mjs";
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
  assert.match(out.stdout, /1 held/);
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
  await assert.rejects(serverNarration({ phrases, voice, cacheDir, client }), held());
  assert.equal(server.posts.length, 1);
  await assert.rejects(serverNarration({ phrases, voice, cacheDir, client }), held(/held in the speech journal/));
  assert.equal(server.posts.length, 1, "the next build or lab round does not send it again");
  const [held1] = listSpeechJournal(path.join(cacheDir, JOURNAL_DIR));
  assert.equal(held1.sha, requestSha256(phraseBody(voice, phrases[0])));
  assert.equal(journalCli(["forget", "--dir", path.join(cacheDir, JOURNAL_DIR), "--sha", held1.sha], { stdout: { write() {} }, stderr: { write() {} } }), 0);

  // The second phrase was bought by a build that stopped before caching it.
  const bought = await openSpeechJournal(path.join(cacheDir, JOURNAL_DIR)).wrap((sent) => synthesize({ ...options(server), body: sent }))(phraseBody(voice, phrases[1]));
  const posts = server.posts.length;
  const built = await serverNarration({ phrases, voice, cacheDir, client });
  assert.equal(server.posts.length, posts + 1, "only the first phrase is bought");
  assert.deepEqual([built.calls, built.characters], [1, 10], "the reused phrase is not counted as this build's");
  assert.deepEqual(built.clips[1], bought.wav);
  assert.deepEqual(readdirSync(path.join(cacheDir, JOURNAL_DIR)), []);
  assert.ok(existsSync(cacheDir));
});
