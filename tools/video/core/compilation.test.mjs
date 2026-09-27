import assert from "node:assert/strict";
import test from "node:test";

import { toSrt } from "./captions.mjs";
import {
  CARD_FRAMES,
  chapterList,
  chapterTitle,
  COMPILATION_STEPS,
  COMPILATION_TITLE_PLACEHOLDER,
  compilationChecksCurrent,
  compilationDocument,
  compilationHash,
  compilationLayout,
  compilationTimeline,
  descriptionWithinBudget,
  episodeLabel,
  estimatedCompilationTimeline,
  isCompilation,
  lintCompilation,
  mergeCaptions,
  OUTRO_FRAMES,
  PLACEHOLDER_TITLE,
  shiftCues,
  totalFrames,
} from "./compilation.mjs";
import { DESCRIPTION_MAX_BYTES } from "./metadata.mjs";
import { LINE_ID, validateVideo } from "./schema.mjs";
import { chapterText, checkChapters, visualHash } from "./timeline.mjs";

const VOICE = { provider: "gemini", name: "Sulafat", style: "沉穩的說書人語氣" };
const EPISODES = [
  { slug: "wuxia-ep-1", number: 1, title: "初入山門" },
  { slug: "wuxia-ep-2", number: 2, title: "夜探藏經閣" },
  { slug: "wuxia-ep-3", number: 3, title: "劍冢之約" },
];
const build = (overrides = {}) => compilationDocument({ series: "wuxia", episodes: EPISODES, voice: VOICE, ...overrides });
const cuts = (doc, frames = 3600) => doc.compilation.episodes.map((slug, index) => ({ slug, frames: frames + index, sha256: `${index}`.repeat(64), file: `/work/${slug}/final.mp4` }));
const paths = (errors) => errors.map((error) => error.path);

test("the builder makes a document that passes validation and lint, with deterministic card and line ids", () => {
  const doc = build();
  assert.equal(doc.slug, "wuxia-full");
  assert.equal(doc.format, "drama");
  assert.ok(isCompilation(doc));
  assert.deepEqual(doc.compilation, { series: "wuxia", episodes: ["wuxia-ep-1", "wuxia-ep-2", "wuxia-ep-3"], chapter_cards: true, outro: true, titles: { "wuxia-ep-1": "初入山門", "wuxia-ep-2": "夜探藏經閣", "wuxia-ep-3": "劍冢之約" } });
  assert.deepEqual(doc.youtube, { category_id: 24, made_for_kids: false, default_language: "zh-TW", title: PLACEHOLDER_TITLE, description: "（合集說明待企劃）", tags: [], video_id: null });
  assert.equal(COMPILATION_TITLE_PLACEHOLDER, "（合集標題待企劃）");
  assert.deepEqual(doc.thumbnail, { template: "thumb", data: { headline: "（待企劃）", shot: "thumb" } });
  assert.deepEqual(doc.scenes.map((scene) => [scene.id, scene.template, scene.chapter ?? null, scene.data.title, scene.lines.map((line) => line.id)]), [
    ["card-1", "chapter", "第 1 集 初入山門", "初入山門", ["c001"]],
    ["card-2", "chapter", "第 2 集 夜探藏經閣", "夜探藏經閣", ["c002"]],
    ["card-3", "chapter", "第 3 集 劍冢之約", "劍冢之約", ["c003"]],
    ["outro", "outro", null, "全集完", ["outro"]],
  ]);
  for (const scene of doc.scenes) for (const line of scene.lines) assert.match(line.id, LINE_ID);
  assert.deepEqual(validateVideo(doc), []);
  assert.deepEqual(build(), doc, "a rebuild gives the same document");
  const lint = lintCompilation(doc, {});
  assert.deepEqual(lint.errors, []);
  assert.deepEqual(lint.warnings.map((warning) => warning.path), ["youtube.title"]);
  assert.equal(lint.summary, null);
  assert.deepEqual(COMPILATION_STEPS, ["metadata planned", "cards rendered", "video compiled", "metadata translated", "final video approved", "upload package", "on YouTube"]);
});

test("a chapter's compilation numbers its cards by the series' episode numbers, and a compilation without cards or an outro has no scenes", () => {
  const later = build({ slug: "wuxia-chapter-2", episodes: [{ slug: "wuxia-ep-11", number: 11, title: "重返" }, { slug: "wuxia-ep-12", number: 12 }] });
  assert.deepEqual(later.compilation.numbers, { "wuxia-ep-11": 11, "wuxia-ep-12": 12 });
  assert.deepEqual(later.compilation.titles, { "wuxia-ep-11": "重返" });
  assert.deepEqual(later.scenes.map((scene) => [scene.id, scene.chapter ?? null, scene.lines[0].id]), [["card-11", "第 11 集 重返", "c011"], ["card-12", "第 12 集", "c012"], ["outro", null, "outro"]]);
  assert.deepEqual(validateVideo(later), []);
  const bare = build({ chapterCards: false, outro: false });
  assert.deepEqual(bare.scenes, []);
  assert.deepEqual(validateVideo(bare), []);
  assert.equal(bare.voice, VOICE);
  const voiceless = compilationDocument({ series: "wuxia", episodes: EPISODES });
  assert.equal("voice" in voiceless, false);
  assert.deepEqual(validateVideo(voiceless), [], "nothing is narrated, so a voice is optional");
});

