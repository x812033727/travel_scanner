import { render, screen, within } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { NewsDesk } from "./news-desk";
import type { GuideSummary } from "@/lib/guides";

const article: GuideSummary = {
  kind: "life", slug: "story", title: "Story", description: "A useful explanation", topics: [],
  destination_id: null, destination_label: null, published_at: "2026-09-16T00:00:00Z", valid_until: null,
  news_date: "2026-09-14", featured: false,
};

describe("NewsDesk", () => {
  it("links to the supplied topic hubs and marks the current topic", () => {
    render(<NewsDesk articles={[article]} topics={[{ slug: "ai-news", label: "AI news", description: "AI developments" }]}
      topicsLabel="Browse topics" active="ai-news" />);
    const topics = screen.getByRole("navigation", { name: "Browse topics" });
    const link = within(topics).getByRole("link", { name: /AI news/ });
    expect(link.getAttribute("href")).toBe("/life/topics/ai-news");
    expect(link.getAttribute("aria-current")).toBe("page");
    expect(screen.getByTestId("news-lead").querySelector("img")).toBeNull();
    expect(screen.getByRole("link", { name: "Story" }).getAttribute("href")).toBe("/life/story");
  });

  it("keeps continuation pages as regular rows and omits an empty sidebar", () => {
    render(<NewsDesk articles={[article]} topics={[]} topicsLabel="Browse topics" lead={false} />);
    expect(screen.queryByTestId("news-lead")).toBeNull();
    expect(screen.queryByRole("complementary")).toBeNull();
    expect(screen.getByText(article.description)).toBeTruthy();
  });

  it("does not render a news desk for an empty result", () => {
    const { container } = render(<NewsDesk articles={[]} topics={[]} topicsLabel="Browse topics" />);
    expect(container.innerHTML).toBe("");
  });
});
