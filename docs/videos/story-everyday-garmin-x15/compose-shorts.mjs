// Offline, deterministic Short metadata composition. No TTS, provider, or upload calls.
import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const dir = path.dirname(fileURLToPath(import.meta.url));
const base = "story-everyday-garmin-x15";
const protectedName = /\b(?:Garmin|Forerunner|NAVIGON|Auto OEM)\b|nüvi|佳明|高民環|GPSMAP/iu;
const videoBytes = readFileSync(path.join(dir, "video.json"));
const video = JSON.parse(videoBytes);
const videoSha = createHash("sha256").update(videoBytes).digest("hex");
const rows = [[], []];
let current = -1;
for (const raw of readFileSync(path.join(dir, "drafts/shorts.md"), "utf8").split(/\r?\n/)) {
  const header = raw.match(/^## Short ([12])/);
  if (header) { current = Number(header[1]) - 1; continue; }
  if (!/^x15s[12]\d{2}\s*\|/.test(raw)) continue;
  const parts = raw.split("|").map(part => part.trim());
  if (current < 0 || parts.length !== 4) throw new Error(`Malformed Short row: ${raw}`);
  const [id, refsText, text, cue] = parts;
  if (!text || !cue) throw new Error(`Missing Short narration or visual cue: ${id}`);
  if (protectedName.test(cue)) throw new Error(`Short visual cue contains a protected name: ${id}`);
  if (!/^(?:G[1-6](?:,G[1-6])*|editorial)$/.test(refsText)) throw new Error(`Invalid Short source: ${id}`);
  rows[current].push({ id, refs: refsText, text, cue });
}
if (rows.some(short => short.length < 5 || short.length > 9)) throw new Error("Expected 5–9 scenes per Short");
for (const [si, short] of rows.entries()) {
  for (const [ri, row] of short.entries()) {
    const expected = `x15s${si + 1}${String(ri + 1).padStart(2, "0")}`;
    if (row.id !== expected) throw new Error(`Expected ${expected}; found ${row.id}`);
  }
}
// Use existing long-video illustrations only after hand-picking story-appropriate shots.
// Keep this mapping distinct from landscape stats cards: vertical cards are native overlays.
// Anchor cuts to spoken line IDs, not scene numbers: scene packing can change
// between script revisions while the intended illustration remains the same.
const shotLineMap = {
  1: ["x150331", "x150104", "x150302", "x150412", "x150425", "x150414", "x150421", "x150423", "x150410"],
  2: ["x150501", "x150502", "x150505", "x150511", "x150540", "x150542", "x150623", "x150601", "x150633"],
};
const byShot = new Map(video.scenes.map(scene => [scene.id, scene]));
const byLine = new Map(video.scenes.flatMap(scene => scene.lines.map(line => [line.id, scene])));
const shotMap = Object.fromEntries(Object.entries(shotLineMap).map(([si, ids]) => [si, ids.map(id => {
  const scene = byLine.get(id);
  if (!scene || scene.template !== "shot") throw new Error(`Unavailable Short source line or landscape stats card: ${id}`);
  return scene.id;
})]));
for (const [si, short] of rows.entries()) {
  if (shotMap[si + 1].length !== short.length) throw new Error(`Short ${si + 1}: hand-pick ${short.length} matching source shots`);
  for (const shot of shotMap[si + 1]) if (!byShot.has(shot) || byShot.get(shot).template !== "shot") throw new Error(`Unavailable/landscape stats shot: ${shot}`);
}
const sec = {
  G1: "https://www.sec.gov/Archives/edgar/data/1121788/000114420407007445/v065417_ex99-1.htm",
  G2: "https://www.sec.gov/Archives/edgar/data/1121788/000114420409010751/v141191_10k.htm",
  G3: "https://www.sec.gov/Archives/edgar/data/1121788/000114420409010317/v141019_ex99-1.htm",
  G4: "https://www.sec.gov/Archives/edgar/data/1121788/000114420411010322/v212200_ex99-1.htm",
  G5: "https://www.sec.gov/Archives/edgar/data/1121788/000114420412012007/v303209_10k.htm",
  G6: "https://www.sec.gov/Archives/edgar/data/1121788/000119312526056025/grmn-ex99_1.htm",
};
const common = { schema_version: 2, format: "shorts", locale: "zh-TW", line: "cut", series: "illustrated", source: { slug: base }, synthetic_media: true, hashtags: ["Garmin", "品牌故事", "GPS"], tags: ["Garmin", "品牌故事", "導航機", "GPS", "年報"] };
const specs = [
  {
    titles: ["Garmin 年報三年之間改了哪個字？", "Garmin：手機導航從可能威脅到已發生壓力"],
    headlines: ["2008：可能", "車用／行動逾七成", "nüvi 約六成四", "三年後", "2011：成長停滯", "nüvi 約四成八", "機器未突然消失", "風險已成事實", "無法獨算手機"],
    description: "Garmin FY2008 10-K 稱手機 GPS 與導航軟體可能拖慢成長；當時 automotive/mobile 事業占公司營收逾七成，nüvi 產品線約占全公司 64%。FY2011 10-K 改稱手機導航的接受度已使成長停滯，nüvi 當年約占全公司 48%。這是公司風險披露，不表示手機獨自造成所有收入下降。完整長片連結待實際發布後回填；畫面是匿名概念插畫。",
    refs: ["G2", "G5"],
  },
  {
    titles: ["Garmin 兩款 GPS 錶之後，收入主角換了嗎？", "Garmin 2025 年營收，手錶之外還有什麼？"],
    headlines: ["2011：GPS 錶", "觸控運動錶", "跑／騎／游", "健身部門 +24%", "車用仍居首", "十四個財年後", "分部邊界不同", "健身第一、戶外第二", "健身＋戶外：60.9%"],
    big: { 4: "約58%", 8: "60.9%" }, kicker: { 4: "2011 全年營收", 8: "2025 全年營收；公司為分母" },
    body: { 2: ["跑步／騎車／游泳"] },
    description: "Garmin FY2011 10-K 記載 Forerunner 610 與 910XT GPS 運動錶新品，並列當年 Fitness 事業營收 +24%；舊車用／行動事業仍占全公司約 58%。FY2025 全年財報顯示 Fitness 是第一大事業、Outdoor 第二，兩者依原始千美元金額合占約 60.9% 的總營收。兩端相隔十四個財年，且部門邊界不同；不能從兩端占比推算某一型號造成的成長或舊事業的衰退。長片正式連結待上架後填入；畫面是匿名概念插畫。",
    refs: ["G5", "G6"],
  },
];
const shorts = rows.map((short, si) => ({
  ...common, slug: `${base}-short-${si + 1}`, titles: specs[si].titles, description: specs[si].description,
  links: specs[si].refs.map(ref => ({ label: `Garmin ${ref} SEC 原件`, url: sec[ref] })),
  scenes: short.map((row, ri) => ({
    beat: ri === 0 ? "hook" : ri === short.length - 1 ? "payoff" : ri < (si === 0 ? 3 : 4) ? "setup" : ri === (si === 0 ? 3 : 4) ? "turn" : "proof",
    shot: shotMap[si + 1][ri],
    headline: specs[si].headlines[ri],
    ...(specs[si].big?.[ri] ? { big: specs[si].big[ri] } : {}),
    ...(specs[si].kicker?.[ri] ? { kicker: specs[si].kicker[ri] } : {}),
    ...(specs[si].body?.[ri] ? { body: specs[si].body[ri] } : {}),
    narration: [row.text],
  })),
}));
for (const short of shorts) {
  const chars = short.scenes.flatMap(scene => scene.narration).join("").length;
  if (chars < 105 || chars > 225) throw new Error(`${short.slug}: ${chars} chars outside 25–55 second paper range`);
}
const bytes = JSON.stringify(shorts, null, 2) + "\n";
writeFileSync(path.join(dir, "shorts.json"), bytes);
const sha = createHash("sha256").update(bytes).digest("hex");
writeFileSync(path.join(dir, "shorts-script.md"), [
  "# X15 Garmin｜兩支獨立 Shorts 逐句稿", "", `長片 SHA-256：\`${videoSha}\`；Shorts SHA-256：\`${sha}\`。離線前製，未配音、剪輯或實測；正式長片網址待上架後回填。每支使用長片匿名插畫，但文字、順序和結尾自成一個故事；5 秒片頭及 21 秒片尾只屬正式長片。`, "",
  ...shorts.flatMap((short, si) => [`## Short ${si + 1}｜${short.titles[0]}`, "", ...short.scenes.map((scene, ri) => `- \`${rows[si][ri].id}\` [${rows[si][ri].refs}] ${scene.narration[0]}（\`${scene.shot}\`）`), "", `一手資料：${short.links.map(link => `[${link.label}](${link.url})`).join("、")}`, ""]),
].join("\n"));
writeFileSync(path.join(dir, "shorts-source-matrix.md"), [
  "# X15 Garmin｜Shorts 逐句作者來源矩陣", "", `\`shorts.json\` SHA-256：\`${sha}\`；主片 SHA-256：\`${videoSha}\`。本表是作者標記，獨立逐句審查尚待完成；來源代碼見 [source-matrix.md](source-matrix.md)。`, "",
  "| Short | 句 ID | 旁白 | 作者來源標記 |", "| --- | --- | --- | --- |",
  ...rows.flatMap((short, si) => short.map(row => `| ${si + 1} | \`${row.id}\` | ${row.text.replaceAll("|", "\\|")} | ${row.refs === "editorial" ? "敘事提問／概念示意／CTA" : row.refs.replaceAll(",", "、")} |`)), "",
].join("\n"));
const portraitFocus = {
  1: [
    "問號與未展開的財報角", "一粗數條細的收入色帶", "產品占公司收入的內外圈", "兩份重疊的無字年報", "手機與趨平的路線", "產品圈與事業圈同框", "貨架上仍在售的獨立設備", "兩條無字風險紙條", "手機旁交會的多股壓力線",
  ],
  2: [
    "兩只匿名運動錶並排", "單只手腕裝置與跑道", "一只錶居中；三項運動由原生字卡承載", "手錶與較大的健身收入線", "舊表的粗藍線；原生約 58% 大字", "首尾兩份無字年報與中間封閉年份", "不同分隔頁的新舊年報", "新表上的健身與戶外前兩條色帶", "健身、戶外兩色帶；原生 60.9% 大字",
  ],
};
writeFileSync(path.join(dir, "shorts-portrait-plan.md"), [
  "# X15 Garmin｜兩支 Shorts 的直式構圖交接", "",
  `離線規劃，綁定主片 SHA-256 \`${videoSha}\` 與 Shorts SHA-256 \`${sha}\`。**尚無插畫、直式渲染或手機實測**；下列 x 座標是 16:9 生圖的指定構圖與首次裁切位置，生成後須逐鏡檢查並以實際主體位置修正。`, "",
  "主片 1920×1080 的每張重用插畫，先把表中主體集中在中央 **x=656–1264、y=0–1080** 的 608×1080 走廊；第一版 `crop=608:1080:656:0`，再等比輸出 1080×1920。若生圖不守此區，選 x=0–1312 內的重裁並保留主體；不能保留時，仍在同集預算與已審劇本內重生該張。不能把橫式收入數字或報表字直接裁進 Short 作證據。", "",
  "原生 9:16 字卡按工具既有版型：1080×1920，標題／大數字／資料列留在 **x=78–902、y≤1380**；字幕條 x=80–900、y=1430–1595，不放進底部操作區；品牌行 y=90、年份／分組行 y=174。標題原始字級 88px、字幕 49px；在 360px 手機寬度試看時約為 29px／16px，若兩行擠壓或對比不足，縮短字卡或加深遮罩，不能靠放大底圖造成裁切。數字、年份、部門名都由原生字卡顯示，插畫保持無可讀字與無商標。", "",
  "| Short／拍 | 重用主片 shot | 608×1080 首選裁切 | 必須留在直式畫面的主體；讀不全時由原生文字承載 |",
  "| --- | --- | --- | --- |",
  ...shorts.flatMap((short, si) => short.scenes.map((scene, ri) => `| ${si + 1}／${ri + 1} | \`${scene.shot}\` | \`x=656, y=0\` | ${portraitFocus[si + 1][ri]}；原生「${scene.headline}」${scene.big ? `、大字「${scene.big}」` : ""}${scene.body ? `、資料列「${scene.body.join("／")}」` : ""} |`)),
  "", "成片前逐張查看中央裁切與左右最壞偏移、360px 手機預覽、標題與字幕的安全區量測；Short 2 第 3 拍不要求三位運動人物都擠進 608px，三項運動已由原生字卡承載。兩支須以實際 TTS 與影片確認各 25–55 秒、可讀來源與片尾真連結；目前沒有這些量測或可點影片網址。", "",
].join("\n"));
console.log(JSON.stringify({ video_sha256: videoSha, shorts_sha256: sha, shorts: shorts.map(short => ({ slug: short.slug, scenes: short.scenes.length, characters: short.scenes.flatMap(scene => scene.narration).join("").length })) }, null, 2));
