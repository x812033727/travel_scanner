#!/usr/bin/env node
// Offline, source-bound draft adapter. This module does not import the API, a DB,
// a provider client or a bundle's executable files.
import { createHash } from "node:crypto";
import { constants, closeSync, fstatSync, lstatSync, openSync, readFileSync, readdirSync, realpathSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { isDeepStrictEqual } from "node:util";
import { validatePlan } from "../../../docs/videos/series-plans/borrowed-dawn/validate.mjs";
import { LONG_ANIME_POLICY, requireAnimePolicy } from "../core/anime-policy.mjs";

export const SOURCE = "docs/videos/series-plans/borrowed-dawn";
const ROOT = fileURLToPath(new URL("../../../", import.meta.url));
export const SOURCE_DIRECTORY = path.join(ROOT, SOURCE);
const seasonsNames = Array.from({ length: 10 }, (_, i) => `season-${String(i + 1).padStart(2, "0")}`);
const groups = {
  source_files: ["authoring-contract.json", "plan.json", "setting.json", ...seasonsNames.map((name) => `${name}.json`)],
  support_files: ["README.md", "review.md", "build.mjs", "validate.mjs", "validate.test.mjs"],
  generated_files: ["setting.md", "outline.md", ...seasonsNames.map((name) => `${name}.md`), "outline.json", "documents.json", "continuity.md", "continuity.csv"],
};
export const FILE_NAMES = [...Object.values(groups).flat(), "manifest.json"].sort();
const MAX_FILE_BYTES = 2 * 1024 * 1024;
const MAX_BUNDLE_BYTES = 8 * 1024 * 1024;
const object = (value) => value !== null && typeof value === "object" && !Array.isArray(value);
const text = (value) => typeof value === "string" && value.trim().length > 0 && !value.includes("\0");
const require = (condition, message) => { if (!condition) throw new Error(message); };
export const sha256 = (raw) => createHash("sha256").update(raw).digest("hex");
const canonical = (value) => Array.isArray(value) ? value.map(canonical) : object(value) ? Object.fromEntries(Object.keys(value).sort().map((key) => [key, canonical(value[key])])) : value;
export const sourceBundleHash = (bundle) => sha256(JSON.stringify(canonical(bundle)));

/** JSON.parse alone silently accepts duplicate keys and overflow to Infinity. */
export function parseSourceJson(raw, name = "JSON") {
  let cursor = 0;
  const fail = (message) => { throw new Error(`${name}: ${message} at offset ${cursor}`); };
  const whitespace = () => { while (/^[ \t\r\n]$/.test(raw[cursor] ?? "")) cursor++; };
  const string = () => {
    const start = cursor++;
    let escaped = false;
    while (cursor < raw.length) {
      const char = raw[cursor++];
      if (!escaped && char === '"') {
        try { return JSON.parse(raw.slice(start, cursor)); } catch { fail("invalid JSON string"); }
      }
      if (!escaped && char === "\\") escaped = true;
      else escaped = false;
    }
    fail("unterminated JSON string");
  };
  const value = (depth = 0) => {
    if (depth > 100) fail("JSON nesting is too deep");
    whitespace();
    const first = raw[cursor];
    if (first === '"') return string();
    if (first === "{" || first === "[") {
      const result = first === "{" ? {} : [];
      const end = first === "{" ? "}" : "]";
      const keys = new Set();
      cursor++;
      whitespace();
      if (raw[cursor] === end) { cursor++; return result; }
      while (cursor < raw.length) {
        if (first === "{") {
          whitespace();
          if (raw[cursor] !== '"') fail("object key must be a string");
          const key = string();
          if (keys.has(key)) fail(`duplicate JSON key ${JSON.stringify(key)}`);
          keys.add(key);
          whitespace();
          if (raw[cursor++] !== ":") fail("missing colon");
          Object.defineProperty(result, key, { value: value(depth + 1), enumerable: true, configurable: true, writable: true });
        } else result.push(value(depth + 1));
        whitespace();
        const separator = raw[cursor++];
        if (separator === end) return result;
        if (separator !== ",") fail("missing separator");
      }
      fail("unterminated JSON container");
    }
    for (const [literal, parsed] of [["true", true], ["false", false], ["null", null]]) {
      if (raw.startsWith(literal, cursor)) { cursor += literal.length; return parsed; }
    }
    const number = /^-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?/.exec(raw.slice(cursor));
    if (!number) fail("invalid JSON value");
    cursor += number[0].length;
    const parsed = Number(number[0]);
    if (!Number.isFinite(parsed)) fail("nonfinite JSON number");
    if (Number.isInteger(parsed) && (!Number.isSafeInteger(parsed) || /[.eE]/.test(number[0]))) fail("integer JSON numbers must use safe integer notation");
    return parsed;
  };
  const parsed = value();
  whitespace();
  if (cursor !== raw.length) fail("unexpected trailing content");
  require(object(parsed), `${name}: expected a JSON object`);
  return parsed;
}

/** Read only this checkout's known pack; never load arbitrary uploaded code. */
export function readAnimeSourceFiles(directory = SOURCE_DIRECTORY) {
  const selected = path.resolve(directory);
  require(selected === path.resolve(SOURCE_DIRECTORY), `source must be the checked-in ${SOURCE}`);
  let current = path.parse(selected).root;
  for (const segment of selected.slice(current.length).split(path.sep).filter(Boolean)) {
    current = path.join(current, segment);
    const info = lstatSync(current);
    require(!info.isSymbolicLink() && info.isDirectory(), `source path cannot contain symlinks: ${current}`);
  }
  require(isDeepStrictEqual(readdirSync(selected).sort(), FILE_NAMES), "source pack has missing or unexpected files");
  const files = {};
  for (const name of FILE_NAMES) {
    const filename = path.join(selected, name);
    const info = lstatSync(filename);
    require(!info.isSymbolicLink() && info.isFile(), `${name}: source pack cannot contain symlinks or nonfiles`);
    const fd = openSync(filename, constants.O_RDONLY | constants.O_NOFOLLOW);
    try {
      const opened = fstatSync(fd);
      require(opened.isFile() && opened.size <= MAX_FILE_BYTES, `${name}: invalid or oversized file`);
      const bytes = readFileSync(fd);
      const raw = new TextDecoder("utf-8", { fatal: true }).decode(bytes);
      require(Buffer.from(raw, "utf8").equals(bytes), `${name}: source must be exact UTF-8`);
      files[name] = raw;
    } finally { closeSync(fd); }
  }
  return files;
}

function additionalSourceSemantics({ plan, setting, contract }) {
  require(plan.schema_version === 1 && plan.slug === "borrowed-dawn", "invalid source plan version/slug");
  for (const key of ["title", "logline", "tone", "source_note"]) require(text(plan[key]), `plan requires ${key}`);
  require(plan.title.length <= 200 && plan.logline.length <= 4000, "source title or premise too long");
  require(isDeepStrictEqual(plan.video_defaults, { category: "anime", format: "drama", look: { preset: "anime-2d" }, locale: "zh-TW" }), "source video defaults drift");
  for (const [key, expected] of [["story_minutes", 22], ["op_ed_budget_minutes", 3], ["broadcast_slot_minutes", 30], ["broadcast_slot_reserve_minutes", 5]]) require(plan.runtime[key] === expected, `source runtime.${key} must be ${expected}`);
  require(plan.production_support.gaps.find((gap) => gap.code === "closed-finale")?.planned_last_tension === 2, "source finale tension must remain 2");
  require(setting.characters.length >= 4 && setting.mysteries.length >= 8 && setting.mysteries.length <= 12, "source needs an ensemble cast and 8–12 mysteries");
  require(isDeepStrictEqual(contract.character_ids, setting.characters.map((character) => character.id)), "source cast order differs from contract");
  require(isDeepStrictEqual(contract.thread_ids, setting.mysteries.map((thread) => thread.id)), "source mystery order differs from contract");
  const fields = (entry, keys, label) => require(object(entry) && keys.every((key) => text(entry[key])), `incomplete ${label}`);
  for (const character of setting.characters) fields(character, ["id", "name", "appearance", "role"], "character");
  require(Array.isArray(setting.rules) && setting.rules.length >= 4 && Array.isArray(setting.factions) && setting.factions.length === 4, "source needs rules and four factions");
  for (const rule of setting.rules) fields(rule, ["name", "rule", "dramatic_cost"], "world rule");
  for (const faction of setting.factions) fields(faction, ["name", "resources", "need", "conflict", "final_contribution"], "faction");
  fields(setting.world, ["name", "premise", "hidden_history", "reveal_policy"], "world");
  require(Array.isArray(setting.world.geography) && setting.world.geography.length > 0, "missing geography");
  for (const place of setting.world.geography) fields(place, ["name", "description"], "geography");
  require(Array.isArray(setting.narrative_constraints) && setting.narrative_constraints.length > 0 && setting.narrative_constraints.every(text) && text(setting.visual_style), "source narrative/visual rules are missing");
  require(Array.isArray(setting.chronology) && setting.chronology.length > 0, "missing chronology");
  const covered = [];
  for (const item of setting.chronology) {
    require(object(item) && Number.isSafeInteger(item.elapsed_months) && item.elapsed_months >= 1 && item.elapsed_months <= 120 && text(item.label) && Array.isArray(item.seasons) && item.seasons.every((n) => Number.isSafeInteger(n) && n >= 1 && n <= 10), "invalid source chronology");
    covered.push(...item.seasons);
  }
  require(isDeepStrictEqual(covered.sort((a, b) => a - b), Array.from({ length: 10 }, (_, i) => i + 1)), "source chronology must cover all ten seasons exactly once");
  require(setting.finale.epilogue_years === 8 && setting.finale.permanent_costs.length >= 4, "source must preserve the eight-year epilogue and permanent costs");
}

// RENDERERS: frozen source format, implemented here rather than executing build.mjs.
function renderDerived(plan, setting, seasons) {
  const cell = (value) => String(value ?? "").replaceAll("|", "／").replaceAll("\n", " ");
  const list = (values) => values.length ? values.join("、") : "—";
  const names = new Map(setting.characters.map((character) => [character.id, character.name]));
  function renderSetting() {
    const lines = [
      `# ${plan.title}｜設定集`, "", plan.logline, "",
      `分類：\`${plan.category}\`；畫風：\`${plan.style_preset}\`；10季×12集。`, "",
      "本檔由 setting.json 與 plan.json 產生，修改來源後執行 build.mjs。這是企劃文件，不代表後台核准或媒體完成。", "",
      `## 世界：${setting.world.name}`, "", setting.world.premise, "",
      ...setting.world.geography.map((place) => `- **${place.name}：**${place.description}`), "",
      "### 古代真相與揭露界線", "", setting.world.hidden_history, "", setting.world.reveal_policy, "",
      "## 核心規則", ""
    ];
    for (const rule of setting.rules) lines.push(`### ${rule.name}`, "", rule.rule, "", `戲劇代價：${rule.dramatic_cost}`, "");
    lines.push("## 四大勢力", "");
    for (const faction of setting.factions) lines.push(`### ${faction.name}`, "", `資源：${faction.resources}。`, "", `需要：${faction.need}。衝突：${faction.conflict}。`, "", `終局交付：${faction.final_contribution}。`, "");
    lines.push("## 人物表", "");
    for (const character of setting.characters) {
      lines.push(`### ${character.name}（${character.id}）`, "", `${character.role}${character.age_at_start ? `；登場${character.age_at_start}歲` : ""}。`, "");
      for (const [key, label] of [["background", "背景"], ["ability", "能力"], ["limits", "限制"], ["arc", "成長與責任"], ["ending", "結局"]]) if (character[key]) lines.push(`**${label}：**${character[key]}`, "");
      lines.push(`**外觀基準：**${character.appearance}`, "");
    }
    lines.push("## 長線謎團", "", "| ID | 問題 | 埋下 | 收束 | 答案 |", "| --- | --- | ---: | ---: | --- |");
    for (const thread of setting.mysteries) lines.push(`| ${thread.id} | ${cell(thread.question)} | ${thread.introduced_in} | ${thread.resolved_in} | ${cell(thread.answer)} |`);
    lines.push("", "中途 payoffs 可以是局部回收，並非整條謎團已解。最後收束集必須再次列出該謎團，對應真實劇情。", "", "## 敘事與畫面", "", ...setting.narrative_constraints.map((text) => `- ${text}`), "", setting.visual_style, "", "## 封閉結局", "", `八年後的尾聲保留：${setting.finale.permanent_costs.join("、")}。`, "", `最後一句：**「${setting.finale.last_line}」**`, "");
    return `${lines.join("\n").trimEnd()}\n`;
  }

  function renderSeason(season) {
    const first = season.episodes[0].number;
    const last = season.episodes.at(-1).number;
    const lines = [`# 第${season.number}季〈${season.title}〉`, "", `全劇第${first}～${last}集；時間：${season.time_span}`, "", `**主題：**${season.theme}`, "", `**核心衝突：**${season.core_conflict}`, "", "正文目標22分鐘；以下是兩段高張力與連貫狀態的細綱，未代替逐場台詞、分鏡或實測媒體。", ""];
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
    const lines = [`# ${plan.title}｜十季總綱`, "", plan.logline, "", "分類 anime，120集，封閉結局。播出時段約30分鐘，正文約22分鐘；原定規格不縮為現行短漫劇。", "", "## 升級與真相曲線", "", "| 季 | 集數 | 時間 | 主題 | 核心衝突 |", "| --- | --- | --- | --- | --- |"];
    for (const season of seasons) lines.push(`| ${season.number} | ${season.episodes[0].number}–${season.episodes.at(-1).number} | ${cell(season.time_span)} | ${cell(season.theme)} | ${cell(season.core_conflict)} |`);
    for (const season of seasons) {
      lines.push("", `## 第${season.number}季〈${season.title}〉`, "", `收束：${season.season_resolution}`, "", `接續：${season.season_hook}`, "", "| 集 | 標題 | 推進 |", "| ---: | --- | --- |");
      for (const episode of season.episodes) lines.push(`| ${episode.number} | ${cell(episode.title)} | ${cell(episode.logline)} |`);
    }
    lines.push("", "## 終局", "", `三座完整天錨與北錨遺址替代樞紐完成首輪安全切換，具名載體真正分區輪休。舊債仍須償還；第120集跳八年後，沒有新敵、新門或未解異常。最後一句：${setting.finale.last_line}`, "");
    return `${lines.join("\n").trimEnd()}\n`;
  }

  function continuity() {
    const episodes = seasons.flatMap((season) => season.episodes);
    const quote = (value) => `"${String(value).replaceAll('"', '""')}"`;
    const headers = ["episode", "title", "time", "knowledge", "character_state", "evidence", "carry_forward", "setups", "payoffs", "general_payoffs"];
    const rows = episodes.map((episode) => [episode.number, episode.title, ...["time", "knowledge", "character_state", "evidence", "carry_forward"].map((key) => episode.state[key]), episode.setups.join(";"), episode.payoffs.join(";"), (episode.general_payoffs ?? []).join(";")].map(quote).join(","));
    const lines = ["# 連貫性與伏筆帳", "", "各集狀態見 continuity.csv。保留已知與未知界線，角色不因觀眾已看過某場戲就自動知道答案。", "", "## 時間線", "", "| 季 | 經過月份 | 內容 |", "| --- | ---: | --- |"];
    for (const item of setting.chronology) lines.push(`| ${item.seasons.join("、")} | ${item.elapsed_months} | ${item.label} |`);
    lines.push("", `主線共約${setting.chronology.reduce((sum, item) => sum + item.elapsed_months, 0)}個月。第72集之後完整一年試驗加後三季約十四個月，在預測區間內完成首輪退出；三年不是安全保證。`, "", "## 兩小時危機", "", "54／55／56／57／58：T−120／95／65／35／0分鐘。本地訊號台與鄰區技師並行，不跨國瞬移。", "", "## 謎團埋回實際位置", "", "| ID | 埋下或推進集 | 局部或最終回收集 | 最終收束 |", "| --- | --- | --- | ---: |");
    for (const thread of setting.mysteries) lines.push(`| ${thread.id} | ${episodes.filter((episode) => episode.setups.includes(thread.id)).map((episode) => episode.number).join("、")} | ${episodes.filter((episode) => episode.payoffs.includes(thread.id)).map((episode) => episode.number).join("、")} | ${thread.resolved_in} |`);
    lines.push("", "## 永久限制", "", ...setting.finale.permanent_costs.map((item) => `- ${item}`), "", "## 製作界線", "", "這份帳追蹤的是企劃狀態，未核准劇本、未生成前情摘要、未讀取正式站狀態。人物外觀與能力限制以設定集為準。", "");
    return { csv: `${headers.join(",")}\n${rows.join("\n")}\n`, md: `${lines.join("\n").trimEnd()}\n` };
  }
  const state = continuity();
  return {
    "setting.md": renderSetting(), "outline.md": renderOutline(),
    ...Object.fromEntries(seasons.map((season) => [`season-${String(season.number).padStart(2, "0")}.md`, renderSeason(season)])),
    "continuity.md": state.md, "continuity.csv": state.csv,
  };
}

export function validateAnimeSourceFiles(files, { source = SOURCE } = {}) {
  require(source === SOURCE, "source path must match the checked-in plan slug");
  require(object(files) && isDeepStrictEqual(Object.keys(files).sort(), FILE_NAMES), "source pack has missing or unexpected files");
  for (const [name, raw] of Object.entries(files)) require(typeof raw === "string" && !raw.includes("\0") && Buffer.from(raw, "utf8").toString("utf8") === raw && Buffer.byteLength(raw, "utf8") <= MAX_FILE_BYTES, `${name}: invalid or oversized source content`);
  const sourceBundle = { schema_version: 1, artifact_kind: "anime-planning-import", source, files };
  require(Buffer.byteLength(JSON.stringify(sourceBundle), "utf8") <= MAX_BUNDLE_BYTES, "source bundle is too large");
  const parsed = Object.fromEntries(FILE_NAMES.filter((name) => name.endsWith(".json")).map((name) => [name, parseSourceJson(files[name], name)]));
  const data = { plan: parsed["plan.json"], setting: parsed["setting.json"], contract: parsed["authoring-contract.json"], seasons: seasonsNames.map((name) => parsed[`${name}.json`]), outline: parsed["outline.json"], documents: parsed["documents.json"], manifest: parsed["manifest.json"], files };
  const result = validatePlan(data);
  require(result.errors.length === 0, `source package failed validation:\n${result.errors.join("\n")}`);
  additionalSourceSemantics(data);
  const expected = renderDerived(data.plan, data.setting, data.seasons);
  for (const [name, raw] of Object.entries(expected)) require(files[name] === raw, `${name}: rendered content differs from source`);
  const outline = { chapters: data.seasons.map((season) => ({ number: season.number, title: season.title, theme: season.theme, episodes: season.episodes.map(({ number, title, logline }) => ({ number, title, logline })) })) };
  require(isDeepStrictEqual(data.outline, outline), "outline projection differs from source");
  const documents = [
    { kind: "setting", body_md: expected["setting.md"], body_json: data.setting },
    { kind: "outline", body_md: expected["outline.md"], body_json: outline },
    ...data.seasons.map((season) => ({ kind: "chapter", chapter_number: season.number, body_md: expected[`season-${String(season.number).padStart(2, "0")}.md`], body_json: season })),
  ];
  require(isDeepStrictEqual(data.documents.documents, documents), "document twins differ from exact source projections");
  return { ...data, sourceBundle, validation: result, documents, episodes: data.seasons.flatMap((season) => season.episodes) };
}

export function buildAnimeProductionInput(files = readAnimeSourceFiles(), options = {}) {
  const validated = validateAnimeSourceFiles(files, options);
  const { plan, setting, sourceBundle } = validated;
  const seriesRequest = {
    slug: `${plan.slug}-production`, title: plan.title, premise: plan.logline,
    kind: "series", category: "anime", aspects: ["world", "bonds", "structure", "mood"],
    tone: "no-romance", style_preset: "anime-2d", genre: "custom", lead: "ensemble",
    target_minutes: 22, planned_episodes: 120, episodes_per_chapter: 12,
    open_ended: false, hands_off: false, compilation: false, visual_tier: "clips",
    production_policy: LONG_ANIME_POLICY,
    runtime_spec: { body_target_seconds: 1320, op_ed_budget_seconds: 180, broadcast_slot_seconds: 1800, slot_reserve_seconds: 300 },
    note: "來源綁定的長篇動漫製作草案；建立後保持暫停，文件、劇本、角色聲線與製作設計待審。",
  };
  requireAnimePolicy(seriesRequest);
  return {
    schema_version: 1, artifact_kind: "anime-production-input-draft", stage: "source-bound-draft",
    ready_for_import: false, ready_for_production: false, admin_series_created: false,
    media_generated: false, published: false, approvals_recorded: false,
    series_request: seriesRequest,
    source_binding: { source: SOURCE, source_slug: plan.slug, manifest_sha256: sha256(files["manifest.json"]), bundle_sha256: sourceBundleHash(sourceBundle), file_sha256: Object.fromEntries(FILE_NAMES.map((name) => [name, sha256(files[name])])) },
    source_metadata: { original_tone: plan.tone, original_runtime: plan.runtime, original_production_support: plan.production_support, source_note: plan.source_note },
    source_bundle: sourceBundle,
    documents: validated.documents,
    episodes: validated.episodes,
    production_requirements: {
      status: "pending-production-review", ready_for_production: false,
      casting: setting.characters.map((character) => ({ character_id: character.id, name: character.name, locale: "zh-TW", source_voice_present: object(character.voice) && text(character.voice.provider) && text(character.voice.name), missing: object(character.voice) && text(character.voice.provider) && text(character.voice.name) ? ["source-bound audition and listening acceptance"] : ["provider and voice name", "performance direction", "source-bound audition and listening acceptance"] })),
      design: ["approved character designs and any named shot looks", "per-episode production design and provider capability checks", "timed animatic and representative pilot"],
      shared: ["narrator casting and listening acceptance", "120 complete 22-minute screenplays and reviewed storyboards", "measured Chinese audio, complete films and switchable CC", "source-bound document and script approvals"],
      measured_body_seconds: null, op_ed_media_seconds: null, slot_reserve_generated: false,
    },
    warnings: ["A validated native request creates a separate paused draft; it grants no planning-row unlock or production approval.", "Source support gaps are historical source metadata and remain unchanged; validated policy support does not complete casting, scripts or media.", "OP/ED is a budget; current channel branding remains at most 30 seconds each. The broadcast slot reserve is never generated.", ...validated.validation.warnings],
  };
}

/** Revalidate a portable draft, optionally binding it to the checkout's current source. */
export function validateAnimeProductionInput(draft, currentFiles = null) {
  require(object(draft) && object(draft.source_bundle), "expected a source-bound anime production input");
  const expected = buildAnimeProductionInput(draft.source_bundle.files, { source: draft.source_bundle.source });
  require(isDeepStrictEqual(draft, expected), "production input differs from its validated source, native policy or pending requirements");
  if (currentFiles !== null) require(isDeepStrictEqual(draft.source_binding.file_sha256, buildAnimeProductionInput(currentFiles).source_binding.file_sha256), "source version changed; rebuild and review the production input");
  return true;
}

export function main(args = process.argv.slice(2), { stdout = process.stdout, stderr = process.stderr } = {}) {
  if (args.includes("--help")) { stdout.write("Usage: node tools/video/production/anime-input.mjs [--source docs/videos/series-plans/borrowed-dawn] [--out <new-file>]\nOffline validation and source-bound draft only; default writes JSON to stdout. No API, approval, activation or media calls.\n"); return 0; }
  try {
    let directory = SOURCE_DIRECTORY;
    let output;
    for (let i = 0; i < args.length; i++) {
      require(["--source", "--out"].includes(args[i]) && text(args[i + 1]) && !args[i + 1].startsWith("--"), `invalid argument ${args[i]}`);
      if (args[i] === "--source") directory = path.resolve(args[++i]);
      else output = path.resolve(args[++i]);
    }
    const draft = buildAnimeProductionInput(readAnimeSourceFiles(directory));
    const encoded = `${JSON.stringify(draft, null, 2)}\n`;
    if (output) {
      const destination = path.join(realpathSync(path.dirname(output)), path.basename(output));
      const repository = `${realpathSync(ROOT)}${path.sep}`;
      require(destination !== repository.slice(0, -1) && !destination.startsWith(repository), "write the review draft outside the repository");
      writeFileSync(output, encoded, { encoding: "utf8", flag: "wx" });
      stdout.write(`Validated 12 source documents, 120 episodes and 240 high-tension beats; wrote paused production draft to ${output}\nready_for_production=false; no import, approval, activation or media generation performed.\n`);
    } else stdout.write(encoded);
    return 0;
  } catch (error) { stderr.write(`${error.message}\n`); return 1; }
}

if (process.argv[1] && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href) process.exitCode = main();
