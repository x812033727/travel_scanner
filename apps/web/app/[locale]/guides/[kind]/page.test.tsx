import { render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import GuideListPage, { generateMetadata } from "./page";

const mocks = vi.hoisted(() => ({
  list: vi.fn(), topics: vi.fn(),
  notFound: vi.fn(() => { throw new Error("NEXT_NOT_FOUND"); }),
}));
vi.mock("@/components/site-header", () => ({ SiteHeader: () => null }));
vi.mock("@/lib/guides.server", () => ({ getGuideList: mocks.list, getGuideTopics: mocks.topics }));
vi.mock("next/navigation", () => ({ notFound: mocks.notFound }));

const summary = {
  slug: "jr-pass-sale", kind: "intel" as const, destination_id: "tokyo", destination_label: "東京",
  topics: [{ slug: "transport", label: "交通" }], title: "JR Pass 調價", description: "十月起調整",
  published_at: "2026-09-01T00:00:00Z", valid_until: "2026-10-01", featured: false,
};

const params = (kind = "intel") => Promise.resolve({ locale: "zh-TW" as const, kind });
const search = (over: { topic?: string; destination?: string; cursor?: string } = {}) => Promise.resolve(over);

beforeEach(() => {
  vi.clearAllMocks();
  mocks.list.mockResolvedValue({ articles: [summary], next_cursor: null });
  mocks.topics.mockResolvedValue([{ slug: "transport", label: "交通" }]);
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

  it("marks the active topic chip so the reader can see the filter", async () => {
    render(await GuideListPage({ params: params(), searchParams: search({ topic: "transport" }) }));
    expect(screen.getByRole("link", { name: "交通" }).getAttribute("aria-current")).toBe("page");
  });

  it("says the section is empty rather than showing a bare heading", async () => {
    mocks.list.mockResolvedValue({ articles: [], next_cursor: null });
    render(await GuideListPage({ params: params(), searchParams: search() }));
    expect(screen.getByText("這裡還沒有已發布的內容。")).toBeTruthy();
  });

  it("offers the next page only when the API says there is one", async () => {
    render(await GuideListPage({ params: params(), searchParams: search() }));
    expect(screen.queryByRole("link", { name: "看更多" })).toBeNull();
    mocks.list.mockResolvedValue({ articles: [summary], next_cursor: "abc123" });
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

  it.each([{ topic: "transport" }, { destination: "tokyo" }, { cursor: "abc" }])(
    "keeps a filtered view out of the index (%o)",
    async (filters) => {
      const metadata = await generateMetadata({ params: params(), searchParams: search(filters) });
      expect(metadata.robots).toEqual({ index: false, follow: true });
    },
  );

  it("does not set its own alternates, so the root layout keeps the language set", async () => {
    const metadata = await generateMetadata({ params: params(), searchParams: search() });
    expect(metadata.alternates).toBeUndefined();
  });
});
