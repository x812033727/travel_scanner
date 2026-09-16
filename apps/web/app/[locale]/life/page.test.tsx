import { render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import LifeHubPage, { generateMetadata } from "./page";

/**
 * The lifestyle hub is the section's only listing: no kind segment, its own topic
 * vocabulary, and its own filtered-view robots rule.
 */

const mocks = vi.hoisted(() => ({
  list: vi.fn(), topics: vi.fn(), article: vi.fn(),
  redirect: vi.fn(() => { throw new Error("NEXT_REDIRECT"); }),
}));
vi.mock("@/components/site-header", () => ({ SiteHeader: () => null }));
vi.mock("next/navigation", () => ({ redirect: mocks.redirect }));
// Only the two reads are stubbed: `hubIsEmpty` stays the real rule, so a test that fakes
// an empty listing is exercising the indexing decision rather than restating it.
vi.mock("@/lib/guides.server", async (original) => ({
  ...await original<typeof import("@/lib/guides.server")>(),
  getGuideList: mocks.list, getGuideTopics: mocks.topics, getGuideArticle: mocks.article,
}));

const summary = {
  slug: "ai-notes", kind: "life" as const, destination_id: null, destination_label: null,
  topics: [{ slug: "ai", label: "AI 工具", section: "life" as const }],
  title: "我每天在用的 AI 工具", description: "四個工具與各自的代價",
  published_at: "2026-09-10T00:00:00Z", valid_until: null, featured: false,
};

const params = Promise.resolve({ locale: "zh-TW" as const });
const search = (over: Record<string, string> = {}) => Promise.resolve({ ...over });

beforeEach(() => {
  vi.clearAllMocks();
  mocks.article.mockResolvedValue({ status: "unpublished", document: null });
  mocks.list.mockResolvedValue({ articles: [summary], next_cursor: null, available: true });
  mocks.topics.mockResolvedValue([{ slug: "ai", label: "AI 工具", section: "life" }]);
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
    for (const call of mocks.list.mock.calls) expect(call).toEqual(["zh-TW", arguments_, 24]);
  });
});
