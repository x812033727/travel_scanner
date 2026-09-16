import { cleanup, render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import catalogue from "@/lib/guide-series.json";
import LifeHubPage, { generateMetadata } from "./page";

/**
 * The lifestyle hub is the section's only listing: no kind segment, its own topic
 * vocabulary, and its own filtered-view robots rule.
 */

const mocks = vi.hoisted(() => ({
  list: vi.fn(), topics: vi.fn(), series: vi.fn(), summary: vi.fn(),
  redirect: vi.fn(() => { throw new Error("NEXT_REDIRECT"); }),
}));
vi.mock("@/components/site-header", () => ({ SiteHeader: () => null }));
vi.mock("next/navigation", () => ({ redirect: mocks.redirect }));
// Only the reads are stubbed: `hubIsEmpty` stays the real rule, so a test that fakes an
// empty listing is exercising the indexing decision rather than restating it.
vi.mock("@/lib/guides.server", async (original) => ({
  ...await original<typeof import("@/lib/guides.server")>(),
  getGuideList: mocks.list, getGuideTopics: mocks.topics,
  getSeriesIndex: mocks.series, guideSitemapSummary: mocks.summary,
}));

const geminiRow = {
  slug: "gemini", section: "life" as const, source: "web-gemini" as const, topic: "ai-chat", entries: null,
  hub: { kind: "life" as const, slug: catalogue.hubSlug, title: "Gemini 完整教學" },
};
const claudeRow = {
  slug: "claude-code", section: "life" as const, source: "api-series" as const, topic: "claude-code", entries: 96,
  hub: { kind: "life" as const, slug: "claude-code-tutorials", title: "Claude Code 教學中心", description: "從安裝到進階" },
};

const summary = {
  slug: "ai-notes", kind: "life" as const, destination_id: null, destination_label: null,
  topics: [{ slug: "ai", label: "AI 工具", section: "life" as const }],
  title: "我每天在用的 AI 工具", description: "四個工具與各自的代價",
  published_at: "2026-09-10T00:00:00Z", valid_until: null, featured: false,
};

const params = Promise.resolve({ locale: "zh-TW" as const });
const search = (over: Record<string, string> = {}) => Promise.resolve({ ...over });

/** The section listing answers with `articles`; the news read (the `ai-news` topic) answers
 *  empty unless a test says otherwise, so a card is on the page once. */
const listing = (articles: unknown[]) =>
  mocks.list.mockImplementation(async (_locale: string, filters: { topic?: string }) =>
    ({ articles: filters.topic === "ai-news" ? [] : articles, next_cursor: null, available: true }));

beforeEach(() => {
  vi.clearAllMocks();
  listing([summary]);
  mocks.topics.mockResolvedValue([{ slug: "ai", label: "AI 工具", section: "life" }]);
  mocks.series.mockResolvedValue([]);
  mocks.summary.mockResolvedValue({ counts: [], available: false });
});

describe("the lifestyle listing", () => {
  it("asks for its own kind and its own vocabulary, never the travel ones", async () => {
    render(await LifeHubPage({ params, searchParams: search() }));
    expect(mocks.list).toHaveBeenCalledWith(
      "zh-TW", expect.objectContaining({ kind: "life" }), 24,
    );
    expect(mocks.topics).toHaveBeenCalledWith("zh-TW", "life");
  });

  it("titles itself with the section name and links each article at its own URL", async () => {
    render(await LifeHubPage({ params, searchParams: search() }));
    expect(screen.getByRole("heading", { level: 1 }).textContent).toBe("生活分享");
    expect(screen.getByRole("link", { name: "我每天在用的 AI 工具" }).getAttribute("href"))
      .toBe("/life/ai-notes");
  });

  it("passes the topic filter through and marks the active chip", async () => {
    render(await LifeHubPage({ params, searchParams: search({ topic: "ai" }) }));
    expect(mocks.list).toHaveBeenCalledWith(
      "zh-TW", expect.objectContaining({ kind: "life", topic: "ai" }), 24,
    );
    // The chip leads to the topic's hub, the page that ranks for it, not to another
    // `?topic=` view of this listing.
    const chip = screen.getByRole("link", { name: "AI 工具" });
    expect(chip.getAttribute("href")).toBe("/life/topics/ai");
    expect(chip.getAttribute("aria-current")).toBe("page");
  });

  it("says the section is empty rather than rendering a bare heading", async () => {
    mocks.list.mockResolvedValue({ articles: [], next_cursor: null, available: true });
    render(await LifeHubPage({ params, searchParams: search() }));
    expect(screen.getByText("這裡還沒有已發布的內容。")).toBeTruthy();
  });

  it("opens with a search box scoped to the section, and says nothing about how big it is", async () => {
    mocks.topics.mockResolvedValue([
      { slug: "ai", label: "AI 工具", section: "life", parent: null, description: "AI 的一切。", count: 500 },
      { slug: "ai-terms", label: "AI 名詞解釋", section: "life", parent: "ai", count: 80 },
      { slug: "finance", label: "理財", section: "life", parent: null, count: 40 },
      { slug: "misc", label: "其他", section: "life", parent: null, count: 0 },
    ]);
    render(await LifeHubPage({ params, searchParams: search() }));
    const form = screen.getByRole("search");
    expect(form.getAttribute("action")).toBe("/zh-TW/search/articles");
    expect(form.querySelector('input[name="section"]')?.getAttribute("value")).toBe("life");
    // The hub used to print "818 篇文章 2 個主題" here; the section grows every week.
    expect(screen.queryByTestId("hub-stats")).toBeNull();
    // The tiles: a parent with its lead and sub-topic chip, an empty parent left out.
    expect(screen.getByText("AI 的一切。")).toBeTruthy();
    expect(screen.getByRole("link", { name: "AI 名詞解釋" }).getAttribute("href")).toBe("/life/topics/ai-terms");
    expect(screen.queryByRole("link", { name: "其他" })).toBeNull();
    // 500 / 80 / 40 decide which tiles draw; none of them reaches the page.
    expect(screen.getByTestId("topic-tiles").textContent).not.toMatch(/\d/);
    expect(screen.getByRole("heading", { level: 2, name: "全部文章" })).toBeTruthy();
  });

  it("leaves the series to the topic hubs, while still reading the registry to place Gemini", async () => {
    mocks.series.mockResolvedValue([claudeRow, geminiRow]);
    render(await LifeHubPage({ params, searchParams: search() }));
    // Every series names one topic, so it belongs on that topic's hub rather than here.
    expect(screen.queryByTestId("series-row")).toBeNull();
    expect(screen.queryByRole("link", { name: "Claude Code 教學中心" })).toBeNull();
    expect(screen.queryByText(/篇完整教學/)).toBeNull();
    // The registry row is still the Gemini hub's publication signal -- the next test
    // depends on it -- so the read stays even though nothing draws from it here.
    expect(mocks.series).toHaveBeenCalledWith("zh-TW");
  });

  it("keeps Gemini lessons out of the listing until the registry lists the hub, which is when it is published", async () => {
    const lesson = { ...summary, slug: catalogue.articles[0].slug, title: "Gemini 第一課" };
    listing([summary, lesson]);
    render(await LifeHubPage({ params, searchParams: search() }));
    expect(screen.queryByRole("link", { name: "Gemini 第一課" })).toBeNull();
    expect(screen.getByRole("link", { name: "我每天在用的 AI 工具" })).toBeTruthy();
    cleanup();
    mocks.series.mockResolvedValue([geminiRow]);
    render(await LifeHubPage({ params, searchParams: search() }));
    expect(screen.getByRole("link", { name: "Gemini 第一課" }).getAttribute("href")).toBe(`/life/${catalogue.articles[0].slug}`);
  });

  it("opens with the newest news from the news topic, with the topic hub as see-all, on the plain page only", async () => {
    const news = { ...summary, slug: "ai-news-openai-devday", title: "OpenAI DevDay 重點", topics: [{ slug: "ai-news", label: "AI 新聞與趨勢", section: "life" as const }] };
    mocks.list.mockImplementation(async (_locale: string, filters: { topic?: string }) =>
      filters.topic === "ai-news"
        ? { articles: [news], next_cursor: null, available: true }
        : { articles: [summary], next_cursor: null, available: true });
    mocks.topics.mockResolvedValue([
      { slug: "ai", label: "AI 工具", section: "life", parent: null, count: 5 },
      { slug: "ai-news", label: "AI 新聞與趨勢", section: "life", parent: "ai", description: "這週的 AI 大事。", count: 3 },
    ]);
    render(await LifeHubPage({ params, searchParams: search() }));
    // Newest first is the API's default order, so no `sort` rides along.
    expect(mocks.list).toHaveBeenCalledWith("zh-TW", { kind: "life", topic: "ai-news" }, 6);
    const block = screen.getByTestId("life-news");
    expect(block.querySelector("h2")?.textContent).toBe("最新新聞");
    expect(screen.getByText("這週的 AI 大事。")).toBeTruthy();
    expect(screen.getByRole("link", { name: "看全部" }).getAttribute("href")).toBe("/life/topics/ai-news");
    expect(screen.getByRole("link", { name: "OpenAI DevDay 重點" }).getAttribute("href")).toBe("/life/ai-news-openai-devday");
    // The news comes right after the hero, before the topics.
    expect(block.compareDocumentPosition(screen.getByTestId("topic-tiles")) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
    cleanup();
    mocks.list.mockClear();
    render(await LifeHubPage({ params, searchParams: search({ topic: "ai" }) }));
    expect(screen.queryByTestId("life-news")).toBeNull();
    expect(mocks.list).not.toHaveBeenCalledWith("zh-TW", expect.objectContaining({ topic: "ai-news" }), 6);
  });

  it("lists in the editor's order, so the overview leads whatever batch came last", async () => {
    await LifeHubPage({ params, searchParams: search() });
    expect(mocks.list).toHaveBeenCalledWith("zh-TW", expect.objectContaining({ sort: "curated" }), 24);
  });

  it("sends a reader whose cursor the API refused to the first page, never to an empty 200", async () => {
    mocks.list.mockResolvedValue({ articles: [], next_cursor: null, available: false });
    await expect(LifeHubPage({ params, searchParams: search({ cursor: "stale" }) })).rejects.toThrow("NEXT_REDIRECT");
    expect(mocks.redirect).toHaveBeenCalledWith("/life");
    mocks.redirect.mockClear();
    render(await LifeHubPage({ params, searchParams: search() }));
    expect(mocks.redirect).not.toHaveBeenCalled();
  });

  it("carries the cursor on the same listing URL as the filter", async () => {
    mocks.list.mockResolvedValue({ articles: [summary], next_cursor: "abc==", available: true });
    render(await LifeHubPage({ params, searchParams: search({ topic: "ai" }) }));
    expect(screen.getByRole("link", { name: "看更多" }).getAttribute("href"))
      .toBe("/life?topic=ai&cursor=abc%3D%3D");
  });
});

describe("what the lifestyle listing tells search engines", () => {
  it("names the topic hub as canonical for a ?topic= view, and nothing otherwise", async () => {
    const filtered = await generateMetadata({ params, searchParams: search({ topic: "ai" }) });
    expect(filtered.alternates).toEqual({ canonical: "http://localhost:3000/zh-TW/life/topics/ai" });
    const plain = await generateMetadata({ params, searchParams: search() });
    expect(plain.alternates).toBeUndefined();
  });

  it("is indexable unfiltered", async () => {
    const metadata = await generateMetadata({ params, searchParams: search() });
    expect(metadata.robots).toBeUndefined();
  });

  // A filtered view is the same collection reordered; it must not compete with the section.
  it.each<Record<string, string>>([{ topic: "ai" }, { cursor: "abc==" }])("is noindex for %o", async (over) => {
    const metadata = await generateMetadata({ params, searchParams: search(over) });
    expect(metadata.robots).toEqual({ index: false, follow: true });
  });

  // Every lifestyle article is zh-TW today, so /en/life, /ja/life, /ko/life and /zh-CN/life
  // are a heading over "nothing here yet": nothing to rank, and a soft 404 to Search Console.
  it("keeps a language with nothing published out of the index, but still followed", async () => {
    mocks.list.mockResolvedValue({ articles: [], next_cursor: null, available: true });
    const metadata = await generateMetadata({ params, searchParams: search() });
    expect(metadata.robots).toEqual({ index: false, follow: true });
  });

  it("stays indexable when the listing could not be read, because empty is not the same as failed", async () => {
    // One API failure must not noindex the section in the language that does publish it.
    mocks.list.mockResolvedValue({ articles: [], next_cursor: null, available: false });
    const metadata = await generateMetadata({ params, searchParams: search() });
    expect(metadata.robots).toBeUndefined();
  });

  it("reads the listing once for the metadata and the body together", async () => {
    // Both call getGuideList with identical arguments, which is what lets React's per-request
    // cache answer the second from the first instead of asking the API twice per crawl.
    const arguments_ = { kind: "life", topic: undefined, cursor: undefined, sort: "curated" };
    await generateMetadata({ params, searchParams: search() });
    render(await LifeHubPage({ params, searchParams: search() }));
    // The news block is the body's own read; the section listing is the shared one.
    const listing = mocks.list.mock.calls.filter((call) => call[1].topic !== "ai-news");
    expect(listing).toEqual([["zh-TW", arguments_, 24], ["zh-TW", arguments_, 24]]);
  });
});
