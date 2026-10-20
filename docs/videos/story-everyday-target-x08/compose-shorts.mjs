// Offline cuts from the locked long-form line text; no TTS or media is generated here.
import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { validate } from "../../../tools/video/shorts/core.mjs";
import { episodeShortsProblems } from "../../../tools/video/shorts/episode.mjs";

const dir = path.dirname(fileURLToPath(import.meta.url));
const videoBytes = readFileSync(path.join(dir, "video.json"));
const video = JSON.parse(videoBytes);
const lineMap = new Map(video.scenes.flatMap(scene => scene.lines.map(line => [line.id, line.text])));
const shotIds = new Set(video.scenes.filter(scene => scene.template === "shot").map(scene => scene.id));
const phrase = id => {
  const result = lineMap.get(id);
  if (!result) throw new Error(`Missing long-form line ${id}`);
  if ([...result].length > 38) throw new Error(`Shorts phrase ${id} exceeds 38 characters`);
  return result;
};
const beat = (kind, shot, headline, ids) => {
  if (!shotIds.has(shot)) throw new Error(`Shorts keyframe ${shot} is not a long-form shot`);
  return { beat: kind, shot, headline, narration: ids.map(phrase) };
};
const common = index => ({
  schema_version: 2,
  slug: `${video.slug}-short-${index}`,
  format: "shorts",
  locale: "zh-TW",
  line: "cut",
  series: "illustrated",
  source: { slug: video.slug },
  synthetic_media: true,
  hashtags: ["Target", "品牌故事", "加拿大"],
  tags: ["Target", "加拿大", "品牌故事", "零售", "商業史"],
});
const shorts = [
  {
    ...common(1),
    titles: ["Target 宣布退出那天，133 家店真的都關了？", "Target 加拿大 133 店宣布退出，何時才全關？"],
    description: "2015-01-15 Target 宣布退出加拿大，加拿大子公司申請 CCAA；當時的 133 間門市在清算期間仍營業。後續季報只證實截至 2015-05-02 全數關閉，沒有給最後一店的確切關閉日。管理層在公告時認為 2021 年前沒有可信獲利情境。完整事件與財報脈絡請看本集長片。資料：Target 2015-01-15 原公告與 FY2015 Q1 Form 10-Q；畫面為匿名概念插畫。",
    links: [
      { label: "Target 2015-01-15 原公告", url: "https://www.sec.gov/Archives/edgar/data/27419/000002741915000005/exhibit99atargetcorporatio.htm" },
      { label: "Target FY2015 Q1 Form 10-Q", url: "https://www.sec.gov/Archives/edgar/data/27419/000002741915000018/tgt-20150502x10xq.htm" },
    ],
    scenes: [
      beat("hook", "x08-b01-s03", "當時 133 店，卻宣布退出", ["x080104", "x080503"]),
      beat("setup", "x08-b01-s01", "2015-01-15｜加拿大子公司申請保護", ["x080101"]),
      beat("turn", "x08-b05-s04", "公告日，門市仍開著", ["x080102", "x080504"]),
      beat("proof", "x08-b05-s11", "截至 5 月 2 日已全關", ["x080510"]),
      beat("payoff", "x08-b04-s41", "管理層看不到近年獲利", ["x080441"]),
      beat("loop", "x08-b01-s10", "開 133 店，為何仍撤？", ["x080110"]),
    ],
  },
  {
    ...common(2),
    titles: ["Target 加拿大退出費用 51.05 億，等於現金燒掉？", "Target 的 51.05 億美元退出費用，怎麼看？"],
    description: "Target FY2014 10-K 將加拿大稅前退出費用列為 US$5.105b，其中 US$4.766b 是非現金投資減損，另有或有負債、員工信託及其他退出費；不能把總額稱為宣布當天等額現金流出。營運虧損是另一項會計數字。完整帳目與撤退決策請看本集長片。資料：Target FY2014 Form 10-K，Note 6；畫面為匿名概念插畫。",
    links: [
      { label: "Target FY2014 Form 10-K，Note 6", url: "https://www.sec.gov/Archives/edgar/data/27419/000002741915000012/tgt-20150131x10k.htm" },
    ],
    scenes: [
      beat("hook", "x08-b06-s02", "US$5.105b 退出費用", ["x080601", "x080602"]),
      beat("setup", "x08-b06-s04", "其中 US$4.766b 非現金", ["x080603"]),
      beat("turn", "x08-b06-s05", "為何減到近零？", ["x080604", "x080605"]),
      beat("proof", "x08-b06-s07", "子公司資產不敷負債", ["x080607", "x080608"]),
      beat("payoff", "x08-b06-s09", "仍有其他退出成本", ["x080609", "x080610"]),
      beat("loop", "x08-b06-s11", "營運虧損另算", ["x080611"]),
    ],
  },
];
const errors = [
  ...shorts.flatMap((short, index) => validate(short).map(problem => `Short ${index + 1}: ${problem}`)),
  ...episodeShortsProblems(shorts, video),
];
if (errors.length) throw new Error(errors.join("\n"));
const bytes = JSON.stringify(shorts, null, 2) + "\n";
writeFileSync(path.join(dir, "shorts.json"), bytes);
const videoSha256 = createHash("sha256").update(videoBytes).digest("hex");
const shortsSha256 = createHash("sha256").update(bytes).digest("hex");
console.log(JSON.stringify({ video_sha256: videoSha256, shorts_sha256: shortsSha256, shorts: shorts.map(short => ({ slug: short.slug, scenes: short.scenes.length, spoken_characters: short.scenes.flatMap(scene => scene.narration).join("").length })) }, null, 2));
