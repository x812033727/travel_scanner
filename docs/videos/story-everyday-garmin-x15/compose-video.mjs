// Deterministic offline preproduction build. Never imports a story or calls a media provider.
import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { textHash } from "../../../tools/video/core/schema.mjs";

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

const camera = ["Medium shot, push in", "Close-up, pull out", "Wide shot, pan left", "Medium close-up, pan right", "Overhead shot, tilt down", "Low-angle shot, tilt up"];
const light = ["Mild glow from a side window", "Soft grey morning light", "Overcast afternoon sky", "Muted skylight", "Gentle indoor light", "Soft evening light"];
const safeguards = [
  "Displays show plain colour fields; no logos or legible lettering.",
  "Paper surfaces have unreadable shapes; no brand marks or realistic machine styling.",
  "Any maps are schematic and unlabeled; no trademarks.",
  "All objects remain general, with no readable inscriptions or real model contours.",
];
const humanAction = cue => {
  if (/boat|chartplotter|sea/.test(cue)) return ["on a small plain boat", "sailor", "touching a plain console"];
  if (/cockpit|aircraft/.test(cue)) return ["in a simple aircraft cockpit", "pilot", "looking down at a plain instrument panel"];
  if (/mountain|trail|hiker|outdoor/.test(cue)) return ["on a winding trail", "hiker", "holding a plain handheld receiver"];
  if (/running|runner|track|fitness|watch|sport/.test(cue)) return ["beside a running track", "runner", "checking a plain wrist receiver"];
  if (/truck|dashboard|steering|car|vehicle|road/.test(cue)) return ["in a plain parked vehicle", "driver", "holding a small route screen"];
  if (/phone|smartphone/.test(cue)) return ["at a plain workbench", "customer", "holding a plain phone"];
  if (/shelf|boxes|cartons|warehouse|device/.test(cue)) return ["at an anonymous electronics shop", "clerk", "lifting a plain equipment box"];
  return ["at an archive desk", "analyst", "turning an unwritten annual-report page"];
};
// Each numerical card is hand-written from G1–G6, then anchored to one exact
// narration beat. Matching a unique phrase keeps IDs stable if a hook moves.
const cardRules = [
  [/全公司收入約十七億七千萬美元/, { title: "2006 全年營收", stats: [{ value: "約 US$1.77bn", label: "全公司收入，非淨利" }], source: "G1｜Garmin FY2006 8-K" }],
  [/那一欄達到約十一億美元/, { title: "2006 車用／行動事業", stats: [{ value: "約 US$1.10bn", label: "全年營收；年增 170%" }], source: "G1｜Garmin FY2006 8-K" }],
  [/二〇〇六年，這系列占全公司收入約兩成八/, { title: "nüvi 占全公司收入", stats: [{ value: "約 28%", label: "2006 全年；不是市場占有率" }], source: "G2｜Garmin FY2008 10-K" }],
  [/隔年，比例跳到五成二/, { title: "nüvi 占全公司收入", stats: [{ value: "約 52%", label: "2007 全年；不是事業占比" }], source: "G2｜Garmin FY2008 10-K" }],
  [/答案，是百分之六十四/, { title: "nüvi 占全公司收入", stats: [{ value: "約 64%", label: "2008 全年；屬於車用／行動事業的一部分" }], source: "G2｜Garmin FY2008 10-K" }],
  [/占公司全年收入，大約百分之七十三/, { title: "2008 車用／行動事業", stats: [{ value: "72.65%", label: "US$2,538.411m ÷ US$3,494.077m" }], source: "G3｜Garmin FY2008 8-K；本包計算" }],
  [/二〇一〇年，車用與行動收入約十六億七千萬/, { title: "車用／行動事業全年營收", stats: [{ value: "US$2.538bn", label: "2008" }, { value: "US$1.669bn", label: "2010；兩年對照，非 2010 年比" }], source: "G3/G4｜Garmin FY2008/FY2010 8-K" }],
  [/全公司收入也從約三十五億，降到約二十七億/, { title: "全公司全年營收", stats: [{ value: "US$3.494bn", label: "2008" }, { value: "US$2.690bn", label: "2010；名目美元" }], source: "G3/G4｜Garmin FY2008/FY2010 8-K" }],
  [/nüvi 占全公司收入的比重，變成約四成八/, { title: "nüvi 占全公司收入", stats: [{ value: "約 48%", label: "2011 全年；非整個車用／行動事業" }], source: "G5｜Garmin FY2011 10-K" }],
  [/那個事業當年仍占約五成八/, { title: "車用／行動事業占全公司收入", stats: [{ value: "約 58%", label: "2011 全年；分子不同於 nüvi" }], source: "G5｜Garmin FY2011 10-K" }],
  [/健身事業，收入增加百分之二十四/, { title: "2011 Fitness 事業", stats: [{ value: "+24%", label: "全年營收年比；非兩款錶銷量" }], source: "G5｜Garmin FY2011 10-K" }],
  [/戶外事業也增加百分之十四/, { title: "2011 Outdoor 事業", stats: [{ value: "+14%", label: "全年營收年比；非兩款錶銷量" }], source: "G5｜Garmin FY2011 10-K" }],
  [/最上方的總收入，約七十二億五千萬美元/, { title: "2025 全年營收", stats: [{ value: "US$7.245519bn", label: "全公司收入，非淨利" }], source: "G6｜Garmin FY2025 8-K" }],
  [/最大一欄叫健身，約二十三億六千萬/, { title: "2025 Fitness 事業", stats: [{ value: "US$2.357bn", label: "全年營收；非只有手錶" }], source: "G6｜Garmin FY2025 8-K" }],
  [/戶外也有約二十億五千萬/, { title: "2025 Outdoor 事業", stats: [{ value: "US$2.054061bn", label: "全年營收；非只有手錶" }], source: "G6｜Garmin FY2025 8-K" }],
  [/航海事業，超過十一億美元/, { title: "2025 Marine 事業", stats: [{ value: "US$1.182615bn", label: "全年營收" }], source: "G6｜Garmin FY2025 8-K" }],
  [/飛航事業，將近十億美元/, { title: "2025 Aviation 事業", stats: [{ value: "US$987.161m", label: "全年營收" }], source: "G6｜Garmin FY2025 8-K" }],
  [/它這一年收入約六億六千萬美元/, { title: "2025 Auto OEM 事業", stats: [{ value: "US$664.682m", label: "全年營收；不可直接對比舊事業" }], source: "G6｜Garmin FY2025 8-K" }],
];
const cards = new Map();
for (const [pattern, data] of cardRules) {
  const matches = allRows.filter(row => pattern.test(row.text));
  if (matches.length !== 1) throw new Error(`Card anchor must match one narration line: ${pattern} (${matches.length})`);
  cards.set(matches[0].id, data);
}
const sayWords = [
  ["Garmin Fit", "嘎明菲特"], ["Auto OEM", "車廠供應部門"],
  ["Forerunner", "佛瑞納"], ["NAVIGON", "納維根"],
  ["Garmin", "嘎明"], ["nüvi", "紐維"], ["GPS", "G P S"], ["XT", "艾克斯提"],
];
const lineFor = row => {
  const line = { id: row.id, text: row.text, emotion: row.text.endsWith("？") ? "台灣口語說書，自然提問，正常語速" : "台灣口語說書，日期與數字清楚，正常語速" };
  const say = sayWords.reduce((value, [written, spoken]) => value.replaceAll(written, spoken), row.text);
  if (say !== row.text) Object.assign(line, { say, say_for: textHash(row.text) });
  return line;
};
const scenes = [];
let shotNo = 0;
for (const [ci, chapter] of chapters.entries()) {
  let sceneNo = 0;
  for (let ri = 0; ri < chapter.rows.length;) {
    const current = chapter.rows[ri];
    const next = chapter.rows[ri + 1];
    const canPair = Boolean(next && !cards.has(current.id) && !cards.has(next.id) && current.text.length + next.text.length <= 36);
    const selected = canPair ? [current, next] : [current];
    const id = `x15-b${String(ci + 1).padStart(2, "0")}-s${String(++sceneNo).padStart(2, "0")}`;
    const card = cards.get(current.id);
    const visualCue = selected.map(row => row.cue.replace(/\bgeneric\b/g, "plain").replace(/\bdevices\b/g, "units").replace(/\bdevice\b/g, "unit")).join("; ");
    const [setting, role, action] = humanAction(visualCue);
    const shotIndex = card ? shotNo : shotNo++;
    const orientation = shotIndex % 4 === 0 ? `one anonymous ${role} facing the viewer and ${action}` : `one anonymous ${role} ${action}`;
    const scene = card ? { id, template: "stats", data: card, lines: selected.map(lineFor) } : {
      id, template: "shot", data: {
        prompt: `${camera[shotIndex % camera.length]} ${setting}, ${orientation}. ${visualCue}. ${light[shotIndex % light.length]}. ${safeguards[shotIndex % safeguards.length]}`,
        camera: camera[shotIndex % camera.length], visual: "still",
      }, lines: selected.map(lineFor),
    };
    if (sceneNo === 1) scene.chapter = chapter.title;
    scenes.push(scene);
    ri += selected.length;
  }
}
scenes.push({ id: "x15-outro", template: "outro", data: { title: "導航不只在車裡", cta: "訂閱品牌故事" }, lines: outro.map(lineFor) });

