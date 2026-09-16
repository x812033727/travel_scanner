import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { TopicTiles } from "./topic-tiles";

const topics = [
  { slug: "ai", label: "AI 工具", section: "life" as const, parent: null, description: "AI 的一切。", count: 5 },
  { slug: "ai-terms", label: "AI 名詞解釋", section: "life" as const, parent: "ai", count: 2 },
  { slug: "ai-news", label: "AI 新聞", section: "life" as const, parent: "ai", count: 0 },
  { slug: "ai-search", label: "AI 搜尋", section: "life" as const, parent: "ai", count: 1 },
  { slug: "ai-chat", label: "對話助理", section: "life" as const, parent: "ai", count: 3 },
  { slug: "ai-coding", label: "AI 寫程式", section: "life" as const, parent: "ai", count: 4 },
  { slug: "website", label: "架站", section: "life" as const, parent: null, count: 0 },
  { slug: "daily", label: "日常", section: "life" as const, parent: null },
];
const labels = { heading: "依主題瀏覽", articles: "{count} 篇", more: "還有 {count} 個子主題" };

describe("topic tiles", () => {
  it("draws a tile per top-level topic with something under it, linking to its hub with its count and lead", () => {
    render(<TopicTiles section="life" topics={topics} labels={labels} />);
    expect(screen.getByRole("heading", { level: 2 }).textContent).toBe("依主題瀏覽");
    expect(screen.getByRole("link", { name: "AI 工具" }).getAttribute("href")).toBe("/life/topics/ai");
    expect(screen.getByText("5 篇")).toBeTruthy();
    expect(screen.getByText("AI 的一切。")).toBeTruthy();
    // Nothing under it in this language: no tile. No count sent (an older API): kept.
    expect(screen.queryByRole("link", { name: "架站" })).toBeNull();
    expect(screen.getByRole("link", { name: "日常" }).getAttribute("href")).toBe("/life/topics/daily");
  });

  it("shows the first three sub-topics with something under them and counts the rest", () => {
    render(<TopicTiles section="life" topics={topics} labels={labels} />);
    const chips = screen.getAllByRole("link").filter((link) => link.className.includes("app-filter-chip"));
    expect(chips.map((chip) => chip.textContent)).toEqual(["AI 名詞解釋", "AI 搜尋", "對話助理"]);
    expect(chips[0].getAttribute("href")).toBe("/life/topics/ai-terms");
    expect(screen.getByText("還有 1 個子主題")).toBeTruthy();
  });

  it("marks the reader's own topic, keeps its family tile active, and keeps an empty topic the reader is on", () => {
    const { container } = render(<TopicTiles section="life" topics={topics} active="ai-terms" labels={labels} />);
    expect(screen.getByRole("link", { name: "AI 名詞解釋" }).getAttribute("aria-current")).toBe("page");
    expect(screen.getByRole("link", { name: "AI 工具" }).getAttribute("aria-current")).toBeNull();
    expect(container.querySelector("li.border-\\[var\\(--teal\\)\\]")?.textContent).toContain("AI 工具");
    render(<TopicTiles section="life" topics={topics} active="website" labels={labels} />);
    expect(screen.getByRole("link", { name: "架站" }).getAttribute("aria-current")).toBe("page");
  });

  it("renders nothing when no top-level topic has anything under it", () => {
    const { container } = render(<TopicTiles section="travel" topics={[{ slug: "beach", label: "海灘", parent: null, count: 0 }]} labels={labels} />);
    expect(container.innerHTML).toBe("");
  });
});
