import { cleanup, render, screen, within } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import ArticleSearchPage, { generateMetadata } from "./page";

/**
 * The results page over the article search. What it owns: turning the URL into one API
 * read, telling "nothing matched" from "the API refused the words" from "the API is down",
 * and keeping every result set reachable without JavaScript.
 */

const mocks = vi.hoisted(() => ({ search: vi.fn(), topics: vi.fn(), series: vi.fn() }));
vi.mock("@/components/site-header", () => ({ SiteHeader: () => null }));
vi.mock("@/lib/guides.server", async (original) => ({
  ...await original<typeof import("@/lib/guides.server")>(),
  getGuideSearch: mocks.search, getGuideTopics: mocks.topics, getSeriesIndex: mocks.series,
}));

const hit = (slug: string, title: string, kind: "intel" | "howto" | "life" = "howto") => ({
  slug, kind, destination_id: kind === "life" ? null : "tokyo", destination_label: kind === "life" ? null : "東京",
  topics: [{ slug: "transport", label: "交通" }], title, description: "描述",
  published_at: "2026-09-01T00:00:00Z", valid_until: null, featured: false,
  snippet: "…提到 JR Pass 的段落…", matched: ["jr", "pass"],
});
const answer = (overrides: Partial<Record<string, unknown>> = {}) => ({
  query: "JR Pass", total: 1, offset: 0, limit: 10, results: [hit("jr-pass-guide", "JR Pass 值得買嗎")],
  best_match: null, next_offset: null, available: true, invalid: false, ...overrides,
});

const params = Promise.resolve({ locale: "zh-TW" as const });
const page = (search: Record<string, string>) => ArticleSearchPage({ params, searchParams: Promise.resolve(search) });

beforeEach(() => {
  vi.clearAllMocks();
  mocks.search.mockResolvedValue(answer());
  mocks.topics.mockResolvedValue([]);
  mocks.series.mockResolvedValue([]);
});
afterEach(cleanup);

