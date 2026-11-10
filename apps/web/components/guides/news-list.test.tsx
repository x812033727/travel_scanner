import { render, screen, within } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import type { GuideSummary } from "@/lib/guides";
import { NewsList } from "./news-list";

const story = (slug: string, title: string, news_date: string | null, published_at = "2026-09-16T05:00:00Z"): GuideSummary => ({
  slug, kind: "life", destination_id: null, destination_label: null, topics: [],
  title, description: `${title}的描述`, published_at, valid_until: null, news_date, featured: false,
});

describe("the news list", () => {
  it("draws one line per story: the day the news happened, then the title as a link, in the order given", () => {
    render(
      <NewsList
        articles={[
          story("ai-news-siri-20260914", "Siri AI 隨 iOS 27 推出", "2026-09-14"),
          story("ai-news-pace-20260912", "Amodei 呼籲放慢前沿 AI", "2026-09-12"),
        ]}
      />,
    );
    const rows = within(screen.getByTestId("news-list")).getAllByRole("listitem");
    expect(rows).toHaveLength(2);
    expect(rows.map((row) => row.querySelector("time")?.getAttribute("dateTime"))).toEqual(["2026-09-14", "2026-09-12"]);
    expect(rows[0].querySelector("time")?.textContent).toBe("2026-09-14");
    expect(within(rows[0]).getByRole("link", { name: "Siri AI 隨 iOS 27 推出" }).getAttribute("href")).toBe("/life/ai-news-siri-20260914");
  });

  it("shows the news day and description, never the publication time or a ranking", () => {
    // Imported in one batch: both stories published in the same minute.
    render(<NewsList articles={[story("a", "甲", "2026-07-01", "2026-09-16T05:00:00Z")]} />);
    const list = screen.getByTestId("news-list");
    expect(list.textContent).toContain("2026-07-01");
    expect(list.textContent).not.toContain("2026-09-16");
    expect(list.textContent).toContain("甲的描述");
    expect(list.tagName).toBe("OL");
  });

  it("keeps an undated piece on its own line without a date", () => {
    render(<NewsList articles={[story("a", "甲", "2026-09-14"), story("sources", "資訊來源", null)]} />);
    const rows = within(screen.getByTestId("news-list")).getAllByRole("listitem");
    expect(rows[1].querySelector("time")).toBeNull();
    expect(within(rows[1]).getByRole("link", { name: "資訊來源" })).toBeTruthy();
  });

  it("draws nothing without a story", () => {
    const { container } = render(<NewsList articles={[]} />);
    expect(container.innerHTML).toBe("");
  });

  it("allows a continuation list to preserve its native position without a lead", () => {
    render(<NewsList articles={[story("seventh", "Seventh story", "2026-09-14")]} start={7} />);
    expect(screen.getByTestId("news-list").getAttribute("start")).toBe("7");
    expect(screen.queryByTestId("news-lead")).toBeNull();
  });

  it("promotes only the first story without repeating it or changing the chronology", () => {
    const first = { ...story("first", "First story", "2026-09-14"), hero: { src: "/guides/first/hero.webp", alt: "Cover", width: 1600, height: 900, credit: null } };
    render(<NewsList articles={[first, story("next", "Next story", "2026-09-12")]} lead />);
    expect(screen.getAllByTestId("news-lead")).toHaveLength(1);
    expect(screen.getAllByRole("link", { name: "First story" })).toHaveLength(1);
    const cover = screen.getByTestId("news-lead").querySelector("img");
    expect(cover?.getAttribute("loading")).toBe("eager");
    expect(cover?.getAttribute("alt")).toBe("");
    expect(within(screen.getByTestId("news-list")).getAllByRole("listitem").map(row => row.querySelector("time")?.dateTime))
      .toEqual(["2026-09-14", "2026-09-12"]);
  });
});
