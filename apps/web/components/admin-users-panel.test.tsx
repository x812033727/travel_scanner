import {
  fireEvent,
  render,
  screen,
  waitFor,
  within,
} from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { AdminUsersPanel } from "./admin-users-panel";
import { AdminOperationsProvider } from "./admin-operations-provider";

const member = {
  id: "11111111-1111-4111-8111-111111111111",
  email: "member@example.com",
  is_active: true,
  is_admin: false,
  effective_is_admin: false,
  admin_source: "none",
  is_self: false,
  can_adjust_usage: true,
  last_activity_at: "2026-09-01T08:00:00Z",
  activity: {
    trips: 1,
    searches: 2,
    alerts: 1,
    community_posts: 0,
    community_comments: 0,
  },
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
  usage_history: [
    {
      id: "22222222-2222-4222-8222-222222222222",
      occurred_at: "2026-08-31T03:00:00Z",
      entry_type: "grant",
      status: "granted",
      change: 3,
      balance_after: 3,
      summary: "註冊贈送 3 次",
      reference: "trial:test",
    },
  ],
  admin_history: [],
};
const readOnlyBootstrap = {
  user: { id: "admin", email: "viewer@example.com" },
  admin_roles: ["viewer"],
  admin_capabilities: ["admin.access", "users.read"],
  navigation: [
    { key: "users", href: "/admin/users", group: "operations" as const },
  ],
  pending_counts: {},
  system_status: {},
  environment: "test",
  can_deploy: false,
  can_manage_database: false,
};

function response(payload: unknown, status = 200) {
  return new Response(JSON.stringify(payload), {
    status,
    headers: { "Content-Type": "application/json" },
  });
}

afterEach(() => {
  vi.unstubAllGlobals();
  vi.restoreAllMocks();
  window.history.replaceState(null, "", "/admin/users");
});

