const path = require("node:path");
const ROOT = path.resolve(__dirname, "../../../..");
// Why 妳/你 reached Jev at all: the narration check's same-sound rule (tools/video/tts/check.mjs:144)
// compares pinyin-pro readings with these exact options. Run from the repo root so require() finds
// the repo's node_modules; nothing is written.
const { pinyin } = require(path.join(ROOT, "node_modules/pinyin-pro"));
const opts = { toneType: "num", type: "array", nonZh: "consecutive", v: true };
const lines = {
  "L002 intended": "字簽了，妳也就沒用了。", "L002 heard": "字簽了 你也就沒用了",
  "L026 intended": "棠棠，妳連我也信不過？", "L026 heard": "棠棠，你連我也信不過？",
  "她": "她", "他": "他", "妳": "妳", "你": "你",
};
const out = { "pinyin-pro": require(path.join(ROOT, "node_modules/pinyin-pro/package.json")).version, readings: {} };
for (const [k, v] of Object.entries(lines)) out.readings[k] = pinyin(v, opts).join(" ");
console.log(JSON.stringify(out, null, 1));
