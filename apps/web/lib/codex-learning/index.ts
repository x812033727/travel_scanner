import catalog from "./catalog.json";
import type { Locale } from "@/i18n/routing";
import type { GuideSummary } from "@/lib/guides";

export const HUB_SLUG = "codex-learning-hub";
export const lessons = catalog;
export type Lesson = typeof catalog[number];
export type LearningEntry = Lesson & { published: boolean; title: string; description: string; updated: string | null };

export function learningEntries(locale: Locale, published: readonly Pick<GuideSummary, "kind" | "slug" | "title" | "description">[]): LearningEntry[] {
  const bySlug = new Map(published.filter((row) => row.kind === "life").map((row) => [row.slug, row]));
  return [...lessons].sort((a, b) => a.order - b.order).map((lesson) => {
    const article = bySlug.get(lesson.slug);
    return { ...lesson, ...lesson.locales[locale], published: Boolean(article),
      title: article?.title ?? lesson.locales[locale].title,
      description: article?.description ?? lesson.locales[locale].description,
      updated: article ? lesson.checkedOn : null };
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
