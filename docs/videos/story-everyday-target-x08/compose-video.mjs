// Deterministic, offline X08 preproduction build. It neither calls media providers nor imports a story.
import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { textHash } from "../../../tools/video/core/schema.mjs";
import { visualFor } from "./drafts/visual-cues.mjs";

const dir = path.dirname(fileURLToPath(import.meta.url));
const checkedOn = "2026-10-20";
const slug = "story-everyday-target-x08";
const sources = [
  { title: "Target FY2012 Form 10-K", url: "https://www.sec.gov/Archives/edgar/data/27419/000104746913003100/a2213506z10-k.htm", checked_on: checkedOn },
  { title: "Target FY2013 Form 10-K", url: "https://www.sec.gov/Archives/edgar/data/27419/000002741914000014/tgt-20140201x10k.htm", checked_on: checkedOn },
  { title: "Target FY2014 Q1 original results", url: "https://www.sec.gov/Archives/edgar/data/27419/000002741914000018/a2014q1ex-99.htm", checked_on: checkedOn },
  { title: "Target FY2014 Q2 original results", url: "https://www.sec.gov/Archives/edgar/data/27419/000002741914000025/a2014q2ex-99.htm", checked_on: checkedOn },
  { title: "Target FY2014 Q3 original results", url: "https://www.sec.gov/Archives/edgar/data/27419/000002741914000033/a2014q3ex-99.htm", checked_on: checkedOn },
  { title: "Target 2015-01-15 original exit announcement", url: "https://www.sec.gov/Archives/edgar/data/27419/000002741915000005/exhibit99atargetcorporatio.htm", checked_on: checkedOn },
  { title: "Target FY2014 Form 10-K", url: "https://www.sec.gov/Archives/edgar/data/27419/000002741915000012/tgt-20150131x10k.htm", checked_on: checkedOn },
  { title: "Target FY2015 Q1 Form 10-Q", url: "https://www.sec.gov/Archives/edgar/data/27419/000002741915000018/tgt-20150502x10xq.htm", checked_on: checkedOn },
];

