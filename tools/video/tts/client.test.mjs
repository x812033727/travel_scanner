import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import test from "node:test";
import path from "node:path";
import { tempDir } from "../core/fixtures/load.mjs";
import { alignClip, judgeLines, MAX_RETRY_WAIT_MS, RATE_WINDOW_MS, SPEECH_UNCERTAIN, SpeechError, speechStatus, synthesize, synthesizeAligned, transcribeClip } from "./client.mjs";
import { listSpeechJournal, openSpeechJournal, requestSha256 } from "./speech-journal.mjs";
import { encodeWav, parseWav } from "./wav.mjs";

const SITE = "https://site.test";
const TOKEN = `mkv_${"t".repeat(43)}`;
const sha256 = (text) => createHash("sha256").update(text).digest("hex");
const audio = () => encodeWav(Int16Array.from({ length: 4800 }, (_, i) => Math.round(Math.sin(i / 8) * 3000)));
// What Node's fetch throws: a TypeError whose cause carries the socket's code.
const failed = (code) => Object.assign(new TypeError("fetch failed"), { cause: Object.assign(new Error(`socket ${code}`), { code }) });
const problem = (status, code, headers = {}) => Response.json({ code, detail: `${code} detail` }, { status, headers });
// A 200 whose body breaks off after its first bytes, the way a dropped connection ends a download.
const brokenBody = () =>
  new Response(new ReadableStream({ start(controller) { controller.enqueue(new Uint8Array([82, 73, 70])); controller.error(new TypeError("terminated")); } }), { status: 200 });

// One of each paid request, and the answer a working server gives it.
const PAID = [
  {
    name: "synthesize",
    path: "speech",
    send: (options) => synthesize({ ...options, body: { voice: "zh-TW-HsiaoChenNeural", segments: [{ parts: [{ text: "好" }], break_after_ms: 0 }] } }),
    ok: () => new Response(audio(), { status: 200, headers: { "Content-Type": "audio/wav", "X-Billable-Characters": "37" } }),
    check: (result) => {
      assert.deepEqual(Buffer.from(result.wav), audio());
      assert.equal(result.billable, 37);
    },
  },
  {
    name: "transcribeClip",
    path: "speech/transcribe",
    send: (options) => transcribeClip({ ...options, wav: audio(), terms: ["Jev"] }),
    ok: () => Response.json({ text: "好" }),
    check: (result) => assert.equal(result, "好"),
  },
  {
    name: "judgeLines",
    path: "speech/judge",
    send: (options) => judgeLines({ ...options, lines: [{ id: "a1", intended: "好", spoken_form: "好", heard: "號" }] }),
    ok: () => Response.json({ results: [{ id: "a1", noul: 0.9 }] }),
    check: (result) => assert.deepEqual([...result], [["a1", 0.9]]),
  },
  {
    // An Azure voice synthesized with its word boundaries: paid like `synthesize`.
    name: "synthesizeAligned",
    path: "speech/align",
    send: (options) => synthesizeAligned({ ...options, body: { voice: "zh-TW-HsiaoChenNeural", segments: [{ parts: [{ text: "好" }], break_after_ms: 0 }] } }),
    ok: () => Response.json({ source: "azure", model: "zh-TW-HsiaoChenNeural", chars: [{ text: "好", start_ms: 10, end_ms: 200 }], audio: audio().toString("base64"), billable_characters: 37 }),
    check: (result) => {
      assert.deepEqual(Buffer.from(result.wav), audio());
      assert.equal(result.billable, 37);
      assert.deepEqual(result.timing, { source: "azure", model: "zh-TW-HsiaoChenNeural", chars: [{ text: "好", start_ms: 10, end_ms: 200 }] });
    },
  },
];

/** A counting server that plays `answers` in order (each returns a Response or throws). */
function server(answers) {
  const calls = [];
  const sleeps = [];
  const options = {
    site: SITE,
    token: TOKEN,
    fetchImpl: async (url, init) => {
      calls.push({ url, method: init.method, body: init.body });
      const answer = answers[Math.min(calls.length, answers.length) - 1];
      return answer();
    },
    sleep: async (ms) => sleeps.push(ms),
  };
  return { calls, sleeps, options };
}

