#!/usr/bin/env node
// ARCHIVAL ONLY: this was the 2026-10-21 preproduction builder (83 stills/11 cards,
// 78-store slide reading). The current C03 video.json has later visual recuts and a
// 79-store annual-report correction. Do not use this script to rebuild the film.
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { spokenUnits } from "../../../tools/video/core/timeline.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const narrationFile = path.join(here, "narration-draft.md");
const narrationBytes = readFileSync(narrationFile);
const narrationSha256 = createHash("sha256").update(narrationBytes).digest("hex");
const reviewedNarrationSha256 = "78955feebfaa88cc677688843ae9d181c3f4714401820566406a5bc99ecf9348";
if (narrationSha256 !== reviewedNarrationSha256) {
  throw new Error(`narration-draft.md changed: ${narrationSha256}; obtain a new independent review before rebuilding`);
}

const paragraphs = [...narrationBytes.toString("utf8").matchAll(/^(\d\d)｜(.+)$/gm)].map((match) => ({
  number: Number(match[1]),
  text: match[2].replace(/\[[^\]]+\]/g, "").replace(/\*\*/g, "").trim(),
}));
if (paragraphs.length !== 20 || paragraphs.some((p, index) => p.number !== index + 1)) {
  throw new Error("expected the reviewed narration's twenty numbered paragraphs in order");
}

// First split on sentence endings. Only two long sentences need a pause within the
// sentence; use their natural comma/colon. Keep a fixed number of scenes per
// paragraph so a reviewed wording change does not renumber unrelated scene IDs.
function splitLong(text) {
  if (spokenUnits(text) <= 42) return [text];
  const candidates = [...text.matchAll(/[，：、]/g)].map((hit) => hit.index + 1)
    .filter((at) => spokenUnits(text.slice(0, at)) >= 12 && spokenUnits(text.slice(at)) >= 12);
  if (!candidates.length) throw new Error(`no natural cut in long narration: ${text}`);
  const middle = spokenUnits(text) / 2;
  const at = candidates.sort((a, b) => Math.abs(spokenUnits(text.slice(0, a)) - middle) - Math.abs(spokenUnits(text.slice(0, b)) - middle))[0];
  return [...splitLong(text.slice(0, at)), ...splitLong(text.slice(at))];
}

const segmented = paragraphs.map((p) => ({
  number: p.number,
  source: p.text,
  lines: (p.text.match(/[^。！？；]+[。！？；]?/g) ?? []).flatMap(splitLong).map((text) => text.trim()),
}));
if (segmented.some((p) => p.lines.join("") !== p.source)) {
  throw new Error("segmentation changed reviewed narration wording");
}
const expectedSceneCounts = [6, 4, 4, 4, 5, 5, 6, 4, 4, 5, 4, 5, 5, 4, 5, 4, 3, 7, 6, 4];
for (const p of segmented) {
  const target = expectedSceneCounts[p.number - 1];
  while (p.lines.length > target) {
    const choices = p.lines.slice(0, -1).map((line, index) => ({
      index, units: spokenUnits(line + p.lines[index + 1]),
    })).filter((choice) => choice.units <= 42);
    if (!choices.length) throw new Error(`cannot merge paragraph ${p.number} into ${target} scenes`);
    choices.sort((a, b) => a.units - b.units || a.index - b.index);
    const index = choices[0].index;
    p.lines.splice(index, 2, p.lines[index] + p.lines[index + 1]);
  }
  if (p.lines.length !== target) throw new Error(`paragraph ${p.number} has ${p.lines.length} scenes, expected ${target}`);
}
const sceneCount = segmented.reduce((sum, p) => sum + p.lines.length, 0);
if (sceneCount !== 94 || segmented.some((p) => p.lines.join("") !== p.source)) {
  throw new Error("scene allocation failed to preserve the reviewed narration");
}

const chapterAt = new Map([
  [1, "一本空白本走上交易所"],
  [2, "無名舊本有了新名字"],
  [5, "空白頁被當成一本書"],
  [8, "出版社的點子變成投資標的"],
  [13, "新主人買下品牌，也接下成本"],
  [17, "故事還在，帳面價值要重算"],
]);

