import assert from "node:assert/strict";
import { copyFileSync, existsSync, mkdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { EXIT, main } from "../cli.mjs";
import { LEASE_FILE } from "../core/project-lease.mjs";
import { sha256File } from "../core/approvals.mjs";
import { brandingHash, pinBranding } from "../core/branding.mjs";
import { fixture, sandbox } from "../core/fixtures/load.mjs";
import { eachLine, textHash } from "../core/schema.mjs";
import { dubArtifacts, loadProject } from "../core/state.mjs";
import { estimateTimeline, framesFor, msToSamples, SAMPLE_RATE, SAMPLES_PER_FRAME } from "../core/timeline.mjs";
import { concatSamples, encodeWav, parseWav } from "../tts/wav.mjs";
import { encodeArgs, stretchArgs } from "./encode.mjs";
import {
  BUDGET_MARGIN, DEFAULT_RATES, DUB_STYLES, GAP_MS, GUARD_MS, LINE_OVERHEAD_MS, MAX_TEMPO, RATE_RATIOS,
  assembleTrack, defaultRate, dubLexicon, dubRequests, dubScript, estimatedLengths, layoutDub, layoutWindow, lineBudgets, measureRate, narrationRate, placeLines, shrinkBudgets, translationHash, windowsOf,
} from "./plan.mjs";

// The fixture videos run seconds; the eight-minute floor has tests of its own.
process.env.VIDEO_MIN_EPISODE_MINUTES ??= "0";

const TOKEN = `mkv_${"t".repeat(43)}`;
const ms = (value) => Math.round((value / 1000) * SAMPLE_RATE);
const tone = (milliseconds) => Int16Array.from({ length: ms(milliseconds) }, (_, index) => Math.round(8000 * Math.sin(index / 7)));
const quiet = (milliseconds) => new Int16Array(ms(milliseconds));

/** A translation file with every line current; `textFor` gives each line's words. */
function translationFor(doc, textFor) {
  const lines = {};
  for (const { line } of eachLine(doc)) lines[line.id] = { source_hash: textHash(line.text), text: textFor(line) };
  return { title: "T", description: "D", tags: [], chapters: {}, source_hashes: {}, lines };
}

const geminiDoc = (doc) => ({ ...doc, voice: { provider: "gemini", name: "Sulafat", style: "Taiwan Mandarin, relaxed." } });

test("a dub reads the translation with the locale's style and only the Latin spoken forms", () => {
  const lexicon = { schema_version: 1, terms: { API: "A P I", p95: "P 九十五", Claude: null } };
  assert.deepEqual(dubLexicon(lexicon).terms, { API: "A P I", p95: null, Claude: null });

  const doc = geminiDoc(fixture());
  const translation = translationFor(doc, (line) => `EN ${line.id}`);
  const { doc: script, missing } = dubScript(doc, translation, "en");
  assert.deepEqual(missing, []);
  assert.equal(script.voice.style, DUB_STYLES.en);
  assert.equal(script.voice.name, "Sulafat");
  assert.ok(!("rate" in script.voice));
  const lines = [...eachLine(script)].map(({ line }) => line);
  assert.ok(lines.every((line) => line.text.startsWith("EN ") && !("say" in line)), "the zh-TW spoken form does not apply to a dub");
  assert.equal(dubScript(doc, translation, "ja", "Custom style").doc.voice.style, "Custom style");

  const stale = { ...translation, lines: { ...translation.lines, k7p2: { source_hash: "000000000000", text: "old" } } };
  const partial = dubScript(doc, stale, "en");
  assert.deepEqual(partial.missing, ["k7p2"]);
  assert.equal([...eachLine(partial.doc)][0].line.text, doc.scenes[0].lines[0].text, "a missing translation keeps the zh-TW text so the planner still runs");

  const other = translationFor(doc, (line) => (line.id === "m4qa" ? "changed" : `EN ${line.id}`));
  assert.notEqual(translationHash(script), translationHash(dubScript(doc, other, "en").doc));
});

test("windows are the slide states, and a window keeps, packs, speeds up or overflows", () => {
  const doc = fixture();
  const timeline = estimateTimeline(doc);
  const windows = windowsOf(timeline);
  // hook (2 lines, one state), questions (3 lines, a reveal each), wrap (2 lines).
  assert.deepEqual(windows.map((window) => window.lines), [["k7p2", "m4qa"], ["x9fe"], ["b3tn"], ["r8wd"], ["h2cz", "p5vs"]]);
  assert.equal(windows[0].start_frame, 0);
  assert.equal(windows.at(-1).end_frame, timeline.total_frames);

  const originals = new Map(timeline.lines.map((line) => [line.id, line]));
  const hook = windows[0];
  const span = (hook.end_frame - hook.start_frame) * SAMPLES_PER_FRAME;
  const share = (fraction) => Math.round(span * fraction);
  const gap = framesFor(msToSamples(GAP_MS));
  const limit = hook.end_frame - framesFor(msToSamples(GUARD_MS));

  const kept = layoutWindow(hook, originals, new Map([["k7p2", share(0.2)], ["m4qa", share(0.2)]]));
  assert.equal(kept.tempo, 1);
  assert.equal(kept.kept_starts, true);
  assert.deepEqual(kept.lines.map((line) => line.start_frame), ["k7p2", "m4qa"].map((id) => originals.get(id).start_frame), "with room to spare, each line starts where its zh-TW line did");

  const packed = layoutWindow(hook, originals, new Map([["k7p2", share(0.2)], ["m4qa", share(0.7)]]));
  assert.equal(packed.tempo, 1);
  assert.equal(packed.kept_starts, false);
  assert.equal(packed.lines[1].start_frame, packed.lines[0].end_frame + gap, "a long second line starts right after the first, not at its zh-TW time");
  assert.ok(packed.lines[1].end_frame <= limit);

  const sped = layoutWindow(hook, originals, new Map([["k7p2", share(0.5)], ["m4qa", share(0.55)]]));
  assert.ok(sped.tempo > 1 && sped.tempo <= MAX_TEMPO, `tempo ${sped.tempo}`);
  assert.equal(sped.over, false);
  assert.ok(sped.lines[1].end_frame <= limit);
  assert.equal(sped.lines[0].audio_samples, Math.round(share(0.5) / sped.tempo));

  const over = layoutWindow(hook, originals, new Map([["k7p2", share(0.8)], ["m4qa", share(0.8)]]));
  assert.equal(over.over, true);
  assert.equal(over.tempo, MAX_TEMPO);
  assert.ok(over.slack_frames < 0);

  const all = layoutDub(timeline, new Map(timeline.lines.map((line) => [line.id, Math.round(line.audio_samples / 2)])));
  assert.equal(all.length, windows.length);
  assert.ok(all.every((window) => window.tempo === 1 && !window.over));
  assert.deepEqual(placeLines(hook, originals, new Map([["k7p2", 3200], ["m4qa", 3200]]), { tempo: 2 }).map((line) => line.audio_samples), [1600, 1600]);
});

test("budgets follow the slot and the rate; an overflowing window shrinks every line by the same share", () => {
  const doc = fixture();
  const timeline = estimateTimeline(doc);
  const budgets = lineBudgets(timeline, 15);
  const first = timeline.lines[0];
  const seconds = (first.end_frame - first.start_frame) / 30 - (GAP_MS + LINE_OVERHEAD_MS) / 1000;
  assert.equal(budgets[first.id], Math.floor(seconds * 15 * MAX_TEMPO * BUDGET_MARGIN));
  assert.ok(Object.values(budgets).every((value) => Number.isInteger(value) && value >= 1));

  const originals = new Map(timeline.lines.map((line) => [line.id, line]));
  const hook = windowsOf(timeline)[0];
  const span = (hook.end_frame - hook.start_frame) * SAMPLES_PER_FRAME;
  const over = layoutWindow(hook, originals, new Map([["k7p2", Math.round(span * 0.8)], ["m4qa", Math.round(span * 0.8)]]));
  const texts = new Map([["k7p2", "a".repeat(100)], ["m4qa", "b".repeat(50)]]);
  const shrunk = shrinkBudgets(over, texts, { lengths: new Map([["k7p2", 3 * SAMPLE_RATE], ["m4qa", 2 * SAMPLE_RATE]]) });
  assert.deepEqual(shrunk.map((line) => line.id), ["k7p2", "m4qa"]);
  assert.ok(shrunk.every((line) => line.max_chars < line.chars && line.max_chars >= 1));
  assert.ok(Math.abs(shrunk[0].max_chars / 100 - shrunk[1].max_chars / 50) < 0.05, "the same share for every line");
  assert.deepEqual(shrunk.map((line) => line.seconds), [3, 2]);
  assert.ok(shrunk[0].window_over_seconds > 0);
  assert.equal(shrinkBudgets(over, texts)[0].seconds, undefined, "seconds only when the clips are known");

  assert.equal(measureRate(new Map([["a", "abcde"], ["b", "fghij"]]), new Map([["a", SAMPLE_RATE], ["b", SAMPLE_RATE]])), 5);
  assert.equal(measureRate(new Map([["a", "abc"]]), new Map()), null);
  assert.equal(estimatedLengths(new Map([["a", "x".repeat(15)]]), 15).get("a"), SAMPLE_RATE);

  // Before a dub is measured, its rate is the narration's own rate scaled per language.
  const anchor = narrationRate(doc, timeline);
  assert.ok(anchor > 0);
  assert.equal(defaultRate("en", doc, timeline), Math.round(anchor * RATE_RATIOS.en * 100) / 100);
  assert.equal(defaultRate("en", doc, null), DEFAULT_RATES.en, "without a timeline, the fixed starting value");
});

test("the track is the video's length with each clip at its frame", () => {
  const clip = Int16Array.from({ length: 2 * SAMPLES_PER_FRAME }, (_, index) => index % 100);
  const lines = [{ id: "a", start_frame: 10, end_frame: 12, audio_samples: clip.length }];
  const track = assembleTrack(100, lines, new Map([["a", clip]]));
  assert.equal(track.length, 100 * SAMPLES_PER_FRAME);
  assert.equal(track[10 * SAMPLES_PER_FRAME + 1], 1);
  assert.equal(track[10 * SAMPLES_PER_FRAME - 1], 0);
  assert.throws(() => assembleTrack(100, [{ id: "a", start_frame: 10, end_frame: 11 }], new Map([["a", clip]])), /its slot/);
  assert.throws(() => assembleTrack(11, lines, new Map([["a", clip]])), /past the end/);
});

test("ffmpeg arguments: pitch-kept tempo, then the video's loudness and the upload codec", () => {
  assert.ok(stretchArgs("in.wav", 1.1, "out.wav").includes("atempo=1.1"));
  const measured = { input_i: "-20.1", input_tp: "-3.2", input_lra: "5.5", input_thresh: "-30.4", target_offset: "0.3" };
  const m4a = encodeArgs("track.wav", measured, "en.m4a", "m4a");
  assert.ok(m4a.includes("aac") && m4a.includes("384k") && m4a.at(-1) === "en.m4a");
  assert.ok(m4a.find((arg) => String(arg).includes("loudnorm=I=-14:TP=-1:LRA=11:measured_I=-20.1")));
  assert.ok(encodeArgs("track.wav", measured, "en.mp3", "mp3").includes("libmp3lame"));
  assert.ok(encodeArgs("track.wav", measured, "en.wav", "wav").includes("pcm_s16le"));
  assert.throws(() => encodeArgs("track.wav", measured, "en.ogg", "ogg"), /unknown dub format/);
});

/** The narration server: status with a Gemini month, and 60 ms of tone a character plus the break. */
function fakeServer() {
  const calls = [];
  const fetchImpl = async (url, init) => {
    calls.push({ url, init });
    if (url.endsWith("/api/video/speech/status")) {
      return Response.json({ configured: false, voices: [], monthly_limit: 0, used: 0, remaining: 0, gemini_configured: true, gemini_monthly_limit: 300000, gemini_used: 1000 });
    }
    const body = JSON.parse(init.body);
    const audio = concatSamples(body.segments.flatMap((segment) => [tone(segment.parts.reduce((sum, part) => sum + part.text.length, 0) * 60), quiet(segment.break_after_ms)]));
    return new Response(encodeWav(audio), { status: 200, headers: { "Content-Type": "audio/wav", "X-Billable-Characters": "10" } });
  };
  return { calls, fetchImpl };
}

/** ffmpeg as the dub sees it: a measurement, a shortened copy for atempo, a plain copy otherwise. */
function fakeFfmpeg() {
  const calls = [];
  return {
    calls,
    locate: async () => ({ ffmpeg: "ffmpeg", ffprobe: "ffprobe", version: "fake ffmpeg" }),
    run: async (file, args) => {
      calls.push(args);
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

/**
 * The narration the dubs are read against, made by tts. At this server's 60 ms a character the
 * fixtures' chapters run under the 10 s YouTube needs, which tts reports with exit 1 once every
 * file is written. A dub reads the timeline, not the chapters, and these tests size their
 * translations to the windows this pace makes, so the pace stays.
 */
async function narrate(box, server, ffmpeg, slug = box.slug) {
  const { ctx, out } = capture(box, server, ffmpeg);
  const code = await main(["tts", "--slug", slug], ctx);
  const chaptersOnly = code === EXIT.lint && /requests synthesized/.test(out.stdout) && /^chapters: /m.test(out.stdout);
  assert.ok(code === EXIT.ok || chaptersOnly, out.stdout + out.stderr);
}

function capture(box, server, ffmpeg) {
  const out = { stdout: "", stderr: "" };
  const ctx = {
    root: box.root,
    env: { VIDEO_WORKDIR: box.work, MOKAAIR_VIDEO_TOKEN: TOKEN },
    home: box.base,
    stdout: { write: (text) => (out.stdout += text) },
    stderr: { write: (text) => (out.stderr += text) },
    now: () => new Date("2026-09-27T07:00:00Z"),
    fetch: server.fetchImpl,
    sleep: async () => {},
    ffmpeg,
  };
  return { ctx, out };
}

test("adding branding reuses dubbed speech, wraps the upload audio and offsets only presentation timing", async () => {
  const box = sandbox();
  const doc = geminiDoc(fixture());
  writeFileSync(path.join(box.dir, "video.json"), JSON.stringify(doc));
  mkdirSync(path.join(box.dir, "i18n"), { recursive: true });
  writeFileSync(path.join(box.dir, "i18n", "en.json"), JSON.stringify(translationFor(doc, (line) => `EN ${line.id}`)));
  const server = fakeServer();
  const ffmpeg = fakeFfmpeg();
  await narrate(box, server, ffmpeg);
  assert.equal(await main(["dub", "--slug", box.slug, "--locale", "en"], capture(box, server, ffmpeg).ctx), EXIT.ok);
  const files = dubArtifacts(box.workdir, "en");
  const before = JSON.parse(readFileSync(files.timeline, "utf8"));
  const bodyNarrationHash = await sha256File(files.narration);
  const selection = { schema_version: 1, id: "channel-v1" };
  for (const [role, frames] of [["intro", 150], ["outro", 90]]) {
    const file = path.join(box.base, `${role}.mp4`);
    writeFileSync(file, role);
    selection[role] = { file, frames, sha256: await sha256File(file) };
  }
  pinBranding(box.workdir, selection);
  writeFileSync(path.join(box.workdir, "checks.json"), JSON.stringify({ speech_hash: before.speech_hash, branding: { hash: brandingHash(selection), intro_frames: 150, outro_frames: 90, body_frames: before.total_frames } }));
  const originalRun = ffmpeg.run;
  ffmpeg.run = async (tool, args) => {
    if (tool !== "ffprobe") return originalRun(tool, args);
    const frames = path.basename(args.at(-1)) === "intro.mp4" ? 150 : 90;
    return { stdout: JSON.stringify({ streams: [{ codec_type: "video", width: 1920, height: 1080, r_frame_rate: "30/1", nb_read_packets: String(frames) }, { codec_type: "audio", duration: frames / 30 }] }), stderr: "" };
  };
  const count = server.calls.length;
  const run = capture(box, server, ffmpeg);
  assert.equal(await main(["dub", "--slug", box.slug, "--locale", "en"], run.ctx), EXIT.ok, run.out.stderr);
  assert.equal(server.calls.length, count + 1, "only a status read; cached speech is not generated again");
  assert.equal(await sha256File(files.narration), bodyNarrationHash, "body narration is byte-identical");
  const after = JSON.parse(readFileSync(files.timeline, "utf8"));
  assert.equal(after.total_frames, before.total_frames + 240);
  assert.equal(after.content_end_frame, before.total_frames + 150);
  assert.deepEqual(after.lines.map((line) => line.start_frame), before.lines.map((line) => line.start_frame + 150));
  assert.deepEqual(after.windows.map((window) => window.start_frame), before.windows.map((window) => window.start_frame + 150));
  const wrap = ffmpeg.calls.findLast((args) => args.some((arg) => String(arg).includes("concat=n=3:v=0:a=1")));
  assert.ok(wrap, "the encoded body is joined to both bumper audio streams");
  assert.equal(wrap.at(-1), path.join(files.dir, "branded.partial.m4a"));
  assert.ok(existsSync(path.join(files.dir, "body.m4a")));
  const trackHash = await sha256File(files.track("m4a"));
  const timelineHash = await sha256File(files.timeline);
  const successRun = ffmpeg.run;
  ffmpeg.run = async (tool, args) => {
    if (tool === "ffmpeg" && args.some((arg) => String(arg).includes("concat=n=3:v=0:a=1"))) {
      writeFileSync(args.at(-1), "interrupted encoder output");
      throw new Error("wrapper interrupted");
    }
    return successRun(tool, args);
  };
  await assert.rejects(main(["dub", "--slug", box.slug, "--locale", "en"], capture(box, server, ffmpeg).ctx), /wrapper interrupted/);
  assert.equal(await sha256File(files.track("m4a")), trackHash, "an interrupted rerun preserves the finished track");
  assert.equal(await sha256File(files.timeline), timelineHash, "the finished track retains its matching timeline");
  const bodyFile = path.join(box.workdir, "timeline.json");
  const changedBody = JSON.parse(readFileSync(bodyFile, "utf8"));
  changedBody.total_frames += 30;
  writeFileSync(bodyFile, JSON.stringify(changedBody));
  const stale = capture(box, server, ffmpeg);
  assert.equal(await main(["status", "--slug", box.slug], stale.ctx), EXIT.ok);
  assert.match(stale.out.stdout, /en stale/);
  assert.equal(await main(["dub", "--slug", box.slug, "--locale", "en"], capture(box, server, ffmpeg).ctx), EXIT.usage, "re-timed TTS requires a new assembled cut first");
});

test("dub writes a track per locale, speeds up a tight window, and reports a window that cannot fit", async () => {
  const box = sandbox();
  const doc = geminiDoc(fixture());
  writeFileSync(path.join(box.dir, "video.json"), `${JSON.stringify(doc, null, 2)}\n`);
  mkdirSync(path.join(box.dir, "i18n"), { recursive: true });
  // en fits with room; ko's opening two lines need a speed-up; ja's first line is far too long.
  const texts = {
    en: (line) => `EN ${line.id}`,
    ko: (line) => (line.id === "k7p2" ? "k".repeat(42) : line.id === "m4qa" ? "m".repeat(46) : `KO ${line.id}`),
    ja: (line) => (line.id === "k7p2" ? "j".repeat(200) : `JA ${line.id}`),
  };
  for (const [locale, textFor] of Object.entries(texts)) writeFileSync(path.join(box.dir, "i18n", `${locale}.json`), JSON.stringify(translationFor(doc, textFor)));
  const server = fakeServer();
  const ffmpeg = fakeFfmpeg();

  await narrate(box, server, ffmpeg);
  const timeline = JSON.parse(readFileSync(path.join(box.workdir, "timeline.json"), "utf8"));

  const dry = capture(box, server, ffmpeg);
  assert.equal(await main(["dub", "--slug", box.slug, "--locale", "en", "--dry-run"], dry.ctx), EXIT.ok);
  assert.match(dry.out.stdout, /en: \d+ requests, \d+ to synthesize/);
  assert.match(dry.out.stdout, /0 would not fit/);
  assert.match(dry.out.stdout, /299000 characters left this month/);
  assert.equal(ffmpeg.calls.length, 0, "a dry run runs no ffmpeg");

  const unchosen = capture(box, server, ffmpeg);
  assert.equal(await main(["dub", "--slug", box.slug, "--dry-run"], unchosen.ctx), EXIT.ok);
  // Every dub locale without a choice; zh-CN, once left out here, is no longer a video language (2026-10-09).
  for (const locale of ["en", "ja", "ko"]) assert.match(unchosen.out.stdout, new RegExp(`^${locale}: `, "m"));

  const sheet = capture(box, server, ffmpeg);
  assert.equal(await main(["i18n-sheet", "--slug", box.slug, "--locale", "en"], sheet.ctx), EXIT.ok);
  const worksheet = JSON.parse(readFileSync(path.join(box.workdir, "i18n", "en.todo.json"), "utf8"));
  assert.ok(worksheet.lines.every((line) => Number.isInteger(line.max_chars) && line.max_chars >= 1), "the sheet carries a dub budget once the narration is timed");
  assert.match(worksheet.note, /max_chars/);

  const run = capture(box, server, ffmpeg);
  assert.equal(await main(["dub", "--slug", box.slug, "--locale", "en,ko,ja"], run.ctx), EXIT.lint, "ja cannot fit, so the run reports it");
  const en = dubArtifacts(box.workdir, "en");
  assert.ok(existsSync(en.track("m4a")), "the English track was encoded");
  const enTimeline = JSON.parse(readFileSync(en.timeline, "utf8"));
  assert.equal(enTimeline.total_frames, timeline.total_frames);
  assert.equal(enTimeline.lines.length, timeline.lines.length);
  assert.ok(enTimeline.lines.every((line) => line.tempo === 1));
  assert.deepEqual(enTimeline.lines.map((line) => line.scene), timeline.lines.map((line) => line.scene), "each dubbed line names its scene, as the narration's does");
  assert.equal(enTimeline.translation_hash, translationHash(dubScript(doc, translationFor(doc, texts.en), "en").doc));
  const enTrack = parseWav(readFileSync(en.narration));
  assert.equal(enTrack.samples.length, timeline.total_frames * SAMPLES_PER_FRAME, "the track is exactly the video's length");
  const enFit = JSON.parse(readFileSync(en.fit, "utf8"));
  assert.deepEqual(enFit.over, []);
  assert.ok(enFit.rates.measured > 0);

  const ko = dubArtifacts(box.workdir, "ko");
  const koTimeline = JSON.parse(readFileSync(ko.timeline, "utf8"));
  const opening = koTimeline.windows[0];
  assert.ok(opening.tempo > 1 && opening.tempo <= MAX_TEMPO, `ko opening window tempo ${opening.tempo}`);
  assert.ok(existsSync(path.join(ko.audio, `k7p2.x${opening.tempo.toFixed(2)}.wav`)), "the sped-up take is kept beside the clip");
  assert.ok(koTimeline.windows.slice(1).every((window) => window.tempo === 1));
  assert.ok(existsSync(ko.track("m4a")));
  assert.match(run.out.stdout, /ko: .*1 of 5 windows sped up/);

  const ja = dubArtifacts(box.workdir, "ja");
  assert.ok(!existsSync(ja.track("m4a")), "no track for a locale that does not fit");
  assert.ok(!existsSync(ja.timeline));
  const jaFit = JSON.parse(readFileSync(ja.fit, "utf8"));
  assert.equal(jaFit.over.length, 2, "both lines of the overflowing window get a budget");
  const long = jaFit.over.find((line) => line.id === "k7p2");
  assert.equal(long.chars, 200);
  assert.ok(long.max_chars < 200 && long.max_chars >= 1);
  assert.match(run.out.stdout, /ja: .*1 windows do not fit even at 1.15x/);
  assert.match(run.out.stdout, /k7p2: \d+ characters \(now 200, spoken in [\d.]+ s; its window is [\d.]+ s over\)/);

  const again = capture(box, server, ffmpeg);
  const synthesized = server.calls.length;
  assert.equal(await main(["dub", "--slug", box.slug, "--locale", "en"], again.ctx), EXIT.ok);
  assert.match(again.out.stdout, /en: 0 requests synthesized \(0 billable characters\), \d+ reused/);
  assert.equal(server.calls.length, synthesized + 1, "only the status call: every clip came from the cache");

  const status = capture(box, server, ffmpeg);
  await main(["status", "--slug", box.slug], status.ctx);
  assert.match(status.out.stdout, /dubs: en current \(en\.m4a\); ja over \(2 lines to shorten \(dubs\/ja\/fit\.json\)\); ko current \(ko\.m4a\)/);

  // A retake through the flags file re-records one line and drops its sped-up copy.
  const flags = path.join(box.workdir, "review", "check-flags.ko.json");
  mkdirSync(path.dirname(flags), { recursive: true });
  writeFileSync(flags, JSON.stringify({ flags: ["k7p2"] }));
  const redo = capture(box, server, ffmpeg);
  assert.equal(await main(["dub", "--slug", box.slug, "--locale", "ko", "--redo", flags], redo.ctx), EXIT.ok);
  assert.match(redo.out.stdout, /ko: 1 requests synthesized/);
});

test("--line-by-line sends one request a line, so a scene is never paid for twice", async () => {
  const box = sandbox();
  const doc = geminiDoc(fixture());
  writeFileSync(path.join(box.dir, "video.json"), `${JSON.stringify(doc, null, 2)}\n`);
  mkdirSync(path.join(box.dir, "i18n"), { recursive: true });
  writeFileSync(path.join(box.dir, "i18n", "en.json"), JSON.stringify(translationFor(doc, (line) => `EN ${line.id}`)));
  const server = fakeServer();
  const ffmpeg = fakeFfmpeg();
  await narrate(box, server, ffmpeg);

  const before = server.calls.length;
  const run = capture(box, server, ffmpeg);
  assert.equal(await main(["dub", "--slug", box.slug, "--locale", "en", "--line-by-line"], run.ctx), EXIT.ok);
  const bodies = server.calls.slice(before).filter((call) => !call.url.endsWith("/status")).map((call) => JSON.parse(call.init.body));
  const lines = [...eachLine(doc)].length;
  assert.ok(lines > [...new Set([...eachLine(doc)].map(({ scene }) => scene.id))].length, "the fixture has scenes of more than one line");
  assert.equal(bodies.length, lines, "one request for each line");
  assert.ok(bodies.every((body) => body.segments.length === 1), "each request carries a single line");
  assert.doesNotMatch(run.out.stdout, /fallback/);
  assert.ok(existsSync(dubArtifacts(box.workdir, "en").track("m4a")));
});

test("a STOP file ends a dub as incomplete: the takes so far are kept, no fit report, timeline or track is written, and the rerun buys only the rest", async () => {
  const box = sandbox();
  const doc = geminiDoc(fixture());
  writeFileSync(path.join(box.dir, "video.json"), `${JSON.stringify(doc, null, 2)}\n`);
  mkdirSync(path.join(box.dir, "i18n"), { recursive: true });
  for (const locale of ["en", "ja"]) writeFileSync(path.join(box.dir, "i18n", `${locale}.json`), JSON.stringify(translationFor(doc, (line) => `${locale} ${line.id}`)));
  const server = fakeServer();
  const ffmpeg = fakeFfmpeg();
  await narrate(box, server, ffmpeg);
  const posts = () => server.calls.filter((call) => call.url.endsWith("/api/video/speech")).length;
  const narrated = posts();
  const stop = path.join(box.work, "STOP");
  // The owner drops a STOP file while the dub's request number `dropAt` is being answered.
  let dropAt = null;
  const owner = {
    calls: server.calls,
    fetchImpl: async (url, init) => {
      const response = await server.fetchImpl(url, init);
      if (url.endsWith("/api/video/speech") && posts() - narrated === dropAt) writeFileSync(stop, "");
      return response;
    },
  };
  const dub = async (...args) => {
    const { ctx, out } = capture(box, owner, ffmpeg);
    return { code: await main(["dub", "--slug", box.slug, ...args], ctx), ...out };
  };
  const en = dubArtifacts(box.workdir, "en");
  const made = () => [en.fit, en.timeline, en.narration, en.track("m4a")].filter((file) => existsSync(file));
  const { requests } = dubRequests(loadProject({ slug: box.slug, root: box.root }), "en");
  assert.equal(requests.length, 3, "a request a scene");

  // A STOP file already there: nothing is bought.
  writeFileSync(stop, "");
  const before = await dub("--locale", "en");
  assert.equal(before.code, EXIT.incomplete, before.stderr);
  assert.match(before.stdout, /^en: stopped by the STOP file; 0 of 3 requests done, rerun to continue$/m);
  assert.equal(posts(), narrated);
  assert.deepEqual(made(), []);

  // Dropped while the first request is answered: its takes are kept, and the next locale is not started.
  rmSync(stop);
  dropAt = 1;
  const stopped = await dub("--locale", "en,ja");
  assert.equal(stopped.code, EXIT.incomplete, stopped.stderr);
  assert.match(stopped.stdout, /^en: stopped by the STOP file; 1 of 3 requests done, rerun to continue$/m);
  assert.doesNotMatch(stopped.stdout, /^(ja|next)\b/m, "the STOP file stops the next locale too, and check-audio is not next");
  assert.equal(posts(), narrated + 1);
  const cache = JSON.parse(readFileSync(en.cache, "utf8"));
  assert.deepEqual(Object.keys(cache.lines), requests[0].lines.map((line) => line.id));
  for (const line of requests[0].lines) {
    assert.equal(cache.lines[line.id], line.key, `${line.id}'s take is kept`);
    assert.ok(existsSync(path.join(en.audio, `${line.id}.wav`)));
  }
  assert.deepEqual(made(), [], "no fit report, timeline or track");
  assert.equal(existsSync(dubArtifacts(box.workdir, "ja").dir), false);

  // With the STOP file still there, the next run stops before it pays for anything.
  const held = await dub("--locale", "en");
  assert.equal(held.code, EXIT.incomplete);
  assert.match(held.stdout, /^en: stopped by the STOP file; 0 of 2 requests done/m);
  assert.equal(posts(), narrated + 1);

  rmSync(stop);
  const resumed = await dub("--locale", "en");
  assert.equal(resumed.code, EXIT.ok, resumed.stderr);
  assert.equal(posts(), narrated + 3, "only the two requests left are synthesized");
  assert.match(resumed.stdout, /^en: 2 requests synthesized \(20 billable characters\), 1 reused;/m);
  assert.deepEqual(made(), [en.fit, en.timeline, en.narration, en.track("m4a")]);

  // A retake the STOP file ends leaves the made track as it was, and the next plain run lays the
  // takes out again without buying any (the worker's next run, automation/flow.mjs makeDub).
  const flags = path.join(box.workdir, "review", "check-flags.en.json");
  mkdirSync(path.dirname(flags), { recursive: true });
  writeFileSync(flags, JSON.stringify({ flags: [requests[0].lines[0].id, requests[2].lines[0].id] }));
  const hashes = () => Promise.all(made().map((file) => sha256File(file)));
  const kept = await hashes();
  dropAt = posts() - narrated + 1;
  const retake = await dub("--locale", "en", "--redo", flags);
  assert.equal(retake.code, EXIT.incomplete, retake.stderr);
  assert.match(retake.stdout, /^en: stopped by the STOP file; 1 of 2 requests done, rerun to continue$/m);
  assert.deepEqual(await hashes(), kept, "the fit report, timeline and track are the last made ones");
  rmSync(stop);
  const paid = posts();
  const remade = await dub("--locale", "en");
  assert.equal(remade.code, EXIT.ok, remade.stderr);
  assert.equal(posts(), paid, "every take is in the cache");
  assert.match(remade.stdout, /^en: 0 requests synthesized \(0 billable characters\), 3 reused;/m);
});

test("dub refuses what it cannot do: an Azure voice, a missing timeline, a bad locale or format", async () => {
  const box = sandbox();
  const server = fakeServer();
  const ffmpeg = fakeFfmpeg();
  const azure = capture(box, server, ffmpeg);
  assert.equal(await main(["dub", "--slug", box.slug, "--locale", "en"], azure.ctx), EXIT.owner);
  assert.match(azure.out.stderr, /Gemini voice/);

  writeFileSync(path.join(box.dir, "video.json"), `${JSON.stringify(geminiDoc(fixture()), null, 2)}\n`);
  const untimed = capture(box, server, ffmpeg);
  assert.equal(await main(["dub", "--slug", box.slug, "--locale", "en"], untimed.ctx), EXIT.usage);
  assert.match(untimed.out.stderr, /run tts first/);
  assert.equal(await main(["dub", "--slug", box.slug, "--locale", "fr"], capture(box, server, ffmpeg).ctx), EXIT.usage);
  assert.equal(await main(["dub", "--slug", box.slug, "--format", "ogg"], capture(box, server, ffmpeg).ctx), EXIT.usage);

  await narrate(box, server, ffmpeg);
  const missing = capture(box, server, ffmpeg);
  assert.equal(await main(["dub", "--slug", box.slug, "--locale", "en"], missing.ctx), EXIT.lint, "no translation yet");
  assert.match(missing.out.stdout, /en: no track; 7 lines have no current translation/);
});

test("a dub of an illustrated video carries the music bed and the cut's effects track in its own format, and status marks it stale when they change", async () => {
  const { illustratedFixture, illustratedBrief } = await import("../core/fixtures/load.mjs");
  const { mixHash, sfxHash } = await import("../core/drama.mjs");
  const { speechHash } = await import("../core/timeline.mjs");
  const { readJson } = await import("../core/paths.mjs");
  const slug = "ranking-first";
  const box = sandbox(slug, "illustrated");
  const doc = { ...illustratedFixture(), slug, voice: { provider: "gemini", name: "Sulafat", style: "說書人" } };
  writeFileSync(path.join(box.dir, "video.json"), `${JSON.stringify(doc, null, 2)}\n`);
  writeFileSync(path.join(box.dir, "brief.md"), illustratedBrief());
  mkdirSync(path.join(box.dir, "i18n"), { recursive: true });
  writeFileSync(path.join(box.dir, "i18n", "en.json"), JSON.stringify(translationFor(doc, (line) => `EN ${line.id}`)));
  // The owner's licensed bed and effect set, as assemble reads them (docs/videos/ILLUSTRATED.md).
  mkdirSync(path.join(box.work, "_music"), { recursive: true });
  writeFileSync(path.join(box.work, "_music", "bed.mp3"), "bed bytes");
  const sfxDir = path.join(box.work, "_sfx", "studio-a");
  mkdirSync(sfxDir, { recursive: true });
  const sounds = {};
  for (const name of ["stamp", "whoosh", "pop"]) {
    writeFileSync(path.join(sfxDir, `${name}.wav`), `${name} bytes`);
    sounds[name] = { file: `${name}.wav` };
  }
  writeFileSync(path.join(sfxDir, "manifest.json"), JSON.stringify({ source: "test", license: "test", sounds }));
  const server = fakeServer();
  const ffmpeg = fakeFfmpeg();
  await narrate(box, server, ffmpeg, slug);
  const timeline = readJson(path.join(box.workdir, "timeline.json"));

  // Before the cut is assembled: the bed is mixed, the effects wait for assemble.
  const early = capture(box, server, ffmpeg);
  assert.equal(await main(["dub", "--slug", slug, "--locale", "en", "--format", "mp3"], early.ctx), EXIT.ok);
  assert.match(early.out.stdout, /en: .*; with the music bed; .*en\.mp3/);
  assert.match(early.out.stdout, /no effects track yet: run assemble first/);
  const en = dubArtifacts(box.workdir, "en");
  const mixed = ffmpeg.calls.filter((args) => args.includes("-filter_complex"));
  assert.ok(mixed.length >= 2, "a measurement pass and an encoding pass through the mix graph");
  const encode = mixed.at(-1);
  assert.ok(encode.includes(path.join(box.work, "_music", "bed.mp3")), "the bed is an input");
  assert.equal(encode.filter((arg) => arg === "-i").length, 2, "voice and bed, no effects yet");
  assert.deepEqual(encode.slice(encode.indexOf("-c:a"), encode.indexOf("-c:a") + 4), ["-c:a", "libmp3lame", "-b:a", "320k"], "the dub's upload format, not the cut's AAC");
  assert.match(encode.join(" "), /sidechaincompress|amix/);
  let record = readJson(en.timeline);
  assert.equal(record.mix_hash, mixHash(doc));
  assert.equal(record.sfx_hash, null, "no effects were carried");
  const waiting = capture(box, server, ffmpeg);
  await main(["status", "--slug", slug], waiting.ctx);
  assert.match(waiting.out.stdout, /dubs: en stale \(made without the video's music or sound effects; run dub again\)/);

  // The cut exists: its effects track is reused under the dub.
  mkdirSync(path.join(box.workdir, "build"), { recursive: true });
  writeFileSync(path.join(box.workdir, "build", "sfx.wav"), "effects bytes");
  writeFileSync(path.join(box.workdir, "checks.json"), JSON.stringify({ ok: true, speech_hash: speechHash(doc, readJson(path.join(box.videos, "lexicon.json"))), sfx_hash: sfxHash(doc) }));
  const calls = ffmpeg.calls.length;
  const full = capture(box, server, ffmpeg);
  assert.equal(await main(["dub", "--slug", slug, "--locale", "en", "--format", "mp3"], full.ctx), EXIT.ok);
  assert.match(full.out.stdout, /with the music bed and sound effects/);
  const withEffects = ffmpeg.calls.slice(calls).filter((args) => args.includes("-filter_complex")).at(-1);
  assert.ok(withEffects.includes(path.join(box.workdir, "build", "sfx.wav")));
  assert.equal(withEffects.filter((arg) => arg === "-i").length, 3, "voice, bed and effects");
  record = readJson(en.timeline);
  assert.equal(record.sfx_hash, sfxHash(doc));
  const current = capture(box, server, ffmpeg);
  await main(["status", "--slug", slug], current.ctx);
  assert.match(current.out.stdout, /dubs: en current \(en\.mp3\)/);

  // A louder bed in the script is a different mix: the dub is stale until made again.
  writeFileSync(path.join(box.dir, "video.json"), `${JSON.stringify({ ...doc, music: { ...doc.music, gain_db: -16 } }, null, 2)}\n`);
  const louder = capture(box, server, ffmpeg);
  await main(["status", "--slug", slug], louder.ctx);
  assert.match(louder.out.stdout, /dubs: en stale/);

  // A missing bed file is the owner's to put back, not a dry track.
  writeFileSync(path.join(box.dir, "video.json"), `${JSON.stringify({ ...doc, music: { track: "gone.mp3" } }, null, 2)}\n`);
  const gone = capture(box, server, ffmpeg);
  assert.equal(await main(["dub", "--slug", slug, "--locale", "en", "--format", "mp3"], gone.ctx), EXIT.usage);
  assert.match(gone.out.stderr, /cannot carry the music bed: music.track gone.mp3 is not in/);
});

test("a dub run by hand while another producer holds the project asks for no speech and writes no track", async () => {
  const box = sandbox();
  const doc = geminiDoc(fixture());
  writeFileSync(path.join(box.dir, "video.json"), JSON.stringify(doc));
  mkdirSync(path.join(box.dir, "i18n"), { recursive: true });
  writeFileSync(path.join(box.dir, "i18n", "en.json"), JSON.stringify(translationFor(doc, (line) => `EN ${line.id}`)));
  const server = fakeServer();
  const ffmpeg = fakeFfmpeg();
  await narrate(box, server, ffmpeg);
  writeFileSync(path.join(box.workdir, LEASE_FILE), JSON.stringify({ schema_version: 1, token: "11111111-2222-3333-4444-555555555555", owner: "auto", pid: 4242, host: "video-worker-elsewhere", boot_id: null, start_ticks: null, acquired_at: "2026-10-07T00:00:00.000Z" }));
  const calls = server.calls.length;
  const run = capture(box, server, ffmpeg);
  assert.equal(await main(["dub", "--slug", box.slug, "--locale", "en"], run.ctx), EXIT.owner);
  assert.match(run.out.stderr, /auto \(pid 4242 on video-worker-elsewhere.*nothing was sent or written/);
  assert.equal(server.calls.length, calls, "no speech request, not even the status");
  assert.equal(existsSync(dubArtifacts(box.workdir, "en").timeline), false);
});
