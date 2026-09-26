import { existsSync, readdirSync, readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";
import {
  AD_CLEARANCE_BLOCKS, adsenseArticleRoute, adsensePlacements, adsenseRequestGate, BLOCKS_PER_AD,
  isAdsenseArticlePath, isAdsenseOrigin, isAdsensePublisherId, isAdsenseSlotId, MAX_ADS,
  MIN_BLOCKS_AFTER, MIN_BLOCKS_BEFORE_WITHOUT_HERO, MIN_BLOCKS_BETWEEN, validAdsenseConfig,
} from "./adsense";
import { splitGuideBlocks, type GuideBlock } from "./guides";

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

type TestBlock = { type: string; level?: number };

/** Cut at every partner button, the way `splitGuideBlocks` cuts a real article. */
function segmentsOf(blocks: readonly TestBlock[]) {
  const segments: { blocks: TestBlock[]; headingStart: number }[] = [{ blocks: [], headingStart: 0 }];
  let headings = 0;
  for (const block of blocks) {
    if (block.type === "offer" || block.type === "partner_link") {
      segments.push({ blocks: [], headingStart: headings });
      continue;
    }
    if (block.type === "heading" && block.level === 2) headings += 1;
    segments[segments.length - 1].blocks.push(block);
  }
  return segments;
}

/**
 * Where the units land, as the index in the ORIGINAL block list each one goes before —
 * partner buttons included — so a test can say "an ad before block 3" about the body it wrote.
 */
function adPositions(blocks: readonly TestBlock[], options?: { hasHero?: boolean }) {
  const placements = adsensePlacements(segmentsOf(blocks), options);
  const positions: number[] = [];
  let index = 0;
  placements.forEach((pieces, segmentIndex) => {
    if (segmentIndex > 0) index += 1; // the button that opened this segment
    pieces.forEach((piece, pieceIndex) => {
      if (pieceIndex > 0) positions.push(index);
      index += piece.blocks.length;
    });
  });
  return positions;
}

describe("where the slots go", () => {
  it("puts the first unit after the first level-2 heading and its first paragraph", () => {
    // Never above the hero, and never before the section it belongs to has said anything.
    expect(adPositions([paragraph, heading, paragraph, ...body(MIN_BLOCKS_AFTER)])).toEqual([3]);
    expect(adPositions([paragraph, paragraph, heading, paragraph, ...body(MIN_BLOCKS_AFTER)])).toEqual([4]);
  });

  it("continues the heading numbering across every cut so the table of contents still points at them", () => {
    const blocks = [
      heading, paragraph, ...body(9),
      heading, paragraph, ...body(9),
      heading, paragraph, ...body(9),
      heading, paragraph, ...body(9),
    ];
    const [pieces] = adsensePlacements(segmentsOf(blocks));
    expect(pieces.length).toBeGreaterThan(2);
    pieces.forEach((piece, index) => {
      const before = pieces.slice(0, index).flatMap((p) => p.blocks);
      expect(piece.headingStart).toBe(before.filter((b) => b.type === "heading").length);
    });
    // Nothing is lost or repeated by cutting.
    expect(pieces.flatMap((piece) => piece.blocks)).toHaveLength(blocks.length);
  });

  it("leaves a thin article alone rather than making it mostly advertisement", () => {
    expect(adPositions([heading, paragraph, ...body(MIN_BLOCKS_AFTER - 1)])).toEqual([]);
    expect(adPositions([heading, paragraph])).toEqual([]);
    expect(adPositions([])).toEqual([]);
    expect(adsensePlacements([{ blocks: [], headingStart: 0 }])).toEqual([[{ blocks: [], headingStart: 0 }]]);
  });

  it("needs a level-2 heading followed by a paragraph", () => {
    expect(adPositions(body(20))).toEqual([]);
    expect(adPositions([{ type: "heading", level: 3 }, paragraph, ...body(20)])).toEqual([]);
    // A heading whose section is a list, not prose: no paragraph to start after.
    expect(adPositions([heading, { type: "list" }, { type: "list" }])).toEqual([]);
  });

  it("keeps more of the article above the first unit when there is no hero", () => {
    // With a hero the first unit follows the first heading and its paragraph. Without one
    // there is far less above that point, so the ad could be the first thing in the viewport.
    const blocks = [heading, paragraph, ...body(MIN_BLOCKS_AFTER + 2)];
    expect(adPositions(blocks, { hasHero: true })).toEqual([2]);
    expect(adPositions(blocks, { hasHero: false })).toEqual([MIN_BLOCKS_BEFORE_WITHOUT_HERO]);
    // A hero-less article too short to afford that clearance simply carries no ad.
    expect(adPositions([heading, paragraph, ...body(MIN_BLOCKS_AFTER)], { hasHero: false })).toEqual([]);
    expect(adPositions([heading, paragraph, ...body(MIN_BLOCKS_AFTER)], { hasHero: true })).toEqual([2]);
    // An article whose intro already sits above the first heading needs no extra push.
    expect(adPositions([paragraph, heading, paragraph, ...body(MIN_BLOCKS_AFTER)], { hasHero: false })).toEqual([3]);
  });

  it("keeps its distance from a partner button on both sides, and from the end panel", () => {
    const offer = { type: "offer" };
    // The first section is too short to hold a unit clear of the button that ends it, so the
    // first unit moves past the button — but not up against it.
    const blocks = [heading, paragraph, paragraph, offer, ...body(12)];
    expect(adPositions(blocks)).toEqual([3 + 1 + AD_CLEARANCE_BLOCKS]);
    // Every placement in a busy body stays clear of every button and of the end.
    const busy = [heading, ...body(5), offer, ...body(7), offer, ...body(4), offer, ...body(20), offer, ...body(9)];
    const buttons = busy.flatMap((block, index) => (block.type === "offer" ? [index] : []));
    const positions = adPositions(busy);
    expect(positions.length).toBeGreaterThan(0);
    for (const position of positions) {
      for (const button of buttons) {
        // A unit before `position` sits between blocks position-1 and position.
        if (button < position) expect(position - button - 1).toBeGreaterThanOrEqual(AD_CLEARANCE_BLOCKS);
        else expect(button - position).toBeGreaterThanOrEqual(AD_CLEARANCE_BLOCKS);
      }
      expect(busy.length - position).toBeGreaterThanOrEqual(AD_CLEARANCE_BLOCKS);
    }
  });

  it("only follows prose, never a heading, an image or a table", () => {
    const image = { type: "image" };
    const table = { type: "table" };
    // No hero, so the earliest place is block 3 — after the image. The next three places
    // follow an image, a table and a heading; the list is the first prose after them.
    const blocks = [heading, paragraph, image, table, heading, { type: "list" }, ...body(10)];
    expect(adPositions(blocks, { hasHero: false })).toEqual([6]);
  });

  it("treats a rich paragraph as prose while keeping code examples intact", () => {
    const rich = { type: "rich_paragraph" };
    const code = { type: "code" };
    const blocks = [heading, rich, code, ...Array.from({ length: 24 }, () => rich)];
    const positions = adPositions(blocks);
    expect(positions.length).toBeGreaterThan(0);
    expect(positions[0]).toBe(2);
    expect(positions.every(position => blocks[position - 1].type !== "code")).toBe(true);
  });

  it("spaces units out and scales how many with the length of the article", () => {
    const count = (length: number) => adPositions([heading, ...body(length - 1)]).length;
    expect(count(BLOCKS_PER_AD * 2 - 1)).toBe(1);
    expect(count(BLOCKS_PER_AD * 2)).toBe(2);
    expect(count(BLOCKS_PER_AD * 3)).toBe(3);
    expect(count(200)).toBe(MAX_ADS);
    const positions = adPositions([heading, ...body(199)]);
    positions.slice(1).forEach((position, index) => {
      expect(position - positions[index]).toBeGreaterThanOrEqual(MIN_BLOCKS_BETWEEN);
    });
  });
});

const contentDirectory = resolve(import.meta.dirname, "../../api/app/guides/content");

describe.skipIf(!existsSync(contentDirectory))("the rules against the articles actually published", () => {
  type Pack = { slug: string; locales: Record<string, { hero?: unknown; blocks: GuideBlock[] }> };
  const documents = readdirSync(contentDirectory)
    .filter((file) => file.endsWith(".json"))
    .flatMap((file) => {
      const pack = JSON.parse(readFileSync(resolve(contentDirectory, file), "utf8")) as Pack;
      return Object.entries(pack.locales).map(([locale, document]) => ({ id: `${pack.slug}:${locale}`, document }));
    });

  it("gives every article of ordinary length at least one unit", () => {
    // The rule this replaced placed a unit in the first slice only, and a third of the
    // articles opened with a partner button too early to carry any ad at all.
    const bare = documents.filter(({ document }) => {
      const segments = splitGuideBlocks(document.blocks);
      const body = segments.reduce((total, segment) => total + segment.blocks.length, 0);
      const units = adsensePlacements(segments, { hasHero: Boolean(document.hero) })
        .reduce((total, pieces) => total + pieces.length - 1, 0);
      return body >= BLOCKS_PER_AD * 2 && units === 0;
    });
    expect(documents.length).toBeGreaterThan(0);
    expect(bare.map(({ id }) => id)).toEqual([]);
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
    // The ad tag can read location.href, so the query would be in its hands. These requests
    // are served without ads instead of being redirected to the bare path, which used to
    // throw away every campaign tag before analytics could read it.
    ["an article URL carrying campaign tags", { pathname: "/zh-TW/life/ai-notes?utm_source=youtube&utm_medium=video" }],
    ["an article URL carrying any other query", { pathname: "/zh-TW/guides/howto/tokyo-esim?q=esim" }],
  ])("refuses %s", (_label, override) => {
    expect(adsenseRequestGate({ ...ok, ...override })).toBeNull();
  });

  it("gives the proxy and the renderer the same answer for the same request", () => {
    // They used to decide separately, and the proxy's decision was the looser of the two:
    // a DNT request got a relaxed policy for ad code it was never going to be served.
    for (const override of [
      {}, { dnt: "1" }, { gpc: "1" }, { host: "localhost:3000" }, { pathname: "/zh-TW/life" },
      { pathname: "/zh-TW/life/ai-notes?utm_campaign=ai-notes" },
    ]) {
      const signals = { ...ok, ...override };
      expect(adsenseRequestGate(signals) !== null).toBe(isAdsenseArticlePath(signals.pathname)
        && isAdsenseOrigin(`https://${signals.host || ""}`)
        && signals.dnt !== "1" && signals.gpc !== "1" && !signals.pathname.includes("?"));
    }
  });
});