const statsCards = new Map([
  [1, { find: "2013 年 4 月 3 日", data: { title: "一本本子走進股市", stats: [{ value: "2013 年 4 月 3 日", label: "義大利交易所掛牌" }], source: "義大利交易所，2013-04-03 上市公告" } }],
  [2, { find: "1986 年停業", data: { title: "品牌轉述的作家故事", stats: [{ value: "1986 年", label: "官網轉述的圖爾製造者停業年份" }], source: "Moleskine 官網 Our Heritage；轉述 Chatwin，非獨立工廠檔案" } }],
  [4, { find: "1997 年 11 月 26 日", data: { title: "舊物件，新的商標", stats: [{ value: "1995 年", label: "招股書記載重啟生產" }, { value: "1997 年", label: "商標註冊" }], source: "2013 年義大利上市招股書，頁 121–122、138–139" } }],
  [5, { find: "還沒寫出來的書", data: { title: "發行人的產品定位", stats: [{ value: "待寫的書", label: "空白頁交給使用者完成" }], source: "2013 年義大利上市招股書，頁 138–139" } }],
  [7, { find: "2005 年約有", data: { title: "批發銷售據點，不是直營店", stats: [{ value: "約 1.2 萬", label: "2005 年據點" }, { value: "約 2 萬", label: "2010 年據點" }], source: "D’Ieteren 2017 投資人簡報，投影片 11、15–16" } }],
  [11, { find: "市值約四億八千八百萬", data: { title: "上市時整家公司市值", stats: [{ value: "約 4.88 億歐元", label: "2013 年 4 月 3 日；非當年營收" }], source: "義大利交易所，2013-04-03 上市公告" } }],
  [12, { find: "七十八家直營店", data: { title: "從批發走向直營", stats: [{ value: "78 家", label: "2016 年底直營店" }], source: "D’Ieteren 2017 投資人簡報，投影片 15–16" } }],
  [13, { find: "四成一股權", data: { title: "收購先簽約", stats: [{ value: "41%", label: "2016 年 9 月簽約收購股權" }], source: "D’Ieteren，2016-09-22 收購公告" } }],
  [15, { find: "百分之八十一", data: { title: "新主人接下的營收結構", stats: [{ value: "81%", label: "2017 年紙本產品銷售占比" }], source: "D’Ieteren，2017 Activity Report，頁 44–45" } }],
  [18, { find: "一億零七百四十萬", data: { title: "品牌資產的帳面重算", stats: [{ value: "約 1.074 億歐元", label: "2025 年品牌無形資產減損；非現金流出" }], source: "D’Ieteren，2025 Full-Year Results，頁 10、25" } }],
  [19, { find: "五千兩百二十萬", data: { title: "2026 年上半年", stats: [{ value: "約 5,220 萬歐元", label: "半年銷售；年增 2.2%" }], source: "D’Ieteren，2026 H1 Results，頁 9" } }],
]);

