#!/usr/bin/env node
// Local structural and continuity checks for Glass Meridian (10 seasons, 120 episodes).
import { readFile } from "node:fs/promises";
import { readFileSync } from "node:fs";
import { createHash } from "node:crypto";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { isDeepStrictEqual } from "node:util";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const CONTRACT = JSON.parse(readFileSync(path.join(HERE, "authoring-contract.json"), "utf8"));
const TOTAL = 120;
const SEASONS = 10;
const PER_SEASON = 12;
const ENDINGS = new Set(["danger", "reveal", "choice", "reversal", "emotion"]);
const STATE_FIELDS = ["time", "knowledge", "character_state", "evidence", "carry_forward"];
const TEXT_FIELDS = ["title", "title_en", "logline", "hook", "conflict", "turn", "theme", "consequence"];
const DEATH_CUTOFFS = new Map([
  ["coroner-hale", 1],
  ["marcus-thorne", 95],
  ["elena-rostova", 106],
  ["julian-vance", 108],
  ["director-cassian", 118],
]);
const SOURCE_NAMES = [
  "authoring-contract.json",
  "plan.json",
  "setting.json",
  ...Array.from({ length: SEASONS }, (_, index) => `season-${String(index + 1).padStart(2, "0")}.json`),
];
const SUPPORT_NAMES = ["README.md", "build.mjs", "validate.mjs", "validate.test.mjs"];
const GENERATED_NAMES = [
  "setting.md",
  "outline.md",
  ...Array.from({ length: SEASONS }, (_, index) => `season-${String(index + 1).padStart(2, "0")}.md`),
  "outline.json",
  "documents.json",
  "continuity.md",
  "continuity.csv",
];

const isObject = (value) => value !== null && typeof value === "object" && !Array.isArray(value);
const isText = (value) => typeof value === "string" && value.trim().length > 0;
const same = isDeepStrictEqual;
const asArray = (value) => (Array.isArray(value) ? value : []);
const digest = (value) => createHash("sha256").update(value).digest("hex");

