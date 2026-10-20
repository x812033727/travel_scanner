// Offline Shorts metadata, source map, and portrait plan; no rendering or upload.
import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { episodeShortsProblems } from "../../../tools/video/shorts/episode.mjs";

const dir = path.dirname(fileURLToPath(import.meta.url));
const base = "story-everyday-uber-x19";
const videoBytes = readFileSync(path.join(dir, "video.json"));
const video = JSON.parse(videoBytes);
const videoSha = createHash("sha256").update(videoBytes).digest("hex");
const src = {
  S2: "https://www.sec.gov/Archives/edgar/data/1543151/000154315120000027/uberq220earningspressr.htm",
  S3a: "https://www.sec.gov/Archives/edgar/data/1543151/000155278120000412/e20423_uber-8k.htm",
  S4: "https://www.sec.gov/Archives/edgar/data/1543151/000162828020015770/uberq320earningspressr.htm",
  S5: "https://www.sec.gov/Archives/edgar/data/1543151/000155278120000580/e20585_ex99-1.htm",
  S5a: "https://www.sec.gov/Archives/edgar/data/1543151/000155278120000580/e20585_uber-8k.htm",
};
const rows = [[], []];
let active = -1;
for (const raw of readFileSync(path.join(dir, "drafts/shorts.md"), "utf8").split(/\r?\n/)) {
  const header = raw.match(/^## Short ([12]):/);
  if (header) { active = Number(header[1]) - 1; continue; }
  if (!/^x19s[12]\d{2}\s*\|/.test(raw)) continue;
  const parts = raw.split("|").map(part => part.trim());
  if (parts.length !== 4 || active < 0) throw new Error(`Malformed Short row: ${raw}`);
  const [id, refsText, text, focus] = parts;
  const refs = refsText === "editorial" ? [] : refsText.split(",");
  if (!text || [...text].length > 38 || !focus || refs.some(ref => !src[ref])) throw new Error(`Invalid Short row: ${id}`);
  if (/Uber|Eats|Postmates|logo|brand|readable|trademark/iu.test(focus)) throw new Error(`Branded visual focus: ${id}`);
  rows[active].push({ id, refs, text, focus });
}
for (const [si, short] of rows.entries()) {
  if (short.length !== 8) throw new Error(`Short ${si + 1} needs eight beats`);
  for (const [ri, row] of short.entries()) if (row.id !== `x19s${si + 1}${String(ri + 1).padStart(2, "0")}`) throw new Error(`Short ID out of order: ${row.id}`);
}
const lineToScene = new Map(video.scenes.flatMap(scene => scene.lines.map(line => [line.id, scene])));
const anchors = [
  ["x190301", "x190305", "x190306", "x190307", "x190319", "x190318", "x190309", "x190322"],
  ["x190401", "x190403", "x190407", "x190409", "x190501", "x190503", "x190504", "x190421"],
];
const crops = [[656, 640, 672, 660, 635, 656, 680, 650], [650, 675, 656, 645, 670, 656, 685, 640]];
const beats = ["hook", "setup", "turn", "proof", "proof", "proof", "proof", "payoff"];
const specs = [
  {
    titles: ["Uber 外送交易額超車，為何還虧？", "外送比載客大，為何不是獲利？"],
    headlines: ["外送超車？", "外送金額更大", "這不是營收", "公司收入另算", "外送還虧", "載客卻為正", "兩張不同帳", "超車不等於賺"],
    numberCards: { 1: { big: "69.61億", note: "外送；2020 Q2 平台訂單額／美元" }, 4: { big: "−2.32億", note: "外送部門調整後 EBITDA／美元" }, 5: { big: "+0.5億", note: "載客部門同尺度／美元" } },
    description: "2020 Q2 Uber Delivery 平台訂單額 US$6.961bn，高於 Mobility US$3.046bn，但這不是 Uber 確認營收或獲利。同期外送部門調整後 EBITDA 為負 US$232m，載客部門為正 US$50m。此 Short 的重點是把交易額與部門指標分開。畫面是無品牌概念插畫，數字由原生 9:16 字卡排版；正式長片網址待真實上傳後回填。",
    refs: ["S2"],
  },
  {
    titles: ["Postmates 救了 Uber 2020 外送反超？", "六月已反超，Postmates 幾月才交割？"],
    headlines: ["收購救了超車？", "六月已反超", "七月才簽約", "交割前仍領先", "十二月才完成", "兩個入口還在", "網路才開始接", "時間不能倒放"],
    numberCards: { 2: { big: "7/6", note: "2020 年簽約；六月季報已結束" }, 3: { big: "85.5億", note: "2020 Q3 外送訂單額／美元；未交割" }, 4: { big: "12/1", note: "2020 年完成 Postmates 收購" } },
    description: "Uber 外送在 2020 Q2 的 Gross Bookings 已超過載客。它 7 月 6 日才簽約收購 Postmates，12 月 1 日才完成；第三季尚未交割時，外送交易額仍高於載客。因此不能把六月反超倒算成收購交割的效果。兩個消費者 App 在交割時仍分開，底層商家與配送網才開始整合。畫面和數字為後製概念設計；正式長片網址待實際上傳後回填。",
    refs: ["S2", "S3a", "S4", "S5", "S5a"],
  },
];
const shorts = rows.map((short, si) => ({
  schema_version: 2, slug: `${base}-short-${si + 1}`, format: "shorts", locale: "zh-TW", line: "cut", series: "illustrated",
  source: { slug: base }, synthetic_media: true, titles: specs[si].titles, description: specs[si].description,
  hashtags: ["Uber", "品牌故事", "商業故事"], tags: ["Uber", "外送", "品牌故事", "商業故事"],
  links: specs[si].refs.map(ref => ({ label: `Uber ${ref} SEC 原件`, url: src[ref] })),
  scenes: short.map((row, ri) => {
    const scene = lineToScene.get(anchors[si][ri]);
    if (!scene || scene.template !== "shot") throw new Error(`Short ${si + 1} beat ${ri + 1} lacks a shot: ${anchors[si][ri]}`);
    if (!scene.data.prompt.toLowerCase().includes(row.focus.toLowerCase())) throw new Error(`Short focus does not match shot: ${scene.id}`);
    return { beat: beats[ri], shot: scene.id, headline: specs[si].headlines[ri], ...(specs[si].numberCards[ri] ?? {}), narration: [row.text] };
  }),
}));
for (const short of shorts) {
  if (new Set(short.scenes.map(scene => scene.shot)).size !== short.scenes.length) throw new Error(`${short.slug}: repeated still`);
  const chars = short.scenes.flatMap(scene => scene.narration).join("").length;
  if (chars < 115 || chars > 225) throw new Error(`${short.slug}: ${chars} characters outside 25–55-second paper range`);
}
const problems = episodeShortsProblems(shorts, video);
if (problems.length) throw new Error(problems.join("\n"));
const bytes = JSON.stringify(shorts, null, 2) + "\n";
writeFileSync(path.join(dir, "shorts.json"), bytes);
const shortsSha = createHash("sha256").update(bytes).digest("hex");
writeFileSync(path.join(dir, "shorts-script.md"), ["# X19 Uber｜兩支獨立 Shorts 逐句稿", "", `主片 SHA-256：${videoSha}；Shorts SHA-256：${shortsSha}。離線前製，未配音、剪輯、實測或發布；兩支各自完整，均不使用主片 5 秒／21 秒書擋。`, "", ...shorts.flatMap((short, si) => [`## Short ${si + 1}｜${short.titles[0]}`, "", ...short.scenes.map((scene, ri) => `- ${rows[si][ri].id} ${scene.narration[0]}（${scene.shot}）`), "", `原始資料：${short.links.map(link => `[${link.label}](${link.url})`).join("、")}`, ""] )].join("\n"));
writeFileSync(path.join(dir, "shorts-source-matrix.md"), ["# X19 Uber｜Shorts 逐句作者來源矩陣", "", `shorts.json SHA-256：${shortsSha}；video.json SHA-256：${videoSha}。作者標記，不是獨立審核 PASS。`, "", "| Short／拍 | 句 ID | 旁白 | 作者來源 |", "| --- | --- | --- | --- |", ...rows.flatMap((short, si) => short.map((row, ri) => `| ${si + 1}／${ri + 1} | ${row.id} | ${row.text} | ${row.refs.length ? row.refs.join("、") : "敘事提問／依原件推理"} |`)), ""].join("\n"));
writeFileSync(path.join(dir, "shorts-portrait-plan.md"), [
  "# X19 Uber｜兩支 Shorts 的逐拍 9:16 規劃", "",
  `離線前製，綁定主片 ${videoSha} 與 Shorts ${shortsSha}。目前沒有插畫、直式輸出或手機檢查，以下裁切需出圖後逐拍核對焦點。`, "",
  "每拍從不同的主片 1920×1080 插畫 shot 取 608×1080 視窗，按表列 x、y=0 裁切，再等比輸出 1080×1920；原畫面提示詞要求焦點在中央 608px 走廊。若焦點出框，可在合法 x=0–1312 中移動；保不住才於 US$25 整片上限內重畫。品牌名、日期與金額都由 Shorts 原生 big／note／headline 排版，不請 image-01 畫字，也不重用橫式 stats 當作影格。", "",
  "直式文字安全區：畫布 1080×1920；headline x=78–902、下緣 y≤1380；字幕 x=80–900、y=1430–1595；底部操作區保留。產出後於 360px 寬手機逐拍看字卡、字幕、手機與車／餐袋焦點，測兩支均為 25–55 秒。Shorts 不套長片片頭片尾，也不預填虛構 watch URL。", "",
  "| Short／拍 | 重用主片 shot | 608×1080 左上角 | 直式焦點 | 原生排字 |",
  "| --- | --- | --- | --- | --- |",
  ...shorts.flatMap((short, si) => short.scenes.map((scene, ri) => `| ${si + 1}／${ri + 1} | ${scene.shot} | x=${crops[si][ri]}, y=0 | ${rows[si][ri].focus} | ${scene.headline}${scene.big ? `；big ${scene.big}；note ${scene.note}` : ""} |`)),
  "", "焦點與 shot prompt 在編譯時逐字核對，正式裁切在真實插畫生成後才驗。", "",
].join("\n"));
console.log(JSON.stringify({ video_sha256: videoSha, shorts_sha256: shortsSha, shorts: shorts.map(short => ({ slug: short.slug, beats: short.scenes.length, chars: short.scenes.flatMap(scene => scene.narration).join("").length })) }, null, 2));
