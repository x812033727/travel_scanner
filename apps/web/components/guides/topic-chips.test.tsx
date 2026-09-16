import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { TopicChips } from "./topic-chips";

const labels = {
  allTopics: "全部主題", topicsLabel: "主題篩選", subtopics: "子主題", moreChips: "更多", fewerChips: "收起",
};
const topics = [
  { slug: "ai", label: "AI 工具", section: "life" as const, parent: null, count: 3 },
  { slug: "finance", label: "理財與金錢", section: "life" as const, parent: null, count: 0 },
  { slug: "website", label: "架站與電商", section: "life" as const, parent: null, count: 1 },
  { slug: "ai-terms", label: "AI 名詞解釋", section: "life" as const, parent: "ai", count: 2 },
  { slug: "ai-news", label: "AI 新聞與趨勢", section: "life" as const, parent: "ai", count: 0 },
  { slug: "wordpress", label: "WordPress", section: "life" as const, parent: "website", count: 1 },
];

describe("the two-level topic chips", () => {
  it("links each top-level topic to its hub and leaves out what this language has nothing under", () => {
    render(<TopicChips section="life" topics={topics} active={null} allHref="/life" labels={labels} />);
    expect(screen.getByRole("link", { name: /AI 工具/ }).getAttribute("href")).toBe("/life/topics/ai");
    // The count decides whether the chip draws at all; it is not printed on it.
    expect(screen.getByRole("link", { name: /AI 工具/ }).textContent).toBe("AI 工具");
    expect(screen.queryByRole("link", { name: /理財與金錢/ })).toBeNull();
    // No family is selected, so no sub-topic row.
    expect(screen.queryByText("子主題")).toBeNull();
    expect(screen.getByRole("link", { name: "全部主題" }).getAttribute("aria-current")).toBe("page");
  });

  it("opens the selected family's sub-topics and marks only the exact selection as current", () => {
    render(<TopicChips section="life" topics={topics} active="ai-terms" allHref="/life" labels={labels} />);
    const parent = screen.getByRole("link", { name: /AI 工具/ });
    expect(parent.getAttribute("aria-current")).toBeNull();
    expect(parent.className).toContain("app-filter-chip-active");
    const child = screen.getByRole("link", { name: /AI 名詞解釋/ });
    expect(child.getAttribute("aria-current")).toBe("page");
    expect(child.getAttribute("href")).toBe("/life/topics/ai-terms");
    expect(screen.getByText("子主題")).toBeTruthy();
    // Another family's children and an empty sibling stay out of the row.
    expect(screen.queryByRole("link", { name: /WordPress/ })).toBeNull();
    expect(screen.queryByRole("link", { name: /AI 新聞與趨勢/ })).toBeNull();
    expect(screen.getByRole("link", { name: "全部主題" }).getAttribute("aria-current")).toBeNull();
  });

  it("shows the family's sub-topics when the parent itself is selected", () => {
    render(<TopicChips section="life" topics={topics} active="ai" allHref="/life" labels={labels} />);
    expect(screen.getByRole("link", { name: /AI 工具/ }).getAttribute("aria-current")).toBe("page");
    expect(screen.getByRole("link", { name: /AI 名詞解釋/ }).getAttribute("aria-current")).toBeNull();
  });

  it("keeps the reader's own selection even when nothing is published under it", () => {
    render(<TopicChips section="life" topics={topics} active="finance" allHref="/life" labels={labels} />);
    expect(screen.getByRole("link", { name: /理財與金錢/ }).getAttribute("aria-current")).toBe("page");
  });

  it("keeps a topic whose count an older API did not send", () => {
    render(<TopicChips section="travel" topics={[{ slug: "transport", label: "交通" }]} active={null} allHref="/guides" labels={labels} />);
    expect(screen.getByRole("link", { name: "交通" }).getAttribute("href")).toBe("/guides/topics/transport");
  });

  it("renders nothing at all for an empty vocabulary", () => {
    const { container } = render(<TopicChips section="life" topics={[]} active={null} allHref="/life" labels={labels} />);
    expect(container.innerHTML).toBe("");
  });
});
