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
  ["x130104", { title: "兩案收購對價", stats: [{ value: "€308m", label: "2019 Anchor＋Gimlet；兩案合計" }], source: "S1｜2019 Q1 6-K" }],
  ["x130315", { title: "整個廣告業務｜2020 Q1 同比", stats: [{ value: "+€22m", label: "收入增額；不是播客獨立收入" }], source: "S2｜2020 Q1 6-K" }],
  ["x130316", { title: "整個廣告業務｜2020 Q1 同比", stats: [{ value: "+€42m", label: "總成本增額；不是播客獨立成本" }], source: "S2｜2020 Q1 6-K" }],
  ["x130319", { title: "播客內容成本｜2020 Q1 同比", stats: [{ value: "+€12m", label: "整個廣告業務成本中的一項；非播客淨利" }], source: "S2｜2020 Q1 6-K" }],
  ["x130403", { title: "部分播客內容資產沖銷", stats: [{ value: "€30m", label: "2023 Q2；非全部播客投資損失" }], source: "S3｜2023 Q2 6-K" }],
  ["x130404", { title: "整個廣告業務毛利率", stats: [{ value: "+1% → −6%", label: "2022 Q2 → 2023 Q2" }], source: "S3｜2023 Q2 6-K" }],
  ["x130501", { title: "整個廣告業務毛利率", stats: [{ value: "−6% → +13%", label: "2023 Q2 → 2024 Q2" }], source: "S5｜2024 Q2 6-K" }],
  ["x130515", { title: "Premium 毛利率", stats: [{ value: "28% → 31%", label: "2023 Q2 → 2024 Q2；非播客單獨毛利" }], source: "S5｜2024 Q2 6-K" }],
  ["x130522", { title: "Spotify 全公司｜2024 全年", stats: [{ value: "首次營業獲利", label: "整家公司全年結果；非播客獨立回報" }], source: "S6｜2024 Q4 earnings exhibit" }],
  ["x130611", { title: "廣告欄的播客成本", stats: [{ value: "−€21m", label: "2025 Q2 同比；Ad-Supported 播客成本" }], source: "S7｜2025 Q2 6-K" }],
]);

