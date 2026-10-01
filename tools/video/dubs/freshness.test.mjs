// A finished dub is current only while `dub` would ask the voice for the same speech: a changed
// target alias or dub voice makes it stale and keeps it out of the upload, records from before
// the fingerprint are stale too, and running `dub` again pays only for the lines that changed.
// Synthetic clips and mocked speech and ffmpeg only: nothing here reaches a real service.
import assert from "node:assert/strict";
import { copyFileSync, mkdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { EXIT, main } from "../cli.mjs";
import { enBrief, enFixture, fixture, fixtureLexicon, sandbox } from "../core/fixtures/load.mjs";
import { eachLine, textHash } from "../core/schema.mjs";
import { currentDub, dubsForUpload } from "../core/stages.mjs";
import { dubArtifacts, dubsStatus, lintProject, loadProject } from "../core/state.mjs";
import { estimateTimeline, SAMPLE_RATE, speechHash } from "../core/timeline.mjs";
import { geminiText } from "../tts/requests.mjs";
import { concatSamples, encodeWav, parseWav } from "../tts/wav.mjs";
import { dubFingerprint, dubRequests, speechCurrent, speechFingerprint } from "./plan.mjs";

const TOKEN = `mkv_${"t".repeat(43)}`;
const VOICE = { provider: "gemini", name: "Sulafat", style: "Conversational." };
// Spelled with escapes so the file stays ASCII: "P nine-ten-five" and "P nine-five" in Chinese.
const P95_OLD = "P 九十五";
const P95_NEW = "P 九五";
const ms = (value) => Math.round((value / 1000) * SAMPLE_RATE);
const tone = (milliseconds) => Int16Array.from({ length: ms(milliseconds) }, (_, index) => Math.round(8000 * Math.sin(index / 7)));

const readJson = (file) => JSON.parse(readFileSync(file, "utf8"));
function writeJson(file, value) {
  mkdirSync(path.dirname(file), { recursive: true });
  writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`);
}

function translationFor(doc, textFor) {
  const lines = {};
  for (const { line } of eachLine(doc)) lines[line.id] = { source_hash: textHash(line.text), text: textFor(line) };
  return { title: "T", description: "D", tags: [], chapters: {}, source_hashes: {}, lines };
}

/** The narration server: a Gemini month with no limit, and 60 ms of tone per written character. */
function fakeServer() {
  const bodies = [];
  const fetch = async (url, init) => {
    if (url.endsWith("/speech/status")) return Response.json({ configured: false, voices: [], remaining: 0, gemini_configured: true, gemini_monthly_limit: 0, gemini_used: 0 });
    assert.ok(url.endsWith("/speech"), `unexpected network request ${url}`);
    const body = JSON.parse(init.body);
    bodies.push(body);
    const audio = concatSamples(body.segments.flatMap((segment) => [tone(segment.parts.reduce((sum, part) => sum + part.text.length, 0) * 60), new Int16Array(ms(segment.break_after_ms))]));
    return new Response(encodeWav(audio), { headers: { "Content-Type": "audio/wav", "X-Billable-Characters": "10" } });
  };
  return { bodies, fetch };
}

/** ffmpeg as the dub sees it: a loudness measurement, a shortened copy for atempo, a plain copy otherwise. */
const fakeFfmpeg = {
  locate: async () => ({ ffmpeg: "ffmpeg", ffprobe: "ffprobe", version: "fake" }),
  run: async (_tool, args) => {
    if (args.includes("null")) return { stdout: "", stderr: 'Parsed_loudnorm {"input_i":"-20","input_tp":"-3","input_lra":"5","input_thresh":"-30","target_offset":"0.5"}' };
    const input = args[args.indexOf("-i") + 1];
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

function context(box, server) {
  const out = { stdout: "", stderr: "" };
  const ctx = {
    root: box.root, home: box.base,
    env: { VIDEO_WORKDIR: box.work, MOKAAIR_VIDEO_TOKEN: TOKEN },
    stdout: { write: (text) => { out.stdout += text; } },
    stderr: { write: (text) => { out.stderr += text; } },
    now: () => new Date("2026-10-01T04:00:00Z"), sleep: async () => {},
    fetch: server.fetch, ffmpeg: fakeFfmpeg,
  };
  return { ctx, out };
}

async function dub(box, server, args) {
  const run = context(box, server);
  const code = await main(["dub", ...box.selector, ...args], run.ctx);
  return { code, ...run.out };
}

/**
 * A video on a shelf (docs/videos/, or an external one opened with --file) whose narration
 * never says the dictionary terms the translations use, so changing their aliases leaves the
 * narration's speech hash alone, as in the App correction. The timeline is estimated, not spoken.
 */
function videoBox({ source = "zh-TW", external = false, terms, translations }) {
  const box = sandbox();
  const doc = { ...(source === "en" ? enFixture() : fixture()), voice: VOICE };
  const shelf = external ? path.join(box.base, "external-shelf") : box.videos;
  const dir = path.join(shelf, doc.slug);
  const file = path.join(dir, "video.json");
  writeJson(file, doc);
  if (source === "en") writeFileSync(path.join(dir, "brief.md"), enBrief());
  else if (external) copyFileSync(path.join(box.dir, "brief.md"), path.join(dir, "brief.md"));
  const lexiconFile = path.join(shelf, "lexicon.json");
  const lexicon = { schema_version: 1, terms: { ...fixtureLexicon().terms, ...terms } };
  writeJson(lexiconFile, lexicon);
  for (const [locale, textFor] of Object.entries(translations)) writeJson(path.join(dir, "i18n", `${locale}.json`), translationFor(doc, textFor));
  const workdir = path.join(box.work, doc.slug);
  const load = () => loadProject(external ? { file, root: box.root } : { slug: doc.slug, root: box.root });
  const project = load();
  assert.deepEqual(lintProject(project).errors, []);
  const speech = speechHash(doc, project.lexicon);
  writeJson(path.join(workdir, "timeline.json"), { ...estimateTimeline(doc), speech_hash: speech });
  const setAlias = (term, say) => {
    const next = readJson(lexiconFile);
    next.terms[term] = say;
    writeJson(lexiconFile, next);
  };
  const look = (locales) => {
    const now = load();
    assert.equal(speechHash(now.doc, now.lexicon), speech, "the narration itself never changes here");
    return { status: dubsStatus(now, workdir, speech), upload: dubsForUpload(now, workdir, speech, locales).dubs.map((each) => each.locale), project: now };
  };
  return { ...box, doc, file, dir, workdir, speech, selector: external ? ["--file", file] : ["--slug", doc.slug], setAlias, look };
}

test("a changed target alias makes only the dubs that say it stale and keeps them out of the upload until a rerun retakes their lines", async () => {
  const box = videoBox({
    terms: { OpenAI: "Open A I", App: "A P P", Store: null },
    translations: {
      en: (line) => (line.id === "k7p2" ? "OpenAI ships an App Store." : `EN ${line.id}`),
      ko: (line) => `KO ${line.id}`,
      // ja's opening window cannot fit even at the top speed-up: the run is over budget.
      ja: (line) => (line.id === "k7p2" ? `OpenAI ${"j".repeat(400)}` : `JA ${line.id}`),
    },
  });
  const server = fakeServer();
  const locales = ["en", "ja", "ko"];
  const first = await dub(box, server, ["--locale", "en,ja,ko"]);
  assert.equal(first.code, EXIT.lint, "ja is over budget");
  const record = readJson(dubArtifacts(box.workdir, "en").timeline);
  assert.match(record.speech_fingerprint, /^[0-9a-f]{16}$/);
  assert.equal(record.style_override, null);
  assert.equal(readJson(dubArtifacts(box.workdir, "ja").fit).speech_fingerprint, dubFingerprint(box.look(locales).project, "ja"), "an over-budget run records what it asked for too");
  let seen = box.look(locales);
  assert.deepEqual([seen.status.en.status, seen.status.ja.status, seen.status.ko.status], ["current", "over", "current"]);
  assert.deepEqual(seen.upload, ["en", "ko"]);

  // An entry no line uses, and an alias English discards like the old one, change nothing.
  box.setAlias("Unused", "un used");
  box.setAlias("App", "a p p");
  seen = box.look(locales);
  assert.deepEqual([seen.status.en.status, seen.status.ja.status, seen.status.ko.status], ["current", "over", "current"]);
  assert.deepEqual(seen.upload, ["en", "ko"]);

  // The alias en and ja actually send changes: both go stale, ko (which never says it) does not.
  box.setAlias("OpenAI", "Open AI");
  seen = box.look(locales);
  assert.equal(seen.status.en.status, "stale");
  assert.match(seen.status.en.note, /older voice or pronunciation; run dub again \(unchanged clips are reused\)/);
  assert.equal(seen.status.ja.status, "stale", "the over-budget run measured the old pronunciation");
  assert.match(seen.status.ja.note, /^the last run was over budget with an older voice or pronunciation/);
  assert.equal(seen.status.ko.status, "current");
  assert.deepEqual(seen.upload, ["ko"], "a stale dub is not packaged");
  assert.equal(currentDub(seen.project, box.workdir, "en", box.speech).stale, true);
  const statusRun = context(box, server);
  assert.equal(await main(["status", "--slug", box.doc.slug], statusRun.ctx), EXIT.ok);
  assert.match(statusRun.out.stdout, /en stale/);

  // A rerun retakes the one line whose request changed and reuses every other clip.
  const before = server.bodies.length;
  const again = await dub(box, server, ["--locale", "en"]);
  assert.equal(again.code, EXIT.ok, again.stderr || again.stdout);
  const sent = server.bodies.slice(before);
  assert.equal(sent.length, 1);
  assert.deepEqual(sent[0].segments.map((segment) => geminiText([{ ...segment, break_after_ms: 0 }])), ["Open AI ships an App Store."]);
  seen = box.look(locales);
  assert.equal(seen.status.en.status, "current");
  assert.deepEqual(seen.upload, ["en", "ko"]);
});

const LEGACY_TRACK = { status: "stale", note: "made before dubs recorded their pronunciation; run dub again (unchanged clips are reused)" };
const LEGACY_OVER = { status: "stale", note: "the last run was over budget before dubs recorded their pronunciation; run dub again (unchanged clips are reused)" };

/** What `dub` wrote before 2026-10-01: the same record without the fingerprint fields. */
function stripFingerprint(file) {
  const { speech_fingerprint, style_override, ...legacy } = readJson(file);
  assert.ok(speech_fingerprint);
  assert.equal(style_override, null);
  writeJson(file, legacy);
}

test("records from before the fingerprint answer by their clip cache: current while every key matches, stale once one differs or the cache is gone", async () => {
  const box = videoBox({
    terms: { OpenAI: "Open A I" },
    translations: {
      en: (line) => (line.id === "k7p2" ? "OpenAI ships it." : `EN ${line.id}`),
      ja: (line) => (line.id === "k7p2" ? `OpenAI ${"j".repeat(400)}` : `JA ${line.id}`),
    },
  });
  const server = fakeServer();
  assert.equal((await dub(box, server, ["--locale", "en"])).code, EXIT.ok);
  assert.equal((await dub(box, server, ["--locale", "ja"])).code, EXIT.lint);
  const en = dubArtifacts(box.workdir, "en");
  const ja = dubArtifacts(box.workdir, "ja");
  // A legacy successful run left both files without one.
  stripFingerprint(en.timeline);
  stripFingerprint(en.fit);
  stripFingerprint(ja.fit);

  // Unchanged speech: the cache holds every key the plan asks for, so nothing flips on deploy.
  let seen = box.look(["en", "ja"]);
  assert.equal(seen.status.en.status, "current");
  assert.equal(seen.status.ja.status, "over");
  assert.deepEqual(seen.upload, ["en"]);

  // A changed target alias: the cached key of the line that says it differs.
  box.setAlias("OpenAI", "Open AI");
  seen = box.look(["en", "ja"]);
  assert.deepEqual(seen.status.en, LEGACY_TRACK);
  assert.deepEqual(seen.status.ja, LEGACY_OVER);
  assert.deepEqual(seen.upload, [], "an unproven track is not packaged");

  // The rerun retakes that one line, reuses the rest and records a fingerprint.
  const before = server.bodies.length;
  const again = await dub(box, server, ["--locale", "en"]);
  assert.equal(again.code, EXIT.ok, again.stderr || again.stdout);
  assert.deepEqual(server.bodies.slice(before).map((body) => body.segments.map((segment) => geminiText([{ ...segment, break_after_ms: 0 }]))), [["Open AI ships it."]]);
  seen = box.look(["en"]);
  assert.equal(seen.status.en.status, "current");
  assert.deepEqual(seen.upload, ["en"]);

  // A legacy track whose evidence is gone or cannot be read is stale.
  stripFingerprint(en.timeline);
  stripFingerprint(en.fit);
  assert.equal(box.look(["en"]).status.en.status, "current");
  const cache = readFileSync(en.cache, "utf8");
  writeFileSync(en.cache, "{ not json");
  assert.deepEqual(box.look(["en"]).status.en, LEGACY_TRACK);
  rmSync(en.cache);
  seen = box.look(["en"]);
  assert.deepEqual(seen.status.en, LEGACY_TRACK);
  assert.deepEqual(seen.upload, []);
  assert.equal(currentDub(seen.project, box.workdir, "en", box.speech).stale, true);

  // A newer run's fingerprinted fit.json beside a legacy track: that run may have cached clips
  // the track does not hold, so the cache proves nothing.
  writeFileSync(en.cache, cache);
  writeJson(en.fit, { ...readJson(en.fit), speech_fingerprint: "0000000000000000" });
  assert.deepEqual(box.look(["en"]).status.en, LEGACY_TRACK);
});

test("a Chinese dub of an English video opened with --file is bound to the shelf's Chinese aliases", async () => {
  const box = videoBox({
    source: "en",
    external: true,
    terms: { p95: P95_OLD, App: "A P P", Store: null },
    translations: { "zh-TW": () => "App Store 使用 p95。" },
  });
  const server = fakeServer();
  const made = await dub(box, server, ["--locale", "zh-TW"]);
  assert.equal(made.code, EXIT.ok, made.stderr || made.stdout);
  assert.ok(server.bodies.every((body) => body.segments.every((segment) => geminiText([{ ...segment, break_after_ms: 0 }]) === `A P P Store 使用 ${P95_OLD}。`)), "the dub spoke the Chinese aliases the English narration drops");
  let seen = box.look(["zh-TW"]);
  assert.equal(seen.status["zh-TW"].status, "current", "status plans from the same raw shelf dictionary as dub");
  assert.deepEqual(seen.upload, ["zh-TW"]);

  // Only the Chinese reading changes; the English narration ignores it.
  box.setAlias("p95", P95_NEW);
  seen = box.look(["zh-TW"]);
  assert.equal(seen.status["zh-TW"].status, "stale");
  assert.deepEqual(seen.upload, []);
  const before = server.bodies.length;
  const again = await dub(box, server, ["--locale", "zh-TW"]);
  assert.equal(again.code, EXIT.ok, again.stderr || again.stdout);
  assert.ok(server.bodies.length > before);
  assert.ok(server.bodies.slice(before).every((body) => body.segments.every((segment) => geminiText([{ ...segment, break_after_ms: 0 }]).includes(P95_NEW))));
  seen = box.look(["zh-TW"]);
  assert.equal(seen.status["zh-TW"].status, "current");
  assert.deepEqual(seen.upload, ["zh-TW"]);
});

test("the fingerprint binds the dub voice and each line's request, and nothing else", () => {
  const box = videoBox({
    terms: { OpenAI: "Open A I" },
    translations: { en: (line) => `EN ${line.id} OpenAI`, ko: (line) => `KO ${line.id}` },
  });
  const project = box.look(["en"]).project;
  const en = dubFingerprint(project, "en");
  assert.equal(en, speechFingerprint(dubRequests(project, "en").requests));
  assert.notEqual(dubFingerprint(project, "en", "Whispered."), en, "the style the voice is asked in");
  assert.notEqual(dubFingerprint({ ...project, doc: { ...project.doc, voice: { ...VOICE, model: "another-model" } } }, "en"), en, "the voice model");
  assert.notEqual(dubFingerprint({ ...project, doc: { ...project.doc, voice: { ...VOICE, name: "Kore" } } }, "en"), en, "the voice");
  const koEdited = { ...project, translations: { ...project.translations, ko: translationFor(project.doc, (line) => `KO ${line.id} changed`) } };
  assert.equal(dubFingerprint(koEdited, "en"), en, "another locale's words");
  assert.equal(dubFingerprint(project, "ja"), null, "no fingerprint without a translation");
  assert.equal(dubFingerprint(null, "en"), null);
  // A --style dub is compared in the style it was made in.
  assert.equal(speechCurrent(project, "en", { speech_fingerprint: dubFingerprint(project, "en", "Whispered."), style_override: "Whispered." }), true);
  assert.equal(speechCurrent(project, "en", { speech_fingerprint: dubFingerprint(project, "en", "Whispered."), style_override: null }), false);
  assert.equal(speechCurrent(project, "en", { speech_fingerprint: en }), true);
  // A record without one answers by the clip cache, and only by a cache that matches every line.
  const keys = Object.fromEntries(dubRequests(project, "en").requests.flatMap((request) => request.lines.map((line) => [line.id, line.key])));
  assert.equal(speechCurrent(project, "en", {}), false, "no cache, no evidence");
  assert.equal(speechCurrent(project, "en", {}, { cache: { lines: keys } }), true);
  assert.equal(speechCurrent(project, "en", {}, { cache: { lines: keys }, legacyGuard: false }), false);
  assert.equal(speechCurrent(project, "en", {}, { cache: { lines: { ...keys, k7p2: "0000000000000000" } } }), false);
  const { k7p2, ...partial } = keys;
  assert.ok(k7p2);
  assert.equal(speechCurrent(project, "en", {}, { cache: { lines: partial } }), false);
  assert.equal(speechCurrent(project, "en", { style_override: "Whispered." }, { cache: { lines: keys } }), false, "the cache is read against the style the dub was made in");
  assert.equal(speechCurrent(project, "ja", {}, { cache: { lines: keys } }), false, "no plan without a translation");
});
