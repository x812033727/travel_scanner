import { describe, expect, it } from "vitest";
import {
  guideHeadings, guideHref, guideListHref, guideSection, isExpired, isGuideKind, isGuidePartnerLink,
  isGuideSummary, isPublishedGuide, isTravelGuideKind, partnerClickPath, readingMinutes, splitGuideBlocks,
  type GuideBlock,
} from "./guides";

const summary = {
  slug: "narita-to-tokyo", kind: "howto", destination_id: "tokyo", destination_label: "東京",
  topics: [{ slug: "transport", label: "交通" }], title: "怎麼走", description: "三種選擇",
  published_at: "2026-09-01T00:00:00Z", valid_until: null, featured: false,
};

const document = {
  title: "怎麼走", description: "三種選擇", version: 2, published_at: "2026-09-01T00:00:00Z",
  blocks: [{ type: "paragraph", text: "Skyliner 最快。" }], sources: [],
};

describe("guide kinds", () => {
  it("accepts only the three kinds that exist as URLs", () => {
    expect(isGuideKind("intel")).toBe(true);
    expect(isGuideKind("howto")).toBe(true);
    expect(isGuideKind("life")).toBe(true);
    for (const value of ["guides", "article", "travel", "", null, undefined, 1]) {
      expect(isGuideKind(value)).toBe(false);
    }
  });

  it("keeps life out of the /guides route, which only serves the two travel kinds", () => {
    expect(isTravelGuideKind("intel")).toBe(true);
    expect(isTravelGuideKind("howto")).toBe(true);
    expect(isTravelGuideKind("life")).toBe(false);
    expect(guideSection("intel")).toBe("travel");
    expect(guideSection("howto")).toBe("travel");
    expect(guideSection("life")).toBe("life");
  });

  it("keeps the kind in the path so an article has exactly one URL", () => {
    expect(guideHref("intel", "jr-pass-sale")).toBe("/guides/intel/jr-pass-sale");
    expect(guideHref("howto", "narita-to-tokyo")).toBe("/guides/howto/narita-to-tokyo");
    expect(guideHref("life", "ai-notes")).toBe("/life/ai-notes");
  });

  it("builds every listing URL, with the topic filter encoded", () => {
    expect(guideListHref("howto")).toBe("/guides/howto");
    expect(guideListHref("intel", "deal")).toBe("/guides/intel?topic=deal");
    expect(guideListHref("life")).toBe("/life");
    expect(guideListHref("life", "ai")).toBe("/life?topic=ai");
    expect(guideListHref("life", null)).toBe("/life");
  });
});

describe("expiry", () => {
  const today = new Date("2026-09-11T08:00:00Z");

  it("treats an article with no validity date as current forever", () => {
    expect(isExpired(null, today)).toBe(false);
  });

  it("keeps a notice current through the whole of its last day", () => {
    expect(isExpired("2026-09-11", today)).toBe(false);
    expect(isExpired("2026-09-12", today)).toBe(false);
  });

  it("marks a notice expired once its last day has passed", () => {
    expect(isExpired("2026-09-10", today)).toBe(true);
  });

  it("does not call a garbled date expired", () => {
    expect(isExpired("not-a-date", today)).toBe(false);
  });
});

