// Deterministically project the owner's approved v8 script and visual plan.
// No source file is edited; --check reads all outputs without writing anything.
import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { textHash } from "../../../tools/video/core/schema.mjs";

const dir = dirname(fileURLToPath(import.meta.url));
const check = process.argv.includes("--check");
if (process.argv.slice(2).some((arg) => arg !== "--check")) {
  throw new Error("Usage: node build-canonical.mjs [--check]");
}
const approved = {
  "script.md": "167DB38F368484951C56972B86A9838BB92B3B0B874952A87FBBAD26B8429312",
  "script-source-notes.md": "EF3AA1C79AB5EB19F0C52E9B024468AD6AF7A3EDC26AF17894D8C97D81BE538C",
  "visual-plan.md": "75E6AD2973078B72A28E17C5B2B9B58ACA5A1A247319CE5AB298D85E6F45DC2C",
  "visual-plan.json": "B211410713F271459AF267CC2F8DB4E8938A7EDB9938B6048A552A1076D4C063",
};
for (const [name, expected] of Object.entries(approved)) {
  const actual = createHash("sha256").update(readFileSync(join(dir, name))).digest("hex").toUpperCase();
  if (actual !== expected) throw new Error(`${name} changed since owner approval: ${actual}`);
}

const script = readFileSync(join(dir, "script.md"), "utf8");
const notes = readFileSync(join(dir, "script-source-notes.md"), "utf8");
const visual = JSON.parse(readFileSync(join(dir, "visual-plan.json"), "utf8"));
const rows = [...script.matchAll(/^- \*\*([HOIETN]\d{2})\*\* (.+?)〔(.+?)〕$/gm)]
  .map((match) => ({ sourceId: match[1], text: match[2], evidence: match[3] }));
if (visual.slug !== "story-everyday-camelbak-c14" ||
    visual.look?.preset !== "cute-mystery" ||
    visual.intro?.after_script_line !== "H05" || visual.intro.duration_s !== 5 ||
    visual.outro?.duration_s !== 21 || rows.length !== 70 || visual.shots?.length !== 70 ||
    new Set(rows.map((row) => row.sourceId)).size !== 70) {
  throw new Error("C14 approved project boundary or 70-line structure changed");
}
const counts = { H: 5, O: 9, I: 13, E: 11, T: 17, N: 15 };
for (const [chapter, expected] of Object.entries(counts)) {
  if (rows.filter((row) => row.sourceId.startsWith(chapter)).length !== expected) {
    throw new Error(`C14 chapter ${chapter} differs from the approved ${expected} lines`);
  }
}
const titles = {
  H: "騎到一半，手還在車把上",
  O: "襪子把水移到背上",
  I: "商品跟著騎士進店",
  E: "嘴邊的出口有了新文件",
  T: "咬合口被帶進水瓶",
  N: "瓶子走出單車店",
};
const sourceIdToLineId = (sourceId) => `c14${sourceId.toLowerCase()}`;
// Reading candidates only: text, subtitles and the owner's approved narration are unchanged.
// These are not pronunciation approvals or evidence of a successful voice audition.
const readings = [
  ["CamelBak", "凱莫貝克"], ["Michael", "麥可"], ["Eidson", "艾德森"],
  ["ThermoBak", "瑟莫貝克"], ["Jeff", "傑夫"], ["Wemmer", "威默"],
  ["GearJunkie", "吉爾將奇"], ["Sally", "莎莉"], ["McCoy", "麥考伊"],
  ["Better", "貝特"], ["Bottle", "博透"],
];
const scenes = rows.map((row, index) => {
  const plan = visual.shots[index];
  if (plan.line !== row.sourceId || !Number.isFinite(plan.planned_duration_s) || plan.planned_duration_s <= 0) {
    throw new Error(`C14 script/visual mismatch at ${row.sourceId}`);
  }
  const lineId = sourceIdToLineId(row.sourceId);
  const scene = {
    id: `c14-sc-${lineId}`,
    ...(index === 0 || rows[index - 1].sourceId[0] !== row.sourceId[0]
      ? { chapter: titles[row.sourceId[0]] } : {}),
  };
  if (plan.kind === "illustration") {
    if (!plan.prompt || !["push_in", "pan_left", "pan_right", "pull_back"].includes(plan.motion)) {
      throw new Error(`C14 illustration ${row.sourceId} lacks its approved prompt/motion`);
    }
    scene.template = "shot";
    scene.data = { prompt: plan.prompt, camera: plan.motion.replaceAll("_", " "), visual: "still" };
  } else if (plan.kind === "card") {
    if (!plan.post_text || Object.hasOwn(plan, "prompt")) {
      throw new Error(`C14 card ${row.sourceId} must only contain approved post text`);
    }
    scene.template = "big";
    scene.data = { text: plan.post_text };
  } else {
    throw new Error(`Unknown C14 visual kind at ${row.sourceId}: ${plan.kind}`);
  }
  scene.claims = [row.sourceId];
  const line = { id: lineId, text: row.text, emotion: "自然說書；公司回顧與年代放慢，章末留半拍" };
  const candidate = readings.reduce((say, [term, reading]) => say.replaceAll(term, reading), row.text);
  if (candidate !== row.text) {
    line.say = candidate;
    line.say_for = textHash(row.text);
  }
  scene.lines = [line];
  return scene;
});
if (scenes.filter((scene) => scene.template === "shot").length !== 54 ||
    scenes.filter((scene) => scene.template === "big").length !== 16) {
  throw new Error("C14 approved visual mix changed from 54 illustrations / 16 cards");
}
const sourceEntries = [...notes.matchAll(/^\| (S\d+) \| \[([^\]]+)\]\((https:\/\/[^)]+)\)/gm)]
  .map((match) => ({ id: match[1], title: match[2], url: match[3] }));
