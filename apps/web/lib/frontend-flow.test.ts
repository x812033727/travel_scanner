import { beforeEach, describe, expect, it } from "vitest";
import { completedTripDestination, planningResumeUrl, planningReturnPath, rememberPlanningIntent, tripDayOptions } from "./frontend-flow";
import { frontendActive, frontendCopy, frontendDestinations } from "./frontend-navigation";

const place = "10000000-0000-4000-8000-000000000001";
const trip = "20000000-0000-4000-8000-000000000001";
describe("frontend flow state", () => {
  beforeEach(() => sessionStorage.clear());
  it("keeps four destinations and a single active destination", () => {
    expect(frontendDestinations).toHaveLength(4);
    for (const path of ["/zh-TW", "/en/explore?x", "/explore/collections", "/trips/new", "/my", "/search/new", "/foods", "/community/collections"]) {
      const normalized = path.split("?")[0];
      expect(frontendDestinations.filter((item) => frontendActive(item.key, normalized))).toHaveLength(1);
    }
    expect(frontendActive("trips", "/search/new")).toBe(false);
    for (const locale of ["en", "zh-TW", "zh-CN", "ja", "ko"]) expect(Object.keys(frontendCopy(locale))).toEqual(Object.keys(frontendCopy("en")));
  });
  it("rejects external or privileged return locations", () => {
    for (const bad of ["//evil.test", "https://evil.test", "/admin", "/api/travel", "/\\evil.test"]) expect(planningReturnPath(bad)).toBe("/explore");
    expect(planningReturnPath("/zh-TW/explore?destination=tokyo&content=abc#card")).toBe("/explore?destination=tokyo&content=abc#card");
  });
  it("returns to the original confirmation without writing or losing filters", () => {
    expect(rememberPlanningIntent("A", "hotspot", place, "/explore?q=park&destination=tokyo")).toBe(true);
    expect(completedTripDestination("B", trip, true)).toBe(`/trips/${trip}`);
    expect(completedTripDestination("A", trip)).toBe(`/trips/${trip}`);
    const result = new URL(completedTripDestination("A", trip, true), "https://example.test");
    expect(result.searchParams.get("q")).toBe("park");
    expect(result.searchParams.get("resume_item")).toBe(`hotspot:${place}`);
    expect(result.searchParams.get("resume_trip")).toBe(trip);
    expect(result.searchParams.get("content")).toBe(`hotspot:${place}`);
    expect(completedTripDestination("A", trip, true)).toBe(`/trips/${trip}`);
  });
  it("rejects stale, malformed or mismatched account intents", () => {
    for (const value of [{ accountId: "B", kind: "hotspot", id: place, createdAt: Date.now(), returnTo: "/explore" }, { accountId: "A", kind: "hotspot", id: place, createdAt: 0, returnTo: "/explore" }, { accountId: "A", kind: "post", id: place, createdAt: Date.now(), returnTo: "/explore" }]) {
      sessionStorage.setItem("mokaair-pending-plan:A", JSON.stringify(value));
      expect(completedTripDestination("A", trip, true)).toBe(`/trips/${trip}`);
    }
    expect(rememberPlanningIntent("A", "hotspot", "bad", "/explore")).toBe(false);
  });
  it("builds stable UTC day options without device timezone drift", () => {
    expect(tripDayOptions("2027-03-13", "2027-03-15", "en").map((day) => day.value)).toEqual(["2027-03-13", "2027-03-14", "2027-03-15"]);
    expect(tripDayOptions("bad", "bad", "en")).toEqual([]);
    expect(planningResumeUrl("/foods?country=JP", "food", place)).toContain("country=JP");
  });
});