test("a paid request sent and left without its answer is sent once and names the request it lost", async () => {
  const lost = [
    ["a connection reset after it went out", () => { throw failed("ECONNRESET"); }, 0],
    ["a socket closed mid-way", () => { throw failed("UND_ERR_SOCKET"); }, 0],
    ["Node's deadline for the headers", () => { throw failed("UND_ERR_HEADERS_TIMEOUT"); }, 0],
    ["a gateway's timeout page", () => new Response("<html>504 Gateway Time-out</html>", { status: 504, headers: { "Content-Type": "text/html" } }), 504],
    ["the web route's lost answer", () => problem(504, "video_speech_answer_lost"), 504],
    // The API's own answers for a provider that may have run the request and lost its answer.
    ["the API's lost provider answer", () => problem(504, "video_speech_upstream_lost"), 504],
    ["the API's uncertain Jev outcome", () => problem(502, "video_judge_outcome_uncertain"), 502],
    // Only the route's 502 says the API was never reached; no speech route answers this one.
    ["an upstream_unavailable no speech route answers", () => problem(503, "upstream_unavailable"), 503],
    ["an error without the API's code", () => Response.json({ detail: "Internal Server Error" }, { status: 500 }), 500],
    ["an error whose detail runs over lines", () => Response.json({ detail: "Internal\nServer Error\n" }, { status: 500 }), 500],
    ["an answer that breaks off", brokenBody, 200],
  ];
  for (const paid of PAID) {
    for (const [what, answer, status] of lost) {
      const label = `${paid.name}: ${what}`;
      const { calls, sleeps, options } = server([answer, paid.ok]);
      await assert.rejects(paid.send(options), (error) => {
        assert.ok(error instanceof SpeechError, label);
        assert.equal(error.code, SPEECH_UNCERTAIN, label);
        // Exit 3, with the code in the message's one line: the worker blocks the video instead of
        // trying again next round or giving a dub up.
        assert.equal(error.who, "owner", label);
        assert.equal(error.status, status, label);
        assert.equal(error.path, paid.path, label);
        assert.equal(error.requestSha256, sha256(calls[0].body), label);
        assert.match(error.message, new RegExp(`^POST /api/video/${paid.path} was sent and no usable answer came back.*not sent again \\(${SPEECH_UNCERTAIN}, request sha256 ${error.requestSha256}\\)$`), label);
        assert.doesNotMatch(error.message, /\n/, label);
        return true;
      });
      assert.equal(calls.length, 1, `${label}: sent once, not five times`);
      assert.deepEqual(sleeps, [], `${label}: no wait for a second try`);
    }
  }
});

test("a paid answer that arrives but cannot be read is not bought again", async () => {
  const unreadable = [
    [PAID[0], () => new Response("<html>not audio</html>", { status: 200, headers: { "X-Billable-Characters": "37" } })],
    [PAID[1], () => new Response("<html>a proxy page</html>", { status: 200 })],
    [PAID[2], () => Response.json(null)],
    [PAID[3], () => Response.json({ source: "azure", chars: [] })],
  ];
  for (const [paid, answer] of unreadable) {
    const { calls, options } = server([answer, paid.ok]);
    await assert.rejects(paid.send(options), (error) => error.code === SPEECH_UNCERTAIN && error.who === "owner" && /the answer could not be read/.test(error.message));
    assert.equal(calls.length, 1, paid.name);
  }
});

test("a paid request that never left, or that the API settled, is tried again and returns the answer that carried it", async () => {
  const settled = [
    ["a refused connection", () => { throw failed("ECONNREFUSED"); }, []],
    ["an unknown host", () => { throw failed("ENOTFOUND"); }, []],
    ["a DNS hiccup", () => { throw failed("EAI_AGAIN"); }, []],
    ["a connect timeout", () => { throw failed("UND_ERR_CONNECT_TIMEOUT"); }, []],
    // The route answers a lost answer with 504 video_speech_answer_lost since #1272, which the
    // production host serves, so its 502 is an API it never reached.
    ["the web route's 502 for an API it never reached", () => problem(502, "upstream_unavailable"), [1000]],
    ["the API's rate limit", () => problem(429, "rate_limit_exceeded", { "Retry-After": "3" }), [3000]],
    ["a busy provider", () => problem(503, "video_speech_upstream_busy", { "Retry-After": "7" }), [7000]],
    // A provider never reached, or one that answered a failure. A host from before the API's 504
    // video_speech_upstream_lost also answers it for a lost provider answer, resent as before.
    ["a provider failure the API answered", () => problem(502, "video_speech_upstream_failed"), [1000]],
    ["a key the provider refused", () => problem(502, "video_speech_upstream_rejected_key"), [1000]],
    ["Jev failing behind the API", () => problem(502, "video_judge_upstream_failed"), [1000]],
  ];
  for (const paid of PAID) {
    for (const [what, answer, waits] of settled) {
      const label = `${paid.name}: ${what}`;
      const { calls, sleeps, options } = server([answer, paid.ok]);
      paid.check(await paid.send(options));
      assert.equal(calls.length, 2, `${label}: tried again`);
      assert.equal(calls[1].body, calls[0].body, `${label}: the same request`);
      if (waits.length) assert.deepEqual(sleeps, waits, label);
    }
  }
});

