// Rebuild the approved C20 short version without changing the historical 42-line project.
// No network or paid media calls. Run `node build.mjs --check` before using the result.
import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const parent = path.resolve(here, "../story-everyday-zippo-c20/reviews");
const inputs = {
  script: ["v8-short-script-candidate-20261024.md", "8bf33f7f733d5acb8c7ac64186b5932c43e6bb06867a6ffbf2ecc6bf0e68d82d"],
  plain: ["v8-short-blind-plain-20261024.txt", "358000a1eba0def8d2c3fbe0c7ddb8276bbacab74f82c534750bbbeac40814e5"],
  visual: ["v8-short-visual-plan-candidate-20261024.json", "d30cbe9f9e92bf8339d82671879ef465538d1691885b5161ca85d7e10d571419"],
};
const sha256 = (bytes) => createHash("sha256").update(bytes).digest("hex");
function locked(key) {
  const [name, expected] = inputs[key];
  const bytes = readFileSync(path.join(parent, name));
  const actual = sha256(bytes);
  if (actual !== expected) throw new Error(`${key} changed: ${actual}; expected ${expected}`);
  return bytes.toString("utf8");
}

const sourceScript = locked("script");
const plain = locked("plain");
const visual = JSON.parse(locked("visual"));
const scriptRows = [...sourceScript.matchAll(/^\|\s*(c20\d{4})\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*$/gm)]
  .map((match) => ({ id: match[1], narration: match[2].trim(), source_tags: match[3].trim() }));
const plainRows = plain.trimEnd().split(/\r?\n/).map((row) => {
  const [id, narration, ...extra] = row.split("\t");
  if (extra.length || !id || !narration) throw new Error(`invalid plain row: ${row}`);
  return { id, narration };
});
if (scriptRows.length !== 36 || plainRows.length !== 36 || visual.shots.length !== 36) throw new Error("v8 needs exactly 36 approved rows");
if (visual.shot_count !== 33 || visual.card_count !== 3 || visual.image_model !== "MiniMax image-01" || JSON.stringify(visual.look) !== JSON.stringify({ preset: "cute-mystery" })) throw new Error("v8 visual contract changed");
const chapterNames = {
  hook: "維修桌上的舊盒究竟保住什麼",
  origin: "單手小盒附上免費修的承諾",
  idea: "專利圖把外殼與內部機件分開",
  engine: "英國維修把外殼與內膽分開處理",
  turn: "美國保證畫出機械與外觀的界線",
  now: "那只舊盒最後保住什麼",
};
const sourceNames = {
  c200207: "Zippo 公司史（後來回顧）",
  c200302: "美國專利 US 2,032,695",
  c200511: "Zippo 美國現行保證說明",
};
const camera = ["push in", "pan left", "pull out"];
let lastChapter = "";
let still = 0;
let card = 0;
const scenes = visual.shots.map((shot, index) => {
  const row = scriptRows[index];
  const projected = plainRows[index];
  if (shot.line_id !== row.id || shot.line_id !== projected.id || shot.narration !== row.narration || row.narration !== projected.narration || shot.source_tags !== row.source_tags) {
    throw new Error(`approved script/plain/visual mismatch at ${shot.line_id}`);
  }
  if (!(shot.chapter in chapterNames)) throw new Error(`unknown chapter ${shot.chapter}`);
  const first = shot.chapter !== lastChapter;
  lastChapter = shot.chapter;
  const scene = {
    id: `c20-sc-${shot.line_id.slice(3)}`,
    ...(first ? { chapter: chapterNames[shot.chapter] } : {}),
    template: shot.kind === "shot" ? "shot" : "big",
    data: shot.kind === "shot"
      ? { prompt: shot.prompt, camera: camera[index % camera.length], visual: "still" }
      : { text: shot.card_text },
    claims: [shot.line_id],
    lines: [{
      id: shot.line_id,
      text: row.narration,
      emotion: "克制的台灣說書；年份、地區與保修範圍放慢，章末問句留半拍",
      ...(shot.line_id === "c200102" ? {
        // Zippo's own Chinese site uses 之宝 as a name; the approved caption remains Zippo.
        say: row.narration.replace("Zippo", "之寶"),
        say_for: createHash("sha256").update(row.narration.normalize("NFC"), "utf8").digest("hex").slice(0, 12),
      } : {}),
    }],
  };
  if (shot.kind === "shot") {
    still += 1;
    if (!shot.prompt || shot.card_text) throw new Error(`invalid still ${shot.line_id}`);
  } else if (shot.kind === "card") {
    card += 1;
    if (!shot.card_text || shot.prompt || !sourceNames[shot.line_id]) throw new Error(`invalid card ${shot.line_id}`);
  } else throw new Error(`invalid kind ${shot.line_id}`);
  return scene;
});
if (still !== 33 || card !== 3 || scenes.filter((scene) => scene.chapter).length !== 6) throw new Error("C20 scene counts changed");

