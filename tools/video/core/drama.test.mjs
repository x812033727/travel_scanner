import assert from "node:assert/strict";
import { createHash } from "node:crypto";
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
  drawnShotScenes,
  isClipShot,
  isKnowledgeLongform,
  isSourced,
  sourcedShotScenes,
  timesSilentShots,
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
import { writeAudioFixture, dramaBrief, dramaFixture, enFixture, explainerFixture, fixture, fixtureBrief, fixtureLexicon, illustratedBrief, illustratedFixture, sandbox, storyFixture } from "./fixtures/load.mjs";
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
    [(doc) => { delete doc.production_policy; delete doc.runtime_spec; }, /a drama with a cast and no length floor, or a complete long-anime production policy/],
  ]) {
    const doc = structuredClone(base);
    change(doc);
    assert.match(validateVideo(doc).map((error) => error.message).join("\n"), expected);
  }
  // A drama with a cast may hold a beat in which nobody speaks (docs/videos/DRAMA.md); a
  // narrated one has no silent shot, since its narration is its clock.
  const ordinary = dramaFixture();
  ordinary.scenes[1].action_seconds = 4;
  ordinary.scenes[1].lines = [];
  assert.deepEqual(validateVideo(ordinary), []);
  const narrated = structuredClone(ordinary);
  narrated.characters = [];
  for (const scene of narrated.scenes) {
    delete scene.data.characters;
    for (const line of scene.lines) delete line.speaker;
  }
  assert.ok(validateVideo(narrated).some((error) => error.path === "scenes[1].action_seconds" && /a drama with a cast and no length floor, or a complete long-anime/.test(error.message)));
  assert.ok(validateVideo(narrated).some((error) => error.path === "scenes[1].lines"));
});

