// Deterministic offline preproduction build. No story import or media-provider call.
import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { textHash } from "../../../tools/video/core/schema.mjs";
import { visualCueCount, visualFor } from "./drafts/visual-cues.mjs";

const dir = path.dirname(fileURLToPath(import.meta.url));
const slug = "story-everyday-fedex-x11";
const sourceUrls = [
  { title: "FedEx FY2022 Form 10-K", url: "https://www.sec.gov/Archives/edgar/data/1048911/000095017022012762/fdx-20220531.htm", checked_on: "2026-10-20" },
  { title: "FedEx FY2023 Form 10-K", url: "https://www.sec.gov/Archives/edgar/data/1048911/000095017023033201/fdx-20230531.htm", checked_on: "2026-10-20" },
  { title: "FedEx FY2024 Form 10-K", url: "https://www.sec.gov/Archives/edgar/data/1048911/000095017024083577/fdx-20240531.htm", checked_on: "2026-10-20" },
  { title: "FedEx FY2025 Form 10-K", url: "https://www.sec.gov/Archives/edgar/data/1048911/000104891125000011/fdx-20250531.htm", checked_on: "2026-10-20" },
  { title: "FedEx FY2026 Form 10-K", url: "https://www.sec.gov/Archives/edgar/data/1048911/000104891126000105/fdx-20260531.htm", checked_on: "2026-10-20" },
];
const chapters = [];
for (const raw of readFileSync(path.join(dir, "drafts/narration.md"), "utf8").split(/\r?\n/)) {
  const header = raw.match(/^## 第[一二三四五六]章｜(.+)$/);
  if (header) { chapters.push({ title: header[1].replace(/（濃縮開場.*$/, ""), rows: [] }); continue; }
  const row = raw.match(/^(.*?)\s+\[((?:F\d+(?:,F\d+)*|editorial))\]$/);
  if (!row) continue;
  if (!chapters.length) throw new Error(`Narration before first chapter: ${raw}`);
  chapters.at(-1).rows.push({ text: row[1].trim(), refs: row[2] === "editorial" ? [] : row[2].split(",") });
}
if (chapters.length !== 6 || chapters.some(chapter => !chapter.rows.length)) throw new Error("Expected six nonempty chapters");
chapters.forEach((chapter, ci) => {
  if (visualCueCount(ci) !== chapter.rows.length) throw new Error(`Chapter ${ci + 1}: ${visualCueCount(ci)} cues vs ${chapter.rows.length} lines`);
});
const idFor = (ci, ri) => `x11${String(ci + 1).padStart(2, "0")}${String(ri + 1).padStart(2, "0")}`;
const rows = chapters.flatMap((chapter, ci) => chapter.rows.map((row, ri) => ({ ...row, id: idFor(ci, ri), chapter: ci + 1 })));

// Two short adjoining lines can share one 5–8 second illustration without
// creating an overlong still. Starts are one-based, per chapter.
const pairStarts = [new Set([2]), new Set([4, 9, 13, 15, 26]), new Set([9, 12, 17, 25]), new Set([10, 15]), new Set([8, 10, 12, 17, 19]), new Set()];
const cards = new Map([
  ["x110221", { title: "FY2022｜Ground 的規模", stats: [{ value: ">680", label: "分揀與配送設施，美加" }, { value: "~160", label: "全自動站點，包含在設施內" }, { value: ">100,000", label: "獨立服務商持有／租用的車" }], source: "FedEx FY2022 10-K" }],
  ["x110307", { title: "FY2023｜Network 2.0", stats: [{ value: ">20", label: "已宣布實施的市場，非州數" }], source: "FedEx FY2023 10-K" }],
  ["x110405", { title: "兩種日期", stats: [{ value: "2024-04", label: "加拿大分階段轉換開始" }, { value: "2024-06-01", label: "Ground／Services 法律合併" }], source: "FedEx FY2024 10-K" }],
  ["x110408", { title: "FY2024｜美國推行範圍", stats: [{ value: ">50", label: "Network 2.0 實施地點" }], source: "FedEx FY2024 10-K" }],
  ["x110502", { title: "截至 2025-05-31", stats: [{ value: "~290", label: "美加實施最佳化的地點，非完成率" }], source: "FedEx FY2025 10-K" }],
  ["x110604", { title: "兩地 Network 2.0 進度", stats: [{ value: "加拿大", label: "FY2025 已完成實施" }, { value: "~360", label: "截至 FY2026 美國實施地點" }, { value: "2027 年底", label: "美國完成的公司預期" }], source: "FedEx FY2025／FY2026 10-K" }],
]);
const pronunciations = [
  ["Ground Economy", "地面經濟型配送"],
  ["FedEx Ground", "聯邦快遞地面包裹"],
  ["FedEx Freight", "聯邦快遞零擔貨運"],
  ["FedEx Services", "聯邦快遞企業服務"],
  ["Federal Express", "聯邦快遞公司"],
  ["one FedEx", "整合聯邦快遞"],
  ["Network 2.0", "網路二點零"],
  ["FedEx", "聯邦快遞"],
  ["Express", "快遞"],
  ["Ground", "地面包裹"],
  ["Freight", "零擔貨運"],
  ["Services", "企業服務"],
];
function lineFor(id, value) {
  const line = { id, text: value, emotion: value.endsWith("？") ? "自然提問，尾音微上揚" : "台灣口語說書，清楚自然，正常語速" };
  const say = pronunciations.reduce((current, [written, spoken]) => current.replaceAll(written, spoken), value);
  if (say !== value) Object.assign(line, { say, say_for: textHash(value) });
  return line;
}
const scenes = [];
for (const [ci, chapter] of chapters.entries()) {
  let sceneNo = 0;
  for (let ri = 0; ri < chapter.rows.length;) {
    const start = ri + 1;
    const pair = pairStarts[ci].has(start);
    const selected = chapter.rows.slice(ri, ri + (pair ? 2 : 1));
    if (pair && (selected.length !== 2 || selected.map(row => row.text).join("").length > 40)) throw new Error(`Invalid pair ${ci + 1}:${start}`);
    if (pair && selected.some((_, offset) => cards.has(idFor(ci, ri + offset)))) throw new Error(`Paired card ${ci + 1}:${start}`);
    const lineId = idFor(ci, ri);
    const card = cards.get(lineId);
    const scene = {
      id: `x11-b${String(ci + 1).padStart(2, "0")}-s${String(++sceneNo).padStart(2, "0")}`,
      template: card ? "stats" : "shot",
      data: card ?? { ...visualFor(ci, ri), visual: "still" },
      lines: selected.map((row, offset) => lineFor(idFor(ci, ri + offset), row.text)),
    };
    if (sceneNo === 1) scene.chapter = chapter.title;
    scenes.push(scene);
    ri += selected.length;
  }
}
const closing = scenes.splice(-3, 3);
if (closing.some(scene => scene.template !== "shot" || scene.lines.length !== 1)) throw new Error("Closing CTA must be three solo shots");
scenes.push({ id: "x11-outro", template: "outro", data: { title: "同一品牌，兩張路網", cta: "訂閱品牌故事" }, lines: closing.flatMap(scene => scene.lines) });

const find = (pattern, after = -1) => {
  const index = rows.findIndex((row, i) => i > after && pattern.test(row.text));
  if (index < 0) throw new Error(`Missing loop anchor: ${pattern}`);
  return [rows[index].id, index];
};
const loopPatterns = [
  [/先想改掉哪一段包裹旅程/, /FedEx 計畫整併分揀設施和設備/, "包裹旅程先改分揀"],
  [/合併文件生效那一天/, /這個地點數，沒有說全美網路/, "公司合併與路網進度"],
  [/地點數；它究竟量到什麼/, /開場問的地點數，量到的是/, "實施地點的口徑"],
  [/兩種時間表，要怎麼在路上/, /超過六百八十處分揀和配送設施/, "兩套網路的物理骨架"],
  [/這些設備會自己改走同一條路/, /這個地點數，沒有說全美網路/, "法律合併不等於現場完成"],
  [/可公司為什麼要在這時動/, /它說電商近年顯著成長/, "公司提出的改網背景"],
  [/第一段旅程會怎樣變/, /FedEx 計畫整併分揀設施和設備/, "先處理分揀"],
  [/城市之間的幹線，若仍各自安排/, /公司還要最佳化企業幹線/, "幹線也被納入"],
  [/地面配送員全換成同一種身分/, /未來仍會用雇員，也會用承包服務商/, "不會換成同一種司機"],
  [/現場先動，還是合併文件先生效/, /加拿大先開始分階段轉換/, "加拿大現場先動"],
  [/逐地安排究竟推進了多少/, /美加已有約二百九十處實施最佳化/, "次年實施範圍"],
  [/誰負責把箱子送到門口/, /有些地點將由服務商取件/, "逐市場配送者"],
  [/什麼可能卡住/, /後勤系統、現場做法和既有合約/, "整合風險中的後勤與合約"],
  [/哪個國家已把路網轉換走完/, /加拿大已完成這項網路計畫的實施/, "加拿大與美國進度分界"],
  [/美國約三百六十處實施；這就算完成嗎/, /仍預計到二〇二七曆年底/, "美國地點不等於完成"],
  [/站內包裹量變動，人手要怎麼跟上/, /引進動態排班/, "分揀人手跟著貨量"],
  [/服務商怎麼決定配送路線/, /接近即時的路線資料/, "服務商使用路線資料"],
];
const loops = loopPatterns.map(([setup, payoff, what]) => {
  const [a, aIndex] = find(setup);
  const [b, bIndex] = find(payoff, aIndex);
  if (aIndex >= bIndex) throw new Error(`Backward loop: ${what}`);
  return { setup: a, payoff: b, what };
});

const description = [
  "同樣叫 FedEx，2022 年報卻把 Express 和 Ground 列成不同公司與配送網。2023 年 FedEx 宣布 one FedEx；2024 年公司架構合併後，實體路線又花了多久調整？本集從 2022–2026 年 SEC 原始年報，追一件概念包裹背後的分揀、取件、幹線與配送。",
  "",
  "FY 指 FedEx 截至各年 5 月 31 日的財年。2024-06-01 是 Ground／Services 併入 Federal Express 的法律日期，不代表所有路線完成整合。FY2024 的 50 多處限美國；FY2025 約 290 處含美加，不能直接換算完成百分比。FY2025 申報亦稱加拿大已完成實施、美國約 130 地點；FY2026 美國約 360 地點，2027 曆年底完成仍是公司預期。FY2026 年報另載 2026-06-01 分拆的是零擔貨運 FedEx Freight，並非小包裹 Ground；這件事與本集的 Ground 路網合併不同。片中匿名插畫是概念示意，不是真實包裹追蹤、商標或現場畫面。資料查核日期：2026-10-20。",
  "",
  "一手資料（FedEx SEC 原始年報）",
  ...sourceUrls.flatMap(source => [source.title, source.url]),
].join("\n");
const video = {
  schema_version: 1, slug, format: "drama", category: "explainer", narration_locale: "zh-TW", target_minutes: [8, 12],
  voice: { provider: "gemini", name: "Sulafat", style: "標準國語，台灣自然口音。像向朋友講一個包裹網路的真實轉折；正常語速，日期和服務名稱讀清楚。", performance: "FY 財年與曆年、2024 法律合併與逐地網路轉換、FY2025 加拿大已完成與 FY2026 美國仍有預期日期的邊界必須清楚。" },
  subtitles: { burn_in: false }, look: { preset: "cute-mystery" }, characters: [],
  series: { slug: "brand-stories-everyday-reversals-extra", episode: 11, chapter: 1 },
  music: { prompt: "light, curious, a little mysterious, no vocals", gain_db: -20, duck_db: -10 },
  loops,
  youtube: { category_id: 27, made_for_kids: false, default_language: "zh-TW", title: "FedEx 明明同一品牌，快遞與地面包裹為何 2024 才合併？｜品牌故事", description, tags: ["FedEx", "聯邦快遞", "品牌故事", "包裹配送", "Express", "Ground", "物流"], video_id: null },
  thumbnail: { template: "thumb", data: { headline: "**兩張網？**", tag: "品牌故事", brand: "FedEx", shot: "x11-b01-s01" } },
  sources: sourceUrls, assets: [], scenes,
};
const bytes = JSON.stringify(video, null, 2) + "\n";
writeFileSync(path.join(dir, "video.json"), bytes);
const sha = createHash("sha256").update(bytes).digest("hex");
const esc = value => value.replaceAll("|", "\\|");
writeFileSync(path.join(dir, "line-source-matrix.md"), [
  "# X11 FedEx｜逐句來源矩陣", "", "由 `compose-video.mjs` 從 `drafts/narration.md` 生成。任何改稿須重編，重做來源審核與盲讀；代碼定義見 [source-matrix.md](source-matrix.md)。", "",
  `- \`video.json\` SHA-256：\`${sha}\``, "", "| 句 ID | 旁白 | 主張 |", "| --- | --- | --- |",
  ...rows.map(row => `| \`${row.id}\` | ${esc(row.text)} | ${row.refs.length ? row.refs.join("、") : "編輯示意／提問／CTA"} |`), "",
].join("\n"));
writeFileSync(path.join(dir, "script.md"), [
  "# X11 FedEx｜繁中逐句稿", "", `離線前製；\`video.json\` SHA-256：\`${sha}\`。首章、三句 CTA、5 秒片頭與 21 秒片尾不計入實質正文；正式 TTS 未實測。`, "",
  ...chapters.flatMap((chapter, ci) => [`## 第 ${ci + 1} 章｜${chapter.title}${ci === 0 ? "（濃縮開場）" : ""}`, "", ...chapter.rows.map((row, ri) => `- \`${idFor(ci, ri)}\` ${row.text}`), ""]),
].join("\n"));
writeFileSync(path.join(dir, "series.json"), JSON.stringify({ kind: "story", slug: "brand-stories-everyday-reversals-extra", episode: 11, chapter: 1, title: "FedEx：同牌兩張網，為何到 2024 才合併？", logline: "從 FY2022 分列的 Express／Ground，到 2024 法律合併與 FY2026 仍在逐地整合的實體網路。", names: ["FedEx", "Federal Express", "FedEx Express", "FedEx Ground", "FedEx Services", "FedEx Freight", "Network 2.0", "one FedEx", "Ground Economy", "Memphis", "Indianapolis"], characters: [], target_minutes: 10, image_model: "image-01", style_preset: "custom", look: { preset: "cute-mystery" }, visual_tier: "stills", compilation: false }, null, 2) + "\n");
const body = chapters.slice(1).flatMap(chapter => chapter.rows).slice(0, -3).map(row => row.text).join("");
console.log(JSON.stringify({ scenes: scenes.length, shots: scenes.filter(scene => scene.template === "shot").length, cards: scenes.filter(scene => scene.template === "stats").length, spoken_lines: rows.length, hook_characters: chapters[0].rows.map(row => row.text).join("").length, body_characters: body.length, body_estimate_minutes_at_300_cpm: +(body.length / 300).toFixed(2), loops: loops.length, video_sha256: sha }, null, 2));
