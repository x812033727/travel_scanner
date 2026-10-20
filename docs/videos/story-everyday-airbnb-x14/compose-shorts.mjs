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
  ["x14-b04-s22", "x14-b02-s16", "x14-b01-s01", "x14-b04-s23", "x14-b04-s24", "x14-b04-s25", "x14-b04-s22", "x14-b01-s01"],
  ["x14-b05-s04", "x14-b05-s07", "x14-b05-s06", "x14-b05-s11", "x14-b05-s17", "x14-b06-s06", "x14-b06-s15", "x14-b06-s14"],
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
// A source shot is a semantic reference, not a claim that a 16:9 frame has
// already been cropped or rendered. Every beat carries its own vertical plan.
const portraitFocus = [
  [
    "審帳者打開全年虧損簿，取消訂單小堆留在簿外；手、簿、代幣同框",
    "淨預訂下降色帶與收入色帶各留兩端，不讓 −41% 看起來像營收降幅",
    "旅客的手拿掉三月日曆上的一格，行李只露一角；保留拿掉的動作",
    "原生直式年度虧損卡：主值與全年 GAAP 口徑一起讀到",
    "原生直式 IPO 股份費用卡：位置承接上一拍，明示它包含在虧損中",
    "無字年度損益簿與獨立的權證重估欄；取消訂單代幣留在另一側，不能畫成分碗訂單",
    "回到審帳者與全年虧損簿，取消訂單小堆仍在簿外，構成首拍回呼",
    "回到同一位旅客拿掉的日曆格，空格與行李角落都可辨",
  ],
  [
    "旅客把行李代幣往連續日曆格推，保留起點、終點與手勢",
    "原生直式 2021 Q4 長住卡：22% 與至少 28 夜／當季 gross nights 同框",
    "原生直式 2019 Q4 同口徑比較卡：16% 和年份完整可讀；不借遠端工作者圖",
    "房東打開長段可訂日曆；只畫開放設定，不能畫成已入住",
    "季損益簿與年損益簿分開；先亮單季淨利，再換成年淨虧",
    "原生直式 2022 Q4 長住卡：21% 與至少 28 夜／當季 gross nights 同框",
    "原生直式 2022 全年 GAAP 淨利卡：先亮首次全年盈利，再亮約十九億美元",
    "審帳者把長住色帶放在全年損益簿旁，留空未填的單獨貢獻欄；不暗示已算出因果",
  ],
];
const nativeCards = new Set(["0:3", "0:4", "1:1", "1:2", "1:5", "1:6"]);
function portraitFor(shortIndex, beatIndex) {
  const native = nativeCards.has(`${shortIndex}:${beatIndex}`);
  return {
    status: "planned",
    rendered: false,
    canvas_px: { width: 1080, height: 1920 },
    source_use: native ? "values-and-period-only" : "semantic-reference-for-new-portrait-art",
    crop_or_rebuild: native ? "rebuild-native-9:16-card" : "reframe-around-action-or-regenerate-9:16-if-crop-loses-required-objects",
    focus: portraitFocus[shortIndex][beatIndex],
    headline_safe_px: { x: 100, y: 280, width: 780, height: 910 },
    cc_clear_px: { x: 100, y: 1260, width: 780, height: 180 },
    controls_clear_px: { x: 880, y: 0, width: 200, height: 1920 },
    crop_check: "Review at phone size; keep the described action and all required objects visible. Rebuild instead of forcing a center crop.",
  };
}
const common = { schema_version: 2, format: "shorts", locale: "zh-TW", line: "cut", series: "illustrated", source: { slug: video.slug }, synthetic_media: true, hashtags: ["Airbnb", "品牌故事", "旅遊"], tags: ["Airbnb", "品牌故事", "旅行", "商業史"] };
const shorts = sections.map((section, i) => {
  const scenes = section.rows.map((row, j) => {
    const shot = shots[i][j];
    if (!shotIds.has(shot)) throw new Error(`Missing long-video shot ${shot}`);
    return { beat: beats[j], shot, headline: headlines[i][j], narration: [row.text], portrait: portraitFor(i, j) };
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
