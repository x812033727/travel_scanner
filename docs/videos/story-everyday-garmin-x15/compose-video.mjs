// Deterministic offline preproduction build. Never imports a story or calls a media provider.
import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const dir = path.dirname(fileURLToPath(import.meta.url));
const slug = "story-everyday-garmin-x15";
const sourceUrls = [
  { code: "G1", title: "Garmin FY2006 8-K 全年財報", url: "https://www.sec.gov/Archives/edgar/data/1121788/000114420407007445/v065417_ex99-1.htm", checked_on: "2026-10-20" },
  { code: "G2", title: "Garmin FY2008 Form 10-K", url: "https://www.sec.gov/Archives/edgar/data/1121788/000114420409010751/v141191_10k.htm", checked_on: "2026-10-20" },
  { code: "G3", title: "Garmin FY2008 8-K 全年財報", url: "https://www.sec.gov/Archives/edgar/data/1121788/000114420409010317/v141019_ex99-1.htm", checked_on: "2026-10-20" },
  { code: "G4", title: "Garmin FY2010 8-K 全年財報", url: "https://www.sec.gov/Archives/edgar/data/1121788/000114420411010322/v212200_ex99-1.htm", checked_on: "2026-10-20" },
  { code: "G5", title: "Garmin FY2011 Form 10-K", url: "https://www.sec.gov/Archives/edgar/data/1121788/000114420412012007/v303209_10k.htm", checked_on: "2026-10-20" },
  { code: "G6", title: "Garmin FY2025 8-K 全年財報", url: "https://www.sec.gov/Archives/edgar/data/1121788/000119312526056025/grmn-ex99_1.htm", checked_on: "2026-10-20" },
];
const allowedRefs = new Set(sourceUrls.map(item => item.code));
const named = /\b(?:Garmin|Forerunner|NAVIGON|Auto OEM)\b|nüvi|佳明|高民環|GPSMAP/iu;
const chapters = Array.from({ length: 6 }, () => ({ title: "", rows: [] }));
const outro = [];
let current = null;
for (const raw of readFileSync(path.join(dir, "drafts/narration.md"), "utf8").split(/\r?\n/)) {
  const header = raw.match(/^## (b0[1-6]|outro):\s*(.*)$/);
  if (header) {
    current = header[1] === "outro" ? outro : chapters[Number(header[1].slice(1)) - 1].rows;
    if (header[1] !== "outro") chapters[Number(header[1].slice(1)) - 1].title = header[2].trim();
    continue;
  }
  if (!/^x15\d{4}\s*\|/.test(raw)) continue;
  const parts = raw.split("|").map(part => part.trim());
  if (!current || parts.length !== 4) throw new Error(`Malformed narration row: ${raw}`);
  const [id, refsText, text, cue] = parts;
  if (!text || !cue) throw new Error(`Missing text/cue: ${id}`);
  if (named.test(cue)) throw new Error(`Visual cue contains a protected name: ${id}`);
  const refs = refsText === "editorial" ? [] : refsText.split(",");
  if (refs.some(ref => !allowedRefs.has(ref))) throw new Error(`Unknown/worker-inaccessible source: ${id} ${refsText}`);
  current.push({ id, refs, text, cue });
}
if (chapters.some(chapter => !chapter.title || chapter.rows.length < 5) || outro.length !== 3) throw new Error("Expected six titled chapters and three closing lines");
const allRows = [...chapters.flatMap(chapter => chapter.rows), ...outro];
if (new Set(allRows.map(row => row.id)).size !== allRows.length) throw new Error("Duplicate narration line ID");
for (const [ci, chapter] of chapters.entries()) {
  for (const [ri, row] of chapter.rows.entries()) {
    const expected = `x15${String(ci + 1).padStart(2, "0")}${String(ri + 1).padStart(2, "0")}`;
    if (row.id !== expected) throw new Error(`Expected ${expected}; found ${row.id}`);
  }
}
for (const [ri, row] of outro.entries()) {
  const expected = `x1506${String(chapters[5].rows.length + ri + 1).padStart(2, "0")}`;
  if (row.id !== expected) throw new Error(`Expected ${expected}; found ${row.id}`);
}

const camera = ["Medium shot, slow push in", "Close-up, static", "Wide shot, slow pan", "Medium close-up, gentle parallax"];
const noText = "No logos, labels, letters, numbers, readable maps, exact product designs, or identifiable real people.";
// A card is inserted only when an editor specifies exact source-backed copy below.
// Key: narration line ID. All other lines use anonymous illustrations.
const cards = new Map(Object.entries({
  // x1503NN: { title: "FY2008", stats: [{ value: "72.65%", label: "automotive/mobile 占公司全年營收" }], source: "Garmin FY2008 8-K" },
}));
const lineFor = row => ({ id: row.id, text: row.text, emotion: row.text.endsWith("？") ? "台灣口語說書，自然提問，正常語速" : "台灣口語說書，日期與數字清楚，正常語速" });
const scenes = chapters.flatMap((chapter, ci) => chapter.rows.map((row, ri) => {
  const id = `x15-b${String(ci + 1).padStart(2, "0")}-s${String(ri + 1).padStart(2, "0")}`;
  const card = cards.get(row.id);
  const scene = card ? { id, template: "stats", data: card, lines: [lineFor(row)] } : {
    id, template: "shot", data: {
      prompt: `${camera[ri % camera.length]}: ${row.cue}. ${noText}`,
      camera: camera[ri % camera.length], visual: "still",
    }, lines: [lineFor(row)],
  };
  if (ri === 0) scene.chapter = chapter.title;
  return scene;
}));
scenes.push({ id: "x15-outro", template: "outro", data: { title: "導航不只在車裡", cta: "訂閱品牌故事" }, lines: outro.map(lineFor) });

// Narrative loops will be anchored to exact new-draft IDs after the writer freezes lines.
const loops = [];
const linePosition = new Map(allRows.map((row, index) => [row.id, index]));
for (const loop of loops) if (!(linePosition.has(loop.setup) && linePosition.has(loop.payoff) && linePosition.get(loop.setup) < linePosition.get(loop.payoff))) throw new Error(`Invalid loop: ${JSON.stringify(loop)}`);

const description = [
  "2008 年 Garmin 有逾七成營收來自 automotive/mobile；2011 年報把手機導航的壓力寫成已使成長停滯。公司後來的總營收為何由五個不同事業構成？本集沿原始 SEC 年報，追專用導航機、運動 GPS 與其他市場的變化。",
  "",
  "2008 automotive/mobile 不是只有車用導航機；2011 手機造成成長停滯是公司的風險披露，不能把 2008–2010 所有收入下滑全歸手機。2025 Auto OEM 不等於舊事業，Fitness／Outdoor 也不等於全部都是手錶。2008、2010、2011、2025 的數字皆是各自財年，非同一年。所有畫面是匿名概念插畫。資料查核：2026-10-20。",
  "",
  "SEC 原始資料：",
  ...sourceUrls.flatMap(source => [source.title, source.url]),
  "",
  "本集主片、兩支 Shorts 及播放清單的真實連結待實際上傳後回填。",
].join("\n");
const video = {
  schema_version: 1, slug, format: "drama", category: "explainer", narration_locale: "zh-TW", target_minutes: [8, 12],
  voice: { provider: "gemini", name: "Sulafat", style: "標準國語，台灣自然口音，像向朋友追一間公司的真實轉折；正常語速，日期、金額與部門名稱清楚。", performance: "2008 的可能與 2011 的已經是公司風險措辭；2008 automotive/mobile 與 2025 Auto OEM 不同口徑。" },
  subtitles: { burn_in: false }, look: { preset: "cute-mystery" }, characters: [],
  series: { slug: "brand-stories-everyday-reversals-extra", episode: 15, chapter: 1 },
  music: { prompt: "light, curious, a little mysterious, no vocals", gain_db: -20, duck_db: -10 },
  loops,
  youtube: { category_id: 27, made_for_kids: false, default_language: "zh-TW", title: "Garmin 一度七成營收靠車用業務，手機來了怎麼辦？｜品牌故事", description, tags: ["Garmin", "品牌故事", "GPS", "導航機", "運動手錶", "年報"], video_id: null },
  thumbnail: { template: "thumb", data: { headline: "**導航機退場？**", tag: "品牌故事", brand: "Garmin", shot: "x15-b01-s01" } },
  sources: sourceUrls.map(({ code, ...source }) => source), assets: [], scenes,
};
const bytes = JSON.stringify(video, null, 2) + "\n";
writeFileSync(path.join(dir, "video.json"), bytes);
const sha = createHash("sha256").update(bytes).digest("hex");
const esc = value => value.replaceAll("|", "\\|");
writeFileSync(path.join(dir, "line-source-matrix.md"), [
  "# X15 Garmin｜逐句作者來源矩陣", "", "由 `compose-video.mjs` 從 `drafts/narration.md` 產生。代碼見 [source-matrix.md](source-matrix.md)；此表須再由獨立來源審查者逐句核對，不能當審查 PASS。", "",
  `- \`video.json\` SHA-256：\`${sha}\``, "", "| 句 ID | 旁白 | 作者來源標記 |", "| --- | --- | --- |",
  ...allRows.map(row => `| \`${row.id}\` | ${esc(row.text)} | ${row.refs.length ? row.refs.join("、") : "敘事提問／概念示意／CTA"} |`), "",
].join("\n"));
writeFileSync(path.join(dir, "script.md"), [
  "# X15 Garmin｜繁中逐句稿", "", `離線前製；\`video.json\` SHA-256：\`${sha}\`。尚未獨立逐句審核、盲讀、TTS 或實際時長測量。第一章後正式 5 秒片頭、末三句後正式 21 秒片尾；兩動畫與末三句不計入實質正文。`, "",
  ...chapters.flatMap((chapter, ci) => [`## 第 ${ci + 1} 章｜${chapter.title}${ci === 0 ? "（濃縮開場）" : ""}`, "", ...chapter.rows.map(row => `- \`${row.id}\` ${row.text}`), ""]),
  "## 片尾三句", "", ...outro.map(row => `- \`${row.id}\` ${row.text}`), "",
].join("\n"));
writeFileSync(path.join(dir, "series.json"), JSON.stringify({ kind: "story", slug: "brand-stories-everyday-reversals-extra", episode: 15, chapter: 1, title: "Garmin：手機導航壓力下的五條營收線", logline: "從 2008 對車用／行動業務的高度依賴，到 2011 手機導航風險成真，以及 2025 五部門的收入結構。", names: ["Garmin", "nüvi", "Forerunner", "Forerunner 610", "Forerunner 910XT", "NAVIGON", "Garmin Fit", "Auto OEM", "GPSMAP"], characters: [], target_minutes: 10, image_model: "image-01", style_preset: "custom", look: { preset: "cute-mystery" }, visual_tier: "stills", compilation: false }, null, 2) + "\n");
const body = chapters.slice(1).flatMap(chapter => chapter.rows).map(row => row.text).join("");
console.log(JSON.stringify({ scenes: scenes.length, shots: scenes.filter(scene => scene.template === "shot").length, cards: scenes.filter(scene => scene.template === "stats").length, spoken_lines: allRows.length, hook_characters: chapters[0].rows.map(row => row.text).join("").length, body_characters: body.length, body_estimate_minutes_at_300_cpm: +(body.length / 300).toFixed(2), loops: loops.length, video_sha256: sha }, null, 2));