test("validation refuses what an episode has and pins the scenes to the block", () => {
  const cast = build();
  cast.characters = [];
  cast.look = { preset: "cinematic-3d" };
  cast.music = { prompt: "guqin" };
  cast.series = { slug: "wuxia", episode: 1, chapter: 1 };
  cast.subtitles = { burn_in: true };
  assert.deepEqual(paths(validateVideo(cast)).sort(), ["characters", "look", "music", "series", "subtitles"]);

  const block = build();
  block.compilation.series = "Bad Slug";
  block.compilation.episodes = ["wuxia-ep-1", "wuxia-ep-1", "wuxia-full"];
  block.compilation.chapter_cards = "yes";
  block.compilation.titles = { "wuxia-ep-9": "x".repeat(41) };
  block.compilation.extra = 1;
  assert.deepEqual(paths(validateVideo(block)).sort(), ["compilation.chapter_cards", "compilation.episodes[1]", "compilation.episodes[2]", "compilation.extra", "compilation.series", "compilation.titles.wuxia-ep-9", "compilation.titles.wuxia-ep-9"].sort());

  const scenes = build();
  scenes.scenes[0].chapter = "開場";
  scenes.scenes[1].template = "shot";
  scenes.scenes[3].chapter = "結尾";
  scenes.scenes[2].lines[0].speaker = "narrator";
  scenes.scenes.push({ id: "extra", template: "title", data: { title: "x" }, lines: [{ id: "zzzz", text: "x" }] });
  assert.deepEqual(paths(validateVideo(scenes)).sort(), ["scenes", "scenes[0].chapter", "scenes[1].template", "scenes[2].lines[0].speaker", "scenes[3].chapter"].sort());

  const thumb = build();
  thumb.thumbnail.data.shot = "opening";
  thumb.format = "slides";
  assert.deepEqual(paths(validateVideo(thumb)).sort(), ["format", "thumbnail.data.shot"]);

  const numbers = build();
  numbers.compilation.numbers = { "wuxia-ep-1": 3, "wuxia-ep-2": 2, "wuxia-ep-3": 0 };
  assert.deepEqual(paths(validateVideo(numbers)).filter((path) => path.startsWith("compilation")).sort(), ["compilation.numbers", "compilation.numbers.wuxia-ep-3"]);

  const missing = build();
  delete missing.compilation.episodes;
  assert.ok(paths(validateVideo(missing)).includes("compilation.episodes"));
  assert.equal(isCompilation({ format: "drama" }), false);
});

test("the layout puts a card before each cut and the outro last, on the frame grid", () => {
  const doc = build();
  const layout = compilationLayout(doc, cuts(doc));
  assert.deepEqual(layout.map((entry) => [entry.kind, entry.id, entry.start_frame, entry.frames]), [
    ["card", "card-1", 0, CARD_FRAMES],
    ["episode", "wuxia-ep-1", 60, 3600],
    ["card", "card-2", 3660, CARD_FRAMES],
    ["episode", "wuxia-ep-2", 3720, 3601],
    ["card", "card-3", 7321, CARD_FRAMES],
    ["episode", "wuxia-ep-3", 7381, 3602],
    ["outro", "outro", 10983, OUTRO_FRAMES],
  ]);
  assert.equal(totalFrames(layout), 11103);
  assert.deepEqual(layout[1], { kind: "episode", id: "wuxia-ep-1", slug: "wuxia-ep-1", episode: 1, start_frame: 60, frames: 3600, file: "/work/wuxia-ep-1/final.mp4", sha256: "0".repeat(64) });
  const bare = build({ chapterCards: false, outro: false });
  assert.deepEqual(compilationLayout(bare, cuts(bare)).map((entry) => [entry.kind, entry.start_frame]), [["episode", 0], ["episode", 3600], ["episode", 7201]]);
  assert.throws(() => compilationLayout(doc, cuts(doc).reverse()), /not compilation\.episodes in order/);
  assert.throws(() => compilationLayout(doc, cuts(doc).map((cut) => ({ ...cut, frames: 0 }))), /no frame count/);
  assert.equal(totalFrames([]), 0);
});

