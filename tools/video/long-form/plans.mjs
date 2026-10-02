// Effective duration revisions over preserved, independently reviewed planning sources.
// No network, production writes, media generation or changes to the source packages.
import { createHash } from "node:crypto";
import { readFileSync, readdirSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

export const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../../..");
export const DIRECTORY = "docs/videos/long-form";
export const CATALOG_COUNTS = { season1: 100, season2: 92, season3: 100, "brand-stories": 100, "ai-terms": 81 };
export const DURATION_NOTE = "長片製作目標10分鐘（600秒）；實際正文及成片至少8分鐘（480秒），片頭片尾不計正文。沿已查核內容補案例、因果步驟與適用界線，不用停頓、重複旁白或拉慢語速補秒；合成後重算章節。";
const digest = (value) => createHash("sha256").update(value).digest("hex");
export const recordHash = (value) => digest(JSON.stringify(value));

export function validatePolicy(policy) {
  const problems = [];
  if (policy?.schema_version !== 1 || policy?.scope !== "KNOWLEDGE_AND_NONFICTION_LONG_FORM") problems.push("invalid duration policy");
  if (policy?.minimum_content_seconds !== 480 || policy?.minimum_final_seconds !== 480) problems.push("both measured minimums must be 480 seconds");
  if (policy?.shorts !== "UNCHANGED") problems.push("Shorts must stay unchanged");
  if (JSON.stringify(Object.keys(policy?.catalogs ?? {}).sort()) !== JSON.stringify(Object.keys(CATALOG_COUNTS).sort())) problems.push("all five catalogs are required");
  for (const [name, count] of Object.entries(CATALOG_COUNTS)) {
    const config = policy?.catalogs?.[name];
    if (config?.expected_entries !== count) problems.push(`${name}: expected ${count} entries`);
    if (!Number.isInteger(config?.target_seconds) || config.target_seconds < 600) problems.push(`${name}: production target must be at least 600 seconds`);
    if (name !== "brand-stories" && config?.target_seconds !== 600) problems.push(`${name}: this revision uses a 600-second production target`);
    if (name === "brand-stories" && config?.target_seconds < 780) problems.push("brand-stories: preserve the existing 13-minute target");
  }
  return problems;
}

// Only explicit duration instructions change. Fact numbers, URLs and Shorts are untouched.
export function reviseDurationText(text) {
  return text.replace(/(?:目標\s*480\s*秒|目標\s*8\s*分鐘|長度\s*8\s*分鐘|風格：扁平插畫解說，8 分鐘)/g,
    (match) => match.startsWith("風格") ? "風格：扁平插畫解說，製作目標10分鐘" : "製作目標600秒")
    .replace(/((?:六章|6章|長片|章節|預估|合計|總長|大綱|企劃)[，、：:／/\s]*)480(?=\s*秒)/g, "$1600")
    .replace(/480(?=\s*秒[／/，、：:\s]*(?:六章|6章|章節|大綱|企劃))/g, "600")
    .replace(/完整八分鐘逐字稿/g, "完整長片逐字稿");
}

export function reviseLongDescription(text) {
  return text.replace(/480(?=-second|\s+seconds|秒|초)/g, (match, index) => {
    const context = text.slice(Math.max(0, index - 40), index + 65);
    return /outline|plan|chapters|六章|6章|企[劃划]|大[綱纲]|構成|构成|台本|기획|개요|구성안/i.test(context) ? "600" : match;
  });
}

export function chapterBudget(durations, target = 600) {
  if (durations.length !== 6 || durations.some((value) => !Number.isInteger(value) || value <= 0)) throw new Error("six positive chapter durations required");
  if (!Number.isInteger(target) || target < 600) throw new Error("chapter target must be at least 600 seconds");
  // Preserve the opening/answer allocations; put the extension into the four explanatory chapters.
  const result = [...durations];
  const available = target - result[0] - result[5];
  const middle = durations.slice(1, 5);
  const original = middle.reduce((a, b) => a + b, 0);
  for (let i = 0; i < 3; i += 1) result[i + 1] = Math.floor(middle[i] * available / original);
  result[4] = available - result.slice(1, 4).reduce((a, b) => a + b, 0);
  if (result.some((value, i) => value < durations[i])) throw new Error("duration revision cannot shorten a chapter");
  return result;
}

export function proposedChapters(source, target = 600) {
  const beforeShorts = source.split("## Shorts")[0];
  const chapters = [];
  const heading = (text) => text.replace(/／\d{2}:\d{2}[–—-]\d{2}:\d{2}(?:／\d+(?: 秒)?)?$/, "");
  for (const line of beforeShorts.split(/\r?\n/)) {
    if (!line.startsWith("| ")) continue;
    const cells = line.split("|").map((cell) => cell.trim());
    const inline = cells[1]?.match(/^[1-6]／.*／(\d+)(?: 秒)?$/);
    if (cells[1] !== "合計" && /^\d+$/.test(cells[2] ?? "")) {
      chapters.push({ heading: heading(cells[1]), original_seconds: Number(cells[2]), content: cells.slice(3, -1).join(" | ") });
    } else if (inline) {
      chapters.push({ heading: heading(cells[1]), original_seconds: Number(inline[1]), content: cells.slice(2, -1).join(" | ") });
    }
  }
  if (chapters.length !== 6 || chapters.reduce((sum, row) => sum + row.original_seconds, 0) !== 480) throw new Error("source six-chapter outline must total 480 seconds");
  const budget = chapterBudget(chapters.map((row) => row.original_seconds), target);
  let start = 0;
  return chapters.map((row, i) => {
    const revised = { heading: row.heading, start_seconds: start, proposed_seconds: budget[i], content: row.content };
    start += budget[i];
    return revised;
  });
}

export function buildPlans(root = ROOT) {
  const bytes = (relative) => readFileSync(path.join(root, relative));
  const json = (relative) => JSON.parse(bytes(relative));
  const policy = json(`${DIRECTORY}/policy.json`);
  const problems = validatePolicy(policy);
  if (problems.length) throw new Error(problems.join("; "));
  const sourceHashes = {};
  const bind = (relative) => {
    sourceHashes[relative] ??= digest(bytes(relative));
    return sourceHashes[relative];
  };
  const entries = [];
  const add = (catalog, record, source, extra = {}) => {
    bind(source);
    entries.push({ catalog, id: record.id, source_status: record.status ?? "reviewed-plan", source, source_record_sha256: recordHash(record),
      target_seconds: policy.catalogs[catalog].target_seconds,
      minimum_content_seconds: policy.minimum_content_seconds, minimum_final_seconds: policy.minimum_final_seconds, ...extra });
  };

  const firstSource = "docs/videos/so-thats-why/episodes.json";
  for (const episode of json(firstSource).episodes) {
    const sourcePackage = `docs/videos/so-thats-why/${episode.fact_check}`;
    const source = bytes(sourcePackage).toString("utf8");
    const blocks = [...source.matchAll(/```text\r?\n([\s\S]*?)\r?\n```/g)].map((match) => match[1]);
    if (blocks.length !== 2) throw new Error(`${episode.id}: first-season premise/note blocks missing`);
    add("season1", episode, firstSource, { video_slug: `sothatswhy-${episode.id.toLowerCase()}`, source_package: sourcePackage, source_package_sha256: bind(sourcePackage),
      stage: "REVIEWED_OUTLINE_NOT_MEDIA", backend_inputs: { style_preset: "flat-explainer", target_minutes: 10, premise: blocks[0], note: reviseDurationText(blocks[1]) } });
  }

  const secondDirectory = "docs/videos/so-thats-why/season2";
  const secondSource = `${secondDirectory}/dispositions.json`;
  const dispositions = json(secondSource);
  const adopted = dispositions.episodes.filter((episode) => episode.decision === "adopt" || episode.decision === "angle");
  if (adopted.length !== 92 || dispositions.episodes.length !== 100 || dispositions.episodes.filter((episode) => episode.decision === "reject-duplicate").length !== 8) throw new Error("season2: expected 92 adopted and eight rejected duplicates");
  const bundles = new Map();
  for (const filename of readdirSync(path.join(root, secondDirectory)).filter((name) => name.endsWith("-packaging.json")).sort()) {
    const relative = `${secondDirectory}/${filename}`;
    bind(relative);
    for (const episode of json(relative).episodes) {
      if (bundles.has(episode.id)) throw new Error(`season2: duplicate package ${episode.id}`);
      bundles.set(episode.id, episode);
    }
  }
  for (const record of adopted) {
    const episode = bundles.get(record.id);
    if (!episode) throw new Error(`season2: missing ${record.id} package`);
    const sourcePackage = `${secondDirectory}/${record.package}`;
    const source = bytes(sourcePackage).toString("utf8");
    if (bind(sourcePackage) !== episode.package_sha256) throw new Error(`${record.id}: stale original package hash`);
    const receipt = `${secondDirectory}/${record.review_receipt}`;
    bind(receipt);
    let chapters;
    try { chapters = proposedChapters(source); } catch (error) { throw new Error(`${record.id}: ${error.message}`); }
    add("season2", record, secondSource, { video_slug: `sothatswhy-${record.id.toLowerCase()}`, source_package: sourcePackage, source_package_sha256: bind(sourcePackage),
      source_review: receipt, stage: "REVIEWED_OUTLINE_NOT_MEDIA", proposed_chapters: chapters,
      backend_inputs: { style_preset: "flat-explainer", target_minutes: 10, premise: episode.backend_inputs.premise, note: `${reviseDurationText(episode.backend_inputs.note)}\n${DURATION_NOTE}` },
      localizations: Object.fromEntries(Object.entries(episode.localizations).map(([locale, fields]) => [locale, { ...fields, description: reviseLongDescription(fields.description) }])),
      shorts_sha256: recordHash(episode.shorts), shorts_source: record.package });
  }

  const thirdSource = "docs/videos/so-thats-why/season3-topics.json";
  for (const episode of json(thirdSource).episodes) {
    const sourceCheck = `docs/videos/so-thats-why/${episode.check}`;
    bind(sourceCheck);
    add("season3", episode, thirdSource, { video_slug: `sothatswhy-${episode.id.toLowerCase()}`, stage: "CHECKED_CANDIDATE_REQUIRES_OUTLINE", source_check: sourceCheck });
  }

  const storySource = "docs/videos/story-plans/brand-stories-100/stories.json";
  const stories = json(storySource);
  if (stories.series.target_minutes * 60 !== policy.catalogs["brand-stories"].target_seconds) throw new Error("brand-stories: target must match the existing story series");
  for (const story of stories.stories) add("brand-stories", story, storySource, { video_slug: story.slug, stage: "REVIEWED_STORY_PLAN_NOT_MEDIA", target_range_seconds: [720, 900] });

  const termsSource = "docs/videos/ai-terms/terms.json";
  const terms = json(termsSource);
  for (const term of terms.terms) add("ai-terms", term, termsSource, { video_slug: term.video_slug, stage: term.status === "covered" ? "COVERED_DO_NOT_REMAKE" : "TERM_PLAN_NOT_MEDIA",
    target_range_seconds: terms.series.target_minutes.map((minutes) => minutes * 60), existing_videos: term.existing_videos });

  for (const [catalog, count] of Object.entries(CATALOG_COUNTS)) {
    const rows = entries.filter((entry) => entry.catalog === catalog);
    if (rows.length !== count || new Set(rows.map((row) => row.id)).size !== count) throw new Error(`${catalog}: expected ${count} unique entries`);
    for (const row of rows) {
      if (!row.id || !row.video_slug) throw new Error(`${catalog}: entry lacks an ID/slug`);
      if (row.backend_inputs && (row.backend_inputs.premise.length > 4000 || row.backend_inputs.note.length > 2000)) throw new Error(`${row.id}: effective backend fields exceed limits`);
      if (row.target_range_seconds?.some((value) => !Number.isFinite(value) || value < 480)) throw new Error(`${row.id}: target range below eight minutes`);
    }
  }
  return { schema_version: 1, revision: policy.revision, status: "DURATION_PLANS_ONLY", writing_instructions: DURATION_NOTE, policy_sha256: bind(`${DIRECTORY}/policy.json`),
    totals: { entries: entries.length, catalogs: CATALOG_COUNTS, excluded_season2_duplicates: 8, covered_ai_terms: entries.filter((entry) => entry.stage === "COVERED_DO_NOT_REMAKE").length },
    media_generated: false, actual_duration_verified: false, platform_imported: false, published: false,
    source_hashes: Object.fromEntries(Object.entries(sourceHashes).sort(([a], [b]) => a.localeCompare(b))), entries };
}

export function findPlan(plans, catalog, id, { forProduction = false } = {}) {
  const entry = plans.entries.find((row) => row.catalog === catalog && row.id === id);
  if (!entry) throw new Error(`unknown long-form plan ${catalog}/${id}`);
  if (forProduction && entry.stage === "COVERED_DO_NOT_REMAKE") throw new Error(`${catalog}/${id} is covered; do not schedule a duplicate`);
  return entry;
}

export function validatePlans(actual, expected) {
  const problems = [];
  if (actual?.media_generated !== false || actual?.actual_duration_verified !== false || actual?.platform_imported !== false || actual?.published !== false) problems.push("duration planning must not assert media or production acceptance");
  if (JSON.stringify(actual) !== JSON.stringify(expected)) problems.push("plans differ from current sources or duration policy; rebuild and review the revision");
  return problems;
}
