// Compose the source-checked X02 drafts into a reviewable local video package.
// Re-run after any draft edit; a changed video hash invalidates media and review receipts.
import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { textHash } from "../../../tools/video/core/schema.mjs";

const dir = path.dirname(fileURLToPath(import.meta.url));
const slug = "story-everyday-dominos-pizza-x02";
const read = name => JSON.parse(readFileSync(path.join(dir, name), "utf8"));
const drafts = [read("drafts/part1.json"), read("drafts/part2.json")];
const original = drafts.flatMap(part => part.scenes);
const sceneWithSpeech = source => {
  const { claim_refs: unused, ...scene } = source;
  scene.lines = scene.lines.map(line => {
    if (!/[A-Za-z]/.test(line.text)) return line;
    const say = line.text
      .replaceAll("Domino’s Pizza", "達美樂披薩")
      .replaceAll("Domino's Pizza", "達美樂披薩")
      .replaceAll("Domino’s", "達美樂")
      .replaceAll("Domino's", "達美樂")
      .replaceAll("Inspired New Pizza", "改良版披薩")
      .replaceAll("Oh Yes We Did", "我們真的做了")
      .replaceAll("BreadBowl Pasta", "麵包碗義大利麵")
      .replaceAll("American Legends", "美國傳奇")
      .replaceAll("Chocolate Lava Crunch Cakes", "熔岩巧克力蛋糕")
      .replaceAll("pizzaturnaround.com", "披薩轉身網站")
      .replaceAll("IPO", "首次公開募股")
      .replaceAll("SEC", "美國證券交易委員會");
    return { ...line, say, say_for: textHash(line.text) };
  });
  return scene;
};
const scenes = original.map(sceneWithSpeech);
const ids = new Map(scenes.flatMap((scene, index) => scene.lines.map(line => [line.id, index])));
const loop = (setup, payoff, what) => {
  if (ids.get(setup) === undefined || ids.get(payoff) === undefined || ids.get(setup) >= ids.get(payoff)) {
    throw new Error(`Invalid story loop: ${setup} → ${payoff}`);
  }
  return { setup, payoff, what };
};

// The opening plants three later payoffs; subsequent chapters keep the factual
// question moving until the next SEC disclosure answers it.
const loops = [
  loop("x020102", "x020505", "遮住的第一季美國同店增幅究竟多少"),
  loop("x020105", "x020301", "招牌產品究竟改動到哪一層"),
  loop("x020106", "x020409", "公司從哪個入口收取消費者回饋"),
  loop("x020107", "x020612", "隔年美國同店是否仍維持正成長"),
  loop("x020204", "x020207", "先前低迷還有哪些壓力"),
  loop("x020210", "x020211", "2009 年全年還有什麼產品動作"),
  loop("x020312", "x020402", "配合新品推出的宣傳活動叫什麼"),
  loop("x020306", "x020612", "配方改動與銷售先後相連能否證明單一原因"),
  loop("x020404", "x020406", "公司稱哪些媒介注意到新品與活動"),
  loop("x020416", "x020505", "可比門市在下一季的整體結果"),
  loop("x020507", "x020601", "首季爆發能否落到全年成績"),
];

