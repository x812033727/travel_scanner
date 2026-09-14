import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { cleanup, render, screen } from "@testing-library/react";
import { renderToStaticMarkup } from "react-dom/server";
import catalogue from "@/lib/guide-series.json";
import type { GuideArticleState } from "@/lib/guides";
import { renderGuideArticle } from "./article-page";
import LifePage from "@/app/[locale]/life/page";
import { siteUrl } from "@/lib/seo";

const mocks = vi.hoisted(() => ({ article: vi.fn(), list: vi.fn() }));
vi.mock("@/lib/guide-series.json", async () => {
  const base = (await vi.importActual<{ default: typeof import("@/lib/guide-series.json") }>("@/lib/guide-series.json")).default;
  const plan = (await import("../../../../docs/gemini-series/advanced/curriculum.json")).default;
  return { default: { ...base, articles: [...base.articles, ...plan.articles.map(article => ({ ...article, stage: 2, minutes: article.estimatedReadingMinutes, labMinutes: article.estimatedLabMinutes }))],
    paths: [...base.paths, ...plan.routes.map(route => ({ ...route, stage: 2, description: route.title }))] } };
});
vi.mock("@/components/site-header", () => ({ SiteHeader: () => null }));
vi.mock("@/lib/adsense.server", () => ({ getAdsenseSlot: async () => ({ enabled: false }) }));
vi.mock("@/lib/guides.server", () => ({ getGuideArticle: mocks.article, getGuideList: mocks.list, getGuideTopics: async () => [], getGuideSeries: async () => null, hubIsEmpty: () => false }));
const deep = catalogue.articles[50];
function state(slug: string): GuideArticleState {
  const article = catalogue.articles.find(entry => entry.slug === slug);
  return { slug, kind: "life", locale: "zh-TW", status: "published", topics: [], destination_id: null, destination_label: null, valid_until: null, expired: false, published_locales: ["zh-TW"],
    document: { title: article?.title ?? catalogue.title, description: "教學摘要", version: 1, published_at: "2026-09-14T00:00:00Z", sources: [],
      blocks: [{ type: "rich_paragraph", inlines: [{ type: "link", text: "深入實作文章", url: `${siteUrl}/zh-TW/life/${deep.slug}` }] }] } };
}
beforeEach(() => {
  vi.clearAllMocks();
  mocks.article.mockImplementation(async (_kind, slug) => state(slug));
  mocks.list.mockResolvedValue({ articles: [], next_cursor: null });
});
afterEach(() => { cleanup(); vi.unstubAllEnvs(); });
describe("Gemini actual page integration", () => {
  it("preserves another series' own navigation", async () => {
    const article = state("claude-code-getting-started");
    article.document!.title = "Claude 入門";
    article.document!.blocks = [{ type: "paragraph", text: "Claude 原有正文" }];
    article.series = { slug: "claude-code", hub: { kind: "life", slug: "claude-code-tutorials", title: "Claude 教學" },
      current: { kind: "life", slug: article.slug, title: "Claude 入門", number: 1, group: "A", level: "入門", platforms: ["CLI"], aliases: [], description: "入門", minutes: 5 },
      previous: null, next: { kind: "life", slug: "claude-code-accounts-and-access", title: "Claude 帳號" }, prerequisites: [], related: [] };
    mocks.article.mockResolvedValue(article);
    const html = renderToStaticMarkup(await renderGuideArticle({ locale: "zh-TW", kind: "life", slug: article.slug }));
    expect(html).toContain("claude-code-tutorials");
    expect(html).toContain("claude-code-accounts-and-access");
    expect(html).toContain("Claude 原有正文");
    expect(html).not.toContain('data-testid="gemini-series-index"');
    expect(mocks.article).toHaveBeenCalledTimes(1);
  });
  it.each([false, true])("uses the same visible set in real article composition (advanced=%s)", async advanced => {
    vi.stubEnv("GEMINI_ADVANCED_SERIES_ENABLED", String(advanced));
    const html = renderToStaticMarkup(await renderGuideArticle({ locale: "zh-TW", kind: "life", slug: catalogue.hubSlug }));
    expect(html.includes(deep.slug)).toBe(advanced);
    render(await renderGuideArticle({ locale: "zh-TW", kind: "life", slug: catalogue.hubSlug }));
    expect(screen.getByTestId("series-lessons").querySelectorAll("li > a")).toHaveLength(advanced ? 86 : 50);
    // The hub's own already-fetched publication state is reused.
    expect(mocks.article.mock.calls.every(call => call[1] === catalogue.hubSlug)).toBe(true);
  });
  it("hides the next lesson and body target at 50, then enables both", async () => {
    vi.stubEnv("GEMINI_ADVANCED_SERIES_ENABLED", "false");
    const route = { locale: "zh-TW" as const, kind: "life" as const, slug: catalogue.articles[49].slug };
    const hidden = renderToStaticMarkup(await renderGuideArticle(route));
    expect(hidden).not.toContain(deep.slug);
    expect(hidden).not.toContain('rel="next"');
    vi.stubEnv("GEMINI_ADVANCED_SERIES_ENABLED", "true");
    const open = renderToStaticMarkup(await renderGuideArticle(route));
    expect(open).toContain(deep.slug);
    expect(open).toContain('rel="next"');
  });
  it("removes the dedicated directory when its hub is not published", async () => {
    mocks.article.mockImplementation(async (_kind, slug) => slug === catalogue.hubSlug ? { ...state(slug), status: "unavailable", document: null } : state(slug));
    const html = renderToStaticMarkup(await renderGuideArticle({ locale: "zh-TW", kind: "life", slug: catalogue.articles[0].slug }));
    expect(html).not.toContain(catalogue.hubSlug);
    expect(html).not.toContain(deep.slug);
  });
  it.each([false, true])("filters both life cards and structured data (advanced=%s)", async advanced => {
    vi.stubEnv("GEMINI_ADVANCED_SERIES_ENABLED", String(advanced));
    mocks.list.mockResolvedValue({ articles: [catalogue.articles[0], deep].map(article => ({ ...article, kind: "life", description: article.purpose, destination_id: null, destination_label: null, topics: [], published_at: "2026-09-14", valid_until: null, featured: false })), next_cursor: null });
    const html = renderToStaticMarkup(await LifePage({ params: Promise.resolve({ locale: "zh-TW" }), searchParams: Promise.resolve({}) }));
    expect(html.includes(deep.slug)).toBe(advanced);
    expect(html).toContain(`${advanced ? 86 : 50} 篇完整教學`);
    expect(html).toContain("claude-code-tutorials");
  });
});
