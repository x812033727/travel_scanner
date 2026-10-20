// Offline, deterministic Short metadata composition. No TTS, provider, or upload calls.
import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const dir = path.dirname(fileURLToPath(import.meta.url));
const base = "story-everyday-garmin-x15";
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
const shotMap = {
  1: [],
  2: [],
};
const byShot = new Map(video.scenes.map(scene => [scene.id, scene]));
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
    description: "Garmin FY2008 10-K 稱手機 GPS 與導航軟體可能拖慢成長；當時 automotive/mobile 事業占公司營收逾七成，nüvi 產品線約占全公司 64%。FY2011 10-K 改稱手機導航的接受度已使成長停滯，nüvi 當年約占全公司 48%。這是公司風險披露，不表示手機獨自造成所有收入下降。完整長片連結待實際發布後回填；畫面是匿名概念插畫。",
    refs: ["G2", "G5"],
  },
  {
    titles: ["Garmin 導航機之外，GPS 又走到哪？", "Garmin 的 GPS 手錶不是唯一新收入線"],
    description: "Garmin FY2011 10-K 記載 Forerunner 610 與 910XT GPS 運動錶新品，並列當年 Fitness 事業營收 +24%、Outdoor +14%。FY2025 全年財報列 Fitness 與 Outdoor 按原始金額合占約 60.9% 的總營收，另外還有 Marine、Aviation、Auto OEM；60.9% 是兩個事業，不能說全是手錶，亦不能宣稱兩款 2011 新品單獨造成 2025 結果。長片正式連結待上架後填入；畫面是匿名概念插畫。",
    refs: ["G5", "G6"],
  },
];
const shorts = rows.map((short, si) => ({
  ...common, slug: `${base}-short-${si + 1}`, titles: specs[si].titles, description: specs[si].description,
  links: specs[si].refs.map(ref => ({ label: `Garmin ${ref} SEC 原件`, url: sec[ref] })),
  scenes: short.map((row, ri) => ({
    beat: ri === 0 ? "hook" : ri === short.length - 1 ? "payoff" : ri === Math.floor(short.length / 2) ? "turn" : "development",
    shot: shotMap[si + 1][ri],
    headline: row.text.slice(0, 14),
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
console.log(JSON.stringify({ video_sha256: videoSha, shorts_sha256: sha, shorts: shorts.map(short => ({ slug: short.slug, scenes: short.scenes.length, characters: short.scenes.flatMap(scene => scene.narration).join("").length })) }, null, 2));
