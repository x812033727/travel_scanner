import { act, renderHook, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { adminNavigate, resolveAdminWorkspaceLocation, useAdminWorkspaceNavigation, type AdminWorkspaceConfig } from "./admin-workspace-navigation";
import { adminDomainsCopy } from "./admin-domains-copy";

const nextRoute = vi.hoisted(() => ({ pathname: null as string | null, search: null as string | null }));
vi.mock("next/navigation", () => ({ usePathname: () => nextRoute.pathname ?? window.location.pathname, useSearchParams: () => new URLSearchParams(nextRoute.search ?? window.location.search) }));
const config: AdminWorkspaceConfig = {
  defaultTab: "catalog", tabs: { catalog: ["merchants", "dishes"], completion: ["coordinates", "taxonomy"], settings: [] },
  legacy: { dishes: { tab: "catalog", section: "dishes" }, coordinates: { tab: "completion", section: "coordinates" }, restaurants: { tab: "nearby", section: "scans", pathname: "/admin/foods" } },
};
beforeEach(() => {
  nextRoute.pathname = null;
  nextRoute.search = null;
  window.history.replaceState(null, "", "/zh-TW/admin/foods");
});
afterEach(() => vi.restoreAllMocks());
describe("admin workspace navigation", () => {
  it("upgrades legacy hashes without losing locale or taxonomy filters", () => {
    const result = resolveAdminWorkspaceLocation("https://example.test/ja/admin/foods?taxonomy=missing_area#dishes", config);
    expect(result.tab).toBe("catalog");
    expect(result.section).toBe("dishes");
    expect(result.url.pathname).toBe("/ja/admin/foods");
    expect(result.url.searchParams.get("taxonomy")).toBe("missing_area");
    expect(result.url.hash).toBe("");
  });
  it("moves restaurant bookmarks from attractions to food and retains filters", () => {
    const result = resolveAdminWorkspaceLocation("https://example.test/ko/admin/hotspots?country=JP#restaurants", config);
    expect(result.redirect).toBe(true);
    expect(result.url.pathname).toBe("/ko/admin/foods");
    expect(result.url.searchParams.get("tab")).toBe("nearby");
    expect(result.url.searchParams.get("section")).toBe("scans");
    expect(result.url.searchParams.get("country")).toBe("JP");
  });
  it("validates tab/section and gives canonical parameters precedence over old hashes", () => {
    expect(resolveAdminWorkspaceLocation("https://a.test/?tab=unknown&section=coordinates", config).section).toBe("merchants");
    const result = resolveAdminWorkspaceLocation("https://a.test/?tab=settings#dishes", config);
    expect(result.tab).toBe("settings");
    expect(result.section).toBe("");
  });
  it("supports back/forward, section changes and same-route link updates", async () => {
    const { result, rerender } = renderHook(() => useAdminWorkspaceNavigation(config));
    await waitFor(() => expect(result.current.ready).toBe(true));
    act(() => result.current.selectTab("completion"));
    expect(result.current.section).toBe("coordinates");
    act(() => result.current.selectSection("taxonomy"));
    expect(result.current.section).toBe("taxonomy");
    act(() => window.history.back());
    await waitFor(() => expect(result.current.section).toBe("coordinates"));
    act(() => window.history.forward());
    await waitFor(() => expect(result.current.section).toBe("taxonomy"));
    window.history.replaceState(null, "", "/zh-TW/admin/foods?tab=settings&provider=google_maps");
    rerender();
    expect(result.current.tab).toBe("settings");
    expect(result.current.query.get("provider")).toBe("google_maps");
  });
  it("allows unsaved-change guards to cancel programmatic navigation", () => {
    const guard = (event: Event) => event.preventDefault();
    window.addEventListener("admin:before-navigate", guard);
    try {
      expect(adminNavigate(new URL("/admin/foods?tab=settings", window.location.origin))).toBe(false);
      expect(window.location.search).toBe("");
    } finally { window.removeEventListener("admin:before-navigate", guard); }
  });
  it("does not add duplicate history entries or wake leave guards for a no-op URL", () => {
    window.history.replaceState(null, "", "/zh-TW/admin/foods?tab=catalog&section=merchants");
    const push = vi.spyOn(window.history, "pushState");
    const guard = vi.fn();
    window.addEventListener("admin:before-navigate", guard);
    try {
      expect(adminNavigate(new URL(window.location.href))).toBe(true);
      expect(push).not.toHaveBeenCalled();
      expect(guard).not.toHaveBeenCalled();
    } finally { window.removeEventListener("admin:before-navigate", guard); }
  });
  it("does not push duplicate workspace tab or section selections", async () => {
    const { result } = renderHook(() => useAdminWorkspaceNavigation(config));
    await waitFor(() => expect(result.current.ready).toBe(true));
    const push = vi.spyOn(window.history, "pushState");
    act(() => result.current.selectTab("catalog"));
    act(() => result.current.selectSection("merchants"));
    expect(push).not.toHaveBeenCalled();
  });
  it("does not normalize the previous URL before Next commits a destination deep link", async () => {
    window.history.replaceState(null, "", "/zh-TW/admin");
    nextRoute.pathname = "/zh-TW/admin/foods";
    nextRoute.search = "tab=completion&section=taxonomy&taxonomy=missing_area";
    const { result, rerender } = renderHook(() => useAdminWorkspaceNavigation(config));
    await waitFor(() => expect(result.current.tab).toBe("completion"));
    expect(window.location.pathname).toBe("/zh-TW/admin");
    expect(window.location.search).toBe("");
    act(() => {
      window.history.replaceState(null, "", nextRoute.pathname + "?" + nextRoute.search);
      window.dispatchEvent(new Event("admin:location-change"));
    });
    rerender();
    expect(result.current.section).toBe("taxonomy");
    expect(window.location.search).toContain("taxonomy=missing_area");
  });
  it("prevents an outgoing workspace from rewriting the next workspace's query", async () => {
    const { result, rerender } = renderHook(() => useAdminWorkspaceNavigation(config));
    await waitFor(() => expect(result.current.ready).toBe(true));
    nextRoute.pathname = "/zh-TW/admin/hotels";
    nextRoute.search = "tab=imports&section=coverage";
    act(() => {
      window.history.replaceState(null, "", nextRoute.pathname + "?" + nextRoute.search);
      window.dispatchEvent(new Event("admin:location-change"));
    });
    rerender();
    expect(result.current.ready).toBe(false);
    expect(window.location.search).toBe("?tab=imports&section=coverage");
  });
  it("has complete isolated copy catalogs in all five locales", () => {
    const keys = Object.keys(adminDomainsCopy("en")).sort();
    for (const locale of ["zh-TW", "zh-CN", "ja", "ko"]) {
      const copy = adminDomainsCopy(locale);
      expect(Object.keys(copy).sort()).toEqual(keys);
      expect(Object.values(copy).every((value) => value.trim())).toBe(true);
      expect(copy.hotels).not.toBe("Hotels");
    }
  });
});