// Each sentence's still uses one anonymous person doing a concrete action in a
// neutral present-day space. These motifs intentionally avoid reconstructing a
// claimed historic shop, factory, stock-exchange floor or named person.
const motifs = {
  1: ["one anonymous customer lifting an unmarked black pocket notebook from a generic bookshop shelf", "one anonymous office analyst placing a plain notebook beside a blank price chart", "one anonymous reader comparing an unmarked old book with a blank pocket notebook", "one anonymous accountant studying blank cards beside a closed notebook on a desk", "one anonymous customer opening a plain notebook to empty pages at a bookshop table", "one anonymous office clerk setting an unmarked notebook beside a closed plain folder"],
  2: ["one anonymous traveler reading an unmarked book at a simple table", "one anonymous customer searching a generic stationery shelf with a visible empty space", "one anonymous traveler gathering several plain pocket notebooks in a small bag", "one anonymous reader closing an unmarked book beside a black notebook", "one anonymous customer looking at a row of plain notebooks in a present-day shop"],
  3: ["one anonymous maker laying a black blank notebook on a design worktable", "one anonymous design worker inspecting the rounded corner of a plain black notebook sample", "one anonymous design worker testing the elastic closure on a plain pocket notebook", "one anonymous reader opening the back pocket of a plain notebook", "one anonymous shopkeeper arranging unmarked pocket notebooks on a neutral shelf"],
  4: ["one anonymous publisher placing a blank notebook beside an unmarked folder", "one anonymous maker comparing an old plain notebook with a fresh blank one", "one anonymous reader touching a black notebook cover on a bookshop table", "one anonymous shopkeeper lifting a plain notebook beside other unmarked stationery", "one anonymous customer opening an empty notebook to inspect its pages"],
  5: ["one anonymous writer opening an empty notebook at a quiet desk", "one anonymous traveler drawing a simple unlettered line in a blank notebook", "one anonymous reader resting a plain notebook beside a stack of unmarked books", "one anonymous customer turning a blank page while seated near a window", "one anonymous shopkeeper placing a plain notebook beside books on a shelf"],
  6: ["one anonymous bookshop clerk setting a plain notebook beside unmarked books", "one anonymous reader lifting an empty notebook from a generic bookshop table", "one anonymous customer holding a blank notebook near a shelf of books", "one anonymous shopkeeper adjusting an unmarked book and notebook display", "one anonymous reader comparing a closed book with an empty pocket notebook"],
  7: ["one anonymous wholesale worker sorting plain notebooks into unmarked cartons", "one anonymous shopkeeper receiving a small carton of unmarked notebooks", "one anonymous stockroom worker placing closed blank cartons on a shelf", "one anonymous retailer pausing before replenishing a generic bookshop display", "one anonymous warehouse worker checking a stack of unmarked cartons", "one anonymous storekeeper opening a plain carton of black notebooks"],
  8: ["one anonymous office worker moving a plain notebook beside an unmarked folder", "one anonymous shopkeeper holding a black notebook in a generic store", "one anonymous investor placing two blank folders across a neutral meeting table", "one anonymous clerk closing a plain company folder beside a notebook", "one anonymous office worker arranging unmarked folders on a desk"],
  9: ["one anonymous office clerk arranging unmarked notebooks beside a plain folder", "one anonymous shopkeeper placing a blank planner beside a pocket notebook", "one anonymous traveler setting a plain notebook beside an unmarked bag", "one anonymous stationery clerk aligning several plain paper products on a shelf", "one anonymous customer lifting a blank notebook from a generic display"],
  10: ["one anonymous customer comparing a plain notebook and unmarked travel accessories", "one anonymous shopkeeper arranging writing tools beside blank notebooks", "one anonymous traveler placing an unmarked journal inside a simple bag", "one anonymous store clerk opening a plain notebook on a neutral retail table", "one anonymous customer inspecting a shelf of unmarked writing goods"],
  11: ["one anonymous office analyst setting an unmarked notebook beside blank accounting cards", "one anonymous investor studying a closed plain folder beside a pocket notebook", "one anonymous store clerk comparing an unmarked notebook display with a blank tablet screen", "one anonymous office clerk moving an unmarked notebook beside a small stack of blank folders", "one anonymous analyst holding a plain notebook over a clean desk"],
  12: ["one anonymous shopkeeper filling a generic retail shelf with unmarked notebooks", "one anonymous customer opening a plain notebook in a small modern shop", "one anonymous store clerk placing an unmarked pen beside a black notebook", "one anonymous retail employee checking blank display panels near notebooks", "one anonymous worker packing a plain notebook for an online order", "one anonymous shopkeeper straightening a display of unmarked notebooks and bags"],
  13: ["one anonymous office clerk placing a blank folder beside a black notebook", "one anonymous accountant arranging two unmarked folders on a meeting table", "one anonymous warehouse worker moving plain notebooks into cartons", "one anonymous investor holding a closed plain folder in a neutral office", "one anonymous retail worker arranging unmarked notebooks on a store shelf"],
  14: ["one anonymous office clerk handing a closed blank folder across an empty meeting table", "one anonymous accountant closing an unmarked company folder beside a notebook", "one anonymous office clerk transferring a sealed paper folder across a contemporary meeting table", "one anonymous customer lifting an unmarked black notebook in a generic shop", "one anonymous office worker stacking blank folders beside a paper notebook"],
  15: ["one anonymous customer holding a plain notebook beside an unmarked bag", "one anonymous reader turning a blank paper page at a desk", "one anonymous traveler laying an unmarked writing tool beside a pocket notebook", "one anonymous customer moving a plain notebook near a blank tablet screen", "one anonymous shopkeeper arranging unmarked paper goods and accessories"],
  16: ["one anonymous retail worker tidying a modest shelf of plain notebooks", "one anonymous store clerk closing an unmarked sales folder at a counter", "one anonymous worker packing a black notebook at a generic online-order desk", "one anonymous accountant checking blank expense cards beside a notebook", "one anonymous shopkeeper examining an unmarked carton in a small stockroom"],
  17: ["one anonymous accountant looking at blank sales cards beside a pocket notebook", "one anonymous shopkeeper arranging plain notebooks on a shelf", "one anonymous warehouse worker pausing beside unmarked notebook cartons", "one anonymous retail worker placing a plain notebook on a clean display", "one anonymous office worker closing a blank sales folder near a notebook"],
  18: ["one anonymous wholesale worker leaving an unmarked carton on a stockroom shelf", "one anonymous storekeeper deciding how many plain notebooks to place on a shelf", "one anonymous office clerk lining up blank order cards beside a notebook", "one anonymous accountant sliding a plain ledger folder beside a black notebook", "one anonymous investor turning a blank card over near a closed notebook", "one anonymous shopkeeper inspecting a modest notebook display", "one anonymous stockroom worker carrying a small carton of plain notebooks"],
  19: ["one anonymous shopkeeper restocking a generic shelf with plain notebooks", "one anonymous office accountant updating blank loan account cards beside a notebook", "one anonymous accountant reviewing blank operating cards on a clean desk", "one anonymous customer opening a black notebook to blank pages", "one anonymous store clerk placing a new stack of unmarked notebooks on a shelf", "one anonymous shopper choosing a plain pocket notebook at a clean counter"],
  20: ["one anonymous reader opening a blank notebook at a warm reading table", "one anonymous customer feeling the plain paper of an unmarked notebook", "one anonymous bookshop shopper holding a black notebook in both hands", "one anonymous reader closing an unmarked notebook with a small smile"],
};

