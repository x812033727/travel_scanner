import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { ListingEmpty, ListingToolbar } from "./listing-toolbar";

const topics = [
  { slug: "transport", label: "交通", section: "travel" as const, parent: null, count: 4 },
  { slug: "food", label: "美食", section: "travel" as const, parent: null, count: 2 },
];
const labels = {
  allTopics: "全部主題", topicsLabel: "主題篩選", subtopics: "子主題", moreChips: "還有 {count} 個", fewerChips: "收起",
  sortLabel: "排序", sortCurated: "精選優先", sortLatest: "最新優先",
};
const sort = { current: "curated" as const, hrefs: { curated: "/guides/howto", latest: "/guides/howto?sort=latest" } };

describe("the listing toolbar", () => {
  it("holds the topic chips, the order as links with the current one marked, and the count", () => {
    render(<ListingToolbar section="travel" topics={topics} active={null} allHref="/guides/howto" sort={sort} count="106 篇文章" labels={labels} />);
    expect(screen.getByRole("link", { name: /交通/ }).getAttribute("href")).toBe("/guides/topics/transport");
    const order = screen.getByRole("navigation", { name: "排序" });
    const curated = screen.getByRole("link", { name: "精選優先" });
    const latest = screen.getByRole("link", { name: "最新優先" });
    expect(order.contains(curated) && order.contains(latest)).toBe(true);
    expect(curated.getAttribute("aria-current")).toBe("page");
    expect(curated.getAttribute("href")).toBe("/guides/howto");
    expect(latest.getAttribute("aria-current")).toBeNull();
    expect(latest.getAttribute("href")).toBe("/guides/howto?sort=latest");
    expect(screen.getByText("106 篇文章")).toBeTruthy();
    expect(screen.getByTestId("listing-toolbar").className).toContain("app-listing-toolbar");
  });

  it("draws no order or count row on a listing with one order and no known count", () => {
    render(<ListingToolbar section="travel" topics={topics} active="food" allHref="/guides/intel" labels={labels} />);
    expect(screen.queryByRole("navigation", { name: "排序" })).toBeNull();
    expect(screen.getByRole("link", { name: /美食/ }).getAttribute("aria-current")).toBe("page");
  });
});

describe("the empty listing", () => {
  it("says so, points at the chips, and offers the section's search", () => {
    render(
      <ListingEmpty
        section="life" action="/zh-TW/search/articles"
        labels={{ empty: "這裡還沒有已發布的內容。", hint: "換個主題試試，或直接搜尋：", label: "搜尋關鍵字", placeholder: "輸入", submit: "搜尋" }}
      />,
    );
    expect(screen.getByText("這裡還沒有已發布的內容。")).toBeTruthy();
    expect(screen.getByText("換個主題試試，或直接搜尋：")).toBeTruthy();
    const form = screen.getByRole("search");
    expect(form.getAttribute("action")).toBe("/zh-TW/search/articles");
    expect(form.querySelector('input[name="section"]')?.getAttribute("value")).toBe("life");
  });
});
