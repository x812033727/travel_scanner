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

function longAnimeEpisode() {
  const doc = dramaFixture();
  doc.slug = "borrowed-dawn-production-e001";
  doc.category = "anime";
  doc.look = { preset: "anime-2d" };
  doc.target_minutes = [22, 22];
  doc.production_policy = "long-anime-v1";
  doc.runtime_spec = { body_target_seconds: 1320, op_ed_budget_seconds: 180, broadcast_slot_seconds: 1800, slot_reserve_seconds: 300 };
  doc.series = { slug: "borrowed-dawn-production", episode: 1, chapter: 1, kind: "series", genre: "custom", lead: "ensemble", planned_episodes: 120, open_ended: false, closed_ending: false };
  for (const scene of doc.scenes) delete scene.data.fit;
  return doc;
}

test("a native long-anime video keeps its policy at the root and its declared series identity", () => {
  assert.deepEqual(validateVideo(longAnimeEpisode()), []);
  for (const [change, expected] of [
    [(doc) => { delete doc.series; }, /kind.*series|genre.*custom|lead.*ensemble/],
    [(doc) => { doc.category = "drama"; }, /category must be anime/],
    [(doc) => { doc.look.preset = "cinematic-3d"; }, /style preset must be anime-2d/],
    [(doc) => { doc.series.kind = "story"; }, /kind must be series/],
    [(doc) => { doc.series.genre = "urban-return"; }, /genre must be custom/],
    [(doc) => { doc.series.lead = "male"; }, /lead must be ensemble/],
    [(doc) => { doc.target_minutes = [21, 23]; }, /target_minutes must match/],
    [(doc) => { doc.production_policy = "long-anime-v2"; }, /production_policy must be long-anime-v1/],
    [(doc) => { delete doc.runtime_spec; }, /runtime_spec must be an object/],
    [(doc) => { delete doc.production_policy; }, /production_policy must be long-anime-v1/],
  ]) {
    const doc = longAnimeEpisode();
    change(doc);
    assert.match(validateVideo(doc).map((error) => error.message).join("\n"), expected);
  }
});

test("anime category alone does not enable a body longer than eight minutes", () => {
  const doc = dramaFixture();
  doc.category = "anime";
  doc.look = { preset: "anime-2d" };
  doc.target_minutes = [1, 8];
  assert.deepEqual(validateVideo(doc), [], "existing short drama remains structurally valid with the anime category");
  doc.target_minutes = [22, 22];
  assert.ok(validateVideo(doc).some((error) => error.path === "production_policy" && /explicit long-anime/.test(error.message)));
});

test("silent long-anime action shots accept the one- and eight-second bounds without invented dialogue", () => {
  for (const seconds of [1, 8]) {
    const doc = longAnimeEpisode();
    doc.scenes[1].action_seconds = seconds;
    doc.scenes[1].lines = [];
    doc.scenes[1].data.prompt = "medium shot of a worker lifting a heavy valve handle with both hands";
    doc.scenes[1].data.motion = "the worker lifts the handle, takes its weight and lowers it into the bracket";
    assert.deepEqual(validateVideo(doc), []);
    const timeline = estimateTimeline(doc);
    const shot = timeline.scenes.find((scene) => scene.id === doc.scenes[1].id);
    assert.equal(shot.end_frame - shot.start_frame, seconds * 30);
    assert.ok(!timeline.lines.some((line) => line.scene === doc.scenes[1].id));
  }
});

test("timed action refuses out-of-range seconds, dialogue, absent direction and an ordinary drama", () => {
  const base = longAnimeEpisode();
  base.scenes[1].action_seconds = 4;
  base.scenes[1].lines = [];
  for (const seconds of [0, 9, -1, 1.5, "4", null]) {
    const doc = structuredClone(base);
    doc.scenes[1].action_seconds = seconds;
    assert.ok(validateVideo(doc).some((error) => error.path === "scenes[1].action_seconds" && /integer from 1 to 8/.test(error.message)), String(seconds));
  }
  for (const [change, expected] of [
    [(doc) => { doc.scenes[1].lines = [{ id: "act1", text: "還有一句對白。", speaker: "jingwei" }]; }, /empty lines array/],
    [(doc) => { delete doc.scenes[1].lines; }, /empty lines array|non-empty array/],
    [(doc) => { delete doc.scenes[1].data.motion; }, /visible-action prompt and motion/],
    [(doc) => { doc.scenes[1].data.motion = "  "; }, /visible-action prompt and motion/],
    [(doc) => { doc.scenes[1].data.prompt = ""; }, /visible-action prompt and motion/],
    [(doc) => { doc.scenes[1].template = "title"; }, /directed shot/],
    [(doc) => { delete doc.production_policy; delete doc.runtime_spec; }, /complete long-anime production policy/],
  ]) {
    const doc = structuredClone(base);
    change(doc);
    assert.match(validateVideo(doc).map((error) => error.message).join("\n"), expected);
  }
  const ordinary = dramaFixture();
  ordinary.scenes[1].action_seconds = 4;
  ordinary.scenes[1].lines = [];
  assert.ok(validateVideo(ordinary).some((error) => error.path === "scenes[1].action_seconds" && /complete long-anime/.test(error.message)));
  assert.ok(validateVideo(ordinary).some((error) => error.path === "scenes[1].lines"));
});

