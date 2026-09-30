import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { AdminOperationsProvider } from "./admin-operations-provider";
import { safeVpsDesktopUrl, YoutubeVpsSettingsCard, type YoutubeVpsSettingsView } from "./admin-video-vps-settings";
import type { AdminBootstrap } from "@/lib/admin-operations";
import { videoVpsCopy } from "@/lib/video-vps-copy";

const endpoint = "/api/travel/admin/video-youtube/vps/settings";
const channel = "UC" + "a".repeat(22);
const saved: YoutubeVpsSettingsView = {
  enabled: true, url: "http://uploader:8789", channel_id: channel, desktop_url: "http://127.0.0.1:6080/vnc.html",
  secret_set: true, configured: true, source: "database", updated_at: "2026-09-30T10:00:00Z",
  last_test_status: null, last_test_message: null, last_tested_at: null,
};
function bootstrap(manage: boolean): AdminBootstrap {
  return { admin_roles: [], admin_capabilities: ["content.read", ...(manage ? ["settings.manage"] : [])], navigation: [], pending_counts: {}, system_status: {}, environment: "test", can_deploy: false, can_manage_database: false };
}
async function mount(manage = true) {
  render(<AdminOperationsProvider bootstrap={bootstrap(manage)}><YoutubeVpsSettingsCard /></AdminOperationsProvider>);
  const card = await screen.findByRole("region", { name: "VPS 上傳服務" });
  await within(card).findByLabelText("服務密鑰");
  await waitFor(() => expect(within(card).getByRole("button", { name: "重新讀取已儲存設定" })).toHaveProperty("disabled", false));
  return within(card);
}
afterEach(() => { vi.unstubAllGlobals(); vi.restoreAllMocks(); });

