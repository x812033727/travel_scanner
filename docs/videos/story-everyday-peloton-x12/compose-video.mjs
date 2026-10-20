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
  "已有美國廠，五月又宣布一座新廠",
  "設備訂單增加，交貨壓力跟上",
  "俄亥俄新廠要組裝自家車款",
  "二月廠殼轉向出售，六月硬體帳見變化",
  "七月轉向代工，九月廠殼仍待售",
  "二〇二三年，出售工作仍在拖延",
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
  let previous = 0;
  for (const row of chapter) {
    const match = new RegExp(`^x12${String(ci + 1).padStart(2, "0")}(\\d{2})$`).exec(row.id);
    const number = Number(match?.[1]);
    // Preserve source-review line IDs when an unnecessary line is cut in a later revision.
    if (!match || number <= previous) throw new Error(`Invalid or unordered chapter line id: ${row.id}`);
    previous = number;
  }
}
for (const [ri, row] of outro.entries()) if (row.id !== `x1206${String(12 + ri).padStart(2, "0")}`) throw new Error(`Bad closing id: ${row.id}`);

const cards = new Map(Object.entries({
  x120407: ["FY2021 → FY2022｜設備類收入", "US$3,149.6m → 2,187.5m", "收入，非單車台數", "K22"],
  x120408: ["FY2021 → FY2022｜訂閱收入", "US$872.2m → 1,394.7m", "同表口徑", "K22"],
  x120512: ["截至 2022-06-30｜Ohio 專案", "約 US$86.6m", "已投資，非出售價格", "K22"],
  x120514: ["FY2022｜Ohio 相關資產減損", "US$40.3m", "含相關製造資產，非售價", "K22"],
  x120601: ["FY2023｜設備類收入", "US$1,130.2m", "收入，非台數", "K23"],
  x120602: ["FY2023｜訂閱收入", "US$1,670.1m", "收入，非利潤", "K23"],
}));
const cameras = ["Medium shot, slow push in", "Close-up, static", "Wide shot, pan right", "Medium shot, parallax"];
const settings = ["plain office", "small workshop", "ordinary warehouse", "modest living room"];
const lights = ["soft window light", "mild overhead light", "grey daylight", "desk lamp"];
const sceneSettings = new Map([
  ["x120101", "clean tabletop Ohio factory diorama"], ["x120103", "clean tabletop Ohio factory diorama"],
  ["x120104", "clean tabletop Ohio factory diorama"], ["x120105", "clean tabletop Ohio factory diorama"],
  ["x120106", "clean tabletop unfinished assembly diagram"], ["x120107", "clean tabletop factory diorama"],
  ["x120108", "clean tabletop Ohio factory diorama"], ["x120109", "clean tabletop accounting diorama"],
  ["x120110", "clean tabletop Ohio factory diorama"], ["x120201", "clean tabletop factory diorama"],
  ["x120203", "clean concept-animation studio"],
  ["x120219", "clean tabletop factory diorama"], ["x120221", "clean tabletop factory diorama"],
  ["x120301", "clean tabletop factory diorama"], ["x120401", "clean tabletop Ohio factory diorama"],
  ["x120402", "clean tabletop Ohio factory diorama"], ["x120403", "clean tabletop factory diorama"],
  ["x120501", "clean conceptual manufacturing-plan studio"], ["x120502", "conceptual Taiwan factory diorama"],
  ["x120506", "conceptual split-screen comparison studio"], ["x120507", "clean tabletop factory diorama"],
  ["x120511", "clean tabletop Ohio factory diorama"], ["x120516", "clean tabletop Ohio factory diorama"],
  ["x120518", "clean tabletop accounting diorama"], ["x120604", "clean conceptual living-room diorama"],
  ["x120608", "clean tabletop Ohio factory diorama"], ["x120611", "clean tabletop Ohio factory diorama"],
]);
const sayWords = [["Peloton", "派樂騰"], ["Output Park", "歐普特帕克"], ["Ohio", "俄亥俄"], ["Precor", "普瑞科"], ["Rexon", "力山"], ["Tonic", "托尼克"], ["Tread+", "Tread Plus"], ["Bike+", "Bike Plus"], ["Tread", "Tread"], ["Bike", "Bike"]];
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
    : { id, template: "shot", data: { prompt: `${cameras[ri % cameras.length]} in a ${sceneSettings.get(row.id) ?? settings[(ri + ci) % settings.length]}: ${row.cue}，所有文件、招牌與器材皆無字無標誌，${lights[(ri + ci) % lights.length]}`, camera: cameras[ri % cameras.length], visual: "still" }, lines: [lineFor(row)] };
  if (ri === 0) scene.chapter = chapterTitles[ci];
  return scene;
}));
scenes.push(...outro.map((row, ri) => ({
  id: `x12-outro-s${String(ri + 1).padStart(2, "0")}`, template: "shot",
  data: { prompt: `${cameras[ri % cameras.length]} in an ordinary office: ${row.cue}，所有文件與道具無字無標誌，soft window light`, camera: cameras[ri % cameras.length], visual: "still" },
  lines: [lineFor(row)],
})));
const loops = [
  ["x120104", "x120301", "既有美國廠之外再蓋新廠的缺口"],
  ["x120105", "x120401", "二月重整怎麼處理 Ohio 廠殼"],
  ["x120106", "x120401", "二月廠殼下一步是否造車"],
  ["x120107", "x120501", "七月自有產線分工改成什麼"],
  ["x120108", "x120507", "自有廠造車工作與 Ohio 廠殼各往哪裡去"],
  ["x120109", "x120512", "Ohio 未投產時已投多少"],
  ["x120109", "x120516", "九月年報是否報出 Ohio 出售回款"],
  ["x120110", "x120612", "Ohio 從新增產能變成已干擾營運的處置負擔"],
  ["x120209", "x120211", "原有代工網可怎樣調整交貨"],
  ["x120213", "x120214", "多蓋新廠能否解除零件供應限制"],
  ["x120221", "x120301", "新廠原本要補的產能"],
  ["x120309", "x120312", "展示間與參觀門前的工程和設備阻礙"],
  ["x120316", "x120401", "無法立刻縮回的廠殼後來怎樣"],
  ["x120319", "x120401", "二月 Ohio 廠殼決定"],
  ["x120413", "x120501", "其他自有產線會怎樣"],
  ["x120510", "x120516", "九月年報有無報出已投 Ohio 的回款"],
  ["x120515", "x120516", "九月年報是否有成交回款"],
  ["x120519", "x120605", "訂閱成長能否證明 Ohio 新機產能仍有需求"],
  ["x120603", "x120605", "訂閱成長是否代表新機訂單"],
  ["x120607", "x120608", "Ohio 出售是否出現新進度"],
  ["x120611", "x120612", "FY2023 出售工作是否已干擾其他營運"],
].map(([setup, payoff, what]) => ({ setup, payoff, what }));
const ids = new Map(allRows.map((row, i) => [row.id, i]));
for (const loop of loops) if (!(ids.has(loop.setup) && ids.has(loop.payoff) && ids.get(loop.setup) < ids.get(loop.payoff))) throw new Error(`Invalid loop: ${JSON.stringify(loop)}`);

