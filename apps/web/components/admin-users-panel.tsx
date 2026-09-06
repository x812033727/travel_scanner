"use client";

import {
  ChevronLeft,
  ChevronRight,
  LoaderCircle,
  Search,
  ShieldCheck,
  UserCog,
  WalletCards,
  X,
} from "lucide-react";
import { useTranslations } from "next-intl";
import { FormEvent, useEffect, useState } from "react";
import { api } from "@/lib/api";

type UserSummary = {
  id: string;
  email: string;
  is_active: boolean;
  is_admin: boolean;
  effective_is_admin: boolean;
  admin_source: string;
  is_self: boolean;
  can_adjust_usage: boolean;
  remaining_uses: number;
  reserved_uses: number;
  available_uses: number;
  created_at: string;
  updated_at: string;
};
type UsageHistory = {
  id: string;
  occurred_at: string;
  entry_type: string;
  status: string;
  change: number;
  balance_after: number;
  summary: string;
  reference: string;
};
type AdminHistory = {
  id: string;
  action: string;
  metadata: Record<string, unknown>;
  created_at: string;
};
type UserDetail = UserSummary & {
  usage_history: UsageHistory[];
  admin_history: AdminHistory[];
};
type UserList = {
  items: UserSummary[];
  page: number;
  limit: number;
  total: number;
  pages: number;
  stats: {
    total: number;
    active: number;
    administrators: number;
    available_uses: number;
  };
};
type AdjustmentResult = {
  user: UserDetail;
  change: number;
  balance_after: number;
  replayed: boolean;
};

const dateTime = new Intl.DateTimeFormat("zh-TW", {
  dateStyle: "medium",
  timeStyle: "short",
});
const integer = new Intl.NumberFormat("zh-TW");
const entryLabel: Record<string, string> = {
  grant: "註冊贈送",
  package_grant: "次數包",
  use: "使用服務",
  admin_adjustment: "後台調整",
};
const auditLabel: Record<string, string> = {
  user_account_updated: "帳號設定變更",
  user_usage_adjusted: "使用次數調整",
  "admin_role.updated": "管理員權限變更",
};

function roleText(user: UserSummary) {
  if (!user.effective_is_admin) return "一般會員";
  return user.admin_source === "environment" ? "環境管理員" : "管理員";
}

