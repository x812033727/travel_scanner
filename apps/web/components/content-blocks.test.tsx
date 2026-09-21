import { cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { ContentBlocks } from "@/components/content-blocks";
import {
  contentBlockLink, contentImageSrc, isContentBlockList, isRichContentBlockList, licenseUrl,
  type ContentBlock, type RichContentBlock,
} from "@/lib/content-blocks";
import { siteUrl } from "@/lib/seo";
import { sitePageLink } from "@/lib/site-pages";

describe("tutorial content", () => {
  it("renders only publication-resolved internal references in the current locale", () => {
    render(<ContentBlocks locale="zh-TW" articleLinks={[{ kind: "life", slug: "visible", title: "Public title" }]} blocks={[
      { type: "rich_paragraph", inlines: [
        { type: "text", text: "See " },
        { type: "article", kind: "life", slug: "visible", text: "visible tutorial" },
        { type: "article", kind: "life", slug: "hidden", text: "hidden tutorial" },
        { type: "code", text: " <script> " },
      ] },
    ]} />);
    expect(screen.getByRole("link", { name: "visible tutorial" }).getAttribute("href")).toBe("/zh-TW/life/visible");
    expect(screen.queryByRole("link", { name: "hidden tutorial" })).toBeNull();
    expect(screen.getByText("hidden tutorial")).toBeTruthy();
    expect(document.querySelector("script")).toBeNull();
  });

  it("draws a summary as a card and a FAQ as disclosures, headed by the words it is given", () => {
    render(<ContentBlocks labels={{ imageCredit: "圖片：", tip: "小提醒", warning: "注意", info: "補充", summary: "重點摘要", faq: "常見問題" }} blocks={[
      { type: "summary", items: ["第一句。", "第二句。"] },
      { type: "faq", items: [{ question: "多久？", answer: "四十一分鐘。" }, { question: "多少錢？", answer: "兩千五。" }] },
    ]} />);
    const card = screen.getByRole("complementary", { name: "重點摘要" });
    expect(within(card).getAllByRole("listitem").map((item) => item.textContent)).toEqual(["第一句。", "第二句。"]);
    const faq = screen.getByRole("region", { name: "常見問題" });
    expect(faq.querySelectorAll("details")).toHaveLength(2);
    expect(within(faq).getByText("多久？").tagName).toBe("SUMMARY");
    expect(within(faq).getByText("四十一分鐘。")).toBeTruthy();
  });

  it("shows a definition card only for a target with a published description, and only when it has the words for it", () => {
    const blocks: RichContentBlock[] = [{ type: "rich_paragraph", inlines: [
      { type: "article", kind: "life", slug: "described", text: "a term" },
      { type: "article", kind: "life", slug: "bare", text: "a plain link" },
    ] }];
    const links = [
      { kind: "life" as const, slug: "described", title: "The term", description: "What it means." },
      { kind: "life" as const, slug: "bare", title: "Bare" },
    ];
    render(<ContentBlocks locale="en" articleLinks={links} blocks={blocks} termLabels={{ card: "名詞說明", readMore: "閱讀全文" }} />);
    const term = screen.getByRole("link", { name: "a term" });
    expect(term.getAttribute("href")).toBe("/en/life/described");
    expect(term.getAttribute("aria-expanded")).toBe("false");
    expect(screen.getByRole("link", { name: "a plain link" }).getAttribute("aria-expanded")).toBeNull();
    cleanup();
    // Without the labels (a caller that is not the article page) every target is a plain link.
    render(<ContentBlocks locale="en" articleLinks={links} blocks={blocks} />);
    expect(screen.getByRole("link", { name: "a term" }).getAttribute("aria-expanded")).toBeNull();
  });
  it("copies exact code including HTML, tabs, quotes and the final newline", async () => {
    const code = '<button>\n\tSave & "test"\n</button>\n';
    const writeText = vi.fn().mockResolvedValue(undefined);
    Object.defineProperty(navigator, "clipboard", { configurable: true, value: { writeText } });
    render(<ContentBlocks blocks={[{ type: "code", label: "index.html", language: "html", code }]} />);
    expect(screen.getByLabelText("index.html").textContent).toBe(code);
    expect(document.querySelector("pre button")).toBeNull();
    fireEvent.click(screen.getByRole("button", { name: "Copy" }));
    await waitFor(() => expect(writeText).toHaveBeenCalledWith(code));
    expect((await screen.findByRole("status")).textContent).toContain("Copied");
  });
  it("keeps a manual-copy path when clipboard access is unavailable", async () => {
    Object.defineProperty(navigator, "clipboard", { configurable: true, value: undefined });
    render(<ContentBlocks blocks={[{ type: "code", label: "CLI", language: "bash", code: "claude --help" }]} />);
    fireEvent.click(screen.getByRole("button", { name: "Copy" }));
    expect((await screen.findByRole("status")).textContent).toContain("Copy failed");
    expect(screen.getByLabelText("CLI").getAttribute("tabindex")).toBe("0");
  });
});

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

  it("never draws a block it does not know as a link, even one that carries a URL", () => {
    // A partner link that escaped the article's splitter, or a block from a newer API, used
    // to fall through to the link branch and reach the page as an ordinary, unqualified link.
    const stray = {
      type: "partner_link", partner: "hostinger", label: "看方案", text: "看方案",
      url: "https://www.hostinger.com/tw?aff_id=1",
    } as unknown as RichContentBlock;
    const { container } = render(<ContentBlocks blocks={[stray]} />);
    expect(container.querySelector("a")).toBeNull();
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

  it("accepts a summary of two to five sentences and a FAQ of two to ten answered questions", () => {
    const faq = (count: number) => ({ type: "faq", items: Array.from({ length: count }, (_, i) => ({ question: `Q${i}?`, answer: `A${i}.` })) });
    const summary = (count: number) => ({ type: "summary", items: Array.from({ length: count }, (_, i) => `S${i}.`) });
    expect(isRichContentBlockList([summary(2), summary(5), faq(2), faq(10)])).toBe(true);
    for (const block of [summary(1), summary(6), faq(1), faq(11), { type: "summary", items: ["ok", " "] },
      { type: "faq", items: [{ question: "Q?", answer: "" }, { question: "Q2?", answer: "A" }] }]) {
      expect(isRichContentBlockList([block]), JSON.stringify(block)).toBe(false);
    }
    // Still guide-only: the legal pages' guard refuses them.
    expect(isContentBlockList([summary(2)])).toBe(false);
  });

  it("accepts an image's long description as text and refuses anything else there", () => {
    expect(isRichContentBlockList([{ ...image, description: "一般室 52,200 韓元。" }])).toBe(true);
    expect(isRichContentBlockList([{ ...image, description: ["not", "text"] }])).toBe(false);
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

  it("draws a diagram wide enough to read, inside a box that scrolls and takes keyboard focus", () => {
    const { container } = render(<ContentBlocks labels={labels} blocks={[{
      type: "image", src: "/guides/narita-to-tokyo/route-map.svg", alt: "路線圖", width: 1600, height: 900,
    }]} />);
    const image = screen.getByRole("img", { name: "路線圖" });
    // 15px, the floor pack_ingest enforces, lands at 11.1 CSS px here; fitted to the 728px
    // column it would be 6.8, and 3.1 on a phone.
    expect(image.style.width).toBe("1180px");
    // Tailwind preflight caps an image at 100% of its box; without this the width is ignored.
    expect(image.style.maxWidth).toBe("none");
    const box = image.parentElement!;
    expect(box.className).toContain("overflow-x-auto");
    // The gutter is cancelled and re-applied inside, so the window into the diagram is the
    // whole phone width. A three-up decoder's column is 361px on screen and never fitted 335.
    expect(box.className).toContain("-mx-5");
    // Left only: that gutter lines the diagram up with the text at rest. A right one would
    // make the end of the scroll stop on blank instead of on the diagram's own edge.
    expect(box.className).toContain("pl-5");
    expect(box.className).not.toContain("px-5");
    expect(box.className).not.toContain("pr-");
    // From xl the box opens to the diagram's own width. The figure's column is 728px, not
    // main's 768: that 768 includes main's own px-5. So the margin is (1180 - 728) / 2.
    expect(box.className).toContain("xl:-mx-[226px]");
    expect(box.className).toContain("xl:pl-0");
    expect(box.getAttribute("tabindex")).toBe("0");
    // The alt belongs to the image; naming the box as well would read it out twice.
    expect(box.getAttribute("aria-label")).toBeNull();
    expect(container.querySelector("figure")).not.toBeNull();
  });

  it("keeps a photograph fitted to the column, with no scroller", () => {
    render(<ContentBlocks labels={labels} blocks={blocks} />);
    const photo = screen.getByRole("img", { name: "Skyliner 列車" });
    expect(photo.style.width).toBe("");
    expect(photo.className).toContain("w-full");
    expect(photo.parentElement!.tagName).toBe("FIGURE");
  });

  it("never draws a diagram larger than it was authored", () => {
    render(<ContentBlocks labels={labels} blocks={[{
      type: "image", src: "/guides/narita-to-tokyo/route-map.svg", alt: "小圖", width: 640, height: 360,
    }]} />);
    expect(screen.getByRole("img", { name: "小圖" }).style.width).toBe("640px");
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

  it("keeps every column readable in a wide table without inheriting arbitrary character breaks", () => {
    render(<ContentBlocks blocks={[{
      type: "table", header: ["方案", "價格", "休館日", "注意事項", "來源"],
      rows: [["交通方案", "3,000 韓元", "星期一", "請確認當日時間", "官方"]],
    }]} />);
    const table = screen.getByRole("table");
    expect(table.className).toContain("[overflow-wrap:normal]");
    expect(table.parentElement!.className).toContain("overflow-x-auto");
    for (const cell of [...screen.getAllByRole("columnheader"), ...screen.getAllByRole("cell")]) {
      expect(cell.className).toContain("min-w-28");
    }
  });

  it("numbers level-2 headings from the start it is given, so sliced bodies keep one sequence", () => {
    render(<ContentBlocks blocks={blocks} labels={labels} headingStart={2} />);
    const headings = screen.getAllByRole("heading", { level: 2 });
    expect(headings.map((heading) => heading.id)).toEqual(["section-3", "section-4"]);
  });

  it("numbers level-3 headings within their section, restarting under every level-2", () => {
    render(<ContentBlocks headingStart={0} blocks={[
      { type: "heading", level: 2, text: "一" },
      { type: "heading", level: 3, text: "一之一" },
      { type: "heading", level: 3, text: "一之二" },
      { type: "heading", level: 2, text: "二" },
      { type: "heading", level: 3, text: "二之一" },
    ]} />);
    expect(screen.getAllByRole("heading", { level: 2 }).map((h) => h.id)).toEqual(["section-1", "section-2"]);
    expect(screen.getAllByRole("heading", { level: 3 }).map((h) => h.id)).toEqual(["section-1-1", "section-1-2", "section-2-1"]);
    cleanup();
    render(<ContentBlocks blocks={[{ type: "heading", level: 2, text: "一" }, { type: "heading", level: 3, text: "一之一" }]} />);
    expect(screen.getByRole("heading", { level: 3 }).id).toBe("");
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

/**
 * A diagram's long description: its `<desc>`, lifted into the block. It has to reach the HTML
 * (the fares and times it states appear nowhere else in the article) without changing what a
 * reader sees first, and without ever inlining the SVG, whose path is vetted but whose
 * contents are not.
 */
describe("an image's long description", () => {
  const labels = { imageCredit: "圖片：", imageDescription: "閱讀完整文字說明", tip: "小提醒", warning: "注意", info: "補充" };
  const photo: RichContentBlock = {
    type: "image", src: "/guides/korea-ktx-srt-ticket-guide/diagram-1.svg", alt: "首爾／水西到釜山的 KTX 與 SRT 路線圖",
    width: 1600, height: 900, caption: "先看兩條線各從哪一站出發。",
    credit: { author: "Mokaair", license: "© Mokaair", source_url: null },
  };
  const diagram: RichContentBlock = {
    ...photo, description: "SRT 水西到釜山最快 2 小時 11 分，一天 44 班，一般室 52,200 韓元、特室 75,700 韓元。",
  };

  it("sits in the figure after the caption as a disclosure that is folded by default", () => {
    const { container } = render(<ContentBlocks blocks={[diagram]} labels={labels} />);
    const figure = container.querySelector("figure")!;
    const details = figure.querySelector("details")!;
    expect(details.open).toBe(false);
    expect(figure.querySelector("figcaption")!.nextElementSibling).toBe(details);
    expect(within(details).getByText("閱讀完整文字說明").tagName).toBe("SUMMARY");
    // Folded or not, the text is in the DOM: that is what a crawler reads.
    expect(within(details).getByText(/52,200 韓元/).tagName).toBe("P");
    expect(details.textContent).toContain("2 小時 11 分");
  });

  it("still references the SVG by its path and inlines none of its markup", () => {
    const { container } = render(<ContentBlocks blocks={[diagram]} labels={labels} />);
    expect(screen.getByRole("img", { name: photo.alt }).getAttribute("src")).toBe(photo.src);
    expect(container.querySelector("svg")).toBeNull();
    expect(container.innerHTML).not.toContain("<svg");
  });

  it("draws no disclosure for a picture without one, or with a blank one", () => {
    const { container } = render(<ContentBlocks blocks={[photo, { ...photo, description: "  " }]} labels={labels} />);
    expect(container.querySelectorAll("figure")).toHaveLength(2);
    expect(container.querySelector("details")).toBeNull();
  });

  it("names the disclosure after the picture when a caller passes no words for it", () => {
    render(<ContentBlocks blocks={[diagram]} />);
    expect(screen.getByText(photo.alt, { selector: "summary" })).toBeTruthy();
  });
});
