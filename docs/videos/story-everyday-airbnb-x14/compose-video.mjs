// Deterministic offline preproduction build. No host import or paid media call.
import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { textHash } from "../../../tools/video/core/schema.mjs";
import { visualCueCount, visualFor } from "./drafts/visual-cues.mjs";

const dir = path.dirname(fileURLToPath(import.meta.url));
const slug = "story-everyday-airbnb-x14";
const sourceUrls = [
  { title: "Airbnb 2020 Form 10-K", url: "https://www.sec.gov/Archives/edgar/data/1559720/000155972021000010/airbnb-10k.htm", checked_on: "2026-10-20" },
  { title: "Airbnb 2020 Q4 shareholder letter", url: "https://www.sec.gov/Archives/edgar/data/1559720/000119312521056952/d147144dex991.htm", checked_on: "2026-10-20" },
  { title: "Airbnb 2021 Q4 shareholder letter", url: "https://www.sec.gov/Archives/edgar/data/1559720/000119312522043371/d251410dex991.htm", checked_on: "2026-10-20" },
  { title: "Airbnb 2022 Q4 shareholder letter", url: "https://www.sec.gov/Archives/edgar/data/1559720/000119312523039008/d451233dex991.htm", checked_on: "2026-10-20" },
];
const chapters = [];
for (const raw of readFileSync(path.join(dir, "drafts/narration.md"), "utf8").split(/\r?\n/)) {
  const header = raw.match(/^## 第[一二三四五六]章｜(.+)$/);
  if (header) { chapters.push({ title: header[1].replace(/（濃縮開場.*$/, ""), rows: [] }); continue; }
  const row = raw.match(/^(.*?)\s+\[((?:A[1-4](?:,A[1-4])*|editorial))\]$/);
  if (!row) continue;
  if (!chapters.length) throw new Error(`Narration before chapter: ${raw}`);
  chapters.at(-1).rows.push({ text: row[1].trim(), refs: row[2] === "editorial" ? [] : row[2].split(",") });
}
if (chapters.length !== 6 || chapters.some(chapter => !chapter.rows.length)) throw new Error("Expected six nonempty chapters");
chapters.forEach((chapter, ci) => {
  if (visualCueCount(ci) !== chapter.rows.length) throw new Error(`Chapter ${ci + 1}: ${visualCueCount(ci)} cues vs ${chapter.rows.length} lines`);
});
const idFor = (ci, ri) => `x14${String(ci + 1).padStart(2, "0")}${String(ri + 1).padStart(2, "0")}`;
const rows = chapters.flatMap((chapter, ci) => chapter.rows.map((row, ri) => ({ ...row, id: idFor(ci, ri), chapter: ci + 1 })));
const find = (pattern, after = -1) => {
  const index = rows.findIndex((row, i) => i > after && pattern.test(row.text));
  if (index < 0) throw new Error(`Missing loop anchor: ${pattern}`);
  return [rows[index].id, index];
};
const loopPatterns = [
  [/房東原本的取消費怎麼算/, /基數是原取消政策/, "開場房東取消費的分母"],
  [/先動哪一筆資源/, /籌到二十億美元定期貸款/, "公司先取得周轉資金"],
  [/哪種可訂日子放到旅客眼前/, /網站和應用程式於是更突出附近/, "附近住宿的產品呈現"],
  [/數字能認出原來那些提供者嗎/, /無法對上同一批提供者/, "總量不是同批名冊"],
  [/最後還剩多少預訂/, /淨預訂夜晚與體驗席位是三點二六九億/, "全年淨預訂量"],
  [/怎麼寫進自己的收入/, /主要是向旅客和房東收的服務費/, "住宿訂單與平台收入"],
  [/每一淨預訂單位的總額也變小嗎/, /每一淨預訂單位對應的訂房總額增加/, "單位淨預訂價值的變化"],
  [/誰來處理它/, /基數是原取消政策/, "房東取消費的支援計算"],
  [/各拿到什麼/, /房東得到十元/, "旅客退款與房東支援"],
  [/房價的四分之一嗎/, /基數是原取消政策/, "房東支援的正確分母"],
  [/那一年的帳又記了什麼/, /兩億零五百一十萬美元/, "承諾上限與列帳付款不同"],
  [/剩下的房源要如何被看見/, /網站和應用程式於是更突出附近/, "近處住宿的產品呈現"],
  [/隔年旅客會怎樣把日曆重新填上/, /比例增加到百分之二十二/, "2021 住宿長度變化"],
  [/多少刊登項目開放這麼長的日期/, /超過九成活躍刊登項目接受二十八夜/, "長住可訂刊登項目"],
  [/當季損益又變了什麼/, /第四季，Airbnb 淨賺/, "2021 單季盈利"],
  [/這類長住會從整體比例消失嗎/, /仍占新訂夜晚百分之二十一/, "遠行恢復後的長住"],
  [/排回疫情前的樣子嗎/, /還沒回到原比例/, "旅行組合仍不同"],
  [/公司的取捨留下了什麼/, /淨利，約十九億美元/, "2022 首個全年盈利"],
  [/哪一步單獨帶來多少利潤嗎/, /財報拆不出各步盈利/, "單招盈利不可歸因"],
];
const loops = loopPatterns.map(([setup, payoff, what]) => {
  const [a, ai] = find(setup); const [b, bi] = find(payoff, ai);
  if (ai >= bi) throw new Error(`Backward loop: ${what}`);
  return { setup: a, payoff: b, what };
});

const card = (title, value, label, source) => ({ title, stats: [{ value, label }], source: `Airbnb ${source}` });
const cards = new Map([
  ["x140206", card("全年 net nights + experiences", "326.9m", "2019 全年", "2020 10-K")],
  ["x140207", card("全年 net nights + experiences", "193.2m", "2020 全年；比 2019 少 41%", "2020 10-K")],
  ["x140216", card("Airbnb 年度營收", "US$4.8bn → US$3.4bn", "2019 → 2020，非 GBV", "2020 10-K")],
  ["x140218", card("單位 net night + experience 的 GBV", "+6%", "非 Airbnb 服務費率", "2020 10-K")],
  ["x140306", card("合資格房東支援承諾", "≤US$250m", "上限，非實際付款", "2020 10-K")],
  ["x140313", card("房東支援計算基準", "25%", "原取消政策本可得金額", "2020 10-K")],
  ["x140315", card("純教學示例，非真實訂單", "40 → 10", "原政策可得額 → 新支援", "2020 10-K 計算規則")],
  ["x140321", card("2020 例外政策付款", "US$205.1m", "顧客付款；主要給房東；收入扣減", "2020 10-K")],
  ["x140402", card("2020 年 4 月", "US$2bn", "定期貸款，非營收", "2020 10-K")],
  ["x140405", card("2020 年 5 月", "~1,800", "減少全職員工，非房東", "2020 10-K")],
  ["x140420", card("年底活躍刊登項目", "~5.6m → ~5.6m", "2019 → 2020；含住宿或體驗", "2020 10-K")],
  ["x140424", card("2020 全年 GAAP 淨虧損", "~US$4.6bn", "含上市相關非現金費用", "2020 10-K")],
  ["x140425", card("2020 上市觸發股份費用", "~US$2.8bn", "非現金 RSU 費用", "2020 10-K")],
  ["x140502", card("2021 全年 net nights + experiences", "300.6m", "扣取消與更改後", "2021 Q4 shareholder letter")],
  ["x140504", card("2021 全年營收", "~US$6.0bn", "服務費等收入，非 GBV", "2021 Q4 shareholder letter")],
  ["x140508", card("28 夜以上占 Q4 gross nights", "16%", "2019 Q4", "2021 Q4 shareholder letter")],
  ["x140509", card("28 夜以上占 Q4 gross nights", "22%", "2021 Q4", "2021 Q4 shareholder letter")],
  ["x140514", card("2021 Q4 末活躍刊登項目", ">90%", "住宿或體驗；可接 ≥28 夜，非已入住", "2021 Q4 shareholder letter")],
  ["x140517", card("2021 Q4 淨利", "+US$55m", "單季，非全年", "2021 Q4 shareholder letter")],
  ["x140518", card("2021 全年淨損", "−US$352m", "全年，非 Q4", "2021 Q4 shareholder letter")],
  ["x140602", card("2022 全年 net nights + experiences", "393.7m", "扣取消與更改後", "2022 Q4 shareholder letter")],
  ["x140604", card("2022 全年營收", "~US$8.4bn", "非 GBV", "2022 Q4 shareholder letter")],
  ["x140605", card("年度營收變化", "~+40%", "2022 比 2021", "2022 Q4 shareholder letter")],
  ["x140608", card("28 夜以上占 Q4 gross nights", "21%", "2022 Q4", "2022 Q4 shareholder letter")],
  ["x140611", card("跨境占 Q4 gross nights", "47% → 44%", "2019 Q4 → 2022 Q4", "2022 Q4 shareholder letter")],
  ["x140615", card("2022 年底活躍刊登項目", "6.6m", "含住宿或體驗，非留存率", "2022 Q4 shareholder letter")],
  ["x140618", card("2022 首個 GAAP 盈利年", "~US$1.9bn", "全年淨利", "2022 Q4 shareholder letter")],
]);
const sayWords = [["GAAP", "一般公認會計原則"], ["IPO", "首次公開發行"], ["Airbnb", "愛彼迎"]];
function lineFor(id, value) {
  const line = { id, text: value, emotion: value.endsWith("？") ? "自然提問，尾音微上揚" : "台灣口語說書，清楚自然，正常語速" };
  const say = sayWords.reduce((current, [written, spoken]) => current.replaceAll(written, spoken), value);
  if (say !== value) Object.assign(line, { say, say_for: textHash(value) });
  return line;
}
const scenes = [];
for (const [ci, chapter] of chapters.entries()) {
  chapter.rows.forEach((row, ri) => {
    const card = cards.get(idFor(ci, ri));
    const scene = {
      id: `x14-b${String(ci + 1).padStart(2, "0")}-s${String(ri + 1).padStart(2, "0")}`,
      template: card ? "stats" : "shot",
      data: card ?? { ...visualFor(ci, ri), visual: "still" },
      lines: [lineFor(idFor(ci, ri), row.text)],
    };
    if (ri === 0) scene.chapter = chapter.title;
    scenes.push(scene);
  });
}
const closing = scenes.splice(-3, 3);
if (closing.some(scene => scene.template !== "shot" || scene.lines.length !== 1)) throw new Error("Closing CTA must be three solo shots");
scenes.push({ id: "x14-outro", template: "outro", data: { title: "一張日曆，兩端的生意", cta: "訂閱品牌故事" }, lines: closing.flatMap(scene => scene.lines) });
const description = [
  "2020 年三、四月合計，Airbnb 的取消夜晚與體驗席位超過同期新預訂；到了 2022 年卻首次按 GAAP 計算全年盈利。這支品牌故事從平台兩端的取消與支援、公司收縮、附近及長住需求，走到旅行恢復時的不同住宿組合。",
  "",
  "期間與分母：三、四月是合計比較，不代表兩個月份各自成立。2019、2020 年末約 560 萬活躍刊登項目是含住宿或體驗的總量，不能據此證明同一批房東留下或補助帶來留存。2021／2022 長住與跨境比例限各年 Q4 gross nights booked。2020 年 GAAP 淨虧損含 IPO 相關非現金費用，不是取消訂單的單一代價。片中日曆與匿名人物是概念示意，非真實個案。資料查核日期：2026-10-20。",
  "",
  "一手資料（Airbnb SEC 原始申報與股東信）",
  ...sourceUrls.flatMap(source => [source.title, source.url]),
].join("\n");
const video = {
  schema_version: 1, slug, format: "drama", category: "explainer", narration_locale: "zh-TW", target_minutes: [8, 12],
  voice: { provider: "gemini", name: "Sulafat", style: "標準國語、台灣自然口音。像向朋友說一個真實商業轉折；正常語速，日期和分母讀清楚。", performance: "三、四月合計與全年、gross 與 net、服務費收入與訂單總額、第四季與全年的差別要清楚。" },
  subtitles: { burn_in: false }, look: { preset: "cute-mystery" }, characters: [],
  series: { slug: "brand-stories-everyday-reversals-extra", episode: 14, chapter: 1 },
  music: { prompt: "light, curious, a little mysterious, no vocals", gain_db: -20, duck_db: -10 }, loops,
  youtube: { category_id: 27, made_for_kids: false, default_language: "zh-TW", title: "Airbnb：取消壓過預訂後，怎樣迎來首個盈利年？｜品牌故事", description, tags: ["Airbnb", "品牌故事", "房東", "旅遊", "長住", "商業史"], video_id: null },
  thumbnail: { template: "thumb", data: { headline: "取消比新訂多", tag: "品牌故事", brand: "Airbnb", shot: "x14-b01-s01" } },
  sources: sourceUrls, assets: [], scenes,
};
const videoBytes = JSON.stringify(video, null, 2) + "\n";
writeFileSync(path.join(dir, "video.json"), videoBytes);
const videoSha = createHash("sha256").update(videoBytes).digest("hex");
const esc = value => String(value).replaceAll("|", "\\|");
writeFileSync(path.join(dir, "line-source-matrix.md"), [
  "# X14 Airbnb｜逐句來源矩陣", "", `主片 SHA-256：\`${videoSha}\`。來源代碼見 \`source-matrix.md\`；編輯示意及提問不作事實證明。`, "",
  "| 句 ID | 旁白 | 來源 |", "| --- | --- | --- |",
  ...rows.map(row => `| \`${row.id}\` | ${esc(row.text)} | ${row.refs.length ? row.refs.join("、") : "編輯示意／提問／CTA"} |`), "",
].join("\n"));
writeFileSync(path.join(dir, "script.md"), [
  "# X14 Airbnb｜繁中逐句稿", "", `離線前製；\`video.json\` SHA-256：\`${videoSha}\`。首章、結尾三句、正式片頭和片尾不計入實質正文；正式 TTS 尚未測量。`, "",
  ...chapters.flatMap((chapter, ci) => [`## 第 ${ci + 1} 章｜${chapter.title}${ci === 0 ? "（濃縮開場）" : ""}`, "", ...chapter.rows.map((row, ri) => `- \`${idFor(ci, ri)}\` ${row.text}`), ""]),
].join("\n"));
writeFileSync(path.join(dir, "series.json"), JSON.stringify({ kind: "story", slug: "brand-stories-everyday-reversals-extra", episode: 14, chapter: 1, title: "Airbnb：取消壓過預訂後，怎樣迎來首個盈利年？", logline: "2020 年合計兩月的取消量超過同期新增預訂，Airbnb 如何在平台兩端、公司成本與旅行需求變化間走到 2022 首個盈利年。", names: ["Airbnb", "Superhost", "GAAP"], characters: [], target_minutes: 10, image_model: "image-01", style_preset: "custom", look: { preset: "cute-mystery" }, visual_tier: "stills", compilation: false }, null, 2) + "\n");
const body = chapters.slice(1).flatMap(chapter => chapter.rows).slice(0, -3).map(row => row.text).join("");
console.log(JSON.stringify({ scenes: scenes.length, shots: scenes.filter(scene => scene.template === "shot").length, cards: scenes.filter(scene => scene.template === "stats").length, spoken_lines: rows.length, hook_characters: chapters[0].rows.map(row => row.text).join("").length, body_characters: body.length, body_estimate_minutes_at_300_cpm: +(body.length / 300).toFixed(2), loops: loops.length, video_sha256: videoSha }, null, 2));
