import { cache } from "react";
import { getGuideList } from "@/lib/guides.server";
import type { GuideSummary } from "@/lib/guides";
import type { Locale } from "@/i18n/routing";
import { HUB_SLUG, lessons } from "./index";

/** Read publication state, including pagination. Never infer publication from bundled content. */
export const getLearningPublication = cache(async (locale: Locale) => {
  const wanted = new Set([HUB_SLUG, ...lessons.map((lesson) => lesson.slug)]);
  const articles: GuideSummary[] = [];
  const seen = new Set<string>();
  let cursor: string | undefined;
  do {
    const page = await getGuideList(locale, { kind: "life", cursor }, 50);
    if (!page.available) return { articles: [], available: false };
    articles.push(...page.articles.filter((row) => wanted.has(row.slug)));
    if (!page.next_cursor) break;
    if (seen.has(page.next_cursor)) return { articles: [], available: false };
    seen.add(page.next_cursor);
    cursor = page.next_cursor;
  } while (articles.length < wanted.size);
  return { articles, available: true };
});
