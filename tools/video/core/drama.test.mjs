import assert from "node:assert/strict";
import { mkdirSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { approve } from "./approvals.mjs";
import {
  charactersBySpeaker,
  hasPictures,
  illustrated,
  picturesHash,
  sfxHash,
  clipKey,
  clipShotScenes,
  clipsHash,
  isClipShot,
  keyframeKey,
  lookHash,
  mixHash,
  promptSimilarity,
  resolveLook,
  resolveSubtitles,
  shotCast,
  shotLooksProblem,
  shotProblems,
  shotVisual,
  stillShotScenes,
  subtitlesHash,
  TIER_CLIP_SHARE_MAX,
  VISUAL_MODES,
  VISUAL_TIERS,
  visualTierProblems,
  voiceFor,
} from "./drama.mjs";
import { writeAudioFixture, dramaBrief, dramaFixture, fixture, fixtureLexicon, illustratedFixture, sandbox } from "./fixtures/load.mjs";
import { lintVideo } from "./lint.mjs";
import { atomicWrite } from "./paths.mjs";
import { validateVideo } from "./schema.mjs";
import { writeScreenplay } from "./screenplay.mjs";
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

test("a slides video cannot carry a cast, speakers or emotions, and a drama cannot use slide templates", () => {
  const slides = fixture();
  slides.characters = [];
  slides.series = { slug: "xianxia", episode: 1, chapter: 1 };
  slides.scenes[0].lines[0].speaker = "narrator";
  slides.scenes[0].lines[1].emotion = "calm";
  assert.deepEqual(paths(validateVideo(slides)), ["characters", "scenes[0].lines[0] (k7p2).speaker", "scenes[0].lines[1] (m4qa).emotion", "series"]);
  const drama = dramaFixture();
  drama.scenes[0].template = "bullets";
  assert.deepEqual(paths(validateVideo(drama)), ["scenes[0].template"]);
});

test("a slides video may carry a look and still shots: illustrated slides (docs/videos/ILLUSTRATED.md)", () => {
  // A look with nothing to draw, and a shot with no look, are each an error.
  const bare = fixture();
  bare.look = { preset: "tech-story" };
  assert.deepEqual(paths(validateVideo(bare)), ["look"]);
  const noLook = illustratedFixture();
  delete noLook.look;
  assert.deepEqual(paths(validateVideo(noLook)), ["look"]);
  // A slides shot is a still under a camera move: no clip, no cast, no clip-only fields, no reveal.
  const doc = illustratedFixture();
  assert.deepEqual(validateVideo(doc), []);
  assert.equal(illustrated(doc), true);
  assert.equal(hasPictures(doc), true);
  assert.equal(illustrated(fixture()), false);
  assert.equal(hasPictures(dramaFixture()), true);
  doc.scenes[1].data.visual = "clip";
  doc.scenes[1].data.characters = ["jingwei"];
  doc.scenes[1].data.fit = "auto";
  doc.scenes[1].data.start_frame = { shot: "podium", at: "last" };
  doc.scenes[2].data.end_frame = { prompt: "the desk, later" };
  doc.scenes[2].lines[0].reveal = 1;
  doc.thumbnail.data.shot = "nowhere";
  assert.deepEqual(paths(validateVideo(doc)), [
    "scenes[1].data.characters",
    "scenes[1].data.characters",
    "scenes[1].data.fit",
    "scenes[1].data.start_frame",
    "scenes[1].data.start_frame",
    "scenes[1].data.visual",
    "scenes[2].data.end_frame",
    "scenes[2].data.end_frame",
    "scenes[2].lines[0] (a3dk).reveal",
    "thumbnail.data.shot",
  ]);
  // The pictures hash follows the shots' prompts and camera words, not the cards.
  const before = picturesHash(illustratedFixture());
  const cards = illustratedFixture();
  cards.scenes[0].data.title = "另一個標題";
  assert.equal(picturesHash(cards), before);
  const prompts = illustratedFixture();
  prompts.scenes[1].data.camera = "pan left";
  assert.notEqual(picturesHash(prompts), before);
  // Sound effects name a licensed set; the hash follows the set and its gain.
  const sfx = illustratedFixture();
  sfx.sfx = { set: "Studio A", gain_db: 3, extra: 1 };
  assert.deepEqual(paths(validateVideo(sfx)), ["sfx.extra", "sfx.gain_db", "sfx.set"]);
  assert.notEqual(sfxHash(illustratedFixture()), sfxHash(fixture()));
});

test("shots, speakers, references and music are range-checked", () => {
  const doc = dramaFixture();
  doc.scenes[0].lines[0].reveal = 1;
  doc.scenes[1].lines[0].speaker = "nobody";
  doc.scenes[1].lines[1].emotion = "x".repeat(81);
  doc.scenes[0].data.characters = ["jingwei", "ghost"];
  doc.scenes[0].data.fit = "stretch";
  doc.scenes[0].data.start_frame = { shot: "bird", at: "last" };
  doc.scenes[1].data.visual = "gif";
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
    "scenes[1].data.visual",
    "scenes[1].lines[0] (x9fe).speaker",
    "scenes[1].lines[1] (b3tn).emotion",
    "scenes[1].lines[1] (b3tn).speaker",
    "scenes[2].data.seed",
    "subtitles.style",
    "thumbnail.data.shot",
  ]);
});

