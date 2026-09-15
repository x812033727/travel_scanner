import { render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { renderTopicHub, topicHubMetadata } from "./topic-hub-page";

/**
 * The topic hub is the page that ranks for a topic. Its rules: the label is the API's,
 * the lead falls back parent → section, an unknown topic is a 404, an unreachable
 * vocabulary is a page that says so and stays out of the index, and hreflang lists only
 * the languages with something under the topic.
 */

const mocks = vi.hoisted(() => ({
  list: vi.fn(), vocabulary: vi.fn(),
  notFound: vi.fn(() => { throw new Error("NEXT_NOT_FOUND"); }),
}));
vi.mock("@/components/site-header", () => ({ SiteHeader: () => null }));
// `hubIsEmpty` stays the real rule for the older-API case below.
vi.mock("@/lib/guides.server", async (original) => ({
  ...await original<typeof import("@/lib/guides.server")>(),
  getGuideList: mocks.list, getGuideTopicList: mocks.vocabulary,
}));
vi.mock("next/navigation", () => ({ notFound: mocks.notFound }));

const summary = {
  slug: "ai-term-quantization", kind: "life" as const, destination_id: null, destination_label: null,
  topics: [{ slug: "ai-terms", label: "AI 名詞解釋", section: "life" as const, parent: "ai" }],
  title: "量化（Quantization）是什麼", description: "用較少位元執行模型的取捨",
  published_at: "2026-09-10T00:00:00Z", valid_until: null, featured: false,
};
const topics = [
  { slug: "ai", label: "AI 工具", section: "life" as const, parent: null, description: "AI 的一切。", count: 5, counts: { "zh-TW": 5, en: 2 } },
  { slug: "ai-terms", label: "AI 名詞解釋", section: "life" as const, parent: "ai", description: null, count: 2, counts: { "zh-TW": 2 } },
  { slug: "ai-news", label: "AI 新聞與趨勢", section: "life" as const, parent: "ai", description: null, count: 0, counts: {} },
];
const route = (over: Partial<Parameters<typeof renderTopicHub>[0]> = {}) =>
  ({ locale: "zh-TW" as const, section: "life" as const, topic: "ai-terms", ...over });

beforeEach(() => {
  vi.clearAllMocks();
  mocks.vocabulary.mockResolvedValue({ topics, available: true });
  mocks.list.mockResolvedValue({ articles: [summary], next_cursor: null, available: true });
});

describe("the topic hub", () => {
  it("titles itself with the topic, falls back to the parent's lead, and lists the articles", async () => {
    render(await renderTopicHub(route()));
    expect(screen.getByRole("heading", { level: 1 }).textContent).toBe("AI 名詞解釋");
    expect(screen.getByText("AI 的一切。")).toBeTruthy();
    expect(screen.getByText("2 篇文章")).toBeTruthy();
    expect(screen.getByRole("link", { name: "量化（Quantization）是什麼" }).getAttribute("href"))
      .toBe("/life/ai-term-quantization");
    expect(mocks.list).toHaveBeenCalledWith("zh-TW", { section: "life", topic: "ai-terms", cursor: undefined }, 24);
    expect(mocks.vocabulary).toHaveBeenCalledWith("zh-TW", "life");
  });

  it("walks the breadcrumb home › section › parent › topic, and marks the topic chip current", async () => {
    render(await renderTopicHub(route()));
    const crumbs = screen.getByRole("navigation", { name: "頁面路徑" });
    const links = Array.from(crumbs.querySelectorAll("a")).map((a) => [a.textContent, a.getAttribute("href")]);
    expect(links).toEqual([["首頁", "/"], ["生活分享", "/life"], ["AI 工具", "/life/topics/ai"]]);
    expect(screen.getByRole("link", { name: /^AI 名詞解釋/ }).getAttribute("aria-current")).toBe("page");
  });

  it("answers 404 for a topic the vocabulary does not know", async () => {
    await expect(renderTopicHub(route({ topic: "recipes" }))).rejects.toThrow("NEXT_NOT_FOUND");
    await expect(topicHubMetadata(route({ topic: "recipes" }))).rejects.toThrow("NEXT_NOT_FOUND");
  });

  it("says the topic is empty in this language rather than showing a bare heading", async () => {
    mocks.list.mockResolvedValue({ articles: [], next_cursor: null, available: true });
    render(await renderTopicHub(route({ topic: "ai-news" })));
    expect(screen.getByText("這裡還沒有已發布的內容。")).toBeTruthy();
    expect(screen.queryByText(/篇文章/)).toBeNull();
  });

  it("offers the next page at its own URL only when the API says there is one", async () => {
    mocks.list.mockResolvedValue({ articles: [summary], next_cursor: "abc123", available: true });
    render(await renderTopicHub(route()));
    expect(screen.getByRole("link", { name: "看更多" }).getAttribute("href")).toBe("/life/topics/ai-terms?cursor=abc123");
  });

  it("survives an unreachable vocabulary as a page that says so, never as a 404", async () => {
    mocks.vocabulary.mockResolvedValue({ topics: [], available: false });
    render(await renderTopicHub(route()));
    expect(mocks.notFound).not.toHaveBeenCalled();
    expect(screen.getByRole("heading", { level: 1 }).textContent).toBe("ai-terms");
    expect(screen.getByText("暫時無法取得這個主題，請稍後再試。")).toBeTruthy();
  });
});

describe("what the topic hub tells search engines", () => {
  it("is indexable where the topic publishes, with a self canonical and only the published languages", async () => {
    const metadata = await topicHubMetadata(route({ topic: "ai" }));
    expect(metadata.title).toBe("AI 工具：文章與攻略 | Mokaair");
    expect(metadata.description).toBe("AI 的一切。");
    expect(metadata.robots).toBeUndefined();
    expect(metadata.alternates?.canonical).toBe("http://localhost:3000/zh-TW/life/topics/ai");
    expect(metadata.alternates?.languages).toEqual({
      en: "http://localhost:3000/en/life/topics/ai",
      "zh-TW": "http://localhost:3000/zh-TW/life/topics/ai",
      "x-default": "http://localhost:3000/en/life/topics/ai",
    });
  });

  it("describes a topic without a lead from the catalogue and lists no x-default without English", async () => {
    const metadata = await topicHubMetadata(route());
    expect(metadata.description).toBe("Mokaair 歸在「AI 名詞解釋」主題下的所有文章與攻略，依最新發布排序，每篇都附資料來源。");
    expect(metadata.alternates?.languages).toEqual({ "zh-TW": "http://localhost:3000/zh-TW/life/topics/ai-terms" });
  });

  it("keeps a topic with nothing published in this language out of the index, but followed", async () => {
    const metadata = await topicHubMetadata(route({ topic: "ai-news" }));
    expect(metadata.robots).toEqual({ index: false, follow: true });
    expect(metadata.alternates?.languages).toBeUndefined();
  });

  it("keeps a paged view out of the index", async () => {
    const metadata = await topicHubMetadata(route({ cursor: "abc" }));
    expect(metadata.robots).toEqual({ index: false, follow: true });
    expect(mocks.list).toHaveBeenCalledWith("zh-TW", { section: "life", topic: "ai-terms", cursor: "abc" }, 24);
  });

  it("keeps an unreachable vocabulary out of the index rather than claiming the topic is gone", async () => {
    mocks.vocabulary.mockResolvedValue({ topics: [], available: false });
    const metadata = await topicHubMetadata(route());
    expect(metadata.robots).toEqual({ index: false, follow: true });
    expect(metadata.title).toBe("ai-terms：文章與攻略 | Mokaair");
  });

  it("falls back to the listing's own emptiness when an older API sends no counts", async () => {
    mocks.vocabulary.mockResolvedValue({ topics: [{ slug: "ai-terms", label: "AI 名詞解釋", section: "life" }], available: true });
    expect((await topicHubMetadata(route())).robots).toBeUndefined();
    mocks.list.mockResolvedValue({ articles: [], next_cursor: null, available: true });
    expect((await topicHubMetadata(route())).robots).toEqual({ index: false, follow: true });
    // A failed listing read is not an empty topic.
    mocks.list.mockResolvedValue({ articles: [], next_cursor: null, available: false });
    expect((await topicHubMetadata(route())).robots).toBeUndefined();
  });

  it("reads the vocabulary and the listing once for the metadata and the body together", async () => {
    await topicHubMetadata(route());
    render(await renderTopicHub(route()));
    expect(mocks.list.mock.calls).toEqual([
      ["zh-TW", { section: "life", topic: "ai-terms", cursor: undefined }, 24],
      ["zh-TW", { section: "life", topic: "ai-terms", cursor: undefined }, 24],
    ]);
  });
});
