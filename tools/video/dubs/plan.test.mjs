import assert from "node:assert/strict";
import { copyFileSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import test from "node:test";

import { EXIT, main } from "../cli.mjs";
import { enBrief, enFixture, fixture, fixtureBrief, fixtureLexicon } from "../core/fixtures/load.mjs";
import { eachLine, LOCALES, textHash } from "../core/schema.mjs";
import { dubArtifacts, lintProject, loadProject } from "../core/state.mjs";
import { estimateTimeline, SAMPLE_RATE, speechHash } from "../core/timeline.mjs";
import { checkFiles, dubLexicon as checkerDubLexicon, lexiconFor, spokenForm } from "../tts/check.mjs";
import { billableForRequest, geminiText, planRequests } from "../tts/requests.mjs";
import { concatSamples, encodeWav } from "../tts/wav.mjs";
import { dubLexicon, dubScript, speechLexicon } from "./plan.mjs";

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
const chinese = (locale) => ["zh-TW", "zh-CN"].includes(locale);

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
  assert.deepEqual(planRequests(doc, speechLexicon(RAW, "zh-CN")), [old]);
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

for (const [source, target, external] of [["zh-TW", "en", false], ["en", "zh-TW", true], ["en", "zh-CN", true]]) {
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
