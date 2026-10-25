// Rebuild the nonpaid canonical project from the owner's approved v13 originals.
// This script reads, hashes, and compares those originals; it never edits them.
import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { textHash } from "../../../tools/video/core/schema.mjs";

const dir = dirname(fileURLToPath(import.meta.url));
const approved = {
  "script.md": "B4AF0F8A47D57E57D35A86A6092851F0282D52B5B5CA95DD62DFE036D0588E8F",
  "script-source-notes.md": "992CA5A43A0B0E5383DA92E010B8780FCE0D910462DCF600D1C97C12615526DD",
  "source-matrix.md": "8F0996CCD52894F97754D5060C44C85310C9073971D365EF353C238760633AFE",
  "visual-plan.md": "F08C0DC4A2EAF2BD1B16ABC44DA8C692EC8C628FD34136151B043A05C70B9553",
  "visual-plan.json": "8496FA62BD8BC9DA93F82B2B72F76826CA30FDFB47481C83F47E60038E9E6D50",
};
for (const [name, expected] of Object.entries(approved)) {
  const actual = createHash("sha256").update(readFileSync(join(dir, name))).digest("hex").toUpperCase();
  if (actual !== expected) throw new Error(`${name} changed since owner approval: ${actual}`);
}

const script = readFileSync(join(dir, "script.md"), "utf8");
const visual = JSON.parse(readFileSync(join(dir, "visual-plan.json"), "utf8"));
const rows = [...script.matchAll(/^\| (c19\d{4}) \| ([^|]+) \| ([^|]+) \|$/gm)]
  .map((match) => ({ id: match[1], text: match[2].trim(), evidence: match[3].trim() }));
if (rows.length !== 79 || visual.shots.length !== 79 || new Set(rows.map((row) => row.id)).size !== 79) {
  throw new Error("C19 approved source must contain 79 distinct script and visual IDs");
}
for (const [index, row] of rows.entries()) {
  const plan = visual.shots[index];
  if (row.id !== plan.line_id || row.text !== plan.narration || row.evidence !== plan.source_tags) {
    throw new Error(`C19 source-to-visual mismatch at ${row.id}`);
  }
}
if (visual.shots.filter((shot) => shot.kind === "shot").length !== 69 ||
    visual.shots.filter((shot) => shot.kind === "card").length !== 10) {
  throw new Error("C19 approved visual mix changed from 69 illustrations / 10 cards");
}

const chapterTitles = {
  hook: "超商貨架旁，這台機器通往哪裡？",
  origin: "店比銀行晚關，需求先來了",
  idea: "先開銀行，再接上機器",
  engine: "一萬台機器，還得補得上鈔",
  turn: "螢幕上的費，和年報裡的收入",
  now: "櫃台關了，這個入口還在",
};
const chapterCounts = { hook: 7, origin: 11, idea: 14, engine: 18, turn: 17, now: 12 };
for (const [chapter, expected] of Object.entries(chapterCounts)) {
  if (visual.shots.filter((shot) => shot.chapter === chapter).length !== expected) {
    throw new Error(`C19 chapter ${chapter} no longer has ${expected} approved lines`);
  }
}
const cardSources = {
  c190208: "Seven Bank ATM 20 周年年表",
  c190302: "Seven Bank 公司沿革",
  c190306: "IY Bank 2001-11-09 設點公告",
  c190311: "IY Bank 2002 首次揭露誌",
  c190401: "Seven Bank 公司沿革",
  c190408: "Seven Bank 公司沿革",
  c190412: "Seven Bank 公司沿革",
  c190414: "Seven Bank Annual Report 2010",
  c190505: "Seven Bank Annual Report 2010",
  c190510: "Seven Bank Annual Report 2010 財務附註",
};
const cameraMoves = ["push in", "pan left", "pull back", "tilt up", "pan right", "tilt down"];
const splitAfter = {
  c190310: "；",
  // Keep the fictional bank approval and cash withdrawal in the same scene.
  c190610: "著落。",
};
const split = (row) => {
  const marker = splitAfter[row.id];
  if (!marker) return [row.text];
  const pivot = row.text.indexOf(marker);
  if (pivot < 0) throw new Error(`C19 split punctuation absent from ${row.id}`);
  const first = row.text.slice(0, pivot + marker.length);
  const second = row.text.slice(pivot + marker.length);
  if (!first || !second || first + second !== row.text) throw new Error(`C19 split altered ${row.id}`);
  return [first, second];
};
const spokenCandidate = (text) => text
  .replaceAll("IY Bank", "I Y 銀行")
  .replaceAll("Seven Bank", "賽文銀行")
  .replaceAll("ATM", "A T M");

