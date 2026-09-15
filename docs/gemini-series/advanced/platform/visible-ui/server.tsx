import { renderToString } from "react-dom/server";
import { fixtureSeries } from "@/components/gemini-series/fixture.test-data";
import { geminiSeriesCopy as copy } from "@/lib/gemini-series-copy";
import { Page, sample } from "./fixture";

export { fixtureSeries, sample };
export function renderPage(advanced: boolean, slug: string) {
  const series = fixtureSeries(advanced);
  const article = series.articles.find(entry => entry.slug === slug);
  if (slug !== series.hubSlug && !article) return null;
  const props = { series, copy, ...(article ? { number: article.number } : {}) };
  return '<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Gemini 可見目錄測試</title><link rel="stylesheet" href="/style.css"><body><div id="root">'
    + renderToString(<Page {...props} />) + '</div><script type="application/json" id="visible-props">'
    + JSON.stringify(props).replace(/</g, "\\u003c") + '</script><script src="/client.js"></script></body></html>';
}
