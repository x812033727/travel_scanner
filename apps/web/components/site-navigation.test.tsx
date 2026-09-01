import { fireEvent, render, screen } from "@testing-library/react";
import { StrictMode } from "react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { closedSiteVisibility, openSiteVisibility } from "@/lib/site-features";
import { SiteNavigation } from "./site-navigation";
import { SiteVisibilityProvider } from "./site-visibility-provider";

afterEach(() => vi.unstubAllGlobals());

describe("SiteNavigation", () => {
  it("shares one auth request across desktop and mobile admin entries", async () => {
    const fetchMock = vi.fn().mockResolvedValue(new Response(JSON.stringify({
      id: "admin-1",
      email: "admin@example.com",
      is_admin: true,
    }), { status: 200 }));
    vi.stubGlobal("fetch", fetchMock);
    render(
      <StrictMode>
        <SiteVisibilityProvider state={{ status: "ready", features: openSiteVisibility }}>
          <SiteNavigation />
        </SiteVisibilityProvider>
      </StrictMode>,
    );

    expect((await screen.findByRole("link", { name: "管理後台" })).getAttribute("href")).toBe("/admin/users");
    fireEvent.click(screen.getByRole("button", { name: "開啟導覽選單" }));
    expect(screen.getAllByRole("link", { name: "管理後台" })).toHaveLength(2);
    expect(fetchMock).toHaveBeenCalledTimes(1);
  });

  it("hides every controlled route when visibility is unavailable", () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(
      new Response(JSON.stringify({ detail: "signed out" }), { status: 401 }),
    ));
    render(
      <SiteVisibilityProvider state={{ status: "unavailable", features: closedSiteVisibility }}>
        <SiteNavigation />
      </SiteVisibilityProvider>,
    );

    expect(screen.queryByRole("link", { name: "熱門景點" })).toBeNull();
    expect(screen.queryByRole("link", { name: "航班動態" })).toBeNull();
    expect(screen.queryByRole("link", { name: "方案與次數包" })).toBeNull();
  });
});
