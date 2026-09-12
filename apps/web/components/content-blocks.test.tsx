import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { ContentBlocks } from "@/components/content-blocks";
import {
  contentBlockLink, contentImageSrc, isContentBlockList, isRichContentBlockList, licenseUrl,
  type ContentBlock, type RichContentBlock,
} from "@/lib/content-blocks";
import { siteUrl } from "@/lib/seo";
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

  it("keeps a link back into this site in the same tab", () => {
    render(<ContentBlocks blocks={[{ type: "link", text: "東京城市頁", url: `${siteUrl}/zh-TW/destinations/tokyo` }]} />);
    const link = screen.getByRole("link", { name: "東京城市頁" });
    expect(link.getAttribute("target")).toBeNull();
    expect(link.getAttribute("rel")).toBeNull();
  });
});

/**
 * The guide-only blocks. They are a superset the renderer draws and the legal pages never
 * send, so the four-block guard above must keep refusing them while the rich guard accepts.
 */
describe("the image path rule", () => {
  it.each([
    "/guides/narita-to-tokyo/hero.jpg",
    "/guides/tokyo-passes/route-map.svg",
    "/guides/a1/b2.webp",
  ])("allows %s", (src) => {
    expect(contentImageSrc(src)).toBe(src);
  });

  it.each([
    ["https://upload.wikimedia.org/x.jpg", "another host"],
    ["/guides/x/../../etc/passwd.png", "a path that climbs out"],
    ["/brand/mokaair-og.svg", "a folder that is not the guides'"],
    ["/guides/x/Hero.JPG", "uppercase"],
    ["/guides/x/hero.gif", "a format the site does not serve"],
    ["/guides/hero.jpg", "no article folder"],
  ])("refuses %s (%s)", (src) => {
    expect(contentImageSrc(src)).toBeNull();
  });
});

describe("licence deeds", () => {
  it("links the Creative Commons family and nothing else", () => {
    expect(licenseUrl("CC BY-SA 4.0")).toBe("https://creativecommons.org/licenses/by-sa/4.0/");
    expect(licenseUrl("CC BY 2.0")).toBe("https://creativecommons.org/licenses/by/2.0/");
    expect(licenseUrl("CC0 1.0")).toBe("https://creativecommons.org/publicdomain/zero/1.0/");
    expect(licenseUrl("© Mokaair")).toBeNull();
    expect(licenseUrl("Public domain")).toBeNull();
  });
});

describe("the rich block guard", () => {
  const image = {
    type: "image", src: "/guides/narita-to-tokyo/route-map.svg", alt: "路線圖", width: 1600, height: 900,
    caption: "示意", credit: { author: "Mokaair", license: "© Mokaair", source_url: null },
  };
  const table = { type: "table", header: ["方式", "時間"], rows: [["Skyliner", "41 分"]], caption: "" };
  const callout = { type: "callout", tone: "warning", title: "注意", text: "末班車後只剩計程車。" };

  it("accepts the three guide-only blocks the shared guard still refuses", () => {
    expect(isRichContentBlockList([image, table, callout])).toBe(true);
    expect(isContentBlockList([image])).toBe(false);
    expect(isContentBlockList([table])).toBe(false);
    expect(isContentBlockList([callout])).toBe(false);
  });

  it("tolerates a caption, credit or title the API left out", () => {
    expect(isRichContentBlockList([
      { type: "image", src: image.src, alt: "x", width: 10, height: 10 },
      { type: "table", header: ["a"], rows: [["b"]] },
      { type: "callout", tone: "tip", text: "x" },
    ])).toBe(true);
  });

  it.each([
    ["an image hosted elsewhere", { ...image, src: "https://example.test/x.jpg" }],
    ["an image without a size", { ...image, width: undefined }],
    ["an image wider than the API allows", { ...image, width: 5000 }],
    ["a credit with a script URL", { ...image, credit: { ...image.credit, source_url: "javascript:alert(1)" } }],
    ["a ragged table", { ...table, rows: [["only one cell"]] }],
    ["a table without a header", { ...table, header: [] }],
    ["a callout with an unknown tone", { ...callout, tone: "danger" }],
  ])("rejects %s", (_label, block) => {
    expect(isRichContentBlockList([block])).toBe(false);
  });
});

