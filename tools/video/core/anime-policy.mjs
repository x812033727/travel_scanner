// Explicit long-anime production rules. A category or a drawing style alone grants no exception.
import { createHash } from "node:crypto";

export const LONG_ANIME_POLICY = "long-anime-v1";
export const ANIME_BODY_TOLERANCE_SECONDS = 60;
export const ANIME_RUNTIME_KEYS = ["body_target_seconds", "op_ed_budget_seconds", "broadcast_slot_seconds", "slot_reserve_seconds"];
export const ANIME_CONTEXT_KEYS = ["slug", "episode", "chapter", "planned_episodes", "open_ended", "closed_ending", "kind", "genre", "lead"];
const object = (value) => value !== null && typeof value === "object" && !Array.isArray(value);
const integer = (value, low, high) => Number.isSafeInteger(value) && value >= low && value <= high;

/** Both fields participate in dispatch: malformed or half-present policies never become legacy drama. */
export const hasAnimePolicy = (value) => Boolean(value && (value.production_policy != null || value.runtime_spec != null));
export const isLongAnime = (value) => value?.production_policy === LONG_ANIME_POLICY;

export function validateAnimeRuntime(spec) {
  if (!object(spec)) return ["runtime_spec must be an object"];
  const problems = [];
  for (const key of Object.keys(spec)) if (!ANIME_RUNTIME_KEYS.includes(key)) problems.push(`runtime_spec.${key} is unknown`);
  if (!integer(spec.body_target_seconds, 9 * 60, 30 * 60) || spec.body_target_seconds % 60 !== 0) problems.push("runtime_spec.body_target_seconds must be whole minutes from 9 to 30, expressed in seconds");
  if (!integer(spec.op_ed_budget_seconds, 0, 300)) problems.push("runtime_spec.op_ed_budget_seconds must be an integer from 0 to 300");
  if (!integer(spec.slot_reserve_seconds, 0, 900)) problems.push("runtime_spec.slot_reserve_seconds must be an integer from 0 to 900");
  if (!integer(spec.broadcast_slot_seconds, 1, 3600)) problems.push("runtime_spec.broadcast_slot_seconds must be a positive integer no greater than 3600");
  if (problems.length === 0 && spec.body_target_seconds + spec.op_ed_budget_seconds + spec.slot_reserve_seconds !== spec.broadcast_slot_seconds) problems.push("runtime_spec body, OP/ED budget and slot reserve must sum exactly to the broadcast slot");
  return problems;
}

/** A series request, or video.json with its trusted series projection, shares one contract. */
export function validateAnimePolicy(value, { series = null } = {}) {
  if (!hasAnimePolicy(value)) return [];
  if (!object(value)) return ["long-anime policy needs an object"];
  const problems = [];
  if (value.production_policy !== LONG_ANIME_POLICY) problems.push(`production_policy must be ${LONG_ANIME_POLICY}`);
  problems.push(...validateAnimeRuntime(value.runtime_spec));
  const video = Object.hasOwn(value, "format");
  const context = video ? series ?? value.series : value;
  if (video && value.format !== "drama") problems.push("long-anime video format must be drama");
  if (value.category !== "anime") problems.push("long-anime category must be anime");
  if ((video ? value.look?.preset : value.style_preset) !== "anime-2d") problems.push("long-anime style preset must be anime-2d");
  for (const [key, expected] of [["kind", "series"], ["genre", "custom"], ["lead", "ensemble"]]) {
    if (context?.[key] !== expected) problems.push(`long-anime ${key} must be ${expected}`);
  }
  if (value.compilation || context?.compilation) problems.push("long-anime episodes cannot be compilations");
  if (object(value.runtime_spec) && Number.isSafeInteger(value.runtime_spec.body_target_seconds)) {
    const minutes = value.runtime_spec.body_target_seconds / 60;
    const target = value.target_minutes;
    const matches = video ? Array.isArray(target) && target.length === 2 && target.every((entry) => entry === minutes) : target === minutes;
    if (!matches) problems.push(`target_minutes must match the ${minutes}-minute story body${video ? " as [target, target]" : ""}`);
  }
  return problems;
}

export function requireAnimePolicy(value, options = {}) {
  const problems = validateAnimePolicy(value, options);
  if (!isLongAnime(value) || problems.length) throw new RangeError(problems.join("; ") || `production_policy must be ${LONG_ANIME_POLICY}`);
  return value.runtime_spec;
}

/** A reviewed episode keeps its series identity and finale declaration with every runtime receipt. */
export function animeRuntimeContext(value, { series = null } = {}) {
  const context = Object.hasOwn(value, "format") ? series ?? value.series : value;
  return Object.fromEntries(ANIME_CONTEXT_KEYS.map((key) => [key, context?.[key] ?? null]));
}

/** Duration approval changes do not invalidate reusable voice clips whose spoken text is unchanged. */
export function runtimePolicyHash(value, options = {}) {
  if (!hasAnimePolicy(value)) return null;
  const runtime = requireAnimePolicy(value, options);
  const context = animeRuntimeContext(value, options);
  return createHash("sha256").update(JSON.stringify([
    LONG_ANIME_POLICY,
    ANIME_RUNTIME_KEYS.map((key) => [key, runtime[key]]),
    value.category, Object.hasOwn(value, "format") ? value.look?.preset : value.style_preset,
    ANIME_CONTEXT_KEYS.map((key) => [key, context[key] ?? null]),
  ])).digest("hex");
}

/** A natural, directed shot interval. Schema/drama validation also checks the visible action. */
export const isAnimeAction = (doc, scene) => isLongAnime(doc) && scene?.action_seconds !== undefined;

/** Only the declared last episode of a closed series may resolve quietly. */
export function isClosedAnimeFinale(series, episodeNumber = series?.episode, beats = null) {
  return isLongAnime(series) && series.open_ended === false
    && Number.isSafeInteger(series.planned_episodes) && series.planned_episodes > 0
    && episodeNumber === series.planned_episodes
    && (beats?.closed_ending ?? series.closed_ending) === true;
}