// Context cuts keep the book present as the story's main object without filling
// every frame with the same cover. Exterior and evening views are deliberately
// present-day, anonymous illustrations of a sales system, never archival claims.
// Keys are zero-based still ordinals within each reviewed paragraph; cards do
// not consume an ordinal.
const contextCuts = {
  1: {
    1: { detail: "one anonymous office analyst placing a blank price chart on a desk", light: "cool office light at dusk" },
    2: { detail: "one anonymous reader comparing unmarked old books at a contemporary street bookstall", light: "overcast afternoon light" },
    3: { detail: "one anonymous accountant studying empty finance cards on a desk", light: "quiet evening desk light" },
  },
  2: {
    1: { detail: "one anonymous customer searching a present-day open-air stationery stall with an empty shelf", light: "soft morning light" },
    2: { detail: "one anonymous traveler gathering plain pocket books at a contemporary station kiosk", light: "dusk street light" },
  },
  3: {
    0: { detail: "one anonymous maker selecting blank paper samples at a modest design table" },
    2: { detail: "one anonymous craft worker checking a rounded black cover sample with a plain elastic band" },
    3: { detail: "one anonymous publisher comparing blank cover samples in a small workshop" },
  },
  4: {
    0: { detail: "one anonymous reader browsing anonymous art history volumes in a public library" },
    2: { detail: "one anonymous customer comparing blank paper and black cover samples at a bookshop table" },
  },
  5: {
    1: { detail: "one anonymous traveler drawing a simple line on loose blank paper at an outdoor cafe table", light: "bright afternoon light" },
    3: { detail: "one anonymous shopkeeper surveying several bookshop shelf locations with blank display panels" },
  },
  6: {
    1: { detail: "one anonymous reader lifting an unlettered book from a neighborhood bookshop shelf" },
    3: { detail: "one anonymous bookshop employee adjusting a display of blank shelf cards" },
    4: { detail: "one anonymous shopper stepping out of a present-day bookshop with a plain paper bag", light: "gentle twilight outside" },
  },
  7: {
    1: { detail: "one anonymous shopkeeper receiving a sealed carton at an open-air storefront", light: "overcast morning light" },
  },
  8: {
    0: { detail: "one anonymous office clerk sliding two closed blank folders across a meeting table" },
    3: { detail: "one anonymous office worker standing beside a closed archive cabinet", light: "warm office light after dark" },
  },
  9: {
    1: { detail: "one anonymous stationery clerk aligning a blank planner, plain pen and simple travel bag on a shelf" },
    2: { detail: "one anonymous traveler setting a plain bag on a contemporary station plaza bench", light: "clear morning light outdoors" },
  },
  10: {
    1: { detail: "one anonymous store clerk arranging an unlettered book, travel bag and writing tool on a display" },
    3: { detail: "one anonymous customer lifting a black pocket book from a clean shop shelf" },
  },
  11: {
    0: { detail: "one anonymous office analyst sorting blank price cards on a desk" },
    1: { detail: "one anonymous investor reviewing an unlettered balance sheet folder" },
  },
  12: {
    0: { detail: "one anonymous warehouse worker carrying a sealed carton across an open loading bay", light: "cool morning light outdoors" },
    2: { detail: "one anonymous retail clerk grouping plain bags and writing tools on a small display" },
    3: { detail: "one anonymous office buyer studying a blank sales-channel board at a meeting table" },
  },
  13: {
    0: { detail: "one anonymous service technician holding an unbranded car-window panel in a neutral workshop" },
  },
  14: {
    1: { detail: "one anonymous accountant sliding a blank share folder across a meeting table" },
    3: { detail: "one anonymous shopkeeper arranging plain bags, pens and paper journals near a street-facing window", light: "late afternoon light" },
  },
  15: {
    0: { detail: "one anonymous customer comparing a plain backpack and an unmarked writing tool in a stationery shop" },
    3: { detail: "one anonymous retail employee looking at a modest present-day storefront from a city sidewalk", light: "evening street light" },
  },
  16: {
    2: { detail: "one anonymous accountant checking blank cost cards beside a shop till" },
    3: { detail: "one anonymous wholesale worker facing stacked sealed cartons at an open loading bay", light: "blue evening light outdoors" },
  },
  17: {
    0: { detail: "one anonymous accountant reviewing blank annual-report pages on a clean desk" },
    2: { detail: "one anonymous warehouse worker checking a few sealed order cartons on a wholesale shelf beside an open loading bay", light: "rainy overcast daylight" },
  },
  18: {
    0: { detail: "one anonymous wholesale worker facing sealed cartons in a contemporary loading bay", light: "rainy morning daylight outdoors" },
    2: { detail: "one anonymous office clerk lining up blank order cards on a desk" },
    3: { detail: "one anonymous accountant sliding a plain ledger folder across a desk" },
    4: { detail: "one anonymous retailer comparing a modest paper-goods shelf with a small reorder stack and face-down wholesale order cards" },
    5: { detail: "one anonymous shopkeeper outside a storefront studying an undecorated shelf through the window", light: "quiet dusk street light" },
  },
  19: {
    1: { detail: "one anonymous office accountant updating blank loan account cards at a desk" },
    4: { detail: "one anonymous shopper taking a plain paper bag from an open-air bookstall", light: "soft street lighting after dark" },
  },
  20: {
    1: { detail: "one anonymous customer feeling the texture of a blank paper sample at a bookshop counter" },
    3: { detail: "one anonymous reader walking away from a contemporary bookshop with a plain bag", light: "fresh morning light outdoors" },
  },
};

