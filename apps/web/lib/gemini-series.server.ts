import "server-only";
import catalogue from "./guide-series.json";
import { projectGeminiSeries } from "./gemini-series-projection";

/** The article page already knows the hub publication state; reuse it without another fetch. */
export function getVisibleGeminiSeries({ locale, hubPublished }: { locale: string; hubPublished: boolean }) {
  if (!hubPublished || locale !== catalogue.locale) return null;
  // Deployment config only. No NEXT_PUBLIC alias, URL flag, cookie or request header.
  return projectGeminiSeries(catalogue, process.env.GEMINI_ADVANCED_SERIES_ENABLED === "true");
}
