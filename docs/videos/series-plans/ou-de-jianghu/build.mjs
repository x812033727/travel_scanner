import { createHash } from "node:crypto";
import { readFileSync, writeFileSync, existsSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const directory = path.dirname(fileURLToPath(import.meta.url));
const json = (name) => JSON.parse(readFileSync(path.join(directory, name), "utf8"));
const bytes = (name) => readFileSync(path.join(directory, name));
const hash = (value) => createHash("sha256").update(value).digest("hex");
const encoded = (value) => `${JSON.stringify(value, null, 2)}\n`;
const cell = (value) => String(value ?? "").replaceAll("|", "／").replaceAll("\n", " ");
const plan = json("plan.json");
const setting = json("setting.json");
const seasons = Array.from({ length: plan.season_count }, (_, i) => json(`season-${String(i + 1).padStart(2, "0")}.json`));
const names = new Map(setting.characters.map((character) => [character.id, character.name]));
const list = (values) => values.length ? values.join("、") : "—";

function renderSetting() {
  const lines = [
    `# ${plan.title}｜設定集`, "", plan.logline, "",
    `分類：\`${plan.category}\`；畫風：\`${plan.style_preset}\`；第一、二季，每季${plan.episodes_per_chapter}集，開放結局（第三季以後見全系列路線圖）。`, "",
    "本檔由 setting.json 與 plan.json 產生，修改來源後執行 build.mjs。這是企劃文件，不代表後台核准或媒體完成。", "",
    `## 世界：${setting.world.name}`, "", setting.world.premise, "",
    ...setting.world.geography.map((place) => `- **${place.name}：**${place.description}`), "",
    "### 前史與揭露界線", "", setting.world.hidden_history, "", setting.world.reveal_policy, "",
    "## 核心規則", ""
  ];
  for (const rule of setting.rules) lines.push(`### ${rule.name}`, "", rule.rule, "", `戲劇代價：${rule.dramatic_cost}`, "");
  lines.push("## 勢力", "");
  for (const faction of setting.factions) lines.push(`### ${faction.name}`, "", `資源：${faction.resources}。`, "", `需要：${faction.need}。衝突：${faction.conflict}。`, "", `期末狀態：${faction.final_contribution}。`, "");
  lines.push("## 人物表", "");
  for (const character of setting.characters) {
    lines.push(`### ${character.name}（${character.id}）`, "", `${character.role}${character.age_at_start ? `；登場${character.age_at_start}歲` : ""}。`, "");
    for (const [key, label] of [["background", "背景"], ["ability", "能力"], ["limits", "限制"], ["arc", "成長與責任"], ["ending", "結局"]]) if (character[key]) lines.push(`**${label}：**${character[key]}`, "");
    lines.push(`**外觀基準：**${character.appearance}`, "");
  }
  lines.push("## 長線謎團", "", "| ID | 問題 | 埋下 | 收束 | 答案 |", "| --- | --- | ---: | ---: | --- |");
  for (const thread of setting.mysteries) lines.push(`| ${thread.id} | ${cell(thread.question)} | ${thread.introduced_in} | ${thread.resolved_in ?? "保留"} | ${cell(thread.answer)} |`);
  lines.push("", "中途 payoffs 可以是局部回收，並非整條謎團已解。最後收束集必須再次列出該謎團，對應真實劇情。", "", "## 敘事與畫面", "", ...setting.narrative_constraints.map((text) => `- ${text}`), "", setting.visual_style, "", "## 第二季結局", "", `不可逆的事：${setting.finale.permanent_costs.join("、")}。`, "", `保留給續期的謎團：${setting.finale.reserved_mysteries.join("、")}。`, "", `最後一句：**「${setting.finale.last_line}」**`, "");
  return `${lines.join("\n").trimEnd()}\n`;
}

function renderSeason(season) {
  const first = season.episodes[0].number;
  const last = season.episodes.at(-1).number;
  const lines = [`# 《${plan.title}》${season.title}`, "", `全劇第${first}～${last}集；時間：${season.time_span}`, "", `**主題：**${season.theme}`, "", `**核心衝突：**${season.core_conflict}`, "", "正文目標22分鐘；以下是兩段高張力與連貫狀態的細綱，未代替逐場台詞、分鏡或實測媒體。", ""];
  for (const episode of season.episodes) {
    lines.push(`## ${episode.number}｜${episode.title}`, "", episode.logline, "", `**開場：**${episode.hook}`, "", `**主要衝突：**${episode.conflict}`, "", `**中段轉折：**${episode.turn}`, "");
    for (const [index, beat] of episode.high_tension.entries()) lines.push(`**高張力${index + 1}（${beat.beat === "first_half" ? "前半" : "後半"}）：**${beat.event}`, "", `賭注：${beat.stakes}　後果：${beat.consequence}`, "");
    lines.push(`**${episode.closed_ending ? "結尾收束" : "結尾懸念"}（${episode.cliffhanger.type}）：**${episode.cliffhanger.text}`, "", `**延續後果：**${episode.consequence}`, "", `**埋下：**${list(episode.setups)}；**回收：**${list(episode.payoffs)}；**局部成果：**${list(episode.general_payoffs ?? [])}`, "", `**五段張力：**${episode.tension.join(" → ")}（企劃評分，非實測）`, "", `**出場：**${episode.characters.map((id) => names.get(id) ?? id).join("、")}；**場景：**${episode.locations.join("、")}`, "", `**主題句：**${episode.theme}`, "", "<details>", "<summary>本集連貫狀態</summary>", "");
    for (const [key, label] of [["time", "時間"], ["knowledge", "已知資訊"], ["character_state", "人物狀態"], ["evidence", "證據"], ["carry_forward", "後續接續"]]) lines.push(`- ${label}：${episode.state[key]}`);
    lines.push("", "</details>", "");
  }
  lines.push("## 本季收束", "", season.season_resolution, "", `接續：${season.season_hook}`, "");
  return `${lines.join("\n").trimEnd()}\n`;
}

function renderOutline() {
  const lines = [`# ${plan.title}｜兩季總綱`, "", plan.logline, "", `分類 anime，${plan.planned_episodes}集，第二季末開放結局。播出時段約30分鐘，正文約22分鐘；原定規格不縮為現行短漫劇。`, "", "## 升級與真相曲線", "", "| 季 | 集數 | 時間 | 主題 | 核心衝突 |", "| --- | --- | --- | --- | --- |"];
  for (const season of seasons) lines.push(`| ${season.number} | ${season.episodes[0].number}–${season.episodes.at(-1).number} | ${cell(season.time_span)} | ${cell(season.theme)} | ${cell(season.core_conflict)} |`);
  for (const season of seasons) {
    lines.push("", `## 《${plan.title}》${season.title}`, "", `收束：${season.season_resolution}`, "", `接續：${season.season_hook}`, "", "| 集 | 標題 | 推進 |", "| ---: | --- | --- |");
    for (const episode of season.episodes) lines.push(`| ${episode.number} | ${cell(episode.title)} | ${cell(episode.logline)} |`);
  }
  lines.push("", "## 第二季終局", "", `${setting.finale.summary} 保留給續期：${setting.finale.reserved_mysteries.join("、")}。最後一句：${setting.finale.last_line}`, "");
  return `${lines.join("\n").trimEnd()}\n`;
}

function continuity() {
  const episodes = seasons.flatMap((season) => season.episodes);
  const quote = (value) => `"${String(value).replaceAll('"', '""')}"`;
  const headers = ["episode", "title", "time", "knowledge", "character_state", "evidence", "carry_forward", "setups", "payoffs", "general_payoffs"];
  const rows = episodes.map((episode) => [episode.number, episode.title, ...["time", "knowledge", "character_state", "evidence", "carry_forward"].map((key) => episode.state[key]), episode.setups.join(";"), episode.payoffs.join(";"), (episode.general_payoffs ?? []).join(";")].map(quote).join(","));
  const lines = ["# 連貫性與伏筆帳", "", "各集狀態見 continuity.csv。保留已知與未知界線，角色不因觀眾已看過某場戲就自動知道答案。", "", "## 時間線", "", "| 季 | 經過月份 | 內容 |", "| --- | ---: | --- |"];
  for (const item of setting.chronology) lines.push(`| ${item.seasons.join("、")} | ${item.elapsed_months} | ${item.label} |`);
  lines.push("", `第一、二季主線共約${setting.chronology.reduce((sum, item) => sum + item.elapsed_months, 0)}個月。`, "", "## 謎團埋回實際位置", "", "| ID | 埋下或推進集 | 局部或最終回收集 | 最終收束 |", "| --- | --- | --- | ---: |");
  for (const thread of setting.mysteries) lines.push(`| ${thread.id} | ${episodes.filter((episode) => episode.setups.includes(thread.id)).map((episode) => episode.number).join("、")} | ${episodes.filter((episode) => episode.payoffs.includes(thread.id)).map((episode) => episode.number).join("、")} | ${thread.resolved_in ?? "保留"} |`);
  lines.push("", "## 不可逆的事", "", ...setting.finale.permanent_costs.map((item) => `- ${item}`), "", "## 製作界線", "", "這份帳追蹤的是企劃狀態，未核准劇本、未生成前情摘要、未讀取正式站狀態。人物外觀與能力限制以設定集為準。", "");
  return { csv: `${headers.join(",")}\n${rows.join("\n")}\n`, md: `${lines.join("\n").trimEnd()}\n` };
}

const output = new Map();
output.set("setting.md", renderSetting());
output.set("outline.md", renderOutline());
for (const season of seasons) output.set(`season-${String(season.number).padStart(2, "0")}.md`, renderSeason(season));
const outlineJson = { chapters: seasons.map((season) => ({ number: season.number, title: season.title, theme: season.theme, episodes: season.episodes.map(({ number, title, logline }) => ({ number, title, logline })) })) };
output.set("outline.json", encoded(outlineJson));
output.set("documents.json", encoded({
  schema_version: 1,
  stage: "planning",
  ready_for_import: false,
  category: plan.category,
  note: "文件形狀參考現有body_md/body_json；不是SeriesIn請求、不是核准紀錄，需先完成plan.json記錄的製作支援。",
  documents: [
    { kind: "setting", body_md: output.get("setting.md"), body_json: setting },
    { kind: "outline", body_md: output.get("outline.md"), body_json: outlineJson },
    ...seasons.map((season) => ({ kind: "chapter", chapter_number: season.number, body_md: output.get(`season-${String(season.number).padStart(2, "0")}.md`), body_json: season }))
  ]
}));
const state = continuity();
output.set("continuity.md", state.md);
output.set("continuity.csv", state.csv);
const sourceNames = ["authoring-contract.json", "plan.json", "setting.json", ...seasons.map((season) => `season-${String(season.number).padStart(2, "0")}.json`)];
const supportNames = ["README.md", "review.md", "build.mjs", "validate.mjs", "validate.test.mjs"].filter((name) => existsSync(path.join(directory, name)));
output.set("manifest.json", encoded({
  schema_version: 1,
  artifact_kind: plan.artifact_kind,
  slug: plan.slug,
  category: plan.category,
  episode_count: seasons.reduce((sum, season) => sum + season.episodes.length, 0),
  season_count: seasons.length,
  ready_for_import: false,
  admin_series_created: false,
  media_generated: false,
  published: false,
  source_files: Object.fromEntries(sourceNames.map((name) => [name, hash(bytes(name))])),
  support_files: Object.fromEntries(supportNames.map((name) => [name, hash(bytes(name))])),
  generated_files: Object.fromEntries([...output].map(([name, value]) => [name, hash(value)]))
}));

const check = process.argv.includes("--check");
const stale = [];
for (const [name, value] of output) {
  const target = path.join(directory, name);
  if (check) {
    if (!existsSync(target) || readFileSync(target, "utf8") !== value) stale.push(name);
  } else writeFileSync(target, value, "utf8");
}
if (stale.length) {
  process.stderr.write(`Generated files differ from source: ${stale.join(", ")}\nRun node docs/videos/series-plans/ou-de-jianghu/build.mjs\n`);
  process.exitCode = 1;
} else process.stdout.write(`${check ? "Checked" : "Built"} ${output.size} generated files; ${seasons.length} seasons, ${seasons.reduce((sum, season) => sum + season.episodes.length, 0)} episodes.\n`);
