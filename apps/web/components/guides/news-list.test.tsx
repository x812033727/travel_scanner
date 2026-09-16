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

  it("shows the news day, never the publication time, and no description or position", () => {
    // Imported in one batch: both stories published in the same minute.
    render(<NewsList articles={[story("a", "甲", "2026-07-01", "2026-09-16T05:00:00Z")]} />);
    const list = screen.getByTestId("news-list");
    expect(list.textContent).toContain("2026-07-01");
    expect(list.textContent).not.toContain("2026-09-16");
    expect(list.textContent).not.toContain("甲的描述");
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
});