const cues = [
  ["an unmarked acquisition folder beside an anonymous creator recording tool on a desk", "fictional creator using a plain microphone and an unbranded distribution tray", "a separate unmarked studio acquisition folder placed beside the first", "a large blank ledger page beside two small folders", "two distinct capability cards, one near recording tools and one near a studio desk", "a content-asset record opens to a covered adjustment field with no visible result", "a sealed whole-company year-end ledger with its result line left blank", "a video cost token poised between two blank service ledgers, not yet assigned", "one anonymous researcher holding an unanswered blank folder"],
  ["two acquisition routes lead to the same unbranded listener player", "anonymous creator records with a plain microphone and carries audio toward a player", "a separate studio desk creates a different anonymous audio card", "two unrelated audio cards from separate desks enter one centered unbranded player", "a listener presses play while two broad service ledgers wait nearby", "an ad coin appears beside a free listening screen and a closed green ledger", "music and audio ad tokens enter one broad green service ledger", "a monthly member coin enters a separate orange service ledger", "two broad service ledgers have no row for either acquisition folder", "creator-tool and content folders beside an empty future-income tray", "an anonymous listener and two purchase folders face an unanswered return tray", "music and audio ad cards enter one broad green ledger", "one monthly member coin serves several unnamed content cards", "plain cash coins and unmarked award tokens side by side", "a purchase-consideration card beside later revenue and operating-cost trays", "a podcast content-cost token approaches the green advertising ledger", "a broad advertising balance remains concealed as the ledger opens"],
  ["the broad green advertising ledger drops below a blank baseline", "a podcast content-cost token joins the broad green ledger", "music, audio and other cost tokens share the same large account", "income coins meet a larger outgoing cost tray within one account", "two broad account trays balanced as an unanswered possibility", "a listener count pile grows faster than incoming ad coins", "podcast content-cost tokens increase beside a growing listener pile", "original acquisition folders stay apart from the broad advertising result", "a missing show-specific results sheet beside the broad advertising ledger", "broad ad revenue and total-cost lanes face each other", "the same green advertising ledger opens to a quarterly page", "free and member listeners hear audio while cost classification stays on one account", "a podcast content-cost token enters the broad green ledger", "a podcast content-cost pile rises from one quarter to another", "incoming ad coins on the broad green ledger", "outgoing total-cost tokens on the same broad green ledger", "two comparable broad-ledger change stacks show the expense side taller", "a covered segment within the broad cost pile asks for its podcast share", "podcast content-cost stack revealed as a subset of broad total cost", "music and other cost tokens remain mixed around the podcast cost subset", "the broad ad account under pressure, with deal folders still separate", "two acquisition folders lack individual advertising-income rows", "a later content-portfolio folder comes onto the desk", "acquisition folders beside a separate portfolio folder with no connecting label"],
  ["a broad podcast content-portfolio folder opens, apart from old acquisition folders", "part of a broad anonymous content-asset stack is removed", "a partial content-asset adjustment card faces the broad portfolio", "two dated broad ad-margin bars occupy one ledger", "a broad advertising cost stack stands higher than its revenue tray", "content-asset, contract and staffing folders appear within one restructuring", "termination papers and empty staff chairs mark separate cost types", "old acquisition folders remain apart from unnamed content-asset cards", "one content-asset card is kept separate from a purchase-consideration card", "blank show identity slots under a broad portfolio folder", "a partial asset adjustment cannot cancel a purchase folder directly", "some anonymous audio cards close without individual names or schedule", "last year's broad ad-margin baseline remains on the desk", "the next year's broad ad ledger arrives beside last year's", "a future cost tray and income tray remain closed", "the prior negative broad margin line faces a still-covered next-year result"],
  ["green advertising ledger with a rising abstract balance", "same green ledger at two distinct dated slots left blank", "a previous-period cost packet kept separate", "a current-period desk without matching packet", "a reduced outgoing-cost pile in the whole ad ledger", "an anonymous producer working with a smaller generic supply stack", "a different licensing-cost tray increases slightly", "accountant turns from costs to incoming coins", "new advertising coins enter green ledger", "music-shaped abstract tiles outside podcast card rack", "two differently coloured advertising trays kept together", "a green ledger showing several factors moving at once", "original acquisition folders remain unanswered beside whole ad ledger", "an orange member ledger with generic music and book shapes", "orange member ledger showing an upward abstract balance", "many unbranded member tokens enter an orange tray", "a subscriber token and an average-revenue token side by side", "incoming member coins grow beside licensing costs", "a generic book-shaped cost tile offsets part of the gain", "two old acquisition folders too small to resolve from broad orange ledger", "a sealed whole-company year-end folder enters the desk", "large whole-company ledger opens in front of researcher", "broad company ledger kept distinct from podcast cards", "one blank podcast-only results sheet still empty", "unbranded audio player remains on an anonymous table", "new unrelated video creator cards appear on a separate workbench", "a researcher asks which of two coloured ledgers receives new costs"],
  ["a green advertising ledger looks deceptively lighter while a new video folder approaches", "an unmarked video creator program folder opens on a desk", "a fictional video creator with a plain camera frame", "creator receives an unmarked compensation token", "anonymous member watches a blank video frame without interruptions", "two separate creator and member cards on a desk", "one historical cost lane sits beside a newly opened member ledger", "one limited video-experience cost token moves to orange member ledger, no member-age grouping", "green ad ledger keeps the remaining generic podcast tokens", "one question folder stands between green and orange ledgers", "a green ledger with smaller podcast cost pile", "an analyst compares one service column against an unseen whole-service total", "one cost token moves between ledgers while the unmeasured remainder stays covered", "blank transfer amount field with no digits or text", "anonymous accountant leaves an unmeasured savings box open", "member income kept apart from podcast-only evidence box", "both ledgers contain several unrelated content token types", "two old acquisition folders lacking individual result sheets", "creator and member on distinct sides of a conceptual service desk", "an unbranded program continues operating beside old acquisition folders", "three separate evidence cards for assets, whole company, and ad service", "three genuine but incompatible evidence cards around one question folder", "anonymous researcher leaves one investment-return answer area empty"],
];
const cueOverrides = new Map([
  ["x130103", "two acquisition folders stacked vertically inside the central frame, one near a creator tool and one near a studio card"],
  ["x130105", "a purchase-price folder faces an empty future-return tray, both centered"],
  ["x130204", "two unrelated anonymous audio cards converge from creator and studio desks into one unbranded player, all centered"],
  ["x130214", "plain cash coins and unmarked award tokens side by side in the central frame"],
  ["x130419", "a later green advertising ledger arrives beside the reorganized content folder"],
  ["x130420", "two still-closed evidence envelopes for prior costs and new ad income"],
  ["x130421", "an analyst holds an empty income tray beside an empty cost tray"],
  ["x130505", "an anonymous accountant examines an ordinary production-cost folder after a prior expense packet"],
  ["x130507", "a lower production-cost tray kept separate from a still-closed advertising-income tray"],
  ["x130513", "several different incoming and outgoing tokens affect one broad green ledger"],
  ["x130516", "a fictional member picks one anonymous audio card while the monthly coin enters a broad service tray"],
  ["x130517", "many anonymous member tokens enter one large orange service tray"],
  ["x130518", "one fictional member's unlabelled reason remains hidden beside an unbranded audio player"],
  ["x130519", "audio, music and book-shaped tiles share one broad member-service ledger"],
  ["x130520", "green and orange quarterly ledgers face one sealed annual company folder"],
  ["x130524", "a new video-creator payment folder appears beside, not inside, an old podcast folder"],
  ["x130525", "a fictional creator and a fictional member stand at two ends of a conceptual video service desk"],
  ["x130526", "one unassigned video-experience cost token waits between green and orange ledgers"],
  ["x130608", "green advertising ledger stacked above orange member ledger in the central frame, one limited video-experience cost token moving between them, no member-age grouping"],
  ["x130610", "green advertising ledger stacked above orange member ledger in the central frame, a blank cost-comparison space between them"],
  ["x130621", "two old acquisition-price folders face separate still-empty lifetime-return trays"],
  ["x130622", "three unrelated evidence cards stop short of the separate acquisition-return trays"],
]);
const camera = ["Medium shot, push in", "Close-up, pull out", "Wide shot, gentle pan left", "Overhead shot, tilt down", "Medium close-up, pan right", "Low-angle shot, lift gently"];
const rooms = ["in an anonymous research room", "in a plain recording booth", "in an accounts library", "along a records aisle", "in a service hall", "beside a review shelf"];
const promptTails = [
  "Anonymous fictional people only; no readable writing, corporate insignia, copyrighted illustrations or celebrity likeness. Reserve open space for editor-applied titles.",
  "All objects are unbranded and without print; avoid numbers, lettering and trademark shapes. Keep the important gesture visible.",
  "Do not imitate a named host, published series imagery, historical contract or company emblem. Place scene elements clearly on camera.",
  "Illustrative, not archival: empty paper surfaces and invented ordinary characters only. Compose a clear action.",
  "No generated glyphs or brand marks; exact dates and figures are added in postproduction as typeset copy.",
  "Unmarked props, generic adults and no protected visual works. Leave clear background for typeset copy.",
];
const portraitTail = " Keep hands and focal props in the central 608-pixel corridor of the 1920x1080 image for 9:16 reframing.";
const shortSourceLines = new Set(["x130101", "x130103", "x130202", "x130203", "x130204", "x130210", "x130214", "x130215", "x130610", "x130603", "x130605", "x130608", "x130614", "x130615"]);
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
      : { id: sceneId, template: "shot", data: { prompt: `${camera[(scenes.length + ci) % camera.length]} ${rooms[ci]}, ${cueOverrides.get(first.id) ?? cues[ci][rows.indexOf(first)]}. ${promptTails[scenes.length % promptTails.length]}${selected.some(row => shortSourceLines.has(row.id)) ? portraitTail : ""}`, camera: camera[(scenes.length + ci) % camera.length], visual: "still" }, lines: selected.map(lineFor) };
    if (shot === 1) scene.chapter = titles[ci];
    scenes.push(scene);
    i += selected.length;
  }
}
scenes.push({ id: "x13-outro", template: "outro", data: { title: "回本，要看對的帳", cta: "訂閱品牌故事" }, lines: outro.map(lineFor) });
const loops = [
  ["x130104", "x130214", "兩案對價不是全額現金"],
  ["x130106", "x130403", "部分內容資產沖銷是三千萬歐元"],
  ["x130107", "x130522", "全公司年度營業結果才在第五章揭曉"],
  ["x130108", "x130608", "新影片觀看體驗的相關成本進Premium"],
  ["x130109", "x130624", "無獨立損益則不能判定兩案回本"],
  ["x130216", "x130301", "整個廣告業務首季毛利轉負"],
  ["x130310", "x130316", "同一廣告業務總成本增額超過收入增額"],
  ["x130318", "x130319", "播客內容成本增額為一千二百萬歐元"],
  ["x130324", "x130401", "重整的是整個播客內容組合，無法指認原兩案"],
  ["x130422", "x130501", "廣告毛利率轉成正十三"],
  ["x130508", "x130510", "音樂廣告是主要廣告增額"],
  ["x130520", "x130522", "首個全年營業獲利屬全公司"],
  ["x130527", "x130613", "廣告欄下降含成本分類變化"],
  ["x130610", "x130611", "廣告欄播客成本同比少兩千一百萬歐元"],
  ["x130623", "x130624", "收購回本無法從公開分類判定"],
].map(([setup, payoff, what]) => ({ setup, payoff, what }));
const position = new Map(allRows.map((row, index) => [row.id, index]));
for (const loop of loops) if (!(position.has(loop.setup) && position.has(loop.payoff) && position.get(loop.setup) < position.get(loop.payoff))) throw new Error(`Broken loop: ${JSON.stringify(loop)}`);

