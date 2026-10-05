import test from "node:test";
import assert from "node:assert/strict";
import { existsSync, mkdtempSync, readFileSync, readdirSync, rmSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import { createHash } from "node:crypto";
import { synthesize, transcribeClip, judgeLines, speechStatus, SPEECH_UNCERTAIN } from "../../../tools/video/tts/client.mjs";
import { encodeWav, parseWav } from "../../../tools/video/tts/wav.mjs";
import { createSpeechJournalFetch, speechConfiguration } from "./speech-journal.mjs";

const site = "https://mokaair.com", token = `mkv_${"s".repeat(40)}`, slug = "ai-real-world-06-digital-yesman";
const hash = (v) => createHash("sha256").update(v).digest("hex");
const raw = encodeWav(Int16Array.from([0, 100, -100, 200, -200, 0]), 24000);
const speechBody = { voice: "gemini:Sulafat", model: "gemini-2.5-flash-preview-tts", style: "Clearly", segments: [{ parts: [{ text: "Approved words" }], break_after_ms: 0 }] };
const wavResponse = () => new Response(raw, { headers: { "Content-Type": "audio/wav", "X-Billable-Characters": "14", "Cache-Control": "no-store", "Authorization": `Bearer ${token}`, "Set-Cookie": token } });
function fixture(t) {
  const workdir = mkdtempSync(path.join(os.tmpdir(), "speech-journal-")); t.after(() => rmSync(workdir, { recursive: true, force: true }));
  const identity = { source_kind: "approved-final-body-range", slug, final_sha256: "a".repeat(64), source_sha256: "b".repeat(64), raw_source: { script_sha256: "c".repeat(64), timeline_sha256: "d".repeat(64), lexicon_sha256: "e".repeat(64) }, request_namespace: "11111111-1111-4111-8111-111111111111", choice: { locales: { en: { metadata: true, captions: true, dub: true } }, decided_at: "2026-10-04T00:00:00Z" }, configuration: speechConfiguration({ voice: { provider: "gemini", name: "Sulafat", model: "selected-model" }, stage_models: { caption_reviewer: { provider: "gemini", model: "selected-reviewer" } } }, { gemini_configured: true, gemini_models: ["selected-model"], gemini_monthly_limit: 1000 }) };
  const journalFile = path.join(workdir, "speech-journal/journal.json"), read = () => JSON.parse(readFileSync(journalFile));
  const make = (fetchImpl, more = {}) => createSpeechJournalFetch({ fetchImpl, site, workdir, readIdentity: async () => structuredClone(identity), ...more });
  const options = (fetchImpl) => ({ site, token, fetchImpl, sleep: async () => {} });
  return { workdir, identity, journalFile, read, make, options };
}
const invoke = (f, fetchImpl, body = speechBody) => synthesize({ ...f.options(fetchImpl), body });

test("real native synthesis saves original response bytes and billable headers before consumption and replays after restart", async (t) => {
  const f = fixture(t); let posts = 0;
  const guarded = f.make(async (_url, init) => { posts++; assert.equal(init.redirect, "error"); assert.equal(new Headers(init.headers).get("authorization"), `Bearer ${token}`); return wavResponse(); });
  const checked = async (...args) => {
    const response = await guarded(...args), journal = f.read(), record = Object.values(journal.entries)[0];
    assert.equal(record.status, "succeeded"); assert.deepEqual(readFileSync(path.join(f.workdir, "speech-journal", record.response.file)), raw); assert.equal(record.response.sha256, hash(raw));
    assert.equal(response.headers.get("authorization"), null); assert.equal(response.headers.get("set-cookie"), null); return response;
  };
  const first = await invoke(f, checked); assert.equal(first.billable, 14); assert.equal(parseWav(first.wav).sampleRate, 48000);
  const second = await invoke(f, f.make(async () => { posts++; assert.fail("restart cannot resubmit the saved speech"); }));
  assert.deepEqual(second, first); assert.equal(posts, 1); assert.equal(readFileSync(f.journalFile, "utf8").includes(token), false);
});

test("real native transcribe and judge preserve complete actual JSON responses with zero POST replay", async (t) => {
  const f = fixture(t); let posts = 0;
  const fetchImpl = f.make(async (url) => { posts++; return url.endsWith("/transcribe") ? Response.json({ text: "Actual heard words" }) : Response.json({ results: [{ id: "aaaa", noul: 0.8 }, { id: "bbbb", noul: 0.2 }] }); });
  const lines = [{ id: "aaaa", intended: "Actual", spoken_form: "Actual", heard: "Actual" }, { id: "bbbb", intended: "Other", spoken_form: "Other", heard: "Different" }];
  const options = f.options(fetchImpl);
  assert.equal(await transcribeClip({ ...options, wav: raw, terms: ["Actual"], language: "en" }), "Actual heard words");
  assert.deepEqual(await judgeLines({ ...options, lines, language: "en" }), new Map([["aaaa", 0.8], ["bbbb", 0.2]]));
  const restarted = f.options(f.make(async () => assert.fail("successful JSON cannot be bought again")));
  assert.equal(await transcribeClip({ ...restarted, wav: raw, terms: ["Actual"], language: "en" }), "Actual heard words");
  assert.deepEqual(await judgeLines({ ...restarted, lines, language: "en" }), new Map([["aaaa", 0.8], ["bbbb", 0.2]])); assert.equal(posts, 2);
});

test("a lost paid POST submits once despite the native five-attempt client and blocks changed voice or another paid route", async (t) => {
  const f = fixture(t); let posts = 0, sleeps = 0;
  const wrapped = f.make(async () => { posts++; throw Error(`connection lost ${token}`); });
  await assert.rejects(synthesize({ site, token, body: speechBody, fetchImpl: wrapped, sleep: async () => { sleeps++; } }), (error) => error.code === "video_speech_result_held");
  assert.equal(posts, 1); assert.equal(sleeps, 0); assert.equal(Object.values(f.read().entries)[0].status, "unknown");
  const restart = f.make(async () => { posts++; return wavResponse(); });
  await assert.rejects(invoke(f, restart, { ...speechBody, voice: "gemini:Other" }), /held/);
  await assert.rejects(transcribeClip({ ...f.options(restart), wav: raw }), /held/); assert.equal(posts, 1);
  assert.equal(readFileSync(f.journalFile, "utf8").includes(token), false);
});

test("lost or truncated response bodies remain held and cannot be bought again", async (t) => {
  for (const reason of ["stream", "length", "wav", "json", "judge"]) await t.test(reason, async (t) => {
    const f = fixture(t); let posts = 0;
    const fetchImpl = f.make(async () => {
      posts++;
      if (reason === "stream") return new Response(new ReadableStream({ start(controller) { controller.error(Error("truncated response")); } }));
      if (reason === "length") return new Response(raw, { headers: { "Content-Length": String(raw.length + 1) } });
      if (reason === "wav") return new Response(raw.subarray(0, raw.length - 2));
      if (reason === "json") return new Response('{"text":');
      return Response.json({ results: [{ id: "wrong", noul: 1 }] });
    });
    const call = reason === "json" ? () => transcribeClip({ ...f.options(fetchImpl), wav: raw }) : reason === "judge" ? () => judgeLines({ ...f.options(fetchImpl), lines: [{ id: "aaaa", intended: "x", spoken_form: "x", heard: "x" }] }) : () => invoke(f, fetchImpl);
    await assert.rejects(call(), /held/); assert.equal(posts, 1); assert.equal(Object.values(f.read().entries)[0].status, "unknown");
    await assert.rejects(invoke(f, fetchImpl), /held/); assert.equal(posts, 1);
  });
});

test("pre-dispatch and response-save failures retain an honest hold, including bytes saved before success receipt fails", async (t) => {
  for (const when of ["intent", "bytes", "success"]) await t.test(when, async (t) => {
    const f = fixture(t); let posts = 0;
    const write = (file, bytes) => {
      if (when === "intent" || when === "bytes" && file.endsWith(".bin") || when === "success" && String(bytes).includes('"status": "succeeded"')) throw Error("disk unavailable");
      writeFileSync(file, bytes);
    };
    await assert.rejects(invoke(f, f.make(async () => { posts++; return wavResponse(); }, { write })), /held/); assert.equal(posts, when === "intent" ? 0 : 1);
    const restart = f.make(async () => { posts++; return wavResponse(); });
    await assert.rejects(invoke(f, restart), /held/); assert.equal(posts, when === "intent" ? 0 : 1);
    if (when === "success") { const record = Object.values(f.read().entries)[0]; assert.equal(record.status, "unknown"); assert.deepEqual(readFileSync(path.join(f.workdir, "speech-journal", record.response.file)), raw); }
  });
});

test("source, final, raw evidence, choice, namespace and public model/capability drift cannot replay or dispatch", async (t) => {
  const f = fixture(t); let posts = 0; await invoke(f, f.make(async () => { posts++; return wavResponse(); }));
  const original = structuredClone(f.identity);
  for (const [name, change] of [
    ["final", (v) => { v.final_sha256 = "f".repeat(64); }], ["source", (v) => { v.source_sha256 = "f".repeat(64); }],
    ["script", (v) => { v.raw_source.script_sha256 = "f".repeat(64); }], ["timing", (v) => { v.raw_source.timeline_sha256 = "f".repeat(64); }], ["lexicon", (v) => { v.raw_source.lexicon_sha256 = "f".repeat(64); }],
    ["choice", (v) => { v.choice.locales.en.dub = false; }], ["namespace", (v) => { v.request_namespace = "22222222-2222-4222-8222-222222222222"; }],
    ["model", (v) => { v.configuration.voice.model = "changed"; }], ["capability", (v) => { v.configuration.speech.gemini_configured = false; }], ["budget", (v) => { v.configuration.speech.gemini_monthly_limit = 2000; }],
  ]) await t.test(name, async () => {
    const changed = structuredClone(original); change(changed);
    await assert.rejects(invoke(f, f.make(async () => { posts++; return wavResponse(); }, { readIdentity: async () => changed })), /held/); assert.equal(posts, 1);
  });
});

test("corrupt, pending, missing or orphan receipts hold every subsequent paid payload", async (t) => {
  const f = fixture(t); let posts = 0; await invoke(f, f.make(async () => { posts++; return wavResponse(); }));
  const original = readFileSync(f.journalFile), record = Object.values(f.read().entries)[0], bytesFile = path.join(f.workdir, "speech-journal", record.response.file);
  for (const [name, change] of [
    ["request", (v) => { Object.values(v.entries)[0].request.body_utf8 += " "; }], ["result hash", (v) => { Object.values(v.entries)[0].response.sha256 = "0".repeat(64); }],
    ["pending", (v) => { Object.values(v.entries)[0].status = "pending"; }], ["unknown", (v) => { Object.values(v.entries)[0].status = "unknown"; }],
    ["auth header", (v) => { Object.values(v.entries)[0].response.headers.authorization = "not allowed"; }], ["path", (v) => { Object.values(v.entries)[0].response.file = "../outside.bin"; }], ["orphan", (v) => { v.entries = {}; }],
    ["billable header", (v) => { Object.values(v.entries)[0].response.headers["x-billable-characters"] = "15"; }],
  ]) await t.test(name, async () => {
    const value = JSON.parse(original); change(value); writeFileSync(f.journalFile, JSON.stringify(value));
    await assert.rejects(invoke(f, f.make(async () => { posts++; return wavResponse(); }), { ...speechBody, style: "new payload" }), /held/); assert.equal(posts, 1);
  });
  writeFileSync(f.journalFile, original); writeFileSync(bytesFile, Buffer.from("changed response")); await assert.rejects(invoke(f, f.make(async () => { posts++; return wavResponse(); })), /held/); assert.equal(posts, 1);
  writeFileSync(bytesFile, raw); writeFileSync(f.journalFile, "{corrupt"); await assert.rejects(invoke(f, f.make(async () => { posts++; return wavResponse(); })), /held/); assert.equal(posts, 1);
  rmSync(f.journalFile); await assert.rejects(invoke(f, f.make(async () => { posts++; return wavResponse(); })), /held/); assert.equal(posts, 1);
});

test("simultaneous native calls cannot race past the pending intent", async (t) => {
  const f = fixture(t); let posts = 0, release, started;
  const reached = new Promise((resolve) => { started = resolve; }), pending = new Promise((resolve) => { release = resolve; });
  const first = invoke(f, f.make(async () => { posts++; started(); await pending; return wavResponse(); }));
  await reached; await assert.rejects(invoke(f, f.make(async () => { posts++; return wavResponse(); })), /held/); assert.equal(posts, 1);
  release(); assert.equal((await first).billable, 14); assert.equal(Object.values(f.read().entries)[0].status, "succeeded");
});

test("GET and unrelated routes pass through, while foreign or changed paid origins never dispatch", async (t) => {
  const f = fixture(t); let calls = 0, identities = 0;
  const fetchImpl = f.make(async () => { calls++; return Response.json({ configured: true }); }, { readIdentity: async () => { identities++; return f.identity; } });
  assert.equal((await speechStatus(f.options(fetchImpl))).configured, true);
  assert.equal((await fetchImpl(`${site}/api/video/reviews/${slug}`, { method: "POST", body: "unrelated" })).status, 200); assert.equal(calls, 2); assert.equal(identities, 0);
  for (const url of ["https://other.invalid/api/video/speech", `${site}/api/video/speech?changed=1`, `${site}/api/video/speech/`, `${site}/api/v1/video/speech`]) assert.equal((await fetchImpl(url, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(speechBody) })).status, 409);
  assert.equal(calls, 2); assert.equal(existsSync(path.join(f.workdir, "speech-journal")), false);
});

