// Offline compilation only: no media provider, paid call, host import, or upload.
import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { textHash } from "../../../tools/video/core/schema.mjs";

const dir = path.dirname(fileURLToPath(import.meta.url));
const slug = "story-everyday-krispy-kreme-x18";
const sourceRows = [
  ["S1", "2024-03-26 joint national expansion announcement", "https://www.sec.gov/Archives/edgar/data/1857154/000185715424000029/exhibit991newsrelease.htm"],
  ["S2", "2024 Q3 results and October rollout", "https://www.sec.gov/Archives/edgar/data/1857154/000185715424000110/exh991q3pressrelease2024.htm"],
  ["S3", "2024 Q4 results and over 1,900 restaurants", "https://www.sec.gov/Archives/edgar/data/1857154/000185715425000009/exh991q4pressrelease2024.htm"],
  ["S4", "2025 Q1 results and rollout reassessment", "https://www.sec.gov/Archives/edgar/data/1857154/000119312525115450/d129226dex991.htm"],
  ["S5", "2025-06-23 joint termination announcement", "https://www.sec.gov/Archives/edgar/data/1857154/000185715425000102/a991pressrelease-june2025.htm"],
  ["S6", "2025 Q2 results and June 29 point-of-access cutoff", "https://www.sec.gov/Archives/edgar/data/1857154/000185715425000125/exh991q2pressrelease2025.htm"],
  ["S7", "2025 Q3 results and post-exit quarter", "https://www.sec.gov/Archives/edgar/data/1857154/000185715425000138/exh991q3pressrelease2025.htm"],
  ["S8", "2025 full-year results", "https://www.sec.gov/Archives/edgar/data/1857154/000185715426000012/exh991q4pressrelease2025.htm"],
];
const sources = sourceRows.map(([code, title, url]) => ({ code, title, url, checked_on: "2026-10-20" }));
const knownSources = new Set(sources.map(source => source.code));
const chapters = Array.from({ length: 6 }, () => []);
const titles = [];
const outro = [];
let section = -1;
for (const raw of readFileSync(path.join(dir, "drafts/narration.md"), "utf8").split(/\r?\n/)) {
  const header = raw.match(/^## (b0[1-6]|outro):\s*(.*)$/);
  if (header) {
    section = header[1] === "outro" ? 6 : Number(header[1].slice(1)) - 1;
    if (section < 6) titles[section] = header[2].replace("（濃縮開場）", "");
    continue;
  }
  if (!/^x18\d{4}\s*\|/.test(raw)) continue;
  const parts = raw.split("|").map(part => part.trim());
  if (parts.length !== 4 || section < 0) throw new Error(`Malformed narration row: ${raw}`);
  const [id, refsText, narration, cue] = parts;
  const chapterNumber = section === 6 ? 6 : section + 1;
  if (!id.startsWith(`x18${String(chapterNumber).padStart(2, "0")}`)) throw new Error(`Wrong chapter ID: ${id}`);
  if (!narration || !cue || narration.length > 48) throw new Error(`Missing or overlong narration line: ${id}`);
  if (/Krispy|Kreme|McDonald|Insomnia|logo|logotype|trademark|brand|readable|lettering/iu.test(cue)) throw new Error(`Protected or text-generating visual cue: ${id}`);
  const refs = refsText === "editorial" ? [] : refsText.split(",");
  if (refs.some(ref => !knownSources.has(ref))) throw new Error(`Unknown source: ${id}`);
  (section === 6 ? outro : chapters[section]).push({ id, narration, refs, cue });
}
if (chapters.some((chapter, i) => !titles[i] || chapter.length < 8) || outro.length !== 3) throw new Error("Six chapters and exactly three closing lines required");
const allRows = [...chapters.flat(), ...outro];
if (new Set(allRows.map(row => row.id)).size !== allRows.length) throw new Error("Duplicate line ID");
for (const chapter of [...chapters, outro]) for (let i = 1; i < chapter.length; i++) if (chapter[i].id <= chapter[i - 1].id) throw new Error(`Unordered line ID: ${chapter[i].id}`);
const openingChars = chapters[0].map(row => row.narration).join("").length;
const bodyChars = chapters.slice(1).flat().map(row => row.narration).join("").length;
if (openingChars < 150 || openingChars > 300 || bodyChars < 2450) throw new Error(`Paper runtime outside bounds: opening=${openingChars}, body=${bodyChars}`);

const cardRules = new Map([
  ["x180212", { title: "2024 年全國計畫", stats: [{ value: "2026 年底", label: "預期全國參與門市供應；不是完成日" }], source: "S1｜2024-03-26" }],
  ["x180313", { title: "已實現的合作進度", stats: [{ value: "> 1,900 家", label: "截至 2024-12-29，每日配送的 McDonald’s 門市" }], source: "S3｜2024 Q4" }],
  ["x180401", { title: "三月末進度", stats: [{ value: "> 2,400 家", label: "截至 2025-03-30；五月公告同時重估部署" }], source: "S4｜2025 Q1" }],
  ["x180502", { title: "雙方共同終止", stats: [{ value: "2025-07-02", label: "合作終止生效；六月二十三日公告" }], source: "S5｜2025-06-23" }],
]);
for (const id of cardRules.keys()) if (!allRows.some(row => row.id === id)) throw new Error(`Missing card anchor: ${id}`);
const shortCues = [
  "plain doughnut tray beside unmarked breakfast counter", "small group of storefronts on simple map",
  "many storefront dots spread on blank map", "sealed plain doughnut trays beside a kitchen door",
  "growing map with calendar page curling", "two unsigned business ledgers side by side",
  "unit-cost bars beside blank demand marks", "delivery route ends at closed generic counter",
  "calendar page near doughnut ledger", "lit anonymous counters beneath a quarter-end marker",
  "distinct storefront types encircle one plain tray", "single route fades from anonymous breakfast map",
  "closed route chart beside an opening later-quarter folder", "two total-map ledgers kept apart",
  "new quarter-end map with fewer dots",
  "unmarked breakfast counter and folded route map, no tray remains",
];
for (const cue of shortCues) if (allRows.filter(row => row.cue.includes(cue)).length !== 1) throw new Error(`Missing or duplicate Shorts cue: ${cue}`);
const shortAnchors = new Set(allRows.filter(row => shortCues.some(cue => row.cue.includes(cue))).map(row => row.id));
for (const id of shortAnchors) if (cardRules.has(id)) throw new Error(`Shorts anchor cannot be a stat card: ${id}`);
const singles = new Set([...shortAnchors, ...cardRules.keys(), ...chapters.map(chapter => chapter[0].id), ...chapters.map(chapter => chapter.at(-1).id)]);
const cameras = ["Medium shot, gentle push in", "Close-up, soft pull out", "Wide shot, pan left", "Overhead shot, pan right", "Medium close-up, still", "Low-angle shot, tilt up"];
const places = ["an anonymous morning shop", "a plain distribution wall", "a generic city delivery route", "a quiet scheduling nook", "an anonymous two-company records shelf", "a quiet quarter-end accounting nook"];
const lights = ["soft morning window light", "diffuse daylight", "warm overcast light", "muted afternoon light", "warm task light", "soft evening light"];
const placeFor = (row, ci) => {
  const cue = row.cue;
  if (/counter|breakfast|storefront|restaurant/i.test(cue)) return "an anonymous food-service interior";
  if (/production|equipment|training|rack|kitchen|cart/i.test(cue)) return "a plain production and loading room";
  if (/route|street|city|delivery/i.test(cue)) return "a delivery staging area";
  if (/map|calendar|ledger|report|folder|notice|shelf/i.test(cue)) return ci % 2 ? "a plain records room" : "a small archive shelf";
  return places[ci];
};
const protections = [
  "No logos, signage, uniforms, labels, numbers, or readable lettering.",
  "Fictional anonymous setting; no real-person faces or identifiable chain design.",
  "All paper and packaging unprinted; precise figures are native postproduction cards.",
  "No trademarks, store architecture, menu graphics, or branded colors.",
];
const toLine = row => {
  const line = { id: row.id, text: row.narration, pause_after_ms: 0, emotion: row.narration.endsWith("？") ? "台灣自然國語說書；問句停半拍" : "台灣自然國語說書；清楚區分預期、已達與終止生效" };
  if (/Krispy Kreme|Insomnia Cookies|EBITDA|GAAP/.test(row.narration)) {
    line.say = row.narration.replaceAll("Krispy Kreme", "克里斯皮克林").replaceAll("Insomnia Cookies", "因索姆尼亞餅乾").replaceAll("EBITDA", "伊比達").replaceAll("GAAP", "蓋普");
    line.say_for = textHash(row.narration);
  }
  return line;
};
const scenes = [];
let shotCount = 0;
for (const [ci, chapter] of chapters.entries()) {
  let si = 0;
  for (let ri = 0; ri < chapter.length;) {
    const row = chapter[ri];
    const next = chapter[ri + 1];
    const pair = Boolean(next && !singles.has(row.id) && !singles.has(next.id) && !row.narration.endsWith("？") && !next.narration.endsWith("？") && row.narration.length + next.narration.length <= 38);
    const selected = pair ? [row, next] : [row];
    const sceneId = `x18-b${String(ci + 1).padStart(2, "0")}-s${String(++si).padStart(2, "0")}`;
    let scene;
    if (cardRules.has(row.id)) {
      scene = { id: sceneId, template: "stats", data: { ...cardRules.get(row.id), visual_note: "Exact dates and figures typeset in postproduction over neutral doughnut-and-route shapes." }, lines: selected.map(toLine) };
    } else {
      const i = shotCount++;
      const portrait = shortAnchors.has(row.id) ? " Keep the action inside the central 608-pixel corridor of a 1920x1080 frame for 9:16 crop." : "";
      const prompt = `${cameras[i % cameras.length]} at ${placeFor(row, ci)}; ${row.cue}; ${lights[i % lights.length]}.${portrait} ${protections[i % protections.length]}`;
      scene = { id: sceneId, template: "shot", data: { prompt, camera: cameras[i % cameras.length], visual: "still" }, lines: selected.map(toLine) };
    }
    if (si === 1) scene.chapter = titles[ci];
    scenes.push(scene);
    ri += selected.length;
  }
}
scenes.push({ id: "x18-outro", template: "outro", data: { title: "那條餐盤路線，收在七月", cta: "訂閱品牌故事" }, lines: outro.map(toLine) });
const loops = [
  { setup: "x180105", payoff: "x180301", what: "十月地圖先到芝加哥" },
  { setup: "x180106", payoff: "x180403", what: "春天重估部署時程" },
  { setup: "x180107", payoff: "x180501", what: "六月的另一份公告" },
  { setup: "x180109", payoff: "x180513", what: "每天送達與單店需求的問題" },
  { setup: "x180204", payoff: "x180207", what: "合作櫃台多久補進新鮮甜甜圈" },
  { setup: "x180209", payoff: "x180218", what: "新合作門市接入既有配送網的預期效益" },
  { setup: "x180216", payoff: "x180308", what: "擴張準備費用落在哪本帳" },
  { setup: "x180224", payoff: "x180301", what: "第一條全國路線在哪座城市" },
  { setup: "x180311", payoff: "x180313", what: "近兩千店預測是否達成" },
  { setup: "x180320", payoff: "x180513", what: "每店需求與每日配送的帳" },
  { setup: "x180407", payoff: "x180408", what: "新櫃台留白的近期安排" },
  { setup: "x180422", payoff: "x180501", what: "六月合作的去向" },
  { setup: "x180505", payoff: "x180513", what: "到了兩千四百家為何停止" },
  { setup: "x180516", payoff: "x180517", what: "合作占麥當勞早餐業務的比例" },
  { setup: "x180520", payoff: "x180603", what: "六月季末仍如何計入合作店" },
  { setup: "x180616", payoff: "x180619", what: "終止後相關成本何時移除" },
];
const order = new Map(allRows.map((row, i) => [row.id, i]));
for (const loop of loops) if (!(order.has(loop.setup) && order.has(loop.payoff) && order.get(loop.setup) < order.get(loop.payoff))) throw new Error(`Unpaid loop: ${JSON.stringify(loop)}`);
if (shotCount < 75 || shotCount > 125) throw new Error(`Illustration count outside budget: ${shotCount}`);
const description = [
  "Krispy Kreme 與麥當勞的肯塔基試點，被兩家公司形容為需求超出預期。2024 年公布的全國計畫隨後走到逾 2,400 家麥當勞，卻在 2025 年提前終止。這支品牌故事追著一盤每天配送的甜甜圈，從試點、分區鋪貨、暫緩部署到兩家公司各自的經濟考量，問需求好為何仍無法支撐合作。",
  "",
  "2026 年底全國供應是原計畫，不是已完成；2025 Q2 全球銷售點截至 6/29，仍含 7/2 才退出的約 2,400 門市。Q2 營收跌幅和淨損另有 Insomnia Cookies 股權處分及非現金減損等因素，不能全算在這項合作。Q3 調整後 EBITDA 利潤率改善有多項因素，當季 GAAP 及 FY2025 全年 GAAP 仍為公司整體淨損。插畫為匿名概念場景，開場店員是明示的示意動作，精確數字由後製字卡顯示。資料查核：2026-10-20。",
  "",
  "SEC 原始資料：",
  ...sources.flatMap(source => [source.title, source.url]),
  "",
  "主片、兩支 Shorts、播放清單與濃縮內容的真實網址待實際上傳後回填。",
].join("\n");
const video = {
  schema_version: 1, slug, format: "drama", category: "explainer", narration_locale: "zh-TW", target_minutes: [8, 12],
  voice: { provider: "gemini", name: "Sulafat", style: "標準國語、台灣自然口音，具體平穩說書；目標每分鐘約二百八十到三百字，自然停頓。", performance: "計畫、已達、暫停與終止要聽得出時間差；TTS 後量實質正文至少八分鐘，不足只能增補有來源的新進展。" },
  subtitles: { burn_in: false }, look: { preset: "cute-mystery" }, characters: [],
  series: { slug: "brand-stories-everyday-reversals-extra", episode: 18, chapter: 1 },
  music: { prompt: "light, curious, gently mysterious, no vocals", gain_db: -20, duck_db: -10 }, loops,
  youtube: { category_id: 27, made_for_kids: false, default_language: "zh-TW", title: "Krispy Kreme：試點說賣得好，為何撤出麥當勞？｜品牌故事", description, tags: ["Krispy Kreme", "麥當勞", "品牌故事", "甜甜圈", "商業故事", "配送成本"], video_id: null },
  thumbnail: { template: "thumb", data: { headline: "好賣為何\n喊停？", tag: "品牌故事", brand: "Krispy Kreme", shot: "x18-b01-s01" } },
  sources: sources.map(({ code, ...source }) => source), assets: [], scenes,
};
const bytes = JSON.stringify(video, null, 2) + "\n";
writeFileSync(path.join(dir, "video.json"), bytes);
const videoSha = createHash("sha256").update(bytes).digest("hex");
writeFileSync(path.join(dir, "series.json"), JSON.stringify({ kind: "story", slug: "brand-stories-everyday-reversals-extra", episode: 18, chapter: 1, planned_episodes: 20, title: "Krispy Kreme：試點說賣得好，為何撤出麥當勞？", logline: "一盤每天配送的甜甜圈，從肯塔基試點走到逾 2,400 家合作店後共同終止；追問好需求與單店成本為何分岔。", names: ["Krispy Kreme", "McDonald’s", "Insomnia Cookies"], characters: [], target_minutes: 10, image_model: "image-01", style_preset: "custom", look: { preset: "cute-mystery" }, visual_tier: "stills", compilation: false }, null, 2) + "\n");
writeFileSync(path.join(dir, "script.md"), ["# X18 Krispy Kreme × McDonald’s｜台灣繁中逐句稿", "", `離線前製；\`video.json\` SHA-256：\`${videoSha}\`。本版開場 ${openingChars} 字、正文 ${bodyChars} 字（紙面 @300 字／分約 ${(bodyChars / 300).toFixed(1)} 分），未經真實 TTS、獨立來源審核或盲評。第一章後接官方 5 秒片頭；最後三句後接官方 21 秒 v4 片尾。`, "", ...chapters.flatMap((chapter, ci) => [`## 第 ${ci + 1} 章｜${titles[ci]}${ci === 0 ? "（濃縮開場）" : ""}`, "", ...chapter.map(row => `- \`${row.id}\` ${row.narration}`), ""]), "## 最後三句", "", ...outro.map(row => `- \`${row.id}\` ${row.narration}`), ""].join("\n"));
writeFileSync(path.join(dir, "line-source-matrix.md"), ["# X18 Krispy Kreme × McDonald’s｜逐句作者來源矩陣", "", `\`video.json\` SHA-256：\`${videoSha}\`。作者標記，**不是獨立查核 PASS**；原件、位元組、SHA 和禁區見 [source-matrix.md](source-matrix.md)。`, "", "| 句 ID | 旁白 | 作者來源 |", "| --- | --- | --- |", ...allRows.map(row => `| \`${row.id}\` | ${row.narration.replaceAll("|", "\\|")} | ${row.refs.length ? row.refs.join("、") : "敘事提問／依相鄰來源推理／CTA"} |`), ""].join("\n"));
console.log(JSON.stringify({ video_sha256: videoSha, scenes: scenes.length, shots: shotCount, cards: cardRules.size, lines: allRows.length, opening_chars: openingChars, substantive_body_chars: bodyChars, loops: loops.length }, null, 2));
