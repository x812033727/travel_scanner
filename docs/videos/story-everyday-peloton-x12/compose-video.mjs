// Rebuilds the local preproduction packet only; never contacts a media provider.
import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { textHash } from "../../../tools/video/core/schema.mjs";

const dir = path.dirname(fileURLToPath(import.meta.url));
const slug = "story-everyday-peloton-x12";
const sourceUrls = [
  { code: "A21", title: "Peloton 2021-05-24 公告，8-K Exhibit 99.1", url: "https://www.sec.gov/Archives/edgar/data/1639825/000163982521000174/pton-may24announcement.htm", checked_on: "2026-10-20" },
  { code: "K21", title: "Peloton FY2021 Form 10-K", url: "https://www.sec.gov/Archives/edgar/data/1639825/000163982521000256/pton-20210630.htm", checked_on: "2026-10-20" },
  { code: "A22", title: "Peloton 2022-07-12 公告，8-K Exhibit 99.1", url: "https://www.sec.gov/Archives/edgar/data/1639825/000163982522000091/ex991pressrelease.htm", checked_on: "2026-10-20" },
  { code: "K22", title: "Peloton FY2022 Form 10-K", url: "https://www.sec.gov/Archives/edgar/data/1639825/000163982522000117/pton-20220630.htm", checked_on: "2026-10-20" },
  { code: "K23", title: "Peloton FY2023 Form 10-K", url: "https://www.sec.gov/Archives/edgar/data/1639825/000163982523000132/pton-20230630.htm", checked_on: "2026-10-20" },
];
const chapterTitles = [
  "Ohio 工廠的計畫與另一份年報",
  "一台設備接上一筆月費",
  "新工廠被畫進產線地圖",
  "同一份年報裡的兩條收入線",
  "自製方案被收起來",
  "訂閱走高，製造方式換了",
];
const chapters = Array.from({ length: 6 }, () => []);
const outro = [];
let current = null;
for (const raw of readFileSync(path.join(dir, "drafts/narration.md"), "utf8").split(/\r?\n/)) {
  const header = raw.match(/^## (b\d\d|outro):/);
  if (header) { current = header[1] === "outro" ? outro : chapters[Number(header[1].slice(1)) - 1]; continue; }
  const parts = raw.split("|").map(part => part.trim());
  if (!/^x12\d{4}$/.test(parts[0] ?? "")) continue;
  if (!current || parts.length !== 4) throw new Error(`Malformed draft row: ${raw}`);
  const [id, refs, text, cue] = parts;
  if (!text || !cue) throw new Error(`Missing text/visual: ${id}`);
  current.push({ id, refs: refs === "editorial" ? [] : refs.split(","), text, cue });
}
if (chapters.some(chapter => chapter.length < 8) || outro.length !== 3) throw new Error("Expected six full chapters and three closing lines");
const allRows = [...chapters.flat(), ...outro];
if (new Set(allRows.map(row => row.id)).size !== allRows.length) throw new Error("Duplicate line id");
for (const [ci, chapter] of chapters.entries()) {
  for (const [ri, row] of chapter.entries()) {
    const expected = `x12${String(ci + 1).padStart(2, "0")}${String(ri + 1).padStart(2, "0")}`;
    if (row.id !== expected) throw new Error(`Nonsequential id: ${row.id}, expected ${expected}`);
  }
}
for (const [ri, row] of outro.entries()) if (row.id !== `x1206${String(chapters[5].length + ri + 1).padStart(2, "0")}`) throw new Error(`Bad closing id: ${row.id}`);

const cards = new Map(Object.entries({
  x120204: ["FY2020｜設備類收入", "US$1,462.2m", "FY2022 10-K 同表口徑", "K22"],
  x120206: ["FY2020 → FY2021｜訂閱收入", "US$363.7m → 872.2m", "收入，不等於利潤", "K22"],
  x120305: ["2021-05｜Ohio 新廠計畫", "約 US$400m", "多年規劃，非已支出", "A21"],
  x120402: ["FY2021 → FY2022｜設備類收入", "US$3,149.6m → 2,187.5m", "收入，非單車台數", "K22"],
  x120403: ["FY2021 → FY2022｜訂閱收入", "US$872.2m → 1,394.7m", "同表口徑", "K22"],
  x120414: ["FY2022｜設備類毛利", "-US$246.3m", "分類毛損，非公司淨損", "K22"],
  x120415: ["FY2022｜訂閱類毛利", "+US$944.7m", "分類毛利，非公司淨利", "K22"],
  x120416: ["FY2021 → FY2022｜設備類毛利率", "29.0% → -11.3%", "收入扣產品成本，非淨利率", "K22"],
  x120515: ["截至 2022-06-30｜Ohio 專案", "約 US$86.6m", "已投資，非出售價格", "K22"],
  x120516: ["FY2022｜Ohio 相關資產減損", "US$40.3m", "含相關製造資產，非售價", "K22"],
  x120601: ["FY2023｜設備類收入", "US$1,130.2m", "收入，非台數", "K23"],
  x120602: ["FY2023｜訂閱收入", "US$1,670.1m", "收入，非利潤", "K23"],
  x120605: ["FY2023｜訂閱類毛利", "+US$1,122.1m", "分類毛利", "K23"],
  x120606: ["FY2023｜設備類毛利", "-US$198.6m", "分類毛損", "K23"],
  x120608: ["FY2023｜公司淨損", "-US$1,261.7m", "全公司，不是單一分類", "K23"],
}));
const cameras = ["Medium shot, slow push in", "Close-up, static", "Wide shot, pan right", "Medium shot, parallax"];
const settings = ["plain office", "small workshop", "ordinary warehouse", "modest living room"];
const lights = ["soft window light", "mild overhead light", "grey daylight", "desk lamp"];
const sayWords = [["Peloton", "派樂騰"], ["Output Park", "歐普特帕克"], ["Precor", "普瑞科"], ["Rexon", "力山"], ["Tonic", "托尼克"], ["Tread+", "Tread Plus"], ["Tread", "Tread"], ["Bike", "Bike"]];
function lineFor(row) {
  const line = { id: row.id, text: row.text, emotion: row.text.endsWith("？") ? "台灣口語說書，自然提問，不刻意放慢" : "台灣口語說書，數字清楚，正常語速" };
  const say = sayWords.reduce((v, [a, b]) => v.replaceAll(a, b), row.text);
  if (say !== row.text) Object.assign(line, { say, say_for: textHash(row.text) });
  return line;
}
const scenes = chapters.flatMap((chapter, ci) => chapter.map((row, ri) => {
  const id = `x12-b${String(ci + 1).padStart(2, "0")}-s${String(ri + 1).padStart(2, "0")}`;
  const card = cards.get(row.id);
  const scene = card ? { id, template: "stats", data: { title: card[0], stats: [{ value: card[1], label: card[2] }], source: sourceUrls.find(s => s.code === card[3]).title }, lines: [lineFor(row)] }
    : { id, template: "shot", data: { prompt: `${cameras[ri % cameras.length]} in a ${settings[(ri + ci) % settings.length]}: ${row.cue}，所有文件、招牌與器材皆無字無標誌，${lights[(ri + ci) % lights.length]}`, camera: cameras[ri % cameras.length], visual: "still" }, lines: [lineFor(row)] };
  if (ri === 0) scene.chapter = chapterTitles[ci];
  return scene;
}));
scenes.push(...outro.map((row, ri) => ({
  id: `x12-outro-s${String(ri + 1).padStart(2, "0")}`, template: "shot",
  data: { prompt: `${cameras[ri % cameras.length]} in an ordinary office: ${row.cue}，所有文件與道具無字無標誌，soft window light`, camera: cameras[ri % cameras.length], visual: "still" },
  lines: [lineFor(row)],
})));
const loops = [
  ["x120105", "x120314", "既有產線外為何另規劃 Ohio"],
  ["x120106", "x120405", "設備與訂閱收入誰先變"],
  ["x120107", "x120503", "製造轉由誰承擔"],
  ["x120109", "x120514", "Ohio 從產能計畫到尋買家"],
  ["x120210", "x120414", "設備銷售增長是否等於毛利"],
  ["x120221", "x120310", "新廠原本要補的產能"],
  ["x120319", "x120402", "增長中的設備收入隔年如何變"],
  ["x120426", "x120502", "固定製造基地是否仍是下一步"],
  ["x120427", "x120503", "下一個造車人是誰"],
  ["x120523", "x120601", "FY2023 收入線怎麼走"],
  ["x120523", "x120615", "Ohio 到 FY2023 的出售狀態"],
  ["x120604", "x120608", "訂閱成長是否代表整體獲利"],
].map(([setup, payoff, what]) => ({ setup, payoff, what }));
const ids = new Map(allRows.map((row, i) => [row.id, i]));
for (const loop of loops) if (!(ids.has(loop.setup) && ids.has(loop.payoff) && ids.get(loop.setup) < ids.get(loop.payoff))) throw new Error(`Invalid loop: ${JSON.stringify(loop)}`);

const description = [
  "2021 年，Peloton 宣布在 Ohio 規劃一座專用工廠，原定 2023 製造連網健身設備、多年預計投入約 US$400m；FY2022 年報卻說公司正在尋找買家。這支品牌故事沿著 Output Park 一座工廠，追設備與訂閱收入、庫存成本和製造分工的轉向。",
  "",
  "約 US$400m 是 2021 年計畫，不是已支出；截至 2022-06-30 專案已投入約 US$86.6m，也不是出售價格。FY2022 硬體類收入包括配件、配送安裝等，不能直接換算單車台數；分類毛利不能當公司淨利。2022-07-12 公告停運的是台灣 Tonic 設施，Rexon 將主造 Bike／Tread；Ohio 到 FY2023 年報仍是尋買家，本文不宣稱後來已售。畫面為匿名概念插畫，不是實際廠房、器材或人物。資料查核日期：2026-10-20。",
  "",
  "一手資料（SEC 原始歸檔）",
  ...sourceUrls.flatMap(source => [source.title, source.url]),
  "",
  "兩支 Shorts 與本集長片的真實 YouTube 連結，待發布後回填。",
].join("\n");
const video = {
  schema_version: 1, slug, format: "drama", category: "explainer", narration_locale: "zh-TW", target_minutes: [8, 12],
  voice: { provider: "gemini", name: "Sulafat", style: "標準國語，台灣自然口音。像向朋友說一座工廠的真實轉折；日期、財年與金額唸清楚，正常語速。", performance: "US$400m 是計畫、US$86.6m 是已投；Ohio 尋買家不是已售；分類毛利不同於淨利。" },
  subtitles: { burn_in: false }, look: { preset: "cute-mystery" }, characters: [],
  series: { slug: "brand-stories-everyday-reversals-extra", episode: 12, chapter: 1 },
  music: { prompt: "light, curious, a little mysterious, no vocals", gain_db: -20, duck_db: -10 },
  loops,
  youtube: { category_id: 27, made_for_kids: false, default_language: "zh-TW", title: "Peloton 四億美元新廠計畫，為何隔年尋找買家？｜品牌故事", description, tags: ["Peloton", "品牌故事", "健身單車", "訂閱", "製造", "Ohio"], video_id: null },
  thumbnail: { template: "thumb", data: { headline: "**廠沒開？**", tag: "品牌故事", brand: "Peloton", shot: "x12-b01-s04" } },
  sources: sourceUrls.map(({ code, ...source }) => source), assets: [], scenes,
};
const bytes = JSON.stringify(video, null, 2) + "\n";
writeFileSync(path.join(dir, "video.json"), bytes);
const sha = createHash("sha256").update(bytes).digest("hex");
const esc = value => value.replaceAll("|", "\\|");
writeFileSync(path.join(dir, "line-source-matrix.md"), [
  "# X12 Peloton｜逐句作者來源矩陣", "", "由 `compose-video.mjs` 從 `drafts/narration.md` 生成。此表是作者標註；另一位代理須以同版 SHA 逐句獨立查核。來源內容見 [source-matrix.md](source-matrix.md)。", "",
  `- \`video.json\` SHA-256：\`${sha}\``, "", "| 句 ID | 旁白 | 來源代碼 |", "| --- | --- | --- |",
  ...allRows.map(row => `| \`${row.id}\` | ${esc(row.text)} | ${row.refs.length ? row.refs.join("、") : "編輯問句／CTA"} |`), "",
].join("\n"));
writeFileSync(path.join(dir, "script.md"), [
  "# X12 Peloton｜繁中逐句稿", "", `離線前製；\`video.json\` SHA-256：\`${sha}\`。尚未獨立查核與盲審；實際 TTS 時長未量。第一章後放正式 5 秒片頭，最後三句後放正式 21 秒片尾；三句與兩段動畫不算正文。`, "",
  ...chapters.flatMap((chapter, ci) => [`## 第 ${ci + 1} 章｜${chapterTitles[ci]}${ci === 0 ? "（濃縮開場）" : ""}`, "", ...chapter.map(row => `- \`${row.id}\` ${row.text}`), ""]),
  "## 片尾三句", "", ...outro.map(row => `- \`${row.id}\` ${row.text}`), "",
].join("\n"));
writeFileSync(path.join(dir, "series.json"), JSON.stringify({ kind: "story", slug: "brand-stories-everyday-reversals-extra", episode: 12, chapter: 1, title: "Peloton：Ohio 工廠為何還沒投產就尋買家？", logline: "從 2021 Ohio 產能計畫到 2022 退出自製、FY2023 仍尋買家，追硬體與訂閱收入分岔。", names: ["Peloton", "Peloton Output Park", "Precor", "Rexon", "Tonic", "Bike", "Bike+", "Tread", "Tread+"], characters: [], target_minutes: 10, image_model: "image-01", style_preset: "custom", look: { preset: "cute-mystery" }, visual_tier: "stills", compilation: false }, null, 2) + "\n");
const body = chapters.slice(1).flat().map(row => row.text).join("");
console.log(JSON.stringify({ scenes: scenes.length, shots: scenes.filter(scene => scene.template === "shot").length, cards: scenes.filter(scene => scene.template === "stats").length, spoken_lines: allRows.length, hook_characters: chapters[0].map(row => row.text).join("").length, body_characters: body.length, body_estimate_minutes_at_250_cpm: +(body.length / 250).toFixed(2), body_estimate_minutes_at_300_cpm: +(body.length / 300).toFixed(2), loops: loops.length, video_sha256: sha }, null, 2));