describe("response guards", () => {
  it("accepts a well-formed summary", () => {
    expect(isGuideSummary(summary)).toBe(true);
  });

  it.each([
    ["an unknown kind", { ...summary, kind: "recipe" }],
    ["a missing title", { ...summary, title: undefined }],
    ["topics that are not labelled", { ...summary, topics: [{ slug: "transport" }] }],
    ["a numeric published_at", { ...summary, published_at: 20260901 }],
  ])("rejects %s", (_label, row) => {
    expect(isGuideSummary(row)).toBe(false);
  });

  it("accepts a published document", () => {
    expect(isPublishedGuide(document)).toBe(true);
  });

  it("rejects a body whose blocks are not the structured union", () => {
    expect(isPublishedGuide({ ...document, blocks: [{ type: "script", text: "x" }] })).toBe(false);
    expect(isPublishedGuide({ ...document, blocks: "<p>hi</p>" })).toBe(false);
  });

  it("rejects a link block whose URL the sanitizer refuses", () => {
    const blocks = [{ type: "link", text: "來源", url: "javascript:alert(1)" }];
    expect(isPublishedGuide({ ...document, blocks })).toBe(false);
  });

  it("rejects sources that are not titled links", () => {
    expect(isPublishedGuide({ ...document, sources: [{ url: "https://example.test/" }] })).toBe(false);
  });

  const hero = {
    src: "/guides/narita-to-tokyo/hero.jpg", alt: "Skyliner", width: 1600, height: 900,
    credit: { author: "Mokaair", license: "© Mokaair", source_url: null },
  };

  it("accepts a hero that is absent, null or a self-hosted raster", () => {
    expect(isPublishedGuide(document)).toBe(true);
    expect(isPublishedGuide({ ...document, hero: null })).toBe(true);
    expect(isPublishedGuide({ ...document, hero })).toBe(true);
    expect(isGuideSummary({ ...summary, hero })).toBe(true);
    expect(isGuideSummary({ ...summary, hero: null })).toBe(true);
  });

  it("rejects a hero that is a vector or hosted elsewhere, which the share card could not use", () => {
    expect(isPublishedGuide({ ...document, hero: { ...hero, src: "/guides/narita-to-tokyo/hero.svg" } })).toBe(false);
    expect(isGuideSummary({ ...summary, hero: { ...hero, src: "https://example.test/hero.jpg" } })).toBe(false);
  });

  it("accepts the guide-only blocks, including the editor's partner buttons", () => {
    const blocks = [
      { type: "image", src: "/guides/narita-to-tokyo/map.svg", alt: "地圖", width: 1600, height: 900 },
      { type: "table", header: ["a"], rows: [["b"]] },
      { type: "callout", tone: "tip", text: "x" },
      { type: "offer", module: "transport", destination_id: null, heading: "" },
    ];
    expect(isPublishedGuide({ ...document, blocks })).toBe(true);
  });

  it("rejects a partner block for a module the catalog does not sell", () => {
    const blocks = [{ type: "offer", module: "insurance", destination_id: null }];
    expect(isPublishedGuide({ ...document, blocks })).toBe(false);
  });

  const partnerLink = {
    type: "partner_link", partner: "hostinger", url: "https://www.hostinger.com/tw?aff_id=1", label: "看方案", note: "",
  };

  it("accepts a partner link for any program code, leaving the registry to the API", () => {
    // A program since removed from the registry must leave the article readable; the link
    // itself then finds no resolved entry and draws nothing.
    expect(isPublishedGuide({ ...document, blocks: [partnerLink] })).toBe(true);
    expect(isPublishedGuide({ ...document, blocks: [{ ...partnerLink, partner: "retired_program", note: undefined }] })).toBe(true);
  });

  it.each([
    ["plain http", { url: "http://www.hostinger.com/tw" }],
    ["a script URL", { url: "javascript:alert(1)" }],
    ["a missing label", { label: undefined }],
    ["a missing partner", { partner: undefined }],
  ])("rejects a partner link with %s", (_label, patch) => {
    expect(isPublishedGuide({ ...document, blocks: [{ ...partnerLink, ...patch }] })).toBe(false);
  });

  it("accepts only resolved partner links with a key the click endpoint understands", () => {
    const resolved = { key: "0123456789abcdef", partner: "hostinger", display_name: "Hostinger", url: partnerLink.url };
    expect(isGuidePartnerLink(resolved)).toBe(true);
    expect(isGuidePartnerLink({ ...resolved, key: "../../admin" })).toBe(false);
    expect(isGuidePartnerLink({ ...resolved, url: "http://www.hostinger.com/tw" })).toBe(false);
    expect(isGuidePartnerLink({ ...resolved, display_name: null })).toBe(false);
  });

  it("counts a partner click through the BFF, with the slug and locale encoded", () => {
    expect(partnerClickPath("life", "claude-code-vps", "zh-TW", "0123456789abcdef"))
      .toBe("/api/travel/guides/life/claude-code-vps/partner-links/0123456789abcdef/click?locale=zh-TW");
  });

  it("tolerates a document from an API that predates modified_at", () => {
    expect(isPublishedGuide({ ...document, modified_at: null })).toBe(true);
    expect(isPublishedGuide({ ...document, modified_at: "2026-09-12T00:00:00Z" })).toBe(true);
    expect(isPublishedGuide({ ...document, modified_at: 20260912 })).toBe(false);
  });
});

