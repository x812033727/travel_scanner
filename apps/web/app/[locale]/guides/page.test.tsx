import { render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import GuidesHubPage, { generateMetadata } from "./page";

/**
 * The section hub over both travel kinds. Its own rule is the one the kind hubs do not have:
 * it is empty only when intel and how-to are both empty, so a language with one article of
 * either kind still belongs in the index.
 */

const mocks = vi.hoisted(() => ({ list: vi.fn(), topics: vi.fn() }));
vi.mock("@/components/site-header", () => ({ SiteHeader: () => null }));
// Only the two reads are stubbed: `hubIsEmpty` stays the real rule, so a test that fakes
// an empty listing is exercising the indexing decision rather than restating it.
vi.mock("@/lib/guides.server", async (original) => ({
  ...await original<typeof import("@/lib/guides.server")>(),
  getGuideList: mocks.list, getGuideTopics: mocks.topics,
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
      ["zh-TW", { kind: "intel" }, 6], ["zh-TW", { kind: "howto" }, 6],
      ["zh-TW", { kind: "intel" }, 6], ["zh-TW", { kind: "howto" }, 6],
    ]);
  });
});
