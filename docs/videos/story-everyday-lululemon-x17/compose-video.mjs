// Offline compilation only: no media provider, paid call, host import, or upload.
import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { textHash } from "../../../tools/video/core/schema.mjs";

const dir = path.dirname(fileURLToPath(import.meta.url));
const slug = "story-everyday-lululemon-x17";
const sources = [
  { code: "S1", title: "Lululemon 2013-03-21 FY2012 results, 8-K exhibit 99.1", url: "https://www.sec.gov/Archives/edgar/data/1397187/000119312513118207/d505115dex991.htm", checked_on: "2026-10-20" },
  { code: "S2", title: "Lululemon FY2012 Form 10-K", url: "https://www.sec.gov/Archives/edgar/data/1397187/000119312513118393/d475380d10k.htm", checked_on: "2026-10-20" },
  { code: "S3", title: "Lululemon 2013-04-03 production update, 8-K exhibit 99.1", url: "https://www.sec.gov/Archives/edgar/data/1397187/000119312513140668/d516336dex991.htm", checked_on: "2026-10-20" },
  { code: "S4", title: "Lululemon FY2013 Q1 Form 10-Q", url: "https://www.sec.gov/Archives/edgar/data/1397187/000119312513253430/d534167d10q.htm", checked_on: "2026-10-20" },
  { code: "S5", title: "Lululemon 2013-06-10 FY2013 Q1 results, 8-K exhibit 99", url: "https://www.sec.gov/Archives/edgar/data/1397187/000119312513253334/d551549dex99.htm", checked_on: "2026-10-20" },
  { code: "S6a", title: "Lululemon FY2013 results, 8-K exhibit 99.1", url: "https://www.sec.gov/Archives/edgar/data/1397187/000139718714000019/lulu-20140202xex991.htm", checked_on: "2026-10-20" },
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
  if (!/^x17\d{4}\s*\|/.test(raw)) continue;
  const parts = raw.split("|").map(part => part.trim());
  if (parts.length !== 4 || current < 0) throw new Error(`Malformed narration row: ${raw}`);
  const [id, refsText, text, cue] = parts;
  const chapterNumber = current === 6 ? 6 : current + 1;
  if (!id.startsWith(`x17${String(chapterNumber).padStart(2, "0")}`)) throw new Error(`Wrong chapter ID: ${id}`);
  if (!text || !cue || text.length > 48) throw new Error(`Missing or overlong narration line: ${id}`);
  if (/Lululemon|Luon|logo|logotype|readable|trademark|brand|text|lettering/iu.test(cue)) throw new Error(`Protected or text-generating visual cue: ${id}`);
  const refs = refsText === "editorial" ? [] : refsText.split(",");
  if (refs.some(ref => !knownSources.has(ref))) throw new Error(`Unknown source: ${id}`);
  (current === 6 ? outro : chapters[current]).push({ id, text, refs, cue });
}
if (chapters.some((chapter, i) => !titles[i] || chapter.length < 8) || outro.length !== 3) throw new Error("Six chapters and three closing lines required");
const allRows = [...chapters.flat(), ...outro];
if (new Set(allRows.map(row => row.id)).size !== allRows.length) throw new Error("Duplicate line ID");
for (const chapter of [...chapters, outro]) for (let i = 1; i < chapter.length; i++) if (chapter[i].id <= chapter[i - 1].id) throw new Error(`Unordered line ID: ${chapter[i].id}`);
const bodyText = chapters.slice(1).flat().map(row => row.text).join("");
const bodyChars = bodyText.length;
const bodyHanDigits = [...bodyText].filter(char => /[\p{Script=Han}〇0-9]/u.test(char)).length;
if (bodyHanDigits < 2450) throw new Error(`Substantive body has fewer than 2450 Han characters and digits: ${bodyHanDigits}`);

