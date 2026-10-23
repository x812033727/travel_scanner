// Rebuild the non-paid C06 manuscript and scene plan. No media or network calls.
import { readFileSync, writeFileSync } from "node:fs";
import { createHash } from "node:crypto";
import { fileURLToPath } from "node:url";
import path from "node:path";

const root = path.dirname(fileURLToPath(import.meta.url));
const script = readFileSync(path.join(root, "script.md"), "utf8");
const scriptRows = script.split(/\r?\n/u).filter((line) => /^\| c06\d{4} \|/u.test(line)).map((line) => {
  const parts = line.split("|").map((part) => part.trim());
  if (parts.length !== 5 || !/^c060[1-6]\d{2}$/u.test(parts[1]) || !parts[2] || !parts[3]) {
    throw new Error(`invalid script row: ${line}`);
  }
  return { id: parts[1], text: parts[2], evidence: parts[3] };
});
const visualRows = readFileSync(path.join(root, "visual-plan.tsv"), "utf8")
  .replace(/(?:\r?\n)+$/u, "").split(/\r?\n/u).map((line) => {
    const parts = line.split("\t");
    const [id, template, content, value = "", source = ""] = parts;
    if (parts.length !== (template === "shot" ? 3 : 5)) throw new Error(`invalid visual row: ${line}`);
    if (!/^c060[1-6]\d{2}$/u.test(id) || !["shot", "stats"].includes(template) || !content) {
      throw new Error(`invalid visual ID/template: ${line}`);
    }
    if (template === "shot" && (value || source)) throw new Error(`shot has card fields: ${id}`);
    if (template === "stats" && (!value || !source)) throw new Error(`card lacks value/source: ${id}`);
    return { id, template, content, value, source };
  });
if (scriptRows.length !== 94 || visualRows.length !== 94) {
  throw new Error(`C06 needs 94 script and visual rows, got ${scriptRows.length}/${visualRows.length}`);
}
const visuals = new Map(visualRows.map((row) => [row.id, row]));
if (visuals.size !== 94 || new Set(scriptRows.map((row) => row.id)).size !== 94) {
  throw new Error("duplicate script or visual ID");
}
const chapterNames = [
  "同一團材料的兩份工作",
  "清潔架上的 Kutol",
  "舊需求慢慢變小",
  "教室裡看見第二種用途",
  "名字、顏色與玩法",
  "專利在後，兩家公司各走各路",
];
const codes = ["h", "o", "i", "e", "t", "n"];
const cameras = ["push in", "pan left", "pull out", "pan right", "tilt up"];
// Provisional spoken forms for local lint; a separate listening/pronunciation review is still required before paid TTS.
const pronunciations = [
  ["Marshall Field's", "馬歇爾菲爾德百貨"],
  ["Rainbow Crafts", "彩虹工藝公司"],
  ["General Mills", "通用磨坊"],
  ["The Strong", "史壯玩具博物館"],
  ["Fun Factory", "造型工廠"],
  ["Macy's", "梅西百貨"],
  ["Play-Doh", "培樂多"],
  ["Kroger", "克羅格"],
  ["Kutol", "庫托"],
  ["Kenner", "肯納"],
  ["Hasbro", "孩之寶"],
];
const spoken = (text) => pronunciations.reduce((value, [name, say]) => value.replaceAll(name, say), text);
const textHash = (text) => createHash("sha256").update(String(text).normalize("NFC"), "utf8").digest("hex").slice(0, 12);
let lastChapter = 0;
let cards = 0;
let cardRun = 0;
let longestCardRun = 0;
const scenes = scriptRows.map(({ id, text }, index) => {
  const chapter = Number(id[4]);
  const visual = visuals.get(id);
  if (!visual) throw new Error(`missing visual for ${id}`);
  if (chapter < lastChapter) throw new Error(`chapter order reversed at ${id}`);
  const scene = {
    id: `c06-${codes[chapter - 1]}${id.slice(-2)}`,
    ...(chapter !== lastChapter ? { chapter: chapterNames[chapter - 1] } : {}),
    template: visual.template,
    data: visual.template === "shot"
      ? { prompt: visual.content, camera: cameras[index % cameras.length], visual: "still" }
      : { stats: [{ value: visual.value, label: visual.content }], source: visual.source },
    lines: [{
      id,
      text,
      ...(spoken(text) !== text ? { say: spoken(text), say_for: textHash(text) } : {}),
      emotion: /[？?]$/u.test(text) ? "說書語氣，問句上揚，停半拍" : "說書語氣，自然有起伏",
    }],
  };
  if (visual.template === "stats") { cards += 1; cardRun += 1; }
  else cardRun = 0;
  longestCardRun = Math.max(longestCardRun, cardRun);
  lastChapter = chapter;
  return scene;
});
if (cards !== 14 || (scenes.length - cards) / scenes.length < 0.7 || longestCardRun > 3) {
  throw new Error(`Curio visual split failed: ${scenes.length - cards} shots, ${cards} cards, run ${longestCardRun}`);
}

