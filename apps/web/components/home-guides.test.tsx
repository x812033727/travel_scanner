import { render, screen, within } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import type { GuideSummary } from "@/lib/guides";
import { HomeGuides, type HomeGuideBlock } from "./home-guides";

const article = (slug: string, kind: GuideSummary["kind"], title: string): GuideSummary => ({
  slug, kind, destination_id: null, destination_label: null, topics: [],
  title, description: `${title}的描述`, published_at: "2026-09-16T05:00:00Z", valid_until: null, news_date: null, featured: false,
});

const blocks = (travel: GuideSummary[], tech: GuideSummary[], money: GuideSummary[]): HomeGuideBlock[] => [
  { key: "travel", href: "/guides", articles: travel },
  { key: "tech", href: "/life/topics/ai", articles: tech },
  { key: "money", href: "/life/topics/finance", articles: money },
];

describe("the home page's guide sections", () => {
  it("says what the site is, then one block per section with its articles and a link to its hub", () => {
    render(<HomeGuides blocks={blocks(
      [article("tokyo-first-trip", "howto", "東京第一次自由行")],
      [article("claude-code-intro", "life", "Claude Code 入門")],
      [article("credit-card-basics", "life", "信用卡入門")],
    )} />);
    expect(screen.getByRole("heading", { level: 2, name: "旅行與生活的實用指南" })).toBeTruthy();
    expect(screen.getByText(/個人站長經營/)).toBeTruthy();

    const travel = screen.getByTestId("home-guides-travel");
    expect(within(travel).getByRole("heading", { name: "旅遊攻略" })).toBeTruthy();
    expect(within(travel).getByRole("link", { name: "看全部" }).getAttribute("href")).toBe("/guides");
    expect(within(travel).getByRole("link", { name: /東京第一次自由行/ }).getAttribute("href")).toBe("/guides/howto/tokyo-first-trip");

    expect(within(screen.getByTestId("home-guides-tech")).getByRole("link", { name: "看全部" }).getAttribute("href")).toBe("/life/topics/ai");
    expect(within(screen.getByTestId("home-guides-money")).getByRole("link", { name: /信用卡入門/ }).getAttribute("href")).toBe("/life/credit-card-basics");
  });

  it("leaves out a block with nothing to show and keeps the introduction", () => {
    render(<HomeGuides blocks={blocks([article("tokyo-first-trip", "howto", "東京第一次自由行")], [], [])} />);
    expect(screen.getByTestId("home-guides-travel")).toBeTruthy();
    expect(screen.queryByTestId("home-guides-tech")).toBeNull();
    expect(screen.queryByTestId("home-guides-money")).toBeNull();
    expect(screen.getByText(/個人站長經營/)).toBeTruthy();
  });
});
