import type { GuideKind } from "./guides";

export type ArticleReference = { kind: GuideKind; slug: string; title: string };
export type SeriesEntry = ArticleReference & {
  number: number; group: string; level: string; platforms: string[]; aliases: string[];
  description: string; minutes: number; operation_minutes?: number | null;
};
export type GuideSeries = {
  slug: string; locale: string; hub: ArticleReference;
  groups: { id: string; title: string }[];
  paths: { id: string; title: string; slugs: string[] }[];
  entries: SeriesEntry[];
};
/** One series or tutorial hub a section page can enter, from `GET /guides/series`. */
export type SeriesSummary = {
  slug: string; section: "travel" | "life"; hub: ArticleReference;
  source: "api-series" | "web-gemini" | "catalogue"; topic: string | null; entries: number | null;
};
export type SeriesNavigation = {
  slug: string; hub: ArticleReference; current: SeriesEntry | null;
  previous: ArticleReference | null; next: ArticleReference | null;
  prerequisites: ArticleReference[]; related: ArticleReference[];
};
const slugPattern = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
const object = (v: unknown): v is Record<string, unknown> => Boolean(v) && typeof v === "object";
const strings = (v: unknown): v is string[] => Array.isArray(v) && v.every(x => typeof x === "string");
export function isArticleReference(v: unknown): v is ArticleReference {
  return object(v) && ["life", "intel", "howto"].includes(String(v.kind))
    && typeof v.slug === "string" && slugPattern.test(v.slug) && typeof v.title === "string";
}
export function isSeriesEntry(v: unknown): v is SeriesEntry {
  return object(v) && Number.isInteger(v.number) && Number(v.number) > 0
    && typeof v.group === "string" && typeof v.level === "string" && strings(v.platforms)
    && strings(v.aliases) && typeof v.description === "string" && Number.isInteger(v.minutes) && Number(v.minutes) > 0
    && (v.operation_minutes == null || (Number.isInteger(v.operation_minutes) && Number(v.operation_minutes) > 0)) && isArticleReference(v);
}
export function isSeriesSummary(v: unknown): v is SeriesSummary {
  return object(v) && typeof v.slug === "string" && slugPattern.test(v.slug)
    && (v.section === "travel" || v.section === "life") && isArticleReference(v.hub)
    && ["api-series", "web-gemini", "catalogue"].includes(String(v.source))
    && (v.topic === null || typeof v.topic === "string")
    && (v.entries === null || (Number.isInteger(v.entries) && Number(v.entries) >= 0));
}
export function isGuideSeries(v: unknown): v is GuideSeries {
  return object(v) && typeof v.slug === "string" && slugPattern.test(v.slug) && typeof v.locale === "string"
    && isArticleReference(v.hub) && Array.isArray(v.entries) && v.entries.every(isSeriesEntry)
    && Array.isArray(v.groups) && v.groups.every(g => object(g) && typeof g.id === "string" && typeof g.title === "string")
    && Array.isArray(v.paths) && v.paths.every(p => object(p) && typeof p.id === "string" && typeof p.title === "string" && strings(p.slugs));
}
export function isSeriesNavigation(v: unknown): v is SeriesNavigation {
  return object(v) && typeof v.slug === "string" && slugPattern.test(v.slug) && isArticleReference(v.hub)
    && (v.current === null || isSeriesEntry(v.current))
    && (v.previous === null || isArticleReference(v.previous)) && (v.next === null || isArticleReference(v.next))
    && Array.isArray(v.prerequisites) && v.prerequisites.every(isArticleReference)
    && Array.isArray(v.related) && v.related.every(isArticleReference);
}
export type SeriesFilters = { q: string; group: string; level: string; platform: string; path: string };
export function readSeriesFilters(params: URLSearchParams): SeriesFilters {
  return { q: (params.get("q") ?? "").slice(0, 200), group: params.get("group") ?? "",
    level: params.get("level") ?? "", platform: params.get("platform") ?? "", path: params.get("path") ?? "" };
}
export function filterSeries(series: GuideSeries, filters: SeriesFilters): SeriesEntry[] {
  const terms = filters.q.normalize("NFKC").toLocaleLowerCase().trim().split(/\s+/).filter(Boolean);
  const path = series.paths.find(p => p.id === filters.path);
  const entries = path ? path.slugs.flatMap(slug => series.entries.filter(e => e.slug === slug)) : series.entries;
  return entries.filter(entry => {
    const haystack = [entry.title, entry.description, ...entry.aliases].join(" ").normalize("NFKC").toLocaleLowerCase();
    return (!filters.group || entry.group === filters.group) && (!filters.level || entry.level === filters.level)
      && (!filters.platform || entry.platforms.includes(filters.platform)) && terms.every(term => haystack.includes(term));
  });
}
