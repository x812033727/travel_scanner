// Compose the X05 source-bound draft into a reviewable video package.
// Any change to the TSV changes the video hash and requires fresh review.
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { textHash } from "../../../tools/video/core/schema.mjs";

const dir = path.dirname(fileURLToPath(import.meta.url));
const slug = "story-everyday-meta-x05";
const rows = readFileSync(path.join(dir, "drafts/lines.tsv"), "utf8").trimEnd().split(/\r?\n/);
assert.equal(rows.shift(), "chapter\tline_id\ttext\tsources\tvisual");
const draft = rows.map((row) => {
  const parts = row.split("\t");
  assert.equal(parts.length, 5, "each draft row needs chapter, id, text, source, visual");
  const [chapter, id, text, refs, visual] = parts;
  assert.match(chapter, /^[1-6]$/);
  assert.match(id, /^m05\d{4}$/);
  assert.ok(text.length && visual.length);
  const sources = refs.split(";");
  assert.ok(sources.every((source) => ["M21", "M22", "M23", "M25", "editorial"].includes(source)));
  return { chapter: Number(chapter), id, text, sources, visual };
});
assert.equal(draft.length, 84);
assert.equal(new Set(draft.map(({ id }) => id)).size, draft.length);
assert.deepEqual([1, 2, 3, 4, 5, 6].map((chapter) => draft.filter((row) => row.chapter === chapter).length), [7, 13, 16, 19, 14, 15]);
assert.ok(draft.every((row, index) => index === 0 || row.chapter >= draft[index - 1].chapter));

const millions = "百萬美元｜營業損益";
const card = (title, stats, source) => ({ title, stats: stats.map(([value, label]) => ({ value, label })), source });
const M21 = "Meta FY2021 Form 10-K，Segment profitability";
const M22 = "Meta FY2022 Form 10-K，Segment profitability";
const M23 = "Meta FY2023 Form 10-K，Segment profitability";
const M25 = "Meta FY2025 Form 10-K，Segment profitability";
const cards = {
  m050101: card("FY2025｜RL 營業虧損", [["−19,193", millions]], M25),
  m050212: card("FY2021｜同年的兩欄", [["+56,946", "FoA 營業利益｜百萬美元"], ["−10,193", "RL 營業虧損｜百萬美元"], ["= +46,753", "全公司營業利益｜百萬美元"]], M21),
  m050303: card("FY2022｜廣告量、價與收入", [["+18%", "廣告送達數｜相較 FY2021"], ["−16%", "平均每則廣告價格｜相較 FY2021"], ["−1%", "廣告收入約減 12.9 億美元"]], "Meta FY2022 Form 10-K，Revenue / Advertising"),
  m050305: card("FY2022｜FoA 成本與費用", [["+22%", "相較 FY2021"], ["+13,080", "增加額｜百萬美元"]], "Meta FY2022 Form 10-K，Consolidated and Segment Results"),
  m050306: card("FY2022｜FoA 營業利益", [["+42,661", millions], ["−25%", "相較 FY2021"]], M22),
  m050316: card("FY2022｜重組費用", [["4,611", "公司總額｜百萬美元"], ["約 41 億美元", "其中認列於 FoA｜年報約數"]], "Meta FY2022 Form 10-K，Consolidated and Segment Results"),
  m050314: card("FY2022｜兩欄合計", [["+42,661", "FoA 營業利益｜百萬美元"], ["−13,717", "RL 營業虧損｜百萬美元"], ["= +28,944", "全公司營業利益｜百萬美元"]], M22),
  m050401: card("FY2023｜廣告送達數", [["+28%", "相較 FY2022"]], "Meta FY2023 Form 10-K，Revenue / Advertising"),
  m050403: card("FY2023｜量與價的結果", [["−9%", "平均每則廣告價格｜相較 FY2022"], ["+16%", "廣告收入｜相較 FY2022"]], "Meta FY2023 Form 10-K，Revenue / Advertising"),
  m050405: card("FY2023｜FoA 營業利益回升", [["+62,871", millions], ["+47%", "相較 FY2022"]], M23),
  m050407: card("FY2023｜RL 營業虧損", [["−16,120", millions], ["+2,403", "虧損幅度增加｜百萬美元"]], M23),
  m050409: card("FY2023｜RL 收入變化", [["−263", "百萬美元｜相較 FY2022"], ["−12%", "相較 FY2022"]], "Meta FY2023 Form 10-K，Reality Labs (RL)"),
  m050501: card("公司營業利益｜兩個端點", [["+46,753", "FY2021｜百萬美元"], ["+46,751", "FY2023｜百萬美元"], ["−2", "兩年差額｜百萬美元"]], "Meta FY2021／FY2023 Form 10-K，Segment profitability"),
  m050507: card("FY2023→FY2025｜兩個分部的端點差", [["+39,598", "FoA 營業利益增加｜百萬美元"], ["+3,073", "RL 虧損幅度擴大｜百萬美元"]], "Meta FY2023／FY2025 Form 10-K，Segment profitability"),
  m050510: card("FY2025｜FoA 營業利益變化", [["約 +153.6 億美元", "相較 FY2024"], ["+18%", "相較 FY2024"]], M25),
  m050604: card("FY2025｜RL 營業虧損變化", [["約 +14.6 億美元", "虧損幅度｜相較 FY2024"]], M25),
  m050611: card("Meta 的公司層級說明", [["仰賴其他業務足夠利潤", "推進下一代運算平台｜年報原文意旨"]], "Meta FY2025 Form 10-K，Revenue and Investments"),
  m050614: card("FY2025｜同年同口徑的答案", [["+102,469", "FoA 營業利益｜百萬美元"], ["−19,193", "RL 營業虧損｜百萬美元"], ["= +83,276", "全公司營業利益｜百萬美元"]], M25),
};
assert.deepEqual(draft.filter((row) => row.visual === "CARD").map((row) => row.id).sort(), Object.keys(cards).sort());