test("a settled failure that does not clear stops after the bounded attempts", async () => {
  const down = server([() => problem(502, "video_speech_upstream_failed")]);
  await assert.rejects(PAID[1].send(down.options), (error) => error.code === "video_speech_upstream_failed" && error.who === "service");
  assert.equal(down.calls.length, 5);
  const unreached = server([() => problem(502, "upstream_unavailable")]);
  await assert.rejects(PAID[2].send(unreached.options), (error) => error.code === "upstream_unavailable" && error.who === "service");
  assert.equal(unreached.calls.length, 5);
  const offline = server([() => { throw failed("ECONNREFUSED"); }]);
  await assert.rejects(PAID[0].send(offline.options), (error) => error.code === "network" && error.who === "service");
  assert.equal(offline.calls.length, 5);
});

test("the status GET keeps every retry, a dropped connection and a lost answer included", async () => {
  const status = () => Response.json({ configured: true, voices: [] });
  for (const [what, answer] of [
    ["a connection reset", () => { throw failed("ECONNRESET"); }],
    ["the web route's 502", () => problem(502, "upstream_unavailable")],
    ["a gateway's timeout page", () => new Response("<html>504</html>", { status: 504 })],
    ["an error without the API's code", () => Response.json({ detail: "Internal Server Error" }, { status: 500 })],
  ]) {
    const { calls, options } = server([answer, status]);
    assert.deepEqual(await speechStatus(options), { configured: true, voices: [] }, what);
    assert.equal(calls.length, 2, what);
    assert.equal(calls[0].method, "GET", what);
  }
});

test("the owner's problems and a spent budget are told after one request, with their meaning kept", async () => {
  const once = [
    [PAID[0], () => problem(401, "video_tool_token_invalid"), "owner"],
    [PAID[0], () => problem(503, "video_speech_not_configured"), "owner"],
    [PAID[0], () => problem(422, "video_speech_voice_not_allowed"), "owner"],
    [PAID[0], () => problem(429, "video_speech_budget_exhausted"), "service"],
    [PAID[1], () => problem(503, "video_speech_not_configured"), "owner"],
    [PAID[2], () => problem(429, "jev_budget_exhausted"), "service"],
    [PAID[3], () => problem(422, "video_speech_voice_not_allowed"), "owner"],
    [PAID[3], () => problem(429, "video_speech_budget_exhausted"), "service"],
  ];
  for (const [paid, answer, who] of once) {
    const { calls, options } = server([answer, paid.ok]);
    const expected = (await answer().json()).code;
    await assert.rejects(paid.send(options), (error) => error instanceof SpeechError && error.code === expected && error.who === who);
    assert.equal(calls.length, 1, `${paid.name}: ${expected}`);
  }
});

