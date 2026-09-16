import { cleanup, render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import GuidesHubPage, { generateMetadata } from "./page";

/**
 * The section hub over both travel kinds. Its own rule is the one the kind hubs do not have:
 * it is empty only when intel and how-to are both empty, so a language with one article of
 * either kind still belongs in the index.
 */

const mocks = vi.hoisted(() => ({ list: vi.fn(), topics: vi.fn(), facets: vi.fn(), series: vi.fn(), summary: vi.fn() }));
vi.mock("@/components/site-header", () => ({ SiteHeader: () => null }));
// Only the reads are stubbed: `hubIsEmpty` stays the real rule, so a test that fakes an
// empty listing is exercising the indexing decision rather than restating it.
vi.mock("@/lib/guides.server", async (original) => ({
  ...await original<typeof import("@/lib/guides.server")>(),
  getGuideList: mocks.list, getGuideTopics: mocks.topics, getDestinationFacets: mocks.facets,
  getSeriesIndex: mocks.series, guideSitemapSummary: mocks.summary,
}));

const summary = {
  slug: "jr-pass-sale", kind: "intel" as const, destination_id: "tokyo", destination_label: "東京",
  topics: [{ slug: "transport", label: "交通" }], title: "JR Pass 調價", description: "十月起調整",
  published_at: "2026-09-01T00:00:00Z", valid_until: "2026-10-01", featured: false,
};

const params = Promise.resolve({ locale: "zh-TW" as const });
const list = (articles: unknown[], available = true) => ({ articles, next_cursor: null, available });
/** `intel` first, `howto` second: the hub reads them in that order. */
const lists = (intel: unknown, howto: unknown) => {
  mocks.list.mockReset();
  mocks.list.mockResolvedValueOnce(intel).mockResolvedValueOnce(howto)
    .mockResolvedValueOnce(intel).mockResolvedValueOnce(howto);
};

beforeEach(() => {
  vi.clearAllMocks();
  mocks.list.mockResolvedValue(list([summary]));
  mocks.topics.mockResolvedValue([{ slug: "transport", label: "交通" }]);
  mocks.facets.mockResolvedValue({ destinations: [], available: true });
  mocks.series.mockResolvedValue([]);
  mocks.summary.mockResolvedValue({ counts: [], available: false });
});

describe("the guides hub", () => {
  it("shows both sections and links each article at its own URL", async () => {
    render(await GuidesHubPage({ params }));
    expect(screen.getByRole("heading", { level: 1 }).textContent).toBe("旅遊情報與攻略");
    expect(screen.getAllByRole("link", { name: "JR Pass 調價" })[0].getAttribute("href"))
      .toBe("/guides/intel/jr-pass-sale");
  });

  it("says the section is empty rather than rendering a bare heading", async () => {
    mocks.list.mockResolvedValue(list([]));
    render(await GuidesHubPage({ params }));
    expect(screen.getAllByText("這裡還沒有已發布的內容。")).toHaveLength(2);
  });

  it("draws each topic with something under it as a tile linking to its hub, and leaves out an empty one", async () => {
    mocks.topics.mockResolvedValue([
      { slug: "transport", label: "交通", section: "travel", parent: null, count: 4 },
      { slug: "beach", label: "海灘", section: "travel", parent: null, count: 0 },
    ]);
    render(await GuidesHubPage({ params }));
    expect(screen.getByRole("link", { name: "交通" }).getAttribute("href")).toBe("/guides/topics/transport");
    expect(screen.getByText("4 篇")).toBeTruthy();
    expect(screen.queryByRole("link", { name: /海灘/ })).toBeNull();
  });

  it("opens with a search box scoped to the section and the figures the API gave", async () => {
    mocks.summary.mockResolvedValue({
      counts: [
        { kind: "intel", locale: "zh-TW", count: 19 }, { kind: "howto", locale: "zh-TW", count: 106 },
        { kind: "life", locale: "zh-TW", count: 800 }, { kind: "howto", locale: "en", count: 3 },
      ],
      available: true,
    });
    mocks.topics.mockResolvedValue([
      { slug: "transport", label: "交通", section: "travel", parent: null, count: 4 },
      { slug: "food", label: "美食", section: "travel", parent: null, count: 2 },
      { slug: "beach", label: "海灘", section: "travel", parent: null, count: 0 },
    ]);
    render(await GuidesHubPage({ params }));
    const form = screen.getByRole("search");
    expect(form.getAttribute("action")).toBe("/zh-TW/search/articles");
    expect(form.querySelector('input[name="section"]')?.getAttribute("value")).toBe("travel");
    // This section's kinds in this language only, and the topics with something under them.
    expect(screen.getByTestId("hub-stats").textContent).toBe("125 篇文章2 個主題");
  });

  it("lists the series the registry offers this section, and no row when there are none", async () => {
    mocks.series.mockResolvedValue([
      { slug: "claude-code", section: "life", hub: { kind: "life", slug: "claude-code-tutorials", title: "Claude Code 教學中心" }, source: "api-series", topic: "claude-code", entries: 96 },
      { slug: "japan-rail", section: "travel", hub: { kind: "howto", slug: "japan-rail-guide", title: "日本鐵路完全攻略", description: "從 JR Pass 到 IC 卡" }, source: "catalogue", topic: "transport", entries: null },
    ]);
    render(await GuidesHubPage({ params }));
    expect(screen.getByRole("link", { name: "日本鐵路完全攻略" }).getAttribute("href")).toBe("/guides/howto/japan-rail-guide");
    expect(screen.queryByRole("link", { name: "Claude Code 教學中心" })).toBeNull();
    cleanup();
    mocks.series.mockResolvedValue([]);
    render(await GuidesHubPage({ params }));
    expect(screen.queryByTestId("series-row")).toBeNull();
  });

  it("groups the destinations with articles by country, and draws nothing without any", async () => {
    mocks.facets.mockResolvedValue({
      destinations: [
        { id: "tokyo", label: "東京", country: "japan", country_label: "日本", count: 11 },
        { id: "seoul", label: "首爾", country: "south-korea", country_label: "韓國", count: 9 },
      ],
      available: true,
    });
    render(await GuidesHubPage({ params }));
    expect(mocks.facets).toHaveBeenCalledWith("zh-TW", "travel");
    expect(screen.getByRole("link", { name: /日本全部/ }).getAttribute("href")).toBe("/guides/howto?country=japan");
    expect(screen.getByRole("link", { name: /首爾/ }).getAttribute("href")).toBe("/guides/howto?destination=seoul");
    cleanup();
    mocks.facets.mockResolvedValue({ destinations: [], available: false });
    render(await GuidesHubPage({ params }));
    expect(screen.queryByTestId("destination-groups")).toBeNull();
  });
});

describe("what the guides hub tells search engines", () => {
  it("is indexable where the section publishes", async () => {
    const metadata = await generateMetadata({ params });
    expect(metadata.robots).toBeUndefined();
  });

  // Thirty articles, all zh-TW: /en/guides, /ja/guides, /ko/guides and /zh-CN/guides answer
  // 200 with two "nothing here yet" lines. Nothing to rank, and a soft 404 to Search Console.
  it("keeps a language with nothing published out of the index, but still followed", async () => {
    mocks.list.mockResolvedValue(list([]));
    const metadata = await generateMetadata({ params });
    expect(metadata.robots).toEqual({ index: false, follow: true });
  });

  it("stays in the index while either kind has an article", async () => {
    lists(list([]), list([summary]));
    expect((await generateMetadata({ params })).robots).toBeUndefined();
    lists(list([summary]), list([]));
    expect((await generateMetadata({ params })).robots).toBeUndefined();
  });

  it("stays indexable when a listing could not be read, because empty is not the same as failed", async () => {
    // One unreadable kind says nothing about the other, and an API outage must not noindex
    // the hub in the language that does publish it.
    lists(list([], false), list([]));
    expect((await generateMetadata({ params })).robots).toBeUndefined();
    mocks.list.mockReset();
    mocks.list.mockResolvedValue(list([], false));
    expect((await generateMetadata({ params })).robots).toBeUndefined();
  });

  it("reads each listing once for the metadata and the body together", async () => {
    // Both ask with identical arguments, which is what lets React's per-request cache answer
    // the body from the metadata's call instead of asking the API twice per crawl.
    await generateMetadata({ params });
    render(await GuidesHubPage({ params }));
    expect(mocks.list.mock.calls).toEqual([
      ["zh-TW", { kind: "intel" }, 6], ["zh-TW", { kind: "howto", sort: "curated" }, 6],
      ["zh-TW", { kind: "intel" }, 6], ["zh-TW", { kind: "howto", sort: "curated" }, 6],
    ]);
  });
});