const chapters = [
  "四張帳頁，先把答案蓋住",
  "二〇二一年，年報改按兩個部門列報",
  "二〇二二年，量價與成本一起改寫正項",
  "二〇二三年，廣告回升而 RL 虧損加深",
  "相似的端點藏著二〇二二年的低谷",
  "二〇二五年，收入、成本與最後答案",
];
const sayText = (text) => text
  .replaceAll("Ray-Ban Display", "雷朋顯示眼鏡")
  .replaceAll("Reels", "瑞爾斯")
  .replaceAll("Meta Platforms, Inc.", "美塔平台公司")
  .replaceAll("Facebook, Inc.", "臉書公司")
  .replaceAll("Meta Quest", "美塔奎斯特")
  .replaceAll("Reality Labs", "實境實驗室")
  .replaceAll("Family of Apps", "應用程式家族")
  .replaceAll("Instagram", "英斯塔格蘭姆")
  .replaceAll("Messenger", "美森傑")
  .replaceAll("WhatsApp", "瓦次艾普")
  .replaceAll("Facebook", "臉書")
  .replaceAll("Meta", "美塔")
  .replaceAll("Quest", "奎斯特")
  .replaceAll("FoA", "艾夫歐欸")
  .replaceAll("RL", "阿爾艾爾")
  .replaceAll("AI", "人工智慧");
const count = new Map();
const scenes = draft.map((row) => {
  const nth = (count.get(row.chapter) ?? 0) + 1;
  count.set(row.chapter, nth);
  const scene = {
    id: `x05-b${String(row.chapter).padStart(2, "0")}-s${String(nth).padStart(2, "0")}`,
    template: row.visual === "CARD" ? "stats" : "shot",
    data: row.visual === "CARD" ? cards[row.id] : {
      prompt: row.visual,
      camera: ["push in", "pan right", "static", "tilt down", "pan left", "drift"][(nth + row.chapter) % 6],
      visual: "still",
    },
    lines: [(() => {
      const line = { id: row.id, text: row.text, emotion: row.text.endsWith("？") ? "問句上揚，停半拍" : "說書語氣，自然有起伏" };
      if (/[A-Za-z]/.test(row.text)) {
        const say = sayText(row.text);
        assert.ok(!/[A-Za-z]/.test(say), `unreviewed Latin speech in ${row.id}: ${say}`);
        line.say = say;
        line.say_for = textHash(row.text);
      }
      return line;
    })()],
  };
  if (nth === 1) scene.chapter = chapters[row.chapter - 1];
  return scene;
});

