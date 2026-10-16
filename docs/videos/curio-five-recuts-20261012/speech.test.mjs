// Offline paid-request safety and multi-language timing checks; no credentials/network.
import assert from "node:assert/strict";
import { mkdtempSync, mkdirSync, readFileSync, realpathSync, rmSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { alignOpenings, checkOpening, describePlan, loadEpisode, LOCALES, synthesizeOpening } from "./speech.mjs";
import { isInside } from "../../../tools/video/core/paths.mjs";
import { SpeechError, SPEECH_UNCERTAIN } from "../../../tools/video/tts/client.mjs";
import { encodeWav, parseWav, requireNarrationFormat } from "../../../tools/video/tts/wav.mjs";

function box(t) {
  const base = mkdtempSync(path.join(os.tmpdir(), "curio-opening-offline-"));
  t.after(() => {
    const absolute = realpathSync(base);
    assert.ok(isInside(absolute, realpathSync(os.tmpdir())) && path.basename(absolute).startsWith("curio-opening-offline-"));
    rmSync(absolute, { recursive: true });
  });
  const sources = path.join(base, "sources");
  const out = path.join(base, "output");
  const sourceDir = path.join(sources, "curio-h01");
  mkdirSync(sourceDir, { recursive: true });
  const source = { slug: "curio-h01", format: "slides", voice: { provider: "gemini", name: "Sulafat", style: "Base style", performance: "Preserve the original performance" }, scenes: [] };
  writeFileSync(path.join(sourceDir, "video.json"), JSON.stringify(source));
  writeFileSync(path.join(sources, "lexicon.json"), JSON.stringify({ schema_version: 1, terms: {} }));
  const lines = ["這是一個尚未解開的問題。", "船上的人去了什麼地方？", "每一條線索都有它的限制。", "接著回到最早的紀錄。"].map((text, index) => ({ id: `intro0${index + 1}`, text, scene: `original-${index + 1}` }));
  const episode = { slug: source.slug, lines, locales: {} };
  for (const locale of LOCALES.slice(1)) {
    const dir = path.join(sourceDir, "dubs", locale);
    mkdirSync(dir, { recursive: true });
    writeFileSync(path.join(dir, "timeline.json"), JSON.stringify({ locale, voice: { ...source.voice, style: `Original ${locale} style` } }));
    episode.locales[locale] = { lines: lines.map((line) => ({ ...line, text: locale === "en" ? "An unanswered question remains." : line.text })) };
  }
  return { base, sources, out, episode, item: (locale = "zh-TW") => loadEpisode({ episode, sources, out, locale }) };
}

const client = { site: "https://test.invalid", token: "offline-test-only" };
const statusImpl = async () => ({ gemini_configured: true, gemini_monthly_limit: 100000, gemini_used: 0 });
const wav = (seconds = 8) => encodeWav(Int16Array.from({ length: 48000 * seconds }, (_, index) => Math.round(4000 * Math.sin(index * 0.12))));

test("a saved opening resumes without another paid call, preserving performance and detecting changed bytes", async (t) => {
  const b = box(t);
  const item = b.item();
  let calls = 0;
  const synthesizeImpl = async ({ body, attempts }) => {
    calls++;
    assert.equal(attempts, 1);
    assert.match(body.style, /Base style/);
    assert.match(body.style, /Preserve the original performance/);
    return { wav: wav(), billable: 15 };
  };
  await synthesizeOpening(item, { client, statusImpl, synthesizeImpl });
  assert.equal(calls, 4);
  assert.equal(describePlan(item).pending_lines, 0);
  await synthesizeOpening(item, { client, statusImpl, synthesizeImpl });
  assert.equal(calls, 4);
  writeFileSync(path.join(item.directory, "audio", "intro01.wav"), "corrupt");
  assert.throws(() => describePlan(item), /cached WAV changed/);
  await assert.rejects(synthesizeOpening(item, { client, statusImpl, synthesizeImpl }), /cached WAV changed/);
  assert.equal(calls, 4);
});

test("an unknown paid POST outcome stays held on the next invocation", async (t) => {
  const b = box(t);
  let calls = 0;
  const synthesizeImpl = async () => { calls++; throw new SpeechError("lost response", { code: SPEECH_UNCERTAIN, who: "owner" }); };
  await assert.rejects(synthesizeOpening(b.item(), { client, statusImpl, synthesizeImpl }), /not sent again/);
  await assert.rejects(synthesizeOpening(b.item(), { client, statusImpl, synthesizeImpl }), /not sent again/);
  assert.equal(calls, 1);
});

test("four locale outputs share exact line windows and sample counts without speed changes", async (t) => {
  const b = box(t);
  const items = LOCALES.map((locale) => b.item(locale));
  let calls = 0;
  for (const [index, item] of items.entries()) await synthesizeOpening(item, { client, statusImpl, synthesizeImpl: async () => { calls++; return { wav: wav(8 + index / 10), billable: 15 }; } });
  const shared = alignOpenings(items);
  assert.equal(calls, 16);
  assert.equal(shared.duration_ok, true);
  assert.equal(shared.padding_ok, true);
  assert.equal(shared.time_stretched, false);
  assert.equal(shared.lines[0].source_scene, "original-1");
  for (const item of items) {
    const bytes = readFileSync(path.join(item.directory, "narration.wav"));
    assert.equal(requireNarrationFormat(parseWav(bytes)).length, shared.total_frames * 1600);
    const timeline = JSON.parse(readFileSync(path.join(item.directory, "timeline.json")));
    assert.deepEqual(timeline.lines.map(({ id, start_frame, end_frame }) => ({ id, start_frame, end_frame })), shared.lines.map(({ id, start_frame, end_frame }) => ({ id, start_frame, end_frame })));
    await synthesizeOpening(item, { synthesizeImpl: async () => { throw new Error("must not pay again"); } });
  }
});

test("source drift and canonical output targets are refused before paid work", async (t) => {
  const b = box(t);
  const item = b.item();
  writeFileSync(item.sourceFile, JSON.stringify({ changed: true }));
  await assert.rejects(synthesizeOpening(item, { synthesizeImpl: async () => { throw new Error("unexpected call"); } }), /source document changed/);
  const second = box(t);
  assert.throws(() => loadEpisode({ episode: second.episode, sources: second.sources, out: second.sources }), /output overlaps/);
});

test("audio check uses cached transcripts/Jev and binds the aligned outputs without claiming owner approval", async (t) => {
  const b = box(t);
  const items = LOCALES.map((locale) => b.item(locale));
  for (const item of items) await synthesizeOpening(item, { client, statusImpl, synthesizeImpl: async () => ({ wav: wav(), billable: 15 }) });
  alignOpenings(items);
  const item = items[0];
  let transcribed = 0;
  let judged = 0;
  const transcribeImpl = async ({ language, attempts }) => {
    assert.equal(language, "zh-TW");
    assert.equal(attempts, 1);
    const index = transcribed++;
    return index === 0 ? "一個還沒回答的問題。" : item.lines[index].text;
  };
  const judgeImpl = async ({ lines }) => { judged++; return new Map(lines.map((line) => [line.id, 0.99])); };
  const report = await checkOpening(item, { client, transcribeImpl, judgeImpl });
  assert.equal(report.ok, true);
  assert.equal(report.owner_listened, false);
  assert.equal(report.full_video_approved, false);
  assert.match(report.narration_sha256, /^[a-f0-9]{64}$/);
  await checkOpening(item, { client, transcribeImpl, judgeImpl });
  assert.equal(transcribed, 4);
  assert.equal(judged, 1);
  writeFileSync(path.join(item.directory, "zh-TW.srt"), "wrong captions");
  await assert.rejects(checkOpening(item, { client, transcribeImpl, judgeImpl }), /captions changed/);
  assert.equal(transcribed, 4);
});
