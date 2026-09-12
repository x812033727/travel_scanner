import { render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import LifeHubPage, { generateMetadata } from "./page";

/**
 * The lifestyle hub is the section's only listing: no kind segment, its own topic
 * vocabulary, and its own filtered-view robots rule.
 */

const mocks = vi.hoisted(() => ({ list: vi.fn(), topics: vi.fn() }));
vi.mock("@/components/site-header", () => ({ SiteHeader: () => null }));
vi.mock("@/lib/guides.server", () => ({ getGuideList: mocks.list, getGuideTopics: mocks.topics }));

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
  mocks.list.mockResolvedValue({ articles: [summary], next_cursor: null });
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
    const chip = screen.getByRole("link", { name: "AI 工具" });
    expect(chip.getAttribute("href")).toBe("/life?topic=ai");
    expect(chip.getAttribute("aria-current")).toBe("page");
  });

  it("says the section is empty rather than rendering a bare heading", async () => {
    mocks.list.mockResolvedValue({ articles: [], next_cursor: null });
    render(await LifeHubPage({ params, searchParams: search() }));
    expect(screen.getByText("這裡還沒有已發布的內容。")).toBeTruthy();
  });

  it("carries the cursor on the same listing URL as the filter", async () => {
    mocks.list.mockResolvedValue({ articles: [summary], next_cursor: "abc==" });
    render(await LifeHubPage({ params, searchParams: search({ topic: "ai" }) }));
    expect(screen.getByRole("link", { name: "看更多" }).getAttribute("href"))
      .toBe("/life?topic=ai&cursor=abc%3D%3D");
  });
});

describe("what the lifestyle listing tells search engines", () => {
  it("is indexable unfiltered", async () => {
    const metadata = await generateMetadata({ params, searchParams: search() });
    expect(metadata.robots).toBeUndefined();
  });

  // A filtered view is the same collection reordered; it must not compete with the section.
  it.each<Record<string, string>>([{ topic: "ai" }, { cursor: "abc==" }])("is noindex for %o", async (over) => {
    const metadata = await generateMetadata({ params, searchParams: search(over) });
    expect(metadata.robots).toEqual({ index: false, follow: true });
  });
});
