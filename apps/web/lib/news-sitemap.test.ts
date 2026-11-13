import { beforeEach, describe, expect, it, vi } from "vitest";
import type { GuideSummary } from "@/lib/guides";
import { loadRecentNewsSitemap, newsLanguageCode, renderNewsSitemapXml } from "./news-sitemap";
import { GET } from "@/app/sitemap-news.xml/route";

const mockGetGuideList = vi.fn();

vi.mock("@/lib/guides.server", () => ({
  getGuideList: (...args: unknown[]) => mockGetGuideList(...args),
}));

const NOW_MS = Date.parse("2026-11-13T08:00:00Z");

function makeArticle(overrides: Partial<GuideSummary>): GuideSummary {
  return {
    slug: "ai-news-gemini-20261113",
    kind: "life",
    destination_id: null,
    destination_label: null,
    topics: [{ slug: "ai-news", label: "AI 快訊" }],
    title: "Gemini 2.5 CLI 新增即時終端機代理模式",
    description: "摘要說明",
    published_at: "2026-11-13T04:00:00Z",
    news_date: "2026-11-13",
    valid_until: null,
    featured: false,
    ...overrides,
  };
}

describe("news-sitemap", () => {
  beforeEach(() => {
    mockGetGuideList.mockReset();
    mockGetGuideList.mockResolvedValue({ articles: [], next_cursor: null, available: true });
  });

  it("maps locales to Google News ISO 639 / Chinese codes", () => {
    expect(newsLanguageCode("zh-TW")).toBe("zh-tw");
    expect(newsLanguageCode("zh-CN")).toBe("zh-cn");
    expect(newsLanguageCode("en")).toBe("en");
    expect(newsLanguageCode("ja")).toBe("ja");
    expect(newsLanguageCode("ko")).toBe("ko");
  });

  it("includes only news and intel published within 48 hours, deduplicated per locale", async () => {
    const recentNews = makeArticle({
      slug: "shared-ai-tech-20261113",
      title: 'OpenAI & Google <Model> "Update"',
      published_at: "2026-11-13T06:00:00Z",
      topics: [
        { slug: "ai-news", label: "AI 快訊" },
        { slug: "tech-news", label: "科技新聞" },
      ],
    });
    const recentIntel = makeArticle({
      slug: "jr-pass-notice",
      kind: "intel",
      topics: [{ slug: "transport", label: "交通" }],
      news_date: null,
      title: "JR 東日本時刻表異動",
      published_at: "2026-11-12T12:00:00Z",
    });
    const staleNews = makeArticle({
      slug: "old-ai-news-20261109",
      published_at: "2026-11-10T00:00:00Z", // > 48h before NOW_MS
    });

    mockGetGuideList.mockImplementation(
      async (locale: string, filters: { topic?: string; kind?: string }) => {
        if (locale === "zh-TW" && (filters.topic === "ai-news" || filters.topic === "tech-news")) {
          return { articles: [recentNews, staleNews], next_cursor: null, available: true };
        }
        if (locale === "ja" && filters.kind === "intel") {
          return { articles: [recentIntel], next_cursor: null, available: true };
        }
        return { articles: [], next_cursor: null, available: true };
      },
    );

    const { available, entries } = await loadRecentNewsSitemap(NOW_MS);
    expect(available).toBe(true);
    expect(entries).toHaveLength(2);
    expect(entries[0].url).toContain("/zh-TW/life/shared-ai-tech-20261113");
    expect(entries[1].url).toContain("/ja/guides/intel/jr-pass-notice");

    const xml = renderNewsSitemapXml(entries);
    expect(xml).toContain('xmlns:news="http://www.google.com/schemas/sitemap-news/0.9"');
    expect(xml).toContain("<news:language>zh-tw</news:language>");
    expect(xml).toContain("<news:language>ja</news:language>");
    expect(xml).toContain(
      "<news:title>OpenAI &amp; Google &lt;Model&gt; &quot;Update&quot;</news:title>",
    );
    expect(xml).not.toContain("old-ai-news-20261109");
  });

  it("answers 503 with Retry-After when an upstream read fails", async () => {
    mockGetGuideList.mockResolvedValueOnce({ articles: [], next_cursor: null, available: false });
    const response = await GET();
    expect(response.status).toBe(503);
    expect(response.headers.get("Retry-After")).toBe("600");
  });

  it("serves valid empty XML when no stories were published in the last 48 hours", async () => {
    const response = await GET();
    const text = await response.text();
    expect(response.status).toBe(200);
    expect(response.headers.get("Content-Type")).toBe("application/xml; charset=utf-8");
    expect(text).toContain("<urlset");
    expect(text).not.toContain("<url>");
  });
});
