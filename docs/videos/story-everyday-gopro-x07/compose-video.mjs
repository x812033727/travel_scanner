// Build the source-bound GoPro X07 preproduction package from one authoring file.
// No paid media or remote API calls occur here. Reviews bind the output SHA.
import { createHash } from "node:crypto";
import { writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { textHash } from "../../../tools/video/core/schema.mjs";
import { chapters } from "./drafts/story.mjs";

const dir = path.dirname(fileURLToPath(import.meta.url));
const slug = "story-everyday-gopro-x07";
const checkedOn = "2026-10-20";
const sources = [
  { title: "GoPro FY2016 Form 10-K", url: "https://www.sec.gov/Archives/edgar/data/1500435/000150043517000013/gpro2016-12x3110xk.htm", checked_on: checkedOn },
  { title: "GoPro FY2016 Q3 Form 10-Q", url: "https://www.sec.gov/Archives/edgar/data/1500435/000150043516000126/gpro2016-09x3010xq.htm", checked_on: checkedOn },
  { title: "GoPro FY2017 Form 10-K", url: "https://www.sec.gov/Archives/edgar/data/1500435/000150043518000010/gpro2017-12x3110xk.htm", checked_on: checkedOn },
  { title: "GoPro FY2017 Q1 Form 10-Q", url: "https://www.sec.gov/Archives/edgar/data/1500435/000150043517000028/gpro2017-03x3110xq.htm", checked_on: checkedOn },
  { title: "GoPro FY2017 Q3 Form 10-Q", url: "https://www.sec.gov/Archives/edgar/data/1500435/000150043517000059/gpro2017-09x3010xq.htm", checked_on: checkedOn },
  { title: "GoPro 2018-01-08 Form 8-K", url: "https://www.sec.gov/Archives/edgar/data/1500435/000150043518000002/gopro8-kjanuary2018.htm", checked_on: checkedOn },
  { title: "GoPro 2018-01-08 company release (8-K Exhibit 99.1)", url: "https://www.sec.gov/Archives/edgar/data/1500435/000150043518000002/pressreleasejanuary2018.htm", checked_on: checkedOn },
  { title: "GoPro FY2018 Form 10-K", url: "https://www.sec.gov/Archives/edgar/data/1500435/000150043519000013/gpro2018-12x3110xk.htm", checked_on: checkedOn },
];
const cameras = ["push in", "pan left", "static", "pan right", "tilt up", "pull back"];
const framings = ["Medium shot", "Wide shot", "Close shot", "Overhead shot"];
const pronunciations = [["GoPro", "狗普羅"], ["Karma", "卡瑪"], ["HERO5 Black", "希羅五布萊克"]];
const makeLine = (id, value) => {
  const line = { id, text: value, emotion: value.endsWith("？") ? "問句上揚，停半拍" : "說書語氣，自然有起伏" };
  const say = pronunciations.reduce((text, [word, spoken]) => text.replaceAll(word, spoken), value);
  if (say !== value) Object.assign(line, { say, say_for: textHash(value) });
  return line;
};
const authoredScenes = chapters.flatMap((chapter, ci) => chapter.rows.map(([value, claim_refs, visual], ri) => {
  const number = String(ri + 1).padStart(2, "0");
  const id = `x07-b${String(ci + 1).padStart(2, "0")}-s${number}`;
  const line = makeLine(`x07${String(ci + 1).padStart(2, "0")}${number}`, value);
  const scene = {
    id,
    template: typeof visual === "string" && visual !== "outro" ? "shot" : visual === "outro" ? "outro" : "stats",
    data: typeof visual === "string" && visual !== "outro"
      ? { prompt: `${framings[(ci + ri) % framings.length]} ${visual}`, camera: cameras[(ci * 2 + ri) % cameras.length], visual: "still" }
      : visual === "outro" ? { title: "GoPro 的退場決定", cta: "訂閱品牌故事" } : visual,
    lines: [line],
    claim_refs,
  };
  if (ri === 0) scene.chapter = chapter.title;
  return scene;
}));
const closing = authoredScenes.splice(-3, 3);
if (!closing.every(scene => scene.template === "outro")) throw new Error("Last three authored lines must be outro");
authoredScenes.push({ id: "x07-outro", template: "outro", data: closing[0].data, lines: closing.flatMap(scene => scene.lines) });
const scenes = authoredScenes.map(({ claim_refs: _refs, ...scene }) => scene);
const ids = new Map(scenes.flatMap((scene, index) => scene.lines.map(line => [line.id, index])));
const loop = (setup, payoff, what) => {
  if (ids.get(setup) === undefined || ids.get(payoff) === undefined || ids.get(setup) >= ids.get(payoff)) throw new Error(`Invalid loop ${setup} -> ${payoff}`);
  return { setup, payoff, what };
};
const loops = [
  loop("x070104", "x070301", "飛行中斷電後的撤回範圍"),
  loop("x070105", "x070401", "隔年第一季的復售計畫是否落地"),
  loop("x070106", "x070411", "年底改價在財報留下的數字"),
  loop("x070107", "x070503", "重組後 Karma 是否仍在產品線"),
  loop("x070108", "x070617", "空中業務為何列入重組"),
  loop("x070205", "x070208", "空中拍攝如何接回地面"),
  loop("x070210", "x070211", "飛手以外的人如何控制畫面"),
  loop("x070215", "x070216", "模組化拍攝系統的開發投入"),
  loop("x070221", "x070301", "上市後飛行問題如何處置"),
  loop("x070305", "x070313", "撤回和相機延誤在報表留下什麼"),
  loop("x070315", "x070401", "出貨後何時重新販售"),
  loop("x070406", "x070409", "第三季 Karma 銷售變化對毛利影響"),
  loop("x070410", "x070413", "年底改價之外是否還有 Karma 專屬費用"),
  loop("x070415", "x070506", "復售後是否仍投入空中市場"),
  loop("x070515", "x070601", "空中業務何時實際關閉"),
  loop("x070611", "x070612", "既有買家的售後支援"),
];
const description = [
  "GoPro 的 Karma 無人機在 2016 年因部分機體飛行中失去電力而撤回，2017 年重新上市。公司在 2018 年公告自稱 Karma 在前一年於其價位帶排第二，卻同時決定售完庫存後退出消費無人機。本集沿同期 SEC 文件，追產品設計、復售、毛利挑戰、重組與後續財報結果。",
  "",
  "『價位帶第二』為 GoPro 2018 年公告中的自述，原件沒有交代價帶界線、地區或可獨立核算的市占分母。公司列出競爭、毛利，以及當時的歐美監管環境可能在往後幾年壓縮市場，作為退出理由；2016 年撤回不能單獨解釋決定。FY2017 第四季 US$80.5m 營收減項含相機與 Karma 的價格保護及通路行銷支持；FY2018 Karma 無人機及配件收入減少 US$62.0m 是同比收入變化，不是產品虧損。插畫為無標誌概念示意，非真實員工、店面或事故影像。資料查核日期：2026-10-20。",
  "",
  "一手資料（SEC 原始申報與公司附件）",
  ...sources.flatMap(source => [source.title, source.url]),
].join("\n");
const doc = {
  schema_version: 1,
  slug,
  format: "drama",
  category: "explainer",
  narration_locale: "zh-TW",
  target_minutes: [8, 10],
  voice: { provider: "gemini", name: "Sulafat", style: "標準國語，咬字清楚，台北人平常說話的語調。像對朋友講有申報支持的品牌轉折；數字放慢，問句上揚，揭曉前停半拍。", performance: "二〇一六年撤回、二〇一七年復售與定價、二〇一八年退出依時間分開；收入、毛利率與費用不要混念。" },
  subtitles: { burn_in: false },
  look: { preset: "cute-mystery" },
  characters: [],
  series: { slug: "brand-stories-everyday-reversals-extra", episode: 7, chapter: 1 },
  music: { prompt: "light, curious, a little mysterious, no vocals", gain_db: -20, duck_db: -10 },
  loops,
  youtube: { category_id: 27, made_for_kids: false, default_language: "zh-TW", title: "GoPro 的無人機才重新上市，為何隔年就退出？｜品牌故事", description, tags: ["GoPro", "Karma", "品牌故事", "無人機", "運動攝影機", "商業史", "企業策略"], video_id: null },
  thumbnail: { template: "thumb", data: { headline: "**停飛？**", tag: "品牌故事", brand: "GoPro", shot: "x07-b02-s08" } },
  sources,
  assets: [],
  scenes,
};
const videoBytes = JSON.stringify(doc, null, 2) + "\n";
writeFileSync(path.join(dir, "video.json"), videoBytes);
const sha256 = createHash("sha256").update(videoBytes).digest("hex");
const escape = value => String(value).replaceAll("|", "\\|").replaceAll("\n", " ");
const original = chapters.flatMap((chapter, ci) => chapter.rows.map(([value, claimRefs], ri) => ({ id: `x07${String(ci + 1).padStart(2, "0")}${String(ri + 1).padStart(2, "0")}`, value, claimRefs })));
const matrix = [
  "# X07 GoPro Karma｜逐句來源矩陣", "",
  "本表由 `drafts/story.mjs` 生成；K 編號及邊界見 [source-matrix.md](source-matrix.md)。本版獨立來源審查見 [source-review-v7.md](reviews/source-review-v7.md)。", "",
  `- \`video.json\` SHA-256：\`${sha256}\``, "",
  "| 句 ID | 旁白 | Treatment 主張 |", "| --- | --- | --- |",
  ...original.map(row => `| \`${row.id}\` | ${escape(row.value)} | ${row.claimRefs.length ? row.claimRefs.join("、") : "編輯問句／CTA"} |`), "",
].join("\n");
writeFileSync(path.join(dir, "line-source-matrix.md"), matrix);
const script = ["# X07 GoPro Karma｜繁中逐句稿", "", `稿件綁定 \`video.json\` SHA-256 \`${sha256}\`。尚無 TTS 實測；片頭片尾不計入實質正文。`, "", ...chapters.flatMap((chapter, ci) => [
  `## ${ci === 0 ? "濃縮開場" : `第 ${ci} 章`}｜${chapter.title}`, "",
  ...chapter.rows.map(([value], ri) => `- \`x07${String(ci + 1).padStart(2, "0")}${String(ri + 1).padStart(2, "0")}\` ${value}`), "",
])].join("\n");
writeFileSync(path.join(dir, "script.md"), script);
writeFileSync(path.join(dir, "series.json"), JSON.stringify({ kind: "story", slug: "brand-stories-everyday-reversals-extra", episode: 7, chapter: 1, title: "GoPro：無人機才復售，為何隔年退出？", logline: "從 Karma 2016 撤回、2017 復售，到公司自稱價位帶第二仍在 2018 關閉空中業務；一台相機公司的新產品線怎麼被毛利與市場難題擋下。", names: ["GoPro", "Karma", "HERO5", "HERO6", "GoPro Plus"], characters: [], target_minutes: 10, image_model: "image-01", style_preset: "custom", look: { preset: "cute-mystery" }, visual_tier: "stills", compilation: false }, null, 2) + "\n");
console.log(JSON.stringify({ scenes: scenes.length, shots: scenes.filter(s => s.template === "shot").length, cards: scenes.filter(s => s.template === "stats").length, lines: original.length, characters: original.reduce((sum, row) => sum + row.value.length, 0), loops: loops.length, video_sha256: sha256 }, null, 2));