const scenes = [];
let lastChapter = null;
for (const [index, row] of rows.entries()) {
  const plan = visual.shots[index];
  if (!Object.hasOwn(chapterTitles, plan.chapter)) throw new Error(`Unexpected C19 chapter ${plan.chapter}`);
  const parts = split(row);
  for (const [partIndex, part] of parts.entries()) {
    const id = `${row.id}${partIndex ? "a" : ""}`;
    const scene = { id: `c19-sc-${id}` };
    if (lastChapter !== plan.chapter) scene.chapter = chapterTitles[plan.chapter];
    lastChapter = plan.chapter;
    const line = {
      id,
      text: part,
      emotion: "自然說書；年份、公司歸因和財務單位放慢，章末問題留半拍",
    };
    const say = spokenCandidate(part);
    if (say !== part) {
      line.say = say;
      line.say_for = textHash(part);
    }
    if (plan.kind === "card") {
      if (parts.length !== 1) throw new Error(`C19 card ${row.id} cannot be split`);
      const separator = " · ";
      const pivot = plan.card_text.indexOf(separator);
      if (pivot < 0) throw new Error(`C19 card ${row.id} has no value-label separator`);
      const value = plan.card_text.slice(0, pivot);
      const label = plan.card_text.slice(pivot + separator.length);
      if (!value || !label || `${value}${separator}${label}` !== plan.card_text || !cardSources[row.id]) {
        throw new Error(`C19 card ${row.id} cannot be reproduced`);
      }
      scene.template = "stats";
      scene.data = { stats: [{ value, label }], source: cardSources[row.id] };
    } else if (plan.kind === "shot") {
      scene.template = "shot";
      scene.data = {
        prompt: `${partIndex ? "Close-up." : "Medium shot."} ${plan.prompt}`,
        camera: cameraMoves[scenes.length % cameraMoves.length],
        visual: "still",
      };
    } else {
      throw new Error(`Unexpected C19 visual kind ${plan.kind}`);
    }
    scene.claims = [row.id];
    scene.lines = [line];
    scenes.push(scene);
  }
}
if (scenes.length !== 81 || scenes.filter((scene) => scene.template === "shot").length !== 71 ||
    scenes.filter((scene) => scene.template === "stats").length !== 10) {
  throw new Error("C19 canonical split should yield 81 scenes, 71 stills, 10 cards");
}