if (sourceEntries.length !== 12 || sourceEntries.some((entry, index) => entry.id !== `S${index + 1}`)) {
  throw new Error("C14 source notes no longer index S1–S12");
}
const citedSourceIds = new Set(rows.flatMap((row) => row.evidence.match(/S\d+/g) ?? []));
if ([...citedSourceIds].some((id) => !sourceEntries.some((source) => source.id === id))) {
  throw new Error("C14 narration cites a source missing from the approved notes");
}
const video = {
  schema_version: 1,
  slug: "story-everyday-camelbak-c14",
  format: "drama",
  // Illustrated shots and postproduced big cards use this supported preset combination.
  category: "explainer",
  narration_locale: "zh-TW",
  target_minutes: [8, 10],
  voice: { provider: "gemini", name: "Sulafat",
    style: "標準國語，台灣日常說書語調；保留問題、轉折和歸因，外文、年份與數字清楚放慢。" },
  subtitles: { burn_in: false },
  look: { preset: "cute-mystery" },
  characters: [],
  series: { slug: "brand-stories-everyday-reversals", episode: 14, chapter: 1 },
  music: { prompt: "light, curious, a little mysterious, no vocals", gain_db: -20, duck_db: -10 },
  loops: [
    { setup: "c14h01", payoff: "c14o06", what: "騎車時怎麼少一次伸手取瓶" },
    { setup: "c14h03", payoff: "c14o07", what: "襪中水袋的出口怎樣關住" },
    { setup: "c14h04", payoff: "c14i10", what: "臨時裝置如何被帶進單車店" },
    { setup: "c14h05", payoff: "c14n13", what: "免持飲水品牌為何又賣水瓶" },
    { setup: "c14o09", payoff: "c14i04", what: "首款商品最初跟著哪些騎士" },
    { setup: "c14i13", payoff: "c14t05", what: "改良口器文件如何連到水瓶申請" },
    { setup: "c14e06", payoff: "c14e08", what: "騎士之外誰需要背水" },
    { setup: "c14e11", payoff: "c14t05", what: "嘴邊出口怎樣走進瓶子設計" },
    { setup: "c14t11", payoff: "c14n02", what: "瓶類如何擴大接觸的使用場景" },
    { setup: "c14n04", payoff: "c14n07", what: "瓶類在當年商品組合占多少" },
  ],
  youtube: {
    category_id: 27, made_for_kids: false, default_language: "zh-TW",
    title: "CamelBak：為了騎車不用拿水瓶，後來為何推出水瓶？｜品牌故事",
    description: "一只襪子裡的水袋，把騎車喝水的動作改了方向。這集沿著 CamelBak 的品牌回顧、專利文件、展會報導和母公司年報，追看它如何走進單車店，又在 2006 年把水瓶列入產品線。\n\n早期原型與巡店細節主要出自品牌多年後回顧；2003 年報導是預備寄送，專利設計不等於每款量產商品。2012／2014 年比例只指各當年 CamelBak 毛銷售額，不能推出個別設計帶動銷量。畫面是匿名、無商標的原創概念插畫，非歷史實錄或專利附圖。來源網址列於本片說明的來源清單；本說明依 2026-10-23 核准稿整理。",
    tags: ["CamelBak", "水袋", "水瓶", "品牌故事", "日用品的意外轉身"],
    video_id: null,
  },
  thumbnail: { template: "thumb", data: {
    headline: "水袋→水瓶？", tag: "品牌故事", brand: "CAMELBAK", shot: "c14-sc-c14h05",
  } },
  // Include only sources actually cited by the approved narration. S6 was not
  // directly reopened in v7, so the excluded background sources are not dated here.
  sources: sourceEntries.filter(({ id }) => citedSourceIds.has(id))
    .map(({ title, url }) => ({ title, url, checked_on: "2026-10-23" })),
  scenes,
};
const series = {
  kind: "story", slug: "brand-stories-everyday-reversals", episode: 14, chapter: 1,
  title: "CamelBak：為了騎車不用拿水瓶，後來為何推出水瓶？",
  logline: "從襪中水袋、單車店與咬合口文件，走到後來因不同飲水場景推出的水瓶產品線。",
  names: ["CamelBak", "Michael Eidson", "Eidson", "ThermoBak", "Jeff Wemmer", "Wemmer", "GearJunkie", "Better Bottle", "Sally McCoy", "McCoy"],
  characters: [], visual_tier: "stills", compilation: false,
};
const outputs = {
  "video.json": `${JSON.stringify(video, null, 2)}\n`,
  "series.json": `${JSON.stringify(series, null, 2)}\n`,
  "claims.md": [
    "# C14 CamelBak｜核准逐句稿的主張索引", "",
    "本表只把站主核准 v8 70 句原稿與行末來源記號逐行對接，並非新一輪史實查核。歸因和限制仍依 script-source-notes.md、v7 全稿獨立覆核及 v8 N10 差異覆核。", "",
    "| 主張 ID | 已核准旁白 | 來源與限制 |", "| --- | --- | --- |",
    ...rows.map((row) => `| ${row.sourceId} | ${row.text} | ${row.evidence} |`), "",
  ].join("\n"),
  "verify-1.md": [
    "# C14 CamelBak｜既有獨立來源判定的 QA 對接", "",
    "衍生收據，非本輪重做來源查核。reviews/independent-v7-source-visual-review.md 對 70 行前版僅 N10 HOLD；reviews/independent-v8-n10-delta-review.md 只補上 N10 窄修 PASS。兩份收據合讀，才是站主核准 v8 的來源／文字配鏡依據。CONFIRMED 表示已核稿遵守來源歸因與限制，不把品牌後來回顧當同期原件，也不把專利提案當量產商品。", "",
    `綁定 script.md SHA-256：${approved["script.md"]}。未核准付費、配音、圖片、成片、匯入或上架。`, "",
    "| 主張 ID | 既有判定 | 原稿來源與限制 |", "| --- | --- | --- |",
    ...rows.map((row) => `| ${row.sourceId} | CONFIRMED | ${row.evidence} |`), "",
  ].join("\n"),
  "brief.md": `# C14 CamelBak｜為了不拿水瓶，為何後來又推出水瓶？\n\n本集屬「日用品的意外轉身」。站主已核准 70 句繁中旁白與 70 鏡 v8 方向；本機器專案只作非付費轉檔，不改受核准 SHA 綁定的原稿或分鏡。C14 的整支 US$25 試片報價仍是未核准提案。\n\n## 問題\n\n騎車不想騰手拿瓶，為何從襪中水袋起步的 CamelBak 後來又推出水瓶？\n\n## 一句答案\n\n依品牌多年後回顧，原型把水背到身上，商品經競技騎士與單車店接觸更多人；2006 年水瓶產品另為不同使用場景進入市場。母公司 2014 年報把瓶類和背水包都列為當年的產品線，瓶類約占 CamelBak 當年毛銷售額一半，但這不證某個原型、專利或銷售員單獨造成比例變化。\n\n## 站主觀點\n\n以「不用拿瓶」開題，沿水袋原型、商品、賣到單車店、嘴邊出口的設計文件與後來的水瓶走一條時間線；結尾回到不同場景要用不同容器。1998 口器專利、2005 水瓶申請、2006 展會實物各守文件身分，不能畫成同一件量產零件。\n\n## 畫面與證據界線\n\n54 鏡是匿名、無標誌的原創概念插圖；16 張為後製字卡，不交給生圖模型畫可讀字。品牌回顧中的 Eidson、Wemmer 不畫真人肖像；不仿當年賽事、店鋪、專利附圖、展場或戰地。2003 年報導只說預備寄送；2012／2014 年比例限各年 CamelBak 毛銷售額。冷開場 H01–H05 後接既有 5 秒片頭，N15 後接 21 秒 v4 片尾與 Studio 連結位；繁中 CC 可關閉。\n\n70 鏡紙上合計 496.5 秒，扣除片頭前冷開場 40.3 秒，片頭後正文僅 456.2 秒，低於須**實測**的 480 秒門檻。這不是語音時長，不能加片頭、片尾或冷開場湊數；未核准付費且缺可歸因預算帳本、舊費用與帳戶實價，TTS、圖片、配樂及媒體製作維持 HOLD。\n`,
};
for (const [name, content] of Object.entries(outputs)) {
  const path = join(dir, name);
  if (check) {
    if (readFileSync(path, "utf8") !== content) throw new Error(`${name} differs from approved-source projection`);
  } else {
    writeFileSync(path, content, "utf8");
  }
}
console.log(JSON.stringify({ checked: check, approved_lines: rows.length, scenes: scenes.length,
  illustrations: 54, cards: 16, indexed_sources: sourceEntries.length, cited_sources: citedSourceIds.size }));