test("native server auth/quota classification is preserved and retryable upstream failure still buys once", async (t) => {
  // The web route's 503/502 `upstream_unavailable` can also mean an answer lost after the POST went
  // out, so the native client itself stops on it as uncertain (exit 3) before the journal's hold.
  for (const [status, code, who, seen = code] of [[401, "video_tool_token_invalid", "owner"], [429, "video_speech_budget_exhausted", "service"], [503, "upstream_unavailable", "owner", SPEECH_UNCERTAIN]]) await t.test(code, async (t) => {
    const f = fixture(t); let posts = 0;
    await assert.rejects(invoke(f, f.make(async () => { posts++; return Response.json({ code, detail: code }, { status }); })), (error) => error.who === who && error.code === seen);
    assert.equal(posts, 1); assert.equal(Object.values(f.read().entries)[0].status, "unknown");
  });
});

test("only tokenless stable settings enter identity and unauthorized body fields refuse before dispatch", async (t) => {
  const first = speechConfiguration({ voice: { name: "Sulafat" }, usage: { tokens: 1 }, token }, { configured: true, used: 1, remaining: 99 });
  const second = speechConfiguration({ voice: { name: "Sulafat" }, usage: { tokens: 2 }, token }, { configured: true, used: 2, remaining: 98 });
  assert.deepEqual(first, second); assert.equal(JSON.stringify(first).includes(token), false);
  assert.throws(() => speechConfiguration({ voice: { token } }), /secret/);
  const f = fixture(t); let posts = 0;
  await assert.rejects(invoke(f, f.make(async () => { posts++; return wavResponse(); }), { ...speechBody, authorization: token }), /held/);
  assert.equal(posts, 0); assert.equal(existsSync(path.join(f.workdir, "speech-journal")), false);
  assert.equal(readdirSync(f.workdir).length, 0);
});

