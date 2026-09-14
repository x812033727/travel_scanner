import catalog from "./catalog.json";
import type { Locale } from "@/i18n/routing";
import type { GuideSummary, GuideBlock } from "@/lib/guides";

export const HUB_SLUG = "codex-learning-hub";
export const lessons = catalog;
export type Lesson = typeof catalog[number];
export type LearningEntry = Lesson & { published: boolean; title: string; description: string; updated: string | null };

export function learningEntries(locale: Locale, published: readonly GuideSummary[]): LearningEntry[] {
  const bySlug = new Map(published.filter((row) => row.kind === "life").map((row) => [row.slug, row]));
  return [...lessons].sort((a, b) => a.order - b.order).map((lesson) => {
    const article = bySlug.get(lesson.slug);
    return { ...lesson, ...lesson.locales[locale], published: Boolean(article),
      title: article?.title ?? lesson.locales[locale].title,
      description: article?.description ?? lesson.locales[locale].description,
      updated: article ? lesson.checkedOn : null };
  });
}

/** Withdrawn translations remain readable as text, never as broken series links. */
export function publishedSeriesLinks(blocks: GuideBlock[], locale: Locale, published: readonly GuideSummary[]): GuideBlock[] {
  const known = new Set([HUB_SLUG, ...lessons.map((row) => row.slug)]);
  const live = new Set(published.filter((row) => row.kind === "life").map((row) => row.slug));
  function allowed(url: string) {
    const target = new URL(url);
    const match = target.pathname.match(/^\/([^/]+)\/life\/([^/]+)$/);
    return target.hostname !== "mokaair.com" || !match || !known.has(match[2])
      || (match[1] === locale && live.has(match[2]));
  }
  return blocks.map((block) => {
    if (block.type === "link" && !allowed(block.url)) return { type: "paragraph", text: block.text };
    if (block.type === "rich_paragraph") return { ...block, spans: block.spans.map((span) =>
      span.type === "link" && !allowed(span.url) ? { type: "text" as const, text: span.text } : span) };
    return block;
  });
}

export function filterLessons(entries: LearningEntry[], query: string, level: string, platform: string, goal: string, unit = "") {
  const terms = query.normalize("NFKC").toLocaleLowerCase().trim().split(/\s+/).filter(Boolean);
  return entries.filter((entry) => {
    const haystack = `${entry.title} ${entry.description} ${entry.aliases} ${entry.slug}`.normalize("NFKC").toLocaleLowerCase();
    return terms.every((term) => haystack.includes(term))
      && (!level || entry.level === Number(level))
      && (!platform || entry.platforms.includes(Number(platform)))
      && (!goal || entry.goals.includes(Number(goal)))
      && (!unit || entry.unit === unit);
  });
}
