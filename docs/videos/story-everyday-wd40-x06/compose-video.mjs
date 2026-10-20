// Compose source-bound X06 preproduction drafts. Re-run after every story edit;
// reviews are valid only for the exact resulting video.json SHA-256.
import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { textHash } from "../../../tools/video/core/schema.mjs";
import { spokenUnits } from "../../../tools/video/core/timeline.mjs";
import { chapters } from "./drafts/story.mjs";

const dir = path.dirname(fileURLToPath(import.meta.url));
const slug = "story-everyday-wd40-x06";
const checkedOn = "2026-10-20";
const sources = [
  { title: "WD-40 FY1995 Form 10-K", url: "https://www.sec.gov/Archives/edgar/data/105132/000089843095002264/0000898430-95-002264.txt", checked_on: checkedOn },
  { title: "WD-40 FY1997 Form 10-K", url: "https://www.sec.gov/Archives/edgar/data/105132/000101706297002143/0001017062-97-002143.txt", checked_on: checkedOn },
  { title: "WD-40 FY2002 Form 10-K", url: "https://www.sec.gov/Archives/edgar/data/105132/000091205702041599/a2092843z10-k.htm", checked_on: checkedOn },
  { title: "WD-40 FY2005 Form 10-K", url: "https://www.sec.gov/Archives/edgar/data/105132/000119312505218608/d10k.htm", checked_on: checkedOn },
  { title: "WD-40 FY2008 Form 10-K", url: "https://www.sec.gov/Archives/edgar/data/105132/000119312508214535/d10k.htm", checked_on: checkedOn },
  { title: "WD-40 FY2025 Form 10-K", url: "https://www.sec.gov/Archives/edgar/data/105132/000010513225000067/wdfc-20250831.htm", checked_on: checkedOn },
  { title: "WD-40 2026 Q3 Form 10-Q", url: "https://www.sec.gov/Archives/edgar/data/105132/000010513226000061/wdfc-20260531.htm", checked_on: checkedOn },
];
const cameras = ["push in", "pan left", "static", "pan right", "tilt up", "pull back"];
const framings = ["Medium shot", "Wide shot", "Close shot", "Overhead shot"];
const pronunciations = [
  ["WD-40", "ＷＤ四十"], ["3-IN-ONE", "三合一"],
  ["Solvol", "索沃"], ["Lava", "拉瓦"],
  ["2000 Flushes", "兩千弗拉許"], ["Carpet Fresh", "卡佩特弗瑞許"],
  ["Spot Shot", "斯波特夏特"],
];
const makeLine = (id, text) => {
  const line = { id, text, emotion: text.endsWith("？") ? "問句上揚，停半拍" : "說書語氣，自然有起伏" };
  const say = pronunciations.reduce((value, [brand, spoken]) => value.replaceAll(brand, spoken), text);
  if (say !== text) Object.assign(line, { say, say_for: textHash(text) });
  return line;
};
const base = chapters.flatMap((chapter, ci) => chapter.rows.map(([text, claim_refs, visual], ri) => {
  const number = String(ri + 1).padStart(2, "0");
  const id = `x06-b${String(ci + 1).padStart(2, "0")}-s${number}`;
  const line = makeLine(`x06${String(ci + 1).padStart(2, "0")}${number}`, text);
  const scene = {
    id,
    template: typeof visual === "string" ? "shot" : "stats",
    data: typeof visual === "string"
      ? { prompt: `${framings[(ci + ri) % framings.length]} ${visual}`, camera: cameras[(ci * 2 + ri) % cameras.length], visual: "still" }
      : visual,
    lines: [line],
    claim_refs,
  };
  if (ri === 0) scene.chapter = chapter.title;
  return scene;
}));
// Every pre-TTS visual state stays under eight estimated seconds. A split preserves
// the source row's claims while cutting the narration at a real punctuation beat.
// The extra image is a different, specifically planned view, not a duplicate frame.
const cutaways = new Map(Object.entries({
  "x06-b02-s03": "Close shot at a 1995 accounts desk, one anonymous clerk studies a plain UK subsidiary ledger beside a small stack of overseas invoices, soft daylight",
  "x06-b02-s07": "Wide shot at a small Pacific port, one anonymous exporter oversees plain cartons beside a departing cargo vessel, hazy morning light",
  "x06-b03-s01": "Close shot at a company product-planning desk, one anonymous clerk sets a plain small oil-bottle mockup beside two unmarked product folders, overhead light",
  "x06-b03-s05": "Overhead shot at a purchase desk, one anonymous accountant separates an intangible-asset folder from an unused plant blueprint, muted lamp light",
  "x06-b03-s15": "Wide shot in a maintenance store, one anonymous buyer studies separate shelves for acquired oil and a newly designed spray, clear afternoon light",
  "x06-b04-s02": "Medium shot in an automotive shop, one anonymous clerk places plain heavy-duty soap beside repair supplies, soft ceiling light",
  "x06-b04-s05": "Close shot at a repair-shop sink, one anonymous worker uses an unmarked liquid hand-cleaner bottle after setting down a tool, daylight",
  "x06-b04-s07": "Overhead shot at a planning table, one anonymous manager moves a plain grocery-basket token toward blank household-brand folders, soft daylight",
  "x06-b04-s08": "Medium shot at a 2001 asset desk, one anonymous buyer places three plain household-cleaner folders beside a hand-soap package, warm desk light",
  "x06-b04-s11": "Wide shot in a hardware warehouse, one anonymous route planner compares grocery broker folders with existing DIY delivery crates, neutral light",
  "x06-b04-s14": "Close shot in a British carpet shop, one anonymous stock clerk positions two plain cleaner bottles under a familiar unmarked shelf section, overcast daylight",
  "x06-b04-s15": "Overhead shot at an accounts desk, one anonymous analyst separates a small British cleaner product-line ledger from a much larger company ledger, desk light",
  "x06-b05-s02": "Wide shot at a year-end accounting desk, one anonymous analyst sets a thick maintenance-products ledger beside a thin homecare ledger, morning light",
  "x06-b05-s04": "Close shot at a maintenance shelf, one anonymous clerk sorts a specialist can apart from the original plain spray can, soft shop light",
  "x06-b05-s05": "Medium shot at a hardware shelf, one anonymous inventory worker keeps a specialist line apart from a plain multi-use spray, even light",
  "x06-b05-s07": "Close shot at a marketing desk, one anonymous planner reduces coins near plain cleaning cartons while leaving maintenance folders open, grey daylight",
  "x06-b06-s03": "Close shot at an accounting desk, one anonymous bookkeeper resumes a stopped row in an unmarked ledger, cool office light",
  "x06-b06-s04": "Wide shot at a small cleaning-products shelf, one anonymous stock clerk checks plain carpet-cleaner bottles beside an active inventory sheet, soft daylight",
  "x06-b06-s07": "Medium shot at a regional accounts table, one anonymous analyst gathers two small homecare ledgers beside a large maintenance ledger, afternoon light",
  "x06-b06-s08": "Wide shot of a mixed maintenance and cleaning shelf, one anonymous store worker leaves the original plain spray can at the center, soft ceiling light",
}));
const statsFirst = new Set(["x06-b04-s15", "x06-b05-s05"]);
const splitScene = scene => {
  const line = scene.lines[0];
  const units = spokenUnits(line.say ?? line.text);
  if (units * 60 / 250 + 1 <= 8) return [scene];
  const cutaway = cutaways.get(scene.id);
  if (!cutaway) throw new Error(`Missing distinct visual for long scene ${scene.id}`);
  const choices = [...line.text].flatMap((char, index) => {
    if (!"；。，：".includes(char)) return [];
    const first = line.text.slice(0, index + 1).trim();
    const second = line.text.slice(index + 1).trim();
    if (!second) return [];
    const firstUnits = spokenUnits(makeLine("tmp-a", first).say ?? first);
    const secondUnits = spokenUnits(makeLine("tmp-b", second).say ?? second);
    if (Math.max(firstUnits, secondUnits) * 60 / 250 + 1 > 8) return [];
    return [{ first, second, balance: Math.abs(firstUnits - secondUnits) }];
  }).sort((a, b) => a.balance - b.balance);
  if (!choices.length) throw new Error(`No under-eight-second split for ${scene.id}`);
  const { first, second } = choices[0];
  const after = { ...scene, id: `${scene.id}b`, lines: [makeLine(`${line.id}b`, second)] };
  delete after.chapter;
  const before = { ...scene, lines: [makeLine(line.id, first)] };
  const alternateCamera = cameras[(cameras.indexOf(scene.data.camera) + 3) % cameras.length] ?? "pan left";
  const extra = { prompt: cutaway, camera: alternateCamera, visual: "still" };
  if (scene.template === "stats" && !statsFirst.has(scene.id)) {
    before.template = "shot";
    before.data = extra;
  } else {
    after.template = "shot";
    after.data = extra;
  }
  return [before, after];
};
const original = base.flatMap(splitScene);
const actualSplits = new Set(original.filter(scene => scene.id.endsWith("b")).map(scene => scene.id.slice(0, -1)));
for (const id of cutaways.keys()) if (!actualSplits.has(id)) throw new Error(`Obsolete split cutaway: ${id}`);
const scenes = original.map(({ claim_refs: _refs, ...scene }) => scene);
const closing = scenes.splice(-3, 3);
scenes.push({
  id: "x06-outro",
  template: "outro",
  data: { title: "品牌與通路", cta: "訂閱品牌故事" },
  lines: closing.flatMap(scene => scene.lines),
});
const ids = new Map(scenes.flatMap((scene, index) => scene.lines.map(line => [line.id, index])));
const loop = (setup, payoff, what) => {
  if (ids.get(setup) === undefined || ids.get(payoff) === undefined || ids.get(setup) >= ids.get(payoff)) throw new Error(`Invalid loop ${setup} → ${payoff}`);
  return { setup, payoff, what };
};
const idFor = prefix => {
  const matches = original.filter(scene => scene.lines[0].text.startsWith(prefix));
  if (matches.length !== 1) throw new Error(`Expected one line beginning ${prefix}, got ${matches.length}`);
  return matches[0].lines[0].id;
};
const loopText = (setup, payoff, what) => loop(idFor(setup), idFor(payoff), what);
const loops = [
  loopText("收購文件除了油", "多年後的年報才回頭確認", "十七國通路如何影響原本的噴劑"),
  loopText("後來貨架多了地毯", "公司想讓這張網", "清潔品牌與原有通路的關係"),
  loopText("二〇二五年，一批清潔品牌", "會計分類也由", "2025 待售到 2026 供使用"),
  loopText("只賣一種產品的公司", "那格空位：十七國通路", "擴張的產品與通路主線"),
  loopText("英國之外，加拿大", "還記得開頭那個十七國數字", "已有海外銷售仍缺哪種入口"),
  loopText("第二瓶油擺在眼前", "還記得開頭那個十七國數字", "第二瓶油之外買到什麼"),
  loopText("原本那罐是噴罐", "還記得開頭那個十七國數字", "第二瓶油更大的價值"),
  loopText("其中幾個市場還沒賣", "多年後的年報才回頭確認", "十七國通路是否真正被用上"),
  loopText("但路線不是單向的", "公司計畫在新興市場", "第二瓶油的目標顧客"),
  loopText("一九九六財年，公司開發", "原有噴劑守廣泛用途", "新產品要補的市場"),
  loopText("可這三樣仍在修理工具", "成了再買家清品牌", "為何收購走到家清貨架"),
  loopText("五金店已能放洗手用品", "公司想讓這張網", "公司打算如何使用超市路線"),
  loopText("這不是噴劑換配方", "收購還帶來雜貨通路", "新品牌如何進店"),
  loopText("公司還想共用銷售", "把 Spot Shot", "家清是否走出美國市場"),
  loopText("英國有新貨架", "公司說，是大客戶不再鋪貨", "美國 Carpet Fresh 失去貨架的原因"),
  loopText("貨架塞滿新品牌", "維護用品約五億", "家清占營收多少"),
  loopText("待售名單裡有廁所清潔", "公司當時說，若售出美洲資產", "曾買進的家清為何待售"),
  loopText("到了隔年四月", "二〇二六年四月，公司不再主動出售", "2026 的出售預期是否成真"),
  loopText("也在重新攤銷的資產裡", "兩地家清合計", "保留後的家清收入份量"),
];
const description = [
  "WD-40 公司四十多年只賣一種主產品，1995 年卻買進另一個潤滑油品牌，往後又買進洗手、廁所和地毯清潔品牌。本集沿 1995–2026 年 SEC 申報，追品牌收購如何帶來新通路、2025 年不同產品組的營收差距，以及 2026 年美洲清潔業務出售計畫的改決定。",
  "",
  "2025 年報曾預期出售美洲家清資產，但 2026 年第三季申報明載公司於 4 月決定不再主動出售、改為保留營運。1995 年以前公司已有海外銷售；2025 年的 176 國與地區及約 66% 海外淨銷售是公司層級，不是單一 WD-40 產品的獨立數字。插畫只作無標誌示意，並非真實員工、店面或產品包裝。資料查核日期：2026-10-20。",
  "",
  "資料來源（SEC 原始申報）",
  ...sources.flatMap(source => [source.title, source.url]),
].join("\n");
const doc = {
  schema_version: 1,
  slug,
  format: "drama",
  category: "explainer",
  narration_locale: "zh-TW",
  target_minutes: [8, 10],
  voice: {
    provider: "gemini", name: "Sulafat",
    style: "標準國語，咬字清楚，台北人平常說話的語調。像對朋友講有申報支持的品牌轉折；數字放慢，問句上揚，揭曉前停半拍。",
    performance: "一九九五年的通路、一九〇〇年代的清潔品牌、二〇二五年的待售與二〇二六年的保留依時間分開；銷售額與利潤不要混念。",
  },
  subtitles: { burn_in: false },
  look: { preset: "cute-mystery" },
  characters: [],
  series: { slug: "brand-stories-everyday-reversals-extra", episode: 6, chapter: 1 },
  music: { prompt: "light, curious, a little mysterious, no vocals", gain_db: -20, duck_db: -10 },
  loops,
  youtube: {
    category_id: 27,
    made_for_kids: false,
    default_language: "zh-TW",
    title: "WD-40 賣一種產品四十多年，為何又買清潔品牌？｜品牌故事",
    description,
    tags: ["WD-40", "品牌故事", "3-IN-ONE", "企業故事", "商業史", "通路", "維護用品", "居家清潔"],
    video_id: null,
  },
  thumbnail: { template: "thumb", data: { headline: "**買通路？**", tag: "品牌故事", brand: "WD-40", shot: "x06-b03-s05" } },
  sources,
  assets: [],
  scenes,
};
const videoBytes = JSON.stringify(doc, null, 2) + "\n";
writeFileSync(path.join(dir, "video.json"), videoBytes);
const sha256 = createHash("sha256").update(videoBytes).digest("hex");
const escapeTable = value => String(value).replaceAll("|", "\\|").replaceAll("\n", " ");
const matrix = [
  "# X06 WD-40｜逐句來源矩陣", "",
  "本表由 `drafts/story.mjs` 的 `claim_refs` 生成。主張與使用界限見 [source-notes.md](source-notes.md)。行內時間、收入與策略均須以所列期間讀；純示意場景與留言邀請另標。", "",
  `- \`video.json\` SHA-256：\`${sha256}\``,
  "- `#` 連至 `source-notes.md` 的可用主張；對應 SEC 文件縮寫見該檔。", "",
  "| 句 ID | 旁白 | 主張編號 |", "| --- | --- | --- |",
  ...original.map(scene => `| \`${scene.lines[0].id}\` | ${escapeTable(scene.lines[0].text)} | ${scene.claim_refs.length ? scene.claim_refs.map(n => `#${n}`).join("、") : "示意場景／編輯提問"} |`), "",
].join("\n");
writeFileSync(path.join(dir, "source-matrix.md"), matrix);
const script = ["# X06 WD-40｜繁中逐句稿", "", `來源綁定：\`video.json\` SHA-256 \`${sha256}\`。實際旁白時間須待正式 TTS 量測；片頭片尾不計正文長度。`, "", ...chapters.flatMap((chapter, ci) => [
  `## ${ci === 0 ? "濃縮開場" : `第 ${ci} 章`}｜${chapter.title}`, "",
  ...original.filter(scene => scene.lines[0].id.startsWith(`x06${String(ci + 1).padStart(2, "0")}`))
    .map(scene => `- \`${scene.lines[0].id}\` ${scene.lines[0].text}`), "",
])].join("\n");
writeFileSync(path.join(dir, "script.md"), script);
console.log(JSON.stringify({ scenes: scenes.length, shots: scenes.filter(s => s.template === "shot").length, cards: scenes.filter(s => s.template !== "shot").length, narration_characters: scenes.reduce((sum, s) => sum + s.lines[0].text.length, 0), loops: loops.length, video_sha256: sha256 }, null, 2));
