// Offline compilation only: no media provider, paid call, host import, or upload.
import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { textHash } from "../../../tools/video/core/schema.mjs";

const dir = path.dirname(fileURLToPath(import.meta.url));
const slug = "story-everyday-uber-x19";
const sources = [
  { code: "S1", title: "Uber 2020 Q1 results, 8-K exhibit 99.1", url: "https://www.sec.gov/Archives/edgar/data/1543151/000154315120000020/uberq120earningspressr.htm", checked_on: "2026-10-20" },
  { code: "S2", title: "Uber 2020 Q2 results, 8-K exhibit 99.1", url: "https://www.sec.gov/Archives/edgar/data/1543151/000154315120000027/uberq220earningspressr.htm", checked_on: "2026-10-20" },
  { code: "S3", title: "Uber 2020-07-06 Postmates acquisition call, 8-K exhibit 99.1", url: "https://www.sec.gov/Archives/edgar/data/1543151/000155278120000412/e20423_ex99-1.htm", checked_on: "2026-10-20" },
  { code: "S3a", title: "Uber 2020-07-06 Postmates acquisition Form 8-K", url: "https://www.sec.gov/Archives/edgar/data/1543151/000155278120000412/e20423_uber-8k.htm", checked_on: "2026-10-20" },
  { code: "S4", title: "Uber 2020 Q3 results, 8-K exhibit 99.1", url: "https://www.sec.gov/Archives/edgar/data/1543151/000162828020015770/uberq320earningspressr.htm", checked_on: "2026-10-20" },
  { code: "S5", title: "Uber 2020-12-01 Postmates close, 8-K exhibit 99.1", url: "https://www.sec.gov/Archives/edgar/data/1543151/000155278120000580/e20585_ex99-1.htm", checked_on: "2026-10-20" },
  { code: "S5a", title: "Uber 2020-12-01 Postmates completion Form 8-K", url: "https://www.sec.gov/Archives/edgar/data/1543151/000155278120000580/e20585_uber-8k.htm", checked_on: "2026-10-20" },
  { code: "S6", title: "Uber 2021 Q2 results, 8-K exhibit 99.1", url: "https://www.sec.gov/Archives/edgar/data/1543151/000154315121000035/uberq221earningspressrelea.htm", checked_on: "2026-10-20" },
  { code: "S7", title: "Uber 2021 Q4 results, 8-K exhibit 99.1", url: "https://www.sec.gov/Archives/edgar/data/1543151/000154315122000004/uberq421earningspressrelea.htm", checked_on: "2026-10-20" },
  { code: "S8", title: "Uber 2022 Q4 results, 8-K exhibit 99.1", url: "https://www.sec.gov/Archives/edgar/data/1543151/000154315123000004/uberq422earningspressrelea.htm", checked_on: "2026-10-20" },
];
const knownSources = new Set(sources.map(source => source.code));
const chapters = Array.from({ length: 6 }, () => []);
const titles = [];
const outro = [];
let current = -1;
for (const raw of readFileSync(path.join(dir, "drafts/narration.md"), "utf8").split(/\r?\n/)) {
  const header = raw.match(/^## (b0[1-6]|outro):\s*(.*)$/);
  if (header) {
    current = header[1] === "outro" ? 6 : Number(header[1].slice(1)) - 1;
    if (current < 6) titles[current] = header[2].replace("（濃縮開場）", "");
    continue;
  }
  if (!/^x19\d{4}\s*\|/.test(raw)) continue;
  const parts = raw.split("|").map(part => part.trim());
  if (parts.length !== 4 || current < 0) throw new Error(`Malformed narration row: ${raw}`);
  const [id, refsText, text, cue] = parts;
  const chapterNumber = current === 6 ? 6 : current + 1;
  if (!id.startsWith(`x19${String(chapterNumber).padStart(2, "0")}`)) throw new Error(`Wrong chapter ID: ${id}`);
  if (!text || !cue || text.length > 52) throw new Error(`Missing or overlong narration line: ${id}`);
  if (/Uber|Eats|Postmates|logo|logotype|readable|trademark|brand|text|lettering/iu.test(cue)) throw new Error(`Protected or text-generating visual cue: ${id}`);
  const refs = refsText === "editorial" ? [] : refsText.split(",");
  if (refs.some(ref => !knownSources.has(ref))) throw new Error(`Unknown source: ${id}`);
  (current === 6 ? outro : chapters[current]).push({ id, text, refs, cue });
}
if (chapters.some((chapter, i) => !titles[i] || chapter.length < 8) || outro.length !== 3) throw new Error("Six chapters and three closing lines required");
const allRows = [...chapters.flat(), ...outro];
if (new Set(allRows.map(row => row.id)).size !== allRows.length) throw new Error("Duplicate line ID");
for (const chapter of [...chapters, outro]) for (let i = 1; i < chapter.length; i++) if (chapter[i].id <= chapter[i - 1].id) throw new Error(`Unordered line ID: ${chapter[i].id}`);
const bodyChars = chapters.slice(1).flat().map(row => row.text).join("").length;
if (bodyChars < 2450) throw new Error(`Substantive body too short on paper: ${bodyChars}`);

const cardRules = new Map([
  ["x190202", { title: "疫情前的載客訂單額", stats: [{ value: "US$12.188bn", label: "2019 Q2 Mobility，平台訂單額" }], source: "S2｜2019 Q2 對照" }],
  ["x190203", { title: "疫情前的外送訂單額", stats: [{ value: "US$3.386bn", label: "2019 Q2 Delivery，平台訂單額" }], source: "S2｜2019 Q2 對照" }],
  ["x190205", { title: "交叉前一季", stats: [{ value: "US$4.683bn", label: "2020 Q1 Eats 訂單額" }], source: "S1｜2020 Q1" }],
  ["x190302", { title: "載客突然縮小", stats: [{ value: "US$3.046bn", label: "2020 Q2 Mobility 訂單額；同比 −75%" }], source: "S2｜2020 Q2" }],
  ["x190304", { title: "外送跨到前面", stats: [{ value: "US$6.961bn", label: "2020 Q2 Delivery 訂單額；同比 +106%" }], source: "S2｜2020 Q2" }],
  ["x190308", { title: "訂單額不是營收", stats: [{ value: "US$10.224bn", label: "2020 Q2 全平台訂單額" }, { value: "US$2.241bn", label: "同季 Uber 確認營收" }], source: "S2｜2020 Q2" }],
  ["x190317", { title: "外送仍未獲利", stats: [{ value: "−US$232m", label: "2020 Q2 Delivery 調整後 EBITDA" }], source: "S2｜2020 Q2" }],
  ["x190402", { title: "收購在交叉之後", stats: [{ value: "約 US$2.65bn", label: "2020-07 全股票收購約定；非六月成交" }], source: "S3/S3a｜2020-07" }],
  ["x190411", { title: "交割前的第三季", stats: [{ value: "US$8.550bn", label: "2020 Q3 Delivery 訂單額" }, { value: "US$5.905bn", label: "同季 Mobility 訂單額" }], source: "S4｜2020 Q3" }],
  ["x190512", { title: "整合後仍領先", stats: [{ value: "US$12.9bn", label: "2021 Q2 Delivery 訂單額" }, { value: "US$8.6bn", label: "同季 Mobility 訂單額" }], source: "S6｜2021 Q2" }],
  ["x190602", { title: "外送部門轉正", stats: [{ value: "+US$25m", label: "2021 Q4 Delivery 調整後 EBITDA，單季" }], source: "S7｜2021 Q4" }],
  ["x190611", { title: "載客重新較大", stats: [{ value: "US$14.894bn", label: "2022 Q4 Mobility 訂單額" }, { value: "US$14.315bn", label: "同季 Delivery 訂單額" }], source: "S8｜2022 Q4" }],
]);
for (const id of cardRules.keys()) if (!allRows.some(row => row.id === id)) throw new Error(`Missing card anchor: ${id}`);
const shortAnchors = new Set([
  "x190301", "x190305", "x190306", "x190307", "x190309", "x190318", "x190319", "x190322",
  "x190401", "x190403", "x190407", "x190409", "x190421", "x190501", "x190503", "x190504",
]);
const single = new Set([...shortAnchors, ...cardRules.keys(), ...chapters.map(chapter => chapter[0].id), ...chapters.map(chapter => chapter.at(-1).id)]);
const cameras = ["Medium shot, slow push in", "Close-up, pull out", "Wide shot, pan left", "Overhead shot, pan right", "Medium close-up, still", "Low-angle shot, tilt up"];
const locations = [
  ["a plain car waiting at a city curb", "inside a simple passenger car", "outside a small restaurant at pickup time"],
  ["an anonymous driver dispatch station", "a local shop counter", "an apartment delivery doorway"],
  ["a quiet street by a restaurant", "a small restaurant pickup shelf", "a plain accounting desk"],
  ["a planning room with unsigned diagrams", "an unmarked courier vehicle", "a busy city delivery curb"],
  ["a shared sorting hub without signage", "a merchant handoff table", "a pair of ordinary handsets"],
  ["a city curb returning to ordinary traffic", "a restaurant counter after reopening", "an accounting desk beside the street"],
];
const lights = ["soft window light", "diffuse morning light", "muted daylight", "warm overhead light", "gentle lamp light", "soft evening light"];
const safeguards = [
  "Featureless mobile screens; no corporate marks or lettering.",
  "Plain vehicles and bags; no logos or real-person likeness.",
  "Ordinary props; no labels, words, or numbers.",
  "Fictional illustration; omit trademarks and recognizable interface designs.",
  "Anonymous setting; no readable signs or distinctive brand colors.",
  "Paperwork without legible marks; exclude actual faces and emblems.",
];
const toLine = row => {
  const line = { id: row.id, text: row.text, pause_after_ms: 0, emotion: row.text.endsWith("？") ? "台灣自然國語說書；問句留半拍" : "台灣自然國語說書；分清訂單額、營收與不同獲利尺度" };
  if (/Postmates|Uber Eats|EBITDA|App/.test(row.text)) {
    line.say = row.text.replaceAll("Postmates", "波斯特梅茲").replaceAll("Uber Eats", "優步外送").replaceAll("EBITDA", "E B I T D A").replaceAll("App", "應用程式");
    line.say_for = textHash(row.text);
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
    const pair = Boolean(next && !single.has(row.id) && !single.has(next.id) && !row.text.endsWith("？") && !next.text.endsWith("？") && row.text.length + next.text.length <= 36);
    const selected = pair ? [row, next] : [row];
    const sceneId = `x19-b${String(ci + 1).padStart(2, "0")}-s${String(++si).padStart(2, "0")}`;
    let scene;
    if (cardRules.has(row.id)) {
      scene = { id: sceneId, template: "stats", data: { ...cardRules.get(row.id), visual_note: "Precise figures are typeset in postproduction over generic car and food-bag silhouettes." }, lines: selected.map(toLine) };
    } else {
      const i = shotCount++;
      const portrait = shortAnchors.has(row.id) ? "Keep the handset, vehicle or bag inside the central 608-pixel corridor of a 1920x1080 frame for 9:16 crop." : "";
      const cue = shortAnchors.has(row.id) ? row.cue : row.cue.replaceAll("blank", ["empty", "unmarked", "plain"][i % 3]).replaceAll("phone", i % 2 ? "handset" : "mobile device");
      const prompt = `${cameras[i % cameras.length]} at ${locations[ci][i % locations[ci].length]}; ${cue}; ${lights[i % lights.length]}. ${portrait} ${safeguards[i % safeguards.length]}`;
      scene = { id: sceneId, template: "shot", data: { prompt, camera: cameras[i % cameras.length], visual: "still" }, lines: selected.map(toLine) };
    }
    if (si === 1) scene.chapter = titles[ci];
    scenes.push(scene);
    ri += selected.length;
  }
}
scenes.push({ id: "x19-outro", template: "outro", data: { title: "同一支手機，兩種需求", cta: "訂閱品牌故事" }, lines: outro.map(toLine) });
const loops = [
  { setup: "x190105", payoff: "x190301", what: "六月究竟是哪條線領先" },
  { setup: "x190106", payoff: "x190401", what: "七月收購發生在交叉前後" },
  { setup: "x190107", payoff: "x190501", what: "兩張外送網何時開始整合" },
  { setup: "x190108", payoff: "x190611", what: "載客訂單何時重新較大" },
  { setup: "x190109", payoff: "x190625", what: "外送為何先超過載客" },
  { setup: "x190204", payoff: "x190301", what: "既有外送網遇危機能否反超" },
  { setup: "x190209", payoff: "x190210", what: "乘客減少後司機接什麼" },
  { setup: "x190214", payoff: "x190217", what: "公司擴大派單同時如何收縮" },
  { setup: "x190222", payoff: "x190301", what: "轉派能否讓交易額換位" },
  { setup: "x190306", payoff: "x190307", what: "交叉比的是哪一種錢" },
  { setup: "x190311", payoff: "x190313", what: "外送反超是否令平台活動增加" },
  { setup: "x190314", payoff: "x190317", what: "較忙的外送是否賺錢" },
  { setup: "x190319", payoff: "x190320", what: "部門走勢相反時公司正式盈虧" },
  { setup: "x190323", payoff: "x190401", what: "收購是否造成六月交叉" },
  { setup: "x190408", payoff: "x190411", what: "交割前第三季誰領先" },
  { setup: "x190413", payoff: "x190415", what: "載客或外送哪邊先留下部門利潤" },
  { setup: "x190420", payoff: "x190601", what: "外送何時讓部門調整後指標轉正" },
  { setup: "x190422", payoff: "x190501", what: "年底收購是否交割" },
  { setup: "x190506", payoff: "x190507", what: "交割後用戶遷移" },
  { setup: "x190513", payoff: "x190514", what: "整合後外送是否賺錢" },
  { setup: "x190517", payoff: "x190519", what: "正式淨利能否歸給外送" },
  { setup: "x190522", payoff: "x190601", what: "外送年底是否轉正" },
  { setup: "x190604", payoff: "x190608", what: "部門轉正能否解釋集團淨利" },
  { setup: "x190609", payoff: "x190611", what: "載客能否重新領先" },
  { setup: "x190617", payoff: "x190623", what: "哪種帳目回答主問題" },
  { setup: "x190620", payoff: "x190621", what: "能否拆出每個轉向動作的貢獻" },
];
const order = new Map(allRows.map((row, i) => [row.id, i]));
for (const loop of loops) if (!(order.has(loop.setup) && order.has(loop.payoff) && order.get(loop.setup) < order.get(loop.payoff))) throw new Error(`Unpaid loop: ${JSON.stringify(loop)}`);
if (shotCount < 75 || shotCount > 120) throw new Error(`Illustration count out of 75–120 range: ${shotCount}`);
const description = [
  "2020 年春天，Uber 讓載客司機更容易接外送。第二季外送 Gross Bookings 高過載客，為什麼訂單額較大的那條路仍虧錢？這支故事跟著同一支匿名派單手機，從司機改接餐袋、七月簽約收購 Postmates、十二月整合，到 2022 年載客金額重新較大。",
  "",
  "所有比較都是平台訂單額，不是 Uber 確認營收或獲利。Postmates 收購在六月季度之後才簽約、十二月才完成；公司淨利也包括股權投資重估，不能全算成外送賺的。情境畫面是無品牌概念插畫，數字由後製字卡呈現。資料檢查：2026-10-20。",
  "",
  "SEC 原始資料：",
  ...sources.flatMap(source => [source.title, source.url]),
  "",
  "主片、兩支 Shorts 與播放清單的真實網址待實際上傳後回填。",
].join("\n");
const video = {
  schema_version: 1, slug, format: "drama", category: "explainer", narration_locale: "zh-TW", target_minutes: [8, 12],
  voice: { provider: "gemini", name: "Sulafat", style: "標準國語、台灣自然口音，平穩具體說書；目標每分鐘約二百八十到三百字，自然停頓。", performance: "一路看同一支派單手機的載客與外送兩條路；所有金額保留季度和尺度。TTS 後量實質正文至少八分鐘，不足須補有來源的新進展。" },
  subtitles: { burn_in: false }, look: { preset: "cute-mystery" }, characters: [],
  series: { slug: "brand-stories-everyday-reversals-extra", episode: 19, chapter: 1 },
  music: { prompt: "light, curious, a little mysterious, no vocals", gain_db: -20, duck_db: -10 }, loops,
  youtube: { category_id: 27, made_for_kids: false, default_language: "zh-TW", title: "Uber：載客驟減，外送交易額為何反超？｜品牌故事", description, tags: ["Uber", "品牌故事", "外送", "載客", "Postmates", "商業故事"], video_id: null },
  thumbnail: { template: "thumb", data: { headline: "外送反超？", tag: "品牌故事", brand: "UBER", shot: "x19-b01-s01" } },
  sources: sources.map(({ code, ...source }) => source), assets: [], scenes,
};
const bytes = JSON.stringify(video, null, 2) + "\n";
writeFileSync(path.join(dir, "video.json"), bytes);
const videoSha = createHash("sha256").update(bytes).digest("hex");
writeFileSync(path.join(dir, "series.json"), JSON.stringify({ kind: "story", slug: "brand-stories-everyday-reversals-extra", episode: 19, chapter: 1, planned_episodes: 20, title: "Uber：載客驟減，外送交易額為何反超", logline: "一支派單手機的載客與外送路線，在 2020 年跨過、又於恢復後換位；平台訂單額與營收、獲利分開看。", names: ["Uber", "Uber Eats", "Postmates"], characters: [], target_minutes: 10, image_model: "image-01", style_preset: "custom", look: { preset: "cute-mystery" }, visual_tier: "stills", compilation: false }, null, 2) + "\n");
writeFileSync(path.join(dir, "script.md"), ["# X19 Uber｜台灣繁中逐句稿", "", `離線前製；video.json SHA-256：${videoSha}。本版正文紙面 ${bodyChars} 字，未經真實 TTS 測長，也未經獨立逐句或盲評。第一章濃縮後接官方 5 秒片頭；最後三句後接官方 21 秒片尾。`, "", ...chapters.flatMap((chapter, ci) => [`## 第 ${ci + 1} 章｜${titles[ci]}${ci === 0 ? "（濃縮開場）" : ""}`, "", ...chapter.map(row => `- ${row.id} ${row.text}`), ""]), "## 最後三句", "", ...outro.map(row => `- ${row.id} ${row.text}`), ""].join("\n"));
writeFileSync(path.join(dir, "line-source-matrix.md"), ["# X19 Uber｜逐句作者來源矩陣", "", `video.json SHA-256：${videoSha}。作者標記，並非獨立來源審核 PASS；原始網址、位元組、SHA 和口徑見 source-matrix.md。`, "", "| 句 ID | 旁白 | 作者來源 |", "| --- | --- | --- |", ...allRows.map(row => `| ${row.id} | ${row.text.replaceAll("|", "\\|")} | ${row.refs.length ? row.refs.join("、") : "敘事提問／依原件推理／CTA"} |`), ""].join("\n"));
console.log(JSON.stringify({ video_sha256: videoSha, scenes: scenes.length, shots: shotCount, cards: cardRules.size, lines: allRows.length, opening_chars: chapters[0].map(row => row.text).join("").length, substantive_body_chars: bodyChars, loops: loops.length }, null, 2));
