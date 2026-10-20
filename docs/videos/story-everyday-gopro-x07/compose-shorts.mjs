// Build the two source-episode Shorts drafts from the X07 long-form narration.
// Free, local preproduction only: this neither synthesizes speech nor renders media.
import { readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { validate } from "../../../tools/video/shorts/core.mjs";
import { episodeShortsProblems } from "../../../tools/video/shorts/episode.mjs";
import { chapters } from "./drafts/story.mjs";

const dir = path.dirname(fileURLToPath(import.meta.url));
const slug = "story-everyday-gopro-x07";
const video = JSON.parse(readFileSync(path.join(dir, "video.json")));
const videoLines = new Map(video.scenes.flatMap(item => item.lines.map(line => [line.id, line.text])));
const lines = new Map(chapters.flatMap((chapter, ci) => chapter.rows.map(([text, claims], ri) => [
  `x07${String(ci + 1).padStart(2, "0")}${String(ri + 1).padStart(2, "0")}`,
  { text, claims },
])));
const phrase = id => {
  const line = lines.get(id);
  if (!line) throw new Error(`No long-form narration line ${id}`);
  if ([...line.text].length > 38) throw new Error(`Shorts phrase ${id} exceeds 38 characters`);
  return line.text;
};
const scene = (beat, shot, headline, ids, options = {}) => {
  const result = { beat, shot, headline, narration: ids.map(phrase), ...options };
  for (const id of ids) if (videoLines.get(id) !== lines.get(id).text) throw new Error(`${id}: video.json is out of sync with drafts/story.mjs; run compose-video.mjs first`);
  return result;
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
  hashtags: ["GoPro", "Karma", "品牌故事"],
  tags: ["GoPro", "Karma", "品牌故事", "無人機", "商業史"],
});
const shorts = [
  {
    ...common(1),
    titles: ["GoPro 自稱 Karma 在其價位帶第二，為何仍退出？", "GoPro 無人機才復售，卻在隔年決定退出？"],
    description: "Karma 2016 年因部分機體飛行中失去電力而全數撤回，2017 年在美國復售。GoPro 在 2018 年公告自稱 Karma 曾達 2017 年其價位帶第二，卻決定售完庫存後退出消費無人機；公司提出競爭與毛利挑戰，也預期歐美當時的監管環境將在往後幾年縮小市場。排名的地區、價位帶邊界與分母未公布。完整故事請看本集長片。資料：GoPro FY2016／FY2017 Form 10-K、2018-01-08 Form 8-K Exhibit 99.1。畫面為無標誌概念示意。",
    scenes: [
      scene("hook", "x07-b01-s01", "2016：新飛機飛行中斷電", ["x070101", "x070102"]),
      scene("setup", "x07-b03-s01", "全部撤回，提供退款", ["x070301", "x070302"]),
      scene("turn", "x07-b04-s02", "2017 美國復售", ["x070401"]),
      scene("proof", "x07-b05-s05", "GoPro 自稱｜其價位帶第 2", ["x070504"]),
      scene("payoff", "x07-b05-s03", "售完庫存後退出", ["x070503"]),
      scene("loop", "x07-b01-s01", "公司說：競爭與毛利壓力", ["x070506"]),
    ],
  },
  {
    ...common(2),
    titles: ["GoPro 的 US$80.5m 營收減項，涉及哪些產品？", "相機與 Karma 調價相關的 US$80.5m 營收減項"],
    description: "GoPro FY2017 第三季季報說，較少的 Karma 銷售對公司毛利率比前季改善有次要貢獻；主因仍是 HERO6 Black 推出。第四季 US$80.5m 營收減項含多款相機與 Karma 的價格保護及通路行銷支持；同季另列 US$14.9m Karma 相關減記及費用。兩項不能合稱 Karma 單品虧損。完整背景請看本集長片。資料：GoPro FY2017 Q3 Form 10-Q、FY2017／FY2018 Form 10-K。畫面為無標誌概念示意。",
    scenes: [
      scene("hook", "x07-b04-s07", "第三季 Karma 銷售較前季少", ["x070407"]),
      scene("setup", "x07-b04-s08", "公司毛利率季增｜主因仍是新相機", ["x070408", "x070409"]),
      scene("turn", "x07-b01-s06", "年底相機改價", ["x070106"]),
      scene("proof", "x07-b04-s10", "US$80.5M 營收減項", ["x070411"], { big: "US$80.5M" }),
      scene("proof", "x07-b04-s12", "相機及 Karma｜兩種支持", ["x070412"]),
      scene("payoff", "x07-b04-s13", "另有 Karma 減記及費用", ["x070413", "x070414"], { big: "US$14.9M" }),
      scene("loop", "x07-b04-s15", "飛機還能繼續賣嗎？", ["x070415"]),
    ],
  },
];
const errors = [...shorts.flatMap((short, index) => validate(short).map(problem => `Short ${index + 1}: ${problem}`)), ...episodeShortsProblems(shorts, video)];
if (errors.length) throw new Error(errors.join("\n"));
const shortsBytes = JSON.stringify(shorts, null, 2) + "\n";
writeFileSync(path.join(dir, "shorts.json"), shortsBytes);
console.log(JSON.stringify(shorts.map(short => ({ slug: short.slug, scenes: short.scenes.length, phrases: short.scenes.reduce((sum, item) => sum + item.narration.length, 0), spoken_characters: short.scenes.flatMap(item => item.narration).join("").length })), null, 2));