function readChapters() {
  const markdown = readFileSync(path.join(dir, "drafts/narration.md"), "utf8");
  const chapters = [];
  for (const raw of markdown.split(/\r?\n/)) {
    const chapter = raw.match(/^## 第[一二三四五六]章｜(.+)$/);
    if (chapter) { chapters.push({ title: chapter[1].replace(/（濃縮開場.*$/, ""), rows: [] }); continue; }
    if (raw.startsWith("## 來源標記")) break;
    const row = raw.match(/^(.*?)\s+\[((?:TC\d+[A-Z]?|editorial)(?:\s*,\s*TC\d+[A-Z]?)*)\]\s*$/);
    if (!row) continue;
    if (!chapters.length) throw new Error(`Narration before first chapter: ${raw}`);
    const refs = row[2].split(/\s*,\s*/).filter(ref => ref !== "editorial");
    chapters.at(-1).rows.push({ text: row[1].trim(), refs });
  }
  if (chapters.length !== 6 || chapters.some(chapter => !chapter.rows.length)) throw new Error("Expected six nonempty chapters");
  return chapters;
}

const cardRules = [
  [/一百三十三間店/, ["2015-01-15｜當時加拿大", "133", "當時的加拿大門市", "Target 2015-01-15 公告"]],
  [/一百八十九個據點/, ["2011｜租賃權益", "189", "Zellers 據點租賃權，不是已開店數", "Target FY2013 10-K，Note 7"]],
  [/一千四百二十萬平方英尺/, ["FY2013｜124 間已開門市", "14.2m sq ft", "合計零售面積；非逐店平均", "Target FY2013 10-K，Canadian Segment"]],
  [/一百二十四間店開業/, ["FY2013｜分批開店", "124", "實際開設門市", "Target FY2013 10-K，MD&A"]],
  [/百分之十四點九/, ["FY2013｜加拿大部門", "14.9%", "毛利率；原因待揭曉", "Target FY2013 10-K，Canadian Segment"]],
  [/一點九六億美元/, ["FY2013｜加拿大部門", "US$196m", "當年商品毛利", "Target FY2014 10-K，Note 6"]],
  [/百分之十八點七/, ["FY2014 Q1｜加拿大部門", "18.7%", "加拿大部門季度毛利率", "Target FY2014 Q1 原始業績公告"]],
  [/下降百分之十一點四/, ["FY2014 Q2｜同店銷售", "−11.4%", "僅 48 間成熟門市", "Target FY2014 Q2 原始業績公告"]],
  [/增加百分之一點六/, ["FY2014 Q3｜同店銷售", "+1.6%", "涵蓋 82 間成熟門市", "Target FY2014 Q3 原始業績公告"]],
  [/二點一一億美元/, ["FY2014 Q3｜加拿大部門", "−US$211m", "當季 EBIT；不是全年虧損", "Target FY2014 Q3 原始業績公告"]],
  [/十九點零二億美元/, ["FY2014｜加拿大", "US$1.902b", "全年銷售；前一年為部分年度", "Target FY2014 10-K，Note 6"]],
  [/八點六九億美元/, ["FY2014｜加拿大", "−US$869m", "稅前營運虧損；非退出費用", "Target FY2014 10-K，Note 6"]],
  [/至少二〇二一年/, ["2015-01-15｜管理層當時判斷", "2021", "至少此前沒有可信獲利情境", "Target 2015-01-15 公告"]],
  [/五月二日/, ["截至 2015-05-02", "全數關閉", "加拿大門市", "Target FY2015 Q1 10-Q，Note 2"]],
  [/五十一點零五億美元/, ["FY2014 Q4｜加拿大退出", "US$5.105b", "稅前退出費用；性質待揭曉", "Target FY2014 10-K，Note 6"]],
  [/四十七點六六億美元/, ["FY2014 Q4｜退出費用之中", "US$4.766b", "非現金投資減損", "Target FY2014 10-K，Note 6"]],
];
const cardFor = (value, refs) => {
  if (/二點一一億美元/.test(value) && (refs.includes("TC11A") || refs.includes("TC25"))) {
    return { title: "FY2014 Q1｜加拿大部門", stats: [{ value: "−US$211m", label: "當季 EBIT；非公司整體" }], source: "Target FY2014 Q1 原始業績公告" };
  }
  const found = cardRules.find(([pattern]) => pattern.test(value));
  if (!found) return null;
  const [title, amount, label, source] = found[1];
  return { title, stats: [{ value: amount, label }], source };
};

const pronunciation = [["Target Canada", "塔吉特加拿大"], ["Brian Cornell", "布萊恩康奈爾"], ["John Mulligan", "約翰穆利根"], ["Zellers", "澤勒斯"], ["Target", "塔吉特"], ["Cornell", "康奈爾"]];
const lineFor = (id, value) => {
  const line = { id, text: value, emotion: value.endsWith("？") ? "自然提問，尾音微上揚" : "台灣口語說書，數字清楚，正常語速" };
  const say = pronunciation.reduce((text, [word, spoken]) => text.replaceAll(word, spoken), value);
  if (say !== value) Object.assign(line, { say, say_for: textHash(value) });
  return line;
};
const chapters = readChapters();
// Preserve original line IDs when passages are inserted or cut; the later
// closure evidence keeps its Chapter 5 source IDs after the exit charge.
const chapter3InsertAt = 15;
const chapter3Added = 2;
const chapter4InsertAt = 9;
const chapter4Added = 2;
function identityFor(ci, ri) {
  if (ci === 2 && ri >= chapter3InsertAt && ri < chapter3InsertAt + chapter3Added) {
    const added = String(ri - chapter3InsertAt + 1).padStart(2, "0");
    return { line: `x0803a${added}`, scene: `x08-b03-a${added}`, visualIndex: 100 + ri - chapter3InsertAt };
  }
  if (ci === 3 && ri >= chapter4InsertAt && ri < chapter4InsertAt + chapter4Added) {
    const added = String(ri - chapter4InsertAt + 1).padStart(2, "0");
    return { line: `x0804a${added}`, scene: `x08-b04-a${added}`, visualIndex: 100 + ri - chapter4InsertAt };
  }
  if (ci === 3 && ri === 22) return { line: "x0804a03", scene: "x08-b04-a03", visualIndex: 102 };
  if (ci === 3 && ri === 30) return { line: "x0804a04", scene: "x08-b04-a04", visualIndex: 103 };
  if (ci === 4 && ri >= 4 && ri <= 6) {
    const added = String(ri - 3).padStart(2, "0");
    return { line: `x0805a${added}`, scene: `x08-b05-a${added}`, visualIndex: 100 + ri - 4 };
  }
  if (ci === 4 && ri === 10) return { line: "x0805a04", scene: "x08-b05-a04", visualIndex: 103 };
  if (ci === 4 && ri === 13) return { line: "x080512", scene: "x08-b05-s12", visualIndex: 11 };
  if (ci === 5 && ri === 9) return { line: "x080510", scene: "x08-b05-s10", visualIndex: 9 };
  if (ci === 5 && ri === 10) return { line: "x080511", scene: "x08-b05-s11", visualIndex: 10 };
  const originalRi = ci === 1 && ri >= 12 ? ri + 3
    : ci === 2 && ri >= chapter3InsertAt + chapter3Added ? ri - chapter3Added + 1
    : ci === 3 && ri >= 31 ? ri - 4
      : ci === 3 && ri >= 23 ? ri - 3
        : ci === 3 && ri >= chapter4InsertAt + chapter4Added ? ri - chapter4Added
      : ci === 4 && ri >= 7 && ri <= 9 ? ri - 3
        : ci === 4 && ri >= 11 && ri <= 12 ? ri - 4
      : ci === 5 && ri >= 11 ? ri + 3 : ri;
  const suffix = `${String(ci + 1).padStart(2, "0")}${String(originalRi + 1).padStart(2, "0")}`;
  return { line: `x08${suffix}`, scene: `x08-b${String(ci + 1).padStart(2, "0")}-s${String(originalRi + 1).padStart(2, "0")}`, visualIndex: originalRi };
}
const authored = chapters.flatMap((chapter, ci) => chapter.rows.map((row, ri) => {
  const identity = identityFor(ci, ri);
  const line = lineFor(identity.line, row.text);
  const card = ci === chapters.length - 1 && ri >= chapter.rows.length - 3 ? null : cardFor(row.text, row.refs);
  const scene = {
    id: identity.scene,
    template: card ? "stats" : "shot",
    data: card ?? { ...visualFor(row.text, ci, identity.visualIndex), visual: "still" },
    lines: [line],
    claim_refs: row.refs,
  };
  if (ri === 0) scene.chapter = chapter.title;
  return scene;
}));
// Hold one coherent action across adjacent short lines when a cut would run below five seconds.
for (const [firstId, secondId] of [
  ["x08-b02-s18", "x08-b02-s19"],
  ["x08-b03-s13", "x08-b03-s14"],
  ["x08-b04-s35", "x08-b04-s36"],
]) {
  const index = authored.findIndex(scene => scene.id === firstId);
  if (index < 0 || authored[index + 1]?.id !== secondId || authored[index].template !== "shot" || authored[index + 1].template !== "shot") {
    throw new Error(`Invalid adjacent shot merge ${firstId} / ${secondId}`);
  }
  authored[index].lines.push(...authored[index + 1].lines);
  authored.splice(index + 1, 1);
}
const closing = authored.splice(-3, 3);
if (closing.some(scene => scene.template === "stats")) throw new Error("Closing three sentences must not be stats cards");
authored.push({ id: "x08-outro", template: "outro", data: { title: "為何 133 店仍撤退？", cta: "訂閱品牌故事" }, lines: closing.flatMap(scene => scene.lines) });
const scenes = authored.map(({ claim_refs: _refs, ...scene }) => scene);
const originalRows = chapters.flatMap((chapter, ci) => chapter.rows.map((row, ri) => ({ ...row, id: identityFor(ci, ri).line, chapter: ci + 1 })));
const findId = (pattern) => {
  const found = originalRows.find(row => pattern.test(row.text));
  if (!found) throw new Error(`Missing loop anchor ${pattern}`);
  return found.id;
};
const anchors = [
  [/門市沒有立刻拉下鐵門/, /截至五月二日/, "公告日仍開的門何時關上"],
  [/一百三十三間店/, /找不到二〇二一年以前/, "店數多為何仍退出"],
  [/幾年前買下的那批租賃權/, /買下 Zellers/, "店網背後的租賃權"],
  [/首批店的毛利/, /百分之十四點九/, "首季毛利能否維持"],
  [/用年底購物季測試/, /購物季沒有出現/, "年底購物季會否帶來轉折"],
  [/第一批 Target 門市，何時迎來顧客/, /前二十四間店終於開張/, "加拿大首批 Target 門市何時迎來顧客"],
  [/收入能趕上嗎/, /銷售十三點一七億美元/, "首年銷售能否跟上展店"],
  [/漂亮的首季比率/, /毛利率只剩百分之十四點九/, "首季比率與全年結果"],
  [/明年銷售若增加/, /前一年毛利比這項費用少/, "次年商品毛利能否追上銷售管理費"],
  [/下一年，這批店會先出現改善嗎/, /初步改善跡象/, "次年改善跡象"],
  [/樣本擴大後，同店銷售會怎樣/, /同店銷售增加百分之一點六/, "樣本擴大後的季度同店比較"],
  [/改掉更大的虧損嗎/, /全年稅前營運仍虧/, "同店回升是否讓公司轉盈"],
  [/董事會會繼續等嗎/, /董事會在一月十四日/, "管理層如何處置虧損"],
  [/先在財報留下多少費用/, /退出費用，稅前共/, "一月退出決定後列出的費用"],
  [/為什麼要減到幾乎是零/, /股權價值因此接近零/, "非現金減損的原因"],
];
const loops = anchors.map(([setup, payoff, what]) => {
  const a = findId(setup); const b = findId(payoff);
  if (originalRows.findIndex(row => row.id === a) >= originalRows.findIndex(row => row.id === b)) throw new Error(`Backward loop: ${what}`);
  return { setup: a, payoff: b, what };
});

const description = [
  "Target 在 2013 財年分批開出 124 間加拿大門市，到 2015 年 1 月宣布退出時共有 133 店。為什麼擴店與銷售增加仍不足以留下？本集以 Target 當時及後續 SEC 申報，追租賃權交易、開店、庫存清理、財報、管理層判斷與其後實際關店。",
  "",
  "2015-01-15 是退出公告及加拿大子公司申請 CCAA 的日期；公告明說門市清算期間仍開放。FY2015 Q1 季報只證實截至 2015-05-02 全店已關，未載最後一店確切日期。FY2013 加拿大部門毛利率 14.9%，Target 歸因於銷售低於預期後清理過剩庫存和供應鏈啟動挑戰；不以空架傳聞代替報表。FY2014 稅前退出費用 US$5.105b，其中 US$4.766b 是非現金投資減損，不等於全額現金流出。2014 Q2 與 Q3 的同店數字涵蓋不同成熟店樣本。插畫為匿名概念示意，非真實店面、人物或申報文件影像。資料查核日期：2026-10-20。",
  "",
  "一手資料（SEC 原始申報及公司附件）",
  ...sources.flatMap(source => [source.title, source.url]),
].join("\n");
const video = {
  schema_version: 1,
  slug,
  format: "drama",
  category: "explainer",
  narration_locale: "zh-TW",
  target_minutes: [8, 11],
  voice: { provider: "gemini", name: "Sulafat", style: "標準國語，台灣自然口音。像對朋友講一個零售品牌的真實轉折；數字咬清楚，問題前停半拍，不靠慢速撐長度。", performance: "2015 年一月宣布、五月前全關；加拿大部門數字、FY2014 稅前營運虧損與非現金退出減損分開讀。" },
  subtitles: { burn_in: false },
  look: { preset: "cute-mystery" },
  characters: [],
  series: { slug: "brand-stories-everyday-reversals-extra", episode: 8, chapter: 1 },
  music: { prompt: "light, curious, a little mysterious, no vocals", gain_db: -20, duck_db: -10 },
  loops,
  youtube: { category_id: 27, made_for_kids: false, default_language: "zh-TW", title: "Target 在加拿大開了 133 家店，為何兩年就撤退？｜品牌故事", description, tags: ["Target", "加拿大", "品牌故事", "零售", "商業史", "企業策略"], video_id: null },
  thumbnail: { template: "thumb", data: { headline: "**全撤？**", tag: "品牌故事", brand: "Target", shot: "x08-b01-s03" } },
  sources,
  assets: [],
  scenes,
};
const bytes = JSON.stringify(video, null, 2) + "\n";
writeFileSync(path.join(dir, "video.json"), bytes);
const sha256 = createHash("sha256").update(bytes).digest("hex");
const esc = text => text.replaceAll("|", "\\|");
writeFileSync(path.join(dir, "line-source-matrix.md"), [
  "# X08 Target Canada｜逐句來源矩陣", "",
  "由 `compose-video.mjs` 從 `drafts/narration.md` 生成，主張 ID 詳見 [source-matrix.md](source-matrix.md)。每次改稿必須重編、重新查核。", "",
  `- \`video.json\` SHA-256：\`${sha256}\``, "",
  "| 句 ID | 旁白 | 主張 |", "| --- | --- | --- |",
  ...originalRows.map(row => `| \`${row.id}\` | ${esc(row.text)} | ${row.refs.length ? row.refs.join("、") : "編輯問句／CTA"} |`), "",
].join("\n"));
writeFileSync(path.join(dir, "script.md"), [
  "# X08 Target Canada｜繁中逐句稿", "", `候選前製；\`video.json\` SHA-256：\`${sha256}\`。片頭與片尾不計入實質正文；本版的實際 TTS 秒數與驗收見 [media-production.md](reviews/media-production.md)。`, "",
  ...chapters.flatMap((chapter, ci) => [`## 第 ${ci + 1} 章｜${chapter.title}${ci === 0 ? "（濃縮開場）" : ""}`, "", ...chapter.rows.map((row, ri) => `- \`${identityFor(ci, ri).line}\` ${row.text}`), ""]),
].join("\n"));
writeFileSync(path.join(dir, "series.json"), JSON.stringify({ kind: "story", slug: "brand-stories-everyday-reversals-extra", episode: 8, chapter: 1, title: "Target：加拿大 133 店仍撤退？", logline: "從 2011 年租賃權、2013 年密集開店到 2015 年決定退出；店數與銷售增加之後，獲利時間為何仍不可接受。", names: ["Target", "Target Canada", "Zellers", "Brian Cornell", "Cornell"], characters: [], target_minutes: 10, image_model: "image-01", style_preset: "custom", look: { preset: "cute-mystery" }, visual_tier: "stills", compilation: false }, null, 2) + "\n");
const bodyText = chapters.slice(1).flatMap(chapter => chapter.rows).slice(0, -3).map(row => row.text).join("");
console.log(JSON.stringify({ scenes: scenes.length, shots: scenes.filter(scene => scene.template === "shot").length, cards: scenes.filter(scene => scene.template === "stats").length, spoken_lines: originalRows.length, hook_characters: chapters[0].rows.map(row => row.text).join("").length, body_characters: bodyText.length, body_estimate_minutes_at_250_cpm: +(bodyText.length / 250).toFixed(2), body_estimate_minutes_at_300_cpm: +(bodyText.length / 300).toFixed(2), loops: loops.length, video_sha256: sha256 }, null, 2));
