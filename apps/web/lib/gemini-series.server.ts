import "server-only";
import catalogue from "./guide-series.json";
import { projectGeminiSeries } from "./gemini-series-projection";
import type { VisibleGeminiSeries } from "./gemini-series-projection";
import { projectGeminiArticleContent } from "./gemini-series-content";
import type { GuideArticleState, GuideKind } from "./guides";

export function getGeminiHubReference(locale: string) {
  return locale === catalogue.locale ? { slug: catalogue.hubSlug, title: catalogue.title } : null;
}

export function isGeminiSeriesPage(slug: string, locale: string, kind: string) {
  return locale === catalogue.locale && kind === "life"
    && (slug === catalogue.hubSlug || catalogue.articles.some(article => article.slug === slug));
}

export const projectGeminiArticle = (state: GuideArticleState, visible: VisibleGeminiSeries | null) => projectGeminiArticleContent(state, catalogue, visible);

export function filterGeminiArticleLinks<T extends { slug: string; kind: GuideKind }>(articles: readonly T[], visible: VisibleGeminiSeries | null) {
  const known = new Set([catalogue.hubSlug, ...catalogue.articles.map(article => article.slug)]);
  const allowed = new Set(visible ? [visible.hubSlug, ...visible.articles.map(article => article.slug)] : []);
  return articles.filter(article => article.kind !== "life" || !known.has(article.slug) || allowed.has(article.slug));
}

/** The article page already knows the hub publication state; reuse it without another fetch. */
export function getVisibleGeminiSeries({ locale, hubPublished }: { locale: string; hubPublished: boolean }) {
  if (!hubPublished || locale !== catalogue.locale) return null;
  // Deployment config only. No NEXT_PUBLIC alias, URL flag, cookie or request header.
  return projectGeminiSeries(catalogue, process.env.GEMINI_ADVANCED_SERIES_ENABLED === "true");
}