const positions = new Map(draft.map((row, index) => [row.id, index]));
const loop = (setup, payoff, what) => {
  assert.ok(positions.has(setup) && positions.has(payoff) && positions.get(setup) < positions.get(payoff));
  return { setup, payoff, what };
};
const loops = [
  loop("m050101", "m050614", "FY2025 RL 營業虧損與公司營業利益的同年答案"),
  loop("m050103", "m050303", "FY2022 廣告送達數與平均價格的兩種刻度"),
  loop("m050104", "m050308", "FY2022 裁員公告與年底公司人數的反差"),
  loop("m050105", "m050419", "FY2023 裁員公告與年底名冊變化"),
  loop("m050106", "m050601", "FY2025 眼鏡與 Quest 銷售方向的揭露"),
  loop("m050106", "m050604", "FY2025 兩類裝置銷售與 RL 整欄虧損方向的對照"),
  loop("m050107", "m050614", "一個部門虧損而整家公司營業利益為正"),
  loop("m050206", "m050212", "FY2021 公司合計由兩個部門結果相加"),
  loop("m050209", "m050212", "FoA 利益是否足以蓋過 RL 虧損"),
  loop("m050213", "m050314", "FY2022 廣告與成本變化後的公司合計"),
  loop("m050314", "m050412", "FY2022 公司營業利益低谷與隔年能否守住"),
  loop("m050304", "m050306", "FoA 收入小降與營業利益明顯下跌的差距"),
  loop("m050307", "m050308", "裁員公告與 FY2022 年底人數口徑的表面矛盾"),
  loop("m050310", "m050313", "RL 庫存成本下降能否抵住其他費用"),
  loop("m050309", "m050316", "FY2022 資料中心決定與重組費用"),
  loop("m050406", "m050407", "FY2023 RL 虧損是否跟著 FoA 改善"),
  loop("m050409", "m050410", "FY2023 RL 收入下降與 Meta Quest 銷量"),
  loop("m050422", "m050420", "FY2023 年末人數下降後行銷與銷售費用是否也下降"),
  loop("m050411", "m050412", "FY2023 公司合計是否離開低谷"),
  loop("m050415", "m050501", "FY2021 與 FY2023 精確公司合計的差額"),
  loop("m050505", "m050507", "FY2025 兩欄端點變化是否仍近乎相抵"),
  loop("m050509", "m050510", "FY2025 FoA 廣告收入能否跑過費用"),
  loop("m050516", "m050510", "FY2025 廣告量價同升與 FoA 營業利益增加"),
  loop("m050513", "m050609", "RL 產品收入類別與單品損益能否混算"),
  loop("m050605", "m050609", "RL 分部虧損能否歸到單一產品"),
  loop("m050610", "m050611", "長期研發需其他業務獲利支持的條件"),
  loop("m050613", "m050614", "FY2025 兩個部門放回同一張表的精確合計"),
];

