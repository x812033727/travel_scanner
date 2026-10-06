import { render, screen, within } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { AiHubRails, loadAiHubRails } from "./ai-hub-rails";

const mocks = vi.hoisted(() => ({ list: vi.fn() }));
vi.mock("@/lib/guides.server", () => ({ getGuideList: mocks.list }));

const article = (slug: string) => ({
  slug, kind: "life" as const, destination_id: null, destination_label: null, topics: [],
  title: `Title ${slug}`, description: "d", published_at: "2026-09-10T00:00:00Z", valid_until: null, featured: false,
  news_date: "2026-10-01",
});
const topic = (slug: string, count: number) => ({ slug, label: `Label ${slug}`, section: "life" as const, parent: "ai", description: `About ${slug}`, count });
const labels = { heading: "By need", seeAll: "See all", cards: { intel: "i", howto: "h", life: "l" } };

beforeEach(() => {
  mocks.list.mockReset().mockImplementation(async (_locale: string, query: { topic: string }) => ({
    available: true, next_cursor: null, articles: query.topic === "ai-work" ? [] : [article(`${query.topic}-1`)],
  }));
});

describe("the AI hub rails", () => {
  it("reads one rail per sub-topic with something published, plus the news, and skips the rest", async () => {
    const { rails, news } = await loadAiHubRails("en", [
      topic("ai-plans", 3), topic("ai-chat", 0), topic("ai-work", 2), topic("ai-news", 4), topic("ai-terms", 9),
    ]);
    // ai-chat has nothing in this language, ai-work's read came back empty, ai-terms is no rail.
    expect(rails.map((rail) => rail.topic.slug)).toEqual(["ai-plans"]);
    expect(news?.topic.slug).toBe("ai-news");
    expect(mocks.list).toHaveBeenCalledWith("en", { kind: "life", topic: "ai-news", sort: "news" }, 6);
    expect(mocks.list).not.toHaveBeenCalledWith("en", expect.objectContaining({ topic: "ai-chat" }), expect.anything());
  });

  it("links each rail to its sub-topic's hub and jumps to it from the row of needs", async () => {
    const { rails, news } = await loadAiHubRails("en", [topic("ai-plans", 3), topic("ai-news", 4)]);
    render(<AiHubRails rails={rails} news={news} labels={labels} />);
    const plans = screen.getByRole("region", { name: "Label ai-plans" });
    expect(within(plans).getByRole("link", { name: "See all" }).getAttribute("href")).toBe("/life/topics/ai-plans");
    expect(within(plans).getByText("About ai-plans")).toBeTruthy();
    expect(screen.getByRole("navigation", { name: "By need" }).querySelectorAll("a")).toHaveLength(2);
  });

  it("renders nothing when no rail has anything", () => {
    const { container } = render(<AiHubRails rails={[]} news={null} labels={labels} />);
    expect(container.innerHTML).toBe("");
  });
});