const description = [
  "2021 年，Peloton 宣布在 Ohio 規劃一座專用工廠，原定 2023 製造連網健身設備、多年預計投入約 US$400m；2022 年 2 月重整已宣布完成 Ohio 廠殼後出售，這仍是計畫，不是已成交。7 月公司才進一步宣布退出整體自有製造。FY2022 年報記下一筆涉及未投產 Ohio 及相關製造資產的減損，9 月提交時仍說正在對外行銷並打算出售。FY2023 年報更記載出售延誤和已發生的營運干擾，仍寫打算出售。這支品牌故事沿著 Output Park 一座工廠，追兩次製造決定與廠房的去向。",
  "",
  "約 US$400m 是 2021 年計畫，不是已支出；截至 2022-06-30 專案已投入約 US$86.6m，也不是出售價格。FY2022 硬體類收入包括配件、配送安裝等，不能直接換算單車台數；分類毛利不能當公司淨利。2 月 Ohio 廠殼完成後出售的公告不等於當時已完工或已售；2022-07-12 公告停運的是台灣 Tonic 設施，Rexon 將主造 Bike／Tread；Ohio 到 FY2023 年報仍是尋買家，本文不宣稱後來已售。畫面為匿名概念插畫，不是實際廠房、器材或人物。資料查核日期：2026-10-20。",
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
  youtube: { category_id: 27, made_for_kids: false, default_language: "zh-TW", title: "Peloton 四億美元新廠計畫，出車前發生了什麼？｜品牌故事", description, tags: ["Peloton", "品牌故事", "健身單車", "訂閱", "製造", "Ohio"], video_id: null },
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
writeFileSync(path.join(dir, "series.json"), JSON.stringify({ kind: "story", slug: "brand-stories-everyday-reversals-extra", episode: 12, chapter: 1, title: "Peloton：Ohio 四億美元新廠計畫，出車前發生了什麼？", logline: "從 2021 Ohio 產能計畫，到 2022 二月規劃完成廠殼後出售、七月整體退出自製，FY2023 仍尋買家。", names: ["Peloton", "Peloton Output Park", "Precor", "Rexon", "Tonic", "Bike", "Bike+", "Tread", "Tread+"], characters: [], target_minutes: 10, image_model: "image-01", style_preset: "custom", look: { preset: "cute-mystery" }, visual_tier: "stills", compilation: false }, null, 2) + "\n");
const body = chapters.slice(1).flat().map(row => row.text).join("");
console.log(JSON.stringify({ scenes: scenes.length, shots: scenes.filter(scene => scene.template === "shot").length, cards: scenes.filter(scene => scene.template === "stats").length, spoken_lines: allRows.length, hook_characters: chapters[0].map(row => row.text).join("").length, body_characters: body.length, body_estimate_minutes_at_250_cpm: +(body.length / 250).toFixed(2), body_estimate_minutes_at_300_cpm: +(body.length / 300).toFixed(2), loops: loops.length, video_sha256: sha }, null, 2));
