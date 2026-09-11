import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { ContentBlocks } from "@/components/content-blocks";
import { contentBlockLink, isContentBlockList, type ContentBlock } from "@/lib/content-blocks";
import { sitePageLink } from "@/lib/site-pages";

/**
 * This renderer and its sanitizer are shared by managed site documents and travel guides.
 * The point of sharing them is that a rule tightened for one surface cannot miss the other,
 * so these cases guard the sanitizer rather than any one page.
 */

describe("the link sanitizer", () => {
  it.each([
    ["javascript:alert(1)", "a script URL"],
    ["data:text/html,<script>alert(1)</script>", "an inline document"],
    ["vbscript:msgbox(1)", "another script scheme"],
    ["https://user:pass@example.test/", "embedded credentials"],
    ["https://exa mple.test/", "whitespace"],
    ["  ", "nothing but spaces"],
    ["not-a-url", "a bare word"],
    ["mailto:not-an-address", "a malformed mailto"],
    ["mailto:someone@example.test?subject=hi", "a mailto carrying a query"],
  ])("refuses %s (%s)", (url) => {
    expect(contentBlockLink(url)).toBeNull();
  });

  it.each([
    "https://example.test/guide",
    "http://example.test/guide",
    "mailto:someone@example.test",
  ])("allows %s", (url) => {
    expect(contentBlockLink(url)).not.toBeNull();
  });

  it("is the same function the managed documents use, not a second copy", () => {
    expect(sitePageLink).toBe(contentBlockLink);
  });
});

describe("the block guard", () => {
  it("accepts the four block types the API can send", () => {
    const blocks = [
      { type: "heading", level: 2, text: "標題" },
      { type: "paragraph", text: "內文" },
      { type: "list", items: ["一", "二"], ordered: true },
      { type: "link", text: "來源", url: "https://example.test/" },
    ];
    expect(isContentBlockList(blocks)).toBe(true);
  });

  it.each([
    ["an unknown type", [{ type: "image", text: "x" }]],
    ["a heading at a level the renderer has no element for", [{ type: "heading", level: 1, text: "x" }]],
    ["a list whose items are not text", [{ type: "list", items: [1], ordered: false }]],
    ["a link the sanitizer refuses", [{ type: "link", text: "x", url: "javascript:alert(1)" }]],
    ["raw HTML instead of blocks", "<p>hello</p>"],
  ])("rejects %s", (_label, blocks) => {
    expect(isContentBlockList(blocks)).toBe(false);
  });
});

describe("rendering", () => {
  const blocks: ContentBlock[] = [
    { type: "heading", level: 2, text: "三種選擇" },
    { type: "heading", level: 3, text: "最快的一種" },
    { type: "paragraph", text: "Skyliner 約 41 分鐘。" },
    { type: "list", items: ["Skyliner", "巴士"], ordered: false },
    { type: "link", text: "時刻表", url: "https://example.test/timetable" },
  ];

  it("draws each block with the element its level asks for", () => {
    render(<ContentBlocks blocks={blocks} />);
    expect(screen.getByRole("heading", { level: 2 }).textContent).toBe("三種選擇");
    expect(screen.getByRole("heading", { level: 3 }).textContent).toBe("最快的一種");
    expect(screen.getAllByRole("listitem")).toHaveLength(2);
  });

  it("opens an external link safely", () => {
    render(<ContentBlocks blocks={blocks} />);
    const link = screen.getByRole("link", { name: "時刻表" });
    expect(link.getAttribute("target")).toBe("_blank");
    expect(link.getAttribute("rel")).toBe("noopener noreferrer");
  });

  it("drops a link the sanitizer refuses rather than rendering a dead anchor", () => {
    render(<ContentBlocks blocks={[{ type: "link", text: "壞連結", url: "javascript:alert(1)" }]} />);
    expect(screen.queryByRole("link")).toBeNull();
    expect(screen.queryByText("壞連結")).toBeNull();
  });
});
