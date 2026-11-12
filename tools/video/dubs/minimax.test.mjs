// Dubs in MiniMax voices (the owner's choice of 2026-11-12): who gets which voice, what falls back
// to Gemini, how a record remembers its voices, and a whole `dub` run against a site with MiniMax.
import assert from "node:assert/strict";
import { mkdirSync, readFileSync, readdirSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { EXIT, main } from "../cli.mjs";
import { fixture, sandbox } from "../core/fixtures/load.mjs";
import { eachLine, textHash } from "../core/schema.mjs";
import { dubArtifacts, loadProject } from "../core/state.mjs";
import { SAMPLE_RATE } from "../core/timeline.mjs";
import { concatSamples, encodeWav } from "../tts/wav.mjs";
import { dubProvider } from "./cli.mjs";
import { DUB_MINIMAX_VOICES, DUB_STYLES, dubFingerprint, dubScript, recordProvider, speechCurrent } from "./plan.mjs";

process.env.VIDEO_MIN_EPISODE_MINUTES ??= "0";

const TOKEN = `mkv_${"t".repeat(43)}`;
const SULAFAT = { provider: "gemini", name: "Sulafat", style: "Taiwan Mandarin, relaxed." };

function translationFor(doc, textFor) {
  const lines = {};
  for (const { line } of eachLine(doc)) lines[line.id] = { source_hash: textHash(line.text), text: textFor(line) };
  return { title: "T", description: "D", tags: [], chapters: {}, source_hashes: {}, lines };
}

/** So That's Why's shape: a cute-cartoon explainer whose host shares the narrator's voice and whose kid has her own. */
function dialogueDoc() {
  const doc = JSON.parse(readFileSync(new URL("../core/fixtures/explainer/video.json", import.meta.url), "utf8"));
  return {
    ...doc,
    look: { preset: "cute-cartoon" },
    voice: SULAFAT,
    characters: [
      { id: "chief", name: "所長", voice: { provider: "gemini", name: "Sulafat", style: "所長，溫和" } },
      { id: "kid", name: "小問", voice: { provider: "gemini", name: "Leda", style: "八歲小女孩" } },
    ],
  };
}

test("every dub locale has MiniMax voices, the narrator's first", () => {
  assert.deepEqual(Object.keys(DUB_MINIMAX_VOICES).sort(), ["en", "es", "id", "ja", "ko", "pt", "th", "vi"]);
  for (const voices of Object.values(DUB_MINIMAX_VOICES)) assert.ok(voices.length >= 1 && voices.every((voice) => /^[A-Za-z]/.test(voice.name)));
  assert.equal(DUB_MINIMAX_VOICES.vi[0].rate, "+15%", "Vietnamese is read faster to fit the windows");
});

test("with MiniMax the narrator reads in the locale's first voice, without a style; Gemini stays as it was", () => {
  const doc = { ...fixture(), voice: SULAFAT };
  const translation = translationFor(doc, (line) => `EN ${line.id}`);
  const minimax = dubScript(doc, translation, "en", null, "minimax").doc;
  assert.deepEqual(minimax.voice, { provider: "minimax", name: "English_CalmWoman" });
  const vi = dubScript(doc, translation, "vi", null, "minimax").doc;
  assert.deepEqual(vi.voice, { provider: "minimax", name: "Vietnamese_kindhearted_girl", rate: "+15%" });
  const gemini = dubScript(doc, translation, "en").doc;
  assert.deepEqual(gemini.voice, { provider: "gemini", name: "Sulafat", style: DUB_STYLES.en });
  assert.deepEqual(dubScript(doc, translation, "en", null, "gemini").doc, gemini, "gemini is the default");
});

test("each distinct voice of a dialogue explainer takes the next MiniMax voice; one past the list keeps Gemini", () => {
  const doc = dialogueDoc();
  const translation = translationFor(doc, (line) => `EN ${line.id}`);
  const en = dubScript(doc, translation, "en", null, "minimax").doc;
  const byId = Object.fromEntries(en.characters.map((character) => [character.id, character.voice]));
  assert.equal(en.voice.name, "English_CalmWoman");
  assert.equal(byId.chief.name, "English_CalmWoman", "the host shares the narrator's zh-TW voice, so its dub voice too");
  assert.equal(byId.kid.name, "English_expressive_narrator");
  const vi = dubScript(doc, translation, "vi", null, "minimax").doc;
  const kid = vi.characters.find((character) => character.id === "kid").voice;
  assert.equal(kid.provider, "gemini", "Vietnamese has one MiniMax voice; the kid keeps her Gemini dub voice");
  assert.equal(kid.name, "Leda");
  assert.match(kid.style, /Vietnamese/);
});

test("a slides cohost takes the second voice", () => {
  const doc = JSON.parse(readFileSync(new URL("../core/fixtures/cohost/video.json", import.meta.url), "utf8"));
  const script = dubScript(doc, translationFor(doc, (line) => `JA ${line.id}`), "ja", null, "minimax").doc;
  assert.equal(script.voice.name, "Japanese_CalmLady");
  assert.equal(script.cohost.voice.name, "Japanese_KindLady");
});

test("a MiniMax dub drops the zh-TW pronunciation hints a Gemini dub keeps", () => {
  const doc = { ...fixture(), voice: SULAFAT, pronunciation_hints: { 和: "hàn" } };
  const translation = translationFor(doc, (line) => `EN ${line.id}`);
  assert.ok(!("pronunciation_hints" in dubScript(doc, translation, "en", null, "minimax").doc));
  assert.deepEqual(dubScript(doc, translation, "en").doc.pronunciation_hints, { 和: "hàn" });
});

test("a record is judged by the voices it was made with", () => {
  const doc = { ...fixture(), voice: SULAFAT };
  const project = { doc, translations: { en: translationFor(doc, (line) => `EN ${line.id}`) }, lexicon: { schema_version: 1, terms: {} } };
  const gemini = dubFingerprint(project, "en");
  const minimax = dubFingerprint(project, "en", null, "minimax");
  assert.notEqual(gemini, minimax);
  assert.equal(recordProvider({}), "gemini", "a record from before MiniMax dubs was Gemini's");
  assert.equal(recordProvider({ voice_provider: "minimax" }), "minimax");
  assert.equal(speechCurrent(project, "en", { speech_fingerprint: gemini }), true);
  assert.equal(speechCurrent(project, "en", { speech_fingerprint: minimax, voice_provider: "minimax" }), true);
  assert.equal(speechCurrent(project, "en", { speech_fingerprint: minimax }), false);
});

test("dub picks MiniMax when the site has its key, unless --provider says otherwise", () => {
  assert.equal(dubProvider({}, { minimax_configured: true }), "minimax");
  assert.equal(dubProvider({}, { minimax_configured: false }), "gemini");
  assert.equal(dubProvider({}, null), "gemini");
  assert.equal(dubProvider({ provider: "gemini" }, { minimax_configured: true }), "gemini");
});

// A site with both keys: 60 ms of tone a character, as the dub tests' server.
function fakeServer() {
  const calls = [];
  const fetchImpl = async (url, init) => {
    calls.push({ url, init });
    if (url.endsWith("/api/video/speech/status")) {
      return Response.json({ configured: false, voices: [], monthly_limit: 0, used: 0, remaining: 0, gemini_configured: true, gemini_monthly_limit: 300000, gemini_used: 1000, minimax_configured: true, minimax_models: ["speech-2.8-hd"], minimax_voices: [], minimax_monthly_limit: 300000, minimax_used: 0 });
    }
    const body = JSON.parse(init.body);
    const ms = (value) => Math.round((value / 1000) * SAMPLE_RATE);
    const audio = concatSamples(body.segments.flatMap((segment) => [Int16Array.from({ length: ms(segment.parts.reduce((sum, part) => sum + part.text.length, 0) * 60) }, (_, index) => Math.round(8000 * Math.sin(index / 7))), new Int16Array(ms(segment.break_after_ms))]));
    return new Response(encodeWav(audio), { status: 200, headers: { "Content-Type": "audio/wav", "X-Billable-Characters": "10" } });
  };
  return { calls, fetchImpl };
}

function fakeFfmpeg() {
  return {
    locate: async () => ({ ffmpeg: "ffmpeg", ffprobe: "ffprobe", version: "fake ffmpeg" }),
    run: async (file, args) => {
      const input = args[args.indexOf("-i") + 1];
      if (args.includes("null")) return { stdout: "", stderr: 'Parsed_loudnorm {"input_i":"-20.0","input_tp":"-3.0","input_lra":"5.0","input_thresh":"-30.0","target_offset":"0.5"}\n' };
      writeFileSync(args.at(-1), readFileSync(input));
      return { stdout: "", stderr: "" };
    },
  };
}

function capture(box, server, ffmpeg) {
  const out = { stdout: "", stderr: "" };
  const ctx = {
    root: box.root, env: { VIDEO_WORKDIR: box.work, MOKAAIR_VIDEO_TOKEN: TOKEN }, home: box.base,
    stdout: { write: (text) => (out.stdout += text) }, stderr: { write: (text) => (out.stderr += text) },
    now: () => new Date("2026-11-12T07:00:00Z"), fetch: server.fetchImpl, sleep: async () => {}, ffmpeg,
  };
  return { ctx, out };
}

const spokenVoices = (server) => server.calls.filter((call) => call.url.endsWith("/api/video/speech")).map((call) => JSON.parse(call.init.body).voice);

test("dub on a site with a MiniMax key reads in MiniMax voices, records it, and stays current", async () => {
  const box = sandbox();
  const doc = { ...fixture(), voice: SULAFAT };
  writeFileSync(path.join(box.dir, "video.json"), JSON.stringify(doc));
  mkdirSync(path.join(box.dir, "i18n"), { recursive: true });
  writeFileSync(path.join(box.dir, "i18n", "en.json"), JSON.stringify(translationFor(doc, (line) => `EN ${line.id}`)));
  const server = fakeServer();
  const ffmpeg = fakeFfmpeg();
  const tts = capture(box, server, ffmpeg);
  const narrated = await main(["tts", "--slug", box.slug], tts.ctx);
  assert.ok([EXIT.ok, EXIT.lint].includes(narrated), tts.out.stdout + tts.out.stderr);
  const before = server.calls.length;

  const run = capture(box, server, ffmpeg);
  assert.equal(await main(["dub", "--slug", box.slug, "--locale", "en"], run.ctx), EXIT.ok, run.out.stdout + run.out.stderr);
  const sent = spokenVoices({ calls: server.calls.slice(before) });
  assert.ok(sent.length > 0 && sent.every((voice) => voice === "minimax:English_CalmWoman"), JSON.stringify(sent));
  const record = JSON.parse(readFileSync(dubArtifacts(box.workdir, "en").timeline, "utf8"));
  assert.equal(record.voice_provider, "minimax");
  assert.equal(speechCurrent(loadProject({ slug: box.slug, root: box.root }), "en", record), true);

  // --provider gemini asks Sulafat again, in the dub style, and records that.
  const again = capture(box, server, ffmpeg);
  const from = server.calls.length;
  assert.equal(await main(["dub", "--slug", box.slug, "--locale", "en", "--provider", "gemini"], again.ctx), EXIT.ok, again.out.stdout + again.out.stderr);
  assert.ok(spokenVoices({ calls: server.calls.slice(from) }).every((voice) => voice === "gemini:Sulafat"));
  assert.equal(JSON.parse(readFileSync(dubArtifacts(box.workdir, "en").timeline, "utf8")).voice_provider, "gemini");
  assert.ok(readdirSync(path.dirname(dubArtifacts(box.workdir, "en").timeline)).length > 0);
});

test("--provider takes only gemini or minimax", async () => {
  const box = sandbox();
  const { ctx } = capture(box, fakeServer(), fakeFfmpeg());
  assert.equal(await main(["dub", "--slug", box.slug, "--provider", "azure"], ctx), EXIT.usage);
});
