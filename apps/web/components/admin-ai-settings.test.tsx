import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { AdminAiSettings } from "./admin-ai-settings";
import { AdminOperationsProvider } from "./admin-operations-provider";
import type { AdminBootstrap } from "@/lib/admin-operations";

vi.mock("@/components/header-session", () => ({ useHeaderSession: () => ({ user: null, sessionIdentity: null, status: undefined }) }));

function bootstrap(capabilities: string[]): AdminBootstrap {
  return { admin_roles: [], admin_capabilities: capabilities, navigation: [], pending_counts: {}, system_status: {}, environment: "test", can_deploy: false, can_manage_database: false };
}

const accounts = { enabled: true, agent_reachable: true, slots: [], defaults: {}, allowlist_configured: true };
const card = (provider: string, label: string, config: Record<string, string | null>) => ({
  provider, label, description: label, enabled: true, configured: true, status: "ready", status_message: "ok",
  config, config_sources: Object.fromEntries(Object.keys(config).map((key) => [key, "admin"])), secrets: {}, field_options: {},
});
let settings = { encryption_source: "SETTINGS_ENCRYPTION_KEY", providers: [] as ReturnType<typeof card>[], audit: [] };

function stubFetch() {
  const fetchMock = vi.fn((input: RequestInfo | URL) => {
    const url = String(input);
    // The models tab also reads the news and video settings; each loads on its own. Answer
    // them like the isolated e2e fixture does, with a list-shaped 200 that is not settings.
    if (url.includes("/admin/news/") || url.includes("/admin/video-automation/")) return Promise.resolve(new Response(JSON.stringify({ items: [], total: 0, page: 1, pages: 0 }), { status: 200, headers: { "Content-Type": "application/json" } }));
    const body = url.includes("/admin/ai-accounts") ? accounts : settings;
    return Promise.resolve(new Response(JSON.stringify(body), { status: 200, headers: { "Content-Type": "application/json" } }));
  });
  vi.stubGlobal("fetch", fetchMock);
  return fetchMock;
}

const called = (fetchMock: ReturnType<typeof stubFetch>, part: string) => fetchMock.mock.calls.some(([input]) => String(input).includes(part));

afterEach(() => {
  settings = { ...settings, providers: [] };
  vi.unstubAllGlobals();
  window.history.replaceState(null, "", "/");
});

describe("AdminAiSettings", () => {
  it("gives the owner three tabs, subscription accounts first", async () => {
    const fetchMock = stubFetch();
    render(<AdminOperationsProvider bootstrap={bootstrap(["roles.manage", "settings.read", "settings.manage"])}><AdminAiSettings /></AdminOperationsProvider>);
    expect(screen.getAllByRole("tab").map((tab) => tab.textContent)).toEqual(["訂閱帳號", "API 金鑰", "各功能模型"]);
    expect(screen.getByRole("tab", { name: "訂閱帳號" }).getAttribute("aria-selected")).toBe("true");
    await waitFor(() => expect(called(fetchMock, "/admin/ai-accounts")).toBe(true));
    fireEvent.click(screen.getByRole("tab", { name: "API 金鑰" }));
    await waitFor(() => expect(called(fetchMock, "/admin/provider-settings")).toBe(true));
    expect(window.location.search).toBe("?tab=api");
    fireEvent.click(screen.getByRole("tab", { name: "各功能模型" }));
    expect(await screen.findByRole("heading", { name: "各功能目前用的模型" })).toBeTruthy();
    await waitFor(() => expect(called(fetchMock, "/admin/news/settings")).toBe(true));
    expect(called(fetchMock, "/admin/video-automation/settings")).toBe(true);
  });

  it("shows other settings readers the keys and models tabs and never asks for the accounts", async () => {
    window.history.replaceState(null, "", "/?tab=subscriptions");
    const fetchMock = stubFetch();
    render(<AdminOperationsProvider bootstrap={bootstrap(["settings.read"])}><AdminAiSettings /></AdminOperationsProvider>);
    expect(screen.getAllByRole("tab").map((tab) => tab.textContent)).toEqual(["API 金鑰", "各功能模型"]);
    expect(screen.getByRole("tab", { name: "API 金鑰" }).getAttribute("aria-selected")).toBe("true");
    await waitFor(() => expect(called(fetchMock, "/admin/provider-settings")).toBe(true));
    expect(called(fetchMock, "/admin/ai-accounts")).toBe(false);
  });

  it("opens an old keys-tab link to a model card on the models tab, and a tab click drops it", async () => {
    window.history.replaceState(null, "", "/?tab=api&provider=ai_planner&field=openai_model");
    stubFetch();
    render(<AdminOperationsProvider bootstrap={bootstrap(["settings.read"])}><AdminAiSettings /></AdminOperationsProvider>);
    expect(screen.getByRole("tab", { name: "各功能模型" }).getAttribute("aria-selected")).toBe("true");
    fireEvent.click(screen.getByRole("tab", { name: "API 金鑰" }));
    expect(window.location.search).toBe("?tab=api");
    expect(screen.getByRole("tab", { name: "API 金鑰" }).getAttribute("aria-selected")).toBe("true");
  });

  it("opens a feature's card from the overview without leaving the page", async () => {
    window.history.replaceState(null, "", "/zh-TW/admin/ai-accounts?tab=models");
    settings = { ...settings, providers: [
      card("ai_planner", "AI 行程規劃", { ai_planner_mode: "openai", openai_model: "gpt-6-sol" }),
      card("ai_guide_search", "AI 景點介紹搜尋", { hotspot_guide_ai_default_provider: "minimax", hotspot_guide_ai_minimax_model: null }),
    ] };
    stubFetch();
    render(<AdminOperationsProvider bootstrap={bootstrap(["settings.read"])}><AdminAiSettings /></AdminOperationsProvider>);
    const row = await waitFor(() => {
      const found = document.querySelector<HTMLElement>('[data-overview-row="guideSearch"]');
      if (!found) throw new Error("the overview has not loaded");
      return found;
    });
    expect(await screen.findByRole("heading", { name: "AI 行程規劃" })).toBeTruthy();
    fireEvent.click(within(row).getByRole("link", { name: "修改" }));
    expect(window.location.search).toBe("?tab=models&provider=ai_guide_search&field=hotspot_guide_ai_default_provider");
    expect(await screen.findByRole("heading", { name: "AI 景點介紹搜尋" })).toBeTruthy();
    expect(screen.getByRole("tab", { name: "各功能模型" }).getAttribute("aria-selected")).toBe("true");
    expect(screen.getByText(/讀不到：新聞設定、影片設定/)).toBeTruthy();
  });
});
