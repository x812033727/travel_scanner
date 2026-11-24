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
const seasons = Array.from({ length: plan.season_count }, (_, i) =>
  json(`season-${String(i + 1).padStart(2, "0")}.json`),
);
const names = new Map(setting.characters.map((character) => [character.id, character.name]));
const list = (values) => (values.length ? values.join("、") : "—");

function renderSetting() {
  const lines = [
    `# ${plan.title}（${plan.title_en}）｜設定集`,
    "",
    plan.logline,
    "",
    `> **EN Logline**: ${plan.logline_en}`,
    "",
    `分類：\`${plan.category}\`；畫風：\`${plan.style_preset}\`；10季×12集（每集目標${plan.runtime.episode_target_minutes}分鐘，單季合集約${plan.runtime.season_compilation_minutes}分鐘）；主語言：\`${plan.languages.primary}\`（同步${plan.languages.dubs_and_subs.length}語）。`,
    "",
    "本檔由 `setting.json` 與 `plan.json` 產生，修改來源後執行 `build.mjs`。這是企劃文件，不代表後台核准或媒體完成。",
    "",
    `## 世界：${setting.world.name}`,
    "",
    setting.world.premise,
    "",
    ...setting.world.geography.map((place) => `- **${place.name}：**${place.description}`),
    "",
    "### 兩百年真相與揭露界線",
    "",
    setting.world.hidden_history,
    "",
    setting.world.reveal_policy,
    "",
    "## 核心規則",
    "",
  ];
  for (const rule of setting.rules) {
    lines.push(`### ${rule.name}`, "", rule.rule, "", `戲劇與製作代價：${rule.dramatic_cost}`, "");
  }
  lines.push("## 五大勢力", "");
  for (const faction of setting.factions) {
    lines.push(
      `### ${faction.name}`,
      "",
      `資源：${faction.resources}`,
      "",
      `需要：${faction.need}衝突：${faction.conflict}`,
      "",
      `終局交付：${faction.final_contribution}`,
      "",
    );
  }
  lines.push("## 人物表（視覺防撞臉基準）", "");
  for (const character of setting.characters) {
    lines.push(
      `### ${character.name}（${character.id}）`,
      "",
      `${character.role}${character.age_at_start ? `；登場${character.age_at_start}歲` : ""}。`,
      "",
    );
    for (const [key, label] of [
      ["background", "背景"],
      ["ability", "能力"],
      ["limits", "限制"],
      ["arc", "弧光"],
      ["ending", "結局"],
    ]) {
      if (character[key]) lines.push(`**${label}：**${character[key]}`, "");
    }
    lines.push(`**AI 真人視覺與聲線基準：**${character.appearance}`, "");
  }
  lines.push(
    "## 長線謎團（12條跨季伏筆）",
    "",
    "| ID | 問題 | 埋下 | 收束 | 答案 |",
    "| --- | --- | ---: | ---: | --- |",
  );
  for (const thread of setting.mysteries) {
    lines.push(
      `| ${thread.id} | ${cell(thread.question)} | E${thread.introduced_in} | E${thread.resolved_in} | ${cell(thread.answer)} |`,
    );
  }
  lines.push(
    "",
    "中途 `payoffs` 可為階段性翻盤揭露；最終收束集必須再次列出該謎團並完成劇情閉環。",
    "",
    "## 敘事與真人寫實 AI 畫面約束",
    "",
    ...setting.narrative_constraints.map((text) => `- ${text}`),
    "",
    setting.visual_style,
    "",
    "## 封閉結局",
    "",
    `五年後尾聲保留不可逆代價：${setting.finale.permanent_costs.join("；")}。`,
    "",
    `最後一句：**「${setting.finale.last_line}」**（${setting.finale.last_line_zh}）`,
    "",
  );
  return `${lines.join("\n").trimEnd()}\n`;
}

