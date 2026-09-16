import { cleanup, render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import GuideListPage, { generateMetadata } from "./page";

const mocks = vi.hoisted(() => ({
  list: vi.fn(), topics: vi.fn(), summary: vi.fn(),
  notFound: vi.fn(() => { throw new Error("NEXT_NOT_FOUND"); }),
  redirect: vi.fn(() => { throw new Error("NEXT_REDIRECT"); }),
}));
vi.mock("@/components/site-header", () => ({ SiteHeader: () => null }));
// Only the two reads are stubbed: `hubIsEmpty` stays the real rule, so a test that fakes
// an empty listing is exercising the indexing decision rather than restating it.
vi.mock("@/lib/guides.server", async (original) => ({
  ...await original<typeof import("@/lib/guides.server")>(),
  getGuideList: mocks.list, getGuideTopics: mocks.topics, guideSitemapSummary: mocks.summary,
}));
vi.mock("next/navigation", () => ({ notFound: mocks.notFound, redirect: mocks.redirect }));

const summary = {
  slug: "jr-pass-sale", kind: "intel" as const, destination_id: "tokyo", destination_label: "東京",
  topics: [{ slug: "transport", label: "交通" }], title: "JR Pass 調價", description: "十月起調整",
  published_at: "2026-09-01T00:00:00Z", valid_until: "2026-10-01", featured: false,
};

const params = (kind = "intel") => Promise.resolve({ locale: "zh-TW" as const, kind });
const search = (over: { topic?: string; destination?: string; country?: string; cursor?: string; sort?: string } = {}) =>
  Promise.resolve(over);

beforeEach(() => {
  vi.clearAllMocks();
  mocks.list.mockResolvedValue({ articles: [summary], next_cursor: null, available: true });
  mocks.topics.mockResolvedValue([{ slug: "transport", label: "交通" }]);
  mocks.summary.mockResolvedValue({ counts: [], available: false });
});

describe("the section listing", () => {
  it("answers 404 for a section that does not exist", async () => {
    await expect(GuideListPage({ params: params("recipes"), searchParams: search() }))
      .rejects.toThrow("NEXT_NOT_FOUND");
    expect(mocks.list).not.toHaveBeenCalled();
  });

  it("renders the articles the server resolved for this URL", async () => {
    render(await GuideListPage({ params: params(), searchParams: search() }));
    expect(screen.getByRole("heading", { level: 1 }).textContent).toBe("旅遊情報");
    expect(screen.getByRole("link", { name: "JR Pass 調價" }).getAttribute("href"))
      .toBe("/guides/intel/jr-pass-sale");
  });

  it("resolves the filter on the server, not after hydration", async () => {
    await GuideListPage({ params: params(), searchParams: search({ topic: "transport" }) });
    expect(mocks.list).toHaveBeenCalledWith("zh-TW", expect.objectContaining({ topic: "transport" }), 24);
  });

  it("marks the active topic chip so the reader can see the filter, and links it to the topic hub", async () => {
    render(await GuideListPage({ params: params(), searchParams: search({ topic: "transport" }) }));
    const chip = screen.getByRole("link", { name: "交通" });
    expect(chip.getAttribute("aria-current")).toBe("page");
    expect(chip.getAttribute("href")).toBe("/guides/topics/transport");
  });

  it("lists how-to guides in the editor's order and intel newest first", async () => {
    await GuideListPage({ params: params("howto"), searchParams: search() });
    expect(mocks.list).toHaveBeenLastCalledWith("zh-TW", expect.objectContaining({ kind: "howto", sort: "curated" }), 24);
    await GuideListPage({ params: params("intel"), searchParams: search() });
    expect(mocks.list).toHaveBeenLastCalledWith("zh-TW", expect.objectContaining({ kind: "intel", sort: "latest" }), 24);
  });

  it("lets the reader flip the order with ?sort=, keeps the filters on the order links, and ignores nonsense", async () => {
    render(await GuideListPage({ params: params("howto"), searchParams: search({ sort: "latest", topic: "transport" }) }));
    expect(mocks.list).toHaveBeenLastCalledWith("zh-TW", expect.objectContaining({ kind: "howto", sort: "latest" }), 24);
    const latest = screen.getByRole("link", { name: "最新優先" });
    expect(latest.getAttribute("aria-current")).toBe("page");
    expect(latest.getAttribute("href")).toBe("/guides/howto?topic=transport&sort=latest");
    // The kind's own default order is the canonical address: no `sort` on it.
    expect(screen.getByRole("link", { name: "精選優先" }).getAttribute("href")).toBe("/guides/howto?topic=transport");
    await GuideListPage({ params: params("howto"), searchParams: search({ sort: "random" }) });
    expect(mocks.list).toHaveBeenLastCalledWith("zh-TW", expect.objectContaining({ sort: "curated" }), 24);
  });

  it("never says how many articles the kind has, filtered or not", async () => {
    // The listing grows every week, so a figure printed here is wrong between deploys.
    // The summary is still what the sitemap is built from; this page just stopped reading it.
    render(await GuideListPage({ params: params("intel"), searchParams: search() }));
    expect(screen.queryByText(/篇文章/)).toBeNull();
    expect(mocks.summary).not.toHaveBeenCalled();
    cleanup();
    render(await GuideListPage({ params: params("intel"), searchParams: search({ topic: "transport" }) }));
    expect(screen.queryByText(/篇文章/)).toBeNull();
  });

  it("sends a reader whose cursor the API refused to the first page, never to an empty 200", async () => {
    // A "see more" link minted before how-to changed its order carries a cursor the new
    // order refuses (422), which the loader reports as unavailable.
    mocks.list.mockResolvedValue({ articles: [], next_cursor: null, available: false });
    await expect(GuideListPage({ params: params("howto"), searchParams: search({ cursor: "stale", topic: "transport" }) }))
      .rejects.toThrow("NEXT_REDIRECT");
    expect(mocks.redirect).toHaveBeenCalledWith("/guides/howto?topic=transport");
    // Without a cursor an unavailable listing is the ordinary empty page, not a redirect.
    mocks.redirect.mockClear();
    render(await GuideListPage({ params: params("howto"), searchParams: search() }));
    expect(mocks.redirect).not.toHaveBeenCalled();
  });

  it("resolves a country filter on the server too", async () => {
    await GuideListPage({ params: params("howto"), searchParams: search({ country: "japan" }) });
    expect(mocks.list).toHaveBeenCalledWith("zh-TW", expect.objectContaining({ country: "japan" }), 24);
  });

  it("says the section is empty rather than showing a bare heading, and offers the search", async () => {
    mocks.list.mockResolvedValue({ articles: [], next_cursor: null, available: true });
    render(await GuideListPage({ params: params(), searchParams: search() }));
    expect(screen.getByText("這裡還沒有已發布的內容。")).toBeTruthy();
    expect(screen.getByRole("search").getAttribute("action")).toBe("/zh-TW/search/articles");
  });

  it("offers the next page only when the API says there is one", async () => {
    render(await GuideListPage({ params: params(), searchParams: search() }));
    expect(screen.queryByRole("link", { name: "看更多" })).toBeNull();
    mocks.list.mockResolvedValue({ articles: [summary], next_cursor: "abc123", available: true });
    render(await GuideListPage({ params: params(), searchParams: search() }));
    expect(screen.getByRole("link", { name: "看更多" }).getAttribute("href")).toContain("cursor=abc123");
  });
});

describe("indexing", () => {
  it("lets the unfiltered section be indexed", async () => {
    const metadata = await generateMetadata({ params: params(), searchParams: search() });
    expect(metadata.title).toBe("旅遊情報");
    expect(metadata.robots).toBeUndefined();
  });

  it("names the topic hub as canonical for a ?topic= view", async () => {
    const metadata = await generateMetadata({ params: params(), searchParams: search({ topic: "transport" }) });
    expect(metadata.alternates).toEqual({ canonical: "http://localhost:3000/zh-TW/guides/topics/transport" });
  });

  it.each([{ topic: "transport" }, { destination: "tokyo" }, { country: "japan" }, { cursor: "abc" }, { sort: "latest" }])(
    "keeps a filtered view out of the index (%o)",
    async (filters) => {
      const metadata = await generateMetadata({ params: params(), searchParams: search(filters) });
      expect(metadata.robots).toEqual({ index: false, follow: true });
    },
  );

  // Every article is zh-TW today, so /en/guides/intel and its three siblings are a heading
  // over "nothing here yet". Nothing to rank, and a soft 404 to Search Console.
  it("keeps a language with nothing published out of the index, but still followed", async () => {
    mocks.list.mockResolvedValue({ articles: [], next_cursor: null, available: true });
    const metadata = await generateMetadata({ params: params(), searchParams: search() });
    expect(metadata.robots).toEqual({ index: false, follow: true });
  });

  it("stays indexable when the listing could not be read, because empty is not the same as failed", async () => {
    mocks.list.mockResolvedValue({ articles: [], next_cursor: null, available: false });
    const metadata = await generateMetadata({ params: params(), searchParams: search() });
    expect(metadata.robots).toBeUndefined();
  });

  it("asks for nothing extra on a filtered view, which is noindex whatever the listing says", async () => {
    mocks.list.mockClear();
    await generateMetadata({ params: params(), searchParams: search({ topic: "transport" }) });
    expect(mocks.list).not.toHaveBeenCalled();
  });

  it("does not set its own alternates, so the root layout keeps the language set", async () => {
    const metadata = await generateMetadata({ params: params(), searchParams: search() });
    expect(metadata.alternates).toBeUndefined();
  });
});
