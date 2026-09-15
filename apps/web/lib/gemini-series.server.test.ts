import { afterEach, describe, expect, it, vi } from "vitest";
vi.mock("server-only", () => ({}));
vi.mock("./guide-series.json", async () => {
  const base = (await vi.importActual<{ default: typeof import("./guide-series.json") }>("./guide-series.json")).default;
  const plan = (await import("./gemini-series-docs.test-data")).loadGeminiCurriculum();
  return { default: { ...base,
    articles: [...base.articles, ...plan.articles.map(article => ({ ...article, stage: 2, minutes: article.estimatedReadingMinutes, labMinutes: article.estimatedLabMinutes }))],
    paths: [...base.paths, ...plan.routes.map(route => ({ ...route, stage: 2, description: route.title }))],
  } };
});
import { getVisibleGeminiSeries } from "./gemini-series.server";

afterEach(() => vi.unstubAllEnvs());
describe("server-only Gemini visibility switch", () => {
  it.each([undefined, "", "false", "1", "TRUE", " true "])("stays at fifty for %s", value => {
    vi.stubEnv("GEMINI_ADVANCED_SERIES_ENABLED", value);
    vi.stubEnv("NEXT_PUBLIC_GEMINI_ADVANCED_SERIES_ENABLED", "true");
    expect(getVisibleGeminiSeries({ locale: "zh-TW", hubPublished: true })?.articles).toHaveLength(50);
  });
  it("reads the server flag at call time and does not cache a previous enabled value", () => {
    vi.stubEnv("GEMINI_ADVANCED_SERIES_ENABLED", "true");
    expect(getVisibleGeminiSeries({ locale: "zh-TW", hubPublished: true })?.articles).toHaveLength(86);
    vi.stubEnv("GEMINI_ADVANCED_SERIES_ENABLED", "false");
    expect(getVisibleGeminiSeries({ locale: "zh-TW", hubPublished: true })?.articles).toHaveLength(50);
  });
  it("returns no catalogue when the hub is unavailable or the locale is unpublished", () => {
    vi.stubEnv("GEMINI_ADVANCED_SERIES_ENABLED", "true");
    expect(getVisibleGeminiSeries({ locale: "zh-TW", hubPublished: false })).toBeNull();
    expect(getVisibleGeminiSeries({ locale: "en", hubPublished: true })).toBeNull();
  });
});
