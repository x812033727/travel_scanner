import { describe, expect, it } from "vitest";
import { serviceDiscoveryDestinations, serviceDiscoveryModules } from "./travel-service-discovery";
import { klookAffiliateCopy } from "./klook-affiliate-copy";

describe("reviewed service discovery context", () => {
  it("maps each category without adding unrelated flight offers", () => {
    expect(serviceDiscoveryModules("hotel")).toEqual(["hotel"]);
    expect(serviceDiscoveryModules("tour")).toEqual(["activities"]);
    expect(serviceDiscoveryModules("transfer")).toEqual(["transport"]);
    expect(serviceDiscoveryModules("esim")).toEqual(["connectivity"]);
    expect(serviceDiscoveryModules("all")).toEqual(["hotel", "activities", "transport", "connectivity"]);
  });
  it("normalizes Osaka and Kyoto once and never guesses unsupported destinations", () => {
    expect(serviceDiscoveryDestinations(["osaka", "kyoto", "osaka-kyoto", "tokyo", "unknown", "tokyo"]))
      .toEqual(["osaka-kyoto", "tokyo"]);
    expect(serviceDiscoveryDestinations([])).toEqual([]);
  });
  it("provides complete independent copy in the five supported locales", () => {
    for (const locale of ["zh-TW", "zh-CN", "en", "ja", "ko"]) {
      expect(Object.keys(klookAffiliateCopy(locale))).toEqual(Object.keys(klookAffiliateCopy("en")));
      expect(Object.values(klookAffiliateCopy(locale)).every(Boolean)).toBe(true);
    }
  });
});
