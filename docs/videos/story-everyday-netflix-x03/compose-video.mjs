// Compile the line-level draft into the non-paid X03 script and source matrix.
// This is a manuscript compiler; it does not invoke voice, image or music services.
import { createHash } from "node:crypto";
import { existsSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { textHash } from "../../../tools/video/core/schema.mjs";

const dir = path.dirname(fileURLToPath(import.meta.url));
const slug = "story-everyday-netflix-x03";
const rows = readFileSync(path.join(dir, "drafts/lines.txt"), "utf8").trim().split("\n");
const chapterNames = {
  1: "一張桌上的兩條路",
  2: "信封裡的訂閱機器",
  3: "先開一扇電腦上的門",
  4: "郵袋和播放鍵一起工作",
  5: "觀眾先換了看片方式",
  6: "最後一封信",
};
const sourceUrls = {
  N06: "https://www.sec.gov/Archives/edgar/data/1065280/000119312507042689/d10k.htm",
  N07: "https://www.sec.gov/Archives/edgar/data/1065280/000119312508040378/d10k.htm",
  N10: "https://www.sec.gov/Archives/edgar/data/1065280/000119312511040217/d10k.htm",
  N23: "https://www.sec.gov/Archives/edgar/data/1065280/000106528024000030/nflx-20231231.htm",
};
const checkedOn = "2026-10-20";
// Keep the channel's cute-mystery palette while preventing the image model from
// turning DVDs, mailers and screens into unrequested chibi mascots.
const lookStyle = "cute Taiwanese YouTube explainer cartoon, 2D flat-colour cel shading, thick clean dark outlines, a limited palette of deep navy night, parchment yellow, muted teal and one warning-red accent, subtle paper grain, simple clear backgrounds, one focal subject in the centre third, playful and friendly, 16:9. Human figures only when specifically requested: draw them as chibi with big round heads, large expressive eyes and comic expressions. In object-only shots, render everyday items as inert objects with no faces, eyes, mouths, limbs, mascot features or extra people.";
const sources = Object.entries(sourceUrls).map(([code, url]) => ({ title: `Netflix ${code.slice(1)} Form 10-K`, url, checked_on: checkedOn }));
const raw = rows.filter(row => row && !row.startsWith("#")).map((row, index) => {
  const fields = row.split("|");
  if (fields.length !== 5) throw new Error(`draft row ${index + 1}: expected five pipe-separated fields`);
  const [chapter, id, text, refs, visual] = fields.map(value => value.trim());
  if (!chapterNames[chapter] || !/^nx\d{4}$/.test(id) || !text || !visual) throw new Error(`draft row ${index + 1}: malformed content`);
  const claim_refs = refs === "-" ? [] : refs.split(",").map(value => value.trim());
  for (const ref of claim_refs) if (!/^(N06|N07|N10|N23)#\d+$/.test(ref)) throw new Error(`draft row ${index + 1}: invalid source reference ${ref}`);
  return { chapter: Number(chapter), id, text, claim_refs, visual };
});
const seen = new Set();
for (const row of raw) {
  if (seen.has(row.id)) throw new Error(`duplicate line ${row.id}`);
  seen.add(row.id);
}
const seenChapter = new Set();
const scenes = [];
const cameras = ["slow push in", "drift", "pan left", "tilt down", "pull out", "pan right"];
let shotIndex = 0;
for (const row of raw) {
  const line = { id: row.id, text: row.text };
  if (row.text.includes("Netflix") || row.text.includes("DVD")) {
    line.say = row.text.replaceAll("Netflix", "網飛").replaceAll("DVD", "ＤＶＤ");
    line.say_for = textHash(row.text);
  }
  if (row.visual.startsWith("OUTRO:")) {
    const last = scenes.at(-1);
    if (last?.template === "outro") {
      last.lines.push(line);
      continue;
    }
    scenes.push({ id: "outro", template: "outro", data: { title: row.visual.slice(6), cta: "訂閱品牌故事", lines: ["兩條路，一門生意"] }, lines: [line] });
    continue;
  }
  let template = "shot";
  let data = { prompt: row.visual, camera: cameras[shotIndex++ % cameras.length], visual: "still" };
  if (row.visual.startsWith("CARD:")) {
    template = "big";
    const [cardText, kicker] = row.visual.slice(5).split("~");
    data = { text: cardText, kicker: kicker || "Netflix 年報" };
  }
  const scene = { id: `scene-${row.id}` };
  if (!seenChapter.has(row.chapter)) {
    scene.chapter = chapterNames[row.chapter];
    seenChapter.add(row.chapter);
  }
  Object.assign(scene, { template, data, lines: [line] });
  scenes.push(scene);
}
const position = new Map(raw.map((row, index) => [row.id, index]));
const loop = (setup, payoff, what) => {
  if (position.get(setup) === undefined || position.get(payoff) === undefined || position.get(setup) >= position.get(payoff)) throw new Error(`invalid loop ${setup} → ${payoff}`);
  return { setup, payoff, what };
};
const loops = [
  loop("nx0104", "nx0318", "寄片仍增時為何增加電腦即看"),
  loop("nx0105", "nx0502", "多數訂戶何時轉向串流觀看"),
  loop("nx0106", "nx0604", "寄片服務實際何時停止"),
  loop("nx0208", "nx0209", "退片之後下一片如何到手"),
  loop("nx0216", "nx0302", "雙軌策略怎樣寫進公司年報"),
  loop("nx0305", "nx0310", "上線時如何逐步向訂戶開放"),
  loop("nx0316", "nx0401", "寄送總量增加時人均月租片數如何變化"),
  loop("nx0407", "nx0408", "平均租片下降是否全因串流"),
  loop("nx0414", "nx0415", "電腦以外的平台當時如何規劃"),
  loop("nx0508", "nx0517", "2010 年寄片總數是否立即下降"),
];
const description = [
  "2007 年一月，Netflix 新增電腦即看；同一年寄給付費訂戶的 DVD 總片數比前一年多 20%。這集沿著四份 SEC 年報，跟著一個訂戶的排片隊列，追問寄片仍成長時為何開出第二條交付路徑，以及這兩條路何時真正分開。",
  "",
  "片中 20% 是 2007 相對 2006 全年的 DVD 寄出總量；2010 年『多數訂戶』說的是每位訂戶各自的觀看方式，不是營收。場景插圖是敘事示意，不是真實影像或軟體畫面。資料核對日期：2026-10-20。",
  "",
  "SEC 原始申報：",
  ...sources.flatMap(source => [source.title, source.url]),
].join("\n");
const doc = {
  schema_version: 1,
  slug,
  format: "drama",
  category: "explainer",
  narration_locale: "zh-TW",
  target_minutes: [9, 11],
  voice: { provider: "gemini", name: "Sulafat", style: "標準國語，咬字清楚，台北人平常說話的語調。像跟朋友說一段有原件支持的品牌故事；數字放慢，問句上揚，揭曉前停半拍。" },
  subtitles: { burn_in: false },
  look: { preset: "cute-mystery", style: lookStyle },
  characters: [],
  series: { slug: "brand-stories-everyday-reversals-extra", episode: 3, chapter: 1 },
  music: { prompt: "light, curious, a little mysterious, no vocals", gain_db: -20, duck_db: -10 },
  loops,
  youtube: { category_id: 27, made_for_kids: false, default_language: "zh-TW", title: "DVD 寄出片數還多了 20%，Netflix 為何先開立即觀看？｜品牌故事", description, tags: ["Netflix", "DVD", "串流", "品牌故事", "企業故事", "影劇訂閱", "年報"], video_id: null },
  thumbnail: { template: "thumb", data: { headline: "寄片增\n**先即看**", tag: "品牌故事", brand: "NETFLIX", shot: "scene-nx0103" } },
  sources,
  assets: [],
  scenes,
};
const video = `${JSON.stringify(doc, null, 2)}\n`;
writeFileSync(path.join(dir, "video.json"), video);
const sha = createHash("sha256").update(video).digest("hex");
const reviewCandidates = [
  ["reviews/source-review-visual-revision.md", "畫面提示詞修訂來源審查"],
  ["reviews/source-review-audio-revision.md", "音訊修訂稿來源審查"],
  ["reviews/source-review-release.md", "發布版來源審查"],
];
const currentReview = reviewCandidates.find(([name]) => {
  const file = path.join(dir, name);
  return existsSync(file) && readFileSync(file, "utf8").includes(sha);
});
const reviewStatus = currentReview
  ? `現行稿的獨立複核見 [${currentReview[1]}](${currentReview[0]})。`
  : "來源對照仍須獨立審查。";
const table = value => String(value).replaceAll("|", "\\|").replaceAll("\n", " ");
const matrix = [
  "# X03 Netflix｜逐句來源矩陣", "",
  `本表由 \`drafts/lines.txt\` 編譯，\`video.json\` 是可供工具讀取的逐句稿。SEC 引文與口徑詳見 [source-notes.md](source-notes.md)；${reviewStatus}`, "",
  `- \`video.json\` SHA-256：\`${sha}\``,
  "- `N06`、`N07`、`N10`、`N23` 對應 `video.json.sources` 的四份原始 10-K；`#` 是 `source-notes.md` 的條目。",
  "- `—` 表示示意動作、銜接問句或編輯邀請，沒有新增外部史實；旁白不能把畫面當紀錄片影像。",
  "", "| 句 ID | 旁白 | 原件條目 |", "| --- | --- | --- |",
  ...raw.map(row => `| \`${row.id}\` | ${table(row.text)} | ${row.claim_refs.join("、") || "—"} |`), "",
].join("\n");
writeFileSync(path.join(dir, "source-matrix.md"), matrix);
const stats = { lines: raw.length, shots: scenes.filter(scene => scene.template === "shot").length, cards: scenes.filter(scene => scene.template !== "shot").length, characters: raw.reduce((sum, row) => sum + row.text.length, 0), loops: loops.length, sha256: sha };
console.log(JSON.stringify(stats, null, 2));
