import { render, screen, within } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import type { GuideSummary } from "@/lib/guides";
import { LifeKnowledge, LifeNewsPreview, LifeReadingJumps } from "./life-discovery";

const article = (n: number): GuideSummary => ({
  slug: `story-${n}`, kind: "life", title: `Story ${n}`, description: "Description",
  destination_id: null, destination_label: null, topics: [], published_at: "2026-11-10T00:00:00Z",
  news_date: "2026-11-10", valid_until: null, featured: false,
});

describe("first-page life discovery", () => {
  it("keeps six stories outside native details and the remaining fourteen in order starting at seven", () => {
    const { container } = render(<LifeNewsPreview articles={Array.from({ length: 20 }, (_, i) => article(i + 1))}
      topics={[]} topicsLabel="Topics" locale="en" />);
    const lists = container.querySelectorAll('ol[data-testid="news-list"]');
    expect(lists).toHaveLength(2);
    expect(lists[0].children).toHaveLength(6);
    expect(lists[0].getAttribute("start")).toBe("1");
    expect(lists[1].children).toHaveLength(14);
    expect(lists[1].getAttribute("start")).toBe("7");
    const details = screen.getByTestId("life-more-news");
    expect(details.tagName).toBe("DETAILS");
    expect(details.hasAttribute("open")).toBe(false);
    expect(details.firstElementChild?.tagName).toBe("SUMMARY");
    expect(details.firstElementChild?.textContent).toBe("Read the remaining 14 stories");
    expect([...lists[1].querySelectorAll("a")].map(link => link.textContent?.includes("Story 7"))).toContain(true);
    expect([...container.querySelectorAll('ol[data-testid="news-list"] a')].map(link => link.getAttribute("href")))
      .toEqual(Array.from({ length: 20 }, (_, i) => `/life/story-${i + 1}`));
    expect(screen.getAllByTestId("news-lead")).toHaveLength(1);
    expect(details.querySelector('[data-testid="news-lead"]')).toBeNull();
  });

  it("has no extra disclosure for six or fewer stories", () => {
    render(<LifeNewsPreview articles={[article(1)]} topics={[]} topicsLabel="Topics" locale="zh-TW" />);
    expect(screen.queryByTestId("life-more-news")).toBeNull();
  });

  it("links only to existing sections and has no empty navigation", () => {
    const { rerender } = render(<LifeReadingJumps locale="zh-TW" news={false} knowledge />);
    expect(screen.queryByRole("link", { name: "看最新新聞" })).toBeNull();
    expect(screen.getByRole("link", { name: "學點實用新知" }).getAttribute("href")).toBe("#life-knowledge");
    rerender(<LifeReadingJumps locale="zh-TW" news={false} knowledge={false} />);
    expect(screen.queryByRole("navigation")).toBeNull();
  });

  it("uses an actual topic label on knowledge cards and keeps their canonical article URL", () => {
    const useful = { ...article(1), news_date: null, topics: [{ slug: "ai", label: "AI" }, { slug: "ai-chat", label: "AI conversations", parent: "ai" }] };
    render(<LifeKnowledge articles={[useful]} labels={{ intel: "Intel", howto: "Guide", life: "Lifestyle" }} locale="en" />);
    const rail = screen.getByTestId("life-knowledge");
    expect(rail.id).toBe("life-knowledge");
    expect(within(rail).getByText("AI conversations")).toBeTruthy();
    expect(within(rail).queryByText("Lifestyle")).toBeNull();
    expect(within(rail).getByRole("link", { name: "Story 1" }).getAttribute("href")).toBe("/life/story-1");
  });
});
