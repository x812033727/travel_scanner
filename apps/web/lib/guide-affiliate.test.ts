import { describe, expect, it } from "vitest";
import {
  guideAffiliateDestination,
  guideAffiliateModules,
  guideAffiliatePlacement,
  MODULE_ORDER,
} from "./guide-affiliate";

const topics = (...slugs: string[]) => slugs.map((slug) => ({ slug, label: slug }));

describe("guideAffiliateModules", () => {
  it("maps each monetisable topic to its module", () => {
    expect(guideAffiliateModules(topics("connectivity"), "howto")).toEqual(["connectivity"]);
    expect(guideAffiliateModules(topics("hotel"), "howto")).toEqual(["hotel"]);
    expect(guideAffiliateModules(topics("transport"), "howto")).toEqual(["transport"]);
    expect(guideAffiliateModules(topics("deal"), "intel")).toEqual(["flight"]);
    for (const slug of ["itinerary", "season", "family", "nature", "culture", "viewpoint", "beach"]) {
      expect(guideAffiliateModules(topics(slug), "howto")).toEqual(["activities"]);
    }
  });

  it("returns nothing for topics with no honest module, or unknown slugs", () => {
    for (const slug of ["entry", "packing", "budget", "etiquette", "safety", "food", "shopping", "nightlife", "made-up"]) {
      expect(guideAffiliateModules(topics(slug), "howto")).toEqual([]);
    }
    expect(guideAffiliateModules([], "howto")).toEqual([]);
  });

  it("dedupes and keeps the canonical module order regardless of topic order", () => {
    expect(guideAffiliateModules(topics("season", "connectivity", "itinerary", "hotel", "deal"), "howto")).toEqual([
      "flight", "hotel", "activities", "connectivity",
    ]);
  });

  // A lifestyle topic names no travel module, so the topic table can say nothing about a
  // `life` article. The editor's destination is the contextual signal instead, and the panel
  // matches the city page's own: every module. See the docstring in guide-affiliate.ts.
  it("offers a lifestyle article every module, whatever its topics say", () => {
    expect(guideAffiliateModules(topics("ai"), "life")).toEqual([...MODULE_ORDER]);
    expect(guideAffiliateModules(topics("tutorial", "gadgets"), "life")).toEqual([...MODULE_ORDER]);
    expect(guideAffiliateModules([], "life")).toEqual([...MODULE_ORDER]);
  });

  it("keeps the lifestyle topics out of the travel sections", () => {
    for (const slug of ["ai", "tutorial", "software", "gadgets", "productivity", "daily", "misc"]) {
      expect(guideAffiliateModules(topics(slug), "howto")).toEqual([]);
      expect(guideAffiliateModules(topics(slug), "intel")).toEqual([]);
    }
  });
});

describe("guideAffiliatePlacement", () => {
  it("records each section under its own surface, so the click report can tell them apart", () => {
    expect(guideAffiliatePlacement("intel")).toBe("guide");
    expect(guideAffiliatePlacement("howto")).toBe("guide");
    expect(guideAffiliatePlacement("life")).toBe("life");
  });
});

describe("guideAffiliateDestination", () => {
  it("passes catalog destinations through and folds Osaka and Kyoto into their shared id", () => {
    expect(guideAffiliateDestination("tokyo")).toBe("tokyo");
    expect(guideAffiliateDestination("kyoto")).toBe("osaka-kyoto");
    expect(guideAffiliateDestination("osaka-kyoto")).toBe("osaka-kyoto");
  });

  it("is null for cross-destination articles and unknown ids", () => {
    expect(guideAffiliateDestination(null)).toBeNull();
    expect(guideAffiliateDestination("atlantis")).toBeNull();
  });
});