test("a clip the server cannot time answers null after one request; a timed one answers its chars", async () => {
  const wav = audio();
  for (const [what, answer] of [
    ["a site from before the route", () => new Response("<html>404</html>", { status: 404 })],
    ["no aligner on the server", () => problem(503, "video_align_unavailable")],
    ["a voice without boundaries", () => problem(422, "video_align_voice_unsupported")],
  ]) {
    const { calls, sleeps, options } = server([answer]);
    assert.equal(await alignClip({ ...options, wav, text: "好" }), null, what);
    assert.equal(calls.length, 1, `${what}: asked once`);
    assert.deepEqual(sleeps, [], `${what}: no wait`);
  }
  const timed = server([() => Response.json({ source: "aligned", model: "m", chars: [{ text: "好", start_ms: 10, end_ms: 200 }] })]);
  assert.deepEqual(await alignClip({ ...timed.options, wav, text: "好", language: "en" }), { source: "aligned", model: "m", chars: [{ text: "好", start_ms: 10, end_ms: 200 }] });
  assert.equal(timed.calls[0].url, `${SITE}/api/video/speech/align`);
  const sent = JSON.parse(timed.calls[0].body);
  assert.deepEqual(sent, { audio: Buffer.from(wav).toString("base64"), text: "好", language: "en" });
  const plain = server([() => Response.json({ source: "aligned", model: "m", chars: [] })]);
  await alignClip({ ...plain.options, wav, text: "好" });
  assert.ok(!("language" in JSON.parse(plain.calls[0].body)), "the default language is not sent");
  const odd = server([() => Response.json({ source: "aligned", chars: [{ text: 1 }] })]);
  assert.equal(await alignClip({ ...odd.options, wav, text: "好" }), null, "a malformed answer is no timing");
  // Nothing is billed, so a failure that may clear is tried again, and the owner's problems are told.
  const flaky = server([() => problem(502, "upstream_unavailable"), () => Response.json({ source: "aligned", model: "m", chars: [] })]);
  assert.deepEqual(await alignClip({ ...flaky.options, wav, text: "好" }), { source: "aligned", model: "m", chars: [] });
  assert.equal(flaky.calls.length, 2);
  const revoked = server([() => problem(401, "video_tool_token_invalid")]);
  await assert.rejects(alignClip({ ...revoked.options, wav, text: "好" }), (error) => error.code === "video_tool_token_invalid" && error.who === "owner");
});

test("synthesizeAligned answers null when the site cannot do it in one call, with nothing paid", async () => {
  for (const [what, answer] of [
    ["a site from before the route", () => new Response("Not Found", { status: 404 })],
    ["a Gemini voice", () => problem(422, "video_align_voice_unsupported")],
  ]) {
    const { calls, sleeps, options } = server([answer]);
    assert.equal(await PAID[3].send(options), null, what);
    assert.equal(calls.length, 1, `${what}: asked once`);
    assert.deepEqual(sleeps, [], `${what}: no wait`);
    assert.deepEqual(JSON.parse(calls[0].body), { speech: { voice: "zh-TW-HsiaoChenNeural", segments: [{ parts: [{ text: "好" }], break_after_ms: 0 }] } }, what);
  }
});

// The routes' own limit: one window of 60 seconds per token, which every route the token calls and
// both worker lanes share (apps/api/app/video_speech/admin_api.py video_tool). Its refusals came
// within a burst of narration lines and blocked a video (2026-10-05-a-burst-of-narration-lines-trips).
const limited = (headers = {}) => () => problem(429, "rate_limit_exceeded", headers);
const EVERY_CALL = () => {
  const wav = audio();
  return [
    ...PAID.map((paid) => [paid.name, paid.send, paid.ok]),
    ["speechStatus", (options) => speechStatus(options), () => Response.json({ configured: true, voices: [] })],
    ["alignClip", (options) => alignClip({ ...options, wav, text: "好" }), () => Response.json({ source: "aligned", model: "m", chars: [] })],
  ];
};

test("the routes' rate limit is waited out: the Retry-After it sends, or a whole window from a host before the header", async () => {
  assert.equal(RATE_WINDOW_MS, 61_000, "one whole window of the token's 60-second limit, and a second for its edge");
  for (const [name, send, ok] of EVERY_CALL()) {
    for (const [what, headers, waits] of [
      ["a host from before the header", {}, [RATE_WINDOW_MS]],
      ["the seconds left in the window", { "Retry-After": "42" }, [42_000]],
      ["a whole window, past the 60 seconds this client used to cut it to", { "Retry-After": "61" }, [61_000]],
      ["a date instead of seconds", { "Retry-After": "Wed, 07 Oct 2026 05:00:00 GMT" }, [RATE_WINDOW_MS]],
    ]) {
      const label = `${name}: ${what}`;
      const { calls, sleeps, options } = server([limited(headers), ok]);
      await send(options);
      assert.equal(calls.length, 2, `${label}: asked again once, after the wait`);
      assert.equal(calls[1].body, calls[0].body, `${label}: the same request`);
      assert.deepEqual(sleeps, waits, label);
    }
  }
});

