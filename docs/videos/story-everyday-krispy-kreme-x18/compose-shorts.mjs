// Offline Shorts metadata, author source map, and provisional 9:16 plan. No rendering or upload.
import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const dir = path.dirname(fileURLToPath(import.meta.url));
const base = "story-everyday-krispy-kreme-x18";
const videoBytes = readFileSync(path.join(dir, "video.json"));
const video = JSON.parse(videoBytes);
const videoSha = createHash("sha256").update(videoBytes).digest("hex");
const src = {
  S1: {
    url: "https://www.sec.gov/Archives/edgar/data/1857154/000185715424000029/exhibit991newsrelease.htm",
    http: 200,
    bytes: 9299,
    sha: "aa75ec80af521f5c4d541424af6bdecd8503e004f646a10f6df2d5bcb2096b31",
  },
  S5: {
    url: "https://www.sec.gov/Archives/edgar/data/1857154/000185715425000102/a991pressrelease-june2025.htm",
    http: 200,
    bytes: 8772,
    sha: "b9489592ff52b75cd8fb0f1a8e55aac9bd8e6342ef314c4c8737f2f838d1da4c",
  },
  S6: {
    url: "https://www.sec.gov/Archives/edgar/data/1857154/000185715425000125/exh991q2pressrelease2025.htm",
    http: 200,
    bytes: 539598,
    sha: "de082d3fde67cf3ac947868785751a0a57f07a719b917fe8f8983a6a5da64e1f",
  },
  S7: {
    url: "https://www.sec.gov/Archives/edgar/data/1857154/000185715425000138/exh991q3pressrelease2025.htm",
    http: 200,
    bytes: 594995,
    sha: "806253d305c7acc3277e07b872133f66074a597f24b977044e98f22d54da7432",
  },
};

