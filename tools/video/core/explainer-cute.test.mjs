// The cute explainer looks on the script's side: their cards, their thumbnail, their brief and
// the picture-variety rules; and first what flat-explainer had before them, which does not move.
import assert from "node:assert/strict";
import test from "node:test";

import { EXPLAINER_CARD_TEMPLATES, pictureVarietyProblems } from "./drama.mjs";
import { explainerFixture } from "./fixtures/load.mjs";
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
