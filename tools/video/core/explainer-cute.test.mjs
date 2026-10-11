// The cute explainer looks on the script's side: their cards, their thumbnail, their brief and
// the picture-variety rules; and first what flat-explainer had before them, which does not move.
import assert from "node:assert/strict";
import test from "node:test";

import { episodeBrief } from "../automation/series.mjs";
import { renderProblems, thumbnailSeries } from "../render/plan.mjs";
import { thumbnailHtml } from "../templates/templates.mjs";
import { CUTE_EXPLAINER_CARD_TEMPLATES, CUTE_EXPLAINER_PRESETS, EXPLAINER_CARD_TEMPLATES, explainerCardTemplates, isCuteExplainer, pictureVarietyProblems } from "./drama.mjs";
import { explainerFixture } from "./fixtures/load.mjs";
import { checkBrief, lintVideo, thumbnailHeadlineProblems } from "./lint.mjs";
import { validateVideo } from "./schema.mjs";

const base = explainerFixture();
const steps = { id: "how", template: "steps", data: { title: "steps", steps: [{ title: "one", detail: "a" }, { title: "two", detail: "b" }], source: "TIME 1991-09-23" }, lines: [{ id: "s1ex", text: "一個人站在圓心。", reveal: 1 }, { id: "s2ex", text: "另一個人拿木板。", reveal: 1 }] };
const table = { id: "names", template: "table", data: { title: "names", columns: ["a", "b"], rows: [["1", "2"], ["3", "4"]] }, lines: [{ id: "t1ex", text: "第一個名字是地圖編號。", reveal: 1 }, { id: "t2ex", text: "第二個是無線電呼號。", reveal: 1 }] };
/** The explainer fixture in `preset`, with a steps and a table card after its fourth scene. */
const withCards = (preset) => ({ ...base, look: { preset }, subtitles: { burn_in: false }, scenes: [...base.scenes.slice(0, 4), steps, table, ...base.scenes.slice(4)] });
const shot = (id, camera, prompt = "Medium shot of a farm gate at dawn, a farmer in a waxed coat lifting the latch, low sun from the left") => ({ id, template: "shot", data: { prompt, camera, visual: "still" }, lines: [{ id: `${id}0x`.slice(0, 4), text: "農夫走到田邊。" }] });
/** The variety problems of a video in `preset` whose shots move as `cameras` say. */
const variety = (preset, cameras, prompt) => pictureVarietyProblems({ ...base, look: { preset }, scenes: cameras.map((camera, index) => shot(`p${index}`, camera, prompt)) });

test("flat-explainer keeps its six cards, and the picture-variety rules still leave it alone", () => {
  assert.deepEqual(EXPLAINER_CARD_TEMPLATES, ["title", "chapter", "outro", "big", "stats", "compare"]);
  const sixCards = 'a drama scene is a "shot" or one of the cards title, chapter, outro, big, stats, compare';
  assert.deepEqual(validateVideo(withCards("flat-explainer")).map((error) => error.message), [sixCards, sixCards]);
  assert.deepEqual(variety("flat-explainer", ["push in", "push in", "push in"]), { errors: [], warnings: [] });
  assert.deepEqual(variety("flat-explainer", ["push in", "pull out"], "Medium shot of a chibi farmer at a gate at dawn, low sun from the left"), { errors: [], warnings: [] });
});

test("the cute presets may also use steps and table cards, and no card beyond those eight", () => {
  assert.deepEqual([...CUTE_EXPLAINER_PRESETS], ["cute-cartoon", "cute-mystery"]);
  assert.deepEqual(CUTE_EXPLAINER_CARD_TEMPLATES, ["title", "chapter", "outro", "big", "stats", "compare", "steps", "table"]);
  assert.equal(explainerCardTemplates("flat-explainer"), EXPLAINER_CARD_TEMPLATES);
  assert.equal(explainerCardTemplates("ink-wash"), EXPLAINER_CARD_TEMPLATES, "a name that is no cute preset gets the explainer's six");
  for (const preset of CUTE_EXPLAINER_PRESETS) {
    assert.equal(explainerCardTemplates(preset), CUTE_EXPLAINER_CARD_TEMPLATES);
    const doc = withCards(preset);
    assert.equal(isCuteExplainer(doc), true, preset);
    assert.deepEqual(validateVideo(preset === "cute-mystery" ? { ...doc, thumbnail: CHANNEL_THUMBNAIL } : doc), [], preset);
    const quote = { id: "said", template: "quote", data: { quote: "q", source: "s" }, lines: [{ id: "q0ex", text: "他說了一句話。" }] };
    assert.match(validateVideo({ ...doc, scenes: [...doc.scenes.slice(0, 4), quote, ...doc.scenes.slice(4)] })[0].message, /one of the cards title, chapter, outro, big, stats, compare, steps, table$/, preset);
  }
  for (const other of [withCards("flat-explainer"), { ...base, format: "slides", look: { preset: "cute-mystery" } }, { ...base, look: undefined }, undefined]) assert.equal(isCuteExplainer(other), false);
});

