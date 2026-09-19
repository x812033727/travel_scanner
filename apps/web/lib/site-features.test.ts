import { describe, expect, it } from "vitest";

import {
  closedSiteVisibility,
  featureEnabled,
  featureVisible,
  openSiteVisibility,
  type SiteVisibilityState,
} from "./site-features";

const state = (
  status: SiteVisibilityState["status"],
  features = openSiteVisibility,
): SiteVisibilityState => ({ status, features });

describe("featureEnabled", () => {
  it("follows the switch when the settings service answered", () => {
    expect(featureEnabled(state("ready"), "hotspots")).toBe(true);
    expect(featureEnabled(state("ready", closedSiteVisibility), "hotspots")).toBe(false);
  });

  it("trusts a remembered answer rather than emitting noindex on a live page", () => {
    // This is the whole point of "stale": the value came from the service, the current read
    // merely failed. Treating it as closed put `noindex` on pages that were open and dropped
    // them from the sitemap for that request.
    expect(featureEnabled(state("stale"), "hotspots")).toBe(true);
  });

  it("still honours a remembered close", () => {
    expect(featureEnabled(state("stale", closedSiteVisibility), "hotspots")).toBe(false);
  });

  it("closes everything only when nothing is known", () => {
    expect(featureEnabled(state("unavailable", closedSiteVisibility), "hotspots")).toBe(false);
    // Even handed open flags, "unavailable" means they were never read.
    expect(featureEnabled(state("unavailable", openSiteVisibility), "hotspots")).toBe(false);
  });
});

describe("featureVisible", () => {
  it("keeps the door on the map when the switches could not be read", () => {
    // A navigation surface stripped by a settings blip re-orphans the pages the footer is
    // now the only inbound link for.
    expect(featureVisible(state("unavailable", closedSiteVisibility), "hotspots")).toBe(true);
  });

  it("uses the real flags whenever there are any, fresh or remembered", () => {
    expect(featureVisible(state("ready", closedSiteVisibility), "hotspots")).toBe(false);
    expect(featureVisible(state("stale", closedSiteVisibility), "hotspots")).toBe(false);
    expect(featureVisible(state("stale"), "hotspots")).toBe(true);
  });
});