const framings = ["Medium shot", "Wide shot", "Close-up", "Medium shot", "Wide shot", "Close-up"];
const cameras = ["push in", "pan left", "pull out", "pan right", "tilt up", "tilt down"];
const light = ["soft window light", "neutral ceiling light", "gentle afternoon light", "diffuse daylight"];
const scenes = [];
const linesByParagraph = new Map();
let shotNumber = 0;
let cardNumber = 0;
for (const p of segmented) {
  let localShot = 0;
  const lineIds = [];
  for (const [index, text] of p.lines.entries()) {
    const id = `c03-p${String(p.number).padStart(2, "0")}-s${String(index + 1).padStart(2, "0")}`;
    const lineId = `c03${String(p.number).padStart(2, "0")}${String(index + 1).padStart(2, "0")}`;
    lineIds.push(lineId);
    const card = statsCards.get(p.number);
    const isCard = Boolean(card && text.includes(card.find));
    let data;
    if (isCard) {
      data = card.data;
      cardNumber += 1;
      statsCards.delete(p.number);
    } else {
      const options = motifs[p.number];
      if (!options?.length) throw new Error(`missing visual motif for paragraph ${p.number}`);
      const chosen = contextCuts[p.number]?.[localShot];
      const detail = chosen?.detail ?? options[localShot % options.length];
      data = {
        prompt: `${framings[(shotNumber + localShot) % framings.length]}, ${detail}, ${chosen?.light ?? light[shotNumber % light.length]}.`,
        camera: cameras[shotNumber % cameras.length],
        visual: "still",
      };
      localShot += 1;
      shotNumber += 1;
    }
    scenes.push({
      id,
      ...(index === 0 && chapterAt.has(p.number) ? { chapter: chapterAt.get(p.number) } : {}),
      template: isCard ? "stats" : "shot",
      data,
      lines: [{ id: lineId, text, emotion: "說書語氣，句尾自然停頓，問題留半拍" }],
    });
  }
  linesByParagraph.set(p.number, lineIds);
}
if (statsCards.size || shotNumber !== 83 || cardNumber !== 11) {
  throw new Error(`visual allocation mismatch: ${shotNumber} stills, ${cardNumber} stats cards, missing cards ${[...statsCards.keys()]}`);
}

