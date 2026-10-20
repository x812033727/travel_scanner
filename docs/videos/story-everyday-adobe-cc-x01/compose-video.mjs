// Compose the reviewed Adobe X01 drafts into the local preview package.
// Run before media generation; changing video.json later invalidates media hashes.
import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { textHash } from "../../../tools/video/core/schema.mjs";

const dir = path.dirname(fileURLToPath(import.meta.url));
const slug = "story-everyday-adobe-cc-x01";
const read = name => JSON.parse(readFileSync(path.join(dir, name), "utf8"));
const drafts = [read("drafts/part1.json"), read("drafts/part2.json")];
const sceneWithSpeech = source => {
  const { claim_refs: unused, ...scene } = source;
  scene.lines = scene.lines.map(line => {
    if (!/[A-Za-z]/.test(line.text)) return line;
    const say = line.text
      .replaceAll("Creative ARR", "創意業務年化經常性收入")
      .replaceAll("Creative Cloud", "創意雲端服務")
      .replaceAll("Creative Suite", "創意軟體套裝")
      .replaceAll("Document Cloud", "文件雲端服務")
      .replaceAll("Photoshop", "修圖軟體")
      .replaceAll("CS6", "第六版創意套裝")
      .replaceAll("Adobe", "阿多比")
      .replaceAll("ARR", "年化經常性收入");
    return { ...line, say, say_for: textHash(line.text) };
  });
  return scene;
};
const original = drafts.flatMap(part => part.scenes);
const scenes = original.map(sceneWithSpeech);
const ids = new Map(scenes.flatMap((scene, index) => scene.lines.map(line => [line.id, index])));
const loop = (setup, payoff, what) => {
  if (ids.get(setup) === undefined || ids.get(payoff) === undefined || ids.get(setup) >= ids.get(payoff)) {
    throw new Error("Invalid story loop: " + setup + " → " + payoff);
  }
  return { setup, payoff, what };
};
const loops = [
  loop("x010105", "x010301", "2013 年新功能會移向哪種授權"),
  loop("x010106", "x010603", "2025 年全公司訂閱與產品收入的差距"),
  loop("x010107", "x010414", "訂閱數上升時營收與淨利承壓的原因"),
  loop("x010207", "x010212", "月費先付的金額與買斷有何差異"),
  loop("x010309", "x010413", "年報預告的轉型壓力怎樣顯在淨利"),
  loop("x010315", "x010402", "訂閱合約收入何時進入財報"),
  loop("x010404", "x010415", "2013 全公司營收實際降到哪裡"),
  loop("x010417", "x010501", "仍在販售的 CS6 後來供應到何時"),
  loop("x010507", "x010510", "2014 年訂閱收入有沒有超過產品收入"),
  loop("x010511", "x010514", "2015 年訂閱和產品收入差距是否拉開"),
  loop("x010521", "x010603", "2025 年全公司訂閱收入占比會有多高"),
];

const checkedOn = "2026-10-20";
const sources = [
  { title: "Adobe FY2012 Form 10-K", url: "https://www.sec.gov/Archives/edgar/data/796343/000079634313000008/adbe10kfy12.htm", checked_on: checkedOn },
  { title: "Adobe FY2013 Form 10-K", url: "https://www.sec.gov/Archives/edgar/data/796343/000079634314000004/adbe10kfy13.htm", checked_on: checkedOn },
  { title: "Adobe FY2015 Form 10-K", url: "https://www.sec.gov/Archives/edgar/data/796343/000079634316000224/adbe10kfy15.htm", checked_on: checkedOn },
  { title: "Adobe FY2025 Form 10-K", url: "https://www.sec.gov/Archives/edgar/data/796343/000079634326000003/adbe-20251128.htm", checked_on: checkedOn },
];
const description = [
  "2013 財年末，Creative Cloud 付費訂閱數從 30 萬升至 140 萬；同一年，Adobe 全公司營收比前一年少約 8%，淨利少 65%。這集沿著 Adobe 的 SEC 年報，拆解永久授權與訂閱的入帳節奏，以及 CS6 一般供應、2014 財年收入分類交叉與 2025 年的長期結果。",
  "",
  "片中訂閱數是財年末的付費訂閱份數，並非不同使用人數；收入比例是 Adobe 全公司分類，不是 Photoshop 或 Creative Cloud 的單品業績。插圖是敘事示意，並非真實人物、辦公室或軟體介面。資料查核日期：2026-10-20。",
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
    performance: "開場 2013 年三組相反數字逐項說清；財年末訂閱數、全年營收與淨利分開念；收入認列和成本分兩步交代；結尾親近自然。",
  },
  subtitles: { burn_in: false },
  look: { preset: "cute-mystery" },
  characters: [],
  series: { slug: "brand-stories-everyday-reversals-extra", episode: 1, chapter: 1 },
  music: { prompt: "light, curious, a little mysterious, no vocals", gain_db: -20, duck_db: -10 },
  loops,
  youtube: {
    category_id: 27,
    made_for_kids: false,
    default_language: "zh-TW",
    title: "訂閱數暴增，營收卻跌？Adobe 轉向 Creative Cloud 的那一年｜品牌故事",
    description,
    tags: ["Adobe", "Creative Cloud", "Photoshop", "品牌故事", "訂閱制", "CS6", "財報", "企業故事"],
    video_id: null,
  },
  thumbnail: { template: "thumb", data: { headline: "訂閱漲\n**營收跌**", tag: "品牌故事", brand: "Adobe", shot: "x01-b01-s04" } },
  sources,
  assets: [],
  scenes,
};
const videoBytes = JSON.stringify(doc, null, 2) + "\n";
writeFileSync(path.join(dir, "video.json"), videoBytes);
const sha256 = createHash("sha256").update(videoBytes).digest("hex");
const escapeTable = value => String(value).replaceAll("|", "\\|").replaceAll("\n", " ");
const sourceFor = number => number <= 14 ? "S12" : number <= 25 ? "S13" : number <= 30 || number === 35 ? "S15" : number <= 33 ? "S25" : "S26Q3";
const matrix = [
  "# X01 Adobe Creative Cloud｜逐句來源矩陣",
  "",
  "本矩陣由 `drafts/part1.json`、`drafts/part2.json` 的 `claim_refs` 產生；主張原文與限制詳見 [source-notes.md](source-notes.md)。旁白以 `video.json` 為準。此表是作者對照，仍需獨立查核。",
  "",
  "- `video.json` SHA-256：`" + sha256 + "`",
  "- S12、S13、S15、S25 對應 `video.json.sources` 的四份 SEC 10-K；S26Q3 僅供背景複核，沒有進入旁白。",
  "- `#` 是 `source-notes.md` 的編號；結尾互動句屬編輯邀請，不主張歷史事實。",
  "",
  "| 句 ID | 旁白 | 來源主張 |",
  "| --- | --- | --- |",
  ...original.map(scene => {
    const refs = scene.claim_refs ?? [];
    const sourceRefs = refs.length ? refs.map(number => sourceFor(number) + " #" + number).join("、") : "編輯邀請";
    return "| `" + scene.lines[0].id + "` | " + escapeTable(scene.lines[0].text) + " | " + sourceRefs + " |";
  }),
  "",
].join("\n");
writeFileSync(path.join(dir, "source-matrix.md"), matrix);
console.log(JSON.stringify({ scenes: scenes.length, shots: scenes.filter(scene => scene.template === "shot").length, cards: scenes.filter(scene => scene.template !== "shot").length, narration_characters: scenes.reduce((sum, scene) => sum + scene.lines[0].text.length, 0), loops: loops.length, video_sha256: sha256 }, null, 2));