describe("/search/articles", () => {
  it("stays out of the index and asks for its own title", async () => {
    const metadata = await generateMetadata({ params });
    expect(metadata.title).toBe("搜尋文章與攻略｜Mokaair");
    expect(metadata.robots).toEqual({ index: false, follow: true });
  });

  it("reads the query, section and offset from the URL and hands them to one search", async () => {
    render(await page({ q: " JR Pass ", section: "travel", offset: "10" }));
    expect(mocks.search).toHaveBeenCalledWith("zh-TW", { q: "JR Pass", section: "travel", offset: 10 });
    expect(screen.getByRole("heading", { level: 2, name: "「JR Pass」共 1 篇文章" })).toBeTruthy();
    expect(screen.getByRole("link", { name: /JR Pass 值得買嗎/ }).getAttribute("href")).toBe("/guides/howto/jr-pass-guide");
    // The words the reader typed are marked in the passage.
    expect(screen.getAllByText("JR", { selector: "mark" }).length).toBeGreaterThan(0);
  });

  it("drops a section it does not know and a garbled offset rather than passing them on", async () => {
    render(await page({ q: "JR Pass", section: "nope", offset: "abc" }));
    expect(mocks.search).toHaveBeenCalledWith("zh-TW", { q: "JR Pass", section: undefined, offset: 0 });
  });

  it("is a plain GET form, so a result set has a URL without JavaScript", async () => {
    render(await page({ q: "JR Pass", section: "life" }));
    const form = screen.getByRole("search");
    expect(form.getAttribute("method")).toBe("get");
    expect(form.getAttribute("action")).toBe("/zh-TW/search/articles");
    expect((within(form).getByRole("searchbox") as HTMLInputElement).value).toBe("JR Pass");
    // The section travels with the words, as a hidden field.
    expect(form.querySelector('input[name="section"]')?.getAttribute("value")).toBe("life");
  });

  it("keeps the query on the scope chips and marks the current one", async () => {
    render(await page({ q: "JR Pass", section: "life" }));
    const scope = screen.getByRole("navigation", { name: "搜尋範圍" });
    expect(within(scope).getByRole("link", { name: "全部" }).getAttribute("href")).toBe("/search/articles?q=JR+Pass");
    expect(within(scope).getByRole("link", { name: "旅遊情報攻略" }).getAttribute("href")).toBe("/search/articles?q=JR+Pass&section=travel");
    expect(within(scope).getByRole("link", { name: "生活分享" }).getAttribute("aria-current")).toBe("page");
  });

  it("shows the best match above the list and never repeats it there", async () => {
    mocks.search.mockResolvedValue(answer({ best_match: hit("jr-pass", "JR Pass"), results: [hit("other", "另一篇")] }));
    render(await page({ q: "JR Pass" }));
    expect(screen.getByRole("heading", { level: 2, name: "最符合的文章" })).toBeTruthy();
    expect(screen.getAllByRole("link", { name: /JR Pass$/ })).toHaveLength(1);
    expect(screen.getByRole("link", { name: /另一篇/ })).toBeTruthy();
  });

  it("pages by offset and says where the reader is", async () => {
    mocks.search.mockResolvedValue(answer({ total: 25, offset: 10, next_offset: 20 }));
    render(await page({ q: "JR Pass", offset: "10" }));
    const pagination = screen.getByRole("navigation", { name: "結果分頁" });
    expect(within(pagination).getByRole("link", { name: "上一頁" }).getAttribute("href")).toBe("/search/articles?q=JR+Pass");
    expect(within(pagination).getByRole("link", { name: "下一頁" }).getAttribute("href")).toBe("/search/articles?q=JR+Pass&offset=20");
    expect(within(pagination).getByText("第 2／3 頁")).toBeTruthy();
  });

  it("draws no pagination for a single page", async () => {
    render(await page({ q: "JR Pass" }));
    expect(screen.queryByRole("navigation", { name: "結果分頁" })).toBeNull();
  });

  it("says nothing matched and offers the topics and series to browse instead", async () => {
    mocks.search.mockResolvedValue(answer({ total: 0, results: [] }));
    mocks.topics.mockImplementation(async (_locale: string, section: string) => section === "travel"
      ? [{ slug: "transport", label: "交通", section: "travel", parent: null, count: 3 }, { slug: "beach", label: "海灘", parent: null, count: 0 }]
      : [{ slug: "ai", label: "AI", section: "life", parent: null, count: 5 }, { slug: "ai-terms", label: "名詞", parent: "ai", count: 2 }]);
    mocks.series.mockResolvedValue([{ slug: "codex", section: "life", hub: { kind: "life", slug: "codex-hub", title: "Codex 教學" }, source: "api-series", topic: "ai", entries: 20 }]);
    render(await page({ q: "zzz" }));
    expect(screen.getByRole("heading", { level: 2, name: "找不到符合「zzz」的文章。" })).toBeTruthy();
    expect(screen.getByRole("link", { name: /交通/ }).getAttribute("href")).toBe("/guides/topics/transport");
    expect(screen.getByRole("link", { name: /^AI/ }).getAttribute("href")).toBe("/life/topics/ai");
    // Only top-level topics with something under them.
    expect(screen.queryByRole("link", { name: /海灘/ })).toBeNull();
    expect(screen.queryByRole("link", { name: /名詞/ })).toBeNull();
    expect(screen.getByRole("link", { name: "Codex 教學" }).getAttribute("href")).toBe("/life/codex-hub");
  });

  it("tells a refused query from an outage, and reads nothing else in either case", async () => {
    mocks.search.mockResolvedValue(answer({ total: 0, results: [], invalid: true }));
    render(await page({ q: "a" }));
    expect(screen.getByRole("alert").textContent).toBe("請輸入至少一個可以搜尋的字詞。");
    expect(screen.queryByRole("heading", { level: 2 })).toBeNull();
    expect(mocks.topics).not.toHaveBeenCalled();
    cleanup();
    mocks.search.mockResolvedValue(answer({ total: 0, results: [], available: false }));
    render(await page({ q: "JR Pass" }));
    expect(screen.getByRole("alert").textContent).toBe("搜尋暫時無法使用，請稍後再試。");
    expect(mocks.topics).not.toHaveBeenCalled();
  });

  it("without a query shows the form and the browse lists, and never calls the API", async () => {
    mocks.topics.mockResolvedValue([{ slug: "ai", label: "AI", parent: null, count: 5 }]);
    render(await page({}));
    expect(mocks.search).not.toHaveBeenCalled();
    expect(screen.getByRole("search")).toBeTruthy();
    expect(screen.getByText("輸入關鍵字開始搜尋，或先從主題與系列瀏覽。")).toBeTruthy();
    expect(screen.getAllByRole("link", { name: /^AI/ }).length).toBeGreaterThan(0);
  });
});