describe("reading the body", () => {
  const blocks: GuideBlock[] = [
    { type: "heading", level: 2, text: "怎麼買票" },
    { type: "paragraph", text: "先決定住哪一區。" },
    { type: "offer", module: "transport", destination_id: null, heading: "先買車票" },
    { type: "heading", level: 2, text: "怎麼搭" },
    { type: "heading", level: 3, text: "從第二航廈" },
    { type: "paragraph", text: "跟著指標走。" },
    { type: "offer", module: "activities", destination_id: "osaka-kyoto", heading: "" },
    { type: "paragraph", text: "結語。" },
  ];

  it("cuts the body at every partner block and numbers headings across the cuts", () => {
    const segments = splitGuideBlocks(blocks);
    expect(segments).toHaveLength(3);
    expect(segments[0].blocks.map((block) => block.type)).toEqual(["heading", "paragraph"]);
    expect(segments[0].headingStart).toBe(0);
    expect(segments[0].offer?.module).toBe("transport");
    expect(segments[1].blocks.map((block) => block.type)).toEqual(["heading", "heading", "paragraph"]);
    // One level-2 heading precedes this slice, so its own heading must become section-2.
    expect(segments[1].headingStart).toBe(1);
    expect(segments[1].offer?.destination_id).toBe("osaka-kyoto");
    expect(segments[2].blocks.map((block) => block.type)).toEqual(["paragraph"]);
    expect(segments[2].offer).toBeNull();
  });

  it("leaves a body without partner blocks as one slice", () => {
    const segments = splitGuideBlocks([{ type: "paragraph", text: "x" }]);
    expect(segments).toHaveLength(1);
    expect(segments[0].offer).toBeNull();
    expect(segments[0].partner).toBeNull();
  });

  it("cuts at a partner link too, and never leaves one for the shared renderer to draw", () => {
    const segments = splitGuideBlocks([
      { type: "heading", level: 2, text: "部署" },
      { type: "partner_link", partner: "hostinger", url: "https://www.hostinger.com/tw", label: "看方案" },
      { type: "offer", module: "hotel", destination_id: "tokyo", heading: "" },
      { type: "heading", level: 2, text: "收尾" },
    ]);
    expect(segments.map((segment) => [segment.offer?.type ?? null, segment.partner?.type ?? null])).toEqual([
      [null, "partner_link"], ["offer", null], [null, null],
    ]);
    expect(segments.flatMap((segment) => segment.blocks).some((block) => (block as { type: string }).type === "partner_link")).toBe(false);
    expect(segments[2].headingStart).toBe(1);
  });

  it("lists the level-2 headings with the ids the renderer gives them", () => {
    expect(guideHeadings(blocks)).toEqual([
      { id: "section-1", text: "怎麼買票" },
      { id: "section-2", text: "怎麼搭" },
    ]);
  });

  it("estimates reading time by character for CJK and by word for the rest, never below a minute", () => {
    const short = { title: "t", description: "d", blocks: [{ type: "paragraph" as const, text: "短" }], sources: [] };
    expect(readingMinutes(short)).toBe(1);
    const long = { ...short, blocks: [{ type: "paragraph" as const, text: "字".repeat(1000) }] };
    expect(readingMinutes(long)).toBe(3);
    const english = { ...short, blocks: [{ type: "paragraph" as const, text: Array(450).fill("word").join(" ") }] };
    expect(readingMinutes(english)).toBe(3);
  });
});