const source = (title, url) => ({ title, url, checked_on: "2026-10-24" });
const video = {
  schema_version: 1,
  slug: "story-everyday-seven-bank-c19",
  format: "drama",
  // Current stills + stats lint supports cute-mystery under explainer.
  category: "explainer",
  narration_locale: "zh-TW",
  target_minutes: [9, 11],
  voice: {
    provider: "gemini", name: "Sulafat",
    style: "標準國語，咬字清楚，台北日常說話語調。以克制的說書節奏講真實銀行網路故事；年份、公司歸因和財務單位放慢，章末留半拍。",
  },
  subtitles: { burn_in: false },
  look: { preset: "cute-mystery" },
  characters: [],
  series: { slug: "brand-stories-everyday-reversals", episode: 19, chapter: 1 },
  music: { prompt: "light, curious, a little mysterious, no vocals", gain_db: -20, duck_db: -10 },
  loops: [
    { setup: "c190103", payoff: "c190608", what: "他行卡可提款的條件" },
    { setup: "c190104", payoff: "c190602", what: "交易如何連回發卡機構" },
    { setup: "c190105", payoff: "c190605", what: "提款機如何維持有鈔" },
    { setup: "c190106", payoff: "c190505", what: "顧客端免費時誰付網路費" },
    { setup: "c190208", payoff: "c190312", what: "既有超商 ATM 先例之後這家銀行做什麼" },
    { setup: "c190305", payoff: "c190306", what: "銀行開業後機器何時開始服務" },
    { setup: "c190407", payoff: "c190411", what: "何時接受海外發卡" },
    { setup: "c190508", payoff: "c190510", what: "網路費用收入的可核年度數字" },
    { setup: "c190518", payoff: "c190605", what: "附近營業款怎樣納入現金管理" },
  ],
  youtube: {
    category_id: 27, made_for_kids: false, default_language: "zh-TW",
    title: "Seven Bank：超商裡的 ATM，怎麼成了一家銀行的網路？｜品牌故事",
    description: "夜裡，一位想像中的顧客拿著他行卡站在超商提款機前。這集從便利商店代收帳單、2001 年銀行與 ATM 網起步，追到後來跨機構服務如何維持機器、現金與費用。\n\n片中顧客、晚餐與提款結果均為明示的假想情境。1987 年顧客需求據公司後來回顧；2001–2007 的設點與服務日期依公司沿革及同期公告。2010 年報的合作機構、費用與現金管理僅指當年模型，不能當今天逐卡費率、個別機器紀錄或每台利潤。畫面均是匿名原創概念插畫，不重建真實店面、提款機、卡片、操作介面或交易。資料查核日期：2026-10-24。",
    tags: ["Seven Bank", "便利商店", "ATM", "銀行", "品牌故事", "日用品的意外轉身"],
    video_id: null,
  },
  thumbnail: {
    template: "thumb",
    data: { headline: "超商\n**開銀行？**", tag: "品牌故事", brand: "SEVEN BANK", shot: "c19-sc-c190101" },
  },
  sources: [
    source("Seven Bank, ATM 20th anniversary history", "https://www.sevenbank.co.jp/corp/company/atm-history.html"),
    source("Seven Bank, company history", "https://www.sevenbank.co.jp/english/corp/company/history.html"),
    source("Seven Bank, Annual Report 2010", "https://www.sevenbank.co.jp/english/ir/library/disclosure/pdf/2010092231.pdf"),
    source("Seven Bank, Integrated Report 2024", "https://www.sevenbank.co.jp/english/ir/library/disclosure/pdf/2024073101.pdf"),
    source("IY Bank, 2005 name change announcement", "https://www.sevenbank.co.jp/corp/news/2005/060801.html"),
    source("IY Bank, Disclosure 2002", "https://www.sevenbank.co.jp/corp/disclosure/pdf/IYBank.pdf"),
    source("IY Bank, 2001 ATM expansion announcement", "https://www.sevenbank.co.jp/corp/news/2001/1109_1.html"),
    source("IY Bank, Disclosure 2005", "https://www.sevenbank.co.jp/corp/disclosure/pdf/2005_all.pdf"),
  ],
  scenes,
};
const series = {
  kind: "story", slug: "brand-stories-everyday-reversals", episode: 19, chapter: 1,
  title: "Seven Bank：超商裡的 ATM，怎麼成了一家銀行的網路？",
  logline: "先有店內提款需求和其他業者的先例，零售集團成立銀行後，才把合作卡、機器維護、現金管理與收費接成一張網。",
  names: ["Seven Bank", "IY Bank", "7-Eleven", "Ito-Yokado", "Seven & i"],
  characters: [], visual_tier: "stills", compilation: false,
};
const write = (name, content) => writeFileSync(join(dir, name), content, "utf8");
write("video.json", `${JSON.stringify(video, null, 2)}\n`);
write("series.json", `${JSON.stringify(series, null, 2)}\n`);
write("claims.md", [
  "# C19 Seven Bank｜核准逐句稿的主張索引", "",
  "此表由站主核准的 79 句 v13 原稿逐行轉出，不是新一輪史實查核。每句的年代、歸因、虛構界線以 source-matrix.md、script-source-notes.md 與 reviews/independent-v13-source-visual.md 為準。", "",
  "| 主張 ID | 已核准旁白 | 來源與限制 |", "| --- | --- | --- |",
  ...rows.map((row) => `| ${row.id} | ${row.text} | ${row.evidence} |`), "",
].join("\n"));
write("verify-1.md", [
  "# C19 Seven Bank｜既有 v13 獨立來源判定的 QA 對接", "",
  "衍生收據，不是本輪新的來源查核。reviews/independent-v13-source-visual.md 已對核准稿逐句來源與文字配鏡均判 79/79 PASS；CONFIRMED 只表示句子遵守各來源所註的年代、歸因與假想情境界線，不表示公司回顧已取得當期問卷、個別提款交易或今日費率證據。該收據的原始雜湊是 CRLF 表示，與 Git LF 原稿的同一性由 reviews/v13-line-ending-hash-reconciliation-20261024.md 核對。", "",
  `綁定 script.md SHA-256：${approved["script.md"]}。此對接不核准配音、圖片、配樂、匯入、上傳或發布。`, "",
  "| 主張 ID | 既有判定 | 原稿來源與限制 |", "| --- | --- | --- |",
  ...rows.map((row) => `| ${row.id} | CONFIRMED | ${row.evidence} |`), "",
].join("\n"));
write("brief.md", `# C19 Seven Bank｜超商提款機，怎麼變成一家銀行的網路？\n\n本集屬於「日用品的意外轉身」。站主已核准六章企劃、79 句繁中旁白與 79 鏡方向；本機器專案只作非付費轉檔，不改已核准雜湊綁定的稿件與分鏡。後台已有待審的劇本卡，但沒有正式成片。C19 尚無整支本機試片報價或付費製作核准。\n\n## 問題\n\n超商裡多放一台提款機，為何還需要成立一家銀行，才把其他金融機構的卡、現金與維護接起來？\n\n## 一句答案\n\n零售集團先成立 IY Bank、取得牌照，經營自家帳戶服務及供合作機構使用的 ATM 網；機器擴張後，還需中繼、維護、現金管理及合作方付的網路使用費。2010 年年報的費用資料是當年整張網的收入，不是顧客眼前每筆費或單機利潤。\n\n## 站主觀點\n\n以一位明示虛構、夜裡想提款的顧客維持故事主線，把觀眾眼前一台機器拆成牌照、合作網路、現金和維護四種不同工作。顧客眼前的費用與經營者取得的網路費分開講，不把任何一筆提款寫成實錄。\n\n## 證據界線\n\n她的晚餐需求與最後成功提款都不可說成史實。1987 年代收與顧客調查按公司事後回顧，1999 年已有其他超商 ATM；不能稱 Seven Bank 首創。2001 年成立、獲牌、開業與機器啟用各是不同日期。2005–2007 擴張與 2010 年模型分開，59 個地點與 66 台機器、555 家合作金融機構、¥853 億年度相關費收入各守正確單位與時點。\n\n## 六章與畫面\n\n夜間提款疑問 → 代收與先例 → 持牌銀行和首批機器 → 設點、補鈔及支援 → 顧客費與合作機構費分開 → 顧客的假想提款回收。原畫面方向是 69 張原創匿名插圖、10 張後製字卡；兩句較長旁白在標點切成兩段場景，顯示文字拼回核准原句，原稿不改。卡片須由後製排字，畫面不仿真 Seven-Eleven 店、真 ATM UI、銀行卡、財報或特定鈔票流向。濃縮開場 c190107 後接既有 5 秒片頭，最後 c190612 後接 21 秒 v4 片尾及連結安全區；繁中 CC 不燒錄。\n\n正文原稿按 250 spoken units/minute 紙上純旁白 458.16 秒，候選 say 讀法則約 468.72 秒，兩種估計均未達到要實測的 480 秒；場景停頓也不能充當語音秒數。C19 無付費試片授權，不得呼叫供應商。若未來另獲授權，須先用實際旁白驗證片頭後正文至少 480 秒，再購圖；真正時間軸的插圖畫面至少 70%，後製字卡連續不得超過三張。\n`);
console.log(JSON.stringify({ approved_lines: rows.length, scenes: scenes.length, stills: scenes.filter((s) => s.template === "shot").length, cards: scenes.filter((s) => s.template === "stats").length, pronunciation_candidates: scenes.filter((s) => s.lines[0].say).length }));
