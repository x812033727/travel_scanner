// Rebuild the nonpaid canonical project from the owner-approved C11 originals.
// The script never edits script.md or either visual-plan file.
import { readFileSync, writeFileSync } from "node:fs";
import { createHash } from "node:crypto";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";
import { textHash } from "../../../tools/video/core/schema.mjs";

const dir = dirname(fileURLToPath(import.meta.url));
const approved = {
  "script.md": "C55D77133E1508BFEACE8B7423E5CF7579ECB768CA33F60BD13380480F589CD3",
  "visual-plan.md": "74159C33441952209A0E94E7C866EBB9EDC967C09449B85958D51BC103034811",
  "visual-plan.json": "DF45CBEA15A41354B1CA8722D79EE633E03B92F87D7B9CA0BE1FE0BF95B73228",
  "script-source-notes.md": "1BD11B87D217C9E3B3F81418EA9FC108CD7C457A27C5B2B992A71AEDADFA95FE",
};
for (const [name, expected] of Object.entries(approved)) {
  const actual = createHash("sha256").update(readFileSync(join(dir, name))).digest("hex").toUpperCase();
  if (actual !== expected) throw new Error(`${name} changed since owner approval: ${actual}`);
}
const script = readFileSync(join(dir, "script.md"), "utf8");
const visual = JSON.parse(readFileSync(join(dir, "visual-plan.json"), "utf8"));
const rows = [...script.matchAll(/^\| (c11\d{4}) \| ([^|]+) \| ([^|]+) \|$/gm)]
  .map((match) => ({ id: match[1], text: match[2].trim(), evidence: match[3].trim() }));
if (rows.length !== 78 || visual.shots.length !== 78 ||
    rows.some((row, index) => row.id !== visual.shots[index].line_id)) {
  throw new Error("C11 approved narration and visual IDs must align 78/78");
}

const chapters = [
  "瓶子退回去，問題留下來",
  "一個故事，兩條第一時間線",
  "杯裡能喝，不等於罐裡能賣",
  "把飲料和金屬隔開",
  "把冰罐送到人群面前",
  "那個拉環，來得比較晚",
];
const shotSize = {
  "極近景": "Extreme close-up.", "近景": "Close-up.",
  "中景": "Medium shot.", "遠景": "Wide shot.",
  "俯視近景": "Top-down close-up.",
};
const cameras = ["push in", "pan left", "pull back", "tilt up", "pan right", "tilt down"];
const cardSources = {
  c110202: "UCC 官方沿革", c110207: "濱田市人物記錄",
  c110211: "UCC 咖啡博物館", c110212: "濱田市／島根縣地方記錄",
  c110410: "UCC 2025／2026 回顧", c110506: "UCC 2025／2026 回顧",
  c110511: "UCC 2025 回顧", c110515: "UCC 2025 包裝回顧",
  c110601: "UCC 2025 包裝回顧",
};
const scenes = rows.map((row, index) => {
  const plan = visual.shots[index];
  const chapterIndex = Number(row.id.slice(3, 5)) - 1;
  const line = {
    id: row.id,
    text: row.text,
    emotion: "自然說書；公司回顧、年份和兩條商品時間線放慢，章末問題留半拍",
  };
  // Pronunciation candidates only. Text, subtitle, and owner-approved wording stay exact.
  if (/UCC|Mira/.test(row.text)) {
    line.say = row.text.replaceAll("UCC", "U C C").replaceAll("Mira", "米拉");
    line.say_for = textHash(row.text);
  }
  const scene = { id: `c11-sc-${row.id}` };
  if (index === 0 || rows[index - 1].id.slice(3, 5) !== row.id.slice(3, 5)) {
    scene.chapter = chapters[chapterIndex];
  }
  scene.template = plan.kind === "stats" ? "stats" : "shot";
  if (plan.kind === "stats") {
    const separator = plan.text.includes("｜") ? "｜" : "：";
    const [value, label, ...extra] = plan.text.split(separator);
    if (!value || !label || extra.length) throw new Error(`Card ${row.id} must have one separator`);
    if (!cardSources[row.id]) throw new Error(`Missing card source ${row.id}`);
    scene.data = { stats: [{ value, label }], source: cardSources[row.id] };
  } else {
    if (!shotSize[plan.camera]) throw new Error(`Unknown shot size ${plan.camera}`);
    scene.data = {
      prompt: `${shotSize[plan.camera]} ${plan.prompt}`,
      camera: cameras[index % cameras.length],
      visual: "still",
    };
  }
  scene.claims = [row.id];
  scene.lines = [line];
  return scene;
});
if (scenes.filter((scene) => scene.template === "shot").length !== 69 ||
    scenes.filter((scene) => scene.template === "stats").length !== 9) {
  throw new Error("C11 approved visual count changed from 69 stills / 9 cards");
}

