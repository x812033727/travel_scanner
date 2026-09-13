import { describe, expect, it } from "vitest";
import {
  adsenseArticleRoute, adsenseRequestGate, adsenseSplit, isAdsenseArticlePath, isAdsenseOrigin,
  isAdsensePublisherId, isAdsenseSlotId, MIN_BLOCKS_AFTER, MIN_BLOCKS_BEFORE_WITHOUT_HERO,
  validAdsenseConfig,
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

  it("keeps more of the article above the slot when there is no hero", () => {
    // With a hero the cut is after the first heading and its paragraph. Without one there is
    // far less above that point, so the ad could be the first thing in the viewport.
    const blocks = [heading, paragraph, ...body(MIN_BLOCKS_AFTER + 2)];
    expect(adsenseSplit(blocks, { hasHero: true })?.before).toHaveLength(2);
    expect(adsenseSplit(blocks, { hasHero: false })?.before).toHaveLength(MIN_BLOCKS_BEFORE_WITHOUT_HERO);
    // A hero-less article too short to afford that clearance simply carries no ad.
    expect(adsenseSplit([heading, paragraph, ...body(MIN_BLOCKS_AFTER)], { hasHero: false })).toBeNull();
    expect(adsenseSplit([heading, paragraph, ...body(MIN_BLOCKS_AFTER)], { hasHero: true })).not.toBeNull();
    // An article whose intro already sits above the first heading needs no extra push.
    const withIntro = [paragraph, heading, paragraph, ...body(MIN_BLOCKS_AFTER)];
    expect(adsenseSplit(withIntro, { hasHero: false })?.before).toHaveLength(3);
    expect(adsenseSplit(withIntro, { hasHero: false })?.headingStart).toBe(1);
  });

  it("skips a paragraph that precedes the first heading", () => {
    const split = adsenseSplit([paragraph, paragraph, heading, paragraph, ...body(MIN_BLOCKS_AFTER)]);
    expect(split?.before.map((block) => block.type)).toEqual(["paragraph", "paragraph", "heading", "paragraph"]);
  });
});

describe("the request gate shared by the proxy and the renderer", () => {
  const ok = {
    host: "mokaair.com", dnt: null, gpc: null,
    pathname: "/zh-TW/guides/howto/tokyo-esim",
  };

  it("reads the article's own identity out of the path", () => {
    expect(adsenseRequestGate(ok)).toEqual({ locale: "zh-TW", kind: "howto", slug: "tokyo-esim" });
    expect(adsenseArticleRoute("/ja/life/ai-notes")).toEqual({ locale: "ja", kind: "life", slug: "ai-notes" });
    expect(adsenseArticleRoute("/en/guides/intel/fare-notice/")).toEqual({ locale: "en", kind: "intel", slug: "fare-notice" });
    expect(adsenseArticleRoute("/zh-TW/guides")).toBeNull();
  });

  it.each([
    ["a browser sending DNT", { dnt: "1" }],
    ["a browser sending GPC", { gpc: "1" }],
    ["a preview host", { host: "preview.example.test" }],
    ["localhost", { host: "localhost:3000" }],
    ["a lookalike host", { host: "mokaair.com.evil.test" }],
    ["no host at all", { host: null }],
    ["a hub", { pathname: "/zh-TW/guides" }],
    ["a shared trip", { pathname: "/zh-TW/share/9f8e7d6c5b4a" }],
  ])("refuses %s", (_label, override) => {
    expect(adsenseRequestGate({ ...ok, ...override })).toBeNull();
  });

  it("gives the proxy and the renderer the same answer for the same request", () => {
    // They used to decide separately, and the proxy's decision was the looser of the two:
    // a DNT request got a relaxed policy for ad code it was never going to be served.
    for (const override of [{}, { dnt: "1" }, { gpc: "1" }, { host: "localhost:3000" }, { pathname: "/zh-TW/life" }]) {
      const signals = { ...ok, ...override };
      expect(adsenseRequestGate(signals) !== null).toBe(isAdsenseArticlePath(signals.pathname)
        && isAdsenseOrigin(`https://${signals.host || ""}`)
        && signals.dnt !== "1" && signals.gpc !== "1");
    }
  });
});