const cardRules = new Map([
  ["x170316", { title: "三月當時的預測", stats: [{ value: "US$12–17m", label: "FY2013 Q1 估計少賣；不是實際損失" }], source: "S1｜2013-03-21" }],
  ["x170317", { title: "三月當時的預測", stats: [{ value: "US$57–67m", label: "FY2013 全年估計少賣；非最終結果" }], source: "S1｜2013-03-21" }],
  ["x170501", { title: "缺貨時間", stats: [{ value: "7 週", label: "FY2013 Q1 最後七週；店內與網站" }], source: "S4｜FY2013 Q1" }],
  ["x170505", { title: "已入帳的存貨準備", stats: [{ value: "US$17.5m", label: "FY2013 Q1 成本；非失去營收總額" }], source: "S4/S5｜FY2013 Q1" }],
  ["x170513", { title: "公司整體營收", stats: [{ value: "+21%", label: "FY2013 Q1 對上年同季；US$345.8m" }], source: "S4/S5｜FY2013 Q1" }],
  ["x170520", { title: "公司整體毛利率", stats: [{ value: "55.0% → 49.4%", label: "上年同季 → FY2013 Q1；不能全歸撤貨" }], source: "S5｜FY2013 Q1" }],
  ["x170603", { title: "公司全年營收", stats: [{ value: "US$1.591bn", label: "FY2013；對 FY2012 +16%，兩年週數不同" }], source: "S6a｜FY2013" }],
  ["x170610", { title: "公司全年毛利率", stats: [{ value: "55.7% → 52.8%", label: "FY2012 → FY2013；非全數撤貨" }], source: "S6a｜FY2013" }],
]);
for (const id of cardRules.keys()) if (!allRows.some(row => row.id === id)) throw new Error(`Missing card anchor: ${id}`);
const shortAnchors = new Set([
  "x170101", "x170301", "x170405", "x170408", "x170409", "x170410", "x170416", "x170426",
  "x170305", "x170310", "x170503", "x170504", "x170509", "x170510", "x170512", "x170506",
]);
const single = new Set([...shortAnchors, ...cardRules.keys(), "x170522", ...chapters.map(chapter => chapter[0].id), ...chapters.map(chapter => chapter.at(-1).id)]);
const cameras = ["Medium shot, gentle push in", "Close-up, slow pull out", "Wide shot, pan left", "Overhead shot, pan right", "Medium close-up, still", "Low-angle shot, tilt up"];
const locations = ["an unbranded apparel store", "a plain fabric and sewing workshop", "an anonymous back-room stock area", "a simple quality inspection table", "a simple store office beside a display wall", "a quiet accounting desk next to an unmarked hanger"];
const lights = ["soft window light", "diffuse morning light", "soft overhead light", "muted daylight", "gentle lamp light", "soft evening light"];
const safeguards = [
  "Unlettered surfaces; no corporate insignia or lettering.",
  "Plain material and props; no logos or real-person likeness.",
  "Unmarked apparel; no labels, words, or numbers.",
  "Fictional scene; omit trademarks and recognizable product design.",
  "Anonymous setting; no readable signage or brand colors.",
  "All paperwork without writing; exclude actual faces and marks.",
];
const toLine = row => {
  const line = { id: row.id, text: row.text, pause_after_ms: 0, emotion: row.text.endsWith("？") ? "台灣自然國語說書；問句留半拍" : "台灣自然國語說書；具體、平穩、不要把估計唸成實績" };
  if (/Lululemon|Luon/.test(row.text)) {
    line.say = row.text.replaceAll("Lululemon", "露露檸檬").replaceAll("Luon", "路昂");
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
    const pair = Boolean(next && !single.has(row.id) && !single.has(next.id) && !row.text.endsWith("？") && !next.text.endsWith("？") && row.text.length + next.text.length <= 42);
    const selected = pair ? [row, next] : [row];
    const sceneId = `x17-b${String(ci + 1).padStart(2, "0")}-s${String(++si).padStart(2, "0")}`;
    let scene;
    if (cardRules.has(row.id)) {
      scene = { id: sceneId, template: "stats", data: { ...cardRules.get(row.id), visual_note: "Typeset the exact figures in postproduction over a neutral silhouette of generic black athletic pants." }, lines: selected.map(toLine) };
    } else {
      const i = shotCount++;
      const portrait = shortAnchors.has(row.id) ? "Hands and the clothing item stay inside the central 608-pixel corridor of a 1920x1080 frame for 9:16 crop." : "";
      const variedCue = !shortAnchors.has(row.id) && i % 3 === 0 ? row.cue.replace(/\bpants\b/giu, "trousers").replace(/\bpant\b/giu, "trouser") : row.cue;
      const prompt = `${cameras[i % cameras.length]} at ${locations[ci]}; ${variedCue}; ${lights[i % lights.length]}. ${portrait} ${safeguards[i % safeguards.length]}`;
      scene = { id: sceneId, template: "shot", data: { prompt, camera: cameras[i % cameras.length], visual: "still" }, lines: selected.map(toLine) };
    }
    if (si === 1) scene.chapter = titles[ci];
    scenes.push(scene);
    ri += selected.length;
  }
}
scenes.push({ id: "x17-outro", template: "outro", data: { title: "一條褲子，四個關口", cta: "訂閱品牌故事" }, lines: outro.map(toLine) });
const loops = [
  { setup: "x170104", payoff: "x170408", what: "四月的檢驗檢討找到哪個缺口" },
  { setup: "x170105", payoff: "x170510", what: "空衣架何時補回" },
  { setup: "x170106", payoff: "x170506", what: "撤貨存貨寫入第一季哪一欄" },
  { setup: "x170207", payoff: "x170410", what: "布樣與成衣差在哪" },
  { setup: "x170217", payoff: "x170303", what: "沿用多年的規格在店裡遇到什麼意外" },
  { setup: "x170224", payoff: "x170301", what: "涉事批次何時開始販售" },
  { setup: "x170304", payoff: "x170306", what: "店外哪些銷售通路也要撤貨" },
  { setup: "x170308", payoff: "x170314", what: "倉庫及途中的受影響貨是否也在範圍" },
  { setup: "x170321", payoff: "x170401", what: "調查首個反常結論" },
  { setup: "x170404", payoff: "x170408", what: "原檢驗漏掉的布料變數" },
  { setup: "x170429", payoff: "x170510", what: "多久才能重新上架" },
  { setup: "x170504", payoff: "x170505", what: "除了少賣預測還有哪筆帳" },
  { setup: "x170512", payoff: "x170517", what: "總營收成長為何能蓋住單品空缺" },
  { setup: "x170522", payoff: "x170524", what: "毛利率降幅是否全由黑褲造成" },
  { setup: "x170527", payoff: "x170604", what: "全年成績能否算出黑褲收入影響" },
  { setup: "x170602", payoff: "x170604", what: "年度公告是否有黑褲單獨少賣實績" },
  { setup: "x170609", payoff: "x170611", what: "全年毛利是否能拆出黑褲份額" },
];
const order = new Map(allRows.map((row, i) => [row.id, i]));
for (const loop of loops) if (!(order.has(loop.setup) && order.has(loop.payoff) && order.get(loop.setup) < order.get(loop.payoff))) throw new Error(`Unpaid loop: ${JSON.stringify(loop)}`);
if (shotCount < 75 || shotCount > 120) throw new Error(`Illustration count out of 75–120 range: ${shotCount}`);
const description = [
  "2013 年 Lululemon 撤下部分黑色 Luon 褲：布料可能符合當時測試，完成的褲子卻出現無法接受的透度。這支故事跟著一條無標誌的示意黑褲，從布樣、成衣到撤貨箱與成本帳，解開公司當時提出的多因素解釋，以及為何總營收仍成長、毛利卻受影響。",
  "",
  "三月估計的 US$57–67m 是 FY2013 預測少賣，不是最後實際損失；US$17.5m 是已入帳存貨準備，也不是全部危機成本。FY2013 的公司指標不得當作這批褲子的銷量。畫面是匿名概念插畫；精確數字由後製字卡顯示。資料檢查：2026-10-20。",
  "",
  "SEC 原始資料：",
  ...sources.flatMap(source => [source.title, source.url]),
  "",
  "主片、兩支 Shorts 與播放清單的真實網址待實際上傳後回填。",
].join("\n");
const video = {
  schema_version: 1, slug, format: "drama", category: "explainer", narration_locale: "zh-TW", target_minutes: [8, 10],
  voice: { provider: "gemini", name: "Sulafat", style: "標準國語、台灣自然口音，平穩具體說書；目標每分鐘約三百二十到三百三十個口語單位，自然停頓且不硬催速度。", performance: "依序看同一件示意黑褲的布樣、成衣、撤貨箱與成本帳；『可能符合』要保留可能，預估和入帳分開讀。TTS 後量實質正文至少八分鐘，不足須增補有來源的新進展。" },
  subtitles: { burn_in: false }, look: { preset: "cute-mystery" }, characters: [],
  series: { slug: "brand-stories-everyday-reversals-extra", episode: 17, chapter: 1 },
  music: { prompt: "light, curious, gently mysterious, no vocals", gain_db: -20, duck_db: -10 }, loops,
  youtube: { category_id: 27, made_for_kids: false, default_language: "zh-TW", title: "Lululemon：布料可能過測試，黑褲為何還是得下架？｜品牌故事", description, tags: ["Lululemon", "品牌故事", "Luon", "運動褲", "產品品質", "商業故事"], video_id: null },
  thumbnail: { template: "thumb", data: { headline: "布過關\n褲太透？", tag: "品牌故事", brand: "Lululemon", shot: "x17-b01-s01" } },
  sources: sources.map(({ code, ...source }) => source), assets: [], scenes,
};
const bytes = JSON.stringify(video, null, 2) + "\n";
writeFileSync(path.join(dir, "video.json"), bytes);
const videoSha = createHash("sha256").update(bytes).digest("hex");
writeFileSync(path.join(dir, "series.json"), JSON.stringify({ kind: "story", slug: "brand-stories-everyday-reversals-extra", episode: 17, chapter: 1, planned_episodes: 20, title: "Lululemon：布料可能過測試，黑褲為何得下架", logline: "一條黑 Luon 褲從布料檢驗到成衣、撤貨與成本帳，追問公司如何查出透度原因，以及為何營收仍增時毛利受傷。", names: ["Lululemon", "Luon"], characters: [], target_minutes: 10, image_model: "image-01", style_preset: "custom", look: { preset: "cute-mystery" }, visual_tier: "stills", compilation: false }, null, 2) + "\n");
writeFileSync(path.join(dir, "script.md"), ["# X17 Lululemon｜台灣繁中逐句稿", "", `離線前製；\`video.json\` SHA-256：\`${videoSha}\`。本版正文紙面 ${bodyHanDigits} 個漢字／數字（${bodyChars} 可見字元），未經真實 TTS 測長，也未經 v8 獨立逐句或雙盲。第一章濃縮後接官方 5 秒片頭；最後三句後接官方 21 秒片尾。`, "", ...chapters.flatMap((chapter, ci) => [`## 第 ${ci + 1} 章｜${titles[ci]}${ci === 0 ? "（濃縮開場）" : ""}`, "", ...chapter.map(row => `- \`${row.id}\` ${row.text}`), ""]), "## 最後三句", "", ...outro.map(row => `- \`${row.id}\` ${row.text}`), ""].join("\n"));
writeFileSync(path.join(dir, "line-source-matrix.md"), ["# X17 Lululemon｜逐句作者來源矩陣", "", `\`video.json\` SHA-256：\`${videoSha}\`。作者標記，**不是獨立來源審核 PASS**；原始網址、位元組、SHA 和口徑見 [source-matrix.md](source-matrix.md)。`, "", "| 句 ID | 旁白 | 作者來源 |", "| --- | --- | --- |", ...allRows.map(row => `| \`${row.id}\` | ${row.text.replaceAll("|", "\\|")} | ${row.refs.length ? row.refs.join("、") : "敘事提問／依原件推理／CTA"} |`), ""].join("\n"));
console.log(JSON.stringify({ video_sha256: videoSha, scenes: scenes.length, shots: shotCount, cards: cardRules.size, lines: allRows.length, opening_chars: chapters[0].map(row => row.text).join("").length, substantive_body_chars: bodyChars, substantive_body_han_digits: bodyHanDigits, loops: loops.length }, null, 2));
