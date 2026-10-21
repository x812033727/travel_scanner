// Offline Shorts metadata, author source map, and 9:16 plan; no rendering or upload.
import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const dir = path.dirname(fileURLToPath(import.meta.url));
const base = "story-everyday-lululemon-x17";
const videoBytes = readFileSync(path.join(dir, "video.json"));
const video = JSON.parse(videoBytes);
const videoSha = createHash("sha256").update(videoBytes).digest("hex");
const src = {
  S1: "https://www.sec.gov/Archives/edgar/data/1397187/000119312513118207/d505115dex991.htm",
  S3: "https://www.sec.gov/Archives/edgar/data/1397187/000119312513140668/d516336dex991.htm",
  S4: "https://www.sec.gov/Archives/edgar/data/1397187/000119312513253430/d534167d10q.htm",
  S5: "https://www.sec.gov/Archives/edgar/data/1397187/000119312513253334/d551549dex99.htm",
};
const rows = [[], []];
let active = -1;
for (const raw of readFileSync(path.join(dir, "drafts/shorts.md"), "utf8").split(/\r?\n/)) {
  const header = raw.match(/^## Short ([12]):/);
  if (header) { active = Number(header[1]) - 1; continue; }
  if (!/^x17s[12]\d{2}\s*\|/.test(raw)) continue;
  const parts = raw.split("|").map(part => part.trim());
  if (parts.length !== 4 || active < 0) throw new Error(`Malformed Short row: ${raw}`);
  const [id, refsText, text, focus] = parts;
  const refs = refsText === "editorial" ? [] : refsText.split(",");
  if (!text || text.length > 40 || !focus || refs.some(ref => !src[ref])) throw new Error(`Invalid Short row: ${id}`);
  if (/Lululemon|Luon|logo|brand|readable|trademark/iu.test(focus)) throw new Error(`Branded visual focus: ${id}`);
  rows[active].push({ id, refs, text, focus });
}
for (const [si, short] of rows.entries()) {
  if (short.length !== 8) throw new Error(`Short ${si + 1} needs eight complete beats`);
  for (const [ri, row] of short.entries()) if (row.id !== `x17s${si + 1}${String(ri + 1).padStart(2, "0")}`) throw new Error(`Short ID out of order: ${row.id}`);
}
const lineToScene = new Map(video.scenes.flatMap(scene => scene.lines.map(line => [line.id, scene])));
const anchors = [
  ["x170101", "x170301", "x170405", "x170408", "x170409", "x170410", "x170416", "x170426"],
  ["x170305", "x170310", "x170503", "x170504", "x170509", "x170510", "x170512", "x170506"],
];
const crops = [[656, 640, 672, 660, 635, 656, 680, 650], [650, 675, 656, 645, 670, 656, 685, 640]];
const beats = ["hook", "setup", "turn", "proof", "proof", "proof", "proof", "payoff"];
const specs = [
  {
    titles: ["Lululemon：布可能達標，褲子為何太透？", "黑 Luon 褲：布樣測試漏了什麼？"],
    headlines: ["布可能達標？", "部分黑褲撤下", "舊標準低端", "檢驗有缺口", "版型又變動", "因素疊起來", "重測三項", "還要看成衣"],
    description: "Lululemon 在 2013 年撤下部分黑色 Luon 褲。公司 4 月 3 日的調查說，涉事布料可能符合當時測試、卻落在容許範圍低端；部分變數測試不全，加上版型細微變動，完成的褲子透度無法接受。這是公司同期的多因素解釋，並非獨立鑑定，也不能寫成所有黑褲都受影響。畫面為無品牌概念插畫；正式長片網址待實際上傳後回填。",
    refs: ["S1", "S3"],
  },
  {
    titles: ["Lululemon 撤下黑褲，營收怎麼還增兩成一？", "撤貨代價藏在財報哪一行？"],
    headlines: ["二〇一三年黑褲下架", "三月當時預估", "預測≠實損", "首季最後七週", "存貨成本入帳", "是成本，不是少賣", "全公司仍增收", "列入銷貨成本"],
    big: { 1: "US$57–67m", 4: "US$17.5m", 6: "+21%" },
    description: "2013 年 3 月，Lululemon 預估 FY2013 全年會因黑 Luon 褲事件少賣 US$57–67m；這是預測，不是最終量到的失去營收。FY2013 Q1 最後七週缺貨，另有 US$17.5m 存貨準備實列銷貨成本。同季公司整體營收仍增 21%；公司說其他既有商品線與新品拉動可比門市銷售。總營收可增，黑褲成本也能同時入帳。畫面為概念插畫，精確數字由後製排字；正式長片網址待上傳後回填。",
    refs: ["S1", "S4", "S5"],
  },
];
const shorts = rows.map((short, si) => ({
  schema_version: 2, slug: `${base}-short-${si + 1}`, format: "shorts", locale: "zh-TW", line: "cut", series: "illustrated",
  source: { slug: base }, synthetic_media: true, titles: specs[si].titles, description: specs[si].description,
  hashtags: ["Lululemon", "品牌故事", "商業故事"], tags: ["Lululemon", "Luon", "品牌故事", "運動褲"],
  links: specs[si].refs.map(ref => ({ label: `Lululemon ${ref} SEC 原件`, url: src[ref] })),
  scenes: short.map((row, ri) => {
    const scene = lineToScene.get(anchors[si][ri]);
    if (!scene || scene.template !== "shot") throw new Error(`Short ${si + 1} beat ${ri + 1} lacks a shot: ${anchors[si][ri]}`);
    if (!scene.data.prompt.toLowerCase().includes(row.focus.toLowerCase())) throw new Error(`Short focus does not match shot: ${scene.id}`);
    return { beat: beats[ri], shot: scene.id, headline: specs[si].headlines[ri], ...(specs[si].big?.[ri] ? { big: specs[si].big[ri] } : {}), narration: [row.text] };
  }),
}));
for (const short of shorts) {
  if (new Set(short.scenes.map(scene => scene.shot)).size !== short.scenes.length) throw new Error(`${short.slug}: repeated still`);
  const chars = short.scenes.flatMap(scene => scene.narration).join("").length;
  if (chars < 115 || chars > 225) throw new Error(`${short.slug}: ${chars} characters outside 25–55-second paper range`);
}
const bytes = JSON.stringify(shorts, null, 2) + "\n";
writeFileSync(path.join(dir, "shorts.json"), bytes);
const shortsSha = createHash("sha256").update(bytes).digest("hex");
writeFileSync(path.join(dir, "shorts-script.md"), ["# X17 Lululemon｜兩支獨立 Shorts 逐句稿", "", `主片 SHA-256：\`${videoSha}\`；Shorts SHA-256：\`${shortsSha}\`。離線前製，未配音、剪輯、實測或發布；兩支各自完整，均不使用主片 5 秒／21 秒官方書擋。`, "", ...shorts.flatMap((short, si) => [`## Short ${si + 1}｜${short.titles[0]}`, "", ...short.scenes.map((scene, ri) => `- \`${rows[si][ri].id}\` ${scene.narration[0]}（\`${scene.shot}\`）`), "", `原始資料：${short.links.map(link => `[${link.label}](${link.url})`).join("、")}`, ""] )].join("\n"));
writeFileSync(path.join(dir, "shorts-source-matrix.md"), ["# X17 Lululemon｜Shorts 逐句作者來源矩陣", "", `\`shorts.json\` SHA-256：\`${shortsSha}\`；\`video.json\` SHA-256：\`${videoSha}\`。作者標記，不是獨立審核 PASS。`, "", "| Short／拍 | 句 ID | 旁白 | 作者來源 |", "| --- | --- | --- | --- |", ...rows.flatMap((short, si) => short.map((row, ri) => `| ${si + 1}／${ri + 1} | \`${row.id}\` | ${row.text} | ${row.refs.length ? row.refs.join("、") : "敘事提問／依原件推理"} |`)), ""].join("\n"));
writeFileSync(path.join(dir, "shorts-portrait-plan.md"), [
  "# X17 Lululemon｜兩支 Shorts 的逐拍 9:16 規劃", "",
  `離線前製，綁定主片 \`${videoSha}\` 與 Shorts \`${shortsSha}\`。目前沒有插畫、直式輸出或手機檢查，以下裁切需出圖後逐拍核對焦點。`, "",
  "每拍從一張不同的主片 1920×1080 插畫 `shot` 取 608×1080 視窗，按表列 x、y=0 裁切，再等比輸出 1080×1920；原畫面提示詞要求焦點在中央 608px 走廊。若焦點出框，可在合法 x=0–1312 中移動；保不住才於 US$25 整片上限內重畫。所有品牌名、年份與數字均以後製原生字卡排版，不請 image-01 畫字。", "",
  "直式文字安全區：畫布 1080×1920；headline x=78–902、下緣 y≤1380；`big` 數字置於同安全寬度內，先在 360px 手機驗完整字形；字幕 x=80–900、y=1430–1595；底部操作區保留。產出後逐拍看字卡、字幕與手／褲焦點，測兩支均為 25–55 秒。Shorts 不套長片片頭片尾，也不預填虛構 watch URL。", "",
  "| Short／拍 | 重用主片 shot | 608×1080 左上角 | 直式焦點 | 原生 headline | 原生大數字 |",
  "| --- | --- | --- | --- | --- | --- |",
  ...shorts.flatMap((short, si) => short.scenes.map((scene, ri) => `| ${si + 1}／${ri + 1} | \`${scene.shot}\` | \`x=${crops[si][ri]}, y=0\` | ${rows[si][ri].focus} | ${scene.headline} | ${scene.big ?? "—"} |`)),
  "", "焦點與 shot prompt 在編譯時逐字核對，正式裁切在真實插畫生成後才驗。", "",
].join("\n"));
console.log(JSON.stringify({ video_sha256: videoSha, shorts_sha256: shortsSha, shorts: shorts.map(short => ({ slug: short.slug, beats: short.scenes.length, chars: short.scenes.flatMap(scene => scene.narration).join("").length })) }, null, 2));
