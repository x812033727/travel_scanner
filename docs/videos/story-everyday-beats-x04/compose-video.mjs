// Compose the source-bound X04 drafts into a reviewable local video package.
// Re-run after any draft edit; a changed video hash invalidates review receipts.
import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { textHash } from "../../../tools/video/core/schema.mjs";

const dir = path.dirname(fileURLToPath(import.meta.url));
const slug = "story-everyday-beats-x04";
const read = name => JSON.parse(readFileSync(path.join(dir, name), "utf8"));
const drafts = [read("drafts/part1.json"), read("drafts/part2.json")];
const original = drafts.flatMap(part => part.scenes);
const sceneWithSpeech = source => {
  const { claim_refs: unused, ...scene } = source;
  scene.lines = scene.lines.map(line => {
    if (!/[A-Za-z]/.test(line.text)) return line;
    const say = line.text
      .replaceAll("Beats Electronics", "比茲電子")
      .replaceAll("Beats Music", "比茲音樂")
      .replaceAll("Apple Music", "蘋果音樂")
      .replaceAll("iTunes Radio", "愛調電台")
      .replaceAll("iTunes Store", "愛調商店")
      .replaceAll("Beats", "比茲")
      .replaceAll("Apple", "蘋果")
      .replaceAll("iTunes", "愛調");
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

// Each pair describes a question the spoken story plants and later resolves.
const loops = [
  loop("x040102", "x040402", "價牌究竟是耳機價格還是兩家公司合計"),
  loop("x040103", "x040205", "收購前既有商店與免費電台能做什麼"),
  loop("x040104", "x040212", "數位音樂銷售下降可否視為收購原因"),
  loop("x040105", "x040304", "另一家被收購公司販售什麼"),
  loop("x040106", "x040509", "一年後電視盒子的音樂清單列出什麼新名字"),
  loop("x040107", "x040306", "另一家公司對既有音樂產品的補足關係"),
  loop("x040208", "x040306", "付費服務對既有音樂產品是什麼關係"),
  loop("x040214", "x040305", "兩份簽名文件分別對應哪種業務"),
  loop("x040313", "x040401", "總對價能否拆算成兩家公司買價"),
  loop("x040403", "x040412a", "附任職條件的股份能否直接加進耳機價格"),
  loop("x040404", "x040405", "會計附註最大的分配數字屬於何物"),
  loop("x040413", "x040502", "隔年產品段先出現哪一種音樂服務"),
  loop("x040511", "x040513", "合併收入欄能否反推單品表現"),
  loop("x040515", "x040603", "兩種商品線隔年是否仍各自列出"),
];

const checkedOn = "2026-10-20";
const sources = [
  { title: "Apple FY2013 Form 10-K", url: "https://www.sec.gov/Archives/edgar/data/320193/000119312513416534/d590790d10k.htm", checked_on: checkedOn },
  { title: "Apple 2014 Q3 Form 10-Q", url: "https://www.sec.gov/Archives/edgar/data/320193/000119312514277160/d740164d10q.htm", checked_on: checkedOn },
  { title: "Apple FY2014 Form 10-K", url: "https://www.sec.gov/Archives/edgar/data/320193/000119312514383437/d783162d10k.htm", checked_on: checkedOn },
  { title: "Apple FY2015 Form 10-K", url: "https://www.sec.gov/Archives/edgar/data/320193/000119312515356351/d17062d10k.htm", checked_on: checkedOn },
  { title: "Apple FY2016 Form 10-K", url: "https://www.sec.gov/Archives/edgar/data/320193/000162828016020309/a201610-k9242016.htm", checked_on: checkedOn },
];
const description = [
  "2014 年，Apple 已有 iTunes 商店和免費電台，卻同時買下 Beats 的音訊產品公司與付費音樂串流公司。這集沿著 Apple 2013–2016 年的 SEC 申報，拆解交易到底包含什麼、26 億美元會計對價如何記錄，以及隔年產品目錄裡兩條線各在哪裡。",
  "",
  "片中 26 億美元是兩家公司合計收購對價，不是耳機或單一服務的估價；年報也沒有披露 Apple Music 與 Beats Music 的技術繼承關係，或 Beats 單獨營收。插圖僅為無商標敘事示意，非真實產品、介面或人物。資料查核日期：2026-10-20。",
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
    provider: "gemini",
    name: "Sulafat",
    style: "標準國語，咬字清楚，台北人平常說話的語調。像跟朋友講一段有原件支持的品牌轉折；數字放慢，問句上揚，揭曉前停半拍。",
    performance: "兩家公司、五份申報與兩個不同的音樂服務名稱分開講；26 億是合計會計對價，不能念成耳機價；結尾親近自然。",
  },
  subtitles: { burn_in: false },
  look: { preset: "cute-mystery" },
  characters: [],
  series: { slug: "brand-stories-everyday-reversals-extra", episode: 4, chapter: 1 },
  music: { prompt: "light, curious, a little mysterious, no vocals", gain_db: -20, duck_db: -10 },
  loops,
  youtube: {
    category_id: 27,
    made_for_kids: false,
    default_language: "zh-TW",
    title: "蘋果買 Beats，為何連音樂訂閱也一起買？｜品牌故事",
    description,
    tags: ["Beats", "Apple", "Apple Music", "品牌故事", "耳機", "訂閱音樂", "企業故事", "2014"],
    video_id: null,
  },
  thumbnail: { template: "thumb", data: { headline: "**不只耳機**", tag: "品牌故事", brand: "BEATS", shot: "x04-b01-s04" } },
  sources,
  assets: [],
  scenes,
};
const videoBytes = JSON.stringify(doc, null, 2) + "\n";
writeFileSync(path.join(dir, "video.json"), videoBytes);
const sha256 = createHash("sha256").update(videoBytes).digest("hex");
const escapeTable = value => String(value).replaceAll("|", "\\|").replaceAll("\n", " ");
const sourceFor = number => number <= 3 ? "S13" : number <= 6 ? "S14Q" : number <= 14 ? "S14" : number <= 18 ? "S15" : "S16";
const matrix = [
  "# X04 Beats｜逐句來源矩陣",
  "",
  "由 `drafts/part1.json`、`drafts/part2.json` 的 `claim_refs` 產生；主張原文與限制詳見 [source-notes.md](source-notes.md)。旁白以 `video.json` 為準。本表是作者對照，正式付費製作前須另由獨立代理查核。",
  "",
  `- \`video.json\` SHA-256：\`${sha256}\``,
  "- S13、S14Q、S14、S15、S16 對應 `video.json.sources` 的五份 SEC 申報；`#` 是 `source-notes.md` 的編號。",
  "- 結尾互動句屬編輯邀請，不主張歷史事實。",
  "",
  "| 句 ID | 旁白 | 來源主張 |",
  "| --- | --- | --- |",
  ...original.map(scene => {
    const refs = scene.claim_refs ?? [];
    const sourceRefs = refs.length ? refs.map(number => `${sourceFor(number)} #${number}`).join("、") : "編輯邀請／示意場景";
    return `| \`${scene.lines[0].id}\` | ${escapeTable(scene.lines[0].text)} | ${sourceRefs} |`;
  }),
  "",
].join("\n");
writeFileSync(path.join(dir, "source-matrix.md"), matrix);
console.log(JSON.stringify({ scenes: scenes.length, shots: scenes.filter(scene => scene.template === "shot").length, cards: scenes.filter(scene => scene.template !== "shot").length, narration_characters: scenes.reduce((sum, scene) => sum + scene.lines[0].text.length, 0), loops: loops.length, video_sha256: sha256 }, null, 2));