test("a silent shot cannot pad a knowledge long-form's floor: a brand story with a lead refuses action_seconds, as the schema and the timeline both say", () => {
  const story = storyFixture();
  story.slug = "story-rolling-suitcase";
  story.characters = [structuredClone(dramaFixture().characters[0])];
  const lead = story.characters[0].id;
  story.scenes.push({ id: "silent-beat", template: "shot", action_seconds: 8, data: { prompt: "The lead at the counter, the suitcase held out", camera: "Wide, locked", motion: "The lead slides the suitcase across the counter", visual: "still", characters: [lead] }, lines: [] });
  const silent = story.scenes.length - 1;
  const errors = validateVideo(story);
  assert.ok(errors.some((error) => error.path === `scenes[${silent}].action_seconds` && /no length floor/.test(error.message)), errors.map((error) => `${error.path}: ${error.message}`).join("\n"));
  assert.ok(errors.some((error) => error.path === `scenes[${silent}].lines`));
  assert.throws(() => estimateTimeline(story), /action_seconds needs a silent shot of a long anime or of a drama with a cast and no length floor/);
  assert.equal(timesSilentShots(story), false);
  assert.equal(isKnowledgeLongform(story), true);
  // The same shot under a slug outside the catalogues, with a category the floors do not know, is an ordinary cast drama.
  const plain = structuredClone(story);
  plain.slug = "rolling-suitcase";
  delete plain.category;
  assert.equal(timesSilentShots(plain), true);
  assert.ok(!validateVideo(plain).some((error) => error.path.endsWith(".action_seconds")));
  // An anime episode times nothing outside its production policy, and an explainer never does.
  assert.equal(timesSilentShots({ ...plain, category: "anime" }), false);
  assert.equal(timesSilentShots({ ...plain, look: { ...plain.look, preset: "flat-explainer" } }), false);
  assert.equal(timesSilentShots(dramaFixture()), true);
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

test("the drama example is valid and lints clean, apart from the craft rows a four-shot retelling cannot meet", () => {
  assert.deepEqual(validateVideo(dramaFixture()), []);
  const result = lintVideo(dramaFixture(), context());
  assert.deepEqual(result.errors, []);
  // The example shows the file's shape, not an episode: narrated, four shots, long lines. The
  // craft rows (drama-craft.md) say so, and nothing else does.
  assert.deepEqual(result.warnings.filter((warning) => !/^craft /.test(warning.message)), []);
  assert.ok(result.warnings.some((warning) => /^craft hook\.opening: /.test(warning.message)));
  assert.equal(result.summary.chapters.length, 3);
});

test("a slides video cannot carry a cast, speakers or repeated takes, while a cue is any line's; a drama cannot use slide templates", () => {
  const slides = fixture();
  slides.characters = [];
  slides.series = { slug: "xianxia", episode: 1, chapter: 1 };
  slides.scenes[0].lines[0].speaker = "narrator";
  slides.scenes[0].lines[1].emotion = "calm";
  slides.scenes[0].lines[1].audio_ref = slides.scenes[0].lines[0].id;
  assert.deepEqual(paths(validateVideo(slides)), ["characters", "scenes[0].lines[0] (k7p2).speaker", "scenes[0].lines[1] (m4qa).audio_ref", "series"]);
  // The cue is range-checked for every format (docs/videos/ILLUSTRATED.md §聲音表演).
  const cued = fixture();
  cued.scenes[0].lines[1].emotion = "x".repeat(81);
  assert.deepEqual(paths(validateVideo(cued)), ["scenes[0].lines[1] (m4qa).emotion"]);
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
  // The cue sheet (docs/videos/ILLUSTRATED.md §配樂與音效): a sound as a scene opens or on a frame,
  // one of the two, by a sound's name, with an optional gain; sha256 binds the set's manifest.
  const cues = illustratedFixture();
  cues.sfx = { set: "studio-a", sha256: "b".repeat(64), cues: [{ scene: "door", sound: "bell", gain_db: -3 }, { frame: 120, sound: "stamp" }, { frame: 0, sound: "soft_chime-2" }] };
  assert.deepEqual(validateVideo(cues), []);
  const badCues = illustratedFixture();
  badCues.sfx = { set: "studio-a", sha256: "nope", cues: [{ scene: "nowhere", sound: "bell" }, { frame: -1, sound: "Bell!" }, { scene: "door", frame: 3, sound: "pop", gain_db: 13, extra: 1 }, "pop"] };
  assert.deepEqual(paths(validateVideo(badCues)), ["sfx.cues[0].scene", "sfx.cues[1].frame", "sfx.cues[1].sound", "sfx.cues[2]", "sfx.cues[2].extra", "sfx.cues[2].gain_db", "sfx.cues[3]", "sfx.sha256"]);
  const tooMany = illustratedFixture();
  tooMany.sfx = { set: "studio-a", cues: Array.from({ length: 201 }, () => ({ scene: "door", sound: "pop" })) };
  assert.deepEqual(paths(validateVideo(tooMany)), ["sfx.cues"]);
  // The hash follows the cue sheet and the bound manifest; a script with neither hashes as it did before them.
  assert.notEqual(sfxHash(cues), sfxHash(illustratedFixture()), "a cue sheet");
  assert.notEqual(sfxHash({ ...illustratedFixture(), sfx: { set: "studio-a", sha256: "b".repeat(64) } }), sfxHash(illustratedFixture()), "a bound manifest");
  assert.equal(sfxHash(illustratedFixture()), sfxHash({ ...illustratedFixture(), sfx: { set: "studio-a", gain_db: -12 } }), "the default gain spelled out is the same track");
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
  const picture = (id) => {
    const file = `keyframes/${id}-1.png`;
    const bytes = `synthetic selected picture: ${id}`;
    atomicWrite(path.join(box.workdir, file), bytes);
    return { file, sha256: createHash("sha256").update(bytes).digest("hex") };
  };
  const shots = Object.fromEntries(drawnShotScenes(project.doc).map((scene) => [scene.id, {
    ...picture(scene.id), needs_review: scene.id === "opening", judge: { overall: 8, passed: true, problems: [] },
    ...(scene.data.end_frame?.prompt ? { end_frame: picture(`${scene.id}-end`) } : {}),
  }]));
  write("keyframes/manifest.json", { look_hash: look, visual_hash: visual, shots });
  assert.match((await status()).next.note, /opening keyframe needs review/);
  shots.opening.needs_review = false;
  write("keyframes/manifest.json", { look_hash: look, visual_hash: visual, shots });
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
  const { PRESETS, SLIDES_PRESET, SLIDES_PRESETS, PRESET_NAMES, slidesPresetFor, cameraMove, pictureVarietyProblems, shotProblems, SAME_MOVE_RUN_MAX, MOTIF_MIN_SHOTS, MOTIF_SHARE_WARN } = await import("./drama.mjs");
  const { estimateTimeline } = await import("./timeline.mjs");
  // The print looks (docs/videos/ILLUSTRATED.md §第二輪): four pairs of risograph inks and a
  // linocut, each a printmaker's brief with the subject where a Short's 9:16 crop keeps it, no
  // "full-bleed" (the model paints a margin for it) and a negative that refuses borders instead.
  assert.deepEqual(SLIDES_PRESETS, ["riso-teal", "riso-navy", "riso-forest", "riso-plum", "linocut-teal"]);
  assert.equal(SLIDES_PRESET, "riso-teal");
  for (const name of SLIDES_PRESETS) {
    const preset = PRESETS[name];
    assert.ok(PRESET_NAMES.includes(name), name);
    assert.match(preset.style, name.startsWith("riso") ? /^risograph print illustration on warm cream paper: .* ink and .* ink, overprinted where they meet, visible halftone dot grain/ : /^two-colour linocut relief print on cream paper/);
    assert.match(preset.style, /small simple people with (?:carved )?dot eyes or seen from behind/);
    assert.match(preset.style, /one clear focal point in the centre third of the frame/);
    assert.match(preset.style, /the picture runs past all four edges of the frame/);
    assert.doesNotMatch(preset.style, /full[- ]bleed|edge to edge|no (?:ink )?outlines/);
    for (const word of ["glossy", "faceless mannequin", "mirror symmetry", "paper border", "white margin", "pillarbox", "blurred side bars", "text", "logo", "real person's likeness", "mascot", "extra fingers"]) assert.ok(preset.negative.includes(word), `${name}: ${word}`);
    assert.ok(preset.style.length <= 600 && preset.negative.length <= 400, `${name}: ${preset.style.length}/${preset.negative.length}`);
    assert.doesNotMatch(`${preset.style} ${preset.negative}`, /off-centre|centred layout/);
  }
  assert.equal(new Set(SLIDES_PRESETS.map((name) => PRESETS[name].style)).size, SLIDES_PRESETS.length, "every look is its own inks");
  // The look of a video with none is one of the rotation, by its slug: stable for a video, spread across videos.
  assert.equal(slidesPresetFor("fixture-illustrated"), slidesPresetFor("fixture-illustrated"));
  assert.ok(SLIDES_PRESETS.includes(slidesPresetFor("anything")));
  assert.ok(SLIDES_PRESETS.includes(slidesPresetFor(undefined)));
  const spread = new Set(["ai-term-token", "ai-term-context-window", "gemini-4-argon-who-can-use-it", "threads-parental-supervision-apac-four-settings", "grok-4-7-bedrock-output-doubles", "fixture-illustrated"].map(slidesPresetFor));
  assert.ok(spread.size >= 4, [...spread].join(", "));
  // The 2026-10-03 morning look stays for a video that names it.
  const preset = PRESETS["tech-story"];
  assert.match(preset.style, /^hand-drawn editorial illustration for a printed magazine feature/);
  assert.match(preset.style, /one clear focal point in the centre third of the frame/);
  assert.doesNotMatch(`${preset.style} ${preset.negative}`, /off-centre|centred layout/);
  // The camera words fold to their move, read from the camera direction alone on whole words,
  // as assemble reads them; a shot that names none drifts, and "locked" holds the picture still.
  assert.equal(cameraMove({ camera: "slow push in" }), "push in");
  assert.equal(cameraMove({ camera: "pan right along the shelf" }), "pan right");
  assert.equal(cameraMove({ camera: "handheld" }), "drift");
  assert.equal(cameraMove({ camera: "handheld", motion: "slow push in" }), "drift", "the motion prompt is what happens in the picture, never the camera");
  assert.equal(cameraMove({ camera: "pan left", motion: "zoom in" }), "pan left");
  assert.equal(cameraMove({ motion: "she pushes the box back and rises" }), "drift");
  assert.equal(cameraMove({ camera: "a surprised enterprise" }), "drift", "\"rise\" inside a word is no tilt");
  assert.equal(cameraMove({ camera: "a slow rise" }), "tilt up");
  assert.equal(cameraMove({ camera: "Locked medium close-up" }), "locked");
  assert.equal(cameraMove({ camera: "static, slight handheld drift" }), "drift", "the drift the writer asked for wins over \"static\"");
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

test("the picture-variety lint reads a size as a size, a prop in both numbers as one prop, a repeated move on the camera alone, and a video told in the dark", async () => {
  const { pictureVarietyProblems, DARK_SHARE_WARN, MOTIF_MIN_SHOTS } = await import("./drama.mjs");
  const moves = ["push in", "pull out", "pan left", "pan right", "tilt up", "tilt down", "drift", "push in", "pull out", "pan left"];
  const video = (prompts, extra = {}) => {
    const doc = illustratedFixture();
    doc.scenes = doc.scenes.filter((scene) => scene.template !== "shot");
    prompts.forEach((prompt, index) => doc.scenes.push({ id: `p${index}`, template: "shot", data: { prompt, camera: moves[index], visual: "still", ...extra }, lines: [{ id: `l${index}zz`, text: "一句。" }] }));
    return doc;
  };
  const sized = (prompt) => !pictureVarietyProblems(video([prompt])).warnings.some((warning) => /name no shot size/.test(warning.message));
  // The sizes in their usual spellings, at the start or followed by shot, view, angle or of.
  for (const prompt of ["Low-angle shot of a lighthouse at noon", "Bird's eye view of a harbour market", "Top-down view of a tiled kitchen floor", "Over-the-shoulder shot of a cook", "High angle of a schoolyard", "A wide shot of a street at noon", "Medium, a harbour at dusk"]) assert.ok(sized(prompt), prompt);
  // An incidental adjective is not a size.
  for (const prompt of ["A medium bowl of rice on a table at noon", "Onions over medium heat in a pan", "A wide street at noon, a cyclist crossing"]) assert.ok(!sized(prompt), prompt);
  // Dairy is not the palette; a cream wall is.
  const restates = (prompt) => pictureVarietyProblems(video([`Close-up of ${prompt}`])).warnings.some((warning) => /restate the look/.test(warning.message));
  for (const prompt of ["whipped cream on a cake", "cream poured into coffee", "an ice-cream cone melting", "sour cream on a plate"]) assert.ok(!restates(prompt), prompt);
  for (const prompt of ["a cream wall with a crack", "a risograph poster on a door"]) assert.ok(restates(prompt), prompt);
  // Plurals fold: ferries and a ferry, shelves and a shelf, boxes and a box are one thing each.
  const motifs = (prompts) => pictureVarietyProblems(video(prompts)).warnings.filter((warning) => /a third is plenty/.test(warning.message)).map((warning) => warning.message);
  assert.equal(MOTIF_MIN_SHOTS, 6);
  const folded = motifs(["Wide shot of a ferry at noon", "Wide shot of ferries at noon", "Wide shot of a ferry in rain", "Wide shot of ferries in fog", "Close-up of a shelf of jars", "Close-up of shelves of jars", "Close-up of shelves", "Close-up of a box of nails", "Close-up of boxes of nails", "Close-up of boxes", "Medium shot of potatoes"]);
  assert.deepEqual(folded, [
    `"ferry" is in 4 of 11 pictures (a third is plenty): give each chapter its own place and props so the video travels`,
  ], "ferry, four of eleven, is over a third; shelf and box, three of eleven, are not");
  assert.deepEqual(motifs(["Wide shot of shoes on a mat", "Close-up of a shoe", "Wide shot of canoes", "Medium shot of a canoe", "Wide shot of a series of arches", "Wide shot of a species of moth"]), [], "shoes keep their o; series and species are not plurals");
  // The motion prompt is what happens in the picture, never the camera: three handheld stills
  // stay a run under "drift" on data.camera whatever their motion prompts say.
  const motion = video(["Wide shot of a quay at noon", "Close-up of a rope", "Medium shot of a crane"], { camera: "handheld" });
  motion.scenes.filter((scene) => scene.template === "shot").forEach((scene) => { scene.data.motion = "slow push in"; });
  const fromMotion = pictureVarietyProblems(motion).errors;
  assert.deepEqual(fromMotion.map((error) => error.path), ["scenes[6] (p2).data.camera"]);
  assert.match(fromMotion[0].message, /3 stills in a row under "drift"/);
  const fromCamera = video(["Wide shot of a quay at noon", "Close-up of a rope", "Medium shot of a crane"], { camera: "push in" });
  assert.deepEqual(pictureVarietyProblems(fromCamera).errors.map((error) => error.path), ["scenes[6] (p2).data.camera"]);
  assert.match(pictureVarietyProblems(fromCamera).errors[0].message, /tilt down, drift\)$/);
  // More than half of the pictures at night or under a lamp is a warning once there are enough to count.
  assert.equal(DARK_SHARE_WARN, 1 / 2);
  const dark = ["Wide shot of a street at night", "Close-up of a lamp on a desk", "Medium shot of a bench at dusk", "Low angle of a tower by moonlight"];
  const day = ["Wide shot of a beach at noon", "Close-up of a kettle in a kitchen"];
  const told = pictureVarietyProblems(video([...dark, ...day])).warnings.filter((warning) => /at night or under a lamp/.test(warning.message));
  assert.deepEqual(told.map((warning) => warning.message), ["4 of 6 pictures are at night or under a lamp; vary the time of day, the weather and where the light comes from (morning, noon, rain, an overcast afternoon, a crowded daylight place): p0, p1, p2, p3"]);
  assert.deepEqual(pictureVarietyProblems(video([...dark.slice(0, 3), ...day, "Medium shot of a bakery at dawn"])).warnings.filter((warning) => /under a lamp/.test(warning.message)), [], "half is not more than half");
  assert.deepEqual(pictureVarietyProblems(video(dark)).warnings.filter((warning) => /under a lamp/.test(warning.message)), [], "fewer than six pictures are not counted");
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

test("a shot cut from another shot's clip names an earlier clip shot and a start; it has no still, continuation, end frame or thumbnail of its own", () => {
  const base = dramaFixture();
  const bird = base.scenes.find((scene) => scene.id === "bird");
  delete bird.data.start_frame;
  bird.data.source = { shot: "sea-storm", from_s: 1.5 };
  assert.deepEqual(validateVideo(base), []);
  const messagesOf = (change) => {
    const doc = structuredClone(base);
    change(doc);
    return validateVideo(doc).map((error) => `${error.path}: ${error.message}`).join("\n");
  };
  assert.match(messagesOf((doc) => { doc.scenes[3].data.source = { shot: "wrap", from_s: 1 }; }), /must be \{ shot: "<an earlier shot id>", from_s: <seconds, 0 or more> \}/, "a card is not a shot");
  assert.match(messagesOf((doc) => { doc.scenes[3].data.source = { shot: "bird", from_s: 1 }; }), /an earlier shot id/, "not itself");
  assert.match(messagesOf((doc) => { doc.scenes[3].data.source.from_s = -1; }), /from_s: <seconds, 0 or more>/);
  assert.match(messagesOf((doc) => { doc.scenes[3].data.source.from_s = "1"; }), /from_s: <seconds, 0 or more>/);
  assert.match(messagesOf((doc) => { doc.scenes[2].data.visual = "still"; }), /sea-storm must be a clip shot with a clip of its own \(not a still, not itself cut from another shot\)/);
  assert.match(messagesOf((doc) => { doc.scenes[2].data.source = { shot: "opening", from_s: 0 }; }), /sea-storm must be a clip shot with a clip of its own/, "no chains");
  assert.match(messagesOf((doc) => { doc.scenes[3].data.visual = "still"; }), /a still has no clip to cut from/);
  assert.match(messagesOf((doc) => { doc.scenes[3].data.start_frame = { shot: "sea-storm", at: "last" }; }), /has no start_frame: that clip is already made/);
  assert.match(messagesOf((doc) => { doc.scenes[3].data.end_frame = { prompt: "the bird gone" }; }), /has no end_frame: that clip is already made/);
  assert.match(messagesOf((doc) => { doc.thumbnail.data.shot = "bird"; }), /thumbnail\.data\.shot: .*a shot cut from another shot's clip has none/);
  // Only a drama cuts from a clip: an illustration is its own picture.
  const slides = illustratedFixture();
  const pictures = slides.scenes.filter((scene) => scene.template === "shot");
  pictures[1].data.source = { shot: pictures[0].id, from_s: 0 };
  assert.match(validateVideo(slides).map((error) => error.message).join("\n"), /only a drama's shot is cut from another shot's clip/);
  // A cut returns to a setup on purpose, so its prompt may repeat the setup's.
  const twin = structuredClone(base);
  twin.scenes[3].data.prompt = twin.scenes[2].data.prompt;
  assert.ok(!shotProblems(twin, estimateTimeline(twin)).warnings.some((warning) => /nearly the same/.test(warning.message)));
  assert.deepEqual(sourcedShotScenes(base).map((scene) => scene.id), ["bird"]);
  assert.deepEqual(drawnShotScenes(base).map((scene) => scene.id), ["opening", "farewell", "sea-storm"]);
  assert.equal(isSourced(base.scenes[2]), false);
});

test("the narration's performance plan is the document voice's alone, within the style's room, and voiceFor reads it ahead of the line's cue (docs/videos/ILLUSTRATED.md §聲音表演)", () => {
  const plan = "開場壓低放慢；每個數字前停半拍；「其實」之後亮起來";
  const doc = illustratedFixture();
  doc.voice.performance = plan;
  assert.deepEqual(validateVideo(doc), []);
  // Accepted on an Azure voice too (lint warns that it is ignored); refused when it is not a plan.
  const azure = fixture();
  azure.voice.performance = plan;
  assert.deepEqual(validateVideo(azure), []);
  for (const bad of ["", "   ", 42, null, "字".repeat(201)]) {
    const wrong = illustratedFixture();
    wrong.voice.performance = bad;
    const errors = validateVideo(wrong);
    assert.deepEqual(paths(errors), ["voice.performance"], JSON.stringify(bad).slice(0, 12));
    assert.match(errors[0].message, /^must be the narration's performance plan .* at most 200 characters$/);
  }
  // The plan and the style share the server's 400 characters.
  const crowded = illustratedFixture();
  crowded.voice.style = "字".repeat(300);
  crowded.voice.performance = "字".repeat(100);
  assert.deepEqual(validateVideo(crowded).map((error) => `${error.path}: ${error.message}`), ["voice.performance: with voice.style it runs past the 400 characters a style may hold; shorten one of them"]);
  crowded.voice.performance = "字".repeat(99);
  assert.deepEqual(validateVideo(crowded), []);
  // A character's voice has its own style and no plan.
  const cast = dramaFixture();
  cast.characters[0].voice.performance = plan;
  assert.deepEqual(paths(validateVideo(cast)), ["characters[0].voice.performance"]);
  // voiceFor: the narrator's lines read the plan after the style and before the cue, a
  // character's line reads neither, and the plan is never a field of the voice sent out.
  const drama = dramaFixture();
  drama.voice.performance = plan;
  const narrator = drama.scenes[0].lines[0];
  assert.deepEqual(voiceFor(drama, narrator), { provider: "gemini", name: "Sulafat", style: `${dramaFixture().voice.style}。${plan}` });
  narrator.emotion = "壓低";
  assert.equal(voiceFor(drama, narrator).style, `${dramaFixture().voice.style}。${plan}。壓低`);
  assert.equal(voiceFor(drama, drama.scenes[1].lines[0]).style, "清亮、倔強的少女聲，台灣國語。開心、有點急");
  assert.equal("performance" in voiceFor(drama, narrator), false);
  assert.equal("performance" in voiceFor(drama, drama.scenes[1].lines[0]), false);
  // An Azure voice takes neither: the plan and the cue leave with it.
  azure.scenes[0].lines[0].emotion = "放慢";
  assert.deepEqual(voiceFor(azure, azure.scenes[0].lines[0]), { provider: "azure", name: "zh-TW-HsiaoChenNeural", rate: "+0%" });
  // A slides line's cue reaches a Gemini style on its own, without a plan.
  const slides = illustratedFixture();
  slides.scenes[1].lines[0].emotion = "放慢，一字一字";
  assert.equal(voiceFor(slides, slides.scenes[1].lines[0]).style, `${slides.voice.style}。放慢，一字一字`);
  assert.equal(voiceFor(slides, slides.scenes[0].lines[0]).style, slides.voice.style);
});

test("a script with no plan and no cue keeps the speech hash it had before the performance contract: the fixtures' hashes are pinned, and a plan or a cue moves them", () => {
  const lexicon = fixtureLexicon();
  // Recorded on 2026-10-05, before voice.performance and slides cues existed, so a timeline from
  // before them stays current and no narration is recorded again for the contract alone. A
  // fixture's narration or voice changing moves its hash on purpose: recompute it with
  // speechHash(<fixture>(), fixtureLexicon()) and pin the new value here.
  for (const [doc, pinned] of [
    [fixture(), "af5d5f5eb75aaa69"],
    [illustratedFixture(), "24b8bd53672b91e8"],
    [dramaFixture(), "3701f1baabd22734"],
    [explainerFixture(), "9fea1c4d8c68e0dc"],
    [storyFixture(), "1a23e4d697759dd1"],
    [enFixture(), "01f2da6b69601188"],
  ]) {
    assert.equal(speechHash(doc, lexicon), pinned, doc.slug);
  }
  const plan = illustratedFixture();
  plan.voice.performance = "開場壓低";
  assert.notEqual(speechHash(plan, lexicon), "24b8bd53672b91e8", "a plan records the narration again");
  const cue = fixture();
  cue.scenes[0].lines[1].emotion = "放慢";
  assert.notEqual(speechHash(cue, lexicon), "af5d5f5eb75aaa69", "a cue on a slides line is another take");
  const narrated = dramaFixture();
  narrated.voice.performance = "壓低";
  assert.notEqual(speechHash(narrated, lexicon), "3701f1baabd22734");
});

test("lint holds the lines to the performance contract: a plan or a cue puts a script in it, then a third of the reachable lines carry a cue or lint warns; an Azure voice gets the ignored warnings instead", () => {
  const coverage = (result) => result.warnings.filter((warning) => /performance cue/.test(warning.message)).map((warning) => `${warning.path}: ${warning.message}`);
  const flatMessage = (carrying, lines) => `scenes: ${carrying} of ${lines} lines carry a performance cue ("emotion"); at least a third should say where the voice slows, lifts or pauses, or the plan is read flat (docs/videos/ILLUSTRATED.md §聲音表演)`;
  const illustrated = (change) => {
    const doc = illustratedFixture();
    change?.(doc);
    return lintVideo(doc, { lexicon: fixtureLexicon(), brief: illustratedBrief(), others: [], translations: {} });
  };
  const cueLines = (doc, count) => {
    let left = count;
    for (const scene of doc.scenes) for (const line of scene.lines) if (left-- > 0) line.emotion = "放慢";
  };
  // Nothing of the contract: the example lints clean, as before it.
  assert.deepEqual(illustrated().warnings, []);
  // A plan with no cue: the voice would read it flat (a warning; the plan itself is valid).
  const flat = illustrated((doc) => { doc.voice.performance = "開場壓低放慢；數字前停半拍"; });
  assert.ok(!flat.errors.some((error) => error.path.startsWith("voice")), JSON.stringify(flat.errors));
  assert.deepEqual(coverage(flat), [flatMessage(0, 11)]);
  // A lone cue puts the script in the contract too.
  assert.deepEqual(coverage(illustrated((doc) => { doc.scenes[1].lines[0].emotion = "放慢"; })), [flatMessage(1, 11)]);
  // Three of eleven is under a third; four is enough, and then the plan has its cues.
  assert.deepEqual(coverage(illustrated((doc) => { doc.voice.performance = "開場壓低"; cueLines(doc, 3); })), [flatMessage(3, 11)]);
  assert.deepEqual(illustrated((doc) => { doc.voice.performance = "開場壓低"; cueLines(doc, 4); }).warnings, []);
  // An Azure narration: the plan and the cue are warned as ignored, and no line can be reached,
  // so coverage says nothing.
  const azure = fixture();
  azure.voice.performance = "開場壓低";
  azure.scenes[0].lines[0].emotion = "放慢";
  assert.deepEqual(lintVideo(azure, context({ brief: fixtureBrief() })).warnings.map((warning) => `${warning.path}: ${warning.message}`), [
    "voice.performance: the performance plan is ignored: the azure voice has no style prompt",
    'scenes[0].lines[0] (k7p2): emotion "放慢" is ignored: the azure voice has no style prompt',
  ]);
  // A drama with a cast is held on its characters' lines (the narrator bridges): the example's
  // three all carry a cue, so a plan on its narrator adds no warning; without them it does.
  const drama = dramaFixture();
  drama.voice.performance = "沉著地說，慢";
  assert.deepEqual(lintVideo(drama, context()).warnings.filter((warning) => !/^craft /.test(warning.message)), []);
  for (const scene of drama.scenes) for (const line of scene.lines) delete line.emotion;
  assert.deepEqual(coverage(lintVideo(drama, context())), [flatMessage(0, 3)]);
});
