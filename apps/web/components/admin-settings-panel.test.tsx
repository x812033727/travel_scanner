import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { AdminSettingsPanel } from "./admin-settings-panel";

const snapshot = {
  encryption_source: "SETTINGS_ENCRYPTION_KEY",
  providers: [
    {
      provider: "google_maps",
      label: "Google Maps",
      description: "地點與路線",
      enabled: true,
      configured: true,
      status: "ready",
      status_message: "Places 與 Routes 已設定",
      config: { route_cache_ttl_seconds: 900 },
      config_sources: { route_cache_ttl_seconds: "environment" },
      secrets: {
        google_maps_api_key: { configured: true, masked: "••••••••abcd", source: "database" },
        next_public_google_maps_browser_key: { configured: false, source: "none" },
      },
    },
  ],
  audit: [],
};

afterEach(() => vi.unstubAllGlobals());

describe("AdminSettingsPanel", () => {
  it("shows only masked secrets and sends a newly entered key", async () => {
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(new Response(JSON.stringify(snapshot), { status: 200 }))
      .mockResolvedValueOnce(new Response(JSON.stringify(snapshot), { status: 200 }));
    vi.stubGlobal("fetch", fetchMock);
    render(<AdminSettingsPanel />);

    const heading = await screen.findByRole("heading", { name: "Google Maps" });
    const section = heading.closest("section");
    expect(section).toBeTruthy();
    expect(within(section!).getByPlaceholderText("••••••••abcd")).toBeTruthy();
    expect(screen.queryByDisplayValue("existing-full-key")).toBeNull();

    fireEvent.change(within(section!).getByLabelText("伺服器 API Key"), {
      target: { value: "new-server-key" },
    });
    fireEvent.click(within(section!).getByRole("button", { name: "儲存設定" }));
    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(2));
    const request = fetchMock.mock.calls[1][1] as RequestInit;
    const body = JSON.parse(String(request.body));
    expect(body.secrets.google_maps_api_key).toBe("new-server-key");
    expect(body.secrets.next_public_google_maps_browser_key).toBeUndefined();
  });

  it("explains when the account is not an administrator", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify({
      code: "admin_required",
      detail: "此功能僅限系統管理員使用",
    }), { status: 403 })));
    render(<AdminSettingsPanel />);
    expect(await screen.findByText("無法開啟管理後台")).toBeTruthy();
    expect(screen.getByText("此功能僅限系統管理員使用")).toBeTruthy();
  });

  it("shows a failed connection check as an error", async () => {
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(new Response(JSON.stringify(snapshot), { status: 200 }))
      .mockResolvedValueOnce(new Response(JSON.stringify({
        status: "failed",
        message: "API key 無效",
        latency_ms: 42,
      }), { status: 200 }))
      .mockResolvedValueOnce(new Response(JSON.stringify(snapshot), { status: 200 }));
    vi.stubGlobal("fetch", fetchMock);
    render(<AdminSettingsPanel />);

    const heading = await screen.findByRole("heading", { name: "Google Maps" });
    const section = heading.closest("section");
    fireEvent.click(within(section!).getByRole("button", { name: "測試連線" }));

    expect((await screen.findByRole("alert")).textContent).toContain("API key 無效（42 ms）");
  });
});