const checkedOn = "2026-10-20";
const sources = [
  { title: "Meta FY2021 Form 10-K", url: "https://www.sec.gov/Archives/edgar/data/1326801/000132680122000018/fb-20211231.htm", checked_on: checkedOn },
  { title: "Meta FY2022 Form 10-K", url: "https://www.sec.gov/Archives/edgar/data/1326801/000132680123000013/meta-20221231.htm", checked_on: checkedOn },
  { title: "Meta FY2023 Form 10-K", url: "https://www.sec.gov/Archives/edgar/data/1326801/000132680124000012/meta-20231231.htm", checked_on: checkedOn },
  { title: "Meta FY2025 Form 10-K", url: "https://www.sec.gov/Archives/edgar/data/1326801/000162828026003942/meta-20251231.htm", checked_on: checkedOn },
];
const description = [
  "Reality Labs 在 FY2025 報告了將近 192 億美元的營業虧損，Meta 全公司的營業損益卻仍是正的。這集跟著四份 SEC 年報的分部表，從 2021 年改名與分欄，拆開 2022 年廣告送達數、平均單價與 FoA 費用的變化，再看 2023 年廣告回升、兩個分部結果分岔，以及 2021 與 2023 年公司合計只差 200 萬美元卻藏著 2022 年低谷。片尾回到 2025 年同年同口徑的答案。",
  "",
  "營業利益與虧損均為財年分部營業損益；廣告價格、送達數及 RL 收入另屬不同指標，比較年度也不同。片中關於下一代運算平台需仰賴其他業務利潤的說法，來自 Meta 自己的 FY2025 年報。報表不能單獨證明逐筆現金轉帳、單品投報或未來產品成敗。畫面為無商標示意，不是真實網站、產品畫面或員工。查核日期：2026-10-20。",
  "",
  "資料來源（SEC 原始申報）",
  ...sources.flatMap((source) => [source.title, source.url]),
].join("\n");
const doc = {
  schema_version: 1,
  slug,
  format: "drama",
  category: "explainer",
  narration_locale: "zh-TW",
  target_minutes: [8, 11],
  voice: {
    provider: "gemini",
    name: "Sulafat",
    style: "標準國語，咬字清楚，台北人平常說話的語調。像跟朋友一起翻一本帳，數字放慢，問句上揚，揭曉前停半拍。",
    performance: "每個數字都連著財年和營業損益口徑；百萬美元與億美元不可混念，英文縮寫須先完成發音審查。",
  },
  subtitles: { burn_in: false },
  look: { preset: "cute-mystery" },
  characters: [],
  series: { slug: "brand-stories-everyday-reversals-extra", episode: 5, chapter: 1 },
  music: { prompt: "light, curious, a little mysterious, no vocals", gain_db: -20, duck_db: -10 },
  loops,
  youtube: {
    category_id: 27,
    made_for_kids: false,
    default_language: "zh-TW",
    title: "Reality Labs 營業虧近 192 億，Meta 為何仍有營業利益？｜品牌故事",
    description,
    tags: ["Meta", "Reality Labs", "Family of Apps", "品牌故事", "營業利益", "分部財報", "FY2025"],
    video_id: null,
  },
  thumbnail: { template: "thumb", data: { headline: "**近192億**", tag: "品牌故事", brand: "META", shot: "x05-b01-s02" } },
  sources,
  assets: [],
  scenes,
};
const videoBytes = JSON.stringify(doc, null, 2) + "\n";
writeFileSync(path.join(dir, "video.json"), videoBytes);
const sha = createHash("sha256").update(videoBytes).digest("hex");
const escape = (value) => String(value).replaceAll("|", "\\|").replaceAll("\n", " ");
const sourceMatrix = [
  "# X05 Meta｜逐句來源矩陣",
  "",
  "由 `drafts/lines.tsv` 的來源欄產生。這是作者對照，不代替獨立逐句審查；SEC 原文與限制見 [source-notes.md](source-notes.md)，四份原文獨立抽核見 [source-audit.md](reviews/source-audit.md)。",
  "",
  `- \`video.json\` SHA-256：\`${sha}\``,
  "- M21／M22／M23／M25 分別對應 FY2021／FY2022／FY2023／FY2025 Form 10-K；`editorial` 是不主張財報事實的觀眾互動。",
  "- 口播中的約數換算請回到原始百萬美元表格；字幕不可抹去『營業』或年度。",
  "",
  "| 句 ID | 旁白 | 來源 |",
  "| --- | --- | --- |",
  ...draft.map((row) => `| \`${row.id}\` | ${escape(row.text)} | ${row.sources.join("、")} |`),
  "",
].join("\n");
writeFileSync(path.join(dir, "source-matrix.md"), sourceMatrix);
const script = [
  "# X05 Meta｜繁中逐句稿",
  "",
  `此檔由 \`drafts/lines.tsv\` 產生，\`video.json\` SHA-256 \`${sha}\`。實際旁白與字幕以 \`video.json\` 為準；目前尚無配音或實測時長。`,
  "",
  ...chapters.flatMap((title, index) => [`## ${index + 1}. ${title}`, "", ...draft.filter((row) => row.chapter === index + 1).map((row) => `- \`${row.id}\` ${row.text}`), ""]),
].join("\n");
writeFileSync(path.join(dir, "script.md"), script);
console.log(JSON.stringify({ scenes: scenes.length, shots: scenes.filter((scene) => scene.template === "shot").length, cards: scenes.filter((scene) => scene.template === "stats").length, narration_characters: draft.reduce((sum, row) => sum + row.text.length, 0), loops: loops.length, video_sha256: sha }, null, 2));