export function validatePlan({ plan, setting, seasons, contract = CONTRACT, outline, documents, manifest, files } = {}) {
  const errors = [];
  const warnings = [
    "本地結構與連貫性驗證不等於可匯入或成片品質；production_support.ready_for_import 必須保留 false。",
    "每集約8分鐘、單季合集約96分鐘為企劃目標，尚未進行逐鏡台詞量測或付費生成。",
  ];
  const check = (condition, message) => {
    if (!condition) errors.push(message);
  };
  const stringList = (value, label, { allowEmpty = false, known } = {}) => {
    if (!Array.isArray(value)) {
      errors.push(`${label} 必須是陣列。`);
      return [];
    }
    check(allowEmpty || value.length > 0, `${label} 不得為空。`);
    check(value.every(isText), `${label} 必須只含非空字串。`);
    check(new Set(value).size === value.length, `${label} 含重複值。`);
    if (known) for (const id of value) check(known.has(id), `${label} 引用未知 ID ${JSON.stringify(id)}。`);
    return value.filter(isText);
  };

  if (!isObject(plan)) errors.push("plan 必須是物件。");
  if (!isObject(setting)) errors.push("setting 必須是物件。");
  if (!Array.isArray(seasons)) errors.push("seasons 必須是依季順序排列的陣列。");
  plan = isObject(plan) ? plan : {};
  setting = isObject(setting) ? setting : {};
  seasons = Array.isArray(seasons) ? seasons : [];
  contract = isObject(contract) ? contract : {};

  check(contract.schema_version === 1, "authoring contract 必須是 schema_version=1。");
  check(contract.title === plan.title && contract.slug === plan.slug, "authoring contract 的 title／slug 必須與 plan 相符。");
  check(contract.planned_episodes === TOTAL && contract.episodes_per_season === PER_SEASON, "authoring contract 必須維持 120 集、每季 12 集。");
  check(contract.primary_language === "en", "authoring contract 主語言必須是 en。");
  check(same(contract.state_fields, STATE_FIELDS), "authoring contract.state_fields 必須完整定義五個連貫狀態欄位。");

  check(plan.artifact_kind === "western-series-plan", "plan.artifact_kind 必須是 western-series-plan。");
  check(plan.style_preset === "live-action-cinematic", "plan.style_preset 必須是 live-action-cinematic。");
  check(plan.open_ended === false, "plan.open_ended 必須是 false。");
  check(plan.planned_episodes === TOTAL, "plan.planned_episodes 必須是 120。");
  check(plan.season_count === SEASONS, "plan.season_count 必須是 10。");
  check(plan.episodes_per_chapter === PER_SEASON, "plan.episodes_per_chapter 必須是 12。");
  check(plan.languages?.primary === "en", "plan.languages.primary 必須是 en。");
  check(asArray(plan.languages?.dubs_and_subs).includes("zh-TW") && asArray(plan.languages?.dubs_and_subs).length === 9, "plan.languages.dubs_and_subs 必須含英文與8語共9語。");

  const support = plan.production_support;
  check(isObject(support), "production_support 必須是物件。");
  for (const key of ["ready_for_import", "admin_series_created", "media_generated", "published"]) {
    check(support?.[key] === false, `production_support.${key} 必須保持 false。`);
  }
  const gaps = Array.isArray(support?.gaps) ? support.gaps : [];
  check(gaps.length > 0, "production_support.gaps 不得為空。");
  const finaleGap = gaps.find((gap) => gap?.code === "closed-finale");
  check(finaleGap?.episode === TOTAL && finaleGap?.planned_last_tension === 2, "closed-finale gap 必須保留 E120 末段張力 2。");

  const cast = Array.isArray(setting.characters) ? setting.characters : [];
  const castIds = new Set();
  for (const character of cast) {
    check(isObject(character) && ["id", "name", "appearance"].every((key) => isText(character?.[key])), "每位角色必須有非空 id/name/appearance。");
    check(!castIds.has(character?.id), `重複角色 ID ${JSON.stringify(character?.id)}。`);
    if (isText(character?.id)) castIds.add(character.id);
  }
  check(same([...castIds].sort(), asArray(contract.character_ids).slice().sort()), "setting／contract 的角色 ID 清單必須一致。");

  const mysteries = Array.isArray(setting.mysteries) ? setting.mysteries : [];
  const threads = new Map();
  for (const mystery of mysteries) {
    check(isObject(mystery) && ["id", "question", "answer"].every((key) => isText(mystery?.[key])), "每條長線必須有非空 id/question/answer。");
    check(!threads.has(mystery?.id), `重複 thread ID ${JSON.stringify(mystery?.id)}。`);
    check(Number.isInteger(mystery?.introduced_in) && mystery.introduced_in >= 1 && mystery.introduced_in <= TOTAL, `thread ${mystery?.id} introduced_in 須在 1–120。`);
    check(Number.isInteger(mystery?.resolved_in) && mystery.resolved_in >= mystery.introduced_in && mystery.resolved_in <= TOTAL, `thread ${mystery?.id} resolved_in 須在 introduced_in–120。`);
    if (isText(mystery?.id)) threads.set(mystery.id, mystery);
  }
  check(same([...threads.keys()].sort(), asArray(contract.thread_ids).slice().sort()), "setting／contract 的 thread ID 清單必須一致。");
  check(setting.finale?.closed === true && setting.finale?.new_crisis_or_sequel_hook === false, "setting.finale 必須為封閉結局。");
  check(isText(setting.finale?.last_line), "setting.finale.last_line 不得為空。");

  check(seasons.length === SEASONS, `必須有 10 季，目前 ${seasons.length} 季。`);
  const episodes = [];
  for (const [seasonIndex, season] of seasons.entries()) {
    const seasonNumber = seasonIndex + 1;
    check(isObject(season) && season?.number === seasonNumber, `season[${seasonIndex}].number 必須是 ${seasonNumber}。`);
    for (const key of ["title", "title_en", "theme", "core_conflict", "time_span", "season_resolution", "season_hook"]) {
      check(isText(season?.[key]), `第 ${seasonNumber} 季缺少非空 ${key}。`);
    }
    const rows = Array.isArray(season?.episodes) ? season.episodes : [];
    check(rows.length === PER_SEASON, `第 ${seasonNumber} 季必須恰好 12 集，目前 ${rows.length} 集。`);
    for (const [index, episode] of rows.entries()) {
      const expected = seasonIndex * PER_SEASON + index + 1;
      const label = `S${seasonNumber}E${expected}`;
      check(isObject(episode) && episode?.number === expected, `${label} 集號必須是 ${expected}。`);
      if (!isObject(episode)) continue;
      episodes.push(episode);
      for (const key of TEXT_FIELDS) check(isText(episode[key]), `${label}.${key} 不得為空。`);
      for (const key of asArray(contract.episode_fields)) check(Object.hasOwn(episode, key), `${label} 缺少欄位 ${key}。`);
      const tension = episode.tension;
      check(Array.isArray(tension) && tension.length === 5 && tension.every((v) => Number.isInteger(v) && v >= 1 && v <= 5), `${label}.tension 必須是五段 1–5 整數。`);
      check(isObject(episode.cliffhanger) && ENDINGS.has(episode.cliffhanger.type) && isText(episode.cliffhanger.text), `${label}.cliffhanger 格式錯誤。`);
      if (episode.number === TOTAL) {
        check(episode.closed_ending === true, "E120 必須 closed_ending=true。");
        check(episode.cliffhanger?.type === "emotion", "E120 cliffhanger.type 必須為 emotion。");
        check(asArray(tension).at(-1) === finaleGap?.planned_last_tension, "E120 末段張力必須等於 closed-finale 宣告值 2。");
      } else {
        check(episode.closed_ending === false, `${label}.closed_ending 必須是 false。`);
        check(Array.isArray(tension) && tension.at(-1) >= 4, `${label} 末段張力必須 >=4。`);
      }
      const chars = stringList(episode.characters, `${label}.characters`, { known: castIds });
      for (const charId of chars) {
        const cutoff = DEATH_CUTOFFS.get(charId);
        if (cutoff !== undefined) {
          check(episode.number <= cutoff, `${label} 不得讓已於 E${cutoff} 永久死亡的角色 ${charId} 再度出場。`);
        }
      }
      stringList(episode.locations, `${label}.locations`);
      const setups = stringList(episode.setups, `${label}.setups`, { allowEmpty: true, known: threads });
      const payoffs = stringList(episode.payoffs, `${label}.payoffs`, { allowEmpty: true, known: threads });
      stringList(episode.general_payoffs, `${label}.general_payoffs`, { allowEmpty: true });
      for (const id of setups) {
        const t = threads.get(id);
        if (t) check(episode.number >= t.introduced_in && episode.number <= t.resolved_in, `${label} setups 引用 ${id} 超出 [E${t.introduced_in}, E${t.resolved_in}]。`);
      }
      for (const id of payoffs) {
        const t = threads.get(id);
        if (t) check(episode.number >= t.introduced_in && episode.number <= t.resolved_in, `${label} payoffs 引用 ${id} 超出 [E${t.introduced_in}, E${t.resolved_in}]。`);
      }
      const beats = Array.isArray(episode.high_tension) ? episode.high_tension : [];
      check(beats.length === 2, `${label}.high_tension 必須剛好兩段。`);
      if (beats.length === 2) {
        check(beats[0]?.beat === "first_half" && beats[1]?.beat === "second_half", `${label}.high_tension 必須依序為 first_half 與 second_half。`);
        for (const beat of beats) {
          for (const key of ["event", "stakes", "consequence"]) check(isText(beat?.[key]), `${label}.high_tension.${key} 不得為空。`);
        }
      }
      check(isObject(episode.state), `${label}.state 必須是物件。`);
      for (const key of STATE_FIELDS) check(isText(episode.state?.[key]), `${label}.state.${key} 不得為空。`);
    }
  }

  for (let i = 1; i < episodes.length - 1; i += 1) {
    const prev = episodes[i - 1];
    const curr = episodes[i];
    check(prev.cliffhanger?.type !== curr.cliffhanger?.type, `E${prev.number} 與 E${curr.number} 的 cliffhanger.type 連續重複 (${curr.cliffhanger?.type})。`);
  }

  for (const [id, thread] of threads) {
    const introEp = episodes.find((e) => e.number === thread.introduced_in);
    const resEp = episodes.find((e) => e.number === thread.resolved_in);
    check(introEp?.setups?.includes(id), `長線 ${id} 必須在 E${thread.introduced_in} 的 setups 中埋下。`);
    check(resEp?.payoffs?.includes(id), `長線 ${id} 必須在 E${thread.resolved_in} 的 payoffs 中收束。`);
  }

  if (outline) {
    check(Array.isArray(outline.chapters) && outline.chapters.length === SEASONS, "outline.json 必須有 10 季。");
  }
  if (documents) {
    check(documents.ready_for_import === false && Array.isArray(documents.documents) && documents.documents.length === SEASONS + 2, "documents.json 結構不符。");
  }
  if (manifest && files) {
    check(manifest.episode_count === TOTAL && manifest.season_count === SEASONS, "manifest.json 集數／季數不符。");
    for (const [group, names] of [
      ["source_files", SOURCE_NAMES],
      ["support_files", SUPPORT_NAMES],
      ["generated_files", GENERATED_NAMES],
    ]) {
      for (const name of names) {
        const raw = files.get(name);
        check(raw !== undefined, `缺少檔案 ${name}。`);
        if (raw !== undefined) check(manifest[group]?.[name] === digest(raw), `manifest.${group}.${name} 雜湊不符。`);
      }
    }
  }

  return { ok: errors.length === 0, errors, warnings, episodeCount: episodes.length, seasonCount: seasons.length };
}

