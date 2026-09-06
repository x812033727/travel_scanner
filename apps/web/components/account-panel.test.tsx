import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import type { ReactNode } from "react";
import { closedSiteVisibility } from "@/lib/site-features";
import { AccountPanel } from "./account-panel";
import { HeaderSessionProvider } from "./header-session";
import { SiteVisibilityProvider } from "./site-visibility-provider";

const me = { id: "u1", email: "user@example.com" };
const usage = {
  remaining_uses: 12,
  reserved_uses: 1,
  available_uses: 11,
  limits: { saved_trips: 20, price_alerts: 20 },
};
const history = {
  items: [
    { id: "l1", occurred_at: "2026-08-30T10:00:00Z", type: "use", status: "charged", operation: "full_trip_search", summary: "旅程查詢 TPE → NRT · 2026-11-10–2026-11-15", change: -1, balance_after: 12, reference: "usage-ref-1", unit: "use", is_legacy: false },
    { id: "l2", occurred_at: "2026-08-29T10:00:00Z", type: "use", status: "released", operation: "public_airline_fare_search", summary: "航空公開票價 TPE → KIX", change: 0, balance_after: 13, reference: "usage-ref-2", unit: "use", is_legacy: false },
  ],
  next_cursor: null,
};

function ok(payload: unknown) {
  return { ok: true, status: 200, json: async () => payload };
}

function stubApi(responses: Record<string, unknown>) {
  return vi.fn(async (url: string) => {
    for (const [suffix, payload] of Object.entries(responses)) {
      if (url.endsWith(suffix) || url.includes(`${suffix}?`)) return ok(payload);
    }
    return { ok: false, status: 404, json: async () => ({ detail: "not found" }) };
  });
}

// The layout wraps the whole page in this, and the panel now reads the answer from it
// instead of asking /auth/me a second time.
function renderPanel(children: ReactNode = <AccountPanel />) {
  return render(<HeaderSessionProvider>{children}</HeaderSessionProvider>);
}

function urls(mock: { mock: { calls: unknown[][] } }) {
  return mock.mock.calls.map(([url]) => String(url));
}

afterEach(() => vi.unstubAllGlobals());