const loops = [
  ["c060106", "c060409", "清潔膏變玩具是否只是換罐子"],
  ["c060107", "c060601", "兒童造型用途的專利何時申請"],
  ["c060108", "c060611", "舊清潔公司後來去哪裡"],
  ["c060205", "c060207", "清潔膏解決哪一種家裡的污痕"],
  ["c060209", "c060310", "柔軟材料除了去污還能有什麼工作"],
  ["c060211", "c060302", "靠煤煙需求的商品是否一直穩定"],
  ["c060214", "c060310", "舊清潔需求轉弱後誰會用軟泥"],
  ["c060305", "c060401", "接手者如何找到新用途"],
  ["c060308", "c060309", "教室裡另一種材料為何難捏"],
  ["c060316", "c060415", "教室用途如何成為玩具生意"],
  ["c060405", "c060406", "教室作品是否指向新的顧客"],
  ["c060408", "c060409", "玩具和清潔品的承諾是否相同"],
  ["c060411", "c060414", "玩具首次成交年份為何未能釘死"],
  ["c060414", "c060415", "誰把教室用途變成正式玩具生意"],
  ["c060417", "c060501", "教室之外如何讓家長把玩具帶回家"],
  ["c060503", "c060504", "新買家怎樣一眼看出軟泥能玩"],
  ["c060505", "c060506", "顏色替新買家增加了什麼"],
  ["c060507", "c060508", "全國買家怎樣知道新玩具"],
  ["c060507", "c060508", "怎樣讓更多人看見新玩具"],
  ["c060511", "c060512", "配件如何延伸下一次玩法"],
  ["c060516", "c060518", "產品設計是否真的改變"],
  ["c060519", "c060601", "專利文件是在商品哪一步出現"],
  ["c060604", "c060609", "較早申請能否證明早年配方"],
  ["c060609", "c060610", "出售的是玩具公司還是整間清潔公司"],
];
const sources = [
  ["Kutol 公司沿革（後來回顧）", "https://www.kutol.com/kutols-story/"],
  ["The Strong：Play-Doh 歷史（收藏機構回顧）", "https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/"],
  ["National Toy Hall of Fame：Play-Doh（同機構）", "https://www.toyhalloffame.org/toys/play-doh/"],
  ["US 3,167,440 核發專利文本", "https://patents.google.com/patent/US3167440A/en"],
  ["Kutol 現行清潔產品目錄", "https://www.kutol.com/product-category/products/"],
  ["Hasbro 2026 年 Play-Doh 新品公告", "https://newsroom.hasbro.com/news-releases/news-release-details/hasbro-introduces-blooms-play-doh-new-creative-experience"],
];
const description = `一罐曾被用來清潔壁紙的材料，如何進入玩具箱？本集沿著 Kutol 與收藏機構的後來回顧，拆開教室試用、重新配方、Rainbow Crafts、顏色、電視展示及造型工具的不同步驟。1955 年正式推出與 1956 年向學校行銷分屬不同里程碑；首筆成交年份未明。1960 年的兒童造型材料專利申請，也不證明早年清潔膏配方相同。畫面為匿名敘事示意，不重建真實人物、教室、原包裝或交易。\n\n資料來源（查核日期 2026-10-22）\n${sources.map(([title, url]) => `${title}\n${url}`).join("\n")}`;
const doc = {
  schema_version: 1,
  slug: "story-everyday-play-doh-c06",
  format: "drama",
  category: "explainer",
  narration_locale: "zh-TW",
  target_minutes: [9, 11],
  voice: {
    provider: "gemini",
    name: "Sulafat",
    style: "標準國語、台灣日常說話語調。像跟朋友講一件真實的商業轉折；年份放慢，問句稍停，不演歷史人物。",
    performance: "開場好奇；清潔架和教室用途的動作說清楚；專利日期維持簡潔；最後兩家公司分岔自然收束。",
  },
  subtitles: { burn_in: false },
  look: { preset: "cute-mystery" },
  characters: [],
  series: { slug: "brand-stories-everyday-reversals", episode: 6, chapter: 1 },
  music: { prompt: "light, curious, a little mysterious, no vocals", gain_db: -20, duck_db: -10 },
  loops: loops.map(([setup, payoff, what]) => ({ setup, payoff, what })),
  youtube: {
    category_id: 27,
    made_for_kids: false,
    default_language: "zh-TW",
    title: "Play-Doh：擦壁紙的材料，為何變成孩子的玩具？｜品牌故事",
    description,
    tags: ["Play-Doh", "培樂多", "Kutol", "品牌故事", "日用品的意外轉身", "玩具", "商業故事"],
    video_id: null,
  },
  thumbnail: { template: "thumb", data: { headline: "擦壁紙？\n**變玩具**", tag: "品牌故事", brand: "PLAY-DOH", shot: "c06-h01" } },
  sources: sources.map(([title, url]) => ({ title, url, checked_on: "2026-10-22" })),
  assets: [],
  scenes,
};
writeFileSync(path.join(root, "video.json"), `${JSON.stringify(doc, null, 2)}\n`, "utf8");
console.log(`${scenes.length} scenes, ${scenes.length - cards} shots, ${cards} cards, max consecutive cards ${longestCardRun}, ${loops.length} loops`);
