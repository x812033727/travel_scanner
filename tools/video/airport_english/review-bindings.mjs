#!/usr/bin/env node
// Bind real independent text reviews to current generated sources; never create approvals.
import { createHash } from "node:crypto";
import { existsSync, readFileSync, readdirSync, writeFileSync } from "node:fs";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { parseArgs } from "node:util";

import { ROOT } from "../core/paths.mjs";
import { lintProject, loadProject } from "../core/state.mjs";
import { LOCALES, prepareLesson, PRODUCTION } from "./prepare.mjs";

export const sha256 = (bytes) => createHash("sha256").update(bytes).digest("hex");
const readJson = (file) => JSON.parse(readFileSync(file, "utf8"));
const jsonBytes = (value) => `${JSON.stringify(value, null, 2)}\n`;
const sorted = (value) => Array.isArray(value) ? value.map(sorted) : value && typeof value === "object" ? Object.fromEntries(Object.keys(value).sort().map((key) => [key, sorted(value[key])])) : value;
export const canonical = (value) => JSON.stringify(sorted(value));
export const contentHash = (lesson) => sha256(canonical(Object.fromEntries(["A", "B", "quiz", "guides", "title_all"].map((key) => [key, lesson[key]]))));
export function englishContentHash(lesson) {
  return sha256(canonical({ ...Object.fromEntries(["A", "B"].map((key) => [key, lesson[key].map(({ id, text }) => ({ id, text }))])), quiz: lesson.quiz.map(({ question, choices, answer }) => ({ question, choices, answer })), guides: Object.fromEntries(Object.entries(lesson.guides).map(([key, value]) => [key, value[0]])) }));
}
export function sharedInstructionsHash(result) {
  return sha256(canonical({
    coaches: result.entries.filter((entry) => entry.semantic_key.startsWith("coach-")).map(({ semantic_key, all }) => ({ semantic_key, all })),
    chapters: result.doc.scenes.filter((scene) => scene.chapter).map((scene) => [scene.chapter, ...LOCALES.slice(1).map((locale) => result.translations[locale].chapters[scene.id])]),
    disclaimers: [result.doc.youtube.description, ...LOCALES.slice(1).map((locale) => result.translations[locale].description)].map((text) => text.split("\n\n").at(-1)),
  }));
}

export function preparedArtifacts(lesson, result) {
  const values = { "video.json": result.doc, "teaching-audio.json": result.teachingAudio, "caption-plan.json": result.captionPlan, "duration-plan.json": result.duration, "metadata-plan.json": result.metadata, "line-map.json": { schema_version: 1, lesson_sha256: sha256(JSON.stringify(lesson)), lines: result.entries.map(({ all, ...entry }) => entry) } };
  return { ...Object.fromEntries(Object.entries(values).map(([name, value]) => [name, jsonBytes(value)])), "brief.md": result.brief, "claims.md": result.claims, ...Object.fromEntries(Object.entries(result.translations).map(([locale, value]) => [`i18n/${locale}.json`, jsonBytes(value)])) };
}

function editorialReport(day) {
  if (day === 1) return { file: "verify-day01.md", reviewer: "airport_lessons_02_21" };
  if (day <= 21) return { file: "verify-02-21.md", reviewer: "airport_lessons_42_60" };
  if (day <= 41) return { file: "verify-22-41.md", reviewer: "airport_lessons_02_21" };
  return { file: "verify-42-60.md", reviewer: "airport_lessons_22_41" };
}

export function editorialContentHash(markdown, day) {
  const matches = day === 1
    ? [...markdown.matchAll(/^Spoken-content SHA-256:\s*`([a-f0-9]{64})`\s*$/gm)].map((match) => match[1])
    : [...markdown.matchAll(/^\|\s*(?:day)?(\d{1,2})(?:\.json)?\s*\|\s*`([a-f0-9]{64})`\s*\|\s*`[a-f0-9]{64}`\s*\|\s*$/gm)].filter((match) => Number(match[1]) === day).map((match) => match[2]);
  if (matches.length !== 1) throw new Error(`Day ${day}: independent editorial content hash is missing or ambiguous`);
  return matches[0];
}