function renderSeason(season) {
  const first = season.episodes[0].number;
  const last = season.episodes.at(-1).number;
  const lines = [
    `# 第${season.number}季〈${season.title} / ${season.title_en}〉`,
    "",
    `全劇第${first}～${last}集；時間：${season.time_span}`,
    "",
    `**主題：**${season.theme}`,
    "",
    `**核心衝突：**${season.core_conflict}`,
    "",
    `每集目標${plan.runtime.episode_target_minutes}分鐘（單季合集約${plan.runtime.season_compilation_minutes}分鐘），英文原音為主；以下為每集冷開場、雙段高張力、集末懸念與連貫狀態細綱，未代替逐鏡分鏡與實測媒體。`,
    "",
  ];
  for (const episode of season.episodes) {
    lines.push(
      `## E${String(episode.number).padStart(3, "0")}｜${episode.title}（${episode.title_en}）`,
      "",
      episode.logline,
      "",
      `**冷開場鉤子：**${episode.hook}`,
      "",
      `**主要衝突：**${episode.conflict}`,
      "",
      `**中段轉折：**${episode.turn}`,
      "",
    );
    for (const [index, beat] of episode.high_tension.entries()) {
      lines.push(
        `**高張力${index + 1}（${beat.beat === "first_half" ? "前半" : "後半"}）：**${beat.event}`,
        "",
        `賭注：${beat.stakes}　後果：${beat.consequence}`,
        "",
      );
    }
    lines.push(
      `**${episode.closed_ending ? "結尾收束" : "集末懸念"}（${episode.cliffhanger.type}）：**${episode.cliffhanger.text}`,
      "",
      `**延續後果：**${episode.consequence}`,
      "",
      `**埋下：**${list(episode.setups)}；**回收：**${list(episode.payoffs)}；**局部成果：**${list(episode.general_payoffs ?? [])}`,
      "",
      `**五段張力：**${episode.tension.join(" → ")}（企劃評分，非實測）`,
      "",
      `**出場：**${episode.characters.map((id) => names.get(id) ?? id).join("、")}；**場景：**${episode.locations.join("、")}`,
      "",
      `**主題句：**${episode.theme}`,
      "",
      "<details>",
      "<summary>本集連貫狀態</summary>",
      "",
    );
    for (const [key, label] of [
      ["time", "時間"],
      ["knowledge", "已知資訊"],
      ["character_state", "人物狀態"],
      ["evidence", "證據"],
      ["carry_forward", "後續接續"],
    ]) {
      lines.push(`- ${label}：${episode.state[key]}`);
    }
    lines.push("", "</details>", "");
  }
  lines.push("## 本季收束與季末翻盤", "", `**收束：**${season.season_resolution}`, "", `**季末翻盤／接續：**${season.season_hook}`, "");
  return `${lines.join("\n").trimEnd()}\n`;
}

function renderOutline() {
  const lines = [
    `# ${plan.title}（${plan.title_en}）｜十季總綱`,
    "",
    plan.logline,
    "",
    `10季×12集＝120集，封閉結局；每集約${plan.runtime.episode_target_minutes}分鐘（單季合集約${plan.runtime.season_compilation_minutes}分鐘），英文原音為主＋8語字幕／配音。`,
    "",
    "## 十季升級與真相曲線",
    "",
    "| 季 | 季名 | 集數 | 時間 | 主題 | 核心衝突 |",
    "| ---: | --- | --- | --- | --- | --- |",
  ];
  for (const season of seasons) {
    lines.push(
      `| ${season.number} | ${cell(season.title)}（${cell(season.title_en)}） | ${season.episodes[0].number}–${season.episodes.at(-1).number} | ${cell(season.time_span)} | ${cell(season.theme)} | ${cell(season.core_conflict)} |`,
    );
  }
  for (const season of seasons) {
    lines.push(
      "",
      `## 第${season.number}季〈${season.title} / ${season.title_en}〉`,
      "",
      `收束：${season.season_resolution}`,
      "",
      `季末翻盤：${season.season_hook}`,
      "",
      "| 集 | 標題 | 英文標題 | 懸念型 | 推進 |",
      "| ---: | --- | --- | --- | --- |",
    );
    for (const episode of season.episodes) {
      lines.push(
        `| ${episode.number} | ${cell(episode.title)} | ${cell(episode.title_en)} | \`${episode.cliffhanger.type}\` | ${cell(episode.logline)} |`,
      );
    }
  }
  lines.push(
    "",
    "## 封閉終局",
    "",
    `十一座存活塔成功並網扛過250年灰潮峰值並反彈軌道核聚變波，軌道十三號站失聯墜海；第119集克拉拉親手爆破子午線一號第一面外牆，第120集跳轉五年後呈現帶著傷疤與逝者記憶的真實重建日常。最後一句：**「${setting.finale.last_line}」**（${setting.finale.last_line_zh}）`,
    "",
  );
  return `${lines.join("\n").trimEnd()}\n`;
}