test("the hash follows the cuts and the card switches, not the titles; checks are current for the same cuts and cards", () => {
  const doc = build();
  const episodes = cuts(doc);
  const hash = compilationHash(doc, episodes);
  assert.match(hash, /^[0-9a-f]{16}$/);
  assert.equal(compilationHash(structuredClone(doc), structuredClone(episodes)), hash);
  assert.notEqual(compilationHash(doc, episodes.map((cut, index) => (index === 1 ? { ...cut, sha256: "f".repeat(64) } : cut))), hash);
  assert.notEqual(compilationHash(build({ outro: false }), episodes), hash);
  assert.notEqual(compilationHash(build({ chapterCards: false }), episodes), hash);
  const retitled = build({ episodes: EPISODES.map((episode) => ({ ...episode, title: `${episode.title}！` })) });
  assert.equal(compilationHash(retitled, episodes), hash, "a title changes the cards' pictures, which the visual hash covers");
  const checks = { ok: true, compilation_hash: hash, visual_hash: visualHash(doc) };
  assert.equal(compilationChecksCurrent(doc, checks, episodes), true);
  assert.equal(compilationChecksCurrent(retitled, checks, episodes), false);
  assert.equal(compilationChecksCurrent(doc, { ...checks, ok: false }, episodes), false);
  assert.equal(compilationChecksCurrent(doc, checks, episodes.map((cut) => ({ ...cut, sha256: null }))), false);
  assert.equal(compilationChecksCurrent(doc, null, episodes), false);
});

test("chapters start at the cards, key on the episode slug, and read like the timeline's", () => {
  const doc = build();
  const layout = compilationLayout(doc, cuts(doc));
  const chapters = chapterList(layout, doc.compilation.titles);
  assert.deepEqual(chapters.map((chapter) => [chapter.at, chapter.title, chapter.scene, chapter.card, chapter.episode]), [
    [0, "第 1 集 初入山門", "wuxia-ep-1", "card-1", 1],
    [122, "第 2 集 夜探藏經閣", "wuxia-ep-2", "card-2", 2],
    [244, "第 3 集 劍冢之約", "wuxia-ep-3", "card-3", 3],
  ]);
  assert.equal(chapters[1].start_frame, 3660);
  const timeline = compilationTimeline(layout, doc.compilation.titles);
  assert.deepEqual(Object.keys(timeline), ["fps", "sample_rate", "total_frames", "scenes", "lines", "chapters", "speech_hash"]);
  assert.equal(timeline.fps, 30);
  assert.equal(timeline.speech_hash, null);
  assert.deepEqual(timeline.chapters[0], { title: "第 1 集 初入山門", scene: "wuxia-ep-1", start_frame: 0, episode: 1 });
  assert.equal(chapterText(timeline), "00:00 第 1 集 初入山門\n02:02 第 2 集 夜探藏經閣\n04:04 第 3 集 劍冢之約");
  assert.equal(chapterText(timeline, { "wuxia-ep-2": "Episode 2: The Library" }).split("\n")[1], "02:02 Episode 2: The Library");
  assert.deepEqual(checkChapters(timeline), []);
  const bare = build({ chapterCards: false, outro: false });
  const bareChapters = chapterList(compilationLayout(bare, cuts(bare)), bare.compilation.titles);
  assert.deepEqual(bareChapters.map((chapter) => [chapter.at, chapter.title, chapter.card]), [[0, "第 1 集 初入山門", null], [120, "第 2 集 夜探藏經閣", null], [240, "第 3 集 劍冢之約", null]]);
  assert.equal(chapterTitle(7), "第 7 集");
  assert.equal(chapterTitle(7, "  題 "), "第 7 集 題");
  assert.equal(estimatedCompilationTimeline(doc).total_frames, 3 * 7200 + 3 * CARD_FRAMES + OUTRO_FRAMES);
});

test("cues shift by the episode's offset and merge in play order", () => {
  const cues = [{ start_ms: 0, end_ms: 1200, text: "一" }, { start_ms: 1500.4, end_ms: 2700, text: "二" }];
  assert.deepEqual(shiftCues(cues, 2000), [{ start_ms: 2000, end_ms: 3200, text: "一" }, { start_ms: 3500, end_ms: 4700, text: "二" }]);
  const first = toSrt([{ start_ms: 100, end_ms: 900, text: "第一集\n第二行" }]);
  const second = toSrt([{ start_ms: 0, end_ms: 1000, text: "第二集" }]);
  assert.deepEqual(mergeCaptions([{ srt: first, offsetMs: 2000 }, { srt: second, offsetMs: 122_000 }]), [
    { start_ms: 2100, end_ms: 2900, text: "第一集\n第二行" },
    { start_ms: 122_000, end_ms: 123_000, text: "第二集" },
  ]);
  assert.deepEqual(mergeCaptions([{ srt: "", offsetMs: 0 }]), []);
});

