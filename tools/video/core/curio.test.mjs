import assert from "node:assert/strict";
import test from "node:test";

import { CURIO_MAX_CARD_RUN, CURIO_MIN_SHOT_SHARE, CURIO_MUSIC, CURIO_PRESET, curioProblems, curioWarnings, GENERIC_PROP_MAX, genericPropWarnings, heimaoSubjectWarnings, isCurio, isPacedSeries, pacingWarnings, SERIES_PACING } from "./curio.mjs";
import { resolveLook } from "./drama.mjs";
import { fixture, fixtureBrief, fixtureLexicon } from "./fixtures/load.mjs";
import { lintVideo } from "./lint.mjs";

const shot = (id, prompt = "Medium shot of a sailor holding a lantern in a wet cabin at night") => ({ id, template: "shot", data: { prompt } });
const card = (id) => ({ id, template: "big", data: { headline: "1872" } });
// An episode drawn the way the delivered ones are: mostly illustrations, a card now and then.
const episode = (scenes, look = { preset: CURIO_PRESET }) => ({ slug: "curio-x01", look, scenes });
const paths = (problems) => problems.map((problem) => problem.path);

test("only a curio- slug is an episode of the series", () => {
  assert.equal(isCurio({ slug: "curio-h04-v2" }), true);
  assert.equal(isCurio({ slug: "sothatswhy-t26" }), false);
  assert.deepEqual(curioProblems({ slug: "ai-term-token", scenes: [card("a"), card("b"), card("c"), card("d"), card("e")] }), []);
});

test("an episode in the series look with illustrations between short card runs passes", () => {
  const scenes = [shot("s1"), card("c1"), shot("s2"), shot("s3"), card("c2"), card("c3"), card("c4"), shot("s4"), shot("s5"), shot("s6"), shot("s7"), shot("s8"), shot("s9"), shot("s10"), shot("s11"), { id: "end", template: "outro", data: {} }];
  assert.deepEqual(curioProblems(episode(scenes)), []);
});

test("the series look is the preset word for word, the way the first three episodes wrote it out", () => {
  const scenes = [shot("s1"), shot("s2")];
  const written = { preset: "custom", style: resolveLook({ preset: CURIO_PRESET }).style, negative: "" };
  assert.deepEqual(curioProblems(episode(scenes, written)), []);
  assert.deepEqual(paths(curioProblems(episode(scenes, null))), ["look"]);
  const added = { preset: CURIO_PRESET, style: `${resolveLook({ preset: CURIO_PRESET }).style}, historical gear uses period materials` };
  assert.deepEqual(paths(curioProblems(episode(scenes, added))), ["look.style"]);
  assert.deepEqual(paths(curioProblems(episode(scenes, { preset: CURIO_PRESET, negative: "photorealistic" }))), ["look.negative"]);
});

test("a body under the illustration share, or a long run of cards, is refused", () => {
  const few = [shot("s1"), card("c1"), shot("s2"), card("c2"), card("c3")];
  const share = curioProblems(episode(few));
  assert.ok(share.some((problem) => problem.path === "scenes" && /2 of 5 body scenes/.test(problem.message)), JSON.stringify(share));
  assert.ok(CURIO_MIN_SHOT_SHARE > 0.4);

  const run = Array.from({ length: CURIO_MAX_CARD_RUN + 1 }, (_, i) => card(`c${i}`));
  const scenes = [...Array.from({ length: 12 }, (_, i) => shot(`s${i}`)), ...run, shot("last")];
  const runs = curioProblems(episode(scenes));
  assert.equal(runs.length, 1);
  assert.match(runs[0].message, new RegExp(`${CURIO_MAX_CARD_RUN + 1} cards in a row \\(c0 … c${CURIO_MAX_CARD_RUN}\\)`));
});

test("lint reports the series problems as errors on a curio- slug and not on any other", () => {
  const context = { lexicon: fixtureLexicon(), brief: fixtureBrief(), others: [], translations: {} };
  const other = lintVideo(fixture(), context);
  assert.ok(!other.errors.some((problem) => problem.path === "look"), JSON.stringify(other.errors));
  const curio = lintVideo({ ...fixture(), slug: "curio-x01" }, context);
  assert.ok(curio.errors.some((problem) => problem.path === "look" && /cute-mystery/.test(problem.message)), JSON.stringify(curio.errors));
});

test("a curio- slug without a music bed is warned, with the series' track to add; any other video is not", () => {
  assert.deepEqual(curioWarnings({ slug: "sothatswhy-t26" }), []);
  assert.deepEqual(curioWarnings({ slug: "curio-x01", music: { track: "own.mp3" } }), []);
  const [warning] = curioWarnings({ slug: "curio-x01" });
  assert.equal(warning.path, "music");
  assert.ok(warning.message.includes(JSON.stringify(CURIO_MUSIC)), warning.message);
  assert.deepEqual(curioWarnings({ slug: "curio-x01", music: { track: "own.mp3" }, subtitles: { burn_in: true } }).map((problem) => problem.path), ["subtitles.burn_in"]);
  assert.deepEqual(curioWarnings({ slug: "curio-x01", music: { track: "own.mp3" }, subtitles: { burn_in: false } }), []);
  const context = { lexicon: fixtureLexicon(), brief: fixtureBrief(), others: [], translations: {} };
  assert.ok(lintVideo({ ...fixture(), slug: "curio-x01" }, context).warnings.some((problem) => problem.path === "music"));
  assert.ok(!lintVideo(fixture(), context).warnings.some((problem) => problem.path === "music"));
});

