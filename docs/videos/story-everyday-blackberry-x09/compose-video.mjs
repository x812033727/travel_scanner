// Deterministic offline preproduction build: no media-provider calls or story import.
import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { textHash } from "../../../tools/video/core/schema.mjs";
import { visualFor, visualCueCount } from "./drafts/visual-cues.mjs";

const dir = path.dirname(fileURLToPath(import.meta.url));
const slug = "story-everyday-blackberry-x09";
const sourceUrls = [
  { title: "BlackBerry FY2015 40-F AIF", url: "https://www.sec.gov/Archives/edgar/data/1070235/000107023515000029/bbry-02282015x40fexhibit11.htm", checked_on: "2026-10-20" },
  { title: "BlackBerry FY2017 40-F AIF", url: "https://www.sec.gov/Archives/edgar/data/1070235/000107023517000008/bbry-02282017x40fexhibit11.htm", checked_on: "2026-10-20" },
  { title: "BlackBerry FY2017 40-F MD&A", url: "https://www.sec.gov/Archives/edgar/data/1070235/000107023517000008/bbry-02282017x40fexhibit13.htm", checked_on: "2026-10-20" },
  { title: "BlackBerry FY2018 40-F MD&A", url: "https://www.sec.gov/Archives/edgar/data/1070235/000107023518000007/bb-02282018x40fexhibit13.htm", checked_on: "2026-10-20" },
  { title: "BlackBerry FY2020 Form 10-K", url: "https://www.sec.gov/Archives/edgar/data/1070235/000107023520000025/bbry-20200229.htm", checked_on: "2026-10-20" },
];