// Setups point to a withheld outcome, with the answer in the actual line named
// by payoff. Keep the opening's later moments open through the six-chapter body.
const loops = [
  { setup: "x150106", payoff: "x150206", what: "開場車用收入急升的幅度" },
  { setup: "x150107", payoff: "x150401", what: "開場同一事業兩年後降到多少" },
  { setup: "x150108", payoff: "x150510", what: "開場運動錶如何接到另一事業收入" },
  { setup: "x150109", payoff: "x150606", what: "開場多年後總營收是否約兩倍" },
  { setup: "x150110", payoff: "x150635", what: "收入後來分布在哪些事業" },
  { setup: "x150209", payoff: "x150214", what: "當年最醒目的車用產品系列" },
  { setup: "x150231", payoff: "x150301", what: "nüvi 在 2008 占全公司營收多少" },
  { setup: "x150308", payoff: "x150310", what: "2008 警訊是否等於當年貨賣不動" },
  { setup: "x150335", payoff: "x150401", what: "高度依賴的車用事業能否維持原營收" },
  { setup: "x150423", payoff: "x150426", what: "2011 年報的風險措辭怎麼變" },
  { setup: "x150509", payoff: "x150510", what: "運動錶以外健身事業當年是否成長" },
  { setup: "x150543", payoff: "x150601", what: "哪張全年表能看之後的收入分布" },
  { setup: "x150607", payoff: "x150629", what: "2025 是否仍是一個車用大欄撐收入" },
  { setup: "x150612", payoff: "x150616", what: "2025 全年能否只用手錶解釋" },
  { setup: "x150625", payoff: "x150626", what: "舊七成能否與新 Auto OEM 直線比較" },
];
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
  thumbnail: { template: "thumb", data: { headline: "導航機退場？", tag: "品牌故事", brand: "Garmin", shot: "x15-b01-s01" } },
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
