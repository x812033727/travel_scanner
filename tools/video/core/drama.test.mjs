import assert from "node:assert/strict";
import { mkdirSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { approve } from "./approvals.mjs";
import {
  charactersBySpeaker,
  clipKey,
  clipsHash,
  keyframeKey,
  lookHash,
  mixHash,
  promptSimilarity,
  resolveLook,
  resolveSubtitles,
  shotProblems,
  subtitlesHash,
  voiceFor,
} from "./drama.mjs";
import { dramaBrief, dramaFixture, fixture, fixtureLexicon, sandbox } from "./fixtures/load.mjs";
import { lintVideo } from "./lint.mjs";
import { atomicWrite } from "./paths.mjs";
import { validateVideo } from "./schema.mjs";
import { DRAMA_STEPS, loadProject, lookChosen, pipelineStatus, SLIDES_STEPS, stepsFor } from "./state.mjs";
import { estimateTimeline, speechHash, visualHash } from "./timeline.mjs";

const paths = (errors) => errors.map((error) => error.path).sort();
const context = (overrides = {}) => ({ lexicon: fixtureLexicon(), brief: dramaBrief(), others: [], translations: {}, ...overrides });

test("the drama example is valid and lints clean", () => {
  assert.deepEqual(validateVideo(dramaFixture()), []);
  const result = lintVideo(dramaFixture(), context());
  assert.deepEqual(result.errors, []);
  assert.deepEqual(result.warnings, []);
  assert.equal(result.summary.chapters.length, 3);
});

test("a slides video cannot carry drama fields, and a drama cannot use slide templates", () => {
  const slides = fixture();
  slides.characters = [];
  slides.look = { preset: "cinematic-3d" };
  slides.scenes[1].template = "shot";
  slides.scenes[0].lines[0].speaker = "narrator";
  slides.scenes[0].lines[1].emotion = "calm";
  assert.deepEqual(paths(validateVideo(slides)), ["characters", "look", "scenes[0].lines[0] (k7p2).speaker", "scenes[0].lines[1] (m4qa).emotion", "scenes[1].template"]);
  const drama = dramaFixture();
  drama.scenes[0].template = "bullets";
  assert.deepEqual(paths(validateVideo(drama)), ["scenes[0].template"]);
});

test("shots, speakers, references and music are range-checked", () => {
  const doc = dramaFixture();
  doc.scenes[0].lines[0].reveal = 1;
  doc.scenes[1].lines[0].speaker = "nobody";
  doc.scenes[1].lines[1].emotion = "x".repeat(81);
  doc.scenes[0].data.characters = ["jingwei", "ghost"];
  doc.scenes[0].data.fit = "stretch";
  doc.scenes[0].data.start_frame = { shot: "bird", at: "last" };
  doc.scenes[2].data.seed = -1;
  doc.thumbnail.data.shot = "wrap";
  doc.music = { gain_db: 3 };
  doc.subtitles.style = "karaoke";
  doc.characters[1].id = "narrator";
  doc.characters[0].voice = { provider: "azure", name: "zh-TW-HsiaoChenNeural", style: "soft" };
  assert.deepEqual(paths(validateVideo(doc)), [
    "characters[0].voice",
    "characters[1].id",
    "music",
    "music.gain_db",
    "scenes[0].data.characters",
    "scenes[0].data.fit",
    "scenes[0].data.start_frame",
    "scenes[0].lines[0] (k7p2).reveal",
    "scenes[1].data.characters",
    "scenes[1].lines[0] (x9fe).speaker",
    "scenes[1].lines[1] (b3tn).emotion",
    "scenes[1].lines[1] (b3tn).speaker",
    "scenes[2].data.seed",
    "subtitles.style",
    "thumbnail.data.shot",
  ]);
});

test("a drama needs a shot, and a custom look needs a style", () => {
  const doc = dramaFixture();
  doc.scenes = doc.scenes.filter((scene) => scene.template !== "shot");
  doc.look = { candidates: 9 };
  delete doc.thumbnail.data.shot;
  assert.deepEqual(paths(validateVideo(doc)), ["look.candidates", "look.style", "scenes"]);
});

test("a preset fills the look in, and a look's own fields win", () => {
  const preset = resolveLook({ preset: "anime-2d" });
  assert.match(preset.style, /anime/);
  assert.equal(preset.candidates, 3);
  const own = resolveLook(dramaFixture().look);
  assert.match(own.style, /jade/);
  assert.match(own.negative, /extra fingers/);
  assert.deepEqual(resolveSubtitles(dramaFixture()), { burn_in: true, style: "drama", speaker_prefix: false });
  assert.equal(resolveSubtitles(fixture()).burn_in, false);
});

test("each line gets its speaker's voice, and a Gemini voice takes the emotion in its style", () => {
  const doc = dramaFixture();
  assert.equal(voiceFor(doc, doc.scenes[0].lines[0]).name, "Sulafat");
  const jingwei = voiceFor(doc, doc.scenes[1].lines[0]);
  assert.equal(jingwei.name, "Kore");
  assert.equal(jingwei.style, "清亮、倔強的少女聲，台灣國語。開心、有點急");
  assert.deepEqual(charactersBySpeaker(doc), { narrator: [...doc.scenes[0].lines[0].text, ...doc.scenes[0].lines[1].text, ...doc.scenes[2].lines[0].text, ...doc.scenes[2].lines[1].text, ...doc.scenes[3].lines[0].text, ...doc.scenes[4].lines[0].text, ...doc.scenes[4].lines[1].text].length, jingwei: [...doc.scenes[1].lines[0].text, ...doc.scenes[3].lines[1].text].length, yandi: [...doc.scenes[1].lines[1].text].length });
});

test("the speech hash follows speakers, emotions and character voices; the slides hash does not change shape", () => {
  const doc = dramaFixture();
  const lexicon = fixtureLexicon();
  const base = speechHash(doc, lexicon);
  const speaker = dramaFixture();
  speaker.scenes[1].lines[0].speaker = "yandi";
  assert.notEqual(speechHash(speaker, lexicon), base);
  const emotion = dramaFixture();
  emotion.scenes[1].lines[0].emotion = "冷淡";
  assert.notEqual(speechHash(emotion, lexicon), base);
  const voice = dramaFixture();
  voice.characters[0].voice.name = "Puck";
  assert.notEqual(speechHash(voice, lexicon), base);
  const prompt = dramaFixture();
  prompt.scenes[0].data.prompt = "something else entirely";
  assert.equal(speechHash(prompt, lexicon), base);
  assert.notEqual(visualHash(prompt), visualHash(doc));
});

test("the look hash follows the look and the cast's appearance only", () => {
  const doc = dramaFixture();
  const base = lookHash(doc);
  const prompt = dramaFixture();
  prompt.scenes[0].data.prompt = "another prompt";
  prompt.scenes[0].lines[0].text = "另一句";
  assert.equal(lookHash(prompt), base);
  const appearance = dramaFixture();
  appearance.characters[0].appearance += ", with a scar";
  assert.notEqual(lookHash(appearance), base);
  const style = dramaFixture();
  style.look.style = "watercolour";
  assert.notEqual(lookHash(style), base);
  const music = dramaFixture();
  music.music.gain_db = -12;
  assert.equal(lookHash(music), base);
  assert.notEqual(mixHash(music), mixHash(doc));
  assert.equal(subtitlesHash(music), subtitlesHash(doc));
});

test("media cache keys are stable, order-insensitive for references and sensitive to the right fields", () => {
  const request = { provider: "gemini", model: "m", prompt: "p", width: 1920, height: 1080, seed: 7, references: ["b", "a"] };
  assert.equal(keyframeKey(request), keyframeKey({ ...request, references: ["a", "b"] }));
  assert.notEqual(keyframeKey(request), keyframeKey({ ...request, seed: 8 }));
  assert.notEqual(keyframeKey(request), keyframeKey({ ...request, negative: "text" }));
  const clip = { provider: "gemini", model: "v", prompt: "p", seconds: 8, resolution: "1080p", startFrame: "abc" };
  assert.equal(clipKey(clip), clipKey({ ...clip }));
  assert.notEqual(clipKey(clip), clipKey({ ...clip, endFrame: "def" }));
  assert.notEqual(clipKey(clip), clipKey({ ...clip, seconds: 6 }));
  assert.notEqual(clipsHash([{ id: "a", sha256: "1" }]), clipsHash([{ id: "a", sha256: "2" }]));
  assert.match(keyframeKey(request), /^[0-9a-f]{16}$/);
});

test("overlong shots are errors, long or look-alike shots are warnings", () => {
  const doc = dramaFixture();
  doc.scenes[0].lines[0].text = "很".repeat(60);
  doc.scenes[1].data.prompt = doc.scenes[0].data.prompt;
  const problems = shotProblems(doc, estimateTimeline(doc));
  assert.equal(problems.errors.length, 1);
  assert.match(problems.errors[0].message, /at most 12 s/);
  assert.ok(problems.warnings.some((warning) => /nearly the same as opening/.test(warning.message)));
  assert.equal(promptSimilarity(doc.scenes[0], doc.scenes[1]), 1);
  const linted = lintVideo(doc, context());
  assert.ok(linted.errors.some((error) => /at most 12 s/.test(error.message)));
});

test("lint wants the drama brief sections and warns about an emotion an Azure voice cannot take", () => {
  const doc = dramaFixture();
  doc.characters[1].voice = { provider: "azure", name: "zh-TW-YunJheNeural", rate: "+0%" };
  const result = lintVideo(doc, context({ brief: "# x\n\n## 站主觀點\n\n有\n" }));
  assert.deepEqual(result.errors.map((error) => error.message), ['brief.md needs a non-empty "## 故事前提" section', 'brief.md needs a non-empty "## 角色" section']);
  assert.ok(result.warnings.some((warning) => /emotion "溫和但擔心" is ignored/.test(warning.message)));
  const slides = fixture();
  slides.music = { track: "a.mp3" };
  assert.ok(lintVideo(slides, context({ brief: undefined, lexicon: fixtureLexicon() })).warnings.some((warning) => warning.path === "music"));
});

test("a drama's status walks the media steps in order, each bound to its hashes", async () => {
  const box = sandbox("fixture-drama", "drama");
  const status = () => pipelineStatus({ slug: box.slug, root: box.root, workdir: box.workdir });
  assert.deepEqual(stepsFor(dramaFixture()), DRAMA_STEPS);
  assert.equal(stepsFor(fixture()), SLIDES_STEPS);
  assert.deepEqual((await status()).steps.map((step) => step.id), DRAMA_STEPS);
  const places = { docDir: box.dir, workdir: box.workdir };
  mkdirSync(box.workdir, { recursive: true });
  await approve({ gate: "outline", ...places });
  writeFileSync(path.join(box.dir, "verify-1.md"), "# ok\n");
  assert.equal((await status()).next.id, "look generated");

  const project = loadProject({ slug: box.slug, root: box.root });
  const look = lookHash(project.doc);
  const write = (name, content) => atomicWrite(path.join(box.workdir, name), JSON.stringify(content));
  write("characters/manifest.json", { look_hash: "stale", characters: { jingwei: { suggested: 1 }, yandi: { suggested: 2 } } });
  assert.equal((await status()).next.id, "look generated");
  write("characters/manifest.json", { look_hash: look, characters: { jingwei: { suggested: 1 }, yandi: {} } });
  assert.equal((await status()).next.id, "look approved");
  await approve({ gate: "look", ...places });
  assert.equal((await status()).next.note, "a character has no chosen sheet");
  write("characters/choice.json", { look_hash: look, chosen: { yandi: 3 } });
  assert.deepEqual(lookChosen({ look_hash: look, characters: { jingwei: { suggested: 1 }, yandi: {} } }, { look_hash: look, chosen: { yandi: 3 } }, look), { jingwei: 1, yandi: 3 });
  assert.equal((await status()).next.id, "narration synthesized");

  const speech = speechHash(project.doc, project.lexicon);
  const visual = visualHash(project.doc);
  write("timeline.json", { ...estimateTimeline(project.doc), speech_hash: speech });
  await approve({ gate: "audio", ...places });
  assert.equal((await status()).next.id, "keyframes drawn");
  write("keyframes/manifest.json", { look_hash: look, visual_hash: visual, shots: { opening: { needs_review: true } } });
  assert.match((await status()).next.note, /needs_review/);
  write("keyframes/manifest.json", { look_hash: look, visual_hash: visual, shots: { opening: {} } });
  assert.equal((await status()).next.id, "storyboard approved");
  await approve({ gate: "storyboard", ...places });
  assert.equal((await status()).next.id, "frames rendered");
  write("frames/manifest.json", { visual_hash: visual });
  assert.equal((await status()).next.id, "frames rendered", "burned-in subtitles bind the frames to the speech");
  write("frames/manifest.json", { visual_hash: visual, speech_hash: speech, subtitles_hash: subtitlesHash(project.doc) });
  assert.equal((await status()).next.id, "clips generated");
  write("clips/manifest.json", { speech_hash: speech, visual_hash: visual, look_hash: look, clips_hash: "c1", shots: {} });
  assert.equal((await status()).next.id, "music generated");
  write("music/manifest.json", { mix_hash: mixHash(project.doc) });
  assert.equal((await status()).next.id, "video assembled");
  writeFileSync(path.join(box.workdir, "final.mp4"), "");
  write("checks.json", { ok: true, speech_hash: speech, visual_hash: visual, look_hash: look, clips_hash: "c0", subtitles_hash: subtitlesHash(project.doc), mix_hash: mixHash(project.doc) });
  assert.equal((await status()).next.id, "video assembled", "the checks must name the clips that were joined");
  write("checks.json", { ok: true, speech_hash: speech, visual_hash: visual, look_hash: look, clips_hash: "c1", subtitles_hash: subtitlesHash(project.doc), mix_hash: mixHash(project.doc) });
  assert.equal((await status()).next.id, "captions written");
});
