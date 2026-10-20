// Offline metadata, source map, and concrete 9:16 crop plan; no audio/render/upload.
import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const dir = path.dirname(fileURLToPath(import.meta.url));
const base = "story-everyday-starbucks-x16";
const videoBytes = readFileSync(path.join(dir, "video.json"));
const video = JSON.parse(videoBytes);
const videoSha = createHash("sha256").update(videoBytes).digest("hex");
const src = {
  S1: "https://www.sec.gov/Archives/edgar/data/829224/000089102008000009/v36971exv99w1.htm",
  S2: "https://www.sec.gov/Archives/edgar/data/829224/000095013408012236/v41893exv99w1.htm",
  S3: "https://www.sec.gov/Archives/edgar/data/829224/000095013408021134/v50316e10vk.htm",
  S4: "https://www.sec.gov/Archives/edgar/data/829224/000095012309064772/v53316e10vk.htm",
  S5: "https://www.sec.gov/Archives/edgar/data/829224/000119312510266333/d10k.htm",
};
const rows = [[], []];
let active = -1;
for (const raw of readFileSync(path.join(dir, "drafts/shorts.md"), "utf8").split(/\r?\n/)) {
  const header = raw.match(/^## Short ([12]):/);
  if (header) { active = Number(header[1]) - 1; continue; }
  if (!/^x16s[12]\d{2}\s*\|/.test(raw)) continue;
  const parts = raw.split("|").map(item => item.trim());
  if (parts.length !== 4 || active < 0) throw new Error(`Malformed Short row: ${raw}`);
  const [id, refs, text, focus] = parts;
  if (text.length > 38 || !text || !focus || /Starbucks|星巴克|Schultz|舒茲|logo|readable/iu.test(focus)) throw new Error(`Invalid Short row: ${id}`);
  if (refs !== "editorial" && refs.split(",").some(ref => !src[ref])) throw new Error(`Unknown source: ${id}`);
  rows[active].push({ id, refs, text, focus });
}
for (const [si, short] of rows.entries()) {
  if (short.length !== 8) throw new Error(`Short ${si + 1} needs eight complete beats`);
  for (const [ri, row] of short.entries()) if (row.id !== `x16s${si + 1}${String(ri + 1).padStart(2, "0")}`) throw new Error(`Short ID out of order: ${row.id}`);
}
const lineToScene = new Map(video.scenes.flatMap(scene => scene.lines.map(line => [line.id, scene])));
// Each source is an actual illustrated scene, never a landscape stats card.
const anchors = [
  ["x160101", "x160103", "x160316", "x160309", "x160318", "x160312", "x160314", "x160329"],
  ["x160517", "x160602", "x160623", "x160604", "x160605", "x160609", "x160618", "x160623"],
];
const crops = [
  [656, 630, 680, 700, 610, 656, 690, 640],
  [656, 700, 635, 656, 690, 620, 656, 675],
];
const specs = [
  {
    titles: ["星巴克要關的店，七成才剛開？", "2008 星巴克關店名單：新店怎麼入選？"],
    headlines: ["約 600 家", "約七成很新", "新店先中？", "分母：入選店", "別算成全部", "看單店利潤", "還看未來回報", "問題是單店帳"],
    description: "2008 年 7 月 1 日，星巴克宣布約 600 家表現不佳的美國直營店關閉計畫，約七成入選店自 2006 財年起才開。七成的分母是被選中關閉的店，不是全美門市或所有新店；公司選店看單店利潤、預期回報及當地條件。畫面為匿名概念插畫，數字是後製字卡。正式長片網址待實際上傳後回填。",
    refs: ["S2"],
  },
  {
    titles: ["星巴克同店從負 6% 到正 7%，只靠關店？", "星巴克 2010 同店翻正，關店能獨拿功勞嗎？"],
    headlines: ["2009：−6%", "2010：+7%", "關店一招？", "同店：滿 13 月", "第 53 週已排除", "交易與客單價↑", "效率也改了", "不能獨算關店"],
    description: "星巴克美國同店銷售由 FY2009 的 −6% 變成 FY2010 的 +7%。同店只算開滿 13 個月的直營店，FY2010 百分比排除多出的第 53 週。該年美國交易次數、平均每筆金額均上升；年報也寫到店內效率與成本改善，無法把轉正獨歸關店。畫面為匿名概念插畫，數字是後製字卡。正式長片網址待實際上傳後回填。",
    refs: ["S4", "S5"],
  },
];
const beat = ["hook", "setup", "turn", "proof", "proof", "proof", "proof", "payoff"];
const shorts = rows.map((short, si) => ({
  schema_version: 2, slug: `${base}-short-${si + 1}`, format: "shorts", locale: "zh-TW", line: "cut", series: "illustrated",
  source: { slug: base }, synthetic_media: true, titles: specs[si].titles, description: specs[si].description,
  hashtags: ["星巴克", "品牌故事", "商業故事"], tags: ["Starbucks", "星巴克", "關店", "品牌故事"],
  links: specs[si].refs.map(ref => ({ label: `Starbucks ${ref} SEC 原件`, url: src[ref] })),
  scenes: short.map((row, ri) => {
    const scene = lineToScene.get(anchors[si][ri]);
    if (!scene || scene.template !== "shot") throw new Error(`Short ${si + 1} beat ${ri + 1} lacks an illustrated shot: ${anchors[si][ri]}`);
    return { beat: beat[ri], shot: scene.id, headline: specs[si].headlines[ri], narration: [row.text] };
  }),
}));
for (const short of shorts) {
  const chars = short.scenes.flatMap(scene => scene.narration).join("").length;
  if (chars < 105 || chars > 225) throw new Error(`${short.slug}: ${chars} characters outside 25–55s paper range`);
}
const bytes = JSON.stringify(shorts, null, 2) + "\n";
writeFileSync(path.join(dir, "shorts.json"), bytes);
const sha = createHash("sha256").update(bytes).digest("hex");
writeFileSync(path.join(dir, "shorts-script.md"), ["# X16 星巴克｜兩支獨立 Shorts 逐句稿", "", `主片 SHA-256：\`${videoSha}\`；Shorts SHA-256：\`${sha}\`。離線前製，未配音、剪輯、實測或發布；兩支均有自己的問題與答案，不需看過長片。正式 5 秒片頭／21 秒片尾只屬長片。`, "", ...shorts.flatMap((short, si) => [`## Short ${si + 1}｜${short.titles[0]}`, "", ...short.scenes.map((scene, ri) => `- \`${rows[si][ri].id}\` [${rows[si][ri].refs}] ${scene.narration[0]}（\`${scene.shot}\`）`), "", `原始資料：${short.links.map(link => `[${link.label}](${link.url})`).join("、")}`, ""])] .join("\n"));
writeFileSync(path.join(dir, "shorts-source-matrix.md"), ["# X16 星巴克｜Shorts 逐句作者來源矩陣", "", `\`shorts.json\` SHA-256：\`${sha}\`；\`video.json\` SHA-256：\`${videoSha}\`。作者標記，非獨立逐句審查 PASS。`, "", "| Short／拍 | 句 ID | 旁白 | 作者來源標記 |", "| --- | --- | --- | --- |", ...rows.flatMap((short, si) => short.map((row, ri) => `| ${si + 1}／${ri + 1} | \`${row.id}\` | ${row.text} | ${row.refs === "editorial" ? "提問／推理" : row.refs.replaceAll(",", "、")} |`)), ""].join("\n"));
writeFileSync(path.join(dir, "shorts-portrait-plan.md"), [
  "# X16 星巴克｜兩支 Shorts 的逐拍 9:16 裁切交接", "",
  `離線規劃，綁定主片 \`${videoSha}\`、Shorts \`${sha}\`。**尚無插畫、直式渲染或手機實測**。表內是實際要採用的第一版 9:16 裁切與原生文字覆蓋；生成後要逐鏡核對焦點，再在相同範圍內調整，不能把數字當作 AI 畫在圖上的文字。`, "",
  "主片畫布 1920×1080，每拍選一張真正的 `shot`，用 608×1080 視窗依表列 x 值裁切（y=0），等比輸出 1080×1920。圖片提示詞要求人物臉、手與主道具留在中央 x=656–1264；本表 x 的小幅移動用於把該拍道具放到直式中心，交接時仍須看原圖確認。若焦點落出裁切，先調 x（合法 0–1312），保不住才在同一整片預算內重畫。", "",
  "原生 9:16 文字與字幕安全區：畫布 1080×1920；所有 headline／大字／資料列置於 x=78–902、下緣 y≤1380；字幕條 x=80–900、y=1430–1595，任何字不進最下方操作區。後製字卡顯示品牌與精確數字，插畫無可讀字、店招、杯標或商標。360px 寬手機預覽須逐拍看對比、遮擋與兩行字幕，正式版再跑工具 `layout` 與 25–55 秒時長。", "",
  "| Short／拍 | 重用 shot | 608×1080 裁切左上角 | 直式焦點 | 原生 headline（在安全區） |",
  "| --- | --- | --- | --- | --- |",
  ...shorts.flatMap((short, si) => short.scenes.map((scene, ri) => `| ${si + 1}／${ri + 1} | \`${scene.shot}\` | \`x=${crops[si][ri]}, y=0\` | ${rows[si][ri].focus} | ${scene.headline} |`)),
  "", "Short 2 第 3／8 拍刻意重用同一張多塊拼圖的插畫，首拍裁左 x=635 呈現未合上，尾拍裁右 x=675 呈現整體；正式剪輯靠後製字卡與鏡頭推移區分，不宣稱兩張不同素材。兩支不套長片片頭片尾，繁中字幕由工具另出，不把字幕燒進長片畫面。", "",
].join("\n"));
console.log(JSON.stringify({ video_sha256: videoSha, shorts_sha256: sha, shorts: shorts.map(short => ({ slug: short.slug, beats: short.scenes.length, chars: short.scenes.flatMap(scene => scene.narration).join("").length })) }, null, 2));
