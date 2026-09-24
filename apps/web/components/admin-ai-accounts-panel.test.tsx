import { act, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { AdminAiAccountsPanel, nextFreeSlot, visibleAccounts, type AiAccount, type AiAccountsOverview } from "./admin-ai-accounts-panel";

const NOW = Date.parse("2026-09-24T09:00:00Z");
const seconds = (offset: number) => Math.round(NOW / 1000) + offset;

function account(tool: "claude" | "codex", slot: "a" | "b" | "c" | "d" | "e", values: Partial<AiAccount> = {}): AiAccount {
  return { tool, slot, is_default: slot === "a", logged_in: false, ...values };
}

function overview(values: Partial<AiAccountsOverview> = {}): AiAccountsOverview {
  const slots = (["claude", "codex"] as const).flatMap((tool) => (["a", "b", "c", "d", "e"] as const).map((slot) => account(tool, slot)));
  return { enabled: true, agent_reachable: true, slots, defaults: { claude: "a", codex: "a" }, allowlist_configured: true, ...values };
}

function withSlots(...changes: AiAccount[]) {
  const base = overview();
  return { ...base, slots: base.slots.map((item) => changes.find((change) => change.tool === item.tool && change.slot === item.slot) ?? item) };
}

function response(value: unknown, status = 200) {
  return Promise.resolve(new Response(JSON.stringify(value), { status, headers: { "Content-Type": "application/json" } }));
}

const login = (values: Record<string, unknown>) => ({ id: "0".repeat(32), tool: "codex", slot: "b", kind: "device_code", status: "pending", url: "https://auth.openai.com/codex/device", user_code: "ABCD-EFGH", error: null, expires_at: seconds(900), ...values });

afterEach(() => {
  vi.useRealTimers();
  vi.restoreAllMocks();
  vi.unstubAllGlobals();
});

describe("visible accounts", () => {
  it("lists signed-in, default and in-progress slots and offers the next free one", () => {
    const accounts = [
      account("codex", "a", { logged_in: true }),
      account("codex", "b"),
      account("codex", "c", { login: login({ slot: "c" }) as AiAccount["login"] }),
      account("codex", "d", { logged_in: null, error: "timeout" }),
      account("codex", "e"),
    ];
    expect(visibleAccounts(accounts).map((item) => item.slot)).toEqual(["a", "c", "d"]);
    expect(nextFreeSlot(accounts)).toBe("b");
    expect(nextFreeSlot(accounts.map((item) => ({ ...item, logged_in: true })))).toBeUndefined();
  });
});

describe("AdminAiAccountsPanel", () => {
  it("shows each account's email, plan and remaining quota", async () => {
    vi.spyOn(Date, "now").mockReturnValue(NOW);
    const state = withSlots(
      account("codex", "a", { logged_in: true, auth_method: "chatgpt", email: "owner@example.com", plan: "pro", usage: { source: "live", windows: [{ window_minutes: 10080, used_percent: 100, resets_at: seconds(212_530) }] } }),
      account("claude", "a", { logged_in: true, auth_method: "claude.ai", email: "owner@example.com", plan: "max", recorder_installed: true, usage: { source: "snapshot", recorded_at: seconds(-300), windows: [{ window_minutes: 300, used_percent: 23.5, resets_at: seconds(3_600) }, { window_minutes: 10080, used_percent: 41, resets_at: seconds(-60) }] } }),
      account("claude", "b", { logged_in: true, auth_method: "console", email: "api@example.com", email_allowed: false }),
    );
    vi.stubGlobal("fetch", vi.fn(() => response(state)));
    render(<AdminAiAccountsPanel />);

    const codex = await screen.findByRole("article", { name: "Codex 帳號 A" });
    expect(within(codex).getByText("owner@example.com")).toBeTruthy();
    expect(within(codex).getByText("Pro")).toBeTruthy();
    expect(within(codex).getByText("每週額度")).toBeTruthy();
    expect(within(codex).getByText("剩餘 0%")).toBeTruthy();
    expect(within(codex).getByText("預設")).toBeTruthy();

    const claude = screen.getByRole("article", { name: "Claude Code 帳號 A" });
    expect(within(claude).getByText("Max")).toBeTruthy();
    expect(within(claude).getByText("5 小時額度")).toBeTruthy();
    // 100 - 23.5, rounded; the weekly window's reset time has passed.
    expect(within(claude).getByText("剩餘 77%")).toBeTruthy();
    expect(within(claude).getByText("剩餘 100%")).toBeTruthy();
    expect(within(claude).getByText("已重置")).toBeTruthy();

    const second = screen.getByRole("article", { name: "Claude Code 帳號 B" });
    expect(within(second).getByText("這個帳號走 API 計費，不是訂閱")).toBeTruthy();
    expect(within(second).getByText("這個帳號不在主機允許的清單內")).toBeTruthy();
    expect(within(second).getByRole("button", { name: "設為預設" })).toBeTruthy();
    expect(screen.getAllByText("會使用下一個空位：帳號 C")).toHaveLength(1);
  });

  it("explains a disabled page and an unreachable agent", async () => {
    vi.stubGlobal("fetch", vi.fn(() => response(overview({ enabled: false, agent_reachable: false, slots: [] }))));
    const { unmount } = render(<AdminAiAccountsPanel />);
    expect(await screen.findByText("AI 帳號管理尚未啟用")).toBeTruthy();
    unmount();
    vi.stubGlobal("fetch", vi.fn(() => response(overview({ agent_reachable: false, agent_error: "socket missing", slots: [] }))));
    render(<AdminAiAccountsPanel />);
    expect(await screen.findByText("連不上主機上的 AI 帳號代理：socket missing")).toBeTruthy();
  });

  it("walks a Codex device-code login from the next free slot to success", async () => {
    vi.useFakeTimers({ shouldAdvanceTime: true });
    let polls = 0;
    const fetchMock = vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      if (url.endsWith("/admin/ai-accounts/codex/b/login") && init?.method === "POST") return response(login({}), 201);
      if (url.endsWith(`/admin/ai-accounts/logins/${"0".repeat(32)}`)) {
        polls += 1;
        return response(login({ status: polls > 1 ? "succeeded" : "pending" }));
      }
      if (url.includes("/admin/ai-accounts")) return response(overview());
      throw new Error(`unexpected ${url}`);
    });
    vi.stubGlobal("fetch", fetchMock);
    render(<AdminAiAccountsPanel />);
    await act(async () => { await vi.advanceTimersByTimeAsync(10); });
    const codexSection = await screen.findByRole("region", { name: "Codex" });
    fireEvent.click(within(codexSection).getByRole("button", { name: "新增帳號" }));

    const dialog = await screen.findByRole("dialog", { name: "登入 Codex（帳號 B）" });
    expect(within(dialog).getByText("ABCD-EFGH")).toBeTruthy();
    expect(within(dialog).getByRole("link", { name: /開啟登入頁/ }).getAttribute("href")).toBe("https://auth.openai.com/codex/device");
    await act(async () => { await vi.advanceTimersByTimeAsync(3_100); });
    await act(async () => { await vi.advanceTimersByTimeAsync(3_100); });
    await waitFor(() => expect(within(dialog).getByText("登入完成。")).toBeTruthy());
    expect(within(dialog).queryByText("ABCD-EFGH")).toBeNull();
    expect(fetchMock).toHaveBeenCalledWith("/api/travel/admin/ai-accounts?fresh=true", expect.anything());
  });

  it("sends a pasted Claude code trimmed and only when it looks like one", async () => {
    const fetchMock = vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      if (url.endsWith("/admin/ai-accounts/claude/a/login")) return response(login({ tool: "claude", slot: "a", kind: "paste_code", url: "https://claude.com/cai/oauth/authorize?code=true", user_code: null }), 201);
      if (url.endsWith("/code") && init?.method === "POST") return response(login({ tool: "claude", slot: "a", kind: "paste_code", status: "verifying", url: null, user_code: null }), 202);
      if (url.includes("/admin/ai-accounts")) return response(overview());
      throw new Error(`unexpected ${url}`);
    });
    vi.stubGlobal("fetch", fetchMock);
    render(<AdminAiAccountsPanel />);
    const claude = await screen.findByRole("article", { name: "Claude Code 帳號 A" });
    fireEvent.click(within(claude).getByRole("button", { name: "登入" }));
    const dialog = await screen.findByRole("dialog", { name: "登入 Claude Code（帳號 A）" });
    const field = within(dialog).getByLabelText("授權後頁面會顯示一段代碼，複製後貼在這裡：");
    const submit = within(dialog).getByRole("button", { name: "送出代碼" });
    fireEvent.change(field, { target: { value: "not a code" } });
    expect((submit as HTMLButtonElement).disabled).toBe(true);
    fireEvent.change(field, { target: { value: "  AbC_-123.~#state-Part  " } });
    fireEvent.click(submit);
    await waitFor(() => expect(within(dialog).getByText("正在驗證…")).toBeTruthy());
    const post = fetchMock.mock.calls.find(([input]) => String(input).endsWith("/code"));
    expect(JSON.parse(String(post?.[1]?.body))).toEqual({ code: "AbC_-123.~#state-Part" });
  });

  it("asks before signing out and switches the default", async () => {
    const state = withSlots(
      account("codex", "a", { logged_in: true, email: "a@example.com" }),
      account("codex", "b", { logged_in: true, email: "b@example.com" }),
    );
    const fetchMock = vi.fn((_input: RequestInfo | URL, init?: RequestInit) => {
      if (init?.method === "PUT") return response({ defaults: { claude: "a", codex: "b" } });
      if (init?.method === "POST") return response({ tool: "codex", slot: "b", logged_in: false });
      return response(state);
    });
    vi.stubGlobal("fetch", fetchMock);
    render(<AdminAiAccountsPanel />);
    const second = await screen.findByRole("article", { name: "Codex 帳號 B" });
    fireEvent.click(within(second).getByRole("button", { name: "設為預設" }));
    await waitFor(() => expect(fetchMock).toHaveBeenCalledWith("/api/travel/admin/ai-accounts/defaults/codex", expect.objectContaining({ method: "PUT", body: JSON.stringify({ slot: "b" }) })));
    fireEvent.click(within(second).getByRole("button", { name: "登出" }));
    expect(fetchMock.mock.calls.some(([input]) => String(input).endsWith("/logout"))).toBe(false);
    fireEvent.click(within(second).getByRole("button", { name: "確認登出" }));
    await waitFor(() => expect(fetchMock.mock.calls.some(([input]) => String(input).endsWith("/admin/ai-accounts/codex/b/logout"))).toBe(true));
  });
});