const checkedOn = "2026-10-20";
const sources = [
  { title: "Domino’s FY2009 Form 10-K", url: "https://www.sec.gov/Archives/edgar/data/1286681/000119312510045334/d10k.htm", checked_on: checkedOn },
  { title: "Domino’s 2010 Q1 Form 10-Q", url: "https://www.sec.gov/Archives/edgar/data/1286681/000119312510105403/d10q.htm", checked_on: checkedOn },
  { title: "Domino’s FY2010 Form 10-K", url: "https://www.sec.gov/Archives/edgar/data/1286681/000119312511050979/d10k.htm", checked_on: checkedOn },
  { title: "Domino’s FY2011 Form 10-K", url: "https://www.sec.gov/Archives/edgar/data/1286681/000119312512083193/d256751d10k.htm", checked_on: checkedOn },
];
const description = [
  "達美樂在 2009 年第四季重做招牌披薩的核心配方。此前，美國本土同店銷售在 2008 財年下滑 4.9%；2010 年第一季，這項單季指標成長 14.3%。本集沿著 Domino’s 2009–2011 年 SEC 申報，追蹤公司如何把門市成績與新品、宣傳、營運及加盟措施連在一起，以及 2010、2011 全年的後續結果。",
  "",
  "片中數字是美國本土可比門市的同店銷售成長率；2008 年數字是全年，2010 年第一季數字是單季，不能當成同一期間直接相減，也不是全公司營收或全球銷售。公司對成因與顧客反應的描述屬其管理層說法，無法由申報資料拆算單一廣告或單一配方的獨立貢獻。插圖是無標誌的敘事示意，並非真實店面、員工、顧客或原廣告畫面。查核日期：2026-10-20。",
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
  target_minutes: [9, 11],
  voice: {
    provider: "gemini",
    name: "Sulafat",
    style: "標準國語，咬字清楚，台北人平常說話的語調。像跟朋友講一段有原件支持的品牌轉折；數字放慢，問句上揚，揭曉前停半拍。",
    performance: "美國同店銷售的季度與全年數字分別說清；公司歸因每次都明講『公司說』；結尾親近自然，不像念財報。",
  },
  subtitles: { burn_in: false },
  look: { preset: "cute-mystery" },
  characters: [],
  series: { slug: "brand-stories-everyday-reversals-extra", episode: 2, chapter: 1 },
  music: { prompt: "light, curious, a little mysterious, no vocals", gain_db: -20, duck_db: -10 },
  loops,
  youtube: {
    category_id: 27,
    made_for_kids: false,
    default_language: "zh-TW",
    title: "招牌披薩重做後，達美樂的美國門市發生什麼事？｜品牌故事",
    description,
    tags: ["達美樂", "Domino's", "Domino's Pizza", "品牌故事", "披薩", "同店銷售", "企業故事", "2009"],
    video_id: null,
  },
  thumbnail: { template: "thumb", data: { headline: "**怎麼翻身**", tag: "品牌故事", brand: "達美樂", shot: "x02-b01-s04" } },
  sources,
  assets: [],
  scenes,
};
const videoBytes = JSON.stringify(doc, null, 2) + "\n";
writeFileSync(path.join(dir, "video.json"), videoBytes);
const sha256 = createHash("sha256").update(videoBytes).digest("hex");
const escapeTable = value => String(value).replaceAll("|", "\\|").replaceAll("\n", " ");
const sourceFor = number => number <= 9 ? "S09" : number <= 14 ? "S10Q1" : number <= 18 || number === 22 ? "S10" : "S11";
const matrix = [
  "# X02 達美樂｜逐句來源矩陣",
  "",
  "由 `drafts/part1.json`、`drafts/part2.json` 的 `claim_refs` 產生；主張原文與限制詳見 [source-notes.md](source-notes.md)。旁白以 `video.json` 為準。本表是作者對照，正式付費製作前須另由獨立代理查核。",
  "",
  `- \`video.json\` SHA-256：\`${sha256}\``,
  "- S09、S10Q1、S10、S11 對應 `video.json.sources` 的四份 SEC 申報；`#` 是 `source-notes.md` 的編號。",
  "- 結尾互動句屬編輯邀請，不主張歷史事實。",
  "",
  "| 句 ID | 旁白 | 來源主張 |",
  "| --- | --- | --- |",
  ...original.map(scene => {
    const refs = scene.claim_refs ?? [];
    const sourceRefs = refs.length ? refs.map(number => `${sourceFor(number)} #${number}`).join("、") : scene.lines[0].id === "x020101" ? "敘事示意" : "編輯邀請";
    return `| \`${scene.lines[0].id}\` | ${escapeTable(scene.lines[0].text)} | ${sourceRefs} |`;
  }),
  "",
].join("\n");
writeFileSync(path.join(dir, "source-matrix.md"), matrix);
console.log(JSON.stringify({ scenes: scenes.length, shots: scenes.filter(scene => scene.template === "shot").length, cards: scenes.filter(scene => scene.template !== "shot").length, narration_characters: scenes.reduce((sum, scene) => sum + scene.lines[0].text.length, 0), loops: loops.length, video_sha256: sha256 }, null, 2));