describe("account panel", () => {
  it("shows non-expiring usage balance and auditable history", async () => {
    vi.stubGlobal("fetch", stubApi({ "/auth/me": me, "/usage/history": history, "/usage": usage }));
    renderPanel();
    expect(await screen.findByText("user@example.com")).toBeTruthy();
    expect(await screen.findByText("11 次")).toBeTruthy();
    expect(screen.getByText("失敗未扣次")).toBeTruthy();
    expect(screen.getByText(/旅程查詢 TPE/)).toBeTruthy();
    expect(screen.getByText("-1 次")).toBeTruthy();
    expect(screen.getByText("0 次")).toBeTruthy();
  });

  it("copies the visible audit reference", async () => {
    const writeText = vi.fn();
    Object.defineProperty(navigator, "clipboard", { configurable: true, value: { writeText } });
    vi.stubGlobal("fetch", stubApi({ "/auth/me": me, "/usage/history": history, "/usage": usage }));
    renderPanel();
    fireEvent.click(await screen.findByRole("button", { name: "複製流水號 usage-ref-1" }));
    expect(writeText).toHaveBeenCalledWith("usage-ref-1");
  });

  it("asks the visitor to sign in when unauthenticated", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ ok: false, status: 401, json: async () => ({ detail: "請先登入後再繼續" }) }));
    renderPanel();

    // One sentence, one button. Pasting the API's own "請先登入後再繼續" in front of a
    // hand-written "請先登入。" produced "請先登入後再繼續，請先登入。" on the live site.
    const link = await screen.findByRole("link", { name: "前往登入" });
    expect(link.getAttribute("href")).toContain("/login?next=");
    expect(screen.getByText("登入後才能查看這裡的內容")).toBeTruthy();
    expect(document.body.textContent).not.toContain("請先登入後再繼續");
  });

  it("asks for nothing a signed-out visitor cannot have", async () => {
    const fetchMock = vi.fn(async () => ({ ok: false, status: 401, json: async () => ({ detail: "請先登入" }) }));
    vi.stubGlobal("fetch", fetchMock);
    renderPanel();
    await screen.findByRole("link", { name: "前往登入" });

    // Measured on the live site before this change: eight of the ten requests a
    // signed-out /account made were 401s, three of them the same /auth/me.
    const asked = urls(fetchMock);
    expect(asked.filter((url) => url.endsWith("/auth/me"))).toHaveLength(1);
    expect(asked.filter((url) => url.includes("/usage"))).toEqual([]);
    expect(asked.filter((url) => url.includes("/auth/identities"))).toEqual([]);
  });

  it("asks once for each thing a signed-in member can have", async () => {
    const fetchMock = stubApi({ "/auth/me": me, "/usage/history": history, "/usage": usage });
    vi.stubGlobal("fetch", fetchMock);
    renderPanel();
    await screen.findByText("11 次");

    const asked = urls(fetchMock);
    expect(asked.filter((url) => url.endsWith("/auth/me"))).toHaveLength(1);
    expect(asked.filter((url) => url.endsWith("/usage"))).toHaveLength(1);
    expect(asked.filter((url) => url.includes("/usage/history"))).toHaveLength(1);
    expect(asked.filter((url) => url.includes("/auth/identities"))).toHaveLength(1);
  });

  it("shows a history error instead of treating a failed request as empty", async () => {
    const fetchMock = vi.fn(async (url: string) => {
      if (url.endsWith("/auth/me")) return ok(me);
      if (url.endsWith("/usage")) return ok(usage);
      return { ok: false, status: 503, json: async () => ({ detail: "unavailable" }) };
    });
    vi.stubGlobal("fetch", fetchMock);
    renderPanel();
    expect(await screen.findByText("目前無法載入使用紀錄，請稍後再試。")).toBeTruthy();
  });

  it("hides the usage-pack link when pricing is closed", async () => {
    vi.stubGlobal("fetch", stubApi({ "/auth/me": me, "/usage/history": history, "/usage": usage }));
    renderPanel(
      <SiteVisibilityProvider state={{ status: "ready", features: closedSiteVisibility }}>
        <AccountPanel />
      </SiteVisibilityProvider>,
    );
    await screen.findByText("user@example.com");
    expect(screen.queryByRole("link", { name: "查看次數包" })).toBeNull();
  });

  it("rejects mismatched new passwords without calling the API", async () => {
    const fetchMock = stubApi({ "/auth/me": me, "/usage/history": history, "/usage": usage });
    vi.stubGlobal("fetch", fetchMock);
    renderPanel();
    await screen.findByText("user@example.com");
    fireEvent.change(screen.getByLabelText(/目前密碼/), { target: { value: "old-password-1" } });
    fireEvent.change(screen.getByLabelText(/^新密碼/), { target: { value: "new-password-12" } });
    fireEvent.change(screen.getByLabelText(/確認新密碼/), { target: { value: "different-pw-12" } });
    fireEvent.click(screen.getByRole("button", { name: "更新密碼" }));
    expect(await screen.findByRole("alert")).toBeTruthy();
    expect(fetchMock).not.toHaveBeenCalledWith(expect.stringContaining("change-password"), expect.anything());
  });

  it("submits a password change and reports success", async () => {
    const fetchMock = vi.fn(async (url: string, init?: RequestInit) => {
      if (url.endsWith("/auth/me")) return ok(me);
      if (url.endsWith("/usage")) return ok(usage);
      if (url.includes("/usage/history")) return ok(history);
      if (url.endsWith("/auth/change-password") && init?.method === "POST") return ok({ user: me, expires_in: 3600 });
      return { ok: false, status: 404, json: async () => ({ detail: "not found" }) };
    });
    vi.stubGlobal("fetch", fetchMock);
    renderPanel();
    await screen.findByText("user@example.com");
    fireEvent.change(screen.getByLabelText(/目前密碼/), { target: { value: "old-password-1" } });
    fireEvent.change(screen.getByLabelText(/^新密碼/), { target: { value: "new-password-12" } });
    fireEvent.change(screen.getByLabelText(/確認新密碼/), { target: { value: "new-password-12" } });
    fireEvent.click(screen.getByRole("button", { name: "更新密碼" }));
    expect(await screen.findByRole("status")).toBeTruthy();
    await waitFor(() => {
      const call = fetchMock.mock.calls.find(([url]) => (url as string).endsWith("/auth/change-password"));
      expect(call).toBeTruthy();
      expect(JSON.parse((call?.[1] as RequestInit).body as string)).toEqual({ current_password: "old-password-1", new_password: "new-password-12" });
    });
  });
});