test("complete PCM response validates every RIFF chunk and frame instead of parser clamping", async (t) => {
  for (const [name, change] of [
    ["data exceeds bytes", (v) => { v.writeUInt32LE(v.readUInt32LE(40) + 2, 40); return v; }],
    ["odd PCM", (v) => { const out = Buffer.concat([v, Buffer.from([1, 0])]); out.writeUInt32LE(out.length - 8, 4); out.writeUInt32LE(v.readUInt32LE(40) + 1, 40); return out; }],
    ["short fmt", (v) => { v.writeUInt32LE(14, 16); return v; }],
    ["fmt exceeds bytes", (v) => { v.writeUInt32LE(v.length, 16); return v; }],
    ["wrong block align", (v) => { v.writeUInt16LE(4, 32); return v; }],
    ["wrong byte rate", (v) => { v.writeUInt32LE(1, 28); return v; }],
    ["partial trailing chunk", (v) => { const out = Buffer.concat([v, Buffer.from("JUNK")]); out.writeUInt32LE(out.length - 8, 4); return out; }],
    ["trailing chunk exceeds bytes", (v) => { const tail = Buffer.alloc(8); tail.write("JUNK"); tail.writeUInt32LE(2, 4); const out = Buffer.concat([v, tail]); out.writeUInt32LE(out.length - 8, 4); return out; }],
    ["unproven outer stream length", (v) => { v.writeUInt32LE(0xffffffff, 4); return v; }],
    ["data before fmt", (v) => { v.write("data", 12); return v; }],
    ["float as PCM", (v) => { v.writeUInt16LE(3, 20); return v; }],
  ]) await t.test(name, async (t) => {
    const f = fixture(t); let posts = 0; const bytes = change(Buffer.from(raw));
    const fetchImpl = f.make(async () => { posts++; return new Response(bytes, { headers: { "Content-Type": "audio/wav" } }); });
    await assert.rejects(invoke(f, fetchImpl), /held/); assert.equal(posts, 1); assert.equal(Object.values(f.read().entries)[0].status, "unknown");
    await assert.rejects(invoke(f, fetchImpl), /held/); assert.equal(posts, 1);
  });
  for (const size of [0, 0xffffffff]) await t.test(`complete final streamed data ${size}`, async (t) => {
    const f = fixture(t), bytes = Buffer.from(raw); bytes.writeUInt32LE(size, 40); let posts = 0;
    const fetchImpl = f.make(async () => { posts++; return new Response(bytes, { headers: { "Content-Type": "audio/wav", "X-Billable-Characters": "14" } }); });
    assert.equal((await invoke(f, fetchImpl)).billable, 14); await invoke(f, fetchImpl); assert.equal(posts, 1);
  });
});

