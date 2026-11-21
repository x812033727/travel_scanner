import { cleanup, render, screen, within } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";
import { Backlinks, RelatedGrid } from "./related-grid";

const kindLabels = { intel: "情報", howto: "攻略", life: "生活分享" };
const item = (slug: string, title: string, kind: "intel" | "howto" | "life" = "life", description: string | null = "描述") =>
  ({ kind, slug, title, description });

afterEach(cleanup);

describe("RelatedGrid", () => {
  it("draws at most four cards, in the API's order, each linked at its own URL", () => {
    render(
      <RelatedGrid
        heading="同主題延伸閱讀"
        items={[item("a", "甲"), item("b", "乙", "howto"), item("c", "丙", "intel", null), item("d", "丁"), item("e", "戊")]}
        kindLabels={kindLabels}
      />,
    );
    const section = screen.getByRole("region", { name: "同主題延伸閱讀" });
    expect(within(section).getAllByRole("listitem")).toHaveLength(4);
    expect(within(section).getByRole("link", { name: "乙" }).getAttribute("href")).toBe("/guides/howto/b");
    expect(within(section).getByText("攻略")).toBeTruthy();
    expect(within(section).queryByRole("link", { name: "戊" })).toBeNull();
    // A reference without a description draws none, rather than an empty line.
    expect(within(section).getAllByText("描述")).toHaveLength(3);
  });

  it("leaves out what the series navigation already lists, and nothing at all when empty", () => {
    render(<RelatedGrid heading="同主題延伸閱讀" items={[item("a", "甲"), item("b", "乙")]} kindLabels={kindLabels} exclude={["a"]} />);
    expect(screen.queryByRole("link", { name: "甲" })).toBeNull();
    expect(screen.getByRole("link", { name: "乙" })).toBeTruthy();
    cleanup();
    render(<RelatedGrid heading="同主題延伸閱讀" items={[item("a", "甲")]} kindLabels={kindLabels} exclude={["a"]} />);
    expect(screen.queryByRole("heading")).toBeNull();
  });

  it("shows the first remaining news recommendation with its description and keeps each row a single named link", () => {
    render(
      <RelatedGrid heading="同主題延伸閱讀" kindLabels={kindLabels} layout="news" exclude={["old"]} items={[
        item("old", "已列文章"), item("lead", "完整的新聞標題", "life", "第一篇的摘要"),
        item("guide", "延伸指南", "howto", "指南摘要"), item("follow", "後續報導", "life", null),
      ]} />,
    );
    const list = screen.getByRole("list");
    const rows = within(list).getAllByRole("listitem");
    expect(rows.map((row) => within(row).getByRole("heading", { level: 3 }).textContent)).toEqual([
      "完整的新聞標題", "延伸指南", "後續報導",
    ]);
    expect(rows.map((row) => within(row).getByRole("link").getAttribute("href"))).toEqual([
      "/life/lead", "/guides/howto/guide", "/life/follow",
    ]);
    const lead = within(rows[0]).getByRole("link", { name: "完整的新聞標題" });
    expect(within(lead).getByText("第一篇的摘要")).toBeTruthy();
    expect(within(rows[1]).getByText("攻略")).toBeTruthy();
    expect(within(list).queryByText("指南摘要")).toBeNull();
    expect(within(list).queryByText("生活分享")).toBeNull();
  });
});

describe("Backlinks", () => {
  it("lists the citing articles as plain links, and draws nothing when there are none", () => {
    render(<Backlinks heading="引用本文的文章" items={[item("a", "甲"), item("b", "乙", "intel")]} />);
    const section = screen.getByRole("region", { name: "引用本文的文章" });
    expect(within(section).getByRole("link", { name: "乙" }).getAttribute("href")).toBe("/guides/intel/b");
    cleanup();
    render(<Backlinks heading="引用本文的文章" items={[]} />);
    expect(screen.queryByRole("heading")).toBeNull();
  });
});