const lineContaining = (paragraph, fragment) => {
  const index = segmented[paragraph - 1].lines.findIndex((text) => text.includes(fragment));
  if (index < 0) throw new Error(`loop anchor missing in paragraph ${paragraph}: ${fragment}`);
  return linesByParagraph.get(paragraph)[index];
};
const first = (paragraph) => linesByParagraph.get(paragraph)[0];
const last = (paragraph) => linesByParagraph.get(paragraph).at(-1);
const loopRows = [
  [lineContaining(1, "作家"), lineContaining(4, "他們用過的不是"), "早於商標的舊式筆記本與現代品牌的關係"],
  [lineContaining(1, "另一家公司"), first(13), "上市後由哪家公司接手股份"],
  [lineContaining(1, "財報"), lineContaining(18, "帳面價值下調"), "財報後來將品牌無形資產帳面價值下調多少"],
  [last(2), first(3), "哪家出版商重啟這類小本子"],
  [last(3), first(4), "重新生產何時變成自己的商標"],
  [last(4), first(5), "黑色空白本還賣什麼定位"],
  [last(5), first(6), "待寫的書先走進哪種店"],
  [last(6), first(7), "少數書架如何擴張到更多城市"],
  [last(7), first(8), "擴張批發網由誰投資"],
  [last(8), first(9), "商標何時成為公司名稱"],
  [last(9), first(10), "同名商品往哪裡延伸"],
  [last(10), first(11), "上市市場替公司標了多少價"],
  [last(11), first(12), "批發之外為何經營直營與電商"],
  [last(12), first(13), "更大的通路網吸引了哪位買方"],
  [last(13), first(14), "簽約後股份最終到誰手裡"],
  [last(14), first(15), "新主人接下的生意還靠紙本嗎"],
  [last(15), first(16), "直營店先碰上什麼營運問題"],
  [last(16), lineContaining(17, "除了批發"), "多年後哪條早期通路先踩煞車"],
  [last(17), first(18), "批發為何拖住 2025 年銷售"],
  [last(18), first(19), "品牌減損後下個半年的補貨變化"],
  [last(19), first(20), "下一本筆記本如何再次被買走"],
];