const rows = [[], []];
let active = -1;
for (const raw of readFileSync(path.join(dir, "drafts/shorts.md"), "utf8").split(/\r?\n/)) {
  const header = raw.match(/^## Short ([12]):/);
  if (header) { active = Number(header[1]) - 1; continue; }
  if (!/^x18s[12]\d{2}\s*\|/.test(raw)) continue;
  const parts = raw.split("|").map(part => part.trim());
  if (parts.length !== 4 || active < 0) throw new Error(`Malformed Short row: ${raw}`);
  const [id, refsText, narration, focus] = parts;
  const refs = refsText.split(",");
  if (!narration || [...narration].length > 38 || !focus || refs.some(ref => ref !== "editorial" && !src[ref])) throw new Error(`Invalid Short row: ${id}`);
  if (/Krispy|McDonald|logo|brand|readable|trademark/iu.test(focus)) throw new Error(`Branded visual focus: ${id}`);
  rows[active].push({ id, refs: refs.filter(ref => ref !== "editorial"), narration, focus });
}
for (const [si, short] of rows.entries()) {
  if (short.length !== 8) throw new Error(`Short ${si + 1} needs eight complete beats`);
  for (const [ri, row] of short.entries()) {
    const expected = `x18s${si + 1}${String(ri + 1).padStart(2, "0")}`;
    if (row.id !== expected) throw new Error(`Short ID out of order: ${row.id}, expected ${expected}`);
  }
}

const beats = ["hook", "setup", "turn", "proof", "proof", "proof", "proof", "payoff"];
const specs = [
  {
    titles: ["Krispy Kreme 試點需求超預期，為何還退出麥當勞？", "160 家試點超預期，2,400 家卻提前停？"],
    headlines: ["試點超預期？", "肯塔基 160 家", "計畫 2026 全國", "每天送三款", "約 2,400 家", "麥當勞說達標", "成本對不上需求", "2025/7/2 終止"],
    description: "2024 年 3 月的兩家公司聯合公告稱，肯塔基 160 家麥當勞試點的需求超出預期，宣布逐步擴張，目標至 2026 年底涵蓋全美參與門市；這是當時的計畫，並未完成。2025 年 6 月的聯合公告稱合作約達 2,400 家麥當勞，麥當勞表示符合自己與加盟主期待；Krispy Kreme 則表示無法把成本調整到符合單店需求，雙方決定於 7 月 2 日終止。畫面是匿名概念插畫，精確數字由後製排字。正式長片網址待實際上傳後回填。",
    refs: ["S1", "S5"],
  },
  {
    titles: ["合作已終止，財報怎麼還算進 2,400 家麥當勞？", "差三天的季末：店數與獲利怎麼讀？"],
    headlines: ["店數還含麥當勞？", "Q2 截至 6/29", "全球 18,113 點", "7/2 才終止", "Q3 全球點位", "差額不能全扣", "改善因素之一", "仍淨損 US$20.1m"],
    description: "Krispy Kreme 的 2025 年第二季在 6 月 29 日結束，全球 18,113 個銷售點當時仍含約 2,400 家麥當勞；合作 7 月 2 日才正式終止。第三季全球銷售點為 14,851，兩季差額不可全當成麥當勞店數變化。公司把移除合作成本列為調整後 EBITDA 利潤率改善的多項因素之一，但第三季 GAAP 淨損仍為 US$20.1m。概念插畫與文字卡不是現場紀錄；正式長片網址待實際上傳後回填。",
    refs: ["S5", "S6", "S7"],
  },
];
const crops = [[656, 640, 672, 660, 635, 656, 680, 650], [650, 675, 656, 645, 670, 656, 685, 640]];

const used = new Set();
const shorts = rows.map((short, si) => ({
  schema_version: 2,
  slug: `${base}-short-${si + 1}`,
  format: "shorts",
  locale: "zh-TW",
  line: "cut",
  series: "illustrated",
  source: { slug: base },
  synthetic_media: true,
  titles: specs[si].titles,
  description: specs[si].description,
  hashtags: ["KrispyKreme", "品牌故事", "商業故事"],
  tags: ["Krispy Kreme", "麥當勞", "品牌故事", "甜甜圈"],
  links: specs[si].refs.map(ref => ({ label: `Krispy Kreme ${ref} SEC 原件`, url: src[ref].url })),
  scenes: short.map((row, ri) => {
    const matches = video.scenes.filter(scene => scene.template === "shot" && scene.data?.prompt?.toLowerCase().includes(row.focus.toLowerCase()));
    if (matches.length !== 1) throw new Error(`${row.id}: expected one matching main-film shot for focus '${row.focus}', found ${matches.length}`);
    const scene = matches[0];
    if (used.has(scene.id)) throw new Error(`${row.id}: main-film shot ${scene.id} already reused in a Short`);
    used.add(scene.id);
    return {
      beat: beats[ri], shot: scene.id, headline: specs[si].headlines[ri], narration: [row.narration],
      ...(si === 1 && ri === 4 ? { big: "14,851", note: "2025-09-28｜全球銷售點；所有通路" } : {}),
    };
  }),
}));
for (const short of shorts) {
  const chars = short.scenes.flatMap(scene => scene.narration).join("").length;
  if (chars < 125 || chars > 240) throw new Error(`${short.slug}: ${chars} characters outside 25–55-second paper range at 300 cpm`);
}
const bytes = JSON.stringify(shorts, null, 2) + "\n";
writeFileSync(path.join(dir, "shorts.json"), bytes);
const shortsSha = createHash("sha256").update(bytes).digest("hex");
writeFileSync(path.join(dir, "shorts-script.md"), [
  "# X18 Krispy Kreme｜兩支獨立 Shorts 逐句稿", "",
  `主片 SHA-256：\`${videoSha}\`；Shorts SHA-256：\`${shortsSha}\`。離線前製，未配音、剪輯、實測或發布；兩支各自完整，均不使用主片 5 秒／21 秒官方書擋。`, "",
  ...shorts.flatMap((short, si) => [
    `## Short ${si + 1}｜${short.titles[0]}`, "",
    ...short.scenes.map((scene, ri) => `- \`${rows[si][ri].id}\` ${scene.narration[0]}（\`${scene.shot}\`）`), "",
    `原始資料：${short.links.map(link => `[${link.label}](${link.url})`).join("、")}`, "",
  ]),
].join("\n"));
writeFileSync(path.join(dir, "shorts-source-matrix.md"), [
  "# X18 Krispy Kreme｜Shorts 逐句作者來源矩陣", "",
  `\`shorts.json\` SHA-256：\`${shortsSha}\`；\`video.json\` SHA-256：\`${videoSha}\`。作者標記，不是獨立審核 PASS。`, "",
  "| 代碼 | SEC 原件 | HTTP／原始 bytes | SHA-256 |", "| --- | --- | ---: | --- |",
  ...Object.entries(src).map(([key, item]) => `| ${key} | [原件](${item.url}) | ${item.http}／${item.bytes.toLocaleString("en-US")} | \`${item.sha}\` |`), "",
  "| Short／拍 | 句 ID | 旁白 | 作者來源 |", "| --- | --- | --- | --- |",
  ...rows.flatMap((short, si) => short.map((row, ri) => `| ${si + 1}／${ri + 1} | \`${row.id}\` | ${row.narration} | ${row.refs.length ? row.refs.join("、") : "敘事提問／依原件推理"} |`)), "",
  "S1 的全國鋪貨與 2026 年底是當時**計畫**，不是達成事實；S5 的 McDonald's 達標評述和 Krispy Kreme 成本評述是各自立場，不能互換。S6 在 6 月 29 日結季；S5 的合作終止日是 7 月 2 日。S7 的 Q3 全球點位差額含其他開閉點位，利潤率改善也有生產力、SG&A 與保險理賠等因素；Q3 仍有 GAAP 淨損。", "",
].join("\n"));
writeFileSync(path.join(dir, "shorts-portrait-plan.md"), [
  "# X18 Krispy Kreme｜兩支 Shorts 的逐拍 9:16 規劃", "",
  `離線前製，綁定主片 \`${videoSha}\` 與 Shorts \`${shortsSha}\`。目前沒有插畫、直式輸出或手機檢查，以下裁切需出圖後逐拍核對焦點。`, "",
  "每拍從一張不同的主片 1920×1080 插畫 `shot` 取 608×1080 視窗，按表列 x、y=0 裁切，再等比輸出 1080×1920；原畫面提示詞要求焦點落在中央 608px 走廊。若焦點出框，可在合法 x=0–1312 中移動；保不住才於 US$25 整片上限內重畫。所有品牌名、年份與數字均以後製原生字卡排版，不請 image-01 畫字。", "",
  "直式文字安全區：畫布 1080×1920；headline x=78–902、下緣 y≤1380；字幕 x=80–900、y=1430–1595；底部操作區保留。Short 2 第五拍重用 Q3 地圖 `shot`，14,851 由 Short 原生 `big` 疊字、日期與全球通路分母由 `note` 疊字，不重用主片 `stats` 卡。產出後於 360px 寬手機逐拍看字卡、字幕與甜甜圈／帳頁焦點，測兩支均為 25–55 秒。Shorts 不套長片片頭片尾，也不預填虛構 watch URL。", "",
  "| Short／拍 | 重用主片 shot | 608×1080 左上角 | 直式焦點 | 原生 headline／big／note |", "| --- | --- | --- | --- | --- |",
  ...shorts.flatMap((short, si) => short.scenes.map((scene, ri) => `| ${si + 1}／${ri + 1} | \`${scene.shot}\` | \`x=${crops[si][ri]}, y=0\` | ${rows[si][ri].focus} | ${[scene.headline, scene.big, scene.note].filter(Boolean).join("／")} |`)),
  "", "焦點與主片 shot prompt 在編譯時逐字核對，正式裁切在真實插畫生成後才驗。", "",
].join("\n"));
console.log(JSON.stringify({ video_sha256: videoSha, shorts_sha256: shortsSha, shorts: shorts.map(short => ({ slug: short.slug, beats: short.scenes.length, chars: short.scenes.flatMap(scene => scene.narration).join("").length })) }, null, 2));