export function editorialReviewRecord(markdown, day, shared = null) {
  const matches = [...markdown.matchAll(/<!-- airport-editorial-review-v1\s+(\{[^\n]+\})\s+-->/g)];
  // The original Day02–21 reviewer is no longer available. A separate reviewer
  // recorded the exact existing PASS-report bytes, without signing on their behalf.
  if (matches.length === 0 && day >= 2 && day <= 21) {
    const recorded = shared?.existing_editorial_report;
    if (recorded?.path !== "verify-02-21.md" || recorded.recorded_by !== "airport_claims_review" || recorded.original_reviewer !== "airport_lessons_42_60" || recorded.recorded_decision !== "text_review_passed" || recorded.report_sha256 !== sha256(markdown)) throw new Error(`Day ${day}: existing editorial PASS report differs from independently recorded evidence`);
    if (!markdown.includes("Reviewer: `/root/airport_lessons_42_60` (AI)") || !markdown.includes("Result: the revised text passes this independent editorial check, with the corrections below applied and re-read.")) throw new Error(`Day ${day}: recorded editorial reviewer or PASS decision is missing`);
    return { schema_version: 1, decision: "text_review_passed", reviewer: recorded.original_reviewer, attestation_kind: "existing_report_recorded_by_separate_reviewer", recorded_by: recorded.recorded_by, content_hashes: { [String(day)]: editorialContentHash(markdown, day) } };
  }
  if (matches.length !== 1) throw new Error(`Day ${day}: current independent editorial decision is missing or ambiguous`);
  const record = JSON.parse(matches[0][1]), assigned = editorialReport(day);
  if (record.schema_version !== 1 || record.decision !== "text_review_passed" || record.reviewer !== assigned.reviewer) throw new Error(`Day ${day}: independent editorial decision or reviewer is not current and accepted`);
  const hash = editorialContentHash(markdown, day);
  if (record.content_hashes?.[String(day)] !== hash) throw new Error(`Day ${day}: current editorial attestation differs from reviewed content hash`);
  return record;
}

export function sharedReviewRecord(markdown) {
  const matches = [...markdown.matchAll(/<!-- airport-shared-review-v1\s+(\{[^\n]+\})\s+-->/g)];
  if (matches.length !== 1) throw new Error("Shared review must contain one independently written binding record");
  const record = JSON.parse(matches[0][1]);
  if (record.schema_version !== 1 || record.decision !== "text_review_passed" || record.reviewer !== "airport_claims_review" || !/^[a-f0-9]{64}$/.test(record.shared_instructions_sha256)) throw new Error("Shared review binding record is incomplete");
  return record;
}

const cleanCell = (value) => String(value ?? "").replace(/[|｜]/g, "/").replace(/\s+/g, " ").trim();
const sortedClaims = (claims) => claims.map((claim) => ({ ...claim, source_urls: [...claim.source_urls].sort() })).sort((a, b) => a.id.localeCompare(b.id));
const sortedSources = (sources) => [...sources].sort((a, b) => a.url.localeCompare(b.url));
const ACCEPTED = new Set(["fictional_scenario_not_external_fact", "supported", "supported_with_existing_qualification", "supported_as_conditional_scenario", "supported_in_warning_context", "supported_as_help_seeking_not_treatment", "supported_as_fictional_truthful_role_play", "supported_as_local_scenario", "correction_verified"]);

