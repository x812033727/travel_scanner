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
  [/旅客能退多少/, /全額現金退款路/, "示意旅客的條件式退款"],
  [/借款文件，金額還沒揭開/, /二十億美元定期貸款/, "四月貸款實際金額"],
  [/員工名冊，下一頁還沒翻/, /減少約一千八百名全職員工/, "五月員工決定"],
  [/哪類房源會先映入眼簾/, /附近、非都會住宿被放得更醒目/, "搜尋頁顯示方向"],
  [/哪個平台數字能證明新訂回來/, /三點九三七億；這才證明新訂回來/, "全片淨預訂量答案"],
  [/總額，能全算成 Airbnb 的收入嗎/, /主要是扣除優惠與退款後的兩端服務費/, "房價與平台收入"],
  [/兩端會卡在哪裡/, /房東可得十元支援/, "示意訂單的兩端結算"],
  [/壓過的究竟是哪一種量/, /同期還沒扣取消的新訂夜晚與體驗席位/, "兩月 gross 比較"],
  [/旅客拿回什麼，房東按哪筆錢算/, /房東可得十元支援/, "條件式退款和支援基準"],
  [/這位示意房東如何過關/, /條件齊了，才計算支援/, "房東支援資格"],
  [/房價的四分之一嗎/, /分母是房東按原取消政策本可收到的費用/, "房東支援分母"],
  [/全年的例外付款又記了多少/, /全年兩億零五百一十萬美元/, "例外政策記帳金額"],
  [/下一段日期可訂，就等於有人訂嗎/, /新的旅客還沒按下預訂/, "可訂與實際訂成"],
  [/員工名冊會變成什麼決定/, /減少約一千八百名全職員工/, "五月縮編"],
  [/哪一種可訂格先有機會被點開/, /附近、非都會住宿被放得更醒目/, "附近住宿展示"],
  [/春天那個空格因此就補上了嗎/, /不保證有人拿走它/, "搜尋展示不保證成交"],
  [/能說明原來那批房東都還在嗎/, /總量算不出那把示意鑰匙/, "刊登總量不能推出留存"],
  [/能認出這張示意房東的下一筆訂單嗎/, /沒有追蹤個別房東/, "年度總量不能識別個案"],
  [/旅客一次選幾晚/, /比例到了百分之二十二/, "長住占比"],
  [/其他房東也能嗎/, /超過九成活躍刊登項目可接受二十八夜/, "長住可訂設定"],
  [/長住會從預訂組合裡消失嗎/, /長住仍占新訂夜晚百分之二十一/, "2022 長住"],
  [/跨境那條路，回到疫情前的位置了嗎/, /二〇一九年同季是百分之四十七/, "跨境尚未回到舊比例"],
  [/會讓公司整年都賺錢嗎/, /首次按 GAAP 計算全年盈利/, "2022 全年盈利"],
  [/真正新增了多少已訂夜晚與體驗席位/, /三點九三七億；這才證明新訂回來/, "已訂總量而非可訂供給"],
];
const loops = loopPatterns.map(([setup, payoff, what]) => {
  const [a, ai] = find(setup); const [b, bi] = find(payoff, ai);
  if (ai >= bi) throw new Error(`Backward loop: ${what}`);
  return { setup: a, payoff: b, what };
});

