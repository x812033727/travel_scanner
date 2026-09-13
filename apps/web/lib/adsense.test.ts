import { describe, expect, it } from "vitest";
import {
  adsenseSplit, isAdsenseArticlePath, isAdsenseOrigin, isAdsensePublisherId, isAdsenseSlotId,
  MIN_BLOCKS_AFTER, validAdsenseConfig,
} from "./adsense";

const PUBLISHER = "ca-pub-4140966684432854";
const SLOT = "1234567890";

const heading = { type: "heading", level: 2 as const };
const paragraph = { type: "paragraph" };
const body = (count: number) => Array.from({ length: count }, () => ({ type: "paragraph" }));

describe("which pages may carry an ad", () => {
  it.each([
    "/zh-TW/guides/intel/tokyo-esim",
    "/en/guides/howto/tokyo-esim",
    "/ja/life/ai-notes",
    "/zh-CN/life/ai-notes/",
    "/ko/guides/intel/tokyo-esim?utm_source=x",
  ])("accepts the article route %s", (path) => {
    expect(isAdsenseArticlePath(path)).toBe(true);
  });

  it.each([
    // Hubs and listings are the "no content" screens outside zh-TW that the policies forbid.
    ["/zh-TW/guides", "hub"],
    ["/zh-TW/guides/intel", "listing"],
    ["/zh-TW/life", "life hub"],
    // The URL is the secret. A script in this document could read the token out of it.
    ["/zh-TW/share/9f8e7d6c5b4a", "shared trip"],
    ["/zh-TW/community/posts/1", "community"],
    ["/zh-TW/trips", "private"],
    ["/zh-TW/account", "private"],
    ["/zh-TW/admin/settings", "admin"],
    ["/zh-TW", "home"],
    // `life` is not a travel guide kind: that URL 404s, so it must not be treated as an article.
    ["/zh-TW/guides/life/ai-notes", "wrong kind"],
    ["/xx/life/ai-notes", "unknown locale"],
    ["/life/ai-notes", "no locale"],
    ["/zh-TW/guides/intel/a/b", "deeper than an article"],
  ])("refuses %s (%s)", (path) => {
    expect(isAdsenseArticlePath(path)).toBe(false);
  });
});

describe("identifiers", () => {
  it("accepts only Google's shapes", () => {
    expect(isAdsensePublisherId(PUBLISHER)).toBe(true);
    expect(isAdsenseSlotId(SLOT)).toBe(true);
    for (const bad of ["", "pub-4140966684432854", `${PUBLISHER}0`, PUBLISHER.toUpperCase(), null]) {
      expect(isAdsensePublisherId(bad)).toBe(false);
    }
    for (const bad of ["", "123456789", "12345678901", "12345678ab", undefined]) {
      expect(isAdsenseSlotId(bad)).toBe(false);
    }
  });

  it("refuses an enabled payload whose identifiers would not render", () => {
    const on = { enabled: true, publisher_id: PUBLISHER, slot_id: SLOT, cmp_enabled: false };
    expect(validAdsenseConfig(on)).toBe(true);
    expect(validAdsenseConfig({ ...on, cmp_enabled: true })).toBe(true);
    expect(validAdsenseConfig({ enabled: false, publisher_id: null, slot_id: null, cmp_enabled: false })).toBe(true);
    expect(validAdsenseConfig({ ...on, slot_id: null })).toBe(false);
    expect(validAdsenseConfig({ ...on, publisher_id: null })).toBe(false);
    expect(validAdsenseConfig({ ...on, enabled: "yes" })).toBe(false);
    // A missing consent flag would read as `undefined` and quietly mean "no CMP"; refuse it
    // so a payload from an older API can never decide personalisation by omission.
    expect(validAdsenseConfig({ enabled: true, publisher_id: PUBLISHER, slot_id: SLOT })).toBe(false);
    expect(validAdsenseConfig(null)).toBe(false);
  });

  it("serves ads on the production origin only", () => {
    expect(isAdsenseOrigin("https://mokaair.com")).toBe(true);
    expect(isAdsenseOrigin("https://www.mokaair.com")).toBe(true);
    for (const bad of ["http://mokaair.com", "https://mokaair.com.evil.test", "https://localhost:3000", "nonsense"]) {
      expect(isAdsenseOrigin(bad)).toBe(false);
    }
  });
});

describe("where the slot goes", () => {
  it("cuts after the first level-2 heading and its first paragraph", () => {
    const blocks = [paragraph, heading, paragraph, ...body(MIN_BLOCKS_AFTER)];
    const split = adsenseSplit(blocks);
    expect(split).not.toBeNull();
    // Never above the hero, and never before the section it belongs to has said anything.
    expect(split?.before).toHaveLength(3);
    expect(split?.after).toHaveLength(MIN_BLOCKS_AFTER);
  });

  it("continues the heading numbering so the table of contents still points at them", () => {
    expect(adsenseSplit([heading, paragraph, ...body(MIN_BLOCKS_AFTER)])?.headingStart).toBe(1);
    expect(adsenseSplit([paragraph, heading, paragraph, ...body(MIN_BLOCKS_AFTER)])?.headingStart).toBe(1);
  });

  it("leaves a thin article alone rather than making it mostly advertisement", () => {
    expect(adsenseSplit([heading, paragraph, ...body(MIN_BLOCKS_AFTER - 1)])).toBeNull();
    expect(adsenseSplit([heading, paragraph])).toBeNull();
    expect(adsenseSplit([])).toBeNull();
  });

  it("needs a level-2 heading followed by a paragraph", () => {
    expect(adsenseSplit(body(20))).toBeNull();
    expect(adsenseSplit([{ type: "heading", level: 3 }, paragraph, ...body(20)])).toBeNull();
    // A heading whose section is a list, not prose: no paragraph to cut after.
    expect(adsenseSplit([heading, { type: "list" }, { type: "list" }])).toBeNull();
  });

  it("skips a paragraph that precedes the first heading", () => {
    const split = adsenseSplit([paragraph, paragraph, heading, paragraph, ...body(MIN_BLOCKS_AFTER)]);
    expect(split?.before.map((block) => block.type)).toEqual(["paragraph", "paragraph", "heading", "paragraph"]);
  });
});
