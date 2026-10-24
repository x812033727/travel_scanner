// Deterministic, nonpaid projection of the owner-approved C08 short-v8 inputs.
// Run from any directory: node docs/videos/story-everyday-kikkoman-c08/short-v8/build.mjs
import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const c08 = path.dirname(here);
const narrationFile = path.join(c08, "reviews", "v8-short-narration-candidate-20261024.md");
const visualFile = path.join(c08, "reviews", "v8-short-visual-plan-candidate-20261024.md");
const expected = {
  [narrationFile]: "040d9a499ddb864f62ebf0edcc948cc58439ffa13d0dae0ce5a9475297ee5d69",
  [visualFile]: "0676e76a4c9d49b12ece74df1835a72ce264eabb24a3158635921f57244dd241",
};
const sha256 = (buffer) => createHash("sha256").update(buffer).digest("hex");
function frozenText(file) {
  const bytes = readFileSync(file);
  const actual = sha256(bytes);
  if (actual !== expected[file]) throw new Error(`${path.basename(file)} changed: ${actual}`);
  return bytes.toString("utf8");
}
function cells(line) {
  return line.split("|").slice(1, -1).map((part) => part.trim());
}

const narration = [];
let chapter = 0;
let chapterName = "";
for (const line of frozenText(narrationFile).split(/\r?\n/)) {
  const heading = /^## ([1-6]) (.+)$/.exec(line);
  if (heading) { chapter = Number(heading[1]); chapterName = heading[2]; }
  if (!/^\| v7\w+ \|/.test(line)) continue;
  const row = cells(line);
  if (row.length !== 3 || !chapter) throw new Error(`bad narration row: ${line}`);
  narration.push({ chapter, chapter_name: chapterName, id: row[0], text: row[1], basis: row[2] });
}
const visuals = [];
for (const line of frozenText(visualFile).split(/\r?\n/)) {
  if (!/^\| [1-6] \| v7\w+ \|/.test(line)) continue;
  const row = cells(line);
  if (row.length !== 5 || !["shot", "card"].includes(row[2])) throw new Error(`bad visual row: ${line}`);
  visuals.push({ chapter: Number(row[0]), id: row[1], type: row[2], direction: row[3], camera_direction: row[4] });
}
if (narration.length !== 36 || visuals.length !== 36) throw new Error(`expected 36/36 rows, got ${narration.length}/${visuals.length}`);
const seen = new Set();
for (let i = 0; i < narration.length; i++) {
  const n = narration[i];
  const v = visuals[i];
  if (n.id !== v.id || n.chapter !== v.chapter || seen.has(n.id)) throw new Error(`row ${i + 1} is not one-to-one`);
  seen.add(n.id);
}
const counts = Array.from({ length: 6 }, (_, index) => narration.filter((row) => row.chapter === index + 1).length);
if (counts.join(",") !== "6,6,6,5,7,6") throw new Error(`chapter counts moved: ${counts}`);
if (visuals.filter((row) => row.type === "shot").length !== 30) throw new Error("expected 30 illustrated shots");
if (visuals.filter((row) => row.type === "card").length !== 6) throw new Error("expected 6 postproduction cards");

