// Builds two independent Shorts and their paper-only 9:16 assembly plan. No provider calls.
import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

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
  ["x130101", "x130103", "x130202", "x130203", "x130104", "x130214", "x130210", "x130204", "x130215"],
  ["x130611", "x130610", "x130603", "x130605", "x130608", "x130614", "x130615"],
];
const headlines = [
  ["兩天兩筆", "為何兩種？", "創作工具", "節目製作", "€308m 對價", "非純現金", "當時的期待", "兩端供給", "回本另算"],
  ["廣告欄 −€21m", "真省多少？", "合格影片", "Premium 會員", "成本換欄", "拆分未知", "不能全算省下"],
];
const beats = [
  ["hook", "turn", "proof", "proof", "proof", "proof", "proof", "payoff", "payoff"],
  ["hook", "turn", "proof", "proof", "proof", "proof", "payoff"],
];
const metadata = [
  {
    titles: ["Spotify 連兩天買播客：一家做節目，一家做什麼？", "Anchor＋Gimlet：Spotify 買進哪兩種能力？"],
    description: "2019 年 2 月，Spotify 連兩天收購 Anchor 與 Gimlet：前者提供播客創作／發行工具，後者製作節目。兩案合計 €308m 是收購對價，包含股份獎酬，不能當成全部當天付現；當時的商業化是公司期待，不等於回本證明。匿名概念插畫；品牌與數字由後製排字。正式長片網址待真實上傳後回填。",
    links: [{ label: "Spotify S1 SEC 原件", url: "https://www.sec.gov/Archives/edgar/data/1639920/000156459019013731/ck0001639920-6k_20190429.htm" }],
  },
  {
    titles: ["Spotify 播客成本少 €21m，真省了多少？", "Spotify 2025 播客成本換欄：省錢還是改列？"],
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
    return { beat: beats[index][beatIndex], shot: source.id, headline: headlines[index][beatIndex], narration: [line.text] };
  }),
}));
const bytes = JSON.stringify(shorts, null, 2) + "\n";
writeFileSync(path.join(dir, "shorts.json"), bytes);
const sha = createHash("sha256").update(bytes).digest("hex");
const mdLines = ["# X13 Spotify｜兩支獨立 Shorts 逐句稿 v6", "", `\`shorts.json\` SHA-256：\`${sha}\`。未配音、生成插畫、直式輸出或手機驗收；兩支各自從頭提出問題並回答。`];
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
  "# X13 Spotify｜兩支 Shorts 9:16 逐拍構圖計畫 v6",
  "",
  "這是**尚未生成畫面**的原生直式重構規格，不是裁切或手機 QA 通過收據。長片來源插畫要求中央 608px 焦點，但輸出仍須逐鏡驗真圖；來源數字卡在直式畫面重新由程式排字。",
  "",
  "每拍輸入為 1920×1080，若是插畫先取 x=656–1264 的 608×1080 中央窗，再重排為 1080×1920。Short 1 兩種能力卡採中央上下堆疊，不放在兩側；Short 2 廣告與會員帳本也上下堆疊，先後鏡頭保持同一色序。若是統計卡直接原生繪製 1080×1920，不裁橫版字。頭條安全區 x=78–902、y≤1380；可關閉繁中字幕預留 x=80–900、y=1430–1595；每拍在 360px 寬手機畫面檢查臉、手、主物、字與控制列不互相遮擋。",
  "",
  "| Short／拍 | 長片來源 | 焦點／內容（直接取自來源鏡頭提示） | 橫版 x 起點 | 直式原生頭條 |",
  "| --- | --- | --- | ---: | --- |",
];
for (const [i, episode] of shorts.entries()) for (const [j, scene] of episode.scenes.entries()) {
  const original = main.scenes.find(item => item.id === scene.shot);
  const focus = original.template === "stats" ? `直式原生數字卡：${original.data.title}` : original.data.prompt.split(". ")[0];
  plan.push(`| ${i + 1}/${j + 1} | \`${scene.shot}\` | ${focus.replaceAll("|", "\\|")} | ${original.template === "stats" ? "原生" : 656} | ${scene.headline} |`);
}
plan.push("", "Short 1 的九拍以兩案能力和收購對價收束，Short 2 的七拍以費用分類和不能全算節省收束。兩支各需正式 TTS 實測 25–55 秒、重新排版文字／CC、核 9:16 真圖與音樂授權；不得以這份紙面規格冒稱成片。", "");
writeFileSync(path.join(dir, "shorts-portrait-plan.md"), plan.join("\n"));
console.log(JSON.stringify({ shorts_sha256: sha, beats: shorts.map(item => item.scenes.length), shot_ids_resolve: true }, null, 2));