const chapters = [];
for (const raw of readFileSync(path.join(dir, "drafts/narration.md"), "utf8").split(/\r?\n/)) {
  const header = raw.match(/^## 第[一二三四五六]章｜(.+)$/);
  if (header) { chapters.push({ title: header[1].replace(/（濃縮開場.*$/, ""), rows: [] }); continue; }
  if (raw.startsWith("## 來源標記")) break;
  const row = raw.match(/^(.*?)\s+\[((?:B\d+(?:,B\d+)*|editorial))\]$/);
  if (!row) continue;
  if (!chapters.length) throw new Error(`Narration before chapter: ${raw}`);
  chapters.at(-1).rows.push({ text: row[1].trim(), refs: row[2] === "editorial" ? [] : row[2].split(",") });
}
if (chapters.length !== 6 || chapters.some(chapter => !chapter.rows.length)) throw new Error("Expected six nonempty chapters");
chapters.forEach((chapter, ci) => {
  if (visualCueCount(ci) !== chapter.rows.length) throw new Error(`Chapter ${ci + 1}: ${visualCueCount(ci)} visual cues vs ${chapter.rows.length} lines`);
});

const cardFor = value => {
  if (/八億八千四百萬/.test(value)) return { title: "FY2016 → FY2017｜硬體及其他收入", stats: [{ value: "US$884m → 374m", label: "收入，非手機銷量" }], source: "BlackBerry FY2017 MD&A" };
  if (/七億七千九百萬/.test(value)) return { title: "FY2016 → FY2017｜舊服務接入費", stats: [{ value: "US$779m → 313m", label: "BB7 與更舊系統為主" }], source: "BlackBerry FY2017 MD&A" };
  if (/四億九千七百萬/.test(value)) return { title: "FY2016 → FY2017｜軟體及服務", stats: [{ value: "US$497m → 622m", label: "財報中的收入類別" }], source: "BlackBerry FY2017 MD&A" };
  if (/約二十二億/.test(value)) return { title: "FY2016 → FY2017｜合併收入", stats: [{ value: "約 US$2.2b → 1.3b", label: "各收入類別相加後的總額" }], source: "BlackBerry FY2017 MD&A" };
  if (/二〇一八財年，BlackBerry 自有手持設備收入降到六千四百萬/.test(value)) return { title: "FY2018｜公司自有手持設備收入", stats: [{ value: "US$64m", label: "收入，非手機出貨支數" }], source: "BlackBerry FY2018 MD&A" };
  if (/第四季，這條收入從前一年同期的五千五百萬/.test(value)) return { title: "FY2017 Q4 → FY2018 Q4｜自有手持設備收入", stats: [{ value: "US$55m → 2m", label: "季度收入，非授權夥伴手機銷量" }], source: "BlackBerry FY2018 MD&A" };
  if (/BlackBerry 合併收入仍降到九億三千二百萬/.test(value)) return { title: "FY2018｜合併收入", stats: [{ value: "US$932m", label: "GAAP 總收入，非手機銷量" }], source: "BlackBerry FY2018 MD&A" };
  if (/授權、智慧財產與其他收入增加七千萬/.test(value)) return { title: "FY2018｜授權、IP 與其他", stats: [{ value: "US$196m", label: "較 FY2017 +US$70m；混合類別" }], source: "BlackBerry FY2018 MD&A" };
  return null;
};

const pronunciation = [
  ["BlackBerry KEYone", "黑莓 Key One"], ["BlackBerry", "黑莓"],
  ["KEYone", "Key One"], ["Foxconn", "富士康"], ["BES12", "B E S 十二"],
  ["DTEK50", "D T E K 五十"], ["DTEK60", "D T E K 六十"],
];
function lineFor(id, value) {
  const line = { id, text: value, emotion: value.endsWith("？") ? "自然提問，尾音微上揚" : "台灣口語說書，清楚自然，正常語速" };
  const say = pronunciation.reduce((current, [written, spoken]) => current.replaceAll(written, spoken), value);
  if (say !== value) Object.assign(line, { say, say_for: textHash(value) });
  return line;
}

const rows = chapters.flatMap((chapter, ci) => chapter.rows.map((row, ri) => ({ ...row, id: `x09${String(ci + 1).padStart(2, "0")}${String(ri + 1).padStart(2, "0")}`, chapter: ci + 1 })));
const scenes = chapters.flatMap((chapter, ci) => chapter.rows.map((row, ri) => {
  const id = `x09-b${String(ci + 1).padStart(2, "0")}-s${String(ri + 1).padStart(2, "0")}`;
  const card = cardFor(row.text);
  const line = lineFor(rows.find(item => item.chapter === ci + 1 && item.text === row.text)?.id ?? `x09${String(ci + 1).padStart(2, "0")}${String(ri + 1).padStart(2, "0")}`, row.text);
  const scene = { id, template: card ? "stats" : "shot", data: card ?? { ...visualFor(ci, ri), visual: "still" }, lines: [line] };
  if (ri === 0) scene.chapter = chapter.title;
  return scene;
}));

const ending = scenes.splice(-3, 3);
if (ending.some(scene => scene.template !== "shot")) throw new Error("Closing three lines must be shots");
scenes.push({ id: "x09-outro", template: "outro", data: { title: "品牌還在，硬體誰做？", cta: "訂閱品牌故事" }, lines: ending.flatMap(scene => scene.lines) });

const find = (pattern, after = -1) => {
  const index = rows.findIndex((row, i) => i > after && pattern.test(row.text));
  if (index < 0) throw new Error(`Missing loop anchor ${pattern}`);
  return [rows[index].id, index];
};
const loopPatterns = [
  [/那批手機做完後/, /Foxconn 製造的手機，仍由 BlackBerry 買進/, "舊代工的買賣責任"],
  [/手機庫存又會怎樣/, /這批庫存不再補貨/, "交接後的舊庫存"],
  [/設計、銷售與客服/, /這次，新品牌手機的設計、製造、銷售和客服/, "KEYone 背後的工作"],
  [/收入又從哪裡來/, /若夥伴銷量超過約定最低量/, "品牌手機的授權收入"],
  [/工作和帳本為什麼要換人/, /所以可推得：舊收入變薄時/, "轉換分工與庫存風險"],
  [/只收一筆品牌費/, /Foxconn 製造的手機，仍由 BlackBerry 買進/, "Foxconn 合作不是純授權"],
  [/工廠，還是買賣責任/, /這次，新品牌手機的設計、製造、銷售和客服/, "代工到授權的差異"],
  [/手機那欄會先怎麼變/, /二〇一七財年的「硬體及其他」收入/, "自有硬體收入下滑"],
  [/另一條舊收入能補住這道缺口/, /服務接入費，從七億七千九百萬/, "舊服務費亦下滑"],
  [/軟體，能補上兩處缺口/, /合併總收入，仍從約二十二億/, "軟體增長不足抵銷"],
  [/誰扛買賣責任/, /這次，新品牌手機的設計、製造、銷售和客服/, "新機的責任人"],
  [/BlackBerry 自己留下什麼/, /BlackBerry 授權的是安全軟體、服務套件/, "黑莓保留的商品"],
  [/品牌風險會跟著消失/, /公司警告，夥伴若違反標準/, "品牌風險"],
  [/隔年自有手持設備收入會怎麼走/, /二〇一八財年，BlackBerry 自有手持設備收入降到六千四百萬/, "交接後的自有手機帳"],
  [/手機本體的收入又從哪裡來/, /轉型期間的手機本體收入，來自/, "剩餘庫存來源"],
  [/品牌手機真的不再出現/, /列出 KEYone，和另外兩款已推出的授權品牌手機/, "品牌手機仍推出"],
  [/那授權一欄能說明多少/, /不能把這個混合欄位的成長/, "混合授權收入來源"],
  [/授權收入，究竟如何進帳/, /若夥伴銷量超過約定最低量/, "手機授權收入認列"],
  [/跨過門檻與沒跨過時/, /若夥伴銷量超過約定最低量/, "手機授權條件"],
];
const loops = loopPatterns.map(([setup, payoff, what]) => {
  const [a, aIndex] = find(setup);
  const [b, bIndex] = find(payoff, aIndex);
  if (aIndex >= bIndex) throw new Error(`Backward loop ${what}`);
  return { setup: a, payoff: b, what };
});

const description = [
  "2017 年，TCL 宣布帶實體鍵盤的 BlackBerry KEYone。幾年前 Foxconn 也替黑莓做過手機，但那批手機由 BlackBerry 買進轉賣；新一輪授權到底換掉了哪段工作？本集用 FY2015、FY2017、FY2018 和 FY2020 的 BlackBerry SEC 原始申報，追公司自有庫存與品牌手機授權的分界。",
  "",
  "FY2017 指截至 2017-02-28 的會計年度；KEYone 年報預計 FY2018 第一季開始供貨。FY2017 既有 DTEK 等裝置仍在銷售，並曾預告可能有一款公司設計、第三方製造的未來手機；轉型不是一天內全停售。FY2016→17 軟服增長主要受 Good Technology、AtHoc 併購帶動。FY2018 自有手持設備收入 US$374m→64m，屬 BlackBerry 舊庫存、配件和修理等收入，非 KEYone 的銷售額；Licensing, IP and Other 的增額主要有 Teletry 及先前 IP 授權，不能全歸手機授權。插畫為匿名概念示意，非真實手機、商標或現場影像。資料查核日期：2026-10-20。",
  "",
  "一手資料（BlackBerry SEC 原始申報）",
  ...sourceUrls.flatMap(source => [source.title, source.url]),
].join("\n");

const video = {
  schema_version: 1, slug, format: "drama", category: "explainer", narration_locale: "zh-TW", target_minutes: [8, 12],
  voice: { provider: "gemini", name: "Sulafat", style: "標準國語，台灣自然口音。像對朋友講一個品牌分工的真實轉折；英文專名和財報數字讀清楚，停頓自然，不刻意放慢。", performance: "FY2017、FY2018 的財年和曆年分清楚；公司自有設備收入與夥伴銷量分開；授權收入認列不可讀成現金收取。" },
  subtitles: { burn_in: false }, look: { preset: "cute-mystery" }, characters: [],
  series: { slug: "brand-stories-everyday-reversals-extra", episode: 9, chapter: 1 },
  music: { prompt: "light, curious, a little mysterious, no vocals", gain_db: -20, duck_db: -10 },
  loops,
  youtube: { category_id: 27, made_for_kids: false, default_language: "zh-TW", title: "BlackBerry KEYone 是誰做的？黑莓為何交出手機硬體｜品牌故事", description, tags: ["BlackBerry", "黑莓", "KEYone", "品牌故事", "手機", "企業轉型", "品牌授權"], video_id: null },
  thumbnail: { template: "thumb", data: { headline: "**誰在做？**", tag: "品牌故事", brand: "BlackBerry", shot: "x09-b01-s03" } },
  sources: sourceUrls, assets: [], scenes,
};
const bytes = JSON.stringify(video, null, 2) + "\n";
writeFileSync(path.join(dir, "video.json"), bytes);
const sha = createHash("sha256").update(bytes).digest("hex");
const esc = value => value.replaceAll("|", "\\|");
writeFileSync(path.join(dir, "line-source-matrix.md"), [
  "# X09 BlackBerry｜逐句來源矩陣", "", "由 `compose-video.mjs` 從 `drafts/narration.md` 生成。任何改稿須重編，重做來源與盲審。主張定義見 [source-matrix.md](source-matrix.md)。", "",
  `- \`video.json\` SHA-256：\`${sha}\``, "", "| 句 ID | 旁白 | 主張 |", "| --- | --- | --- |",
  ...rows.map(row => `| \`${row.id}\` | ${esc(row.text)} | ${row.refs.length ? row.refs.join("、") : "編輯問句／CTA"} |`), "",
].join("\n"));
writeFileSync(path.join(dir, "script.md"), [
  "# X09 BlackBerry｜繁中逐句稿", "", `離線前製；\`video.json\` SHA-256：\`${sha}\`。片頭片尾與最後三句不計入實質正文，正式 TTS 尚未實測。`, "",
  ...chapters.flatMap((chapter, ci) => [`## 第 ${ci + 1} 章｜${chapter.title}${ci === 0 ? "（濃縮開場）" : ""}`, "", ...chapter.rows.map((row, ri) => `- \`x09${String(ci + 1).padStart(2, "0")}${String(ri + 1).padStart(2, "0")}\` ${row.text}`), ""]),
].join("\n"));
writeFileSync(path.join(dir, "series.json"), JSON.stringify({ kind: "story", slug: "brand-stories-everyday-reversals-extra", episode: 9, chapter: 1, title: "BlackBerry：品牌還在，誰做硬體？", logline: "從 FY2015 買入轉售 Foxconn 製手機，到 FY2017 合作夥伴宣布 KEYone，再看 FY2018 舊庫存不補與後來的授權收入規則。", names: ["BlackBerry", "KEYone", "TCL", "Optiemus", "PT BB Merah Putih", "Foxconn", "BES12", "Classic", "Passport", "Android", "Windows Phone", "Good Technology", "AtHoc", "DTEK50", "DTEK60", "Aurora", "Motion", "Teletry"], characters: [], target_minutes: 10, image_model: "image-01", style_preset: "custom", look: { preset: "cute-mystery" }, visual_tier: "stills", compilation: false }, null, 2) + "\n");
const body = chapters.slice(1).flatMap(chapter => chapter.rows).slice(0, -3).map(row => row.text).join("");
console.log(JSON.stringify({ scenes: scenes.length, shots: scenes.filter(scene => scene.template === "shot").length, cards: scenes.filter(scene => scene.template === "stats").length, spoken_lines: rows.length, hook_characters: chapters[0].rows.map(row => row.text).join("").length, body_characters: body.length, body_estimate_minutes_at_250_cpm: +(body.length / 250).toFixed(2), body_estimate_minutes_at_300_cpm: +(body.length / 300).toFixed(2), loops: loops.length, video_sha256: sha }, null, 2));
