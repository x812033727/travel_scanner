// Standalone Shorts scripts using the episode's illustration shot IDs. No paid call.
import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { validate } from "../../../tools/video/shorts/core.mjs";

const dir = path.dirname(fileURLToPath(import.meta.url));
const videoBytes = readFileSync(path.join(dir, "video.json"));
const video = JSON.parse(videoBytes);
const videoSha = createHash("sha256").update(videoBytes).digest("hex");
const shotIds = new Set(video.scenes.map(scene => scene.id));
const sections = [];
for (const raw of readFileSync(path.join(dir, "drafts/shorts.md"), "utf8").split(/\r?\n/)) {
  const header = raw.match(/^## Short [12]｜(.+)$/);
  if (header) { sections.push({ title: header[1], rows: [] }); continue; }
  const row = raw.match(/^(.*?)\s+\[((?:A[1-4](?:,A[1-4])*|editorial))\]$/);
  if (row) {
    if (!sections.length) throw new Error("Short line before section");
    sections.at(-1).rows.push({ text: row[1].trim(), refs: row[2] === "editorial" ? [] : row[2].split(",") });
  }
}
if (sections.length !== 2 || sections.some(short => short.rows.length !== 8)) throw new Error("Expected two eight-line Shorts");
const shots = [
  ["x14-b04-s26", "x14-b02-s17", "x14-b01-s01", "x14-b02-s20", "x14-b04-s26", "x14-b02-s11", "x14-b04-s26", "x14-b01-s01"],
  ["x14-b05-s05", "x14-b05-s07", "x14-b05-s06", "x14-b05-s13", "x14-b05-s19", "x14-b06-s09", "x14-b06-s17", "x14-b05-s20"],
];
const beats = ["hook", "setup", "setup", "turn", "proof", "proof", "payoff", "loop"];
const headlines = [
  ["虧 46 億美元＝退訂？", "全年淨預訂 −41%", "三、四月合計取消超新訂", "淨虧損還含上市費用", "IPO 股份費用 ~US$2.8bn", "全年非現金變動 ~8.7億美元", "46 億 ≠ 取消帳單", "不能自創疫情虧損"],
  ["長住升＝首次盈利？", "2021 Q4 長住 22%", "2019 Q4 是 16%", "逾九成活躍刊登可接長住", "Q4 賺／全年虧", "2022 Q4 長住 21%", "2022 首個盈利年", "份額 ≠ 單獨功勞"],
];
const sourceLinks = [
  [{ label: "Airbnb 2020 Form 10-K", url: "https://www.sec.gov/Archives/edgar/data/1559720/000155972021000010/airbnb-10k.htm" }],
  [
    { label: "Airbnb 2021 Q4 shareholder letter", url: "https://www.sec.gov/Archives/edgar/data/1559720/000119312522043371/d251410dex991.htm" },
    { label: "Airbnb 2022 Q4 shareholder letter", url: "https://www.sec.gov/Archives/edgar/data/1559720/000119312523039008/d451233dex991.htm" },
  ],
];
const descriptions = [
  "Airbnb 2020 年淨預訂夜晚與體驗席位下降 41%，全年 GAAP 淨虧損約 US$4.6bn；其中含 IPO 觸發的約 US$2.8bn 股份費用及全年約 US$868.5m 非現金權證公允價值變動。不能把全部淨虧損說成取消訂單的代價，也不能扣兩項自創『真正疫情虧損』。匿名畫面是概念示意；長片正式網址待發布後補入。",
  "Airbnb 2021 Q4 的 28 夜以上長住占當季 gross nights booked 22%，2019 Q4 同口徑是 16%；2021 Q4 末超過九成活躍刊登項目（可為住宿或體驗）接受至少 28 夜預訂，這是可訂設定，不代表已入住。2021 Q4 有 US$55m 淨利，全年仍淨虧 US$352m。2022 Q4 長住占 21%，2022 全年 GAAP 淨利約 US$1.9bn。這組同期事實不能算出長住的獨立獲利貢獻。匿名畫面是概念示意；長片正式網址待發布後補入。",
];
const common = { schema_version: 2, format: "shorts", locale: "zh-TW", line: "cut", series: "illustrated", source: { slug: video.slug }, synthetic_media: true, hashtags: ["Airbnb", "品牌故事", "旅遊"], tags: ["Airbnb", "品牌故事", "旅行", "商業史"] };
const shorts = sections.map((section, i) => {
  const scenes = section.rows.map((row, j) => {
    const shot = shots[i][j];
    if (!shotIds.has(shot)) throw new Error(`Missing long-video shot ${shot}`);
    return { beat: beats[j], shot, headline: headlines[i][j], narration: [row.text] };
  });
  const short = {
    ...common, slug: `${video.slug}-short-${i + 1}`,
    titles: [section.title, i === 0 ? "Airbnb 2020 虧損，不等於旅客取消的帳單" : "Airbnb 長住占比提高，能單獨解釋首次盈利嗎？"],
    description: descriptions[i], links: sourceLinks[i], scenes,
  };
  const chars = section.rows.map(row => row.text).join("").length;
  if (chars < 105 || chars > 225) throw new Error(`${short.slug}: ${chars} characters outside 25–55-second paper range`);
  const errors = validate(short);
  if (errors.length) throw new Error(`${short.slug}: ${errors.join("; ")}`);
  return short;
});
const bytes = JSON.stringify(shorts, null, 2) + "\n";
writeFileSync(path.join(dir, "shorts.json"), bytes);
const shortsSha = createHash("sha256").update(bytes).digest("hex");
writeFileSync(path.join(dir, "shorts-script.md"), [
  "# X14 Airbnb｜兩支獨立 Shorts", "",
  `主片 SHA-256：\`${videoSha}\`；Shorts SHA-256：\`${shortsSha}\`。各自有主角、事件、問題與結局；纸面時長須由正式 TTS 重測。Shot 引用長片的插畫位置，旁白按本 Short 獨立錄製。`, "",
  ...shorts.flatMap((short, i) => [`## Short ${i + 1}｜${short.titles[0]}`, "", `- 字數：${sections[i].rows.map(row => row.text).join("").length}；按每分鐘 250–300 字約 ${(sections[i].rows.map(row => row.text).join("").length / 300 * 60).toFixed(1)}–${(sections[i].rows.map(row => row.text).join("").length / 250 * 60).toFixed(1)} 秒，未測聲音。`, `- 一手連結：${short.links.map(link => link.url).join("、")}`, "", ...short.scenes.map(scene => `- **${scene.beat}｜${scene.headline}**（\`${scene.shot}\`）：${scene.narration.join("")}`), ""]),
].join("\n").replace("纸面", "紙面"));
writeFileSync(path.join(dir, "shorts-source-matrix.md"), [
  "# X14 Airbnb｜Shorts 逐句來源矩陣", "", `Shorts SHA-256：\`${shortsSha}\`。來源代碼見 \`source-matrix.md\`。`, "",
  ...sections.flatMap((section, i) => [`## Short ${i + 1}`, "", "| 句 ID | 旁白 | 來源 |", "| --- | --- | --- |", ...section.rows.map((row, j) => `| \`x14short${i + 1}-${String(j + 1).padStart(2, "0")}\` | ${row.text.replaceAll("|", "\\|")} | ${row.refs.length ? row.refs.join("、") : "編輯提問"} |`), ""]),
].join("\n"));
console.log(JSON.stringify({ video_sha256: videoSha, shorts_sha256: shortsSha, shorts: shorts.map((short, i) => ({ slug: short.slug, characters: sections[i].rows.map(row => row.text).join("").length, scenes: short.scenes.length })) }, null, 2));
