// Two offline from-episode cuts. Narration and shot IDs must exist in video.json.
import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const dir = path.dirname(fileURLToPath(import.meta.url));
const videoBytes = readFileSync(path.join(dir, "video.json"));
const video = JSON.parse(videoBytes);
const videoSha = createHash("sha256").update(videoBytes).digest("hex");
const byLine = new Map(video.scenes.flatMap(scene => scene.lines.map(line => [line.id, { scene, line }])));
const take = (id, beat, headline) => {
  const found = byLine.get(id);
  if (!found) throw new Error(`Missing from-episode line ${id}`);
  return { beat, shot: found.scene.id, headline, narration: [found.line.text] };
};
const common = { schema_version: 2, format: "shorts", locale: "zh-TW", line: "cut", series: "illustrated", source: { slug: video.slug }, synthetic_media: true, hashtags: ["FedEx", "聯邦快遞", "品牌故事"], tags: ["FedEx", "聯邦快遞", "品牌故事", "包裹配送"] };
const shorts = [
  {
    ...common, slug: `${video.slug}-short-1`,
    titles: ["FedEx 同一品牌，兩家公司 2024 合了，路網呢？", "FedEx 的 Express 和 Ground 曾是兩家公司"],
    description: "FedEx FY2022 年報仍把 Express 和 Ground 分列；FY2023 宣布 one FedEx，Ground 與 Services 到 2024-06-01 才併入 Federal Express。FY2024 年報同時只報美國 50 多處實施 Network 2.0；法律合併不代表所有實體路網同日完成整合。完整事件與財年邊界見本集長片；畫面是匿名概念插畫。長片正式網址待發布後填入。",
    links: [
      { label: "FedEx FY2022 Form 10-K", url: "https://www.sec.gov/Archives/edgar/data/1048911/000095017022012762/fdx-20220531.htm" },
      { label: "FedEx FY2023 Form 10-K", url: "https://www.sec.gov/Archives/edgar/data/1048911/000095017023033201/fdx-20230531.htm" },
      { label: "FedEx FY2024 Form 10-K", url: "https://www.sec.gov/Archives/edgar/data/1048911/000095017024083577/fdx-20240531.htm" },
    ],
    scenes: [
      take("x110101", "hook", "FY2022｜同一品牌"),
      take("x110102", "setup", "Express 與 Ground"),
      take("x110103", "turn", "兩家公司"),
      take("x110301", "event", "FY2023 宣布 one FedEx"),
      take("x110401", "next-year", "2024 年加拿大先分階段轉換"),
      take("x110404", "payoff", "2024-06-01 法律合併"),
      take("x110407", "evidence", "美國當時只有 50 多處實施"),
      take("x110408", "close", "法律日期不是路網完成日"),
    ],
  },
  {
    ...common, slug: `${video.slug}-short-2`,
    titles: ["FedEx 合併後，路線為何還沒全改完？", "FedEx Network 2.0：加拿大完成，美國仍有目標日"],
    description: "FedEx 把 Network 2.0 定為美加包裹取件、運輸與配送的多年效率工程。FY2025 年報記載美加約 290 個地點實施最佳化，並稱加拿大已完成、美國約 130 個地點實施；FY2026 年報稱美國約 360 個地點實施，預計 2027 曆年底完成。美國日期是公司預期，不能說已完成。完整事件見本集長片；畫面是匿名概念插畫。長片正式網址待發布後填入。",
    links: [
      { label: "FedEx FY2023 Form 10-K", url: "https://www.sec.gov/Archives/edgar/data/1048911/000095017023033201/fdx-20230531.htm" },
      { label: "FedEx FY2025 Form 10-K", url: "https://www.sec.gov/Archives/edgar/data/1048911/000104891125000011/fdx-20250531.htm" },
      { label: "FedEx FY2026 Form 10-K", url: "https://www.sec.gov/Archives/edgar/data/1048911/000104891126000105/fdx-20260531.htm" },
    ],
    scenes: [
      take("x110301", "hook", "FY2023｜one FedEx"),
      take("x110303", "setup", "Network 2.0"),
      take("x110304", "engine", "美加取件、運輸、配送"),
      take("x110501", "turn", "FY2025 新數字"),
      take("x110601", "compare", "FY2025 加拿大已完成"),
      take("x110602", "contrast", "同時美國約 130 處"),
      take("x110603", "progress", "FY2026 美國約 360 處"),
      take("x110604", "close", "2027 年底仍是預期"),
    ],
  },
];
const length = short => short.scenes.flatMap(scene => scene.narration).join("").length;
for (const short of shorts) {
  const chars = length(short);
  if (chars < 105 || chars > 225) throw new Error(`${short.slug}: ${chars} chars outside 25–55 second planning range`);
}
const bytes = JSON.stringify(shorts, null, 2) + "\n";
writeFileSync(path.join(dir, "shorts.json"), bytes);
const shortsSha = createHash("sha256").update(bytes).digest("hex");
writeFileSync(path.join(dir, "shorts-script.md"), [
  "# X11 FedEx｜兩支從長片衍生的 Shorts", "",
  `主片 SHA-256：\`${videoSha}\`；Shorts SHA-256：\`${shortsSha}\`。每句都來自鎖定主片，時長按每分鐘 250–300 字估計，剪輯後仍須用 TTS 音訊實測；Shorts 不額外插主片的 5 秒片頭或 21 秒片尾。`, "",
  ...shorts.flatMap((short, i) => [`## Short ${i + 1}｜${short.titles[0]}`, "", `- 來源：\`${short.source.slug}\`；\`from-episode\`，重用主片的聲音與畫面。`, `- 字數：${length(short)}；估時約 ${(length(short) / 300 * 60).toFixed(1)}–${(length(short) / 250 * 60).toFixed(1)} 秒。`, `- 一手連結：${short.links.map(link => link.url).join("、")}`, "", ...short.scenes.map(scene => `- **${scene.beat}｜${scene.headline}**（\`${scene.shot}\`）：${scene.narration.join("")}`), ""]),
].join("\n"));
console.log(JSON.stringify({ video_sha256: videoSha, shorts_sha256: shortsSha, cuts: shorts.map(short => ({ slug: short.slug, characters: length(short), estimated_seconds_at_300_cpm: +(length(short) / 300 * 60).toFixed(1), estimated_seconds_at_250_cpm: +(length(short) / 250 * 60).toFixed(1) })) }, null, 2));
