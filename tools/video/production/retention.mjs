// A Chinese-first production must keep its paid picture sources and dry sound for the
// later cast mixes. This is a retention promise, never a claim that those mixes exist.
import { createHash } from "node:crypto";
import { existsSync, readFileSync } from "node:fs";
import path from "node:path";

import { atomicWrite, docDir } from "../core/paths.mjs";

export const LOCALIZATION_RETENTION_FILE = "localization-retention.json";
const POLICY = "retain-until-explicit-owner-release";
const HASH = /^[a-f0-9]{64}$/;
const SLUG = /^[a-z0-9](?:[a-z0-9-]{0,58}[a-z0-9])?$/;
// The languages a cast mix may be planned in: core/schema.mjs LOCALES but zh-TW (schema.mjs
// imports this module, so the list is spelled out here).
const LOCALES = ["en", "ja", "ko"];
const object = (value) => value !== null && typeof value === "object" && !Array.isArray(value);
const sha256 = (value) => createHash("sha256").update(JSON.stringify(value)).digest("hex");
const PLAN_KEYS = new Set(["schema_version", "primary_locale", "planned_locales", "start_after", "status", "retain_source_media", "source_sha256", "profile_sha256"]);

/** The durable video.json marker; settlement obtains it only from the approved profile. */
export function localizationPlan(production) {
  const profile = production?.profile;
  const phase = profile?.phases?.localization;
  if (profile?.phases?.primary?.locale !== "zh-TW" || !Array.isArray(phase?.locales) || !phase.locales.length) return null;
  const plan = {
    schema_version: 1,
    primary_locale: "zh-TW",
    planned_locales: [...phase.locales],
    start_after: phase.start_after,
    status: phase.readiness,
    retain_source_media: true,
    source_sha256: production.source_binding?.source_sha256,
    profile_sha256: sha256(profile),
  };
  const problems = localizationPlanProblems(plan);
  if (problems.length) throw new Error(`invalid approved localization plan: ${problems.join("; ")}`);
  return plan;
}

/** Unknown/completed/released states cannot accidentally turn retention off. */
export function localizationPlanProblems(plan) {
  if (!object(plan)) return ["must be an object"];
  const errors = [];
  for (const key of Object.keys(plan)) if (!PLAN_KEYS.has(key)) errors.push(`unknown field ${key}`);
  if (plan.schema_version !== 1) errors.push("schema_version must be 1");
  if (plan.primary_locale !== "zh-TW") errors.push("primary_locale must be zh-TW");
  if (!Array.isArray(plan.planned_locales) || !plan.planned_locales.length || plan.planned_locales.some((locale) => !LOCALES.includes(locale)) || new Set(plan.planned_locales).size !== plan.planned_locales.length) errors.push("planned_locales must contain distinct later delivery locales");
  if (plan.start_after !== "approved-chinese-final") errors.push("start_after must be approved-chinese-final");
  if (plan.status !== "planned-not-implemented-for-drama") errors.push("status must remain planned-not-implemented-for-drama");
  if (plan.retain_source_media !== true) errors.push("retain_source_media must be true; release is not implemented");
  for (const key of ["source_sha256", "profile_sha256"]) if (!HASH.test(plan[key] ?? "")) errors.push(`${key} must be a SHA-256`);
  return errors;
}

/** A second durable copy survives replacing a script or losing its repository context. */
export function writeLocalizationRetention(workdir, { slug, seriesSlug, production }) {
  const plan = localizationPlan(production);
  const file = path.join(workdir, LOCALIZATION_RETENTION_FILE);
  if (!plan) return null; // Absence of a new plan never removes an existing promise.
  if (!SLUG.test(slug) || !SLUG.test(seriesSlug)) throw new Error("localization retention needs valid video and series slugs");
  let record = { schema_version: 1, slug, series_slug: seriesSlug, policy: POLICY, plans: [] };
  if (existsSync(file)) {
    record = JSON.parse(readFileSync(file, "utf8"));
    if (record.schema_version !== 1 || record.slug !== slug || record.series_slug !== seriesSlug || record.policy !== POLICY || !Array.isArray(record.plans) || record.plans.some((entry) => localizationPlanProblems(entry).length)) throw new Error("existing localization retention record is invalid; keep media and repair the record");
  }
  if (!record.plans.some((entry) => sha256(entry) === sha256(plan))) {
    record.plans.push(plan);
    atomicWrite(file, `${JSON.stringify(record, null, 2)}\n`);
  }
  return record;
}

const keep = (locales = []) => `planned ${locales.length ? `${locales.join(", ")} ` : ""}cast localization still needs the picture, dry voices and M&E sources; explicit archive/release is not implemented`;

/** Read-only: site language selections, elapsed time and a dropped state cannot release it. */
export function localizationRetentionHold(video, { videos, repos, fs }) {
  const cache = new Map();
  const inspect = (entry) => {
    if (cache.has(entry.slug)) return cache.get(entry.slug);
    const result = { held: null, doc: null };
    cache.set(entry.slug, result);
    const marker = path.join(entry.workdir, LOCALIZATION_RETENTION_FILE);
    // Even a damaged/empty marker is evidence of a promise, never permission to delete.
    if (fs.existsSync(marker)) result.held = keep();
    for (const repo of repos) {
      for (const name of ["video.json", "series.json"]) {
        const file = path.join(docDir(entry.slug, repo), name);
        if (!fs.existsSync(file)) continue;
        let value;
        try { value = JSON.parse(fs.readFileSync(file, "utf8").replace(/^\uFEFF/, "")); }
        catch {
          result.held ??= "its saved production context cannot be read; retain media until localization retention can be checked";
          continue;
        }
        if (name === "video.json") result.doc ??= value;
        if (object(value) && Object.hasOwn(value, "localization_plan")) {
          const plan = value.localization_plan;
          result.held = keep(Array.isArray(plan?.planned_locales) ? plan.planned_locales : []);
        }
        const phase = value?.production?.profile?.phases?.localization;
        if (phase && (Array.isArray(phase.locales) ? phase.locales.length : true)) result.held = keep(Array.isArray(phase.locales) ? phase.locales : []);
      }
    }
    return result;
  };
  const own = inspect(video);
  if (own.held) return own.held;
  const series = video.state.compilation?.series ?? own.doc?.compilation?.series;
  if (!series && !own.doc?.compilation) return null;
  const episodeSlugs = new Set((own.doc?.compilation?.episodes ?? []).filter((slug) => typeof slug === "string" && SLUG.test(slug)));
  for (const entry of videos) if (series && entry.state.series?.slug === series && !entry.state.compilation) episodeSlugs.add(entry.slug);
  for (const slug of episodeSlugs) {
    const entry = videos.find((candidate) => candidate.slug === slug) ?? { slug, workdir: path.join(path.dirname(video.workdir), slug), state: {} };
    const episode = inspect(entry);
    if (episode.held) return `compilation includes ${slug}, whose ${episode.held}`;
  }
  return null;
}
