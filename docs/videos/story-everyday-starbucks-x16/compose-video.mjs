// Rebuilds the offline preproduction package. No media provider, import, or upload calls.
import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const dir = path.dirname(fileURLToPath(import.meta.url));
const slug = "story-everyday-starbucks-x16";
const sources = [
  { code: "S1", title: "Starbucks 2008-01-07 8-K exhibit 99.1", url: "https://www.sec.gov/Archives/edgar/data/829224/000089102008000009/v36971exv99w1.htm", checked_on: "2026-10-20" },
  { code: "S2", title: "Starbucks 2008-07-01 8-K exhibit 99.1", url: "https://www.sec.gov/Archives/edgar/data/829224/000095013408012236/v41893exv99w1.htm", checked_on: "2026-10-20" },
  { code: "S3", title: "Starbucks FY2008 Form 10-K", url: "https://www.sec.gov/Archives/edgar/data/829224/000095013408021134/v50316e10vk.htm", checked_on: "2026-10-20" },
  { code: "S4", title: "Starbucks FY2009 Form 10-K", url: "https://www.sec.gov/Archives/edgar/data/829224/000095012309064772/v53316e10vk.htm", checked_on: "2026-10-20" },
  { code: "S5", title: "Starbucks FY2010 Form 10-K", url: "https://www.sec.gov/Archives/edgar/data/829224/000119312510266333/d10k.htm", checked_on: "2026-10-20" },
];
const codes = new Set(sources.map(source => source.code));
const lines = [[], [], [], [], [], []];
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
  if (!/^x16\d{4}\s*\|/.test(raw)) continue;
  const parts = raw.split("|").map(part => part.trim());
  if (parts.length !== 4 || current < 0) throw new Error(`Malformed narration row: ${raw}`);
  const [id, refsText, text, cue] = parts;
  const expectedChapter = current === 6 ? 6 : current + 1;
  if (!id.startsWith(`x16${String(expectedChapter).padStart(2, "0")}`)) throw new Error(`Wrong chapter ID: ${id}`);
  if (!text || !cue || text.length > 24) throw new Error(`Missing/long line: ${id} ${text.length}`);
  if (/Starbucks|星巴克|Schultz|舒茲|logo|logotype|readable|trademark/iu.test(cue)) throw new Error(`Protected or text-generating visual cue: ${id}`);
  const refs = refsText === "editorial" ? [] : refsText.split(",");
  if (refs.some(ref => !codes.has(ref))) throw new Error(`Unknown source: ${id}`);
  (current === 6 ? outro : lines[current]).push({ id, text, refs, cue });
}
if (lines.some((chapter, i) => !titles[i] || chapter.length < 9) || outro.length !== 3) throw new Error("Six chapters and three ending lines required");
const allRows = [...lines.flat(), ...outro];
if (new Set(allRows.map(row => row.id)).size !== allRows.length) throw new Error("Duplicate line ID");
for (const chapter of [...lines, outro]) for (let i = 1; i < chapter.length; i++) if (chapter[i].id <= chapter[i - 1].id) throw new Error(`Line IDs out of order: ${chapter[i].id}`);

