import { render, screen } from "@testing-library/react";
import { StrictMode } from "react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { closedSiteVisibility, openSiteVisibility } from "@/lib/site-features";
import { HeaderSessionProvider } from "./header-session";
import { SiteNavigation } from "./site-navigation";
import { SiteVisibilityProvider } from "./site-visibility-provider";
import { ThemeProvider } from "./theme-provider";

afterEach(() => vi.unstubAllGlobals());

describe("SiteNavigation", () => {
  it("shares one auth request across desktop and compact mobile controls", async () => {
    const fetchMock = vi.fn(async (input: RequestInfo | URL) => new Response(JSON.stringify(String(input).endsWith("/discovery/status") ? { enabled: false } : {
      id: "admin-1",
      email: "admin@example.com",
      is_admin: true,
    }), { status: 200 }));
    vi.stubGlobal("fetch", fetchMock);
    render(
      <StrictMode>
        <SiteVisibilityProvider state={{ status: "ready", features: openSiteVisibility }}>
          <HeaderSessionProvider>
            <ThemeProvider><SiteNavigation /></ThemeProvider>
          </HeaderSessionProvider>
        </SiteVisibilityProvider>
      </StrictMode>,
    );

    // Both bars carry the link and CSS shows exactly one of them per viewport, so an
    // administrator reaches the control centre on a phone as well as on a desktop.
    const adminLinks = await screen.findAllByRole("link", { name: "管理後台" });
    expect(adminLinks).toHaveLength(2);
    expect(adminLinks.every((link) => link.getAttribute("href") === "/admin")).toBe(true);
    expect(screen.getByRole("link", { name: "會員帳號" }).getAttribute("href")).toBe("/account");
    expect(fetchMock.mock.calls.filter(([input]) => String(input).endsWith("/auth/me"))).toHaveLength(1);
    expect(fetchMock.mock.calls.filter(([input]) => String(input).endsWith("/discovery/status"))).toHaveLength(1);
  });

  it("keeps the nav when visibility could not be read, hides it when closed", () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(
      new Response(JSON.stringify({ detail: "signed out" }), { status: 401 }),
    ));
    const unavailable = render(
      <SiteVisibilityProvider state={{ status: "unavailable", features: closedSiteVisibility }}>
        <HeaderSessionProvider>
          <ThemeProvider><SiteNavigation /></ThemeProvider>
        </HeaderSessionProvider>
      </SiteVisibilityProvider>,
    );

    // A failed settings fetch is not the owner closing the site: the links stay
    // and PublicFeatureGate still guards each page behind them.
    expect(screen.getByRole("link", { name: "熱門景點" })).toBeTruthy();
    expect(screen.getByRole("link", { name: "航班動態" })).toBeTruthy();
    unavailable.unmount();

    render(
      <SiteVisibilityProvider state={{ status: "ready", features: closedSiteVisibility }}>
        <HeaderSessionProvider>
          <ThemeProvider><SiteNavigation /></ThemeProvider>
        </HeaderSessionProvider>
      </SiteVisibilityProvider>,
    );
    expect(screen.queryByRole("link", { name: "熱門景點" })).toBeNull();
    expect(screen.queryByRole("link", { name: "航班動態" })).toBeNull();
    expect(screen.queryByRole("link", { name: "方案與次數包" })).toBeNull();
  });

  // Discovery mode used to drop TextSizeSwitcher, ThemeSwitcher and HeaderAuth as a
  // single group, which left the desktop header with no way to sign in or out at all.
  // useDiscoveryStatus caches its answer in module scope and only re-asks after 30s,
  // so this case ages that cache out — and runs last, because the answer it caches
  // (discovery on) would change what every earlier case renders.
  it("keeps the sign-in control in the desktop header while discovery is on", async () => {
    const realNow = Date.now;
    vi.spyOn(Date, "now").mockImplementation(() => realNow() + 60_000);
    vi.stubGlobal("fetch", vi.fn(async (input: RequestInfo | URL) =>
      String(input).endsWith("/discovery/status")
        ? new Response(JSON.stringify({ enabled: true }), { status: 200 })
        : new Response(JSON.stringify({ detail: "signed out" }), { status: 401 })));
    try {
      render(
        <SiteVisibilityProvider state={{ status: "ready", features: openSiteVisibility }}>
          <HeaderSessionProvider>
            <ThemeProvider><SiteNavigation /></ThemeProvider>
          </HeaderSessionProvider>
        </SiteVisibilityProvider>,
      );

      // The discovery destinations confirm the header really is in discovery mode.
      expect((await screen.findAllByRole("link", { name: "\u63a2\u7d22" })).length).toBeGreaterThan(0);
      expect((await screen.findByRole("link", { name: "\u767b\u5165" })).getAttribute("href")).toBe("/login");
    } finally {
      vi.mocked(Date.now).mockRestore();
    }
  });
});
