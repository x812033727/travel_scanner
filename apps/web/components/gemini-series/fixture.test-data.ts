/** Test fixture only. Production components never import this file. */
import base from "@/lib/guide-series.json";
import curriculum from "../../../../docs/gemini-series/advanced/curriculum.json";
import { projectGeminiSeries, type GeminiCatalogue } from "@/lib/gemini-series-projection";

export function fixtureCatalogue(): GeminiCatalogue {
  return {
    ...structuredClone(base),
    articles: [...structuredClone(base.articles), ...curriculum.articles.map(article => ({
      ...article, stage: 2, minutes: article.estimatedReadingMinutes, labMinutes: article.estimatedLabMinutes,
    }))],
    paths: [...structuredClone(base.paths), ...curriculum.routes.map(route => ({ ...route, stage: 2, description: route.title }))],
    commands: [...base.commands, { command: "python batch.py", description: "批次恢復範例", kind: "終端機命令", article: 85, anchor: "section-3" }],
  };
}
export const fixtureSeries = (advanced = false) => projectGeminiSeries(fixtureCatalogue(), advanced);