export function planReviewBinding({ production = PRODUCTION, day }) {
  if (!Number.isInteger(day) || day < 1 || day > 60) throw new Error("day must be 1 through 60");
  const name = `day${String(day).padStart(2, "0")}`, dir = path.join(production, name);
  const lessonBytes = readFileSync(path.join(production, "lessons", `${name}.json`));
  const lesson = JSON.parse(lessonBytes), profile = readJson(path.join(production, "profile.json"));
  if (lesson.day !== day) throw new Error(`${name}: lesson identity mismatch`);
  const editorial = editorialReport(day);
  if (lesson.editorial_review !== `reviews/${editorial.file}`) throw new Error(`${name}: independent editorial report differs from assigned review`);
  const reviewNames = [editorial.file, "claims-review.json", "claims-review.md", "verify-shared-instructions.md"];
  const evidence = Object.fromEntries(reviewNames.map((file) => [file, readFileSync(path.join(production, "reviews", file), "utf8")]));
  const shared = sharedReviewRecord(evidence["verify-shared-instructions.md"]);
  const editorialDecision = editorialReviewRecord(evidence[editorial.file], day, shared);
  const expectedContentHash = editorialDecision.content_hashes[String(day)];
  if (contentHash(lesson) !== expectedContentHash) throw new Error(`${name}: teaching content changed after independent editorial review`);
  const facts = JSON.parse(evidence["claims-review.json"]);
  if (facts.schema_version !== 1 || facts.series !== "airport-english-60-days" || facts.review_type !== "independent_public_source_factual_review" || facts.reviewer !== "airport_claims_review (separate agent from lesson authors)") throw new Error(`${name}: factual review identity or schema differs from the independent source ledger`);
  if (facts.status !== "factual_review_complete_for_recorded_text_snapshots" || facts.remaining_factual_corrections !== 0) throw new Error(`${name}: factual review has unresolved claims`);
  const factSnapshots = facts.production_source_hashes.filter((entry) => entry.day === day);
  if (factSnapshots.length !== 1 || englishContentHash(lesson) !== factSnapshots[0].reviewed_english_content_sha256) throw new Error(`${name}: English content changed after independent source review`);
  const sourceMap = new Map(facts.sources.map((source) => [source.id, source]));
  if (sourceMap.size !== facts.sources.length) throw new Error("Duplicate source IDs in facts review");
  const claims = facts.claims.filter((claim) => claim.days.includes(day));
  if (!claims.length || new Set(claims.map((claim) => claim.id)).size !== claims.length || claims.some((claim) => !ACCEPTED.has(claim.verdict))) throw new Error(`${name}: missing, ambiguous or unresolved reviewed claims`);
  const expectedClaims = claims.map((claim) => ({ id: claim.id, text: claim.claim, status: claim.verdict, source_urls: claim.sources.map((id) => {
    const source = sourceMap.get(id);
    if (!source || source.http_status !== 200 || !/^[a-f0-9]{64}$/.test(source.response_sha256)) throw new Error(`${name}: ${id} lacks retrieved official-source evidence`);
    return source.url;
  }) }));
  const expectedUrls = new Set(expectedClaims.flatMap((claim) => claim.source_urls));
  const expectedSources = facts.sources.filter((source) => expectedUrls.has(source.url)).map((source) => ({ title: source.title, url: source.url, checked_on: source.checked_date }));
  if (canonical(sortedClaims(lesson.claims ?? [])) !== canonical(sortedClaims(expectedClaims))) throw new Error(`${name}: claim text, verdict or source URLs differ from independent source review`);
  if (canonical(sortedSources(lesson.sources ?? [])) !== canonical(sortedSources(expectedSources))) throw new Error(`${name}: source metadata differs from independent source review`);
  const result = prepareLesson(lesson, profile);
  if (sharedInstructionsHash(result) !== shared.shared_instructions_sha256) throw new Error(`${name}: shared teaching instructions changed after review`);
  if (shared.thumbnail_headlines?.[String(day)] !== lesson.thumbnail_headline) throw new Error(`${name}: thumbnail wording changed after shared metadata review`);
  const artifacts = preparedArtifacts(lesson, result), generatedHashes = {};
  for (const [file, expected] of Object.entries(artifacts)) {
    const actual = readFileSync(path.join(dir, file));
    if (!actual.equals(Buffer.from(expected))) throw new Error(`${name}: stale generated artifact ${file}; run fresh prepare`);
    generatedHashes[file] = sha256(actual);
  }
  const lint = lintProject(loadProject({ file: path.join(dir, "video.json"), root: ROOT }));
  if (lint.errors.length) throw new Error(`${name}: official lint has ${lint.errors.length} errors`);
  const boundClaims = claims.map((claim) => ({ id: claim.id, verdict: claim.verdict === "fictional_scenario_not_external_fact" ? "OUT OF SCOPE" : claim.verdict === "correction_verified" ? "CHANGED" : "CONFIRMED", source_claim_sha256: sha256(canonical({ claim, sources: claim.sources.map((id) => sourceMap.get(id)) })), source_turns: claim.turns, scene_ids: result.doc.scenes.filter((scene) => scene.claims?.includes(claim.id)).map((scene) => scene.id) }));
  const binding = { schema_version: 1, day, slug: result.doc.slug, status: "independent_text_reviews_bound_to_current_sources", production_approval: false, release_ready: false, checked_on: facts.checked_date, lesson_sha256: sha256(lessonBytes), editorial_content_sha256: expectedContentHash, facts_english_content_sha256: factSnapshots[0].reviewed_english_content_sha256, shared_instructions_sha256: shared.shared_instructions_sha256, claims_and_sources_sha256: sha256(canonical({ claims: sortedClaims(expectedClaims), sources: sortedSources(expectedSources) })), profile_sha256: sha256(readFileSync(path.join(production, "profile.json"))), lexicon_sha256: sha256(readFileSync(path.join(production, "lexicon.json"))), reviews: reviewNames.map((file) => ({ path: `../reviews/${file}`, sha256: sha256(evidence[file]), reviewer: file === editorial.file ? editorial.reviewer : "airport_claims_review" })), generated_artifacts: generatedHashes, claims: boundClaims, lint: { errors: lint.errors, warnings: lint.warnings }, approval_records_created: false };
  const rows = claims.map((claim, index) => {
    const bound = boundClaims[index], beforeAfter = claim.original_wording ? `${claim.original_wording} -> ${claim.suggested_wording}` : "unchanged";
    const where = claim.id === "AE-C01" ? "youtube.description; fictional dialogue and quiz" : `scene.claims:${claim.id}; exact scene IDs in review-binding.json claims[${index}]`;
    return `| ${claim.id} | ${cleanCell(claim.claim)} | ${where} | ${claim.sources.map((id) => sourceMap.get(id).url).join(" ") || "fictional examples; no external policy claim"} | ${claim.sources.length ? "200 (recorded official retrieval)" : "not applicable"} | ${bound.verdict} | ${cleanCell(beforeAfter)} |`;
  });
  const counts = (verdict) => boundClaims.filter((claim) => claim.verdict === verdict).length;
  const markdown = [`# verify-1: ${result.doc.slug}`, "", "This file binds existing independent reviews to the matching generated script. It does not claim a new human review, a new web retrieval, audio review, production approval or publication approval.", "", `Editorial reviewer: ${editorial.reviewer}. Official-source and shared-instruction reviewer: airport_claims_review. Reviewed source date: ${facts.checked_date}.`, "", ...binding.reviews.map((review) => `- [${path.basename(review.path)}](${review.path}), SHA-256: \`${review.sha256}\`.`), "", `Canonical teaching content: \`${expectedContentHash}\`. English factual-content snapshot: \`${binding.facts_english_content_sha256}\`. Current video.json: \`${generatedHashes["video.json"]}\`. Complete artifact and claim bindings are in [review-binding.json](review-binding.json).`, "", "| # | claim | where | URL | HTTP status | verdict | before -> after |", "| --- | --- | --- | --- | --- | --- | --- |", ...rows, "", `Claims: ${boundClaims.length}; CONFIRMED: ${counts("CONFIRMED")}; CHANGED and independently rechecked: ${counts("CHANGED")}; NOT FOUND: 0; fictional OUT OF SCOPE: ${counts("OUT OF SCOPE")}.`, "", "No opinion/brief mismatch was identified in the cited reviews. Fictional flight numbers, gates, timings and arrangements are examples, not actual airport policies. Source restrictions may change; checked dates and jurisdiction/airline limits remain in the source ledger. No universal entry permission, baggage allowance or compensation is certified.", "", `Second fact-check round required by more-than-three-factual-changes rule: ${counts("CHANGED") > 3 ? "yes" : "no"}. This entry inherits completed source-review corrections; it makes no new factual edits.`, "", `Official lint on the current generated sources: ${lint.errors.length} errors, ${lint.warnings.length} warnings. Warning details are in review-binding.json; warnings are not silently relabelled as cleared.`, "", "Listener findings and the actual scope of translation/quiz review remain in the cited independent reports. Common instructions allow learners to pause for long lines; final natural pace, number/letter pronunciation, multilingual slots, subtitles, measured 600-second duration, visual quality and final/package QA remain unverified. No approval record was created.", ""].join("\n");
  return { day, dir, binding, markdown };
}

