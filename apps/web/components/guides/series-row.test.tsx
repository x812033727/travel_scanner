import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { SeriesRow } from "./series-row";

const labels = { heading: "系列與教學中心", lead: "照順序讀的系列。", entries: "{count} 篇" };
const rows = [
  {
    slug: "claude-code", section: "life" as const, source: "api-series" as const, topic: "claude-code", entries: 96,
    hub: { kind: "life" as const, slug: "claude-code-tutorials", title: "Claude Code 教學中心", description: "從安裝到進階" },
  },
  {
    slug: "gemini", section: "life" as const, source: "web-gemini" as const, topic: "ai-chat", entries: null,
    hub: { kind: "life" as const, slug: "gemini-guide", title: "Gemini 完整教學" }, note: "50 篇完整教學，含手機與 CLI。",
  },
];

describe("the series row", () => {
  it("links each hub once, under its description or the page's note, with the lesson count when known", () => {
    render(<SeriesRow series={rows} labels={labels} />);
    expect(screen.getByRole("heading", { level: 2 }).textContent).toBe("系列與教學中心");
    expect(screen.getByRole("link", { name: "Claude Code 教學中心" }).getAttribute("href")).toBe("/life/claude-code-tutorials");
    expect(screen.getByText("從安裝到進階")).toBeTruthy();
    expect(screen.getByText("96 篇")).toBeTruthy();
    expect(screen.getByText("50 篇完整教學，含手機與 CLI。")).toBeTruthy();
    // Exactly one link to a hub: the Gemini e2e counts them on the section page.
    expect(screen.getAllByRole("link").filter((link) => link.getAttribute("href") === "/life/gemini-guide")).toHaveLength(1);
  });

  it("renders nothing without a series", () => {
    const { container } = render(<SeriesRow series={[]} labels={labels} />);
    expect(container.innerHTML).toBe("");
  });
});