const cardRules = [
  [/約六百家美國直營店/, { title: "2008-07-01 宣布", stats: [{ value: "約 600 家", label: "美國直營店關閉計畫；含先前 100 家" }], source: "S2｜Starbucks 8-K exhibit" }],
  [/百分之四。/, { title: "美國同店銷售", stats: [{ value: "+4%", label: "FY2007；開滿 13 個月的直營店" }], source: "S3｜FY2008 10-K" }],
  [/已轉成下滑百分之五。/, { title: "美國同店銷售", stats: [{ value: "−5%", label: "FY2008；不是所有新店的成績" }], source: "S3｜FY2008 10-K" }],
  [/三點四八億美元/, { title: "關店預計稅前費用", stats: [{ value: "US$328m–348m", label: "2008-07 當時估計；非實支結果" }], source: "S2｜Starbucks 8-K exhibit" }],
  [/實際關掉二百零五家/, { title: "七月 600 家計畫的進度", stats: [{ value: "205 家", label: "FY2008 已關；非全年淨減" }], source: "S3｜FY2008 10-K" }],
  [/淨數竟增加四百四十五家/, { title: "美國直營店年度淨變化", stats: [{ value: "+445 家", label: "FY2008；6,793 → 7,238" }], source: "S3｜FY2008 10-K" }],
  [/累積五百八十八家/, { title: "七月 600 家計畫", stats: [{ value: "588 家", label: "205（FY2008）＋383（FY2009）" }], source: "S3/S4｜FY2008/FY2009 10-K" }],
  [/另關一百八十三/, { title: "2009-01 另列約 200 家", stats: [{ value: "183 家", label: "FY2009 已關；與 588 分屬兩批" }], source: "S4｜FY2009 10-K" }],
  [/再跌百分之六/, { title: "美國同店銷售", stats: [{ value: "−6%", label: "FY2009；13 個月以上直營店" }], source: "S4/S5｜FY2009/FY2010 10-K" }],
  [/轉成成長百分之七/, { title: "美國同店銷售", stats: [{ value: "+7%", label: "FY2010；排除第 53 週" }], source: "S5｜FY2010 10-K" }],
  [/十四億一千九百四十萬/, { title: "全公司營業利益", stats: [{ value: "US$562.0m", label: "FY2009" }, { value: "US$1,419.4m", label: "FY2010；含第 53 週" }], source: "S5｜FY2010 10-K" }],
];
const cards = new Map();
for (const [pattern, card] of cardRules) {
  const matches = allRows.filter(row => pattern.test(row.text));
  if (matches.length !== 1) throw new Error(`Card anchor ambiguous: ${pattern} (${matches.length})`);
  cards.set(matches[0].id, card);
}
const camera = ["Medium shot, push in", "Close-up, pull out", "Wide shot, pan left", "Medium close-up, pan right", "Overhead shot, tilt down", "Low-angle shot, tilt up"];
const rooms = ["in a plain small office", "at an anonymous cafe counter", "in a city planning studio", "at a street corner storefront", "in an unbranded archive aisle", "beside a quiet neighborhood sidewalk"];
const light = ["mild window light", "soft grey morning light", "muted afternoon light", "soft lamp light", "overcast daylight", "soft evening light"];
const safeguards = [
  "Paper surfaces stay blank; cups lack emblems; the appearance is invented.",
  "Documents display only colour blocks; no print, trademarks, or recognizable person.",
  "Labels are absent; clothing and containers have no brand marks or real-world likeness.",
  "Pages and façades contain empty areas; exclude lettering, corporate insignia, or celebrity likeness.",
  "Objects bear no inscriptions or pictograms; the character is anonymous and fictional.",
  "Fixtures have no titles, digits, or lettering; no insignia or real person's identity.",
];
const portraitSourceLines = new Set(["x160101", "x160103", "x160316", "x160309", "x160318", "x160312", "x160314", "x160329", "x160517", "x160602", "x160623", "x160604", "x160605", "x160609", "x160618"]);
const portraitInstruction = " Keep the person's face, hands, and focal prop inside the central 608-pixel corridor of a 1920x1080 frame for a later 9:16 crop.";
const lineFor = row => ({ id: row.id, text: row.text, pause_after_ms: 0, emotion: row.text.endsWith("？") ? "台灣國語口語說書，留半拍讓問題落地" : "台灣國語口語說書，數字與年份清楚，正常語速" });
const scenes = [];
let shotCount = 0;
for (const [ci, chapter] of lines.entries()) {
  let si = 0;
  for (let ri = 0; ri < chapter.length;) {
    const row = chapter[ri];
    const next = chapter[ri + 1];
    const pair = Boolean(next && !cards.has(row.id) && !cards.has(next.id) && !portraitSourceLines.has(next.id) && row.text.length + next.text.length <= 35);
    const selected = pair ? [row, next] : [row];
    const id = `x16-b${String(ci + 1).padStart(2, "0")}-s${String(++si).padStart(2, "0")}`;
    const card = cards.get(row.id);
    let scene;
    if (card) scene = { id, template: "stats", data: card, lines: selected.map(lineFor) };
    else {
      const i = shotCount++;
      const cue = selected[0].cue.replace(/^anonymous /, "");
      const portrait = selected.some(item => portraitSourceLines.has(item.id));
      const angle = i % 4 === 0 ? "in front view, eyes toward viewer" : i % 4 === 1 ? "in three-quarter view" : i % 4 === 2 ? "in side-profile view" : "with head turned downward";
      const prompt = `${camera[i % camera.length]} ${rooms[ci]}, one anonymous ${cue}, ${angle}, ${light[i % light.length]}.${portrait ? portraitInstruction : ""} ${safeguards[i % safeguards.length]}`;
      scene = { id, template: "shot", data: { prompt, camera: camera[i % camera.length], visual: "still" }, lines: selected.map(lineFor) };
    }
    if (si === 1) scene.chapter = titles[ci];
    scenes.push(scene);
    ri += selected.length;
  }
}
scenes.push({ id: "x16-outro", template: "outro", data: { title: "每家店都要算自己的帳", cta: "訂閱品牌故事" }, lines: outro.map(lineFor) });
const loops = [
  { setup: "x160103", payoff: "x160309", what: "七成到底是哪個分母" },
  { setup: "x160105", payoff: "x160203", what: "一月董事會如何改變展店速度" },
  { setup: "x160106", payoff: "x160407", what: "九月底直營店淨數為何仍上升" },
  { setup: "x160107", payoff: "x160501", what: "隔年另列多少家美國店" },
  { setup: "x160108", payoff: "x160601", what: "二〇一〇年美國同店怎麼變" },
  { setup: "x160109", payoff: "x160641", what: "新店入選背後的單店回報問題" },
  { setup: "x160227", payoff: "x160301", what: "七月公告是否擴大原先關店計畫" },
  { setup: "x160332", payoff: "x160401", what: "財年截止時實際關掉幾家" },
  { setup: "x160428", payoff: "x160502", what: "隔年新名單是否屬於另一批" },
  { setup: "x160528", payoff: "x160601", what: "留下的成熟店有沒有轉好" },
];
const positions = new Map(allRows.map((row, i) => [row.id, i]));
for (const loop of loops) if (!(positions.has(loop.setup) && positions.has(loop.payoff) && positions.get(loop.setup) < positions.get(loop.payoff))) throw new Error(`Unpaid loop: ${JSON.stringify(loop)}`);
const description = [
  "2008 年 7 月 1 日，星巴克宣布擬關閉約 600 家表現不佳的美國直營店，其中約七成入選店自 2006 財年起才開。為什麼新店也在名單裡？本集沿 SEC 原始公告和 2008–2010 年報，分清計畫、實際關閉、年度淨店數與同店銷售。",
  "",
  "約 600 家含先前的 100 家；七成的分母是入選關閉的店。2009 年另列的約 200 家是另一批。FY2010 同店增幅排除第 53 週，但全公司營業利益未做這項調整。插畫是匿名概念畫面；片中數字與文字卡由後製排版。資料檢查：2026-10-20。",
  "",
  "SEC 原始資料：",
  ...sources.flatMap(source => [source.title, source.url]),
  "",
  "主片、兩支 Shorts、播放清單的真實網址待實際上傳後回填。",
].join("\n");
const video = {
  schema_version: 1, slug, format: "drama", category: "explainer", narration_locale: "zh-TW", target_minutes: [8, 12],
  voice: { provider: "gemini", name: "Sulafat", style: "標準國語，台灣自然口音，像向朋友追一間公司的真實轉折；日期、財年、百分比讀清楚。", performance: "七成是入選關閉店的比例；計畫與實際、關閉數與淨店數分開說，答案不搶先講。" },
  subtitles: { burn_in: false }, look: { preset: "cute-mystery" }, characters: [],
  series: { slug: "brand-stories-everyday-reversals-extra", episode: 16, chapter: 1 },
  music: { prompt: "light, curious, a little mysterious, no vocals", gain_db: -20, duck_db: -10 }, loops,
  youtube: { category_id: 27, made_for_kids: false, default_language: "zh-TW", title: "星巴克剛開的店，怎麼又列進關店名單？｜品牌故事", description, tags: ["星巴克", "Starbucks", "品牌故事", "2008", "關店", "商業故事"], video_id: null },
  thumbnail: { template: "thumb", data: { headline: "新店\n要關？", tag: "品牌故事", brand: "星巴克", shot: "x16-b01-s01" } },
  sources: sources.map(({ code, ...source }) => source), assets: [], scenes,
};
const bytes = JSON.stringify(video, null, 2) + "\n";
writeFileSync(path.join(dir, "video.json"), bytes);
const sha = createHash("sha256").update(bytes).digest("hex");
writeFileSync(path.join(dir, "series.json"), JSON.stringify({ kind: "story", slug: "brand-stories-everyday-reversals-extra", episode: 16, chapter: 1, planned_episodes: 20, title: "星巴克：剛開的店為何進入關店名單", logline: "從 2008 年約 600 家美國直營店關閉公告，到 2009 年實際進度與 2010 年同店轉正，追問快速展店和單店回報的落差。", names: ["星巴克", "Starbucks", "Howard Schultz", "舒茲"], characters: [], target_minutes: 10, image_model: "image-01", style_preset: "custom", look: { preset: "cute-mystery" }, visual_tier: "stills", compilation: false }, null, 2) + "\n");
writeFileSync(path.join(dir, "script.md"), ["# X16 星巴克｜繁中逐句稿", "", `離線前製；\`video.json\` SHA-256：\`${sha}\`。未獨立逐句審核、盲讀、配音或測量實際時長。第一章濃縮後接正式 5 秒片頭；最後三句後接 21 秒 v4 片尾。`, "", ...lines.flatMap((chapter, ci) => [`## 第 ${ci + 1} 章｜${titles[ci]}${ci === 0 ? "（濃縮開場）" : ""}`, "", ...chapter.map(row => `- \`${row.id}\` ${row.text}`), ""]), "## 最後三句", "", ...outro.map(row => `- \`${row.id}\` ${row.text}`), ""].join("\n"));
writeFileSync(path.join(dir, "line-source-matrix.md"), ["# X16 星巴克｜逐句作者來源矩陣", "", `\`video.json\` SHA-256：\`${sha}\`。本表是作者標記，**不是獨立來源審核 PASS**。來源代碼、原文 URL 與口徑見 [source-matrix.md](source-matrix.md)。`, "", "| 句 ID | 旁白 | 作者來源標記 |", "| --- | --- | --- |", ...allRows.map(row => `| \`${row.id}\` | ${row.text.replaceAll("|", "\\|")} | ${row.refs.length ? row.refs.join("、") : "敘事提問／推理／CTA"} |`), ""].join("\n"));
console.log(JSON.stringify({ video_sha256: sha, scenes: scenes.length, shots: scenes.filter(scene => scene.template === "shot").length, cards: scenes.filter(scene => scene.template === "stats").length, lines: allRows.length, hook_chars: lines[0].map(row => row.text).join("").length, substantive_body_chars: lines.slice(1).flat().map(row => row.text).join("").length, loops: loops.length }, null, 2));
