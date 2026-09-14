import { cache } from "react";
import { getGuideSeries } from "@/lib/guides.server";
import type { Locale } from "@/i18n/routing";

/** Share the API publication boundary with inline references and article navigation. */
export const getLearningPublication = cache(async (locale: Locale) => {
  const series = await getGuideSeries("codex", locale);
  return { articles: series?.entries ?? [], available: Boolean(series) };
});
