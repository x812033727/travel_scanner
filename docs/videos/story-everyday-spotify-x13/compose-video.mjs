// Deterministic, offline X13 preproduction compiler. Never calls media or upload providers.
import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const dir = path.dirname(fileURLToPath(import.meta.url));
const slug = "story-everyday-spotify-x13";
const sources = [
  ["S1", "Spotify 2019 Q1 6-K", "https://www.sec.gov/Archives/edgar/data/1639920/000156459019013731/ck0001639920-6k_20190429.htm"],
  ["S2", "Spotify 2020 Q1 6-K", "https://www.sec.gov/Archives/edgar/data/1639920/000156459020019718/ck0001639920-6k_20200429.htm"],
  ["S3", "Spotify 2023 Q2 6-K", "https://www.sec.gov/Archives/edgar/data/1639920/000163992023000010/spot-20230630x6xk.htm"],
  ["S4", "Spotify 2023-12-04 6-K", "https://www.sec.gov/Archives/edgar/data/1639920/000114036123055913/ef20015890_6k.htm"],
  ["S5", "Spotify 2024 Q2 6-K", "https://www.sec.gov/Archives/edgar/data/1639920/000163992024000009/spot-20240630x6xk.htm"],
  ["S6", "Spotify 2024 Q4 earnings exhibit", "https://www.sec.gov/Archives/edgar/data/1639920/000114036125002936/ef20042791_ex99-1.htm"],
  ["S7", "Spotify 2025 Q2 6-K", "https://www.sec.gov/Archives/edgar/data/1639920/000163992025000012/spot-20250630x6xk.htm"],
  ["S8", "Spotify 2026 Q2 6-K", "https://www.sec.gov/Archives/edgar/data/1639920/000162828026052543/spot-20260630x6xk.htm"],
  ["S9", "Spotify 2023-07-25 Q2 earnings exhibit", "https://www.sec.gov/Archives/edgar/data/1639920/000114036123035965/brhc20056303_ex99-1.htm"],
].map(([code, title, url]) => ({ code, title, url, checked_on: "2026-10-20" }));