/** The drama example stretched to `count` shots, the first `clips` of them clips and the rest stills. */
function episodeWith(count, clips) {
  const doc = dramaFixture();
  const shot = doc.scenes[0];
  doc.scenes = Array.from({ length: count }, (_, index) => ({
    ...structuredClone(shot),
    id: `shot-${index + 1}`,
    data: { ...structuredClone(shot.data), ...(index < clips ? {} : { visual: "still" }) },
    lines: shot.lines.map((line) => ({ ...line, id: `${line.id.slice(0, 2)}${String(index).padStart(2, "0")}` })),
  }));
  doc.thumbnail.data.shot = "shot-1";
  return doc;
}

test("a shot is a clip unless it says still, and both kinds validate", () => {
  assert.deepEqual(VISUAL_MODES, ["clip", "still"]);
  const doc = dramaFixture();
  assert.equal(shotVisual(doc.scenes[0]), "clip");
  assert.equal(shotVisual(doc.scenes[4]), "clip", "a card answers clip too; callers ask isShot first");
  doc.scenes[1].data.visual = "still";
  doc.scenes[3].data.visual = "clip";
  assert.deepEqual(validateVideo(doc), []);
  assert.equal(shotVisual(doc.scenes[1]), "still");
  assert.equal(isClipShot(doc.scenes[0]), true);
  assert.equal(isClipShot(doc.scenes[1]), false);
  assert.equal(isClipShot(doc.scenes[4]), false, "the outro card is not a clip shot");
  assert.deepEqual(clipShotScenes(doc).map((scene) => scene.id), ["opening", "sea-storm", "bird"]);
  assert.deepEqual(stillShotScenes(doc).map((scene) => scene.id), ["farewell"]);
  assert.notEqual(visualHash(doc), visualHash(dramaFixture()), "flipping a shot to a still redraws the pictures");
  const explicit = dramaFixture();
  explicit.scenes[0].data.visual = "clip";
  assert.notEqual(visualHash(explicit), visualHash(dramaFixture()), "the field is part of the data hash as written");
});

test("a binge tier caps the clips, rounded up: 12 of 30 in hybrid, 3 of 30 in stills, and clips caps nothing", () => {
  assert.deepEqual(VISUAL_TIERS, ["clips", "hybrid", "stills"]);
  assert.deepEqual(TIER_CLIP_SHARE_MAX, { clips: 1, hybrid: 0.4, stills: 0.1 });
  assert.deepEqual(validateVideo(episodeWith(30, 12)), []);
  assert.deepEqual(visualTierProblems(episodeWith(30, 12), "hybrid"), { errors: [], warnings: [] });
  const hybrid = visualTierProblems(episodeWith(30, 13), "hybrid");
  assert.deepEqual(hybrid.warnings, []);
  assert.deepEqual(hybrid.errors, [{ path: "scenes", message: '13 of 30 shots are clips; the "hybrid" tier allows at most 12: mark the rest visual "still"' }]);
  assert.deepEqual(visualTierProblems(episodeWith(30, 3), "stills").errors, []);
  assert.match(visualTierProblems(episodeWith(30, 4), "stills").errors[0].message, /4 of 30 shots are clips; the "stills" tier allows at most 3/);
  assert.deepEqual(visualTierProblems(episodeWith(30, 0), "stills"), { errors: [], warnings: [] }, "no clips at all is fine");
  assert.deepEqual(visualTierProblems(episodeWith(30, 30), "clips"), { errors: [], warnings: [] });
  const remarked = visualTierProblems(episodeWith(30, 28), "clips");
  assert.deepEqual(remarked.errors, []);
  assert.equal(remarked.warnings.length, 1);
  assert.match(remarked.warnings[0].message, /^the clips tier plays every shot as a clip; 2 still shots/);
  assert.deepEqual(visualTierProblems(episodeWith(4, 4), "hybrid").errors.length, 1, "4 shots allow ceil(1.6) = 2 clips");
  assert.deepEqual(visualTierProblems(episodeWith(4, 2), "hybrid").errors, []);
  const unknown = visualTierProblems(episodeWith(4, 4), "premium");
  assert.equal(unknown.errors.length, 1);
  assert.equal(unknown.errors[0].path, "series.visual_tier");
  assert.match(unknown.errors[0].message, /"premium" is not a visual tier; the tiers are clips, hybrid, stills/);
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
  const ccOnly = dramaFixture();
  delete ccOnly.subtitles;
  assert.equal(resolveSubtitles(ccOnly).burn_in, false, "default is CC only; explicit legacy burn-in remains readable");
  assert.equal(resolveSubtitles(fixture()).burn_in, false);
});

