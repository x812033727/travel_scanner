// Builds two independent Shorts and their paper-only 9:16 assembly plan. No provider calls.
import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { episodeShortsProblems } from "../../../tools/video/shorts/episode.mjs";

const dir = path.dirname(fileURLToPath(import.meta.url));
const main = JSON.parse(readFileSync(path.join(dir, "video.json"), "utf8"));
const lineScene = new Map(main.scenes.flatMap(scene => scene.lines.map(line => [line.id, scene])));
const raw = readFileSync(path.join(dir, "drafts/shorts.md"), "utf8");
const groups = [[], []];
let current = -1;
for (const line of raw.split(/\r?\n/)) {
  const heading = line.match(/^## Short ([12])｜/);
  if (heading) { current = Number(heading[1]) - 1; continue; }
  const match = line.match(/^- `(x13s[12]\d{2})` (.*?)〔([^〕]+)〕$/);
  if (match && current >= 0) groups[current].push({ id: match[1], text: match[2], refs: [...match[3].matchAll(/S([1-9])/g)].map(([, n]) => `S${n}`) });
}
if (groups[0].length !== 9 || groups[1].length !== 7) throw new Error("Expected independent 9/7-beat Shorts scripts");
const shots = [
  ["x130401", "x130405", "x130406", "x130408", "x130409", "x130601", "x130603", "x130605", "x130619"],
  ["x130611", "x130607", "x130603", "x130605", "x130612", "x130614", "x130615"],
];
const headlines = [
  ["部分內容沖銷", "若干節目關閉", "全面退場？", "影片供給仍在", "不同內容", "新方案啟動", "合格創作者", "會員觀看", "並未全面退出"],
  ["廣告欄播客成本", "真省多少？", "合格影片", "Premium 會員", "成本換欄", "拆分未知", "不能全算省下"],
];
const numericOverlays = [
  { beat: 0, big: "€30m", body: ["2023 Q2｜部分播客內容資產"], note: "S3 SEC｜並非全部播客投資" },
  { beat: 0, big: "−€21m", body: ["2025 Q2 同比｜Ad-Supported"], note: "S7 SEC｜非全平台播客總支出" },
];
const beats = [
  ["hook", "turn", "proof", "proof", "proof", "proof", "proof", "payoff", "payoff"],
  ["hook", "turn", "proof", "proof", "proof", "proof", "payoff"],
];
const metadata = [
  {
    titles: ["Spotify 關閉若干播客，真的全面退出了嗎？", "Spotify 沖銷 €30m 播客內容，後來還做播客嗎？"],
    description: "2023 Q2 Spotify 沖銷 €30m 的部分播客內容資產，也在同季關閉若干節目。2023-07-25 公告提到超過十萬檔可用影片播客；這不是被關節目的新身分。2025 年 Partner Program 又讓合格影片播客創作者依觀看表現取得給付；部分市場 Premium 會員觀看這類影片時沒有動態插播廣告。這些動作回答的是有無全面退出，不是單一節目去向。匿名概念插畫；精確數字後製排字。正式長片網址待真實上傳後回填。",
    links: [
      { label: "Spotify S3 SEC 原件", url: "https://www.sec.gov/Archives/edgar/data/1639920/000163992023000010/spot-20230630x6xk.htm" },
      { label: "Spotify S9 SEC 原件", url: "https://www.sec.gov/Archives/edgar/data/1639920/000114036123035965/brhc20056303_ex99-1.htm" },
      { label: "Spotify S7 SEC 原件", url: "https://www.sec.gov/Archives/edgar/data/1639920/000163992025000012/spot-20250630x6xk.htm" },
    ],
  },
  {
    titles: ["Spotify 廣告欄播客成本少 €21m，真省了多少？", "Spotify 2025 廣告欄播客成本換欄：省錢還是改列？"],
    description: "Spotify 2025 Q2 的 Ad-Supported 業務播客成本同比少 €21m，但提供給 Premium 會員的新影片觀看體驗，其相關播客成本開始列到 Premium，其餘仍在 Ad-Supported。報表沒有拆出真節省與分類變動的比例，不能把 €21m 全算成播客省下的錢。匿名概念插畫；精確數字由後製排字。正式長片網址待真實上傳後回填。",
    links: [{ label: "Spotify S7 SEC 原件", url: "https://www.sec.gov/Archives/edgar/data/1639920/000163992025000012/spot-20250630x6xk.htm" }],
  },
];
const shorts = groups.map((lines, index) => ({
  schema_version: 2,
  slug: `story-everyday-spotify-x13-short-${index + 1}`,
  format: "shorts", locale: "zh-TW", line: "cut", series: "illustrated",
  source: { slug: main.slug }, synthetic_media: true,
  titles: metadata[index].titles, description: metadata[index].description,
  hashtags: ["Spotify", "品牌故事", "播客"],
  tags: ["Spotify", "播客", "品牌故事", "商業故事"],
  links: metadata[index].links,
  scenes: lines.map((line, beatIndex) => {
    const source = lineScene.get(shots[index][beatIndex]);
    if (!source) throw new Error(`Short source scene missing for ${line.id}: ${shots[index][beatIndex]}`);
    if (source.template !== "shot") throw new Error(`Short source must be a shot for ${line.id}: ${source.id} is ${source.template}`);
    const overlay = numericOverlays[index].beat === beatIndex ? numericOverlays[index] : null;
    return { beat: beats[index][beatIndex], shot: source.id, headline: headlines[index][beatIndex], ...(overlay ? { big: overlay.big, body: overlay.body, note: overlay.note } : {}), narration: [line.text] };
  }),
}));
const productionProblems = episodeShortsProblems(shorts, main);
if (productionProblems.length) throw new Error(`Episode Shorts production check failed:\n${productionProblems.join("\n")}`);
const bytes = JSON.stringify(shorts, null, 2) + "\n";
writeFileSync(path.join(dir, "shorts.json"), bytes);
const sha = createHash("sha256").update(bytes).digest("hex");
const mdLines = ["# X13 Spotify｜兩支獨立 Shorts 逐句稿 v10", "", `\`shorts.json\` SHA-256：\`${sha}\`。未配音、生成插畫、直式輸出或手機驗收；兩支各自從頭提出問題並回答。`];
const sources = ["# X13 Spotify｜Shorts 作者來源索引", "", `\`shorts.json\` SHA-256：\`${sha}\`。作者標記，待獨立來源審查。`, "", "| 句 ID | 旁白 | 作者來源 |", "| --- | --- | --- |"];
for (const [i, lines] of groups.entries()) {
  mdLines.push("", `## Short ${i + 1}`, "");
  for (const row of lines) {
    mdLines.push(`- \`${row.id}\` ${row.text}`);
    sources.push(`| \`${row.id}\` | ${row.text} | ${row.refs.join("、")} |`);
  }
}
writeFileSync(path.join(dir, "shorts-script.md"), mdLines.join("\n") + "\n");
writeFileSync(path.join(dir, "shorts-source-matrix.md"), sources.join("\n") + "\n");
const plan = [
  "# X13 Spotify｜兩支 Shorts 9:16 逐拍構圖計畫 v10",
  "",
  "這是**尚未生成畫面**的原生直式重構規格，不是裁切或手機 QA 通過收據。每拍 `shot` 均須是長片真正的 `shot` 影格；兩張長片 `stats` 不送入 Shorts 影格管線。數字由 Shorts `big` 欄位在 1080×1920 直式卡原生排字，場景底圖另取有效的匿名插畫。編譯器直接呼叫 `episodeShortsProblems(shorts, video)` 防止再引用 `stats`。",
  "",
  "每拍有效插畫先從 1920×1080 取 x=656–1264 的 608×1080 中央窗，再重排為 1080×1920。Short 1 關閉音訊格與開放影片格以兩個不同中央架位呈現，不畫成同一檔節目轉型；Short 2 廣告與會員帳本上下堆疊，先後鏡頭保持同一色序。Shorts 卡片工具原生文字內容區 x=80–900、y=258–1378；可關閉繁中字幕區 x=80–900、y=1430–1595；片尾控制區 y≥1640 不放關鍵字。每拍在 360px 寬手機畫面檢查臉、手、主物、字與控制列不互相遮擋。",
  "",
  "兩張原生數字卡：Short 1 第 1 拍以 `x130401` 的有效匿名內容架插畫作背景，`headline` 為「部分內容沖銷」、`big` 為 **€30m**，47px `body` 放「2023 Q2｜部分播客內容資產」，`note` 放 S3 SEC 及非全體範圍；先留下是否全面退出的問題。Short 2 第 1 拍以 `x130611` 的有效服務帳插畫作背景，`headline` 為「廣告欄播客成本」、`big` 為 **−€21m**，47px `body` 放「2025 Q2 同比｜Ad-Supported」，`note` 放 S7 SEC 與非全平台總支出範圍；第一句旁白說明廣告欄同比變動，不提前回答『真省』或 Premium 搬移。`big` 用 Shorts 工具的 168px 字級、`headline` 88px；`note` 28px 只輔助來源，關鍵口徑另由頭條與旁白交代。原生排字後仍須以 360px 畫面實測可讀性。",
  "",
  "| Short／拍 | 長片有效 shot | 焦點／內容（直接取自來源鏡頭提示） | 橫版 x 起點 | 直式原生頭條／大數字 |",
  "| --- | --- | --- | ---: | --- |",
];
for (const [i, episode] of shorts.entries()) for (const [j, scene] of episode.scenes.entries()) {
  const original = main.scenes.find(item => item.id === scene.shot);
  const focus = original.data.prompt.split(". ")[0];
  plan.push(`| ${i + 1}/${j + 1} | \`${scene.shot}\` | ${focus.replaceAll("|", "\\|")} | 656 | ${scene.headline}${scene.big ? `／**${scene.big}**` : ""} |`);
}
plan.push("", "Short 1 的九拍從部分內容縮編追到新影片合作，Short 2 的七拍解釋費用分類和不能全算節省。兩支各需正式 TTS 實測 25–55 秒、重新排版文字／CC、核 9:16 真圖與音樂授權；不得以這份紙面規格冒稱成片。", "");
writeFileSync(path.join(dir, "shorts-portrait-plan.md"), plan.join("\n"));
console.log(JSON.stringify({ shorts_sha256: sha, beats: shorts.map(item => item.scenes.length), episode_shorts_problems: productionProblems }, null, 2));