const sourceRefs = note => {
  const refs = new Set([...note.matchAll(/S([1-9])\s*[–-]\s*S([1-9])/g)].flatMap(([, first, last]) => Array.from({ length: Number(last) - Number(first) + 1 }, (_, i) => `S${Number(first) + i}`)));
  for (const [, number] of note.matchAll(/\bS([1-9])\b/g)) refs.add(`S${number}`);
  return [...refs].sort();
};
const markdown = readFileSync(path.join(dir, "drafts/narration.md"), "utf8");
const chapters = Array.from({ length: 6 }, () => []);
const titles = [];
let chapterIndex = -1;
for (const raw of markdown.split(/\r?\n/)) {
  const heading = raw.match(/^## 第[一二三四五六]章｜(.+)$/);
  if (heading) { chapterIndex += 1; titles.push(heading[1].replace("（開場濃縮）", "")); continue; }
  const match = raw.match(/^- `(x13\d{4})` (.*?)〔([^〕]+)〕$/);
  if (!match) continue;
  if (chapterIndex < 0 || chapterIndex > 5) throw new Error(`Narration line outside chapter: ${raw}`);
  const [, id, text, note] = match;
  if (!id.startsWith(`x13${String(chapterIndex + 1).padStart(2, "0")}`)) throw new Error(`Wrong chapter ID: ${id}`);
  if (text.length > 42) throw new Error(`Narration line over 42 chars: ${id} (${text.length})`);
  chapters[chapterIndex].push({ id, text, note, refs: sourceRefs(note) });
}
if (titles.length !== 6 || chapters.some((rows, i) => rows.length < (i === 0 ? 9 : 16))) throw new Error("Need six complete chapters");
const outro = chapters[5].splice(-3);
if (outro.map(row => row.id).join(",") !== "x130624,x130625,x130626") throw new Error("Expected exactly three ending lines");
const allRows = [...chapters.flat(), ...outro];
if (new Set(allRows.map(row => row.id)).size !== allRows.length) throw new Error("Duplicate line IDs");

const statCards = new Map([
  ["x130104", { title: "兩案收購對價", stats: [{ value: "€308m", label: "Anchor＋Gimlet；含股份獎酬，非純現金" }], source: "S1｜2019 Q1 6-K" }],
  ["x130315", { title: "整個廣告業務｜2020 Q1 同比", stats: [{ value: "+€22m", label: "收入增額；不是播客獨立收入" }], source: "S2｜2020 Q1 6-K" }],
  ["x130316", { title: "整個廣告業務｜2020 Q1 同比", stats: [{ value: "+€42m", label: "總成本增額；不是播客獨立成本" }], source: "S2｜2020 Q1 6-K" }],
  ["x130403", { title: "部分播客內容資產沖銷", stats: [{ value: "€30m", label: "2023 Q2；非全部播客投資損失" }], source: "S3｜2023 Q2 6-K" }],
  ["x130404", { title: "整個廣告業務毛利率", stats: [{ value: "+1% → −6%", label: "2022 Q2 → 2023 Q2" }], source: "S3｜2023 Q2 6-K" }],
  ["x130416", { title: "可用影片播客", stats: [{ value: ">100,000", label: "2023-07-25 公告當時；3 月為 70,000" }], source: "S9｜2023-07-25 earnings exhibit" }],
  ["x130501", { title: "整個廣告業務毛利率", stats: [{ value: "−6% → +13%", label: "2023 Q2 → 2024 Q2" }], source: "S5｜2024 Q2 6-K" }],
  ["x130515", { title: "Premium 毛利率", stats: [{ value: "28% → 31%", label: "2023 Q2 → 2024 Q2；非播客單獨毛利" }], source: "S5｜2024 Q2 6-K" }],
  ["x130611", { title: "廣告欄的播客成本", stats: [{ value: "−€21m", label: "2025 Q2 同比；含分類變動，真節省額未拆" }], source: "S7｜2025 Q2 6-K" }],
]);

const cues = [
  ["two blank acquisition folders on an unmarked office desk", "anonymous office hand placing a plain folder beside another", "two unrelated blank audio cards kept apart", "a large blank ledger page beside two small folders", "an unmarked supply card beside a simple recording setup", "a separate stack of generic content cards partially set aside", "a fresh group of generic video-shaped cards on another table", "a whole-company ledger opened away from the card groups", "one anonymous researcher holding an unanswered blank folder"],
  ["anonymous researcher reopening the two blank folders", "ordinary fictional adult speaking into an unmarked microphone", "anonymous creator using a plain recording console", "a simple unbranded upload control with no legible interface", "a different anonymous studio team planning audio on blank cards", "two visibly separate blank capability cards", "a creator handing an audio card to a blank distribution tray", "a studio producer examining an empty production board", "an open blank results folder with no figures", "a generic listener at an unbranded audio player", "plain audio-card and advertising tokens on separate surfaces", "an anonymous member with a simple audio device", "two separate coloured service folders", "anonymous researcher comparing two blank ledgers", "mixed plain content tokens in two different folders", "a blank question folder between two business ledgers", "a hand separating contract paper from coins"],
  ["the original two abstract contract folders side by side", "blank coin tokens and plain award tokens separated", "a careful accountant setting aside a false cash-only tally", "a blank future-results page attached to two contract folders", "an anonymous researcher lifting a page marked only by blank colour blocks", "a third generic studio card placed well apart from first two", "anonymous studio desk with generic sports-themed shapes but no symbols", "three unrelated blank content groups not merged", "a production room and an unbranded listener space", "two plain trays for money entering and leaving", "a coloured advertising ledger opened beside an audio card", "a member listens on a plain device away from the ad ledger", "a researcher follows one empty cost lane", "content-production props beside an expanding cost pile", "incoming coins placed in a green service tray", "outgoing cost tokens placed in a different green tray", "one anonymous analyst sees cost pile rise faster", "a green ledger showing a downward abstract balance bar", "more incoming coins but an even larger cost pile", "an ordinary listener beside a quiet audio player", "one green ledger closed without a podcast-specific column", "an empty answer box on an anonymous evidence folder", "a later portfolio folder brought onto the desk", "two contract folders held separate from the portfolio folder"],
  ["a distinct new portfolio folder opens on an anonymous desk", "many unrelated blank content cards sorted into groups", "part of a generic asset-card stack moved to a separate tray", "a green service ledger with two unlabelled comparison bars", "an accountant checks a coloured bar below a plain baseline", "three separate plain cost folders without numbers", "a plain contract folder and empty staff chairs kept separate", "a generic content card removed from an asset tray without naming a show", "the original acquisition folders kept far from unnamed content cards", "a partial asset tray with plenty of cards still present", "different investment groups in distinct trays", "anonymous planner rearranging a broad content portfolio", "one blank question folder left open", "a different group of unnamed audio cards set aside", "a darkened blank audio card with no schedule depiction", "many fresh video-shaped cards in their own rack", "two racks separated by a clear gap", "generic asset tray and video rack side by side, never transforming", "a green advertising ledger and orange member ledger placed side by side", "mixed music and audio tokens in each broad service ledger", "an empty podcast-specific results sheet", "anonymous researcher turning to a later green ledger"],
  ["green advertising ledger with a rising abstract balance", "same green ledger at two distinct dated slots left blank", "a previous-period cost packet kept separate", "a current-period desk without matching packet", "a reduced outgoing-cost pile in the whole ad ledger", "an anonymous producer working with a smaller generic supply stack", "a different licensing-cost tray increases slightly", "accountant turns from costs to incoming coins", "new advertising coins enter green ledger", "music-shaped abstract tiles outside podcast card rack", "two differently coloured advertising trays kept together", "a green ledger showing several factors moving at once", "original acquisition folders remain unanswered beside whole ad ledger", "an orange member ledger with generic music and book shapes", "orange member ledger showing an upward abstract balance", "many unbranded member tokens enter an orange tray", "a subscriber token and an average-revenue token side by side", "incoming member coins grow beside licensing costs", "a generic book-shaped cost tile offsets part of the gain", "two old acquisition folders too small to resolve from broad orange ledger", "a sealed whole-company year-end folder enters the desk", "large whole-company ledger opens in front of researcher", "broad company ledger kept distinct from podcast cards", "one blank podcast-only results sheet still empty", "unbranded audio player remains on an anonymous table", "new unrelated video creator cards appear on a separate workbench", "a researcher asks which of two coloured ledgers receives new costs"],
  ["the orange member ledger opens to a new blank page", "four generic market blocks on an anonymous map", "a fictional video creator with a plain camera frame", "creator receives an unmarked compensation token", "anonymous member watches a blank video frame without interruptions", "two separate creator and member cards on a desk", "nine more generic market blocks join separate group", "orange member ledger receives one limited cost token", "green ad ledger keeps the remaining generic podcast tokens", "one question folder stands between green and orange ledgers", "a green ledger with smaller podcast cost pile", "an analyst pauses before treating a smaller pile as savings", "a cost token changes ledgers while another disappears", "blank transfer amount field with no digits or text", "anonymous accountant refuses to close a premature savings box", "member income kept apart from podcast-only evidence box", "both ledgers contain several unrelated content token types", "empty podcast-only net result sheet remains unfilled", "creator and member on distinct sides of a conceptual service desk", "old acquisition folders beside new creator-payment cards, not physically linked", "an investment folder and a whole-company ledger kept separate", "several genuine but incompatible evidence cards around one question folder", "anonymous researcher leaves the answer area empty"],
];
const camera = ["Medium shot, push in", "Close-up, pull out", "Wide shot, gentle pan left", "Overhead shot, tilt down", "Medium close-up, pan right", "Low-angle shot, lift gently"];
const rooms = ["at an anonymous research desk", "in a plain recording booth", "in an accounts library", "along an archive aisle", "in a media studio", "beside a conceptual desk"];
const promptTails = [
  "Anonymous fictional people only; no readable writing, corporate insignia, program cover or celebrity likeness. Reserve open space for editor-applied titles.",
  "All objects are unbranded and without print; avoid numbers, lettering and trademark shapes. Keep the important gesture visible.",
  "Do not imitate a named host, actual show artwork, historical contract or company emblem. Place scene elements clearly on camera.",
  "Illustrative, not archival: empty paper surfaces and invented ordinary characters only. Compose a clear action.",
  "No generated glyphs or brand marks; exact dates and figures are added in postproduction as typeset copy.",
  "Unmarked props, generic adults and no protected cover art. Leave clear background for typeset copy.",
];
const portraitTail = " Keep hands and focal props in the central 608-pixel corridor of the 1920x1080 image for 9:16 reframing.";
const shortSourceLines = new Set(["x130101", "x130103", "x130203", "x130205", "x130207", "x130206", "x130302", "x130304", "x130610", "x130603", "x130605", "x130608", "x130609", "x130613", "x130614", "x130615"]);
const lineFor = row => ({ id: row.id, text: row.text, pause_after_ms: 0, emotion: row.text.endsWith("？") ? "台灣國語自然說書，問題落地稍停" : "台灣國語自然說書，年份與分母清楚" });
const scenes = [];
for (const [ci, rows] of chapters.entries()) {
  let shot = 0;
  for (let i = 0; i < rows.length;) {
    const first = rows[i], second = rows[i + 1];
    const pair = second && !statCards.has(first.id) && !statCards.has(second.id) && !shortSourceLines.has(first.id) && !shortSourceLines.has(second.id) && first.text.length + second.text.length <= 34;
    const selected = pair ? [first, second] : [first];
    const sceneId = `x13-b${String(ci + 1).padStart(2, "0")}-s${String(++shot).padStart(2, "0")}`;
    const card = statCards.get(first.id);
    const scene = card
      ? { id: sceneId, template: "stats", data: card, lines: selected.map(lineFor) }
      : { id: sceneId, template: "shot", data: { prompt: `${camera[(scenes.length + ci) % camera.length]} ${rooms[ci]}, ${cues[ci][rows.indexOf(first)]}. ${promptTails[scenes.length % promptTails.length]}${selected.some(row => shortSourceLines.has(row.id)) ? portraitTail : ""}`, camera: camera[(scenes.length + ci) % camera.length], visual: "still" }, lines: selected.map(lineFor) };
    if (shot === 1) scene.chapter = titles[ci];
    scenes.push(scene);
    i += selected.length;
  }
}
scenes.push({ id: "x13-outro", template: "outro", data: { title: "回本，要看對的帳", cta: "訂閱品牌故事" }, lines: outro.map(lineFor) });
const loops = [
  ["x130104", "x130303", "兩案對價不是全額現金"],
  ["x130106", "x130403", "部分內容資產沖銷是三千萬歐元"],
  ["x130107", "x130416", "七月公告時可用影片播客逾十萬"],
  ["x130109", "x130624", "無獨立損益則不能判定兩案回本"],
  ["x130216", "x130322", "廣告分類交不出兩案回本數"],
  ["x130324", "x130409", "沖銷不能指認原兩案失敗"],
  ["x130413", "x130416", "七月仍有逾十萬可用影片播客"],
  ["x130422", "x130501", "廣告毛利率轉成正十三"],
  ["x130508", "x130510", "音樂廣告是主要廣告增額"],
  ["x130521", "x130522", "首個全年營業獲利屬全公司"],
  ["x130527", "x130601", "新會員影片相關成本進Premium"],
  ["x130610", "x130613", "廣告欄下降含成本分類變化"],
  ["x130623", "x130624", "收購回本無法從公開分類判定"],
].map(([setup, payoff, what]) => ({ setup, payoff, what }));
const position = new Map(allRows.map((row, index) => [row.id, index]));
for (const loop of loops) if (!(position.has(loop.setup) && position.has(loop.payoff) && position.get(loop.setup) < position.get(loop.payoff))) throw new Error(`Broken loop: ${JSON.stringify(loop)}`);

const description = [
  "Spotify 在 2019 年兩天內買進播客創作／發行工具與節目製作公司，兩案收購對價合計 €308m。2023 年公司重整播客內容組合，2024 年又首次實現全公司全年營業獲利。這能證明兩筆收購或播客業務回本嗎？本集沿一手 SEC 原件把每筆數字的期間、範圍和能證明的事分清楚。",
  "",
  "2023 Q2 有部分播客內容資產沖銷；2023-07-25 發布的更新說當時可用影片播客逾十萬，不代表截至 Q2 末已達此數。2025 年部分合格影片播客體驗相關成本轉列 Premium，公開報表仍沒有播客獨立損益。畫面是匿名概念插畫，數字卡由後製排版。查核日期：2026-10-20。",
  "",
  "SEC 原始資料：",
  ...sources.map(source => `${source.title}\n${source.url}`),
  "",
  "主片、兩支 Shorts 與播放清單的真實 YouTube 連結待實際上傳後回填。",
].join("\n");
const video = {
  schema_version: 1, slug, format: "drama", category: "explainer", narration_locale: "zh-TW", target_minutes: [8, 12],
  voice: { provider: "gemini", name: "Sulafat", style: "標準國語，台灣自然口音，像向朋友追一筆投資的公開紀錄；日期、季度、業務範圍清楚。", performance: "兩案對價、廣告／會員分類及全公司獲利分開讀；留住每次未能蓋回本章的問題。" },
  subtitles: { burn_in: false }, look: { preset: "cute-mystery" }, characters: [],
  series: { slug: "brand-stories-everyday-reversals-extra", episode: 13, chapter: 1 },
  music: { prompt: "light, curious, a little mysterious, no vocals", gain_db: -20, duck_db: -10 }, loops,
  youtube: { category_id: 27, made_for_kids: false, default_language: "zh-TW", title: "Spotify 買兩家播客公司，財報能證明回本嗎？｜品牌故事", description, tags: ["Spotify", "播客", "品牌故事", "Anchor", "Gimlet", "商業故事"], video_id: null },
  thumbnail: { template: "thumb", data: { headline: "播客\n回本？", tag: "品牌故事", brand: "Spotify", shot: "x13-b01-s01" } },
  sources: sources.map(({ code, ...source }) => source), assets: [], scenes,
};
const bytes = JSON.stringify(video, null, 2) + "\n";
writeFileSync(path.join(dir, "video.json"), bytes);
const hash = createHash("sha256").update(bytes).digest("hex");
writeFileSync(path.join(dir, "series.json"), JSON.stringify({ kind: "story", slug: "brand-stories-everyday-reversals-extra", episode: 13, chapter: 1, planned_episodes: 20, title: "Spotify：兩筆播客收購能否判定回本", logline: "從 2019 年兩筆播客收購一路核對 2020 廣告分類、2023 內容重整、2024 全公司獲利與 2025 影片成本改列，釐清公開紀錄能否證明回本。", names: ["Spotify", "Anchor", "Gimlet", "The Ringer"], characters: [], target_minutes: 10, image_model: "image-01", style_preset: "custom", look: { preset: "cute-mystery" }, visual_tier: "stills", compilation: false }, null, 2) + "\n");
writeFileSync(path.join(dir, "script.md"), ["# X13 Spotify｜六章繁中逐句稿 v4", "", `離線前製；\`video.json\` SHA-256：\`${hash}\`。未獨立逐句審核、盲評、配音或測量實際時長。濃縮開場後接正式 5 秒片頭；最後三句後接正式 21 秒 v4 片尾。`, "", ...chapters.flatMap((rows, i) => [`## 第 ${i + 1} 章｜${titles[i]}${i === 0 ? "（開場濃縮）" : ""}`, "", ...rows.map(row => `- \`${row.id}\` ${row.text}`), ""]), "## 最後三句", "", ...outro.map(row => `- \`${row.id}\` ${row.text}`), ""].join("\n"));
writeFileSync(path.join(dir, "line-source-matrix.md"), ["# X13 Spotify｜作者逐句來源索引", "", `\`video.json\` SHA-256：\`${hash}\`。作者標記不等於獨立來源審核；來源 URL 與邊界見 [source-matrix.md](source-matrix.md)。`, "", "| 句 ID | 旁白 | 作者來源 |", "| --- | --- | --- |", ...allRows.map(row => `| \`${row.id}\` | ${row.text.replaceAll("|", "\\|")} | ${row.refs.join("、") || "敘事分析／提問"} |`), ""].join("\n"));
console.log(JSON.stringify({ video_sha256: hash, lines: allRows.length, scenes: scenes.length, shots: scenes.filter(scene => scene.template === "shot").length, cards: scenes.filter(scene => scene.template === "stats").length, opening_chars: chapters[0].map(row => row.text).join("").length, body_chars: chapters.slice(1).flat().map(row => row.text).join("").length }, null, 2));
