// A compilation's public copy is read before a viewer has seen any episode. Review receipts
// bind the exact public words to the saved mysteries, without interpreting chapter/episode units.
import { createHash } from "node:crypto";

import { compilationChapterTitles, composeMetadata } from "../package/metadata.mjs";
import { descriptionWithinBudget, estimatedCompilationTimeline } from "./compilation.mjs";
import { articleUrl } from "./metadata.mjs";
import { narrationLocale } from "./schema.mjs";
import { chapterList, formatClock } from "./timeline.mjs";

export const COMPILATION_REVIEW_FILE = "compilation-review.json";

const object = (value) => value !== null && typeof value === "object" && !Array.isArray(value);

/** An explicit empty array means no mysteries; an old context with no array is unknown. */
export function contextFromSeries(context) {
  if (!Array.isArray(context?.mysteries)) return null;
  const source = (doc) => doc ? {
    id: doc.id ?? null,
    version: doc.version ?? null,
    body_json: structuredClone(doc.body_json ?? null),
  } : null;
  return {
    mysteries: structuredClone(context.mysteries),
    reveal_schedule: structuredClone(context.outline?.body_json?.reveal_schedule ?? []),
    setting_md: context.setting?.body_md ?? "",
    outline_md: context.outline?.body_md ?? "",
    setting: source(context.setting),
    outline: source(context.outline),
  };
}

/** Every locale's composed public copy, plus the source thumbnail/cards and optional alternatives. */
export function publicTexts({ doc, translations = {}, timeline = null, plan = null, pack = null }) {
  const measured = timeline ?? estimatedCompilationTimeline(doc);
  const narration = narrationLocale(doc);
  const { metadata } = composeMetadata({ doc, timeline: measured, translations, pack });
  const locales = { [narration]: { title: metadata.title, description: metadata.description }, ...metadata.localizations };
  return Object.fromEntries(Object.entries(locales).map(([locale, fields]) => {
    const translation = locale === narration ? null : translations[locale];
    const tags = translation?.tags?.length ? translation.tags : doc.youtube.tags;
    const titles = { ...compilationChapterTitles(doc), ...(translation?.chapters ?? {}) };
    const budget = descriptionWithinBudget(translation?.description ?? doc.youtube.description, measured, titles, {
      locale, sources: doc.sources ?? [], tags,
      article: pack ? articleUrl(pack, pack.locales?.[locale] ? locale : narration, doc.slug) : null,
    });
    return [locale, {
      ...fields,
      tags,
      chapters: chapterList(measured, budget.titles).map((chapter) => ({ at: formatClock(chapter.start), title: chapter.title })),
      ...(locale === narration ? {
        thumbnail: { headline: doc.thumbnail?.data?.headline ?? null, tag: doc.thumbnail?.data?.tag ?? null },
        cards: doc.scenes.filter((scene) => ["chapter", "outro"].includes(scene.template)).map((scene) => ({
          id: scene.id, chapter: scene.chapter ?? null, data: scene.data,
          lines: (scene.lines ?? []).map((line) => line.text),
        })),
        titles: plan?.titles ?? [],
        pinned_comment: plan?.pinned_comment ?? null,
      } : {}),
    }];
  }));
}

function canonical(value) {
  if (Array.isArray(value)) return value.map(canonical);
  if (object(value)) return Object.fromEntries(Object.keys(value).sort().map((key) => [key, canonical(value[key])]));
  return value;
}

/** A full digest of both the review's private context and its exact public words. */
export function reviewHash(context, locale, fields) {
  return createHash("sha256").update(JSON.stringify(canonical({ schema_version: 1, context, locale, fields }))).digest("hex");
}

export function reviewCurrent(receipts, context, locale, fields) {
  const receipt = receipts?.locales?.[locale];
  return Array.isArray(context?.mysteries) && receipts?.schema_version === 1 && receipt?.passed === true
    && receipt.input_sha256 === reviewHash(context, locale, fields);
}

/** Null only for an explicit independent pass with no reported problem. */
export function reviewProblem(verdict) {
  if (!object(verdict) || Object.keys(verdict).some((key) => !["passed", "problems"].includes(key))
      || typeof verdict.passed !== "boolean" || !Array.isArray(verdict.problems)
      || !verdict.problems.every((problem) => typeof problem === "string" && problem.trim())) {
    return "the public-text review must contain only passed (boolean) and problems (a list of nonempty strings)";
  }
  if (verdict.problems.length) return verdict.problems.join("; ");
  return verdict.passed ? null : "the reviewer did not approve the public text";
}