test("a curio- or sothatswhy- drama without the series pacing is warned, with the fields to add; anything else is not", () => {
  assert.equal(isPacedSeries({ slug: "curio-h24" }), true);
  assert.equal(isPacedSeries({ slug: "sothatswhy-p05-down-jacket" }), true);
  assert.equal(isPacedSeries({ slug: "daily-ai-20261029" }), false);
  const missing = pacingWarnings({ slug: "curio-h24", format: "drama" });
  assert.deepEqual(paths(missing), ["pauses", "still_motion"]);
  assert.ok(missing[0].message.includes(JSON.stringify(SERIES_PACING.pauses)), missing[0].message);
  assert.deepEqual(paths(pacingWarnings({ slug: "sothatswhy-p05-down-jacket", format: "drama", pauses: { line_ms: 0 } })), ["still_motion"]);
  assert.deepEqual(pacingWarnings({ slug: "curio-h24", format: "drama", ...SERIES_PACING }), []);
  assert.deepEqual(pacingWarnings({ slug: "curio-h01", format: "slides" }), [], "the old slides pilots move their pictures another way");
  assert.deepEqual(pacingWarnings({ slug: "daily-ai-20261029", format: "drama" }), []);
  const context = { lexicon: fixtureLexicon(), brief: fixtureBrief(), others: [], translations: {} };
  assert.ok(!lintVideo(fixture(), context).warnings.some((problem) => problem.path === "still_motion"));
});

test("repeating generic purse/wallet or plain-covered book stand-ins across 3+ shots warns on curio-, sothatswhy- and story- dramas", () => {
  assert.equal(GENERIC_PROP_MAX, 2);
  const purses = [
    shot("p1", "Close-up of a fat leather purse bursting with gold coins on a sunny oak table"),
    shot("p2", "Close-up of a flat leather wallet lying empty beside a brass key"),
    shot("p3", "Medium shot of a merchant clutching a heavy purse in a bright courtyard"),
  ];
  const books = [
    shot("b1", "Close-up of a thick book with a plain cover resting on a wooden desk"),
    shot("b2", "Close-up of a plain-covered book beside a brass compass"),
    shot("b3", "Medium shot of a clerk closing a thick plain-covered book in daylight"),
  ];
  assert.deepEqual(genericPropWarnings({ slug: "curio-w01", format: "drama", scenes: purses.slice(0, 2) }), [], "at most two generic stand-ins is fine");
  for (const slug of ["curio-w02", "sothatswhy-g12", "story-everyday-crocs-c01"]) {
    const [purseWarn] = genericPropWarnings({ slug, format: "drama", scenes: purses });
    assert.match(purseWarn.message, /3 shots draw the generic purse\/wallet \(錢包／皮夾\) stand-in \(p1, p2, p3\)/, slug);
    const [bookWarn] = pacingWarnings({ slug, format: "drama", ...SERIES_PACING, scenes: books });
    assert.match(bookWarn.message, /3 shots draw the generic thick\/plain-covered book \(空白厚書\) stand-in \(b1, b2, b3\)/, slug);
  }
  assert.deepEqual(genericPropWarnings({ slug: "daily-ai-20261118", format: "drama", scenes: purses }), [], "other formats are untouched");
});

test("heimao thumbnails warn when line 1 hides the subject behind a nameless demonstrative or pronoun", () => {
  const thumb = (headline, layout = "heimao-left") => ({ template: "thumb", data: { layout, headline, sub: "3 份紀錄" } });
  for (const [slug, bad] of [
    ["curio-s10-v2", "這句話**根本沒寫？**"],
    ["curio-s13-v2", "這兩字**沒簽過？**"],
    ["sothatswhy-p12-qr-code", "它髒了**照樣能掃？**"],
    ["story-dolby", "他**憑什麼躺賺？**"],
  ]) {
    const [warn] = pacingWarnings({ slug, format: "drama", ...SERIES_PACING, thumbnail: thumb(bad) });
    assert.equal(warn.path, "thumbnail.data.headline", slug);
    assert.match(warn.message, /nameless demonstrative\/pronoun/, slug);
  }
  for (const good of ["本能寺**誰喊的？**", "真田幸村**叫錯了？**", "QR 髒了**照樣能掃？**", "杜比**憑什麼躺賺？**", "宮本武藏**沒遲到？**"]) {
    assert.deepEqual(heimaoSubjectWarnings({ slug: "curio-s14", format: "drama", thumbnail: thumb(good) }), [], good);
  }
  assert.deepEqual(heimaoSubjectWarnings({ slug: "daily-ai-20261120", format: "drama", thumbnail: thumb("這句話**根本沒寫？**") }), [], "other series are untouched");
});