test("shot looks validate names and keep face-sheet and speech identity while invalidating selected visuals", () => {
  const doc = dramaFixture();
  const baseLook = lookHash(doc);
  const baseSpeech = speechHash(doc, fixtureLexicon());
  const baseVisual = visualHash(doc);
  doc.characters[0].shot_looks = [{ id: "present", appearance: "adult woman in a dark business suit, short black hair" }];
  assert.equal(shotLooksProblem(doc.characters[0]), null);
  assert.equal(visualHash(doc), baseVisual, "an unused catalog entry changes no picture");
  const scene = doc.scenes.find((item) => item.id === "farewell");
  scene.data.character_looks = { jingwei: "present" };
  assert.deepEqual(paths(validateVideo(doc)), []);
  assert.equal(shotCast(doc, scene)[0].appearance, doc.characters[0].shot_looks[0].appearance);
  assert.deepEqual(shotCast(doc, scene)[0].voice, doc.characters[0].voice);
  assert.equal(lookHash(doc), baseLook, "the approved base face sheet is reused");
  assert.equal(speechHash(doc, fixtureLexicon()), baseSpeech, "a visual variant never changes a speaker");
  const selected = visualHash(doc);
  assert.notEqual(selected, baseVisual);
  doc.characters[0].shot_looks[0].appearance = "adult woman in a red suit";
  assert.notEqual(visualHash(doc), selected, "catalog edits invalidate even when the selected id stays the same");
  scene.data.character_looks = { jingwei: "unknown" };
  assert.ok(paths(validateVideo(doc)).includes("scenes[1].data.character_looks.jingwei"));
  scene.data.character_looks = { ghost: "present" };
  assert.ok(paths(validateVideo(doc)).includes("scenes[1].data.character_looks.ghost"));
  doc.characters[0].shot_looks = [{ id: "xx", appearance: "coat", voice: { name: "other" } }];
  assert.match(shotLooksProblem(doc.characters[0]), /only id/);
  doc.characters[0].shot_looks = [{ id: "xx", appearance: "coat" }, { id: "xx", appearance: "hat" }];
  assert.match(shotLooksProblem(doc.characters[0]), /duplicate/);
  doc.characters[0].shot_looks = {};
  assert.doesNotThrow(() => validateVideo(doc), "invalid catalogs produce lint errors rather than crashing");
  assert.doesNotThrow(() => visualHash(doc), "status can hash a malformed script before reporting its lint errors");
  assert.match(shotLooksProblem({ shot_looks: [{ id: ["present"], appearance: "coat" }] }), /only id/);
});

test("each line gets its speaker's voice, and a Gemini voice takes the emotion in its style", () => {
  const doc = dramaFixture();
  assert.equal(voiceFor(doc, doc.scenes[0].lines[0]).name, "Sulafat");
  const jingwei = voiceFor(doc, doc.scenes[1].lines[0]);
  assert.equal(jingwei.name, "Kore");
  assert.equal(jingwei.style, "清亮、倔強的少女聲，台灣國語。開心、有點急");
  assert.deepEqual(charactersBySpeaker(doc), { narrator: [...doc.scenes[0].lines[0].text, ...doc.scenes[0].lines[1].text, ...doc.scenes[2].lines[0].text, ...doc.scenes[2].lines[1].text, ...doc.scenes[3].lines[0].text, ...doc.scenes[4].lines[0].text, ...doc.scenes[4].lines[1].text].length, jingwei: [...doc.scenes[1].lines[0].text, ...doc.scenes[3].lines[1].text].length, yandi: [...doc.scenes[1].lines[1].text].length });
});

