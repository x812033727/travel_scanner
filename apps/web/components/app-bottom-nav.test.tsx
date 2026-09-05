import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { AppBottomNav } from "./app-bottom-nav";
import { SiteVisibilityProvider } from "./site-visibility-provider";
import { closedSiteVisibility, openSiteVisibility } from "@/lib/site-features";

describe("AppBottomNav", () => {
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

  it("keeps every tab when the switches could not be read", () => {
    // "unavailable" is a failed fetch, not the owner closing the site: the
    // navigation stays and each page still enforces its own gate.
    render(
      <SiteVisibilityProvider state={{ status: "unavailable", features: closedSiteVisibility }}>
        <AppBottomNav />
      </SiteVisibilityProvider>,
    );
    expect(screen.getAllByRole("link")).toHaveLength(5);
  });
});