// The stats template is only a text preview. visual-plan.json keeps the exact approved
// direction; v7e03 still needs a separately reviewed flat diagram in postproduction.
const cardPreview = {
  v7o01: { value: "1.8 L", label: "設計團隊多年後回顧的大瓶", source: "R1" },
  v7o05: { value: "1955｜1 L 瓶", label: "公司回顧", source: "K1" },
  v7bb01: { value: "寬底、收腰", label: "後年展覽標籤", source: "M1" },
  v7e03: { value: "下緣內收／上緣在前", label: "平面功能示意待後製", source: "E1、K4、M1" },
  v7e04: { value: "接近 100 個模型", label: "後年展覽標籤", source: "M1" },
  v7n01: { value: "1961｜150 mL", label: "桌上瓶上市", source: "K1、K2a、D1" },
};
const original = JSON.parse(readFileSync(path.join(c08, "video.json"), "utf8"));
const slug = "story-everyday-kikkoman-c08-short-v8";
const chapterStarts = new Set(narration.filter((row, index) => index === 0 || row.chapter !== narration[index - 1].chapter).map((row) => row.id));
const scenes = narration.map((row, index) => {
  const visual = visuals[index];
  const scene = {
    id: `c08-v8-sc-${row.id}`,
    ...(chapterStarts.has(row.id) ? { chapter: row.chapter_name } : {}),
    template: visual.type === "shot" ? "shot" : "stats",
    data: visual.type === "shot"
      ? { prompt: visual.direction, camera: visual.camera_direction, visual: "still" }
      : { stats: [{ value: cardPreview[row.id].value, label: cardPreview[row.id].label }], source: cardPreview[row.id].source },
    claims: [row.id],
    lines: [{ id: row.id, text: row.text, emotion: original.scenes[0].lines[0].emotion }],
  };
  return scene;
});
const sources = [0, 1, 6, 7, 8, 10, 11].map((index) => original.sources[index]);
const video = {
  ...original,
  slug,
  target_minutes: [4, 5],
  loops: [
    { setup: "v7h02", payoff: "v7e07", what: "移瓶時那一滴怎麼少些" },
    { setup: "v7h04", payoff: "v7i04", what: "商品瓶為何接手陶壺" },
    { setup: "v7h05", payoff: "v7i04", what: "縮小容量是否夠用" },
    { setup: "v7o07", payoff: "v7i01", what: "龜甲萬找誰設計" },
    { setup: "v7bi07", payoff: "v7b03", what: "瓶腰怎麼給手握" },
    { setup: "v7b07", payoff: "v7e03", what: "嘴尖上下緣的方向" },
    { setup: "v7be08", payoff: "v7n01", what: "何時成為預裝商品" },
    { setup: "v7bn02", payoff: "v7n04", what: "用完後如何補充" },
  ],
  youtube: {
    ...original.youtube,
    title: "龜甲萬：小醬油瓶怎麼走上餐桌？｜品牌故事",
    description: "從大瓶與陶壺的分工，到 1961 年 150 mL 預裝桌上瓶：龜甲萬如何讓商品瓶走上餐桌？本集沿著握法、瓶嘴與補充開口，追問一次倒醬油的動作。公司與設計團隊的事後回顧、設計師訪談與 MoMA 後年展覽標籤各有來源界線；畫面是匿名功能示意，沒有重建當年原物。資料查核日期：2026-10-24。",
    video_id: null,
  },
  thumbnail: { ...original.thumbnail, data: { ...original.thumbnail.data, shot: "c08-v8-sc-v7h01" } },
  sources,
  scenes,
};
const series = {
  ...JSON.parse(readFileSync(path.join(c08, "series.json"), "utf8")),
  logline: "一支預先裝好的 150 mL 醬油瓶，怎麼取代大瓶轉注陶壺的桌上工作，並在收手時少留一滴？",
  image_model: "image-01",
  look: { preset: "cute-mystery" },
};
const visualPlan = {
  schema_version: 1,
  slug,
  approved_narration_sha256: expected[narrationFile],
  approved_visual_plan_sha256: expected[visualFile],
  rows: visuals.map(({ id, type, direction, camera_direction }) => ({ id, type, ...(type === "shot" ? { prompt: direction } : { postproduction_text: direction }), camera_direction })),
};
const write = (name, value) => writeFileSync(path.join(here, name), `${JSON.stringify(value, null, 2)}\n`, "utf8");
write("video.json", video);
write("series.json", series);
write("visual-plan.json", visualPlan);
writeFileSync(path.join(here, "script.md"), [
  "# C08 龜甲萬｜短版 v8 核准旁白投影",
  "",
  `原件 SHA-256：${expected[narrationFile]}。本檔只投影原件的 ID 與旁白；原件來源界線見 reviews/v8-short-narration-candidate-20261024.md。`,
  "",
  ...Array.from({ length: 6 }, (_, index) => {
    const rows = narration.filter((row) => row.chapter === index + 1);
    return [`## ${index + 1} ${rows[0].chapter_name}`, "", ...rows.map((row) => `- ${row.id} ${row.text}`), ""];
  }).flat(),
].join("\n"), "utf8");
writeFileSync(path.join(here, "claims.md"), [
  "# C08 龜甲萬｜短版 v8 主張索引",
  "",
  `原件 SHA-256：${expected[narrationFile]}。依據與界線逐字取自凍結旁白稿；獨立 36／36 來源判定見 ../reviews/v8-short-independent-review-20261024.md。`,
  "",
  "| 主張 ID | 旁白 | 依據與界線 |",
  "| --- | --- | --- |",
  ...narration.map((row) => `| ${row.id} | ${row.text} | ${row.basis} |`),
  "",
].join("\n"), "utf8");
writeFileSync(path.join(here, "verify-1.md"), [
  "# C08 龜甲萬｜短版 v8 獨立查核的 QA 對接",
  "",
  `凍結旁白 SHA-256：${expected[narrationFile]}；逐鏡 SHA-256：${expected[visualFile]}。本表轉載 ../reviews/v8-short-independent-review-20261024.md 的 36／36 來源與配鏡 PASS，不是新一輪查核、實際 TTS、圖片驗收或付費許可。`,
  "",
  "| 主張 ID | 既有獨立判定 | 依據與界線 |",
  "| --- | --- | --- |",
  ...narration.map((row) => `| ${row.id} | CONFIRMED | ${row.basis} |`),
  "",
].join("\n"), "utf8");
console.log(`C08 short-v8: ${narration.length} lines, ${visuals.filter((row) => row.type === "shot").length} shots, ${visuals.filter((row) => row.type === "card").length} cards; frozen hashes match`);