test("drama-local pronunciation and exact-take references validate before synthesis", () => {
  const doc = dramaFixture();
  doc.pronunciation_hints = { 精衛: "ㄐㄧㄥ ㄨㄟˋ", 炎帝: null };
  const source = doc.scenes[1].lines[0];
  doc.scenes[3].lines[1] = { ...source, id: "copy1", audio_ref: source.id, pause_after_ms: 900 };
  assert.deepEqual(validateVideo(doc), []);
  for (const mutate of [
    (bad) => { bad.pronunciation_hints = { English: "not a production Chinese term" }; },
    (bad) => { bad.pronunciation_hints = { 精衛: 42 }; },
    (bad) => { bad.pronunciation_hints = []; },
    (bad) => { bad.scenes[3].lines[1].audio_ref = "copy1"; },
    (bad) => { bad.scenes[1].lines[0].audio_ref = "copy1"; },
    (bad) => { bad.scenes[3].lines[1].speaker = "yandi"; },
    (bad) => { bad.scenes[3].lines[1].emotion = "完全不同的演法"; },
    (bad) => { bad.scenes[3].lines[1].text = "另一句台詞。"; },
  ]) {
    const bad = structuredClone(doc); mutate(bad);
    assert.ok(validateVideo(bad).length);
  }
  const overflow = structuredClone(doc);
  overflow.characters[0].voice.style = "字".repeat(399);
  assert.ok(validateVideo(overflow).some((error) => error.message.includes("exceeds 400")));
  const slides = fixture();
  slides.pronunciation_hints = { 精衛: "ㄐㄧㄥ ㄨㄟˋ" };
  slides.scenes[0].lines[1].audio_ref = slides.scenes[0].lines[0].id;
  assert.ok(validateVideo(slides).some((error) => error.path === "pronunciation_hints"));
  assert.ok(validateVideo(slides).some((error) => error.path.endsWith("audio_ref")));
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
  // Music under slides is the channel's own now (docs/videos/ILLUSTRATED.md): no warning.
  const slides = fixture();
  slides.music = { track: "a.mp3" };
  assert.ok(!lintVideo(slides, context({ brief: undefined, lexicon: fixtureLexicon() })).warnings.some((warning) => warning.path === "music"));
});

test("a drama's status walks the media steps in order, each bound to its hashes", async () => {
  const box = sandbox("fixture-drama", "drama");
  const status = () => pipelineStatus({ slug: box.slug, root: box.root, workdir: box.workdir });
  assert.deepEqual(stepsFor(dramaFixture()), DRAMA_STEPS, "every drama reads its screenplay before the sheets (docs/videos/DRAMA-FLOW.md)");
  assert.deepEqual(stepsFor({ ...dramaFixture(), series: { slug: "xianxia", episode: 1, chapter: 1 } }), DRAMA_STEPS);
  assert.deepEqual(stepsFor({ ...dramaFixture(), music: undefined }), DRAMA_STEPS.filter((id) => id !== "music generated"));
  assert.equal(stepsFor(fixture()), SLIDES_STEPS);
  assert.deepEqual((await status()).steps.map((step) => step.id), stepsFor(dramaFixture()));
  const places = { docDir: box.dir, workdir: box.workdir };
  mkdirSync(box.workdir, { recursive: true });
  await approve({ gate: "outline", ...places });
  writeFileSync(path.join(box.dir, "verify-1.md"), "# ok\n");
  // The owner reads the screenplay before any sheet is drawn (docs/videos/DRAMA-FLOW.md, section 2).
  assert.equal((await status()).next.id, "script approved");
  writeScreenplay(box.dir, dramaFixture());
  await approve({ gate: "script", ...places });
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
  const audioTimeline = writeAudioFixture({ ...estimateTimeline(project.doc), speech_hash: speech }, box.workdir);
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
  write("checks.json", { ok: true, narration_sha256: audioTimeline.audio_evidence.narration_sha256, speech_hash: speech, visual_hash: visual, look_hash: look, clips_hash: "c0", subtitles_hash: subtitlesHash(project.doc), mix_hash: mixHash(project.doc) });
  assert.equal((await status()).next.id, "video assembled", "the checks must name the clips that were joined");
  write("checks.json", { ok: true, narration_sha256: audioTimeline.audio_evidence.narration_sha256, speech_hash: speech, visual_hash: visual, look_hash: look, clips_hash: "c1", subtitles_hash: subtitlesHash(project.doc), mix_hash: mixHash(project.doc) });
  assert.equal((await status()).next.id, "captions written");
});

test("a still shot carries no end frame: it describes a clip's last frame and would be bought unseen", () => {
  const doc = dramaFixture();
  const shot = doc.scenes.find((scene) => scene.template === "shot");
  shot.data.visual = "still";
  shot.data.end_frame = { prompt: "the same room, empty" };
  const problems = validateVideo(doc).filter((problem) => problem.path.endsWith(".end_frame"));
  assert.deepEqual(problems.map((problem) => problem.message), ["a still shot has no end_frame: it belongs to a clip"]);
  delete shot.data.end_frame;
  assert.deepEqual(validateVideo(doc).filter((problem) => problem.path.includes(shot.id)), []);
});
