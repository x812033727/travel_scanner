// Rebuild the non-paid C04 manuscript and scene plan. No media or network calls.
import { readFileSync, writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";
import { textHash } from "../../../tools/video/core/schema.mjs";

const root = path.dirname(fileURLToPath(import.meta.url));
const readRows = (name, columns) => readFileSync(path.join(root, name), "utf8")
  .replace(/(?:\r?\n)+$/u, "").split(/\r?\n/u).filter(Boolean).map((row, index) => {
    const parts = row.split("\t");
    if (parts.length !== columns) throw new Error(`${name}:${index + 1}: expected ${columns} tab-separated fields, got ${parts.length}`);
    return parts;
  });

const chapterNames = new Map([
  ["H", "出貨箱裡的壁紙"],
  ["O", "先想讓牆面有花紋"],
  ["I", "溫室只是過站"],
  ["E", "一九五九年的接縫"],
  ["T", "箱子裡的工作"],
  ["N", "連空氣加入的時間也改了"],
]);
const chapterNumbers = new Map([...chapterNames.keys()].map((key, index) => [key, index + 1]));
const rows = readRows("draft-lines.tsv", 4);
const visualRows = readRows("visual-plan.tsv", 5);
if (rows.length !== 94 || visualRows.length !== rows.length) throw new Error(`C04 needs 94 script and visual rows, got ${rows.length}/${visualRows.length}`);
const visuals = new Map(visualRows.map(([id, template, content, value, source]) => [id, { template, content, value, source }]));
if (visuals.size !== rows.length) throw new Error("duplicate or missing visual IDs");
let lastChapter = "";
let cards = 0;
let run = 0;
let longestCardRun = 0;
const cameras = ["push in", "pan left", "pull out", "pan right", "tilt up"];
const scenes = rows.map(([chapter, draftId, text, claims], index) => {
  if (!chapterNames.has(chapter) || !new RegExp(`^${chapter}[0-9]{2}$`, "u").test(draftId)) throw new Error(`bad draft ID ${draftId}`);
  if (!text || !claims) throw new Error(`empty script or source annotation at ${draftId}`);
  const visual = visuals.get(draftId);
  if (!visual || !["shot", "stats"].includes(visual.template)) throw new Error(`missing visual for ${draftId}`);
  const say = text.replace(/\bIBM\b/gu, "愛比欸姆");
  const scene = {
    id: `c04-${draftId.toLowerCase()}`,
    ...(lastChapter !== chapter ? { chapter: chapterNames.get(chapter) } : {}),
    template: visual.template,
    data: visual.template === "shot"
      ? { prompt: visual.content, camera: cameras[index % cameras.length], visual: "still" }
      : { stats: [{ value: visual.value, label: visual.content }], source: visual.source },
    lines: [{
      id: `c04${String(chapterNumbers.get(chapter)).padStart(2, "0")}${draftId.slice(1)}`,
      text,
      ...(say !== text ? { say, say_for: textHash(text) } : {}),
      emotion: /[？?]$/u.test(text) ? "說書語氣，問句上揚，停半拍" : "說書語氣，自然有起伏",
    }],
  };
  if (visual.template === "stats") { cards += 1; run += 1; }
  else run = 0;
  longestCardRun = Math.max(longestCardRun, run);
  lastChapter = chapter;
  return scene;
});
if (cards > 28 || longestCardRun > 3 || (scenes.length - cards) / scenes.length < 0.7) throw new Error(`Curio visual split failed: ${scenes.length - cards} shots, ${cards} cards, run ${longestCardRun}`);

const id = (draftId) => `c04${String(chapterNumbers.get(draftId[0])).padStart(2, "0")}${draftId.slice(1)}`;
const loopRows = [
  ["H02", "T12", "早期電腦與這張氣室薄片的關聯"],
  ["H03", "O03", "氣室材料原本打算貼在哪裡"],
  ["H07", "I02", "溫室用途看中材料的哪項特性"],
  ["H08", "E07", "走向包裝後接縫為何換做法"],
  ["O05", "O09", "薄薄的牆面凸起要怎麼撐住"],
  ["O11", "O14", "裝潢點子後來是否流行"],
  ["O12", "O13", "有背層的薄膜能否順著家具曲線彎曲"],
  ["O17", "I01", "裝飾之外下一個用途在哪裡"],
  ["I06", "I08", "搬運時氣室怎樣先替貨物受力"],
  ["I09", "E08", "泡泡如何在送達時仍保有空氣"],
  ["I14", "E01", "氣室為何一冷卻反而變扁"],
  ["E05", "E07", "每個氣室的接縫如何變得可靠"],
  ["E09", "E11", "熱封平面與成形凸起如何分別控溫"],
  ["E12", "E13", "氣室幾乎壓扁時還能靠什麼抵抗"],
  ["E16", "E18", "包裝專利申請與公司成立孰先孰後"],
  ["E20", "T06", "連續加熱時薄膜如何平整進入模具"],
  ["T04", "T08", "第二張膜如何趕上剛成形氣室並封口"],
  ["T08", "T09", "熱封之後如何避免片材離開滾輪時分開"],
  ["T11", "T12", "哪種貨物被原廠拿來舉出貨案例"],
  ["T15", "N01", "多次搬運後怎樣讓氣室仍有空氣"],
  ["N05", "N06", "為何另一款產品在倉庫先不充氣"],
  ["N06", "N11", "預先鼓起的材料如何減少儲運空間"],
  ["N07", "N08", "平卷能否到包裝台才充氣"],
  ["N11", "N12", "長卷片材如何按眼前箱子取段"],
];

const sources = [
  ["US 3,026,231，牆面用途專利核發文本", "https://patents.google.com/patent/US3026231A/en"],
  ["US 3,142,599，緩衝材料專利核發文本", "https://patents.google.com/patent/US3142599A/en"],
  ["US 3,208,898，壓紋貼合設備專利核發文本", "https://patents.google.com/patent/US3208898A/en"],
  ["Sealed Air 公司史", "https://www.sealedair.com/company/our-company/who-we-are"],
  ["Sealed Air Bubble Wrap 產品史", "https://www.sealedair.com/products/brand/bubble-wrap"],
  ["Sealed Air 2013 年溫室用途回顧", "https://www.sealedair.com/company/media-center/press-releases/sealed-air-announces-finalists-bubble-wrap-appreciation-day-hall-of-fame"],
  ["IBM 1401 官方史", "https://www.ibm.com/history/1401"],
  ["IBM 歷史研究：1401 於 1960 年開始出貨", "https://www.ibm.com/support/pages/zvm/history/360rev.pdf"],
  ["Sealed Air NewAir I.B. 2017 年手冊", "https://www.sealedair.com/content/dam/protective-materials/inflatables/newair-ib/NewAir%20I.B.%20Extreme%20H160%20Brochure.pdf"],
  ["Sealed Air 2012 Form 10-K：1960 年成立", "https://www.sec.gov/Archives/edgar/data/1012100/000119312513087879/d452256d10k.htm"],
];
const description = `泡泡紙原本想貼上牆，最後怎麼走進出貨箱？這集循著三份後來核發、分別標示 1957、1959、1960 年申請日期的美國專利，拆開牆面花紋、緩衝材料與連續製造的不同工作。溫室與 IBM 1401 包裝關聯取自 Sealed Air 後來的回顧；IBM 自身史頁未獨立證實包裝供應商。插圖為敘事示意，不重建當年人物、設備或交易現場。\n\n資料來源（原件；查核日期 2026-10-22）\n${sources.map(([title, url]) => `${title}\n${url}`).join("\n")}`;
const doc = {
  schema_version: 1,
  slug: "story-everyday-bubble-wrap-c04",
  format: "drama",
  category: "explainer",
  narration_locale: "zh-TW",
  target_minutes: [9, 11],
  voice: {
    provider: "gemini",
    name: "Sulafat",
    style: "標準國語、台灣日常說話語調。像跟朋友講一件真實的商業轉折；日期放慢，問題稍停，不演歷史人物。",
    performance: "開場帶好奇；牆面技術用清楚的動作語氣；1959 年接縫揭曉加重；IBM 段落保留公司回顧語氣；結尾親近自然。",
  },
  subtitles: { burn_in: false },
  look: { preset: "cute-mystery" },
  characters: [],
  series: { slug: "brand-stories-everyday-reversals", episode: 4, chapter: 1 },
  music: { prompt: "light, curious, a little mysterious, no vocals", gain_db: -20, duck_db: -10 },
  loops: loopRows.map(([setup, payoff, what]) => ({ setup: id(setup), payoff: id(payoff), what })),
  youtube: {
    category_id: 27,
    made_for_kids: false,
    default_language: "zh-TW",
    title: "Bubble Wrap：泡泡紙本想貼牆，為何走進紙箱？｜品牌故事",
    description,
    tags: ["Bubble Wrap", "泡泡紙", "氣泡紙", "Sealed Air", "品牌故事", "日用品的意外轉身", "包裝", "商業故事"],
    video_id: null,
  },
  thumbnail: { template: "thumb", data: { headline: "貼牆？\n**進紙箱**", tag: "品牌故事", brand: "BUBBLE WRAP", shot: "c04-h01" } },
  sources: sources.map(([title, url]) => ({ title, url, checked_on: "2026-10-22" })),
  assets: [],
  scenes,
};
writeFileSync(path.join(root, "video.json"), `${JSON.stringify(doc, null, 2)}\n`, "utf8");
console.log(`${scenes.length} scenes, ${scenes.length - cards} shots, ${cards} cards, max consecutive cards ${longestCardRun}, ${loopRows.length} loops`);
