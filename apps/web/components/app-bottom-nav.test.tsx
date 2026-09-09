import { render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { AppBottomNav } from "./app-bottom-nav";
import { SiteVisibilityProvider } from "./site-visibility-provider";
import { closedSiteVisibility, openSiteVisibility } from "@/lib/site-features";
const discovery = vi.hoisted(() => ({ enabled: false, loading: false }));
vi.mock("@/lib/discovery", () => ({useDiscoveryStatus: () => discovery}));
beforeEach(() => { discovery.enabled = false; discovery.loading = false; });

describe("AppBottomNav", () => {
  it("exposes exactly four primary destinations with discovery enabled", () => {
    discovery.enabled = true;
    render(<AppBottomNav />);
    expect(screen.getAllByRole("link").map((link) => [link.textContent, link.getAttribute("href")])).toEqual([
      ["探索", "/explore"], ["收藏", "/explore/collections"], ["我的旅程", "/trips"], ["我的", "/my"],
    ]);
  });
  it("waits for the flag instead of showing the legacy navigation first", () => {
    discovery.loading = true; render(<AppBottomNav />);
    expect(screen.queryByRole("link")).toBeNull();
  });
  it("provides the five thumb-friendly app destinations", () => {
    render(<AppBottomNav />);
    const links = screen.getAllByRole("link");
    expect(links.map((link) => link.textContent)).toEqual(["探索", "規劃", "旅程", "通知", "我的"]);
    expect(links.map((link) => link.getAttribute("href"))).toEqual([
      "/hotspots", "/#trip-search", "/trips", "/alerts", "/account",
    ]);
    for (const link of links) expect(link.className).toContain("app-bottom-nav-item");
  });

  it("drops a tab whose feature the site has turned off", () => {
    render(
      <SiteVisibilityProvider state={{ status: "ready", features: { ...openSiteVisibility, alerts_enabled: false } }}>
        <AppBottomNav />
      </SiteVisibilityProvider>,
    );
    const labels = screen.getAllByRole("link").map((link) => link.textContent);
    expect(labels).toEqual(["探索", "規劃", "旅程", "我的"]);
  });

  it("points explore at foods when hotspots are turned off instead of dropping it", () => {
    render(
      <SiteVisibilityProvider state={{ status: "ready", features: { ...openSiteVisibility, hotspots_enabled: false } }}>
        <AppBottomNav />
      </SiteVisibilityProvider>,
    );
    const explore = screen.getByRole("link", { name: "探索" });
    expect(explore.getAttribute("href")).toBe("/foods");
    expect(screen.getAllByRole("link")).toHaveLength(5);
  });

  it("keeps every tab when the switches could not be read", () => {
    // "unavailable" is a failed fetch, not the owner closing the site: the
    // navigation stays and each page still enforces its own gate.
    render(
      <SiteVisibilityProvider state={{ status: "unavailable", features: closedSiteVisibility }}>
        <AppBottomNav />
      </SiteVisibilityProvider>,
    );
    const links = screen.getAllByRole("link");
    expect(links).toHaveLength(5);
    expect(screen.getByRole("link", { name: "探索" }).getAttribute("href")).toBe("/hotspots");
  });
});