test("a limit that keeps refusing is told after five requests, as the service's and never as a lost answer, with no wait after the last", async () => {
  for (const [name, send] of EVERY_CALL()) {
    const { calls, sleeps, options } = server([limited()]);
    await assert.rejects(send(options), (error) => {
      assert.ok(error instanceof SpeechError, name);
      assert.deepEqual([error.code, error.status, error.who], ["rate_limit_exceeded", 429, "service"], name);
      return true;
    });
    assert.equal(calls.length, 5, name);
    assert.deepEqual(sleeps, Array(4).fill(RATE_WINDOW_MS), name);
  }
});

test("a wait longer than one retry should sit through is told at once: the transcriber's hourly limit, a provider's long quota", async () => {
  assert.equal(MAX_RETRY_WAIT_MS, 90_000);
  for (const [what, answer, asked] of [
    ["the hourly transcription limit", limited({ "Retry-After": "2400" }), 1],
    ["a provider asking for fifteen minutes", () => problem(429, "video_speech_upstream_busy", { "Retry-After": "900" }), 1],
    ["a minute and a half, the longest wait taken", limited({ "Retry-After": "90" }), 2],
    ["a second longer", limited({ "Retry-After": "91" }), 1],
  ]) {
    const { calls, sleeps, options } = server([answer, PAID[1].ok]);
    if (asked === 2) {
      PAID[1].check(await PAID[1].send(options));
      assert.deepEqual(sleeps, [90_000], what);
    } else {
      await assert.rejects(PAID[1].send(options), (error) => error.status === 429 && error.who === "service" && error.code !== SPEECH_UNCERTAIN, what);
      assert.deepEqual(sleeps, [], `${what}: no wait at all`);
    }
    assert.equal(calls.length, asked, what);
  }
});

test("other retries keep their backoff, and nothing waits after the last request", async () => {
  const told = server([() => problem(503, "video_speech_upstream_busy", { "Retry-After": "10" }), PAID[1].ok]);
  PAID[1].check(await PAID[1].send(told.options));
  assert.deepEqual(told.sleeps, [10_000], "a busy provider's own Retry-After");
  const bare = server([() => problem(429, "video_speech_upstream_busy"), PAID[1].ok]);
  PAID[1].check(await PAID[1].send(bare.options));
  assert.deepEqual(bare.sleeps, [1000], "a provider's 429 without the header is not the routes' window");
  const offline = server([() => { throw failed("ECONNREFUSED"); }]);
  await assert.rejects(speechStatus(offline.options), (error) => error.code === "network");
  assert.deepEqual(offline.sleeps, [1000, 2000, 4000, 8000]);
  const down = server([() => problem(502, "upstream_unavailable")]);
  await assert.rejects(PAID[2].send(down.options), (error) => error.code === "upstream_unavailable");
  assert.deepEqual(down.sleeps, [1000, 2000, 4000, 8000]);
});

test("through the speech journal, a narration the limit refused is sent again, and one it kept refusing leaves no entry to hold", async () => {
  const dir = path.join(tempDir("speech-client-"), "speech-journal");
  const narrate = (options) => openSpeechJournal(dir).wrap((body) => synthesize({ ...options, body }));
  const line = (text) => ({ voice: "zh-TW-HsiaoChenNeural", segments: [{ parts: [{ text }], break_after_ms: 0 }] });
  const once = server([limited(), PAID[0].ok]);
  PAID[0].check(await narrate(once.options)(line("好")));
  assert.equal(once.calls.length, 2);
  assert.equal(listSpeechJournal(dir).find((entry) => entry.sha === requestSha256(line("好")))?.status, "confirmed", "its answer is kept like any other");
  const refused = server([limited()]);
  await assert.rejects(narrate(refused.options)(line("壞")), (error) => error.code === "rate_limit_exceeded" && error.who === "service");
  assert.equal(refused.calls.length, 5);
  assert.equal(listSpeechJournal(dir).some((entry) => entry.sha === requestSha256(line("壞"))), false, "the API refused it before any provider call: nothing to hold");
  const later = server([PAID[0].ok]);
  PAID[0].check(await narrate(later.options)(line("壞")));
  assert.equal(later.calls.length, 1, "the next run sends it");
});

