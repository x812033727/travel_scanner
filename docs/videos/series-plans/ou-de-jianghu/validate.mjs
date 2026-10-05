#!/usr/bin/env node
// Local planning checks. These do not measure screenplay minutes, originality,
// narrative meaning, legal consent, animation quality, or production readiness.
import { readFile } from "node:fs/promises";
import { readFileSync } from "node:fs";
import { createHash } from "node:crypto";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { isDeepStrictEqual } from "node:util";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const CONTRACT = JSON.parse(readFileSync(path.join(HERE, "authoring-contract.json"), "utf8"));
const TOTAL = 24;
const SEASONS = 2;
const PER_SEASON = 12;
const ENDINGS = new Set(["danger", "reveal", "choice", "reversal", "emotion"]);
const STATE_FIELDS = ["time", "knowledge", "character_state", "evidence", "carry_forward"];
const TEXT_FIELDS = ["title", "logline", "hook", "conflict", "turn", "theme", "consequence"];
const isObject = (value) => value !== null && typeof value === "object" && !Array.isArray(value);
const isText = (value) => typeof value === "string" && value.trim().length > 0;
const same = isDeepStrictEqual;
const asArray = (value) => Array.isArray(value) ? value : [];
const SOURCE_NAMES = ["authoring-contract.json", "plan.json", "setting.json", ...Array.from({ length: SEASONS }, (_, index) => `season-${String(index + 1).padStart(2, "0")}.json`)];
const SUPPORT_NAMES = ["README.md", "review.md", "build.mjs", "validate.mjs", "validate.test.mjs"];
const GENERATED_NAMES = ["setting.md", "outline.md", ...Array.from({ length: SEASONS }, (_, index) => `season-${String(index + 1).padStart(2, "0")}.md`), "outline.json", "documents.json", "continuity.md", "continuity.csv"];
const digest = (value) => createHash("sha256").update(value).digest("hex");