test("eighty titled chapters fall back to 「第 N 集」 so the description stays within 5,000 bytes", () => {
  const episodes = Array.from({ length: 80 }, (_, index) => ({ slug: `wuxia-ep-${index + 1}`, number: index + 1, title: "山海經最倔強的一隻鳥到底為什麼要填海呢這是第一部的長標題" }));
  const doc = build({ episodes });
  const layout = compilationLayout(doc, doc.compilation.episodes.map((slug) => ({ slug, frames: 7200, sha256: "a".repeat(64) })));
  const timeline = compilationTimeline(layout, doc.compilation.titles);
  const body = "第一部的每一集，接連著看。";
  const budget = descriptionWithinBudget(body, timeline, {}, { sources: [], tags: ["仙俠"] });
  assert.equal(budget.shortened, true);
  assert.ok(Buffer.byteLength(budget.description, "utf8") <= DESCRIPTION_MAX_BYTES, `${Buffer.byteLength(budget.description, "utf8")} bytes`);
  assert.match(budget.description, /\n00:00 第 1 集\n/);
  assert.match(budget.description, /\n5:1\d:\d\d 第 80 集\n/, "eighty four-minute episodes run past five hours");
  assert.equal(Object.keys(budget.titles).length, 80);
  assert.equal(budget.titles["wuxia-ep-80"], "第 80 集");
  const en = descriptionWithinBudget("Every episode of part one.", timeline, Object.fromEntries(episodes.map((episode) => [episode.slug, `Episode ${episode.number}: ${"a long English title that goes on and on".repeat(2)}`])), { locale: "en" });
  assert.equal(en.shortened, true);
  assert.equal(en.titles["wuxia-ep-3"], "Episode 3");
  // A skipped episode leaves a gap in the numbers: the fallback says the episode's number, as its card does, not its position.
  const gapped = build({ episodes: episodes.filter((episode) => episode.number !== 2) });
  const gappedLayout = compilationLayout(gapped, gapped.compilation.episodes.map((slug) => ({ slug, frames: 7200, sha256: "a".repeat(64) })));
  const gappedBudget = descriptionWithinBudget(body, compilationTimeline(gappedLayout, gapped.compilation.titles), {}, { sources: [], tags: ["仙俠"] });
  assert.equal(gappedBudget.shortened, true);
  assert.equal(gappedBudget.titles["wuxia-ep-3"], "第 3 集", "the second chapter is episode 3");
  assert.equal(gappedBudget.titles["wuxia-ep-80"], "第 80 集");
  assert.match(en.description, /Chapters\n00:00 Episode 1\n/);
  assert.equal(episodeLabel(4, "ja"), "第4話");
  assert.equal(episodeLabel(4, "ko"), "4화");
  // Three chapters fit with their titles and keep them.
  const short = build();
  const fits = descriptionWithinBudget(body, compilationTimeline(compilationLayout(short, cuts(short)), short.compilation.titles), {});
  assert.equal(fits.shortened, false);
  assert.match(fits.description, /00:00 第 1 集 初入山門/);
  // Lint on the eighty-episode document warns about the fallback and passes.
  const lint = lintCompilation({ ...doc, youtube: { ...doc.youtube, title: "仙門風雲 全集", description: body } }, {});
  assert.deepEqual(lint.errors, []);
  assert.ok(lint.warnings.some((warning) => warning.path === "youtube.description" && /第 N 集/.test(warning.message)));
});

test("lint reports the translations' state by field and by episode slug, and a title over YouTube's limit", () => {
  const doc = build();
  const en = { title: "Part one", description: "All of it.", tags: ["wuxia"], chapters: { "wuxia-ep-1": "Episode 1", "wuxia-ep-2": "Episode 2" }, lines: {} };
  const lint = lintCompilation(doc, { translations: { en, ja: { title: "", description: "d" } } });
  assert.deepEqual(lint.errors, []);
  const en1 = lint.warnings.filter((warning) => warning.path === "i18n/en.json").map((warning) => warning.message);
  assert.deepEqual(en1, ["1 chapters without a translated title (keyed by episode slug): wuxia-ep-3"]);
  const ja = lint.warnings.filter((warning) => warning.path === "i18n/ja.json").map((warning) => warning.message);
  assert.deepEqual(ja, ["not translated: title", "3 chapters without a translated title (keyed by episode slug): wuxia-ep-1, wuxia-ep-2, wuxia-ep-3"]);
  const long = { ...doc, youtube: { ...doc.youtube, title: "字".repeat(101) } };
  assert.match(lintCompilation(long, {}).errors[0].message, /youtube\.title: 101 characters/);
  const broken = lintCompilation({ ...doc, compilation: { ...doc.compilation, episodes: [] } }, {});
  assert.ok(broken.errors.length > 0);
});