function continuity() {
  const episodes = seasons.flatMap((season) => season.episodes);
  const quote = (value) => `"${String(value).replaceAll('"', '""')}"`;
  const headers = [
    "episode",
    "title",
    "title_en",
    "cliffhanger_type",
    "time",
    "knowledge",
    "character_state",
    "evidence",
    "carry_forward",
    "setups",
    "payoffs",
    "general_payoffs",
  ];
  const rows = episodes.map((episode) =>
    [
      episode.number,
      episode.title,
      episode.title_en,
      episode.cliffhanger.type,
      ...["time", "knowledge", "character_state", "evidence", "carry_forward"].map(
        (key) => episode.state[key],
      ),
      episode.setups.join(";"),
      episode.payoffs.join(";"),
      (episode.general_payoffs ?? []).join(";"),
    ]
      .map(quote)
      .join(","),
  );
  const lines = [
    "# 連貫性與伏筆帳",
    "",
    "全120集逐集狀態見 `continuity.csv`。嚴守人物資訊邊界與不可逆死亡／傷殘規則。",
    "",
    "## 時間線",
    "",
    "| 季 | 經過月份 | 階段內容 |",
    "| --- | ---: | --- |",
  ];
  for (const item of setting.chronology) {
    lines.push(`| S${item.seasons.join("、S")} | ${item.elapsed_months} | ${item.label} |`);
  }
  lines.push(
    "",
    "## 第九季72小時灰潮即時倒數",
    "",
    "E97–E108嚴格按T-72至T-0即時倒數推進（於E98確認灰潮提早12小時抵達，改由各塔在地代表同步搶修並網，絕不跨塔瞬移）。",
    "",
    "## 12條長線謎團實際埋回位置",
    "",
    "| ID | 埋下或推進集 | 階段或最終回收集 | 最終收束 |",
    "| --- | --- | --- | ---: |",
  );
  for (const thread of setting.mysteries) {
    lines.push(
      `| ${thread.id} | ${episodes.filter((e) => e.setups.includes(thread.id)).map((e) => `E${e.number}`).join("、")} | ${episodes.filter((e) => e.payoffs.includes(thread.id)).map((e) => `E${e.number}`).join("、")} | E${thread.resolved_in} |`,
    );
  }
  lines.push(
    "",
    "## 永久代價與不可逆死亡鎖定",
    "",
    ...setting.finale.permanent_costs.map((item) => `- ${item}`),
    "",
    "## 製作界線",
    "",
    "這份帳追蹤的是企劃狀態，尚未進入逐鏡台詞腳本、後台匯入、媒體生成或正式站發布。",
    "",
  );
  return { csv: `${headers.join(",")}\n${rows.join("\n")}\n`, md: `${lines.join("\n").trimEnd()}\n` };
}

const output = new Map();
output.set("setting.md", renderSetting());
output.set("outline.md", renderOutline());
for (const season of seasons) {
  output.set(`season-${String(season.number).padStart(2, "0")}.md`, renderSeason(season));
}
const outlineJson = {
  chapters: seasons.map((season) => ({
    number: season.number,
    title: season.title,
    title_en: season.title_en,
    theme: season.theme,
    episodes: season.episodes.map(({ number, title, title_en, logline }) => ({
      number,
      title,
      title_en,
      logline,
    })),
  })),
};
output.set("outline.json", encoded(outlineJson));
output.set(
  "documents.json",
  encoded({
    schema_version: 1,
    stage: "planning",
    ready_for_import: false,
    category: plan.category,
    note: "企劃交付文件包；非SeriesIn請求或核准紀錄，開拍前須先完成S1E01三鏡小樣與角色定妝鎖定。",
    documents: [
      { kind: "setting", body_md: output.get("setting.md"), body_json: setting },
      { kind: "outline", body_md: output.get("outline.md"), body_json: outlineJson },
      ...seasons.map((season) => ({
        kind: "chapter",
        chapter_number: season.number,
        body_md: output.get(`season-${String(season.number).padStart(2, "0")}.md`),
        body_json: season,
      })),
    ],
  }),
);
const state = continuity();
output.set("continuity.md", state.md);
output.set("continuity.csv", state.csv);

const sourceNames = [
  "authoring-contract.json",
  "plan.json",
  "setting.json",
  ...seasons.map((season) => `season-${String(season.number).padStart(2, "0")}.json`),
];
const supportNames = ["README.md", "build.mjs", "validate.mjs", "validate.test.mjs"].filter((name) =>
  existsSync(path.join(directory, name)),
);
output.set(
  "manifest.json",
  encoded({
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
    generated_files: Object.fromEntries([...output].map(([name, value]) => [name, hash(value)])),
  }),
);

const check = process.argv.includes("--check");
const stale = [];
for (const [name, value] of output) {
  const target = path.join(directory, name);
  if (check) {
    if (!existsSync(target) || readFileSync(target, "utf8") !== value) stale.push(name);
  } else {
    writeFileSync(target, value, "utf8");
  }
}
if (stale.length) {
  process.stderr.write(
    `Generated files differ from source: ${stale.join(", ")}\nRun node docs/videos/series-plans/glass-meridian/build.mjs\n`,
  );
  process.exitCode = 1;
} else {
  process.stdout.write(
    `${check ? "Checked" : "Built"} ${output.size} generated files; ${seasons.length} seasons, ${seasons.reduce((sum, season) => sum + season.episodes.length, 0)} episodes.\n`,
  );
}