export function AdminUsersPanel() {
  const [data, setData] = useState<UserList>();
  const tAdmin = useTranslations("admin");
  const [query, setQuery] = useState("");
  const [submittedQuery, setSubmittedQuery] = useState("");
  const [page, setPage] = useState(1);
  const [selected, setSelected] = useState<UserDetail>();
  const [loading, setLoading] = useState(true);
  const [detailLoading, setDetailLoading] = useState(false);
  const [busy, setBusy] = useState(false);
  // Disabling an account or stripping admin rights is one tap in a table an
  // owner works through on a phone; arm the button first so a stray thumb
  // cannot do it by accident.
  const [armedAction, setArmedAction] = useState<"disable" | "admin" | null>(null);
  const [error, setError] = useState<string>();
  const [notice, setNotice] = useState<string>();
  const [usageChange, setUsageChange] = useState("");
  const [usageReason, setUsageReason] = useState("");

  function usersPath() {
    const params = new URLSearchParams({ page: String(page), limit: "20" });
    if (submittedQuery) params.set("query", submittedQuery);
    return `/admin/users?${params}`;
  }

  async function loadUsers() {
    setLoading(true);
    setError(undefined);
    try {
      setData(await api<UserList>(usersPath()));
    } catch (reason) {
      setError((reason as Error).message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    let active = true;
    const params = new URLSearchParams({ page: String(page), limit: "20" });
    if (submittedQuery) params.set("query", submittedQuery);
    api<UserList>(`/admin/users?${params}`)
      .then((result) => {
        if (active) setData(result);
      })
      .catch((reason: Error) => {
        if (active) setError(reason.message);
      })
      .finally(() => {
        if (active) setLoading(false);
      });
    return () => {
      active = false;
    };
  }, [page, submittedQuery]);

  function submitSearch(event: FormEvent) {
    event.preventDefault();
    setLoading(true);
    setError(undefined);
    const nextQuery = query.trim();
    if (page === 1 && submittedQuery === nextQuery) {
      void loadUsers();
      return;
    }
    setPage(1);
    setSubmittedQuery(nextQuery);
  }

  async function openUser(userId: string) {
    setDetailLoading(true);
    setError(undefined);
    setNotice(undefined);
    try {
      setSelected(await api<UserDetail>(`/admin/users/${userId}`));
    } catch (reason) {
      setError((reason as Error).message);
    } finally {
      setDetailLoading(false);
    }
  }

  useEffect(() => {
    if (!armedAction) return;
    const timer = window.setTimeout(() => setArmedAction(null), 5_000);
    return () => window.clearTimeout(timer);
  }, [armedAction]);

  async function updateAccount(
    patch: { is_active?: boolean; is_admin?: boolean },
    message: string,
  ) {
    if (!selected) return;
    setBusy(true);
    setError(undefined);
    setNotice(undefined);
    try {
      const updated = await api<UserDetail>(`/admin/users/${selected.id}`, {
        method: "PUT",
        body: JSON.stringify(patch),
      });
      setSelected(updated);
      setNotice(message);
      await loadUsers();
    } catch (reason) {
      setError((reason as Error).message);
    } finally {
      setBusy(false);
    }
  }

  async function adjustUsage(event: FormEvent) {
    event.preventDefault();
    if (!selected) return;
    const change = Number(usageChange);
    if (!Number.isInteger(change) || change === 0) {
      setError("請輸入非 0 的整數；正數增加、負數扣除。");
      return;
    }
    setBusy(true);
    setError(undefined);
    setNotice(undefined);
    try {
      const result = await api<AdjustmentResult>(
        `/admin/users/${selected.id}/usage-adjustments`,
        {
          method: "POST",
          headers: { "Idempotency-Key": `admin-${crypto.randomUUID()}` },
          body: JSON.stringify({ change, reason: usageReason }),
        },
      );
      setSelected(result.user);
      setUsageChange("");
      setUsageReason("");
      setNotice(
        `${change > 0 ? "增加" : "扣除"} ${integer.format(Math.abs(change))} 次，餘額為 ${integer.format(result.balance_after)} 次。`,
      );
      await loadUsers();
    } catch (reason) {
      setError((reason as Error).message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="mt-8 space-y-6">
      {error && (
        <p
          role="alert"
          className="rounded-xl bg-red-50 p-4 text-sm text-red-800"
        >
          {error}
        </p>
      )}
      {notice && (
        <p
          role="status"
          className="rounded-xl bg-emerald-50 p-4 text-sm text-emerald-800"
        >
          {notice}
        </p>
      )}

      {data && (
        <section
          aria-label="會員統計"
          className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4"
        >
          {[
            ["會員總數", data.stats.total],
            ["啟用帳號", data.stats.active],
            ["管理員", data.stats.administrators],
            ["可用總次數", data.stats.available_uses],
          ].map(([label, value]) => (
            <div
              key={String(label)}
              className="rounded-2xl border border-[var(--line)] bg-white p-5"
            >
              <p className="text-xs font-semibold text-[var(--muted)]">
                {label}
              </p>
              <p className="mt-2 text-3xl font-bold">
                {integer.format(Number(value))}
              </p>
            </div>
          ))}
        </section>
      )}

      <section className="rounded-[1.75rem] border border-[var(--line)] bg-white p-5 shadow-sm md:p-7">
        <div className="flex flex-col justify-between gap-4 md:flex-row md:items-end">
          <div>
            <h2 className="text-xl font-bold">會員清單</h2>
            <p className="mt-1 text-sm text-[var(--muted)]">
              Email 搜尋支援部分文字，結果依註冊時間排序。
            </p>
          </div>
          <form onSubmit={submitSearch} className="flex w-full max-w-md gap-2">
            <label className="sr-only" htmlFor="member-query">
              搜尋 Email
            </label>
            <input
              id="member-query"
              type="search"
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              placeholder="搜尋 Email"
              className="min-w-0 flex-1 rounded-xl border border-[var(--line)] px-4 py-3"
            />
            <button
              type="submit"
              className="flex items-center gap-2 rounded-xl bg-[var(--ink)] px-4 py-3 text-sm font-semibold text-white"
            >
              <Search size={16} />
              搜尋
            </button>
          </form>
        </div>

        {loading ? (
          <p className="mt-8 flex items-center gap-2 text-sm text-[var(--muted)]">
            <LoaderCircle size={17} className="animate-spin" />
            正在讀取會員…
          </p>
        ) : data?.items?.length ? (
          <div className="mt-6 overflow-x-auto">
              <table className="admin-responsive-table admin-users-table w-full min-w-[840px] text-left text-sm">
              <thead>
                <tr className="border-b border-[var(--line)] text-xs text-[var(--muted)]">
                  <th className="px-3 py-3">會員</th>
                  <th className="px-3 py-3">狀態</th>
                  <th className="px-3 py-3">權限</th>
                  <th className="px-3 py-3">次數</th>
                  <th className="px-3 py-3">註冊時間</th>
                  <th className="px-3 py-3 text-right">操作</th>
                </tr>
              </thead>
              <tbody>
                {data.items?.map((user) => (
                  <tr
                    key={user.id}
                    className="border-b border-[var(--line)] last:border-0"
                  >
                    <td className="px-3 py-4">
                      <p className="font-semibold">{user.email}</p>
                      {user.is_self && (
                        <span className="text-xs text-[var(--teal)]">
                          目前帳號
                        </span>
                      )}
                    </td>
                    <td className="px-3 py-4">
                      <span
                        className={`rounded-full px-2.5 py-1 text-xs font-semibold ${user.is_active ? "bg-emerald-50 text-emerald-800" : "bg-slate-100 text-slate-700"}`}
                      >
                        {user.is_active ? "啟用" : "停用"}
                      </span>
                    </td>
                    <td className="px-3 py-4">{roleText(user)}</td>
                    <td className="px-3 py-4">
                      <strong>{integer.format(user.available_uses)}</strong>{" "}
                      可用
                      {user.reserved_uses > 0 && (
                        <span className="ml-1 text-xs text-[var(--muted)]">
                          （保留 {user.reserved_uses}）
                        </span>
                      )}
                    </td>
                    <td className="px-3 py-4 text-[var(--muted)]">
                      {dateTime.format(new Date(user.created_at))}
                    </td>
                    <td className="px-3 py-4 text-right">
                      <button
                        type="button"
                        onClick={() => openUser(user.id)}
                        className="rounded-lg border border-[var(--line)] px-3 py-2 font-semibold hover:bg-[var(--paper)]"
                      >
                        管理
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <p className="mt-6 rounded-xl bg-[var(--paper)] p-6 text-sm text-[var(--muted)]">
            沒有符合條件的會員。
          </p>
        )}

        {data && (
          <div className="mt-5 flex items-center justify-between text-sm">
            <span className="text-[var(--muted)]">
              第 {data.page} / {data.pages} 頁，共 {data.total} 位
            </span>
            <div className="flex gap-2">
              <button
                type="button"
                aria-label="上一頁"
                disabled={page <= 1 || loading}
                onClick={() => {
                  setLoading(true);
                  setPage((current) => current - 1);
                }}
                className="rounded-lg border border-[var(--line)] p-2 disabled:opacity-40"
              >
                <ChevronLeft size={17} />
              </button>
              <button
                type="button"
                aria-label="下一頁"
                disabled={page >= data.pages || loading}
                onClick={() => {
                  setLoading(true);
                  setPage((current) => current + 1);
                }}
                className="rounded-lg border border-[var(--line)] p-2 disabled:opacity-40"
              >
                <ChevronRight size={17} />
              </button>
            </div>
          </div>
        )}
      </section>

      {detailLoading && (
        <p className="flex items-center gap-2 text-sm text-[var(--muted)]">
          <LoaderCircle size={17} className="animate-spin" />
          正在讀取會員詳細資料…
        </p>
      )}
      {selected && (
        <section
          aria-labelledby="member-detail-title"
          className="rounded-[1.75rem] border border-[var(--line)] bg-white p-5 shadow-sm md:p-7"
        >
          <div className="flex items-start justify-between gap-4">
            <div>
              <p className="text-xs font-semibold tracking-[.12em] text-[var(--teal)]">
                MEMBER DETAIL
              </p>
              <h2
                id="member-detail-title"
                className="mt-1 break-all text-2xl font-bold"
              >
                {selected.email}
              </h2>
              <p className="mt-1 text-sm text-[var(--muted)]">
                註冊於 {dateTime.format(new Date(selected.created_at))}
              </p>
            </div>
            <button
              type="button"
              aria-label="關閉會員詳細資料"
              onClick={() => setSelected(undefined)}
              className="rounded-lg border border-[var(--line)] p-2"
            >
              <X size={18} />
            </button>
          </div>

          <div className="mt-6 grid gap-4 md:grid-cols-3">
            <div className="rounded-2xl bg-[var(--paper)] p-5">
              <UserCog size={20} className="text-[var(--teal)]" />
              <p className="mt-3 text-xs text-[var(--muted)]">帳號狀態</p>
              <p className="mt-1 font-bold">
                {selected.is_active ? "啟用" : "停用"}
              </p>
              <button
                type="button"
                disabled={busy || selected.is_self}
                onClick={() => {
                  if (selected.is_active && armedAction !== "disable") {
                    setArmedAction("disable");
                    return;
                  }
                  setArmedAction(null);
                  void updateAccount(
                    { is_active: !selected.is_active },
                    selected.is_active
                      ? "會員帳號已停用。"
                      : "會員帳號已重新啟用。",
                  );
                }}
                className={`mt-4 w-full rounded-xl border px-3 py-2 text-sm font-semibold disabled:opacity-40 ${armedAction === "disable" ? "border-red-300 bg-red-50 text-red-800" : "border-[var(--line)]"}`}
              >
                {armedAction === "disable" ? tAdmin("usersPanel.confirmDisable") : selected.is_active ? "停用帳號" : "重新啟用"}
              </button>
              {selected.is_self && (
                <p className="mt-2 text-xs text-[var(--muted)]">
                  不可停用目前帳號。
                </p>
              )}
            </div>
            <div className="rounded-2xl bg-[var(--paper)] p-5">
              <ShieldCheck size={20} className="text-[var(--coral)]" />
              <p className="mt-3 text-xs text-[var(--muted)]">系統權限</p>
              <p className="mt-1 font-bold">{roleText(selected)}</p>
              <button
                type="button"
                disabled={
                  busy ||
                  selected.is_self ||
                  selected.admin_source === "environment"
                }
                onClick={() => {
                  if (selected.is_admin && armedAction !== "admin") {
                    setArmedAction("admin");
                    return;
                  }
                  setArmedAction(null);
                  void updateAccount(
                    { is_admin: !selected.is_admin },
                    selected.is_admin
                      ? "管理員權限已移除。"
                      : "管理員權限已授予。",
                  );
                }}
                className={`mt-4 w-full rounded-xl border px-3 py-2 text-sm font-semibold disabled:opacity-40 ${armedAction === "admin" ? "border-red-300 bg-red-50 text-red-800" : "border-[var(--line)]"}`}
              >
                {armedAction === "admin" ? tAdmin("usersPanel.confirmRemoveAdmin") : selected.is_admin ? "移除管理員" : "設為管理員"}
              </button>
              {selected.admin_source === "environment" && (
                <p className="mt-2 text-xs text-[var(--muted)]">
                  由 ADMIN_EMAILS 管理。
                </p>
              )}
            </div>
            <div className="rounded-2xl bg-[var(--paper)] p-5">
              <WalletCards size={20} className="text-[var(--teal)]" />
              <p className="mt-3 text-xs text-[var(--muted)]">可用／保留次數</p>
              <p className="mt-1 text-2xl font-bold">
                {integer.format(selected.available_uses)}{" "}
                <span className="text-sm font-normal text-[var(--muted)]">
                  ／ {integer.format(selected.reserved_uses)}
                </span>
              </p>
              <p className="mt-4 text-xs text-[var(--muted)]">
                帳面餘額 {integer.format(selected.remaining_uses)}{" "}
                次；扣除時不得低於保留次數。
              </p>
            </div>
          </div>

          <form
            onSubmit={adjustUsage}
            className="mt-6 rounded-2xl border border-[var(--line)] p-5"
          >
            <h3 className="font-bold">人工調整使用次數</h3>
            <p className="mt-1 text-sm text-[var(--muted)]">
              正數增加、負數扣除；原因及操作人會永久寫入帳本。
            </p>
            {selected.is_self &&
              (selected.can_adjust_usage ? (
                <p className="mt-2 text-xs font-semibold text-[var(--teal)]">
                  目前帳號由 ADMIN_EMAILS 授權，可調整自己的使用次數。
                </p>
              ) : (
                <p className="mt-2 text-xs font-semibold text-[var(--coral)]">
                  不可調整目前管理員自己的次數，請由另一位管理員操作。
                </p>
              ))}
            <div className="mt-4 grid gap-4 md:grid-cols-[10rem_1fr_auto]">
              <label className="text-sm font-semibold">
                調整次數
                <input
                  type="number"
                  required
                  step="1"
                  min="-10000"
                  max="10000"
                  disabled={!selected.can_adjust_usage}
                  value={usageChange}
                  onChange={(event) => setUsageChange(event.target.value)}
                  placeholder="例如 5 或 -2"
                  className="mt-2 w-full rounded-xl border border-[var(--line)] px-3 py-3 font-normal disabled:opacity-50"
                />
              </label>
              <label className="text-sm font-semibold">
                調整原因
                <input
                  type="text"
                  required
                  minLength={3}
                  maxLength={255}
                  disabled={!selected.can_adjust_usage}
                  value={usageReason}
                  onChange={(event) => setUsageReason(event.target.value)}
                  placeholder="例如：客服補償、修正錯誤加值"
                  className="mt-2 w-full rounded-xl border border-[var(--line)] px-3 py-3 font-normal disabled:opacity-50"
                />
              </label>
              <button
                type="submit"
                disabled={busy || !selected.can_adjust_usage}
                className="self-end rounded-xl bg-[var(--teal)] px-5 py-3 text-sm font-semibold text-white disabled:opacity-50"
              >
                {busy ? "處理中…" : "寫入調整"}
              </button>
            </div>
          </form>

          <div className="mt-6 grid gap-6 lg:grid-cols-2">
            <section>
              <h3 className="font-bold">最近使用紀錄</h3>
              {selected.usage_history.length ? (
                <ol className="mt-3 divide-y divide-[var(--line)]">
                  {selected.usage_history.map((item) => (
                    <li key={item.id} className="py-3 text-sm">
                      <div className="flex items-center justify-between gap-4">
                        <span className="font-semibold">
                          {entryLabel[item.entry_type] || item.entry_type}
                        </span>
                        <strong
                          className={
                            item.change >= 0
                              ? "text-emerald-700"
                              : "text-red-700"
                          }
                        >
                          {item.change > 0 ? "+" : ""}
                          {item.change}
                        </strong>
                      </div>
                      <p className="mt-1 text-[var(--muted)]">
                        {item.summary} · 餘額 {item.balance_after}
                      </p>
                      <time className="mt-1 block text-xs text-[var(--muted)]">
                        {dateTime.format(new Date(item.occurred_at))}
                      </time>
                    </li>
                  ))}
                </ol>
              ) : (
                <p className="mt-3 text-sm text-[var(--muted)]">
                  尚無使用紀錄。
                </p>
              )}
            </section>
            <section>
              <h3 className="font-bold">最近管理紀錄</h3>
              {selected.admin_history.length ? (
                <ol className="mt-3 divide-y divide-[var(--line)]">
                  {selected.admin_history.map((item) => (
                    <li key={item.id} className="py-3 text-sm">
                      <span className="font-semibold">
                        {auditLabel[item.action] || item.action}
                      </span>
                      <time className="mt-1 block text-xs text-[var(--muted)]">
                        {dateTime.format(new Date(item.created_at))}
                      </time>
                    </li>
                  ))}
                </ol>
              ) : (
                <p className="mt-3 text-sm text-[var(--muted)]">
                  尚無管理紀錄。
                </p>
              )}
            </section>
          </div>
        </section>
      )}
    </div>
  );
}