const sources = [
  { title: "Zippo 公司史（1930 年代，公司事後回顧）", url: "https://kb.zippo.com/the-history-of-zippo", checked_on: "2026-10-24" },
  { title: "美國專利 US 2,032,695 原始掃描", url: "https://patentimages.storage.googleapis.com/c6/09/ea/1d1b14be9be79c/US2032695.pdf", checked_on: "2026-10-24" },
  { title: "Zippo 美國 Warranty & Repair", url: "https://kb.zippo.com/warranty-repair", checked_on: "2026-10-24" },
  { title: "Zippo 美國未點火問答", url: "https://kb.zippo.com/zippo-lighter/not-lighting", checked_on: "2026-10-24" },
  { title: "Zippo 美國斷鉸鏈問答", url: "https://kb.zippo.com/zippo-lighter/hinge-broke", checked_on: "2026-10-24" },
  { title: "Zippo 美國外觀磨損問答", url: "https://kb.zippo.com/zippo-lighter/worn-deco", checked_on: "2026-10-24" },
  { title: "Zippo 英國防風款維修說明", url: "https://www.zippo.co.uk/pages/zippo-repairs-windproof-lighter", checked_on: "2026-10-24" },
];
const video = {
  schema_version: 1,
  slug: "story-everyday-zippo-c20-short-v8",
  format: "drama",
  category: "explainer",
  narration_locale: "zh-TW",
  target_minutes: [5, 7],
  voice: { provider: "gemini", name: "Sulafat", style: "標準國語，台北日常語調。克制、好奇地講維修桌上的物件；年份、地區與條款界線放慢，不作吸菸或點火示範。" },
  subtitles: { burn_in: false },
  look: { preset: "cute-mystery" },
  characters: [],
  series: { slug: "brand-stories-everyday-reversals", episode: 20, chapter: 1 },
  music: { prompt: "light, curious, a little mysterious, no vocals", gain_db: -20, duck_db: -10 },
  loops: [
    { setup: "c200105", payoff: "c200504", what: "英國換內膽後舊件是否寄回" },
    { setup: "c200105", payoff: "c200510", what: "美國會否修斷掉的鉸鏈" },
    { setup: "c200105", payoff: "c200511", what: "美國會否保外觀塗裝磨損" },
    { setup: "c200107", payoff: "c200608", what: "終身免費修保住哪一種價值" },
    { setup: "c200209", payoff: "c200303", what: "內外兩層是如何分開的" },
    { setup: "c200213", payoff: "c200303", what: "正式申請畫出的內外套合" },
    { setup: "c200409", payoff: "c200502", what: "英國只修外殼時要寄什麼" },
    { setup: "c200505", payoff: "c200510", what: "鉸鏈與塗裝是不同問題" },
  ],
  youtube: {
    category_id: 27, made_for_kids: false, default_language: "zh-TW",
    title: "Zippo：終身保證，到底修好什麼？｜品牌故事",
    description: "一只舊打火機送修，終身承諾保住的是每片金屬，還是讓它繼續工作的能力？從公司事後回顧的 1933 年初期承諾，到原始專利的內外結構，再分別看英國現行內膽處置和美國現行機械、外觀保證界線。維修桌與人物是虛構示意，不是當年紀錄或真實個案；本片沒有吸菸或點火教學。資料核對日期：2026-10-24。\n\n資料來源：\nhttps://kb.zippo.com/the-history-of-zippo\nhttps://patentimages.storage.googleapis.com/c6/09/ea/1d1b14be9be79c/US2032695.pdf\nhttps://kb.zippo.com/warranty-repair\nhttps://kb.zippo.com/zippo-lighter/hinge-broke\nhttps://kb.zippo.com/zippo-lighter/worn-deco\nhttps://www.zippo.co.uk/pages/zippo-repairs-windproof-lighter",
    tags: ["Zippo", "終身保證", "品牌故事", "日用品的意外轉身", "維修"], video_id: null,
  },
  thumbnail: { template: "thumb", data: { headline: "壞了就修？", tag: "品牌故事", brand: "ZIPPO", shot: "c20-sc-0101" } },
  sources,
  scenes,
};
const series = {
  kind: "story", slug: "brand-stories-everyday-reversals", episode: 20, chapter: 1,
  title: "Zippo：終身保證，到底修好什麼？",
  logline: "一只舊金屬小盒的維修問題，從 1933 年公司回顧、原始專利，走到英國內膽與美國機械／外觀保證界線。",
  names: ["Zippo", "George G. Blaisdell", "George Gimera", "布萊斯德爾", "吉梅拉"],
  characters: [], visual_tier: "stills", compilation: false,
};
const labels = scriptRows.map((row) => {
  const shot = visual.shots.find((each) => each.line_id === row.id);
  return `| ${row.id} | ${row.narration} | ${shot.source_tags.replaceAll("|", "／")} |`;
});
const claims = `# C20 Zippo v8｜核准 36 句主張索引\n\n此表由鎖定的 v8 劇本及分鏡產生；來源與畫面 36／36 的獨立判定在舊專案 reviews/source-visual-v8-short-independent-20261024.md。這不是新的來源查核。公司史、原始專利、美國與英國現行服務的時地與權限不得混用。\n\n| 主張 ID | 已核准旁白 | 來源與畫面界線 |\n| --- | --- | --- |\n${labels.join("\n")}\n`;
const verify = `# C20 Zippo v8｜獨立查核結果對接\n\n衍生收據，並非新一輪獨立查核。鎖定 v8 輸入 SHA-256：劇本 ${inputs.script[1].toUpperCase()}；純旁白 ${inputs.plain[1].toUpperCase()}；分鏡 ${inputs.visual[1].toUpperCase()}。舊專案 reviews/source-visual-v8-short-independent-20261024.md 為 36／36 逐句來源與配鏡 PASS；兩位純旁白讀者各 12／12 Yes。站主精確稿件與本機試片 US$25 上限核准見舊專案 reviews/owner-v8-short-script-approval-20261024.md 和 reviews/owner-v8-paid-pilot-approval-20261024.md。\n\n| 主張 ID | 判定 | 來源及畫面限制 |\n| --- | --- | --- |\n${scriptRows.map((row) => `| ${row.id} | CONFIRMED | ${row.source_tags.replaceAll("|", "／")} |`).join("\n")}\n\n未實測配音、片格插圖時間、費用路由、成片或後台匯入。\n`;
const brief = `# C20 Zippo v8｜終身保證，到底修好什麼？\n\n本專案屬於「日用品的意外轉身」第 20 集。它從站主核准的 36 句／36 鏡 v8 短版直接建置；舊 story-everyday-zippo-c20 的 42 句原稿保持歷史版本。\n\n## 問題\n\n假想的一只舊金屬盒送到維修桌，免費修的承諾到底保住什麼？\n\n## 一句答案\n\n1933 年初期承諾只按公司事後回顧說明；原始專利可見內外套合，不能證當年實際送修工序。今天英國站對內膽處置及原件取回另有明文；美國站對傳統防風口袋打火機只保機械功能，鉸鏈破損與塗裝磨耗有不同答案。\n\n## 站主觀點\n\n讓觀眾順著桌上的同一只舊盒，辨清公司事後回顧、專利原件和現行英美服務條款。修好機械功能與保留每片舊件是兩個不同問題；不得把任一國的服務規則說成全球保證。\n\n## 六章\n\n冷開場是維修桌問句，接 5 秒頻道片頭；其後按公司回顧的單手小盒、1934／1936 年專利、英國現行寄件與內膽流程、美國現行保證界線，最後回到舊盒與觀眾的價值選擇。第 6 章後接既有 21 秒 v4 片尾及結束畫面連結。繁中 CC 可關閉，不燒字幕。\n\n## 製作停線\n\n只有非付費機器稿。站主核准本稿及本機試片 US$25 總額，但 C20 單集可歸因預算路由、實際語音價格、已花／未結費用與約六分鐘的實測時長政策仍須驗證。先按合格的 36 句實際配音量正文，再決定是否購買插圖；每圖至多三次，33 張不同插圖，3 張本機字卡。成片仍須以真實片格量正文插圖時間占比至少 70%。未後台匯入、上傳或發布。\n`;
const script = `# C20 Zippo v8｜36 句核准短版\n\n此檔由原核准稿逐字投影，原稿及 SHA 在 README.md。只有下表「旁白」進配音；章名和來源備註不念。\n\n| ID | 旁白 | 依據 |\n| --- | --- | --- |\n${labels.join("\n")}\n`;
const outputs = {
  "video.json": `${JSON.stringify(video, null, 2)}\n`,
  "series.json": `${JSON.stringify(series, null, 2)}\n`,
  "claims.md": claims,
  "verify-1.md": verify,
  "brief.md": brief,
  "script.md": script,
};
const check = process.argv.includes("--check");
for (const [name, content] of Object.entries(outputs)) {
  const dest = path.join(here, name);
  if (check) {
    const actual = readFileSync(dest, "utf8");
    if (actual !== content) throw new Error(`stale build output: ${name}`);
  } else writeFileSync(dest, content, "utf8");
}
console.log(`${check ? "checked" : "built"} ${scenes.length} scenes (${still} shots, ${card} cards), ${scriptRows.length} exact lines`);
