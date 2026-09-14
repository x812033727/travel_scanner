import messages from "@/messages/zh-TW/common.json";
import catalogue from "./guide-series.json";

export const geminiSeries = catalogue;
// This series currently publishes only zh-TW. UI copy still lives in the message catalog.
export const geminiCopy = messages.geminiSeries;
export type SeriesArticle = typeof catalogue.articles[number];
export const seriesArticle = (number: number) => catalogue.articles.find((article) => article.number === number);
export const seriesHref = (slug: string, anchor?: string) => `/${catalogue.locale}/life/${slug}${anchor ? `#${anchor}` : ""}`;

export function seriesMember(slug: string, locale: string, kind: string): SeriesArticle | undefined {
  if (locale !== catalogue.locale || kind !== "life") return undefined;
  return catalogue.articles.find((article) => article.slug === slug);
}

export function matchesSeriesArticle(article: SeriesArticle, query: string): boolean {
  const haystack = [article.title, article.purpose, article.level, ...article.platforms, ...article.keywords].join(" ").normalize("NFKC").toLocaleLowerCase();
  return query.normalize("NFKC").trim().toLocaleLowerCase().split(/\s+/).every((word) => haystack.includes(word));
}