describe("AdminUsersPanel", () => {
  it("normalizes registration date filters only on the outbound API request", async () => {
    window.history.replaceState(
      null,
      "",
      "/admin/users?registered_from=2026-09-01&registered_to=2026-09-09",
    );
    const fetchMock = vi.fn().mockResolvedValue(response(list));
    vi.stubGlobal("fetch", fetchMock);
    render(<AdminUsersPanel />);
    await screen.findByText("member@example.com");
    const request = new URL(
      String(fetchMock.mock.calls[0][0]),
      "https://mokaair.test",
    );
    expect(request.searchParams.get("registered_from")).toBe(
      "2026-09-01T00:00:00.000Z",
    );
    expect(request.searchParams.get("registered_to")).toBe(
      "2026-09-09T23:59:59.999Z",
    );
    expect(window.location.search).toContain("registered_to=2026-09-09");
  });

  it("lists members and searches by email", async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(response(list))
      .mockResolvedValueOnce(response(list));
    vi.stubGlobal("fetch", fetchMock);
    render(<AdminUsersPanel />);

    expect(await screen.findByText("member@example.com")).toBeTruthy();
    expect(screen.getAllByText("7").length).toBeGreaterThan(0);
    fireEvent.change(screen.getByLabelText("搜尋 Email"), {
      target: { value: "member@" },
    });
    fireEvent.click(screen.getByRole("button", { name: "搜尋" }));

    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(2));
    expect(String(fetchMock.mock.calls[1][0])).toContain("query=member%40");
  });

  it("shows aggregated activity and keeps activity filters and sorting in the URL", async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(response(list))
      .mockResolvedValueOnce(response(list));
    vi.stubGlobal("fetch", fetchMock);
    render(<AdminUsersPanel />);

    const row = (await screen.findByText("member@example.com")).closest("tr")!;
    expect(within(row).getByText("4")).toBeTruthy();
    expect(within(row).getByText("1 旅程 · 2 搜尋 · 1 通知")).toBeTruthy();

    fireEvent.change(screen.getByLabelText("產品活動"), {
      target: { value: "has_activity" },
    });
    fireEvent.change(screen.getAllByLabelText("排序")[0], {
      target: { value: "last_activity_at" },
    });
    fireEvent.click(screen.getByRole("button", { name: "搜尋" }));

    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(2));
    const request = new URL(
      String(fetchMock.mock.calls[1][0]),
      "https://mokaair.test",
    );
    expect(request.searchParams.get("activity")).toBe("has_activity");
    expect(request.searchParams.get("sort")).toBe("last_activity_at");
    expect(window.location.search).toContain("activity=has_activity");
    expect(window.location.search).toContain("sort=last_activity_at");
  });

  it("labels members with no product activity instead of inventing activity", async () => {
    const quietMember = {
      ...member,
      id: "99999999-9999-4999-8999-999999999999",
      email: "quiet@example.com",
      activity: {
        trips: 0,
        searches: 0,
        alerts: 0,
        community_posts: 0,
        community_comments: 0,
      },
      last_activity_at: null,
    };
    const fetchMock = vi
      .fn()
      .mockResolvedValue(response({ ...list, items: [quietMember] }));
    vi.stubGlobal("fetch", fetchMock);
    render(<AdminUsersPanel />);

    const row = (await screen.findByText("quiet@example.com")).closest("tr")!;
    expect(within(row).getByText("尚無活動")).toBeTruthy();
  });

  it("uses the legacy account update only to reactivate an inactive account", async () => {
    const inactiveDetail = { ...detail, is_active: false, status: "inactive" };
    const activeDetail = { ...detail, is_active: true, status: "active" };
    const inactiveList = {
      ...list,
      items: [{ ...member, is_active: false, status: "inactive" }],
    };
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(response(inactiveList))
      .mockResolvedValueOnce(response(inactiveDetail))
      .mockResolvedValueOnce(response(activeDetail))
      .mockResolvedValueOnce(response(list));
    vi.stubGlobal("fetch", fetchMock);
    render(<AdminUsersPanel />);

    fireEvent.click(await screen.findByRole("button", { name: "管理" }));
    fireEvent.click(await screen.findByRole("button", { name: "重新啟用" }));

    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(4));
    const request = fetchMock.mock.calls[2][1] as RequestInit;
    expect(request.method).toBe("PUT");
    expect(JSON.parse(String(request.body))).toEqual({ is_active: true });
    expect(await screen.findByText("會員帳號已重新啟用。")).toBeTruthy();
  });

  it("does not expose the obsolete account-disable action for an active account", async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(response(list))
      .mockResolvedValueOnce(response({ ...detail, status: "active" }));
    vi.stubGlobal("fetch", fetchMock);
    render(<AdminUsersPanel />);
    fireEvent.click(await screen.findByRole("button", { name: "管理" }));
    await screen.findByRole("heading", { name: "停權管理" });
    expect(screen.queryByRole("button", { name: "停用帳號" })).toBeNull();
  });

  it("requires usage.manage even when the selected user is otherwise adjustable", async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(response(list))
      .mockResolvedValueOnce(response(detail));
    vi.stubGlobal("fetch", fetchMock);
    render(
      <AdminOperationsProvider bootstrap={readOnlyBootstrap}>
        <AdminUsersPanel />
      </AdminOperationsProvider>,
    );
    fireEvent.click(await screen.findByRole("button", { name: "管理" }));
    expect(
      await screen.findByRole("heading", { name: "人工調整使用次數" }),
    ).toBeTruthy();
    expect(
      (screen.getByLabelText("調整次數") as HTMLInputElement).disabled,
    ).toBe(true);
    expect(
      (screen.getByRole("button", { name: "寫入調整" }) as HTMLButtonElement)
        .disabled,
    ).toBe(true);
  });

  it("keeps suspension and session-revocation reasons independent", async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(response(list))
      .mockResolvedValueOnce(response(detail));
    vi.stubGlobal("fetch", fetchMock);
    render(<AdminUsersPanel />);
    fireEvent.click(await screen.findByRole("button", { name: "管理" }));
    const sessions = (
      await screen.findByRole("heading", { name: "登入工作階段" })
    ).closest("article")!;
    const revoke = within(sessions).getByRole("button", {
      name: "強制全部裝置登出",
    }) as HTMLButtonElement;
    expect(revoke.disabled).toBe(true);
    fireEvent.change(screen.getByLabelText("停權／解除原因"), {
      target: { value: "support review" },
    });
    expect(revoke.disabled).toBe(true);
    fireEvent.change(within(sessions).getByLabelText("操作原因"), {
      target: { value: "possible stolen session" },
    });
    expect(revoke.disabled).toBe(false);
  });

  it("clears and disables role expiry when owner is selected", async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(response(list))
      .mockResolvedValueOnce(response(detail));
    vi.stubGlobal("fetch", fetchMock);
    render(<AdminUsersPanel />);

    fireEvent.click(await screen.findByRole("button", { name: "管理" }));
    await screen.findAllByRole("heading", { name: "管理角色" });
    const expiry = screen.getByLabelText(
      "角色到期時間（選填）",
    ) as HTMLInputElement;
    fireEvent.change(expiry, { target: { value: "2026-10-01T12:00" } });
    expect(expiry.value).toBe("2026-10-01T12:00");

    fireEvent.click(screen.getByRole("checkbox", { name: "Owner" }));

    expect(expiry.value).toBe("");
    expect(expiry.disabled).toBe(true);
    expect(
      screen.getByText("Owner 是永久復原角色，不可設定到期時間。"),
    ).toBeTruthy();
  });

  it("rejects a timed suspension outside the 90-day safety window", async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(response(list))
      .mockResolvedValueOnce(response(detail));
    vi.stubGlobal("fetch", fetchMock);
    render(<AdminUsersPanel />);

    fireEvent.click(await screen.findByRole("button", { name: "管理" }));
    await screen.findByRole("heading", { name: "停權管理" });
    fireEvent.change(screen.getByLabelText("停權／解除原因"), {
      target: { value: "extended review" },
    });
    fireEvent.change(screen.getByLabelText(/^停權至（留空為永久）/), {
      target: { value: "2099-01-01T12:00" },
    });
    fireEvent.click(screen.getByRole("button", { name: "套用停權" }));

    expect(
      within(await screen.findByRole("alert")).getByText(
        "限時停權最多 90 天；更長期間請使用需密碼確認的永久停權。",
      ),
    ).toBeTruthy();
    expect(fetchMock).toHaveBeenCalledTimes(2);
  });

  it("clears the previous member and every mutation draft when browser history selects another user", async () => {
    const other = {
      ...member,
      id: "77777777-7777-4777-8777-777777777777",
      email: "other@example.com",
    };
    const otherDetail = { ...detail, ...other };
    const twoUsers = {
      ...list,
      items: [member, other],
      total: 2,
      stats: { ...list.stats, total: 2, active: 2 },
    };
    const fetchMock = vi.fn(async (input: string | URL | Request) => {
      const path = String(input);
      if (path.endsWith(`/admin/users/${member.id}`)) return response(detail);
      if (path.endsWith(`/admin/users/${other.id}`))
        return response(otherDetail);
      return response(twoUsers);
    });
    vi.stubGlobal("fetch", fetchMock);
    render(<AdminUsersPanel />);
    const memberRow = (await screen.findByText(member.email)).closest("tr")!;
    fireEvent.click(within(memberRow).getByRole("button", { name: "管理" }));
    await screen.findByRole("dialog", { name: member.email });
    fireEvent.change(screen.getByLabelText("調整次數"), {
      target: { value: "9" },
    });
    fireEvent.change(screen.getByLabelText("調整原因"), {
      target: { value: "draft for first member" },
    });

    const next = new URL(window.location.href);
    next.searchParams.set("user", other.id);
    window.history.pushState(null, "", next);
    window.dispatchEvent(new PopStateEvent("popstate"));
    await screen.findByRole("dialog", { name: other.email });
    expect((screen.getByLabelText("調整次數") as HTMLInputElement).value).toBe(
      "",
    );
    expect((screen.getByLabelText("調整原因") as HTMLInputElement).value).toBe(
      "",
    );
  });

  it("writes a signed usage adjustment with an idempotency key", async () => {
    const adjustedDetail = {
      ...detail,
      remaining_uses: 13,
      available_uses: 12,
      usage_history: [
        {
          ...detail.usage_history[0],
          entry_type: "admin_adjustment",
          change: 5,
          balance_after: 13,
          summary: "客服補償",
        },
      ],
    };
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(response(list))
      .mockResolvedValueOnce(response(detail))
      .mockResolvedValueOnce(
        response({
          user: adjustedDetail,
          change: 5,
          balance_after: 13,
          replayed: false,
        }),
      )
      .mockResolvedValueOnce(response({ ...list, items: [adjustedDetail] }));
    vi.stubGlobal("fetch", fetchMock);
    vi.spyOn(globalThis.crypto, "randomUUID").mockReturnValue(
      "33333333-3333-4333-8333-333333333333",
    );
    render(<AdminUsersPanel />);

    fireEvent.click(await screen.findByRole("button", { name: "管理" }));
    await screen.findByRole("heading", { name: "人工調整使用次數" });
    fireEvent.change(screen.getByLabelText("調整次數"), {
      target: { value: "5" },
    });
    fireEvent.change(screen.getByLabelText("調整原因"), {
      target: { value: "客服補償" },
    });
    fireEvent.click(screen.getByRole("button", { name: "寫入調整" }));

    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(4));
    const request = fetchMock.mock.calls[2][1] as RequestInit;
    expect(request.method).toBe("POST");
    expect(
      (request.headers as Record<string, string>)["Idempotency-Key"],
    ).toContain("33333333");
    expect(JSON.parse(String(request.body))).toEqual({
      change: 5,
      reason: "客服補償",
    });
    expect(await screen.findByText("增加 5 次，餘額為 13 次。")).toBeTruthy();
  });

  it("allows an environment administrator to adjust their own usage", async () => {
    const environmentSelf = {
      ...detail,
      id: "44444444-4444-4444-8444-444444444444",
      email: "environment-admin@example.com",
      is_admin: false,
      effective_is_admin: true,
      admin_source: "environment",
      is_self: true,
      can_adjust_usage: true,
    };
    const adjustedSelf = {
      ...environmentSelf,
      remaining_uses: 6,
      available_uses: 5,
      usage_history: [
        {
          ...detail.usage_history[0],
          entry_type: "admin_adjustment",
          change: -2,
          balance_after: 6,
          summary: "自助扣除次數",
        },
      ],
    };
    const environmentList = { ...list, items: [environmentSelf] };
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(response(environmentList))
      .mockResolvedValueOnce(response(environmentSelf))
      .mockResolvedValueOnce(
        response({
          user: adjustedSelf,
          change: -2,
          balance_after: 6,
          replayed: false,
        }),
      )
      .mockResolvedValueOnce(response({ ...list, items: [adjustedSelf] }));
    vi.stubGlobal("fetch", fetchMock);
    vi.spyOn(globalThis.crypto, "randomUUID").mockReturnValue(
      "55555555-5555-4555-8555-555555555555",
    );
    render(<AdminUsersPanel />);

    fireEvent.click(await screen.findByRole("button", { name: "管理" }));
    expect(
      await screen.findByText(
        "目前帳號由 ADMIN_EMAILS 授權，可調整自己的使用次數。",
      ),
    ).toBeTruthy();
    const changeInput = screen.getByLabelText("調整次數") as HTMLInputElement;
    expect(changeInput.disabled).toBe(false);
    fireEvent.change(changeInput, { target: { value: "-2" } });
    fireEvent.change(screen.getByLabelText("調整原因"), {
      target: { value: "自助扣除次數" },
    });
    fireEvent.click(screen.getByRole("button", { name: "寫入調整" }));

    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(4));
    const request = fetchMock.mock.calls[2][1] as RequestInit;
    expect(JSON.parse(String(request.body))).toEqual({
      change: -2,
      reason: "自助扣除次數",
    });
    expect(await screen.findByText("扣除 2 次，餘額為 6 次。")).toBeTruthy();
  });

  it("keeps self-adjustment disabled for a database administrator", async () => {
    const databaseSelf = {
      ...detail,
      id: "66666666-6666-4666-8666-666666666666",
      email: "database-admin@example.com",
      is_admin: true,
      effective_is_admin: true,
      admin_source: "database",
      is_self: true,
      can_adjust_usage: false,
    };
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(response({ ...list, items: [databaseSelf] }))
      .mockResolvedValueOnce(response(databaseSelf));
    vi.stubGlobal("fetch", fetchMock);
    render(<AdminUsersPanel />);

    fireEvent.click(await screen.findByRole("button", { name: "管理" }));
    expect(
      await screen.findByText(
        "不可調整目前管理員自己的次數，請由另一位管理員操作。",
      ),
    ).toBeTruthy();
    expect(
      (screen.getByLabelText("調整次數") as HTMLInputElement).disabled,
    ).toBe(true);
    expect(
      (screen.getByRole("button", { name: "寫入調整" }) as HTMLButtonElement)
        .disabled,
    ).toBe(true);
  });
});