test("STOP after the awaited speech identity or intent holds the native client without a POST", async (t) => {
  for (const when of ["identity", "intent"]) await t.test(when, async (t) => {
    const f = fixture(t); let posts = 0;
    const readIdentity = async () => {
      await Promise.resolve();
      if (when === "identity") writeFileSync(path.join(f.workdir, "STOP"), "owner STOP during the fresh identity probe");
      return structuredClone(f.identity);
    };
    const write = (file, bytes) => {
      writeFileSync(file, bytes);
      if (when === "intent" && String(bytes).includes('"status": "pending"')) writeFileSync(path.join(f.workdir, "STOP"), "owner STOP after the intent was saved");
    };
    await assert.rejects(invoke(f, f.make(async () => { posts++; return wavResponse(); }, { readIdentity, write })), /held/);
    assert.equal(posts, 0); assert.ok(existsSync(path.join(f.workdir, "STOP")));
    if (when === "identity") assert.equal(existsSync(path.join(f.workdir, "speech-journal")), false);
    else {
      const receipt = readFileSync(f.journalFile);
      assert.equal(Object.values(f.read().entries)[0].status, "unknown");
      await assert.rejects(invoke(f, f.make(async () => { posts++; return wavResponse(); })), /held/);
      assert.deepEqual(readFileSync(f.journalFile), receipt); assert.equal(posts, 0);
    }
  });
});

test("STOP preserves every existing succeeded or unknown speech receipt byte for byte", async (t) => {
  for (const savedStatus of ["succeeded", "unknown"]) await t.test(savedStatus, async (t) => {
    const f = fixture(t); let posts = 0;
    const first = f.make(async () => { posts++; if (savedStatus === "unknown") throw Error("lost result"); return wavResponse(); });
    if (savedStatus === "unknown") await assert.rejects(invoke(f, first), /held/); else await invoke(f, first);
    const receipt = readFileSync(f.journalFile);
    const wrapped = f.make(async () => { posts++; return wavResponse(); }, { readIdentity: async () => { await Promise.resolve(); writeFileSync(path.join(f.workdir, "STOP"), "owner STOP during the fresh probe"); return f.identity; } });
    await assert.rejects(invoke(f, wrapped), /held/);
    assert.equal(posts, 1); assert.deepEqual(readFileSync(f.journalFile), receipt);
    assert.equal(Object.values(f.read().entries)[0].status, savedStatus);
  });
});
