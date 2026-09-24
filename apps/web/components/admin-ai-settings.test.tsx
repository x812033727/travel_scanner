import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { AdminAiSettings } from "./admin-ai-settings";
import { AdminOperationsProvider } from "./admin-operations-provider";
import type { AdminBootstrap } from "@/lib/admin-operations";

vi.mock("@/components/header-session", () => ({ useHeaderSession: () => ({ user: null, sessionIdentity: null, status: undefined }) }));

function bootstrap(capabilities: string[]): AdminBootstrap {
  return { admin_roles: [], admin_capabilities: capabilities, navigation: [], pending_counts: {}, system_status: {}, environment: "test", can_deploy: false, can_manage_database: false };
}

const accounts = { enabled: true, agent_reachable: true, slots: [], defaults: {}, allowlist_configured: true };
const settings = { encryption_source: "SETTINGS_ENCRYPTION_KEY", providers: [], audit: [] };

function stubFetch() {
  const fetchMock = vi.fn((input: RequestInfo | URL) => {
    const url = String(input);
    const body = url.includes("/admin/ai-accounts") ? accounts : settings;
    return Promise.resolve(new Response(JSON.stringify(body), { status: 200, headers: { "Content-Type": "application/json" } }));
  });
  vi.stubGlobal("fetch", fetchMock);
  return fetchMock;
}

const called = (fetchMock: ReturnType<typeof stubFetch>, part: string) => fetchMock.mock.calls.some(([input]) => String(input).includes(part));

afterEach(() => {
  vi.unstubAllGlobals();
  window.history.replaceState(null, "", "/");
});

describe("AdminAiSettings", () => {
  it("gives the owner both tabs, subscription accounts first", async () => {
    const fetchMock = stubFetch();
    render(<AdminOperationsProvider bootstrap={bootstrap(["roles.manage", "settings.read", "settings.manage"])}><AdminAiSettings /></AdminOperationsProvider>);
    const subscriptions = screen.getByRole("tab", { name: "訂閱帳號" });
    expect(subscriptions.getAttribute("aria-selected")).toBe("true");
    await waitFor(() => expect(called(fetchMock, "/admin/ai-accounts")).toBe(true));
    fireEvent.click(screen.getByRole("tab", { name: "API 金鑰與模型" }));
    await waitFor(() => expect(called(fetchMock, "/admin/provider-settings")).toBe(true));
    expect(window.location.search).toBe("?tab=api");
  });

  it("shows other settings readers the API tab alone and never asks for the accounts", async () => {
    window.history.replaceState(null, "", "/?tab=subscriptions");
    const fetchMock = stubFetch();
    render(<AdminOperationsProvider bootstrap={bootstrap(["settings.read"])}><AdminAiSettings /></AdminOperationsProvider>);
    expect(screen.queryByRole("tablist")).toBeNull();
    await waitFor(() => expect(called(fetchMock, "/admin/provider-settings")).toBe(true));
    expect(called(fetchMock, "/admin/ai-accounts")).toBe(false);
  });
});