/** Validate source data; optional derived documents are compared with their sources. */
export function validatePlan({ plan, setting, seasons, contract = CONTRACT, outline, documents, manifest, files } = {}) {
  const errors = [];
  const warnings = [
    "本地企劃結構驗證不等於可匯入；production_support.ready_for_import 必須保留 false。",
    "22 分鐘是正文規劃預算，尚未提供或量測完整台詞、分鏡及媒體。",
    "第一期是開放結局：三條保留謎團留給續期，不代表全系列已規劃到可製作。",
    "原創性、伏筆是否真有意義、張力強度與終局是否留下新危機，仍需人工審讀。",
  ];
  const check = (condition, message) => { if (!condition) errors.push(message); };
  const stringList = (value, label, { allowEmpty = false, known } = {}) => {
    if (!Array.isArray(value)) { errors.push(`${label} 必須是陣列。`); return []; }
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
  check(contract.category === "anime" && contract.style_preset === "anime-2d", "authoring contract 必須維持 anime／anime-2d。");
  check(contract.planned_episodes === TOTAL && contract.episodes_per_season === PER_SEASON, `authoring contract 必須維持 ${TOTAL} 集、每季 ${PER_SEASON} 集。`);
  check(contract.story_minutes === 22 && contract.broadcast_minutes === 30, "authoring contract 必須維持正文 22、播出 30 分鐘。");
  check(same(contract.state_fields, STATE_FIELDS), "authoring contract.state_fields 必須完整定義五個連貫狀態欄位。");

  check(plan.artifact_kind === "anime-series-plan", "plan.artifact_kind 必須是 anime-series-plan。");
  check(plan.category === "anime", "plan.category 必須是 anime。");
  check(plan.style_preset === "anime-2d", "plan.style_preset 必須是 anime-2d。");
  check(plan.video_defaults?.category === "anime", "video_defaults.category 必須是 anime。");
  check(plan.video_defaults?.look?.preset === "anime-2d", "video_defaults.look.preset 必須是 anime-2d。");
  check(plan.kind === "series", "plan.kind 必須是 series。");
  check(plan.genre === "custom", "plan.genre 必須保留 custom，不得改題材繞過工人限制。");
  check(plan.lead === "ensemble", "plan.lead 必須保留 ensemble。");
  check(plan.open_ended === true, "plan.open_ended 必須是 true：第一期收完無歸箭的故事線，保留謎團給續期。");
  check(plan.planned_episodes === TOTAL, `plan.planned_episodes 必須是 ${TOTAL}。`);
  check(plan.season_count === SEASONS, `plan.season_count 必須是 ${SEASONS}。`);
  check(plan.episodes_per_chapter === PER_SEASON, `plan.episodes_per_chapter 必須是 ${PER_SEASON}。`);
  check(plan.runtime?.story_minutes === 22, "runtime.story_minutes 必須是 22，不得縮水。");
  check(plan.runtime?.broadcast_slot_minutes === 30, "runtime.broadcast_slot_minutes 必須是 30。");
  const runtime = plan.runtime ?? {};
  check(Number.isFinite(runtime.op_ed_budget_minutes) && runtime.op_ed_budget_minutes >= 0, "OP/ED 預算必須為非負分鐘數。");
  check(Number.isFinite(runtime.broadcast_slot_reserve_minutes) && runtime.broadcast_slot_reserve_minutes >= 0, "播出保留預算必須為非負分鐘數。");
  check(runtime.story_minutes + runtime.op_ed_budget_minutes + runtime.broadcast_slot_reserve_minutes === 30, "正文、OP/ED 與播出保留分鐘數必須合計 30。");

  const support = plan.production_support;
  check(isObject(support), "production_support 必須是物件，不能省略生產限制。");
  for (const key of ["ready_for_import", "admin_series_created", "media_generated", "published"])
    check(support?.[key] === false, `production_support.${key} 必須保持 false。`);
  const gaps = Array.isArray(support?.gaps) ? support.gaps : [];
  check(gaps.length > 0, "production_support.gaps 必須誠實保留未支援項目。");
  check(gaps.every((gap) => isObject(gap) && isText(gap.code) && isText(gap.note)), "每個 production gap 都需要 code 與具體 note。");
  check(new Set(gaps.map((gap) => gap?.code)).size === gaps.length, "production_support.gaps 的 code 不得重複。");
  const durationGap = gaps.find((gap) => gap?.code === "episode-duration");
  check(durationGap?.required_story_minutes === 22 && durationGap?.current_drama_max_minutes === 8, "episode-duration gap 必須保留 22 分鐘需求與目前 8 分鐘上限。");
  check(gaps.find((gap) => gap?.code === "ensemble-retention")?.current_genre === "custom", "ensemble-retention gap 必須保留 custom 工人政策未相符的限制。");
  const budgetGap = gaps.find((gap) => gap?.code === "episode-budget");
  check(Number.isFinite(budgetGap?.shots_per_episode) && budgetGap.shots_per_episode > 0 && isText(budgetGap?.note), "episode-budget gap 必須記錄每集鏡頭數與成本估算的依據。");
  for (const gap of gaps) if (isText(gap?.note)) warnings.push(`未解 production gap [${gap.code}]：${gap.note}`);

  const cast = Array.isArray(setting.characters) ? setting.characters : [];
  check(cast.length > 0, "setting.characters 不得為空。");
  const castIds = new Set();
  for (const character of cast) {
    check(isObject(character) && ["id", "name", "appearance"].every((key) => isText(character?.[key])), "每位角色必須有非空 id/name/appearance。");
    check(/^[a-z][a-z0-9-]{1,23}$/.test(character?.id ?? ""), `角色 ID ${JSON.stringify(character?.id)} 格式錯誤。`);
    check(!castIds.has(character?.id), `重複角色 ID ${JSON.stringify(character?.id)}。`);
    if (isText(character?.id)) castIds.add(character.id);
  }
  for (const id of stringList(contract.character_ids, "contract.character_ids")) check(castIds.has(id), `setting 缺少約定角色 ${id}。`);
  check(same([...castIds].sort(), asArray(contract.character_ids).slice().sort()), "setting／contract 的角色 ID 清單必須一致。");
  const mysteries = Array.isArray(setting.mysteries) ? setting.mysteries : [];
  check(mysteries.length > 0, "setting.mysteries 不得為空。");
  const threads = new Map();
  for (const mystery of mysteries) {
    check(isObject(mystery) && ["id", "question", "answer"].every((key) => isText(mystery?.[key])), "每條長線必須有非空 id/question/answer。");
    check(!threads.has(mystery?.id), `重複 thread ID ${JSON.stringify(mystery?.id)}。`);
    check(Number.isInteger(mystery?.introduced_in) && mystery.introduced_in >= 1 && mystery.introduced_in <= TOTAL, `thread ${mystery?.id} introduced_in 必須在 1–${TOTAL}。`);
    if (mystery?.resolved_in === null) check(mystery?.reserved === true, `thread ${mystery?.id} resolved_in 為 null 時必須標 reserved=true（保留給續期）。`);
    else check(Number.isInteger(mystery?.resolved_in) && mystery.resolved_in >= mystery.introduced_in && mystery.resolved_in <= TOTAL && mystery?.reserved !== true, `thread ${mystery?.id} resolved_in 必須介於引入集與 ${TOTAL}，且不得同時 reserved。`);
    if (isText(mystery?.id)) threads.set(mystery.id, mystery);
  }
  for (const id of stringList(contract.thread_ids, "contract.thread_ids")) check(threads.has(id), `setting 缺少約定 thread ${id}。`);
  check(same([...threads.keys()].sort(), asArray(contract.thread_ids).slice().sort()), "setting／contract 的 thread ID 清單必須一致。");
  check(setting.finale?.closed === false, "setting.finale.closed 必須是 false：第一期開放結局。");
  check(setting.finale?.new_crisis_or_sequel_hook === true, "setting.finale.new_crisis_or_sequel_hook 必須是 true，誠實宣告保留的續期鉤子。");
  check(isText(setting.finale?.last_line), "setting.finale.last_line 必須是非空台詞。");
  check(isText(setting.finale?.summary), "setting.finale.summary 必須寫出第一期收了哪些線。");
  stringList(setting.finale?.permanent_costs, "setting.finale.permanent_costs");
  const reservedIds = stringList(setting.finale?.reserved_mysteries, "setting.finale.reserved_mysteries", { known: threads });
  check(reservedIds.length >= 3, "第一期至少保留 3 條謎團給續期。");
  for (const [id, thread] of threads) check((thread.reserved === true) === reservedIds.includes(id), `thread ${id} 的 reserved 標記必須與 finale.reserved_mysteries 一致。`);

  check(seasons.length === SEASONS, `必須有 ${SEASONS} 季，目前 ${seasons.length} 季。`);
  const episodes = [];
  for (const [seasonIndex, season] of seasons.entries()) {
    const seasonNumber = seasonIndex + 1;
    check(isObject(season), `season[${seasonIndex}] 必須是物件。`);
    check(season?.number === seasonNumber, `season[${seasonIndex}].number 必須是 ${seasonNumber}。`);
    for (const key of ["title", "theme", "core_conflict", "time_span", "season_resolution", "season_hook"])
      check(isText(season?.[key]), `第 ${seasonNumber} 季缺少非空 ${key}。`);
    const rows = Array.isArray(season?.episodes) ? season.episodes : [];
    check(rows.length === PER_SEASON, `第 ${seasonNumber} 季必須恰好 ${PER_SEASON} 集，目前 ${rows.length} 集。`);
    for (const [index, episode] of rows.entries()) {
      const expected = seasonIndex * PER_SEASON + index + 1;
      const label = `第 ${seasonNumber} 季 episode[${index}]／E${episode?.number ?? "?"}`;
      check(isObject(episode), `${label} 必須是物件。`);
      check(episode?.number === expected, `${label} 全劇集號必須是 ${expected}，不得重排或換季。`);
      if (!isObject(episode)) continue;
      episodes.push(episode);
      for (const key of TEXT_FIELDS) check(isText(episode[key]), `${label}.${key} 必須是非空字串。`);
      for (const key of asArray(contract.episode_fields)) check(Object.hasOwn(episode, key), `${label} 缺少約定欄位 ${key}。`);
      const tension = episode.tension;
      check(Array.isArray(tension) && tension.length === 5 && tension.every((value) => Number.isInteger(value) && value >= 1 && value <= 5), `${label}.tension 必須是五段 1–5 的整數曲線。`);
      check(isObject(episode.cliffhanger) && ENDINGS.has(episode.cliffhanger.type) && isText(episode.cliffhanger.text), `${label}.cliffhanger 必須有允許的 type 與非空 text。`);
      check(episode.closed_ending === false, `${label}.closed_ending 必須是 false：第一期沒有封閉收束，E${TOTAL} 以懸念接續期。`);
      check(Array.isArray(tension) && tension.at(-1) >= 4, `${label} 末段張力必須 >=4。`);
      check(Array.isArray(tension) && new Set(tension).size > 1, `${label} 五段張力不能一路平。`);
      stringList(episode.characters, `${label}.characters`, { known: castIds });
      stringList(episode.locations, `${label}.locations`);
      stringList(episode.setups, `${label}.setups`, { allowEmpty: true, known: threads });
      stringList(episode.payoffs, `${label}.payoffs`, { allowEmpty: true, known: threads });
      if (Object.hasOwn(episode, "general_payoffs")) stringList(episode.general_payoffs, `${label}.general_payoffs`, { allowEmpty: true });
      const beats = Array.isArray(episode.high_tension) ? episode.high_tension : [];
      check(beats.length === 2, `${label}.high_tension 必須恰好兩段。`);
      for (const [beatIndex, beat] of beats.entries()) {
        check(isObject(beat), `${label}.high_tension[${beatIndex}] 必須是物件。`);
        check(beat?.beat === ["first_half", "second_half"][beatIndex], `${label}.high_tension 必須先 first_half 後 second_half。`);
        for (const key of ["event", "stakes", "consequence"]) check(isText(beat?.[key]), `${label}.high_tension[${beatIndex}].${key} 必須非空。`);
      }
      for (const key of STATE_FIELDS) check(isText(episode.state?.[key]), `${label}.state.${key} 必須是非空字串。`);
    }
  }
  check(episodes.length === TOTAL, `必須有 ${TOTAL} 集，目前 ${episodes.length} 集。`);
  const numbers = episodes.map((episode) => episode.number);
  check(new Set(numbers).size === numbers.length, "全劇集號含重複值。");
  check(same(numbers, Array.from({ length: TOTAL }, (_, index) => index + 1)), `全劇集號必須依序且唯一涵蓋 1–${TOTAL}。`);
  for (let index = 1; index < episodes.length; index++)
    check(episodes[index - 1].cliffhanger?.type !== episodes[index].cliffhanger?.type, `E${episodes[index - 1].number}／E${episodes[index].number} 相鄰 ending type 不得相同。`);
  for (let index = 0; index + 4 <= episodes.length; index++) {
    const window = episodes.slice(index, index + 4);
    check(window.some((episode) => asArray(episode.payoffs).length > 0 || asArray(episode.general_payoffs).some(isText)), `E${window[0].number}–E${window[3].number} 四集窗口缺少具體一般成果或長線部分回收。`);
  }
  for (const [id, thread] of threads) {
    const setups = episodes.filter((episode) => asArray(episode.setups).includes(id));
    const payoffs = episodes.filter((episode) => asArray(episode.payoffs).includes(id));
    check(setups.length > 0, `thread ${id} 沒有實際 setup。`);
    if (thread.reserved !== true) check(payoffs.length > 0, `thread ${id} 沒有實際 payoff。`);
    // This registry defines introduced_in as the earliest seed, not the first
    // explicit question. Reclassify local facts rather than silently retagging it.
    for (const episode of [...setups, ...payoffs]) check(episode.number >= thread.introduced_in, `E${episode.number} thread ${id} 早於 introduced_in=${thread.introduced_in}，不可提前埋回。`);
    for (const episode of payoffs) check(setups.some((setup) => setup.number <= episode.number), `E${episode.number} thread ${id} 先 payoff 後 setup。`);
    if (thread.reserved !== true) check(payoffs.some((episode) => episode.number === thread.resolved_in), `thread ${id} resolved_in=${thread.resolved_in} 當集沒有對應 payoff。`);
    else check(setups.some((episode) => episode.number === thread.introduced_in), `保留的 thread ${id} 必須在 introduced_in=${thread.introduced_in} 當集實際埋下。`);
  }

  if (outline !== undefined) {
    check(isObject(outline) && Array.isArray(outline.chapters), "outline.chapters 必須是陣列。");
    check(outline?.chapters?.length === SEASONS, `outline 必須對應 ${SEASONS} 季。`);
    for (const [index, chapter] of asArray(outline?.chapters).entries()) {
      const source = seasons[index];
      check(chapter?.number === source?.number && chapter?.theme === source?.theme, `outline 第 ${index + 1} 季 number／theme 偏離 source。`);
      check(chapter?.title === source?.title, `outline 第 ${index + 1} 季標題偏離 source。`);
      const summary = (rows) => asArray(rows).map((row) => ({ number: row?.number, title: row?.title, logline: row?.logline }));
      check(same(summary(chapter?.episodes), summary(source?.episodes)), `outline 第 ${index + 1} 季集號／標題／logline 偏離 source。`);
    }
  }

  if (documents !== undefined) {
    check(isObject(documents), "documents 必須是物件。");
    check(documents?.schema_version === 1 && documents?.stage === "planning", "documents 必須是 schema_version=1 的 planning 文件。");
    check(documents?.ready_for_import === false && documents?.category === "anime", "documents 必須維持 anime 與 ready_for_import=false。");
    const rows = asArray(documents?.documents);
    check(rows.length === SEASONS + 2, `documents 必須包含 1 份 setting、1 份 outline 與 ${SEASONS} 份 chapter。`);
    const expected = [
      { kind: "setting", body: setting, markdown: "setting.md" },
      { kind: "outline", body: outline, markdown: "outline.md" },
      ...seasons.map((season, index) => ({ kind: "chapter", chapter: index + 1, body: season, markdown: `season-${String(index + 1).padStart(2, "0")}.md` })),
    ];
    for (const [index, document] of rows.entries()) {
      const target = expected[index];
      check(isObject(document) && document.kind === target?.kind, `documents[${index}] kind／順序不符來源。`);
      if (!target) continue;
      if (target.kind === "chapter") check(document?.chapter_number === target.chapter, `documents[${index}] chapter_number 不符來源。`);
      check(same(document?.body_json, target.body), `documents[${index}].body_json 偏離來源 ${target.markdown}。`);
      check(isText(document?.body_md), `documents[${index}].body_md 必須是實際非空 Markdown。`);
      if (files !== undefined) check(document?.body_md === files?.[target.markdown], `documents[${index}].body_md 不等於實際 ${target.markdown}。`);
    }
    if (files === undefined) warnings.push("未提供原始檔案 bytes；documents 的 body_md 只能驗非空，尚未比對實際 Markdown。");
  }

  if (manifest !== undefined) {
    check(isObject(manifest), "manifest 必須是物件。");
    check(manifest?.schema_version === 1 && manifest?.artifact_kind === plan.artifact_kind && manifest?.slug === plan.slug, "manifest 版本／kind／slug 必須與 plan 相符。");
    check(manifest?.category === "anime" && manifest?.episode_count === TOTAL && manifest?.season_count === SEASONS, `manifest 必須宣告 anime、${TOTAL} 集、${SEASONS} 季。`);
    for (const key of ["ready_for_import", "admin_series_created", "media_generated", "published"]) check(manifest?.[key] === false, `manifest.${key} 必須保持 false。`);
    for (const [field, names] of [["source_files", SOURCE_NAMES], ["support_files", SUPPORT_NAMES], ["generated_files", GENERATED_NAMES]]) {
      const entries = isObject(manifest?.[field]) ? manifest[field] : {};
      check(same(Object.keys(entries).sort(), [...names].sort()), `manifest.${field} 清單缺失或新增未約定檔案。`);
      for (const [name, hash] of Object.entries(entries)) {
        check(/^[a-f0-9]{64}$/.test(hash), `manifest.${field}.${name} 必須是 SHA256。`);
        if (files !== undefined) {
          const raw = files?.[name];
          check(typeof raw === "string" || Buffer.isBuffer(raw), `manifest 雜湊檢查缺少實際檔案 ${name}。`);
          if (typeof raw === "string" || Buffer.isBuffer(raw)) check(digest(raw) === hash, `manifest 雜湊不符：${name}；修改來源後須重新 build。`);
        }
      }
    }
    if (files === undefined) warnings.push("未提供原始檔案 bytes；manifest 只驗清單與宣告，SHA256 尚未核對。");
  }
  if (files !== undefined) {
    const sourceValues = { "plan.json": plan, "setting.json": setting, "authoring-contract.json": contract, ...Object.fromEntries(seasons.map((season, index) => [`season-${String(index + 1).padStart(2, "0")}.json`, season])) };
    for (const [name, value] of Object.entries(sourceValues)) {
      try { check(same(JSON.parse(files[name]), value), `傳入來源與實際 ${name} 不一致。`); }
      catch { errors.push(`實際 ${name} 缺少可讀 JSON，不能驗證來源。`); }
    }
    for (const [name, value] of [["outline.json", outline], ["documents.json", documents], ["manifest.json", manifest]]) {
      if (value === undefined) continue;
      try { check(same(JSON.parse(files[name]), value), `傳入衍生資料與實際 ${name} 不一致。`); }
      catch { errors.push(`實際 ${name} 缺少可讀 JSON。`); }
    }
  }
  return { errors, warnings, episode_count: episodes.length, season_count: seasons.length };
}

/** Keep local-file loading separate from data validation for meaningful mutation tests. */
export async function loadPlan(directory = HERE, { sourcesOnly = false } = {}) {
  const errors = [];
  const files = {};
  const read = async (name) => {
    try { files[name] = await readFile(path.join(directory, name), "utf8"); return JSON.parse(files[name]); }
    catch (error) { errors.push(`${name}: ${error.message}`); return null; }
  };
  const [plan, setting, contract, ...seasons] = await Promise.all([
    read("plan.json"), read("setting.json"), read("authoring-contract.json"),
    ...Array.from({ length: SEASONS }, (_, index) => read(`season-${String(index + 1).padStart(2, "0")}.json`)),
  ]);
  const data = { plan, setting, contract, seasons, files };
  if (!sourcesOnly) {
    [data.outline, data.documents, data.manifest] = await Promise.all([read("outline.json"), read("documents.json"), read("manifest.json")]);
    await Promise.all([...GENERATED_NAMES, ...SUPPORT_NAMES].filter((name) => !Object.hasOwn(files, name)).map(async (name) => {
      try { files[name] = await readFile(path.join(directory, name), "utf8"); }
      catch (error) { errors.push(`${name}: ${error.message}`); }
    }));
  }
  return { data, errors };
}

/** Real worker checks, reported separately from structural-only document shape. */
export async function workerCompatibility({ plan, documents }) {
  const { documentProblem } = await import(new URL("../../../../tools/video/automation/series.mjs", import.meta.url));
  const actualSeries = { ...plan, chapters: SEASONS };
  const { genre, ...structuralSeries } = actualSeries;
  return {
    scope: "本地 documentProblem，未呼叫 API、未匯入、未製作；純結構工作參數省略 genre，實際工人參數保留 plan.genre。",
    results: asArray(documents?.documents).map((document) => ({
      kind: document.kind,
      ...(document.kind === "chapter" ? { chapter_number: document.chapter_number } : {}),
      structural_only_problem: documentProblem(document.kind, document, { series: structuralSeries, chapter_number: document.chapter_number }),
      actual_worker_problem: documentProblem(document.kind, document, { series: actualSeries, chapter_number: document.chapter_number }),
    })),
  };
}

async function main(args) {
  if (args.includes("--help")) {
    console.log("Usage: node validate.mjs [directory] [--json] [--sources-only] [--worker-compatibility]\nLocal plan validation only; no network or import operations.\nDefault checks sources, derived documents and manifest hashes; --sources-only is for pre-build checks.\nWorker compatibility reports structural-only checks separately from the actual plan's genre policy.");
    return;
  }
  const positional = args.filter((arg) => !arg.startsWith("--"));
  const unknown = args.filter((arg) => arg.startsWith("--") && !["--json", "--sources-only", "--worker-compatibility"].includes(arg));
  if (unknown.length || positional.length > 1) {
    console.error(`Unknown arguments: ${args.join(" ")}`);
    process.exitCode = 1;
    return;
  }
  if (args.includes("--sources-only") && args.includes("--worker-compatibility")) {
    console.error("--worker-compatibility requires generated documents; do not combine it with --sources-only.");
    process.exitCode = 1;
    return;
  }
  const { data, errors: loadErrors } = await loadPlan(positional[0] ? path.resolve(positional[0]) : HERE, { sourcesOnly: args.includes("--sources-only") });
  const result = validatePlan(data);
  result.errors.unshift(...loadErrors);
  if (args.includes("--sources-only")) result.warnings.push("只驗來源；尚未核對衍生 Markdown、documents 與 manifest。");
  if (args.includes("--worker-compatibility")) {
    if (result.errors.length) result.warnings.push("來源或衍生文件尚未通過；略過工人相容檢查。");
    else {
      try { result.worker_compatibility = await workerCompatibility(data); }
      catch (error) { result.errors.push(`本地工人相容檢查無法完成：${error.message}`); }
    }
  }
  if (args.includes("--json")) console.log(JSON.stringify(result, null, 2));
  else {
    console.log(`企劃檢查：${result.season_count} 季／${result.episode_count} 集；${result.errors.length} 項錯誤。`);
    for (const error of result.errors) console.error(`ERROR: ${error}`);
    for (const warning of result.warnings) console.warn(`WARNING: ${warning}`);
    if (result.worker_compatibility) {
      console.log(result.worker_compatibility.scope);
      for (const row of result.worker_compatibility.results) console.log(`${row.kind}${row.chapter_number ? ` ${row.chapter_number}` : ""}: structural-only=${row.structural_only_problem ?? "pass"}; actual-worker=${row.actual_worker_problem ?? "pass"}`);
    }
    console.log(result.errors.length ? "未通過本地結構驗證。" : "本地結構驗證通過；不是可匯入或可製作的完成證明。");
  }
  process.exitCode = result.errors.length ? 1 : 0;
}

if (process.argv[1] && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href)
  await main(process.argv.slice(2));