const sources = [
  ["Moleskine 2013 年義大利上市招股書", "https://www.borsaitaliana.it/prospetti-informativi/1513pros_1_it.pdf"],
  ["Moleskine, Our Heritage", "https://www.moleskine.com/en-hk/the-world-of-moleskine/our-heritage/"],
  ["Moleskine, Code of Ethics", "https://www.moleskine.com/en-no/code-of-ethics.html"],
  ["D’Ieteren 2017 年投資人簡報", "https://dieterengroup.imgix.net/documents/presentations/moleskine_lorenzo_viglione.pdf"],
  ["義大利交易所 2013 年上市公告", "https://www.borsaitaliana.it/borsaitaliana/ufficio-stampa/comunicati-stampa/2013/moleskine.en.htm"],
  ["D’Ieteren 2016 年收購公告", "https://dieterengroup.imgix.net/press-releases/DIeteren-Moleskine_-ENG_FINAL.pdf"],
  ["D’Ieteren 2017 年完成收購公告", "https://dieterengroup.imgix.net/press-releases/2017_01_24_Moleskine_squeeze_out_EN.pdf"],
  ["D’Ieteren 2017 Activity Report — Moleskine", "https://dieterengroup.imgix.net/annual-reports/3_moleskine_en.pdf"],
  ["D’Ieteren 2017 Annual Report", "https://dieterengroup.imgix.net/annual-reports/annualreport2017_en_0-1.pdf"],
  ["D’Ieteren 2025 Full-Year Results", "https://dieterengroup.imgix.net/press-releases/20260310_FY-2025-Results_EN_FV.pdf"],
  ["D’Ieteren 2026 Half-Year Results", "https://dieterengroup.imgix.net/press-releases/20260909_Press-release_H1-2026-results_EN_FV-with-appendix.pdf"],
].map(([title, url]) => ({ title, url, checked_on: "2026-10-21" }));

const doc = {
  schema_version: 1,
  slug: "story-everyday-moleskine-c03",
  format: "drama",
  category: "explainer",
  narration_locale: "zh-TW",
  target_minutes: [9, 11],
  voice: {
    provider: "gemini",
    name: "Sulafat",
    style: "標準國語，咬字清楚，台北人平常說話的語調。像跟朋友講一段真實的商業轉折，數字放慢，問句上揚，揭曉前停半拍。",
    performance: "開場交易所壓低；舊本與新商標分開說；通路擴張加快；收購與減損的不同會計概念放慢；2026 回升保持克制；結尾親近自然。",
  },
  subtitles: { burn_in: false },
  look: { preset: "cute-mystery" },
  characters: [],
  series: { slug: "brand-stories-everyday-reversals", episode: 3, chapter: 1 },
  music: { prompt: "light, curious, a little mysterious, no vocals", gain_db: -20, duck_db: -10 },
  loops: loopRows.map(([setup, payoff, what]) => ({ setup, payoff, what })),
  youtube: {
    category_id: 27,
    made_for_kids: false,
    default_language: "zh-TW",
    title: "Moleskine：新品牌如何把老式筆記本變成全球生意？｜品牌故事",
    description: "1997 年才註冊的現代品牌，怎麼把無名的舊式小黑本做成跨國生意？這集從品牌轉述的 Chatwin 故事、米蘭出版商的書店策略，走到上市、收購與 2025–2026 年的通路和財務變化。\n\n歷史藝術家沒有使用後來註冊的 Moleskine 品牌商品；品牌官網的 1986 年故事屬於其轉述。2013 年上市市值、2017 年紙本營收比重、2025 年品牌減損與 2026 年半年業績是不同財務概念。插圖為匿名敘事示意，不代表歷史人物、真實工廠、上市會場或交易現場。資料查核日期：2026-10-21。\n\n一手來源：\n" + sources.map((source) => `${source.title}\n${source.url}`).join("\n"),
    tags: ["Moleskine", "筆記本", "品牌故事", "日用品的意外轉身", "書店", "品牌歷史"],
  },
  thumbnail: {
    template: "thumb",
    data: { headline: "新品牌\n**老故事？**", tag: "品牌故事", brand: "Moleskine", shot: scenes.findLast((scene) => scene.template === "shot").id },
  },
  sources,
  assets: [],
  scenes,
};

const out = path.join(here, "video.json");
if (process.argv.includes("--inspect")) {
  const chapterCounts = [];
  for (const [index, p] of segmented.entries()) {
    const pScenes = scenes.filter((scene) => scene.id.startsWith(`c03-p${String(p.number).padStart(2, "0")}-`));
    chapterCounts.push(`${String(index + 1).padStart(2, "0")}: ${pScenes.length} scenes (${pScenes.filter((scene) => scene.template === "stats").length} card), ${p.lines.map((line) => spokenUnits(line)).join("/")} units`);
  }
  process.stdout.write(`${chapterCounts.join("\n")}\n`);
} else {
  throw new Error(`archival ${doc.slug} builder (${shotNumber} stills/${cardNumber} cards) cannot overwrite the current 67-still/27-card film at ${out}`);
}
