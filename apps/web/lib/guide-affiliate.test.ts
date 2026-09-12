import { describe, expect, it } from "vitest";
import { guideAffiliateDestination, guideAffiliateModules } from "./guide-affiliate";

const topics = (...slugs: string[]) => slugs.map((slug) => ({ slug, label: slug }));

describe("guideAffiliateModules", () => {
  it("maps each monetisable topic to its module", () => {
    expect(guideAffiliateModules(topics("connectivity"))).toEqual(["connectivity"]);
    expect(guideAffiliateModules(topics("hotel"))).toEqual(["hotel"]);
    expect(guideAffiliateModules(topics("transport"))).toEqual(["transport"]);
    expect(guideAffiliateModules(topics("deal"))).toEqual(["flight"]);
    for (const slug of ["itinerary", "season", "family", "nature", "culture", "viewpoint", "beach"]) {
      expect(guideAffiliateModules(topics(slug))).toEqual(["activities"]);
    }
  });

  it("returns nothing for topics with no honest module, or unknown slugs", () => {
    for (const slug of ["entry", "packing", "budget", "etiquette", "safety", "food", "shopping", "nightlife", "made-up"]) {
      expect(guideAffiliateModules(topics(slug))).toEqual([]);
    }
    expect(guideAffiliateModules([])).toEqual([]);
  });

  it("dedupes and keeps the canonical module order regardless of topic order", () => {
    expect(guideAffiliateModules(topics("season", "connectivity", "itinerary", "hotel", "deal"))).toEqual([
      "flight", "hotel", "activities", "connectivity",
    ]);
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
