import { render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { HeaderAuth } from "./header-auth";
import { HeaderSessionProvider } from "./header-session";
import { SiteVisibilityProvider } from "./site-visibility-provider";
import { openSiteVisibility } from "@/lib/site-features";

vi.mock("next/navigation", () => ({ useRouter: () => ({ push: vi.fn(), refresh: vi.fn() }), useSearchParams: () => new URLSearchParams() }));

function ok(payload: unknown) {
  return { ok: true, status: 200, json: async () => payload };
}

function renderHeaderAuth(memberFeaturesEnabled = true) {
  return render(
    <SiteVisibilityProvider state={{ status: "ready", features: { ...openSiteVisibility, member_features_enabled: memberFeaturesEnabled } }}>
      <HeaderSessionProvider><HeaderAuth /></HeaderSessionProvider>
    </SiteVisibilityProvider>,
  );
}

afterEach(() => vi.unstubAllGlobals());

describe("header auth", () => {
  it("shows the login link when the visitor is not authenticated", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ ok: false, status: 401, json: async () => ({ detail: "未登入" }) }));
    renderHeaderAuth();
    expect(await screen.findByRole("link", { name: "登入" })).toBeTruthy();
  });

  it("hides the signed-out login button when member features are disabled", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ ok: false, status: 401, json: async () => ({ detail: "未登入" }) }));
    const { container } = renderHeaderAuth(false);
    await new Promise((resolve) => setTimeout(resolve, 0));
    expect(screen.queryByRole("link", { name: "登入" })).toBeNull();
    expect(container.textContent).toBe("");
  });

  it("does not disguise a server failure as a signed-out visitor", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ ok: false, status: 500, json: async () => ({ detail: "資料庫錯誤" }) }));
    renderHeaderAuth();
    expect((await screen.findByRole("status")).textContent).toContain("登入狀態異常");
    expect(screen.queryByRole("link", { name: "登入" })).toBeNull();
  });

  it("shows the account email and logout button when authenticated", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(ok({ id: "u1", email: "user@example.com" })));
    renderHeaderAuth();
    expect(await screen.findByRole("button", { name: "登出" })).toBeTruthy();
    expect(screen.getByText("user@example.com")).toBeTruthy();
  });

  it("shows the admin link only for administrators, even when public member chrome is hidden", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(ok({
      id: "u1", email: "admin@example.com", is_admin: true,
    })));
    renderHeaderAuth(false);
    expect((await screen.findByRole("link", { name: "管理後台" })).getAttribute("href")).toBe("/admin");
    expect(screen.getByRole("button", { name: "登出" })).toBeTruthy();
  });
});
