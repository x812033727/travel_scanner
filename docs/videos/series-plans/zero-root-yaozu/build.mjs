#!/usr/bin/env node
// Renders the readable files of the 長燈村 plan from its JSON sources: outline.md, setting.md,
// season-NN.md and episodes.csv. Never edit those by hand; edit the JSON and run this again.
//   node docs/videos/series-plans/zero-root-yaozu/build.mjs [--check]
import { existsSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const read = (name) => JSON.parse(readFileSync(join(here, name), "utf8"));
const pad = (n) => String(n).padStart(2, "0");
const setting = read("setting.json");
const outline = read("outline.json");
const tones = Object.fromEntries(setting.tones.map((tone) => [tone.id, tone.name]));
const names = Object.fromEntries([...setting.characters, ...setting.beasts].map((row) => [row.id, row.name]));
const CLIFF = { danger: "危機", reveal: "揭露", choice: "抉擇", reversal: "反轉", emotion: "情感" };
const HOOK = { question: "提問", danger: "危機", image: "畫面", line: "台詞", reversal: "反轉" };
const ARC = { wins: "贏", suffers: "受挫", mixed: "有得有失" };
const SAT = { face_slap: "打臉", identity_reveal: "身份揭露", counter_kill: "反殺", level_up: "升級", first_clear: "首通", betrayer_punished: "背叛者遭報", villain_humbled: "反派低頭", hidden_power: "藏拙露鋒", public_vindication: "當眾平反", rescue: "及時救場", reversal: "反轉" };
const BEAT = { opening: "開場", first_half: "前半", midpoint: "中段", second_half: "後半", ending: "結尾" };
const GENERATED = "<!-- 由 build.mjs 從 JSON 產生，不要手改。 -->\n\n";

function settingMd() {
  const lines = [`# ${setting.title}｜設定集`, "", setting.logline, "", "## 前提", "", setting.premise, "", "## 世界", ""];
  for (const region of setting.world.regions) lines.push(`- **${region.name}**：${region.what}`);
  lines.push("", "## 規則與代價", "", "| 規則 | 內容 | 代價 |", "| --- | --- | --- |");
  for (const rule of setting.world.rules) lines.push(`| ${rule.name} | ${rule.rule} | ${rule.cost} |`);
  lines.push("", "## 勢力", "");
  for (const faction of setting.world.factions) lines.push(`- **${faction.name}**：${faction.what}`);
  lines.push("", "## 人物", "", "| id | 名字 | 身分 | 外貌（真人提示詞） | 聲音 | 走向 |", "| --- | --- | --- | --- | --- | --- |");
  for (const row of setting.characters) lines.push(`| \`${row.id}\` | ${row.name} | ${row.role} | ${row.appearance} | ${row.tts ? row.tts.voice.replace("gemini:", "") : "未定"} | ${row.arc} |`);
  lines.push("", "## 神獸", "");
  for (const beast of setting.beasts) lines.push(`- **${beast.name}**（${beast.source}，第 ${beast.season} 季）：${beast.appearance}`);
  lines.push("", "## 長線謎團", "", "| id | 問題 | 埋 | 揭 | 答案 |", "| --- | --- | --- | --- | --- |");
  for (const row of setting.mysteries) lines.push(`| ${row.id} | ${row.question} | S${row.setup_season} | S${row.reveal_season} | ${row.answer} |`);
  lines.push("", "## 調性", "");
  for (const tone of setting.tones) lines.push(`- **${tone.name}**：${tone.how}`);
  lines.push("", "## 不黃標（廣告友善）", "", setting.advertiser_safety.goal, "");
  for (const rule of setting.advertiser_safety.rules) lines.push(`- ${rule}`);
  lines.push("", "## 顏值", "", setting.glamour.goal, "", "要：", "");
  for (const rule of setting.glamour.do) lines.push(`- ${rule}`);
  lines.push("", "不要：", "");
  for (const rule of setting.glamour.dont) lines.push(`- ${rule}`);
  lines.push("", "## 畫面", "", setting.visual_bible.look, "", `奇觀：${setting.visual_bible.money_shots.join("；")}`, "", `母題：${setting.visual_bible.motifs.join("；")}`, "");
  return GENERATED + lines.join("\n");
}

function outlineMd() {
  const lines = [`# ${setting.title}｜十季總綱`, "", outline.arc, "", `**結局**：${outline.ending}`, ""];
  for (const season of outline.seasons) {
    lines.push(`## 第 ${season.number} 季《${season.title}》（第 ${season.episodes[0]}–${season.episodes[1]} 集）`, "", `主題：${season.theme}`, "", `開季：${season.start_state}`, "", `季末：${season.end_state}`, "");
    for (const chapter of season.chapters) {
      lines.push(`### 篇章 ${chapter.number}〈${chapter.title}〉第 ${chapter.episodes[0]}–${chapter.episodes[1]} 集｜${chapter.tones.map((id) => tones[id]).join("、")}`, "", chapter.beats, "", `- 短線：${chapter.threads.join("；")}`, `- 篇章結尾：${chapter.end}`, `- 奇觀：${chapter.spectacle}`, "");
    }
  }
  return GENERATED + lines.join("\n");
}

function seasonMd(season) {
  const plan = outline.seasons.find((row) => row.number === season.number);
  const lines = [`# 第 ${season.number} 季《${season.title}》逐集細綱`, "", `主題：${season.theme}`, "", `開季：${season.start_state}`, "", `季末：${season.end_state}`, ""];
  if (season.guest_cast?.length) {
    lines.push("## 本季客串", "", "| id | 名字 | 身分 | 外貌 |", "| --- | --- | --- | --- |");
    for (const guest of season.guest_cast) lines.push(`| \`${guest.id}\` | ${guest.name} | ${guest.role ?? ""} | ${guest.appearance} |`);
    lines.push("");
  }
  if (season.threads?.length) {
    lines.push("## 本季短線", "", "| id | 懸念 | 埋 | 收 |", "| --- | --- | --- | --- |");
    for (const thread of season.threads) lines.push(`| ${thread.id} | ${thread.question} | ${thread.setup_episode ?? ""} | ${thread.payoff_episode ?? ""} |`);
    lines.push("");
  }
  const guests = Object.fromEntries((season.guest_cast ?? []).map((row) => [row.id, row.name]));
  for (const chapter of plan.chapters) {
    lines.push(`## 篇章 ${chapter.number}〈${chapter.title}〉`, "");
    for (const ep of season.episodes.filter((row) => row.chapter === chapter.number)) {
      lines.push(
        `### 第 ${ep.number} 集（本季第 ${ep.season_episode} 集）〈${ep.title}〉｜${ep.duration_s} 秒`,
        "",
        `**上架標題**：${ep.youtube_title}`,
        "",
        `- 一句話：${ep.logline}`,
        `- 前 3 秒（${HOOK[ep.hook_type]}）：${ep.hook}`,
        `- 中段鉤子：${ep.mid_hook}`,
        `- 衝突：${ep.conflict}`,
        `- 轉折：${ep.turn}`,
        `- 爽點：${ep.satisfaction.map((beat) => `${BEAT[beat.beat]}・${SAT[beat.type]}${beat.what ? `（${beat.what}）` : ""}`).join("、")}`,
        `- 結尾（${CLIFF[ep.cliffhanger.type]}）：${ep.cliffhanger.text}`,
        `- 觀眾帶走的問題：${ep.cliffhanger.question ?? "—"}`,
        `- 奇觀：${ep.spectacle}`,
        `- 顏值：${ep.glamour_shot}`,
        `- 調性：${ep.tones.map((id) => tones[id]).join("、")}｜主角：${ARC[ep.lead_arc]}｜張力 ${ep.tension.join("-")}`,
        `- 出場：${ep.characters.map((id) => names[id] ?? guests[id] ?? id).join("、")}｜場景：${ep.locations.join("、")}`,
        `- 埋：${ep.setups.join("、") || "—"}｜收：${ep.payoffs.join("、") || "—"}${ep.reveals.length ? `｜揭曉：${ep.reveals.join("、")}` : ""}`,
        `- 狀態：${ep.state.time}；${ep.state.knowledge}；接下去：${ep.state.carry_forward}`,
        "",
      );
    }
  }
  return GENERATED + lines.join("\n");
}

function csv(seasons) {
  const cell = (value) => `"${String(value ?? "").replaceAll('"', '""')}"`;
  const header = ["number", "season", "season_episode", "chapter", "title", "youtube_title", "duration_s", "hook_type", "cliffhanger_type", "lead_arc", "tones", "setups", "payoffs", "reveals"];
  const rows = seasons.flatMap((season) => season.episodes.map((ep) => [ep.number, season.number, ep.season_episode, ep.chapter, ep.title, ep.youtube_title, ep.duration_s, ep.hook_type, ep.cliffhanger.type, ep.lead_arc, ep.tones.join(" "), ep.setups.join(" "), ep.payoffs.join(" "), ep.reveals.join(" ")]));
  return [header, ...rows].map((row) => row.map(cell).join(",")).join("\n") + "\n";
}

const seasons = outline.seasons.map((row) => row.number).filter((n) => existsSync(join(here, `season-${pad(n)}.json`))).map((n) => read(`season-${pad(n)}.json`));
const outputs = { "setting.md": settingMd(), "outline.md": outlineMd(), "episodes.csv": csv(seasons) };
for (const season of seasons) outputs[`season-${pad(season.number)}.md`] = seasonMd(season);

const check = process.argv.includes("--check");
const stale = [];
for (const [name, body] of Object.entries(outputs)) {
  const path = join(here, name);
  if (check) {
    if (!existsSync(path) || readFileSync(path, "utf8") !== body) stale.push(name);
  } else writeFileSync(path, body);
}
if (stale.length) {
  console.error(`out of date, run build.mjs: ${stale.join(", ")}`);
  process.exit(1);
}
console.log(check ? "up to date" : `wrote ${Object.keys(outputs).length} files`);
