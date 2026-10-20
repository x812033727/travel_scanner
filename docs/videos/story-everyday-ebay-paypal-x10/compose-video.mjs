// Free local preproduction build; no remote or paid media calls.
import { createHash } from "node:crypto";
import { writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { textHash } from "../../../tools/video/core/schema.mjs";
import { chapters } from "./drafts/story.mjs";

const dir = path.dirname(fileURLToPath(import.meta.url));
const slug = "story-everyday-ebay-paypal-x10";
const checked_on = "2026-10-20";
const sources = [
  { title: "eBay FY2002 Form 10-K", url: "https://www.sec.gov/Archives/edgar/data/1065088/000089161803001538/f88540e10vk.htm", checked_on },
  { title: "eBay 2002-10-03 Form 8-K", url: "https://www.sec.gov/Archives/edgar/data/1065088/000089161802004533/f84762e8vk.htm", checked_on },
  { title: "eBay FY2014 Form 10-K", url: "https://www.sec.gov/Archives/edgar/data/1065088/000106508815000054/ebay201410-k.htm", checked_on },
  { title: "PayPal 2015 Form 10 information statement, Exhibit 99.1", url: "https://www.sec.gov/Archives/edgar/data/1633917/000119312515237232/d877527dex991.htm", checked_on },
  { title: "eBay／PayPal 2015 Operating Agreement, 8-K Exhibit 10.1", url: "https://www.sec.gov/Archives/edgar/data/1065088/000119312515257121/d93601dex101.htm", checked_on },
  { title: "eBay FY2015 Q3 Form 10-Q", url: "https://www.sec.gov/Archives/edgar/data/1065088/000106508815000252/ebay10-qq32015.htm", checked_on },
  { title: "eBay FY2018 Q1 Form 10-Q", url: "https://www.sec.gov/Archives/edgar/data/1065088/000106508818000020/ebay10-qq12018.htm", checked_on },
  { title: "eBay FY2019 Form 10-K", url: "https://www.sec.gov/Archives/edgar/data/1065088/000106508820000006/ebay201910-k.htm", checked_on },
  { title: "eBay FY2020 Form 10-K", url: "https://www.sec.gov/Archives/edgar/data/1065088/000106508821000006/ebay-20201231.htm", checked_on },
  { title: "eBay FY2021 Form 10-K", url: "https://www.sec.gov/Archives/edgar/data/1065088/000106508822000006/ebay-20211231.htm", checked_on },
  { title: "eBay FY2022 Form 10-K", url: "https://www.sec.gov/Archives/edgar/data/1065088/000106508823000006/ebay-20221231.htm", checked_on },
];
const cameras = ["push in", "pan left", "static", "pan right", "tilt up", "pull back"];
const framings = ["Medium shot", "Wide shot", "Close shot", "Overhead shot"];
const makeLine = (id, value) => {
  const line = { id, text: value, emotion: value.endsWith("？") ? "問句上揚，留一個短停頓" : "自然說書，數字逐位清楚" };
  const say = value.replaceAll("eBay", "伊貝").replaceAll("PayPal", "佩寶");
  if (say !== value) Object.assign(line, { say, say_for: textHash(value) });
  return line;
};
const authoredScenes = chapters.flatMap((chapter, ci) => chapter.rows.map(([value, claim_refs, visual], ri) => {
  const number = String(ri + 1).padStart(2, "0");
  const id = `x10-b${String(ci + 1).padStart(2, "0")}-s${number}`;
  const line = makeLine(`x10${String(ci + 1).padStart(2, "0")}${number}`, value);
  const scene = {
    id,
    template: typeof visual === "string" && visual !== "outro" ? "shot" : visual === "outro" ? "outro" : "stats",
    data: typeof visual === "string" && visual !== "outro"
      ? { prompt: `${framings[(ci + ri) % framings.length]} ${visual}`, camera: cameras[(ci * 2 + ri) % cameras.length], visual: "still" }
      : visual === "outro" ? { title: "付款的所有權與控制權", cta: "訂閱品牌故事" } : visual,
    lines: [line],
    claim_refs,
  };
  if (ri === 0) scene.chapter = chapter.title;
  return scene;
}));
const closing = authoredScenes.splice(-3, 3);
if (!closing.every(scene => scene.template === "outro")) throw new Error("Last three authored lines must be native outro");
authoredScenes.push({ id: "x10-outro", template: "outro", data: closing[0].data, lines: closing.flatMap(scene => scene.lines) });
const scenes = authoredScenes.map(({ claim_refs: _refs, ...scene }) => scene);
const ids = new Map(scenes.flatMap((scene, index) => scene.lines.map(line => [line.id, index])));
const loop = (setup, payoff, what) => {
  if (ids.get(setup) === undefined || ids.get(payoff) === undefined || ids.get(setup) >= ids.get(payoff)) throw new Error(`Invalid loop ${setup} -> ${payoff}`);
  return { setup, payoff, what };
};
const loops = [
  loop("x100102", "x100501", "二〇一八年付款中介如何成為產品能力"),
  loop("x100103", "x100403", "PayPal 分拆究竟怎麼完成"),
  loop("x100105", "x100408", "分家後付款合作如何延續"),
  loop("x100106", "x100601", "五年協議何時到期"),
  loop("x100107", "x100703", "最後誰管理平台的付款"),
  loop("x100217", "x100303", "PayPal 平台外交易占比"),
  loop("x100404", "x100405", "公司分拆安排是否有現金出售"),
  loop("x100315", "x100406", "分拆後 PayPal 是否立刻退出結帳"),
  loop("x100416", "x100505", "五年協議期間是否啟動新路"),
  loop("x100515", "x100609", "到期後新路能接住多少賣家"),
  loop("x100615", "x100702", "全市場遷移是否完成"),
  loop("x100707", "x100708", "財報是否留下結果"),
  loop("x100206", "x100207", "電子郵件如何支援收付款"),
  loop("x100308", "x100311", "董事會何時轉向分拆"),
  loop("x100409", "x100410", "營運協議的初始期限"),
  loop("x100507", "x100508", "付款中介是否離開工程清單"),
  loop("x100608", "x100609", "分批遷移後活躍賣家規模"),
  loop("x100210", "x100212", "舊付款服務的處置計畫"),
  loop("x100302", "x100305", "網站交易在總付款額的比例"),
  loop("x100611", "x100612", "公司如何描述買賣家體驗"),
  loop("x100711", "x100712", "成交額是否跟收入同步成長"),
];
const description = [
  "eBay 在 2002 年買下 PayPal 來改善網路交易付款，2015 年卻把 PayPal 分拆成獨立公司；幾年後，它又開始替自己的市集中介付款。為什麼先拆後接？本集沿 SEC 原始申報，追一筆交易如何從成交走到收款，以及兩家公司分開後仍持續的五年營運協議。",
  "",
  "2014 年 US$227.9bn 是 PayPal Net TPV，US$59.6bn 是其中的 On-eBay Net TPV，26% 不是營收比例。2015 年是向原股東分配 PayPal 股份，並非 eBay 現金賣出。2019 年的 US$2.0bn 是 2018 起累計處理付款額，非 eBay 收入。2021 年 US$1.5bn 淨交易收入年增還有廣告等共同因素。公司對分拆與自管付款好處的表述屬當時主張。插畫為無標誌概念示意，不是真實公司人員、網站畫面或 SEC 文件。資料查核日期：2026-10-20。",
  "",
  "一手資料（SEC 原始申報及附件）",
  ...sources.flatMap(source => [source.title, source.url]),
].join("\n");
const doc = {
  schema_version: 1,
  slug,
  format: "drama",
  category: "explainer",
  narration_locale: "zh-TW",
  target_minutes: [8, 10],
  voice: { provider: "gemini", name: "Sulafat", style: "台灣標準國語、自然說書。問句留下短暫懸念，年份和美元數字放慢念清楚。", performance: "把收購、計畫分拆、完成分拆、協議到期與全市場遷移分開；付款交易額、交易收入、GMV 不混念。" },
  subtitles: { burn_in: false },
  look: { preset: "cute-mystery" },
  characters: [],
  series: { slug: "brand-stories-everyday-reversals-extra", episode: 10, chapter: 1 },
  music: { prompt: "light, curious, slightly mysterious, no vocals", gain_db: -20, duck_db: -10 },
  loops,
  youtube: { category_id: 27, made_for_kids: false, default_language: "zh-TW", title: "eBay 拆出 PayPal 後，為何又自己接手收款？｜品牌故事", description, tags: ["eBay", "PayPal", "品牌故事", "支付", "網路拍賣", "商業史"], video_id: null },
  thumbnail: { template: "thumb", data: { headline: "**又收款？**", tag: "品牌故事", brand: "eBay", shot: "x10-b01-s02" } },
  sources,
  assets: [],
  scenes,
};
const videoBytes = JSON.stringify(doc, null, 2) + "\n";
writeFileSync(path.join(dir, "video.json"), videoBytes);
const sha256 = createHash("sha256").update(videoBytes).digest("hex");
const escape = value => String(value).replaceAll("|", "\\|").replaceAll("\n", " ");
const original = chapters.flatMap((chapter, ci) => chapter.rows.map(([value, claimRefs], ri) => ({ id: `x10${String(ci + 1).padStart(2, "0")}${String(ri + 1).padStart(2, "0")}`, value, claimRefs })));
const matrix = [
  "# X10 eBay／PayPal｜逐句來源矩陣", "",
  "本表由 `drafts/story.mjs` 生成；B 編號及邊界見 [source-matrix.md](source-matrix.md)。獨立審查完成後，審查收據會綁定本版 SHA。", "",
  `- \`video.json\` SHA-256：\`${sha256}\``, "",
  "| 句 ID | 旁白 | Treatment 主張 |", "| --- | --- | --- |",
  ...original.map(row => `| \`${row.id}\` | ${escape(row.value)} | ${row.claimRefs.length ? row.claimRefs.join("、") : "編輯問句／CTA"} |`), "",
].join("\n");
writeFileSync(path.join(dir, "line-source-matrix.md"), matrix);
const script = ["# X10 eBay／PayPal｜繁中逐句稿", "", `稿件綁定 \`video.json\` SHA-256 \`${sha256}\`。尚無 TTS 實測；站主片頭片尾不計入實質正文。`, "", ...chapters.flatMap((chapter, ci) => [
  `## ${ci === 0 ? "濃縮開場" : `第 ${ci} 章`}｜${chapter.title}`, "",
  ...chapter.rows.map(([value], ri) => `- \`x10${String(ci + 1).padStart(2, "0")}${String(ri + 1).padStart(2, "0")}\` ${value}`), "",
])].join("\n");
writeFileSync(path.join(dir, "script.md"), script);
writeFileSync(path.join(dir, "series.json"), JSON.stringify({ kind: "story", slug: "brand-stories-everyday-reversals-extra", episode: 10, chapter: 1, title: "eBay 拆出 PayPal 後，為何又自己接手收款？", logline: "從 2002 年買下 PayPal 加快交易、2015 年股權分拆但保留五年營運協議，到 2018–2021 年 eBay 逐步接回市集的付款流程。", names: ["eBay", "PayPal"], characters: [], target_minutes: 10, image_model: "image-01", style_preset: "custom", look: { preset: "cute-mystery" }, visual_tier: "stills", compilation: false }, null, 2) + "\n");
console.log(JSON.stringify({ scenes: scenes.length, shots: scenes.filter(s => s.template === "shot").length, cards: scenes.filter(s => s.template === "stats").length, lines: original.length, characters: original.reduce((sum, row) => sum + row.value.length, 0), loops: loops.length, video_sha256: sha256 }, null, 2));