test("only the declared last episode of a closed anime may declare closure", () => {
  const final = longAnimeEpisode();
  final.series.episode = 120;
  final.series.chapter = 10;
  final.series.closed_ending = true;
  assert.deepEqual(validateVideo(final), []);
  for (const [change, expected] of [
    [(doc) => { doc.series.episode = 119; }, /only the declared final episode/],
    [(doc) => { doc.series.open_ended = true; }, /only the declared final episode/],
    [(doc) => { doc.series.closed_ending = false; }, /must deliver its approved closed ending/],
    [(doc) => { delete doc.series.closed_ending; }, /boolean declaration|must deliver/],
    [(doc) => { doc.series.open_ended = "false"; }, /boolean declaration/],
    [(doc) => { doc.series.planned_episodes = 119; }, /positive episode count/],
    [(doc) => { doc.series.planned_episodes = 0; }, /positive episode count/],
  ]) {
    const doc = structuredClone(final);
    change(doc);
    assert.match(validateVideo(doc).map((error) => error.message).join("\n"), expected);
  }
});

test("long anime rejects freeze and slow fitting while ordinary drama retains both", () => {
  for (const fit of ["freeze", "slow"]) {
    const anime = longAnimeEpisode();
    anime.scenes[1].data.fit = fit;
    assert.ok(validateVideo(anime).some((error) => error.path === "scenes[1].data.fit" && /frozen tails or slowed clips/.test(error.message)));
    const ordinary = dramaFixture();
    ordinary.scenes[1].data.fit = fit;
    assert.deepEqual(validateVideo(ordinary), []);
  }
});

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