// 奇聞檔案局 wears the channel's thumbnail (owner's decision 1): a tag and a sub, no pillar, no layout.
const CHANNEL_THUMBNAIL = { template: "thumb", data: { headline: "光？\n**先到**", tag: "奇異現象", sub: "數三秒的檔案", shot: "flash" } };

test("a cute-mystery script wears the channel's thumbnail: valid as the writer is told to write it, and So That's Why's fields are refused", () => {
  const mystery = { ...withCards("cute-mystery"), thumbnail: CHANNEL_THUMBNAIL, youtube: { ...base.youtube, title: "為什麼雷聲總比閃電晚到？｜奇聞檔案局" } };
  assert.deepEqual(validateVideo(mystery), []);
  assert.equal(thumbnailSeries(mystery), null);
  assert.deepEqual(renderProblems(mystery), []);
  assert.deepEqual(thumbnailHeadlineProblems(mystery), []);
  const html = thumbnailHtml(mystery.thumbnail, { series: thumbnailSeries(mystery), slug: mystery.slug });
  assert.equal(html.includes("原來如此事務所") || html.includes("thumb-stamp") || /pillar-/.test(html), false, "nothing of So That's Why's thumbnail is drawn");
  const withData = (extra) => ({ ...mystery, thumbnail: { ...mystery.thumbnail, data: { ...mystery.thumbnail.data, ...extra } } });
  assert.match(renderProblems(withData({ pillar: "H" }))[0].message, /pillar must be one of business/);
  assert.match(renderProblems(withData({ layout: "right" }))[0].message, /layout must be one of a, b, c/);
  // cute-cartoon is So That's Why redrawn and keeps that series' thumbnail.
  assert.equal(thumbnailSeries(withCards("cute-cartoon")), "sothatswhy");
  assert.deepEqual(renderProblems(withCards("cute-cartoon")), []);
});

test("a 奇聞檔案局 brief with the labelled 原因 lines has the explainer's sections, and its script lints without an error of this format", () => {
  const series = { slug: "one-off-1", kind: "one-off", title: "t", premise: "p", style_preset: "cute-mystery", target_minutes: 10, genre: "xianxia-bonds" };
  const brief = episodeBrief(series, { number: 1, title: "t", logline: "l" }, [], { question: "q", answer: "a", hook: "h", reasons: ["流傳的版本：x", "紀錄：y", "紀錄：z", "目前最站得住的解釋：w"], closing: "存檔。", sources: ["https://example.org/"] });
  assert.deepEqual(checkBrief(brief, "drama", "cute-mystery"), []);
  assert.match(brief, /## 原因\n- 流傳的版本：x\n- 紀錄：y\n- 紀錄：z\n- 目前最站得住的解釋：w\n/);
  const mystery = { ...withCards("cute-mystery"), thumbnail: CHANNEL_THUMBNAIL };
  const linted = lintVideo(mystery, { brief, lexicon: { schema_version: 1, terms: {} }, minEpisodeMinutes: 0 });
  assert.deepEqual(linted.errors.filter((error) => /card|template|thumbnail|look|characters/.test(`${error.path} ${error.message}`)), []);
});

test("the picture-variety rules hold a cute explainer's stills as they hold illustrated slides", () => {
  for (const preset of CUTE_EXPLAINER_PRESETS) {
    const same = variety(preset, ["push in", "push in", "push in"]);
    assert.equal(same.errors.length, 1, preset);
    assert.match(same.errors[0].message, /3 stills in a row under "push in"/);
    assert.equal(variety(preset, ["push in", "pull out", "push in"]).errors.length, 0, preset);
    // The look's own words in a prompt pin every picture to one finish: the cute looks' as well as the print looks'.
    for (const word of ["chibi", "cartoon", "flat colours", "thick dark outlines", "cel-shaded"]) {
      const restated = variety(preset, ["push in", "pull out"], `Medium shot of a ${word} farmer at a gate at dawn, low sun from the left`).warnings.map((warning) => warning.message).join(" | ");
      assert.ok(restated.includes(`restate the look ("${word}")`), `${preset}: ${word}: ${restated}`);
    }
    // Palette words are also things, so they are not counted: a navy officer is a person.
    assert.doesNotMatch(variety(preset, ["push in", "pull out"], "Medium shot of a navy officer at a harbour gate at dawn, low sun from the left").warnings.map((warning) => warning.message).join(" | "), /restate the look/, preset);
  }
});