export function assertReviewBindingCurrent({ production = PRODUCTION, day }) {
  const plan = planReviewBinding({ production, day });
  for (const [file, expected] of [["review-binding.json", jsonBytes(plan.binding)], ["verify-1.md", plan.markdown]]) {
    if (!existsSync(path.join(plan.dir, file)) || readFileSync(path.join(plan.dir, file), "utf8") !== expected) throw new Error(`day${String(day).padStart(2, "0")}: ${file} is missing or stale; regenerate review bindings`);
  }
  return plan.binding;
}

export function bindReviews({ production = PRODUCTION, days = null, check = false } = {}) {
  const selected = days ?? readdirSync(path.join(production, "lessons")).filter((name) => /^day\d{2}\.json$/.test(name)).sort().map((name) => Number(name.slice(3, 5)));
  if (!selected.length || new Set(selected).size !== selected.length) throw new Error("Select one or more unique episode days");
  // Check the whole selected batch before writing anything. No partial successful batch.
  const plans = selected.map((day) => check ? { day, binding: assertReviewBindingCurrent({ production, day }) } : planReviewBinding({ production, day }));
  if (!check) for (const plan of plans) {
    writeFileSync(path.join(plan.dir, "review-binding.json"), jsonBytes(plan.binding));
    writeFileSync(path.join(plan.dir, "verify-1.md"), plan.markdown);
  }
  return { episodes: plans.length, mode: check ? "checked_current_bindings" : "bound_existing_independent_reviews", approvals_created: false, media_created: false, release_ready: false };
}

export function main(argv) {
  const { values } = parseArgs({ args: argv, options: { production: { type: "string" }, days: { type: "string" }, check: { type: "boolean" } }, strict: true });
  const result = bindReviews({ production: path.resolve(values.production ?? PRODUCTION), days: values.days ? values.days.split(",").map(Number) : null, check: values.check ?? false });
  console.log(JSON.stringify(result));
  return 0;
}
if (process.argv[1] && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href) {
  try { process.exitCode = main(process.argv.slice(2)); }
  catch (error) { console.error(error.message); process.exitCode = 1; }
}