export async function validateDirectory(dir = HERE) {
  const readJson = async (name) => JSON.parse(await readFile(path.join(dir, name), "utf8"));
  const plan = await readJson("plan.json");
  const setting = await readJson("setting.json");
  const contract = await readJson("authoring-contract.json");
  const seasons = await Promise.all(
    Array.from({ length: SEASONS }, (_, i) => readJson(`season-${String(i + 1).padStart(2, "0")}.json`)),
  );
  const outline = await readJson("outline.json");
  const documents = await readJson("documents.json");
  const manifest = await readJson("manifest.json");
  const files = new Map();
  for (const name of [...SOURCE_NAMES, ...SUPPORT_NAMES, ...GENERATED_NAMES]) {
    files.set(name, await readFile(path.join(dir, name)));
  }
  return validatePlan({ plan, setting, seasons, contract, outline, documents, manifest, files });
}

if (process.argv[1] && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href) {
  const result = await validateDirectory(HERE);
  for (const warning of result.warnings) process.stdout.write(`WARN: ${warning}\n`);
  if (!result.ok) {
    for (const error of result.errors) process.stderr.write(`FAIL: ${error}\n`);
    process.stderr.write(`Validation failed with ${result.errors.length} error(s).\n`);
    process.exitCode = 1;
  } else {
    process.stdout.write(`OK: ${result.seasonCount} seasons, ${result.episodeCount} episodes, 12 mysteries, 12 characters validated.\n`);
  }
}