const description = [
  "Spotify 在 2019 年兩天內買進播客創作／發行工具與節目製作公司，兩案收購對價合計 €308m。2023 年公司重整播客內容組合，2024 年又首次實現全公司全年營業獲利。這能證明兩筆收購或播客業務回本嗎？本集沿一手 SEC 原件把每筆數字的期間、範圍和能證明的事分清楚。",
  "",
  "2023 Q2 有部分播客內容資產沖銷，同季也有若干節目關閉；公告沒有逐檔清單，不能回推到當年兩筆收購。2025 年提供給 Premium 會員的新影片觀看體驗，相關播客成本部分改列 Premium；其餘播客內容成本仍在 Ad-Supported。公開報表仍沒有播客獨立損益。畫面是匿名概念插畫，數字卡由後製排版。查核日期：2026-10-20。",
  "",
  "SEC 原始資料：",
  ...sources.map(source => `${source.title}\n${source.url}`),
  "",
  "主片、兩支 Shorts 與播放清單的真實 YouTube 連結待實際上傳後回填。",
].join("\n");
const video = {
  schema_version: 1, slug, format: "drama", category: "explainer", narration_locale: "zh-TW", target_minutes: [8, 12],
  voice: { provider: "gemini", name: "Sulafat", style: "標準國語，台灣自然口音，像向朋友追一筆投資的公開紀錄；日期、季度、業務範圍清楚。", performance: "兩案對價、廣告／會員分類及全公司獲利分開讀；每份新證據帶出一個新問題。" },
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
writeFileSync(path.join(dir, "series.json"), JSON.stringify({ kind: "story", slug: "brand-stories-everyday-reversals-extra", episode: 13, chapter: 1, planned_episodes: 20, title: "Spotify：兩筆播客收購能否判定回本", logline: "從 2019 年兩筆播客收購一路核對 2020 廣告分類、2023 內容重整、2024 全公司獲利與 2025 影片成本改列，釐清公開紀錄能否證明回本。", names: ["Spotify", "Anchor", "Gimlet"], characters: [], target_minutes: 10, image_model: "image-01", style_preset: "custom", look: { preset: "cute-mystery" }, visual_tier: "stills", compilation: false }, null, 2) + "\n");
writeFileSync(path.join(dir, "script.md"), ["# X13 Spotify｜六章繁中逐句稿 v6", "", `離線前製；\`video.json\` SHA-256：\`${hash}\`。未獨立逐句審核、盲評、配音或測量實際時長。濃縮開場後接正式 5 秒片頭；最後三句後接正式 21 秒 v4 片尾。`, "", ...chapters.flatMap((rows, i) => [`## 第 ${i + 1} 章｜${titles[i]}${i === 0 ? "（開場濃縮）" : ""}`, "", ...rows.map(row => `- \`${row.id}\` ${row.text}`), ""]), "## 最後三句", "", ...outro.map(row => `- \`${row.id}\` ${row.text}`), ""].join("\n"));
writeFileSync(path.join(dir, "line-source-matrix.md"), ["# X13 Spotify｜作者逐句來源索引", "", `\`video.json\` SHA-256：\`${hash}\`。作者標記不等於獨立來源審核；來源 URL 與邊界見 [source-matrix.md](source-matrix.md)。`, "", "| 句 ID | 旁白 | 作者來源 |", "| --- | --- | --- |", ...allRows.map(row => `| \`${row.id}\` | ${row.text.replaceAll("|", "\\|")} | ${row.refs.join("、") || "敘事分析／提問"} |`), ""].join("\n"));
console.log(JSON.stringify({ video_sha256: hash, lines: allRows.length, scenes: scenes.length, shots: scenes.filter(scene => scene.template === "shot").length, cards: scenes.filter(scene => scene.template === "stats").length, opening_chars: chapters[0].map(row => row.text).join("").length, body_chars: chapters.slice(1).flat().map(row => row.text).join("").length }, null, 2));