describe("VPS settings", () => {
  it("keeps the five catalogs aligned", () => {
    const keys = Object.keys(videoVpsCopy("en")).sort();
    for (const locale of ["zh-TW", "zh-CN", "ja", "ko"]) expect(Object.keys(videoVpsCopy(locale)).sort()).toEqual(keys);
  });

  it("shows read-only settings without allowing saves or connection tests", async () => {
    const fetchMock = vi.fn(() => Promise.resolve(Response.json(saved)));
    vi.stubGlobal("fetch", fetchMock);
    const card = await mount(false);
    expect(card.getByRole("note").textContent).toContain("修改與測試需要設定管理權限");
    expect(card.getByLabelText("服務密鑰")).toHaveProperty("disabled", true);
    expect(card.getByLabelText("服務密鑰")).toHaveProperty("value", "");
    expect(card.getByRole("button", { name: "儲存 VPS 設定" })).toHaveProperty("disabled", true);
    expect(card.getByRole("button", { name: "測試已儲存的連線" })).toHaveProperty("disabled", true);
    fireEvent.submit(card.getByRole("form"));
    expect(fetchMock).toHaveBeenCalledTimes(1);
    expect(card.getByRole("link", { name: "開啟遠端桌面登入" }).getAttribute("href")).toBe(saved.desktop_url);
  });

  it("sends only changed fields and keeps a blank secret, using only the saved desktop URL", async () => {
    const fetchMock = vi.fn((_: RequestInfo | URL, init?: RequestInit) => Promise.resolve(Response.json(
      init?.method === "PUT" ? { ...saved, desktop_url: "https://desktop.example.test/vnc.html", updated_at: "2026-09-30T11:00:00Z" } : saved,
    )));
    vi.stubGlobal("fetch", fetchMock);
    const card = await mount();
    fireEvent.change(card.getByLabelText("遠端桌面網址"), { target: { value: "https://desktop.example.test/vnc.html" } });
    expect(card.getByRole("link", { name: "開啟遠端桌面登入" }).getAttribute("href")).toBe(saved.desktop_url);
    expect(card.getByRole("button", { name: "測試已儲存的連線" })).toHaveProperty("disabled", true);
    fireEvent.click(card.getByRole("button", { name: "儲存 VPS 設定" }));
    await card.findByText("VPS 設定已儲存。");
    const call = fetchMock.mock.calls.find(([, init]) => init?.method === "PUT")!;
    expect(call[0]).toBe(endpoint);
    expect(JSON.parse(String(call[1]?.body))).toEqual({ desktop_url: "https://desktop.example.test/vnc.html", expected_updated_at: saved.updated_at });
    expect(card.getByLabelText("服務密鑰")).toHaveProperty("value", "");
    expect(card.getByRole("link", { name: "開啟遠端桌面登入" }).getAttribute("href")).toBe("https://desktop.example.test/vnc.html");
  });

  it("requires a new secret for a new endpoint and clears it only after a successful save", async () => {
    const fetchMock = vi.fn((_: RequestInfo | URL, init?: RequestInit) => Promise.resolve(Response.json(
      init?.method === "PUT" ? { ...saved, url: "http://new-uploader:8789", updated_at: "2026-09-30T11:00:00Z" } : saved,
    )));
    vi.stubGlobal("fetch", fetchMock);
    const card = await mount();
    fireEvent.change(card.getByLabelText("服務網址"), { target: { value: "http://new-uploader:8789" } });
    expect(card.getByRole("button", { name: "儲存 VPS 設定" })).toHaveProperty("disabled", true);
    expect(card.getByText("變更服務網址時，請填入新服務的密鑰。")).toBeTruthy();
    const input = card.getByLabelText("服務密鑰");
    expect(input).toHaveProperty("type", "password");
    fireEvent.change(input, { target: { value: "s".repeat(32) } });
    fireEvent.click(card.getByRole("button", { name: "儲存 VPS 設定" }));
    await card.findByText("VPS 設定已儲存。");
    expect(JSON.parse(String(fetchMock.mock.calls.find(([, init]) => init?.method === "PUT")![1]?.body))).toEqual({ url: "http://new-uploader:8789", secret: "s".repeat(32), expected_updated_at: saved.updated_at });
    expect(input).toHaveProperty("value", "");
  });

  it("preserves every edit including the secret on 409, and reloads without overwriting unrelated concurrent changes", async () => {
    let reads = 0, writes = 0;
    const newer = { ...saved, desktop_url: "https://latest.example.test/vnc.html", updated_at: "2026-09-30T12:00:00Z" };
    const nextChannel = "UC" + "b".repeat(22);
    const fetchMock = vi.fn((_: RequestInfo | URL, init?: RequestInit) => {
      if (init?.method === "PUT") return Promise.resolve(++writes === 1
        ? Response.json({ code: "vps_settings_conflict", detail: "Version changed" }, { status: 409 })
        : Response.json({ ...newer, channel_id: nextChannel }));
      return Promise.resolve(Response.json(++reads === 1 ? saved : newer));
    });
    vi.stubGlobal("fetch", fetchMock);
    const card = await mount();
    fireEvent.change(card.getByLabelText("YouTube 頻道 ID"), { target: { value: nextChannel } });
    fireEvent.change(card.getByLabelText("服務密鑰"), { target: { value: "s".repeat(32) } });
    fireEvent.click(card.getByRole("button", { name: "儲存 VPS 設定" }));
    expect((await card.findByRole("alert")).textContent).toContain("你的修改已保留");
    expect(card.getByLabelText("服務密鑰")).toHaveProperty("value", "s".repeat(32));
    expect(card.getByLabelText("YouTube 頻道 ID")).toHaveProperty("value", nextChannel);
    fireEvent.click(card.getByRole("button", { name: "重新讀取已儲存設定" }));
    await card.findByText(/已讀取最新設定/);
    expect(card.getByLabelText("服務密鑰")).toHaveProperty("value", "s".repeat(32));
    expect(card.getByLabelText("遠端桌面網址")).toHaveProperty("value", newer.desktop_url);
    fireEvent.click(card.getByRole("button", { name: "儲存 VPS 設定" }));
    await card.findByText("VPS 設定已儲存。");
    const lastWrite = fetchMock.mock.calls.filter(([, init]) => init?.method === "PUT").at(-1)!;
    expect(JSON.parse(String(lastWrite[1]?.body))).toEqual({ channel_id: nextChannel, secret: "s".repeat(32), expected_updated_at: newer.updated_at });
    expect(card.getByLabelText("服務密鑰")).toHaveProperty("value", "");
  });

  it("tests the saved service without claiming Google sign-in", async () => {
    const fetchMock = vi.fn((url: RequestInfo | URL, init?: RequestInit) => Promise.resolve(Response.json(
      String(url).endsWith("/test") && init?.method === "POST" ? { ...saved, last_test_status: "success", last_tested_at: "2026-09-30T12:00:00Z", browser_status: "idle", active_jobs: 0 } : saved,
    )));
    vi.stubGlobal("fetch", fetchMock);
    const card = await mount();
    fireEvent.click(card.getByRole("button", { name: "測試已儲存的連線" }));
    await card.findByText("服務連線成功");
    expect(card.getByText(/連線測試成功不代表已登入 Google/)).toBeTruthy();
    expect(card.getByText(/背景工作狀態: 閒置/)).toBeTruthy();
    const post = fetchMock.mock.calls.find(([, init]) => init?.method === "POST")!;
    expect(post[0]).toBe(endpoint + "/test");
    expect(JSON.parse(String(post[1]?.body))).toEqual({});
  });

  it("shows a failed service test and permits a retry without changing settings", async () => {
    vi.stubGlobal("fetch", vi.fn((_: RequestInfo | URL, init?: RequestInit) => Promise.resolve(Response.json(
      init?.method === "POST" ? { ...saved, last_test_status: "failed", last_test_message: "Service unavailable" } : saved,
    ))));
    const card = await mount();
    fireEvent.click(card.getByRole("button", { name: "測試已儲存的連線" }));
    expect((await card.findByRole("alert")).textContent).toBe("服務連線失敗");
    expect(card.getByText("Service unavailable")).toBeTruthy();
    expect(card.queryByText("服務連線成功")).toBeNull();
    expect(card.getByRole("button", { name: "測試已儲存的連線" })).toHaveProperty("disabled", false);
  });

  it("keeps drafts and shows the API reason when an incomplete legacy setting prevents saving", async () => {
    const incomplete = { ...saved, configured: false, channel_id: "", source: "environment" };
    vi.stubGlobal("fetch", vi.fn((_: RequestInfo | URL, init?: RequestInit) => Promise.resolve(
      init?.method === "PUT"
        ? Response.json({ code: "vps_not_configured", detail: "The existing VPS configuration is incomplete" }, { status: 503 })
        : Response.json(incomplete),
    )));
    const card = await mount();
    expect(card.getByText("設定尚未完整")).toBeTruthy();
    fireEvent.click(card.getByLabelText("啟用 VPS 上傳"));
    fireEvent.change(card.getByLabelText("遠端桌面網址"), { target: { value: "https://desktop.example.test/vnc.html" } });
    fireEvent.change(card.getByLabelText("服務密鑰"), { target: { value: "s".repeat(32) } });
    fireEvent.click(card.getByRole("button", { name: "儲存 VPS 設定" }));
    expect((await card.findByRole("alert")).textContent).toBe("The existing VPS configuration is incomplete");
    expect(card.getByLabelText("啟用 VPS 上傳")).toHaveProperty("checked", false);
    expect(card.getByLabelText("遠端桌面網址")).toHaveProperty("value", "https://desktop.example.test/vnc.html");
    expect(card.getByLabelText("服務密鑰")).toHaveProperty("value", "s".repeat(32));
  });

  it.each(["http://10.1.2.3:6080/vnc.html", "http://172.16.0.1/vnc.html", "http://172.31.255.255/vnc.html", "http://192.168.1.20/vnc.html", "http://127.0.0.2/vnc.html", "http://[::1]:6080/vnc.html", "http://[fc00::1]/vnc.html", "http://[fdff::1]/vnc.html", "http://mokaair-studio-uploader:6080/vnc.html", "https://desktop.example.test/vnc.html"])("allows saved desktop addresses accepted by the private-service policy: %s", (url) => {
    expect(safeVpsDesktopUrl(url)).toBe(url);
  });

  it.each(["javascript:alert(1)", "http://public.example.test/vnc.html", "http://172.15.0.1/vnc.html", "http://172.32.0.1/vnc.html", "http://[fe80::1]/vnc.html", "https://user:pass@desktop.example.test/", "https://desktop.example.test/vnc.html?token=secret", "https://desktop.example.test/vnc.html#secret", "https://desktop.example.test\\vnc.html"])("never makes an unsafe desktop address clickable: %s", (url) => {
    expect(safeVpsDesktopUrl(url)).toBeNull();
  });
});