const video = {
  schema_version: 1,
  slug: "story-everyday-ucc-c11",
  format: "drama",
  // Current stills + stats lint supports cute-mystery under explainer.
  category: "explainer",
  narration_locale: "zh-TW",
  target_minutes: [9, 11],
  voice: {
    provider: "gemini", name: "Sulafat",
    style: "標準國語，咬字清楚，台北日常說話語調。以克制的說書節奏講真實商品史；公司歸因、日期與外文放慢，章末留半拍。",
  },
  subtitles: { burn_in: false },
  look: { preset: "cute-mystery" },
  characters: [],
  series: { slug: "brand-stories-everyday-reversals", episode: 11, chapter: 1 },
  music: { prompt: "light, curious, a little mysterious, no vocals", gain_db: -20, duck_db: -10 },
  loops: [
    { setup: "c110105", payoff: "c110407", what: "奶咖入罐面對哪幾道互不相同的難題" },
    { setup: "c110108", payoff: "c110603", what: "帶得走是否等於能順手喝" },
    { setup: "c110205", payoff: "c110212", what: "早於 UCC 的罐咖啡與含奶主張如何分開" },
    { setup: "c110213", payoff: "c110408", what: "奶咖分層的公開解法能說到哪裡" },
    { setup: "c110214", payoff: "c110405", what: "金屬罐還會造成什麼問題" },
    { setup: "c110314", payoff: "c110406", what: "咖啡變黑的處理範圍" },
    { setup: "c110412", payoff: "c110510", what: "商品上市後如何走到更多來客面前" },
    { setup: "c110416", payoff: "c110511", what: "陌生的罐裝飲用方式如何被看見" },
    { setup: "c110516", payoff: "c110602", what: "哪一代包裝才有拉環" },
    { setup: "c110608", payoff: "c110610", what: "後來的旅客如何不用打孔器開罐" },
  ],
  youtube: {
    category_id: 27, made_for_kids: false, default_language: "zh-TW",
    title: "UCC：一罐咖啡能帶上車，為什麼還得拿工具打孔？｜品牌故事",
    description: "一瓶咖啡牛奶在車站得退回，變成可帶走的罐子後，卻還不能順手打開。這集沿 UCC 的退瓶回顧，追奶咖入罐遇到的飲品與罐壁難題、1969 年上市、1970 年大阪萬博，以及 1981 年才出現的第三代拉環。\n\n1965 年 Mira 罐裝咖啡的較早銷售見濱田市地方記錄；UCC 博物館的優先權說法限於「含奶」罐裝咖啡。研發與萬博成效主要是 UCC 多年後回顧；所引來源未提供同期配方、完整銷售底帳或精確首賣日。畫面皆為匿名、無標誌的原創概念插畫，不重建創辦人、原罐或會場實景。資料查核日期：2026-10-23。",
    tags: ["UCC", "罐裝咖啡", "奶咖", "品牌故事", "日用品的意外轉身", "拉環"],
    video_id: null,
  },
  thumbnail: {
    template: "thumb",
    data: { headline: "奶咖罐\n**怎麼開？**", tag: "品牌故事", brand: "UCC", shot: "c11-sc-c110101" },
  },
  sources: [
    { title: "UCC, 2026 product history", url: "https://www.ucc.co.jp/company/news/2026/rel260302.html", checked_on: "2026-10-23" },
    { title: "UCC, 2025 product retrospective", url: "https://www.ucc.co.jp/company/pressroom/pickup/20250716.html", checked_on: "2026-10-23" },
    { title: "UCC Coffee Museum", url: "https://www.ucc.co.jp/museum/sp/jp/001.html", checked_on: "2026-10-23" },
    { title: "UCC, company history", url: "https://www.ucc.co.jp/company/history/", checked_on: "2026-10-23" },
    { title: "Hamada City, Miura Yoshitake short record", url: "https://www.city.hamada.shimane.jp/www/contents/1437096185880/index.html", checked_on: "2026-10-23" },
    { title: "Hamada City, Miura Yoshitake", url: "https://www.city.hamada.shimane.jp/www/contents/1445997212239/index.html", checked_on: "2026-10-23" },
    { title: "Shimane Prefecture, local history", url: "https://www.pref.shimane.lg.jp/admin/seisaku/koho/ichiban/", checked_on: "2026-10-23" },
  ],
  scenes,
};
const series = {
  kind: "story", slug: "brand-stories-everyday-reversals", episode: 11, chapter: 1,
  title: "UCC：一罐咖啡能帶上車，為什麼還得拿工具打孔？",
  logline: "瓶裝奶咖的退瓶麻煩催生可攜罐；飲品與罐壁、銷售、開罐方式分別跨過不同門檻。",
  names: ["UCC", "Mira", "上島忠雄", "三浦義武", "Ueshima", "Miura", "日本橋三越"],
  characters: [], visual_tier: "stills", compilation: false,
};
const write = (name, body) => writeFileSync(join(dir, name), body, "utf8");
write("video.json", `${JSON.stringify(video, null, 2)}\n`);
write("series.json", `${JSON.stringify(series, null, 2)}\n`);
write("claims.md", [
  "# C11 UCC｜核准逐句稿的主張索引", "",
  "此表是站主核准 78 句原稿的逐句投影，並非新查核。來源與界線沿用 source-matrix.md、script-source-notes.md 及獨立差異審查。", "",
  "| 主張 ID | 已核准旁白 | 來源與限制 |", "| --- | --- | --- |",
  ...rows.map((row) => `| ${row.id} | ${row.text} | ${row.evidence} |`), "",
].join("\n"));
write("verify-1.md", [
  "# C11 UCC｜既有獨立來源判定的 QA 對接", "",
  "衍生收據，非新一輪獨立查核。原初逐句審查 HOLD 及舊版 v5 單句 HOLD 保留歷史效力；後續 v2–v4 差異審查、現行 c110410 獨立重核與現行稿兩位盲讀 PASS，才構成站主核准版的來源及敘事依據。CONFIRMED 只表示已核稿遵守來源歸因與推論界線，不能把 UCC 或地方政府的事後回顧當同期原件。", "",
  "綁定 script.md SHA-256：C55D77133E1508BFEACE8B7423E5CF7579ECB768CA33F60BD13380480F589CD3。未核准付費製作、配音、圖像、成片或上架。", "",
  "| 主張 ID | 既有判定 | 原稿來源與限制 |", "| --- | --- | --- |",
  ...rows.map((row) => `| ${row.id} | CONFIRMED | ${row.evidence} |`), "",
].join("\n"));
write("brief.md", `# C11 UCC｜一罐奶咖為何能帶走卻不能順手喝？\n\n本集屬於「日用品的意外轉身」。站主已核准六章企劃、78 句旁白與 78 鏡方向；本機器專案只作非付費轉檔，沒有改動受核准雜湊綁定的原稿、分鏡或來源說明。C11 尚無整支報價及付費試片核准。\n\n## 問題\n\n瓶裝咖啡牛奶得退回攤位，罐裝可帶走；為何 UCC 的早期奶咖罐還需要另一件工具才能喝到？\n\n## 一句答案\n\n依 UCC 後來回顧，奶咖先須處理分層、熱處理風味及罐壁變色，1969 年才能作為商品出售；1970 年大阪萬博是品牌自述的推廣轉點。早期罐要用開孔器打飲口和氣孔，1981 年第三代才改拉環。\n\n## 站主觀點\n\n把「帶得走」與「打得開」當作兩道分開的日常便利設計：先讓觀眾看見玻璃瓶被留下，再逐步揭露奶咖入罐、罐壁、銷售與拉環的不同關口。資料分層講述，不以 UCC 的含奶主張抹掉 Mira 較早的罐咖啡記錄，也不把公司事後回顧當作可稽核銷售數字。\n\n## 來源與畫面邊界\n\n1965 年 Mira 已有較早的罐咖啡地方記錄，UCC 博物館的「世界首款」只以含奶罐咖啡限定並明示歸屬。Mira 奶成分未知；1970 年萬博後需求增加只按 UCC 事後說法，不畫成可稽核銷售曲線。內塗層只用於解釋罐壁變黑，不能推其同時解決分層或風味。\n\n六章順序為退瓶、兩條「第一」時間線、飲品難題、罐壁塗層、萬博推廣、第三代拉環。畫面均為匿名、無標誌的原創概念示意；九張字卡後製，不讓圖片模型畫真包裝、可讀字、真人肖像或實際萬博建物。第一章 c110108 後接既有 5 秒片頭，最後 c110615 後接 21 秒 v4 片尾與連結安全區；繁中 CC 可關閉。\n\n正文須先以實際 TTS 證明至少 480 秒，再決定能否購圖；真實時間軸的插圖比率須至少 70%，旁白及圖片都要各自驗收。紙上字數估時不能代替任一關卡。\n`);
console.log(JSON.stringify({ lines: rows.length, stills: scenes.filter((s) => s.template === "shot").length, cards: scenes.filter((s) => s.template === "stats").length, say: scenes.filter((s) => s.lines[0].say).length }));