test("illustrated slides are drawn as a printmaker's brief and lint keeps their pictures varied (docs/videos/ILLUSTRATED.md §畫面不像 AI)", async () => {
  const { PRESETS, SLIDES_PRESET, cameraMove, pictureVarietyProblems, shotProblems, SAME_MOVE_RUN_MAX, MOTIF_MIN_SHOTS, MOTIF_SHARE_WARN } = await import("./drama.mjs");
  const { estimateTimeline } = await import("./timeline.mjs");
  const preset = PRESETS[SLIDES_PRESET];
  assert.match(preset.style, /^hand-drawn editorial illustration for a printed magazine feature/);
  assert.match(preset.style, /paper grain and a little misregistration/);
  assert.match(preset.style, /small simple people with dot eyes or seen from behind/);
  for (const word of ["glossy", "faceless mannequin", "mirror symmetry", "text", "logo", "real person's likeness", "mascot", "extra fingers"]) assert.ok(preset.negative.includes(word), word);
  assert.ok(preset.style.length <= 600 && preset.negative.length <= 400);
  // The subject stays where a Short's 9:16 crop keeps it; nothing pushes it to one side.
  assert.match(preset.style, /one clear focal point in the centre third of the frame/);
  assert.doesNotMatch(`${preset.style} ${preset.negative}`, /off-centre|centred layout/);
  // The camera words fold to their move, the camera direction first and then the motion prompt,
  // as assemble reads them; a shot that names none drifts.
  assert.equal(cameraMove({ camera: "slow push in" }), "push in");
  assert.equal(cameraMove({ camera: "pan right along the shelf" }), "pan right");
  assert.equal(cameraMove({ camera: "handheld" }), "drift");
  assert.equal(cameraMove({ camera: "handheld", motion: "slow push in" }), "push in");
  assert.equal(cameraMove({ camera: "pan left", motion: "zoom in" }), "pan left");
  assert.equal(cameraMove({}), "drift");
  // The example keeps the rules; a drama is not held to them.
  const doc = illustratedFixture();
  assert.deepEqual(pictureVarietyProblems(doc), { errors: [], warnings: [] });
  assert.deepEqual(pictureVarietyProblems(dramaFixture()), { errors: [], warnings: [] });
  const shots = doc.scenes.filter((scene) => scene.template === "shot");
  // Three stills in a row under one move is an error (the second is allowed).
  assert.equal(SAME_MOVE_RUN_MAX, 2);
  const run = illustratedFixture();
  run.scenes.find((scene) => scene.id === "desk").data.camera = "push in";
  assert.deepEqual(pictureVarietyProblems(run).errors, []);
  run.scenes.find((scene) => scene.id === "clock").data.camera = "dolly in";
  const errors = pictureVarietyProblems(run).errors;
  assert.deepEqual(errors.map((error) => error.path), ["scenes[3] (clock).data.camera"]);
  assert.match(errors[0].message, /3 stills in a row under "push in"; alternate the moves/);
  assert.ok(shotProblems(run, estimateTimeline(run)).errors.some((error) => error.path === "scenes[3] (clock).data.camera"), "lint reads it through shotProblems");
  // No shot size, or the look's own words, are warnings gathered per video, not per shot.
  const flat = illustratedFixture();
  flat.scenes.find((scene) => scene.id === "podium").data.prompt = "flat editorial illustration of a podium with three trophies, deep teal ground, warm cream shapes";
  flat.scenes.find((scene) => scene.id === "race").data.prompt = "two runners on a track at night, amber floodlight";
  const warnings = pictureVarietyProblems(flat).warnings;
  assert.equal(warnings.length, 2, JSON.stringify(warnings));
  assert.match(warnings[0].message, /^2 of 5 pictures name no shot size .*: say how close the camera is in podium, race$/);
  assert.match(warnings[1].message, /^2 of 5 pictures restate the look \("flat editorial illustration", "amber"\); the look adds the style and the palette, the prompt describes the picture: podium, race$/);
  // Prompts written as the guide asks raise nothing: the sizes it names are sizes here, a noun
  // that happens to be a palette word is not the look, and neither a stopword's plural nor the
  // shot-size word every prompt opens with is a motif.
  const guided = illustratedFixture();
  const written = [
    "Medium: a baker kneading dough at a workshop bench before dawn, flour on the boards, figures passing the window",
    "Close up of a kettle on a stove, steam against a tiled wall, figures reflected in the metal",
    "Extreme close up of a key in a worn lock, a thumb on the bow",
    "Medium, a harbour at dusk, a child holding an ice cream cone beside two figures on the quay",
    "Medium view of a classroom after hours, chairs stacked on benches, one coat left on a hook",
  ];
  guided.scenes.filter((scene) => scene.template === "shot").forEach((scene, index) => { scene.data.prompt = written[index]; });
  guided.scenes.push({ id: "sixth", template: "shot", data: { prompt: "Medium shot of a market stall, a vendor weighing fruit on brass scales, crates behind", camera: "pull out", visual: "still" }, lines: [{ id: "s6zz", text: "第六張。" }] });
  assert.deepEqual(pictureVarietyProblems(guided), { errors: [], warnings: [] });
  // A place or an object in more than a third of the pictures, once there are enough to count.
  assert.equal(MOTIF_MIN_SHOTS, 6);
  assert.equal(MOTIF_SHARE_WARN, 1 / 3);
  const desks = illustratedFixture();
  const extra = shots.map((scene, index) => ({ ...scene, id: `more-${index}`, data: { ...scene.data, prompt: `Close-up of a wooden desk with a brass lamp ${index}`, camera: ["pull out", "tilt up", "drift", "pan left", "push in"][index] }, lines: [{ id: `m${index}zz`, text: "再一張。" }] }));
  desks.scenes.push(...extra);
  const motifs = pictureVarietyProblems(desks).warnings.filter((warning) => /pictures \(a third is plenty\)/.test(warning.message));
  assert.deepEqual(motifs.map((warning) => warning.message), [`"lamp" is in 6 of 10 pictures (a third is plenty): give each chapter its own place and props so the video travels`, `"desk" is in 5 of 10 pictures (a third is plenty): give each chapter its own place and props so the video travels`]);
  assert.equal(pictureVarietyProblems(desks).errors.length, 0);
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
