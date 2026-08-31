import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { AdminUsersPanel } from "./admin-users-panel";

const member = {
  id: "11111111-1111-4111-8111-111111111111",
  email: "member@example.com",
  is_active: true,
  is_admin: false,
  effective_is_admin: false,
  admin_source: "none",
  is_self: false,
  remaining_uses: 8,
  reserved_uses: 1,
  available_uses: 7,
  created_at: "2026-08-31T03:00:00Z",
  updated_at: "2026-08-31T03:00:00Z",
};
const list = {
  items: [member],
  page: 1,
  limit: 20,
  total: 1,
  pages: 1,
  stats: { total: 1, active: 1, administrators: 0, available_uses: 7 },
};
const detail = {
  ...member,
  usage_history: [{
    id: "22222222-2222-4222-8222-222222222222",
    occurred_at: "2026-08-31T03:00:00Z",
    entry_type: "grant",
    status: "granted",
    change: 3,
    balance_after: 3,
    summary: "註冊贈送 3 次",
    reference: "trial:test",
  }],
  admin_history: [],
};

function response(payload: unknown, status = 200) {
  return new Response(JSON.stringify(payload), { status, headers: { "Content-Type": "application/json" } });
}

afterEach(() => {
  vi.unstubAllGlobals();
  vi.restoreAllMocks();
});

describe("AdminUsersPanel", () => {
  it("lists members and searches by email", async () => {
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(response(list))
      .mockResolvedValueOnce(response(list));
    vi.stubGlobal("fetch", fetchMock);
    render(<AdminUsersPanel />);

    expect(await screen.findByText("member@example.com")).toBeTruthy();
    expect(screen.getAllByText("7").length).toBeGreaterThan(0);
    fireEvent.change(screen.getByLabelText("搜尋 Email"), { target: { value: "member@" } });
    fireEvent.click(screen.getByRole("button", { name: "搜尋" }));

    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(2));
    expect(String(fetchMock.mock.calls[1][0])).toContain("query=member%40");
  });

  it("updates account status and refreshes the list", async () => {
    const disabledDetail = { ...detail, is_active: false };
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(response(list))
      .mockResolvedValueOnce(response(detail))
      .mockResolvedValueOnce(response(disabledDetail))
      .mockResolvedValueOnce(response({ ...list, items: [{ ...member, is_active: false }] }));
    vi.stubGlobal("fetch", fetchMock);
    render(<AdminUsersPanel />);

    fireEvent.click(await screen.findByRole("button", { name: "管理" }));
    fireEvent.click(await screen.findByRole("button", { name: "停用帳號" }));

    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(4));
    const request = fetchMock.mock.calls[2][1] as RequestInit;
    expect(request.method).toBe("PUT");
    expect(JSON.parse(String(request.body))).toEqual({ is_active: false });
    expect(await screen.findByText("會員帳號已停用。")).toBeTruthy();
  });

  it("writes a signed usage adjustment with an idempotency key", async () => {
    const adjustedDetail = {
      ...detail,
      remaining_uses: 13,
      available_uses: 12,
      usage_history: [{
        ...detail.usage_history[0],
        entry_type: "admin_adjustment",
        change: 5,
        balance_after: 13,
        summary: "客服補償",
      }],
    };
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(response(list))
      .mockResolvedValueOnce(response(detail))
      .mockResolvedValueOnce(response({
        user: adjustedDetail,
        change: 5,
        balance_after: 13,
        replayed: false,
      }))
      .mockResolvedValueOnce(response({ ...list, items: [adjustedDetail] }));
    vi.stubGlobal("fetch", fetchMock);
    vi.spyOn(globalThis.crypto, "randomUUID").mockReturnValue("33333333-3333-4333-8333-333333333333");
    render(<AdminUsersPanel />);

    fireEvent.click(await screen.findByRole("button", { name: "管理" }));
    await screen.findByRole("heading", { name: "人工調整使用次數" });
    fireEvent.change(screen.getByLabelText("調整次數"), { target: { value: "5" } });
    fireEvent.change(screen.getByLabelText("調整原因"), { target: { value: "客服補償" } });
    fireEvent.click(screen.getByRole("button", { name: "寫入調整" }));

    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(4));
    const request = fetchMock.mock.calls[2][1] as RequestInit;
    expect(request.method).toBe("POST");
    expect((request.headers as Record<string, string>)["Idempotency-Key"]).toContain("33333333");
    expect(JSON.parse(String(request.body))).toEqual({ change: 5, reason: "客服補償" });
    expect(await screen.findByText("增加 5 次，餘額為 13 次。")).toBeTruthy();
  });
});
