import { beforeEach, describe, expect, it, vi } from "vitest";
import { siteUrl } from "@/lib/seo";
import { GET as getLifeFeed } from "@/app/[locale]/life/feed.xml/route";
import { GET as getTopicFeed } from "@/app/[locale]/life/topics/[topic]/feed.xml/route";
import { buildGuideAtomFeed } from "./guide-atom-feed";

const mocks = vi.hoisted(() => ({
  loadGuideList: vi.fn(),
  loadGuideTopicList: vi.fn(),
}));

vi.mock("@/lib/guides.server", async (original) => ({
  ...await original<typeof import("@/lib/guides.server")>(),
  loadGuideList: mocks.loadGuideList,
  loadGuideTopicList: mocks.loadGuideTopicList,
}));

const story = {
  slug: "gemini-cli-release",
  kind: "life" as const,
  destination_id: null,
  destination_label: null,
  topics: [{ slug: "ai-news", label: "AI 新聞" }],
  title: "Gemini CLI 2.0 發布：免費額度與 <MCP> 支援總整理",
  description: "整理免費與付費額度差異，以及支援的作業系統與安裝步驟。",
  published_at: "2026-11-12T08:30:00Z",
  valid_until: null,
  news_date: "2026-11-12",
  featured: false,
};

beforeEach(() => {
  vi.clearAllMocks();
  mocks.loadGuideList.mockResolvedValue({ articles: [story], next_cursor: null, available: true });
  mocks.loadGuideTopicList.mockResolvedValue({
    topics: [{ slug: "ai-news", label: "AI 新聞", description: "每日 AI 快訊" }],
    available: true,
  });
});

describe("buildGuideAtomFeed", () => {
  it("renders valid Atom 1.0 XML with escaped titles, canonical entry URLs and topic categories", () => {
    const xml = buildGuideAtomFeed({
      locale: "zh-TW",
      feedPath: "/life/feed.xml",
      hubPath: "/life",
      title: "Mokaair｜每日 AI 科技快訊 & 軟體動態",
      subtitle: "核對官方來源的 AI、科技與加密貨幣新聞",
      articles: [story],
    });

    expect(xml.startsWith('<?xml version="1.0" encoding="UTF-8"?>\n<feed xmlns="http://www.w3.org/2005/Atom" xml:lang="zh-TW">')).toBe(true);
    expect(xml).toContain("<title>Mokaair｜每日 AI 科技快訊 &amp; 軟體動態</title>");
    expect(xml).toContain(`<link rel="self" type="application/atom+xml" href="${siteUrl}/zh-TW/life/feed.xml"/>`);
    expect(xml).toContain(`<link rel="alternate" type="text/html" href="${siteUrl}/zh-TW/life"/>`);
    expect(xml).toContain("<title>Gemini CLI 2.0 發布：免費額度與 &lt;MCP&gt; 支援總整理</title>");
    expect(xml).toContain(`<id>${siteUrl}/zh-TW/life/gemini-cli-release</id>`);
    expect(xml).toContain("<updated>2026-11-12T08:30:00.000Z</updated>");
    expect(xml).toContain('<category term="ai-news" label="AI 新聞"/>');
  });

  it("handles an empty feed with a deterministic fallback timestamp", () => {
    const xml = buildGuideAtomFeed({
      locale: "en",
      feedPath: "/life/topics/tech-news/feed.xml",
      hubPath: "/life/topics/tech-news",
      title: "Tech news | Mokaair",
      articles: [],
      fallbackUpdated: "2026-11-13T00:00:00Z",
    });
    expect(xml).toContain("<updated>2026-11-13T00:00:00.000Z</updated>");
    expect(xml).not.toContain("<entry>");
  });
});

describe("Atom feed route handlers", () => {
  it("serves merged dated news on /[locale]/life/feed.xml and returns 503 with Retry-After on API outage", async () => {
    const ok = await getLifeFeed(new Request("http://localhost:3000/zh-TW/life/feed.xml"), {
      params: Promise.resolve({ locale: "zh-TW" }),
    });
    expect(ok.status).toBe(200);
    expect(ok.headers.get("Content-Type")).toBe("application/atom+xml; charset=utf-8");
    expect(await ok.text()).toContain("gemini-cli-release");

    mocks.loadGuideList.mockResolvedValueOnce({ articles: [], next_cursor: null, available: false });
    const down = await getLifeFeed(new Request("http://localhost:3000/zh-TW/life/feed.xml"), {
      params: Promise.resolve({ locale: "zh-TW" }),
    });
    expect(down.status).toBe(503);
    expect(down.headers.get("Retry-After")).toBe("600");
  });

  it("serves news topic feeds and returns 404 for unknown locales or non-news topics", async () => {
    const ok = await getTopicFeed(new Request("http://localhost:3000/zh-TW/life/topics/ai-news/feed.xml"), {
      params: Promise.resolve({ locale: "zh-TW", topic: "ai-news" }),
    });
    expect(ok.status).toBe(200);
    expect(await ok.text()).toContain("AI 新聞");

    const nonNews = await getTopicFeed(new Request("http://localhost:3000/zh-TW/life/topics/software/feed.xml"), {
      params: Promise.resolve({ locale: "zh-TW", topic: "software" }),
    });
    expect(nonNews.status).toBe(404);

    const badLocale = await getLifeFeed(new Request("http://localhost:3000/fr/life/feed.xml"), {
      params: Promise.resolve({ locale: "fr" }),
    });
    expect(badLocale.status).toBe(404);
  });
});
