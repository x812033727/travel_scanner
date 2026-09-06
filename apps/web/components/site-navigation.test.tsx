import { render, screen } from "@testing-library/react";
import { StrictMode } from "react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { closedSiteVisibility, openSiteVisibility } from "@/lib/site-features";
import { HeaderSessionProvider } from "./header-session";
import { SiteNavigation } from "./site-navigation";
import { SiteVisibilityProvider } from "./site-visibility-provider";

afterEach(() => vi.unstubAllGlobals());

describe("SiteNavigation", () => {
  it("shares one auth request across desktop and compact mobile controls", async () => {
    const fetchMock = vi.fn().mockResolvedValue(new Response(JSON.stringify({
      id: "admin-1",
      email: "admin@example.com",
      is_admin: true,
    }), { status: 200 }));
    vi.stubGlobal("fetch", fetchMock);
    render(
      <StrictMode>
        <SiteVisibilityProvider state={{ status: "ready", features: openSiteVisibility }}>
          <HeaderSessionProvider>
            <SiteNavigation />
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
    expect(fetchMock).toHaveBeenCalledTimes(1);
  });

  it("keeps the nav when visibility could not be read, hides it when closed", () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(
      new Response(JSON.stringify({ detail: "signed out" }), { status: 401 }),
    ));
    const unavailable = render(
      <SiteVisibilityProvider state={{ status: "unavailable", features: closedSiteVisibility }}>
        <HeaderSessionProvider>
          <SiteNavigation />
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
          <SiteNavigation />
        </HeaderSessionProvider>
      </SiteVisibilityProvider>,
    );
    expect(screen.queryByRole("link", { name: "熱門景點" })).toBeNull();
    expect(screen.queryByRole("link", { name: "航班動態" })).toBeNull();
    expect(screen.queryByRole("link", { name: "方案與次數包" })).toBeNull();
  });
});
