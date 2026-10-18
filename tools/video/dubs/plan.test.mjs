import assert from "node:assert/strict";
import { copyFileSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import test from "node:test";

import { EXIT, main } from "../cli.mjs";
import { enBrief, enFixture, fixture, fixtureBrief, fixtureLexicon } from "../core/fixtures/load.mjs";
import { eachLine, LOCALES, textHash } from "../core/schema.mjs";
import { dubArtifacts, lintProject, loadProject } from "../core/state.mjs";
import { estimateTimeline, FPS, framesFor, msToSamples, SAMPLE_RATE, SAMPLES_PER_FRAME, speechHash } from "../core/timeline.mjs";
import { checkFiles, dubLexicon as checkerDubLexicon, lexiconFor, spokenForm } from "../tts/check.mjs";
import { billableForRequest, geminiText, planRequests } from "../tts/requests.mjs";
import { concatSamples, encodeWav } from "../tts/wav.mjs";
import {
  GAP_MS, GUARD_MS, MAX_TEMPO, MAX_TEMPO_OVERRUN, OVERRUN_TOLERANCE_SECONDS,
  absorbOverruns, dubLexicon, dubScript, layoutDub, layoutDubTolerant, overrunSummary, shiftWindow, speechLexicon, windowLimit,
} from "./plan.mjs";

// The fixture videos run seconds; the eight-minute floor has tests of its own.
process.env.VIDEO_MIN_EPISODE_MINUTES ??= "0";

const WORDS = "App iOS API CBS OpenAI ChatGPT DevDay p95";
const RAW = {
  schema_version: 1,
  terms: {
    App: "A P P", iOS: "i O S", API: "A P I", CBS: "C B S", OpenAI: "Open A I",
    ChatGPT: "Chat G P T", DevDay: "Dev Day", p95: "P 九十五",
  },
};
const FOREIGN = "App iOS A P I C B S Open A I Chat G P T Dev Day p95";
const CHINESE = "A P P i O S A P I C B S Open A I Chat G P T Dev Day P 九十五";
const chinese = (locale) => locale === "zh-TW";

function script(text) {
  return {
    format: "slides",
    voice: { provider: "gemini", name: "Sulafat", style: "Conversational." },
    scenes: [{ id: "intro", lines: [{ id: "line1", text }] }],
  };
}

test("only full letter spellings of non-capitalized words lose their alias outside Chinese", () => {
  const terms = Object.freeze({
    ...RAW.terms, app: " a\tp  p ", IOS: "i o s", Camel: "c A m E l",
    Application: "App", Applet: "A P P", Word: "WORD", Another: "A.N.O.T.H.E.R",
    Claude: null, Japanese: "ｶﾀｶﾅ",
  });
  const lexicon = Object.freeze({ schema_version: 1, note: "shared shelf", terms });
  const before = structuredClone(lexicon);
  const selected = dubLexicon(lexicon);
  assert.deepEqual(selected.terms, {
    ...RAW.terms, App: null, iOS: null, p95: null, app: null, IOS: "i o s", Camel: null,
    Application: "App", Applet: "A P P", Word: "WORD", Another: "A.N.O.T.H.E.R",
    Claude: null, Japanese: null,
  });
  assert.equal(selected.note, "shared shelf");
  assert.deepEqual(lexicon, before, "selection never edits the shelf dictionary");
  assert.equal(checkerDubLexicon, dubLexicon, "the checker reexports the synthesis rule");
  assert.deepEqual(dubLexicon(undefined).terms, {});
});

for (const locale of LOCALES) {
  test(`${locale} request text and checked spoken form use the same pronunciation`, () => {
    const selected = speechLexicon(RAW, locale);
    const [request] = planRequests(script(WORDS), selected);
    const expected = chinese(locale) ? CHINESE : FOREIGN;
    assert.equal(geminiText(request.body.segments), expected);
    assert.equal(spokenForm({ text: WORDS }, lexiconFor(RAW, locale, "en")), expected);
    assert.deepEqual(lexiconFor(RAW, locale), selected);
    if (chinese(locale)) assert.equal(selected, RAW, "Chinese keeps the raw aliases");
  });
}

test("changed word pronunciations invalidate request and clip keys without invalidating acronyms", () => {
  const doc = script("App Store uses iOS and API.");
  const [old] = planRequests(doc, RAW);
  const [fixed] = planRequests(doc, speechLexicon(RAW, "en"));
  assert.equal(geminiText(old.body.segments), "A P P Store uses i O S and A P I.");
  assert.equal(geminiText(fixed.body.segments), "App Store uses iOS and A P I.");
  assert.notEqual(fixed.key, old.key);
  assert.notEqual(fixed.lines[0].key, old.lines[0].key);
  assert.deepEqual(planRequests(doc, speechLexicon(RAW, "zh-TW")), [old]);
  const unchanged = script("API CBS OpenAI ChatGPT DevDay");
  assert.deepEqual(planRequests(unchanged, dubLexicon(RAW)), planRequests(unchanged, RAW));
  assert.deepEqual(planRequests(doc, dubLexicon(RAW)), planRequests(doc, dubLexicon({
    ...RAW, terms: { ...RAW.terms, App: "a p p", iOS: "I o s" },
  })), "equivalent discarded aliases do not invalidate an already natural-word clip");
});

function writeJson(file, value) {
  mkdirSync(path.dirname(file), { recursive: true });
  writeFileSync(file, JSON.stringify(value));
}

function projectFixture(t, sourceLocale, targetLocale, external) {
  const base = mkdtempSync(path.join(tmpdir(), "dub-words-"));
  t.after(() => rmSync(base, { recursive: true, force: true }));
  const root = path.join(base, "repo");
  const shelf = external ? path.join(base, "external-shelf") : path.join(root, "docs", "videos");
  const doc = sourceLocale === "en" ? enFixture() : fixture();
  doc.voice = { provider: "gemini", name: "Sulafat", style: "Conversational." };
  const dir = path.join(shelf, doc.slug);
  const file = path.join(dir, "video.json");
  const work = path.join(base, "work");
  const workdir = path.join(work, doc.slug);
  const lexicon = { schema_version: 1, terms: { ...fixtureLexicon().terms, ...RAW.terms, Store: null } };
  writeJson(file, doc);
  writeFileSync(path.join(dir, "brief.md"), sourceLocale === "en" ? enBrief() : fixtureBrief());
  writeJson(path.join(shelf, "lexicon.json"), lexicon);
  if (external) {
    writeJson(path.join(root, "docs", "videos", "lexicon.json"), {
      schema_version: 1, terms: { App: "wrong root dictionary", iOS: "wrong root", p95: null },
    });
  }
  const text = chinese(targetLocale) ? "App Store 使用 iOS、API 與 p95。" : "App Store uses iOS API p95.";
  const translation = {
    title: "Title", description: "Description", tags: [], chapters: {}, source_hashes: {},
    lines: Object.fromEntries([...eachLine(doc)].map(({ line }) => [line.id, {
      text, source_hash: textHash(line.text),
    }])),
  };
  writeJson(path.join(dir, "i18n", `${targetLocale}.json`), translation);
  const project = loadProject({ file, root });
  assert.deepEqual(lintProject(project).errors, [], "the CLI fixture must pass ordinary lint");
  const timeline = estimateTimeline(doc);
  timeline.speech_hash = speechHash(doc, project.lexicon);
  writeJson(path.join(workdir, "timeline.json"), timeline);
  const translated = dubScript(doc, translation, targetLocale).doc;
  return {
    base, root, work, workdir, file, doc, lexicon, text, translated,
    selector: external ? ["--file", file] : ["--slug", doc.slug],
    planned: planRequests(translated, speechLexicon(lexicon, targetLocale)),
  };
}

function services() {
  const calls = { speech: [], transcribe: [], judge: [], ffmpeg: [] };
  const fetch = async (url, init) => {
    if (url.endsWith("/speech/status")) return Response.json({
      configured: false, voices: [], remaining: 0,
      gemini_configured: true, gemini_monthly_limit: 0, gemini_used: 0,
    });
    const body = JSON.parse(init.body);
    if (url.endsWith("/speech/transcribe")) {
      calls.transcribe.push(body);
      return Response.json({ text: "Different transcript to inspect the judge input." });
    }
    if (url.endsWith("/speech/judge")) {
      calls.judge.push(body);
      return Response.json({ results: body.lines.map((line) => ({ id: line.id, noul: 0.99 })) });
    }
    assert.ok(url.endsWith("/speech"), `unexpected network request ${url}`);
    calls.speech.push(body);
    const tone = Int16Array.from({ length: SAMPLE_RATE / 4 }, (_, index) => Math.round(8000 * Math.sin(index / 7)));
    const samples = concatSamples(body.segments.flatMap((segment) => [
      tone, new Int16Array(Math.round(segment.break_after_ms / 1000 * SAMPLE_RATE)),
    ]));
    return new Response(encodeWav(samples), {
      headers: { "Content-Type": "audio/wav", "X-Billable-Characters": "10" },
    });
  };
  const ffmpeg = {
    locate: async () => ({ ffmpeg: "fake", ffprobe: "fake", version: "fake" }),
    run: async (_tool, args) => {
      calls.ffmpeg.push(args);
      if (args.includes("null")) return {
        stdout: "", stderr: 'Parsed_loudnorm {"input_i":"-20","input_tp":"-3","input_lra":"5","input_thresh":"-30","target_offset":"0.5"}',
      };
      assert.ok(!args.some((arg) => String(arg).startsWith("atempo=")), "short clips fit without time stretching");
      copyFileSync(args[args.indexOf("-i") + 1], args.at(-1));
      return { stdout: "", stderr: "" };
    },
  };
  return { calls, fetch, ffmpeg };
}

function context(box, server, { dry = false } = {}) {
  const output = { stdout: "", stderr: "" };
  return {
    output,
    ctx: {
      root: box.root, home: box.base,
      env: { VIDEO_WORKDIR: box.work, ...(dry ? {} : { MOKAAIR_VIDEO_TOKEN: `mkv_${"t".repeat(43)}` }) },
      stdout: { write: (text) => { output.stdout += text; } },
      stderr: { write: (text) => { output.stderr += text; } },
      now: () => new Date("2026-09-30T04:00:00Z"), sleep: async () => {},
      fetch: dry ? async () => { throw new Error("dry-run must not request speech"); } : server.fetch,
      ffmpeg: server.ffmpeg,
    },
  };
}

for (const [source, target, external] of [["zh-TW", "en", false], ["en", "zh-TW", true], ["en", "ko", true]]) {
  test(`CLI ${source} → ${target}${external ? " via --file" : ""} plans, speaks and checks the target shelf aliases`, async (t) => {
    const box = projectFixture(t, source, target, external);
    const server = services();
    const command = ["dub", ...box.selector, "--locale", target];
    const files = dubArtifacts(box.workdir, target);
    if (target === "en") {
      const oldRequests = planRequests(box.translated, {
        ...box.lexicon, terms: { ...box.lexicon.terms, p95: null },
      });
      writeJson(files.cache, {
        lines: Object.fromEntries(oldRequests.flatMap((request) => request.lines.map((line) => [line.id, line.key]))),
        stretched: {},
      });
      mkdirSync(files.audio, { recursive: true });
      for (const request of oldRequests) for (const line of request.lines) {
        writeFileSync(path.join(files.audio, `${line.id}.wav`), encodeWav(new Int16Array(480)));
      }
    }
    const dry = context(box, server, { dry: true });
    assert.equal(await main([...command, "--dry-run"], dry.ctx), EXIT.ok, dry.output.stderr);
    const estimate = box.planned.reduce((sum, request) => sum + billableForRequest(request.body), 0);
    assert.ok(dry.output.stdout.includes(`${estimate} billable characters now (${estimate} for the track)`));
    assert.equal(server.calls.speech.length, 0);
    assert.equal(server.calls.ffmpeg.length, 0);
    const run = context(box, server);
    assert.equal(await main(command, run.ctx), EXIT.ok, run.output.stderr || run.output.stdout);
    assert.deepEqual(server.calls.speech, box.planned.map((request) => request.body));
    const expected = chinese(target)
      ? "A P P Store 使用 i O S、A P I 與 P 九十五。" : "App Store uses iOS A P I p95.";
    for (const body of server.calls.speech) {
      for (const segment of body.segments) assert.equal(geminiText([{ ...segment, break_after_ms: 0 }]), expected);
    }
    const cache = JSON.parse(readFileSync(files.cache, "utf8"));
    for (const request of box.planned) for (const line of request.lines) assert.equal(cache.lines[line.id], line.key);
    const synthesized = server.calls.speech.length;
    const again = context(box, server);
    assert.equal(await main(command, again.ctx), EXIT.ok, again.output.stderr);
    assert.equal(server.calls.speech.length, synthesized, "correct target pronunciation reuses its cache");
    const check = context(box, server);
    assert.equal(await main(["check-audio", ...box.selector, "--locale", target], check.ctx), EXIT.ok, check.output.stderr || check.output.stdout);
    const checked = JSON.parse(readFileSync(path.join(box.workdir, checkFiles(target, source).cache), "utf8"));
    assert.equal(Object.keys(checked.lines).length, [...eachLine(box.doc)].length);
    assert.ok(Object.values(checked.lines).every((line) => line.spoken_form === expected));
    assert.ok(server.calls.judge.length > 0);
    assert.ok(server.calls.judge.flatMap((body) => body.lines).every((line) => line.spoken_form === expected));
    assert.ok(server.calls.transcribe.every((body) => body.language === (target === "zh-TW" ? undefined : target)));
    assert.deepEqual(JSON.parse(readFileSync(path.join(path.dirname(path.dirname(box.file)), "lexicon.json"), "utf8")), box.lexicon);
  });
}

// Three slide windows, one line each, cut like production's: a 160-frame "who-first", a
// 100-frame "home-bits", a 60-frame "tail". Lines start where their window does, as the
// timeline builder lays them (a reveal lands on a line's start).
function threeWindows() {
  const scenes = [["who-first", 0, 160], ["home-bits", 160, 260], ["tail", 260, 320]];
  return {
    total_frames: 320,
    scenes: scenes.map(([id, start, end]) => ({ id, states: [{ reveal: 0, start_frame: start, end_frame: end }] })),
    lines: scenes.map(([id, start, end], index) => ({ id: `l${index}`, scene: id, start_frame: start, end_frame: end, audio_samples: (end - start) * SAMPLES_PER_FRAME })),
  };
}

/** Clip samples that make `window` stick out by `frames` once sped up to MAX_TEMPO. */
function overBy(window, frames) {
  return Math.round(MAX_TEMPO * (windowLimit(window) - window.start_frame + frames) * SAMPLES_PER_FRAME) - 100;
}

const framesOf = (ms) => framesFor(msToSamples(ms));

test("a window over by a few frames is let through: the pause after it first, its own tempo second, still over past both", async () => {
  assert.equal(OVERRUN_TOLERANCE_SECONDS, 0.3);
  assert.equal(MAX_TEMPO_OVERRUN, 1.25);
  const timeline = threeWindows();
  const [first, second, third] = layoutDub(timeline, new Map([["l0", 1600], ["l1", 1600], ["l2", 1600]]));
  const originals = new Map(timeline.lines.map((line) => [line.id, line]));
  const guard = framesOf(GUARD_MS);
  const gap = framesOf(GAP_MS);
  const lay = (samples) => layoutDubTolerant(timeline, new Map([["l0", samples[0]], ["l1", samples[1]], ["l2", samples[2]]]));
  const room = (window, fraction) => Math.round((window.end_frame - window.start_frame) * fraction * SAMPLES_PER_FRAME);

  // Over by 0.07 s (two frames, production's ko "who-first"): the overrun ends inside the guard,
  // and the next window is not touched.
  const strict = layoutDub(timeline, new Map([["l0", overBy(first, 2)], ["l1", room(second, 0.4)], ["l2", room(third, 0.4)]]));
  assert.deepEqual([strict[0].over, strict[0].tempo, strict[0].slack_frames], [true, MAX_TEMPO, -2], "without the tolerance the window is over at MAX_TEMPO");
  const inGuard = await lay([overBy(first, 2), room(second, 0.4), room(third, 0.4)]);
  assert.deepEqual([inGuard[0].over, inGuard[0].absorbed, inGuard[0].overrun_seconds, inGuard[0].tempo, inGuard[0].slack_frames], [false, "next-slack", 0.07, MAX_TEMPO, -2]);
  assert.ok(inGuard[0].lines.at(-1).end_frame <= first.end_frame, "the voice still ends before the slide changes");
  assert.equal(inGuard[1].shifted_frames, undefined);
  assert.equal(inGuard[1].lines[0].start_frame, second.start_frame);
  assert.equal(overrunSummary(inGuard), "1 window ran 0.07 s long: absorbed by the pause after it (who-first)");

  // Over by 0.2 s (six frames): past the slide change, so the next window's first line waits
  // for it, the gap between, and that window's slack takes the shift; the third does not move.
  const shifted = await lay([overBy(first, 6), room(second, 0.4), room(third, 0.4)]);
  assert.deepEqual([shifted[0].over, shifted[0].absorbed, shifted[0].overrun_seconds, shifted[0].tempo], [false, "next-slack", 0.2, MAX_TEMPO]);
  const spoke = shifted[0].lines.at(-1).end_frame;
  assert.equal(spoke, windowLimit(first) + 6);
  assert.equal(shifted[1].lines[0].start_frame, spoke + gap, "the next line starts a gap after the overrun");
  assert.equal(shifted[1].shifted_frames, 6 - guard + gap);
  assert.deepEqual([shifted[1].over, shifted[1].tempo, shifted[1].absorbed], [false, 1, undefined]);
  assert.deepEqual(shifted[2].lines, (await lay([1600, room(second, 0.4), room(third, 0.4)]))[2].lines, "the window after the next is as it was");
  assert.ok(shifted[1].lines[0].end_frame <= windowLimit(second));

  // Over by 0.27 s (eight frames, production's sec-ai ko) with a next window too full to wait:
  // this window alone is sped up past MAX_TEMPO, to 1.21x here, and nothing else changes.
  const sped = await lay([overBy(first, 8), room(second, 0.95), room(third, 0.4)]);
  assert.deepEqual([sped[0].over, sped[0].absorbed, sped[0].overrun_seconds, sped[0].tempo], [false, "tempo", 0.27, 1.21]);
  assert.ok(sped[0].tempo > MAX_TEMPO && sped[0].tempo <= MAX_TEMPO_OVERRUN);
  assert.ok(sped[0].lines.at(-1).end_frame <= windowLimit(first), "at its own tempo the window fits its limit again");
  assert.equal(sped[0].lines[0].audio_samples, Math.round(overBy(first, 8) / 1.21));
  assert.equal(sped[1].lines[0].start_frame, second.start_frame);
  assert.equal(sped[1].shifted_frames, undefined);
  assert.equal(overrunSummary(sped), "1 window ran 0.27 s long: sped up to 1.21x (who-first)");

  // The pause is preferred even when the tempo would do: the same eight frames with room after.
  const paused = await lay([overBy(first, 8), room(second, 0.4), room(third, 0.4)]);
  assert.deepEqual([paused[0].absorbed, paused[0].tempo, paused[1].shifted_frames], ["next-slack", MAX_TEMPO, 8 - guard + gap]);

  // Over by 0.6 s: beyond the tolerance, so the window stays over for the translator.
  const still = await lay([overBy(first, 18), room(second, 0.4), room(third, 0.4)]);
  assert.deepEqual([still[0].over, still[0].absorbed, still[0].tempo, still[0].slack_frames], [true, undefined, MAX_TEMPO, -18]);
  assert.equal(still[1].lines[0].start_frame, second.start_frame);
  assert.equal(overrunSummary(still), null);

  // Within the tolerance but neither way works: a short last window (no window after it, only the
  // guard) over by eight frames needs more than MAX_TEMPO_OVERRUN.
  const last = await lay([1600, 1600, overBy(third, 8)]);
  assert.deepEqual([last[2].over, last[2].absorbed, last[2].tempo], [true, undefined, MAX_TEMPO]);
  assert.ok(MAX_TEMPO * (windowLimit(third) - third.start_frame + 8) / (windowLimit(third) - third.start_frame) > MAX_TEMPO_OVERRUN);

  // Two windows let through read as one line, in window order.
  const both = await lay([overBy(first, 2), room(second, 0.95), overBy(third, 1)]);
  assert.equal(overrunSummary(both), "2 windows ran long: who-first 0.07 s absorbed by the pause after it; tail 0.03 s absorbed by the pause after it");

  // shiftWindow keeps a window's rhythm: with kept starts only the lines the overrun reaches move.
  const two = { ...first, lines: [{ id: "a", scene: "who-first", start_frame: 0, end_frame: 20, audio_samples: 20 * SAMPLES_PER_FRAME, tempo: 1 }, { id: "b", scene: "who-first", start_frame: 80, end_frame: 100, audio_samples: 20 * SAMPLES_PER_FRAME, tempo: 1 }], tempo: 1, kept_starts: true, over: false, slack_frames: 57 };
  const twoOriginals = new Map([["a", { start_frame: 0 }], ["b", { start_frame: 80 }]]);
  const moved = shiftWindow(two, twoOriginals, 10);
  assert.deepEqual(moved.lines.map((line) => [line.start_frame, line.end_frame, line.tempo]), [[10, 30], [80, 100]].map(([start, end]) => [start, end, 1]));
  assert.deepEqual([moved.shifted_frames, moved.over, moved.slack_frames], [10, false, windowLimit(first) - 100]);
  assert.equal(await absorbOverruns([{ ...first, lines: [], over: false }], originals).then((out) => out[0].absorbed), undefined, "a window that fits is left alone");
  assert.equal(FPS, 30);
});
