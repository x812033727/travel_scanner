// Build source-episode Shorts from exact long-form narration; local and free.
import { readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { validate } from "../../../tools/video/shorts/core.mjs";
import { episodeShortsProblems } from "../../../tools/video/shorts/episode.mjs";
import { chapters } from "./drafts/story.mjs";

const dir = path.dirname(fileURLToPath(import.meta.url));
const slug = "story-everyday-ebay-paypal-x10";
const video = JSON.parse(readFileSync(path.join(dir, "video.json")));
const videoScenes = new Map(video.scenes.map(item => [item.id, item]));
const videoLines = new Map(video.scenes.flatMap(item => item.lines.map(line => [line.id, line.text])));
const lines = new Map(chapters.flatMap((chapter, ci) => chapter.rows.map(([text, claims], ri) => [
  `x10${String(ci + 1).padStart(2, "0")}${String(ri + 1).padStart(2, "0")}`,
  { text, claims },
])));
const phrase = id => {
  const line = lines.get(id);
  if (!line) throw new Error(`No main-video line ${id}`);
  if ([...line.text].length > 38) throw new Error(`Shorts phrase ${id} exceeds 38 characters`);
  if (videoLines.get(id) !== line.text) throw new Error(`${id}: main video out of sync; run compose-video.mjs`);
  return line.text;
};
const scene = (beat, shot, headline, ids, options = {}) => {
  const sourceScene = videoScenes.get(shot);
  if (!sourceScene || sourceScene.template !== "shot") throw new Error(`${shot}: Shorts require a main-video illustration shot`);
  for (const id of ids) if (!sourceScene.lines.some(line => line.id === id)) throw new Error(`${shot}: narration ${id} does not belong to this source shot`);
  return { beat, shot, headline, narration: ids.map(phrase), ...options };
};
const common = index => ({
  schema_version: 2,
  slug: `${slug}-short-${index}`,
  format: "shorts",
  locale: "zh-TW",
  line: "cut",
  series: "illustrated",
  source: { slug },
  synthetic_media: true,
  hashtags: ["eBay", "PayPal", "品牌故事"],
  tags: ["eBay", "PayPal", "品牌故事", "支付", "商業史"],
});
const shorts = [
  {
    ...common(1),
    titles: ["eBay 分拆 PayPal，有收到出售現金嗎？", "PayPal 獨立上市，eBay 拿到現金了嗎？"],
    description: "2015-07-17 eBay 把 PayPal 股份分配給原股東，每一股 eBay 股票收到一股 PayPal 股票；這不是 eBay 現金出售 PayPal。兩家公司同時以營運協議延續支付合作，初始期限五年。完整背景請看長片。資料：eBay FY2015 Q3 Form 10-Q、PayPal 2015 Form 10 information statement、2015 Operating Agreement。畫面為無標誌概念示意。",
    scenes: [
      scene("hook", "x10-b04-s04", "分拆＝現金出售？", ["x100404"]),
      scene("setup", "x10-b04-s01", "分拆當天有兩件事", ["x100401"]),
      scene("turn", "x10-b04-s02", "原股東每股獲配一股", ["x100402"]),
      scene("proof", "x10-b04-s05", "eBay 沒收到出售現金", ["x100405"]),
      scene("payoff", "x10-b04-s13", "分拆股權，支付仍合作", ["x100413"]),
      scene("loop", "x10-b04-s07", "營運協議繼續合作", ["x100407"]),
    ],
  },
  {
    ...common(2),
    titles: ["eBay 拆出 PayPal，收款何時接回來？", "分拆 PayPal 後，eBay 為何再做自己的收款？"],
    description: "eBay 2015 年分拆 PayPal，2018 年把付款中介列為產品開發重點。2019 年底累計為近 25,000 賣家處理付款；2020 年原營運協議到期，年底 managed payments 活躍賣家逾一百萬；公司 2021 年報說全市場遷移完成。這是平台收款流程的轉移，並不是買回 PayPal 或宣稱 PayPal 無法用於結帳。完整背景請看長片。資料：eBay FY2015 Q3 10-Q、FY2018 Q1 10-Q、FY2019–2021 10-K。畫面為無標誌概念示意。",
    scenes: [
      scene("hook", "x10-b01-s02", "2018 又要做付款中介", ["x100102"]),
      scene("turn", "x10-b01-s03", "三年前才分拆 PayPal", ["x100103"]),
      scene("proof", "x10-b05-s05", "2018 開始中介付款", ["x100505"]),
      scene("proof", "x10-b05-s08", "2019 美國採用加快", ["x100508"]),
      scene("proof", "x10-b06-s02", "舊合約到期後繼續擴張", ["x100602"]),
      scene("payoff", "x10-b07-s03", "2021 年底管理平台付款", ["x100703"]),
      scene("loop", "x10-b07-s16", "股權與結帳，是兩種決策", ["x100716"]),
    ],
  },
];
const errors = [...shorts.flatMap((short, index) => validate(short).map(problem => `Short ${index + 1}: ${problem}`)), ...episodeShortsProblems(shorts, video)];
if (errors.length) throw new Error(errors.join("\n"));
const bytes = JSON.stringify(shorts, null, 2) + "\n";
writeFileSync(path.join(dir, "shorts.json"), bytes);
console.log(JSON.stringify(shorts.map(short => ({ slug: short.slug, scenes: short.scenes.length, phrases: short.scenes.reduce((sum, item) => sum + item.narration.length, 0), spoken_characters: short.scenes.flatMap(item => item.narration).join("").length })), null, 2));
