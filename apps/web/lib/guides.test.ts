import { describe, expect, it } from "vitest";
import { guideHref, guideListHref, guideSection, isExpired, isGuideKind, isGuideSummary, isPublishedGuide, isTravelGuideKind } from "./guides";

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
});