const card = (title, value, label, source) => ({ title, stats: [{ value, label }], source: `Airbnb ${source}` });
const cards = new Map([
  ["x140305", card("合資格房東支援承諾", "≤US$250m", "上限，非實際付款", "2020 10-K")],
  ["x140312", card("房東支援計算基準", "25%", "原取消政策本可得金額", "2020 10-K")],
  ["x140314", card("假設房東支援｜非真實訂單", "40 → 10", "房東原取消費 → 房東支援", "2020 10-K 計算規則")],
  ["x140317", card("2020 例外政策付款", "US$205.1m", "公司付予顧客，主要給房東；營收扣減", "2020 10-K")],
  ["x140402", card("2020 年 4 月", "US$2bn", "定期貸款，非營收", "2020 10-K")],
  ["x140405", card("2020 年 5 月", "~1,800", "減少全職員工，非房東", "2020 10-K")],
  ["x140419", card("年底活躍刊登項目", "~5.6m → ~5.6m", "2019 → 2020；含住宿或體驗", "2020 10-K")],
  ["x140423", card("全年 net nights + experiences", "326.9m → 193.2m", "2019 → 2020；少 41%", "2020 10-K")],
  ["x140502", card("2021 全年 net nights + experiences", "300.6m", "扣取消與更改後", "2021 Q4 shareholder letter")],
  ["x140506", card("28 夜以上占 Q4 gross nights", "16%", "2019 Q4", "2021 Q4 shareholder letter")],
  ["x140507", card("28 夜以上占 Q4 gross nights", "22%", "2021 Q4", "2021 Q4 shareholder letter")],
  ["x140512", card("2021 Q4 末長住可訂設定", ">90%", "公司活躍刊登項目口徑；≥28 夜為住宿預訂，非已入住", "2021 Q4 shareholder letter")],
  ["x140516", card("2021 季與年不是同一件事", "Q4 +US$55m / FY −US$352m", "第四季單季淨利／全年淨虧", "2021 Q4 shareholder letter")],
  ["x140605", card("28 夜以上占 Q4 gross nights", "21%", "2022 Q4", "2022 Q4 shareholder letter")],
  ["x140609", card("跨境占 Q4 gross nights", "47% → 44%", "2019 Q4 → 2022 Q4", "2022 Q4 shareholder letter")],
  ["x140614", card("2022 首個 GAAP 盈利年", "~US$1.9bn", "全年淨利", "2022 Q4 shareholder letter")],
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
scenes.push({ id: "x14-outro", template: "outro", data: { title: "一張日曆，兩端的生意", lines: ["2022 全年淨預訂：393.7m", "夜晚＋體驗席位；已扣取消與改訂"], cta: "訂閱品牌故事" }, lines: closing.flatMap(scene => scene.lines) });
const description = [
  "2020 年三、四月合計，Airbnb 的取消夜晚與體驗席位超過同期新預訂；到了 2022 年卻首次按 GAAP 計算全年盈利。這支品牌故事從一筆明示為假設的取消單出發，按條件算旅客退款和房東支援，追蹤借款縮支、附近與長住需求，最後以全年淨預訂量檢驗新訂是否回來。不宣稱同一位旅客或房東後來有新訂。",
  "",
  "期間與分母：三、四月是合計比較，不代表兩個月份各自成立。2019、2020 年末約 560 萬活躍刊登項目是含住宿或體驗的總量，不能據此證明同一批房東留下或補助帶來留存。2021／2022 長住與跨境比例限各年 Q4 gross nights booked。2020 年 GAAP 淨虧損含 IPO 相關非現金費用，不是取消訂單的單一代價。片中假設 2020 年 3 月 10 日下訂、3 月 30 日入住、3 月 20 日因疫情取消，以及房價 100／原取消費 40／支援 10 的算例，均非真實個案，仍須各自符合政策。資料查核日期：2026-10-20。",
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
  youtube: { category_id: 27, made_for_kids: false, default_language: "zh-TW", title: "Airbnb：取消壓過新訂後，怎麼證明預訂回來了？｜品牌故事", description, tags: ["Airbnb", "品牌故事", "房東", "旅遊", "長住", "商業史"], video_id: null },
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
writeFileSync(path.join(dir, "series.json"), JSON.stringify({ kind: "story", slug: "brand-stories-everyday-reversals-extra", episode: 14, chapter: 1, title: "Airbnb：取消壓過新訂後，怎麼證明預訂回來了？", logline: "2020 年合計兩月的取消量超過同期新增預訂；一張假設日曆先走完退款與房東支援的條件，再用全平台淨預訂量證明其後新訂回來。", names: ["Airbnb", "Superhost", "GAAP"], characters: [], target_minutes: 10, image_model: "image-01", style_preset: "custom", look: { preset: "cute-mystery" }, visual_tier: "stills", compilation: false }, null, 2) + "\n");
const body = chapters.slice(1).flatMap(chapter => chapter.rows).slice(0, -3).map(row => row.text).join("");
console.log(JSON.stringify({ scenes: scenes.length, shots: scenes.filter(scene => scene.template === "shot").length, cards: scenes.filter(scene => scene.template === "stats").length, spoken_lines: rows.length, hook_characters: chapters[0].rows.map(row => row.text).join("").length, body_characters: body.length, body_estimate_minutes_at_300_cpm: +(body.length / 300).toFixed(2), loops: loops.length, video_sha256: videoSha }, null, 2));