describe("rendering the rich blocks", () => {
  const labels = { imageCredit: "圖片：", tip: "小提醒", warning: "注意", info: "補充" };
  const blocks: RichContentBlock[] = [
    { type: "heading", level: 2, text: "第一段" },
    {
      type: "image", src: "/guides/narita-to-tokyo/skyliner.webp", alt: "Skyliner 列車", width: 1200, height: 800,
      caption: "京成 Skyliner",
      credit: { author: "Someone", license: "CC BY-SA 4.0", source_url: "https://commons.wikimedia.org/wiki/File:Skyliner.jpg" },
    },
    { type: "table", header: ["方式", "時間"], rows: [["Skyliner", "41 分"], ["巴士", "85 分"]], caption: "2026 年 9 月查證" },
    { type: "callout", tone: "warning", title: "末班車", text: "23:30 之後只剩計程車。" },
    { type: "heading", level: 2, text: "第二段" },
  ];

  it("draws an image as a figure with its caption and a linked credit", () => {
    render(<ContentBlocks blocks={blocks} labels={labels} />);
    const image = screen.getByRole("img", { name: "Skyliner 列車" });
    expect(image.getAttribute("src")).toBe("/guides/narita-to-tokyo/skyliner.webp");
    expect(image.getAttribute("width")).toBe("1200");
    expect(image.getAttribute("loading")).toBe("lazy");
    expect(screen.getByText(/京成 Skyliner/).textContent).toContain("圖片：Someone (CC BY-SA 4.0)");
    expect(screen.getByRole("link", { name: "Someone" }).getAttribute("href")).toBe("https://commons.wikimedia.org/wiki/File:Skyliner.jpg");
    expect(screen.getByRole("link", { name: "CC BY-SA 4.0" }).getAttribute("href")).toBe("https://creativecommons.org/licenses/by-sa/4.0/");
  });

  it("draws a table with a header row, its cells and its caption, inside a box that scrolls", () => {
    const { container } = render(<ContentBlocks blocks={blocks} labels={labels} />);
    expect(screen.getAllByRole("columnheader").map((cell) => cell.textContent)).toEqual(["方式", "時間"]);
    expect(screen.getAllByRole("cell").map((cell) => cell.textContent)).toEqual(["Skyliner", "41 分", "巴士", "85 分"]);
    expect(screen.getByText("2026 年 9 月查證").tagName).toBe("CAPTION");
    expect(container.querySelector("table")!.parentElement!.className).toContain("overflow-x-auto");
  });

  it("draws a callout as a note headed by its tone and title", () => {
    render(<ContentBlocks blocks={blocks} labels={labels} />);
    const note = screen.getByRole("note");
    expect(note.textContent).toContain("注意 · 末班車");
    expect(note.textContent).toContain("23:30 之後只剩計程車。");
  });

  it("numbers level-2 headings from the start it is given, so sliced bodies keep one sequence", () => {
    render(<ContentBlocks blocks={blocks} labels={labels} headingStart={2} />);
    const headings = screen.getAllByRole("heading", { level: 2 });
    expect(headings.map((heading) => heading.id)).toEqual(["section-3", "section-4"]);
  });

  it("gives headings no id at all when no start is given, which is what the legal pages want", () => {
    render(<ContentBlocks blocks={blocks} />);
    for (const heading of screen.getAllByRole("heading", { level: 2 })) expect(heading.id).toBe("");
  });

  it("drops an image whose path fails the rule rather than fetching it", () => {
    render(<ContentBlocks blocks={[{ ...blocks[1], src: "https://example.test/x.jpg" } as RichContentBlock]} />);
    expect(screen.queryByRole("img")).toBeNull();
  });
});
