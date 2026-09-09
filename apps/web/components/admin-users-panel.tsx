"use client";

import {
  CalendarClock,
  ChevronLeft,
  ChevronRight,
  KeyRound,
  MailCheck,
  Search,
  ShieldCheck,
  UserCog,
  WalletCards,
} from "lucide-react";
import { useLocale, useTranslations } from "next-intl";
import {
  FormEvent,
  useCallback,
  useEffect,
  useMemo,
  useState,
  useSyncExternalStore,
} from "react";
import { useAdminOperations } from "@/components/admin-operations-provider";
import {
  AdminConfirmDialog,
  AdminDataTable,
  AdminDetailDrawer,
  AdminEmptyState,
  AdminErrorState,
  AdminFilterBar,
  AdminSkeleton,
  AdminStatusPill,
} from "@/components/admin-ui";
import { adminCan } from "@/lib/admin-operations";
import { adminUsersCopy } from "@/lib/admin-users-copy";
import { api } from "@/lib/api";
import { Link } from "@/i18n/navigation";

type UserActivity = {
  trips: number;
  searches: number;
  alerts: number;
  community_posts: number;
  community_comments: number;
};
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
  status?: string;
  admin_roles?: string[];
  auth_methods?: string[];
  email_verified?: boolean;
  last_login_at?: string;
  suspended_at?: string;
  suspended_until?: string;
  suspension_reason?: string;
  last_activity_at?: string;
  activity?: UserActivity;
  erasure_status?: string;
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
type Identity = {
  provider: string;
  email?: string;
  email_verified?: boolean;
  linked_at?: string;
  last_login_at?: string;
};
type Erasure = {
  id: string;
  status: string;
  scheduled_for?: string;
  requested_at?: string;
  cancelled_at?: string;
  completed_at?: string;
  reason?: string;
};
type UserDetail = UserSummary & {
  usage_history: UsageHistory[];
  admin_history: AdminHistory[];
  auth_identities?: Identity[];
  erasure?: Erasure | null;
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
    suspended?: number;
    erasure_pending?: number;
  };
};
type AdjustmentResult = {
  user: UserDetail;
  change: number;
  balance_after: number;
  replayed: boolean;
};
type WrappedUser = UserDetail | { user: UserDetail; replayed?: boolean };
type SensitiveAction = "roles" | "suspend" | "erase";

const roles = [
  "viewer",
  "support",
  "content",
  "operations",
  "database_operator",
  "deployer",
  "owner",
] as const;
const roleCopyKeys: Record<string, string> = {
  viewer: "rolesViewer",
  support: "rolesSupport",
  content: "rolesContent",
  operations: "rolesOperations",
  database_operator: "rolesDatabase",
  deployer: "rolesDeployer",
  owner: "rolesOwner",
};
const entryKeys = new Set([
  "grant",
  "package_grant",
  "use",
  "admin_adjustment",
]);
const auditKeys: Record<string, string> = {
  user_account_updated: "user_account_updated",
  user_usage_adjusted: "user_usage_adjusted",
  "admin_role.updated": "adminRoleUpdated",
};
const listParamNames = [
  "query",
  "status",
  "role",
  "verified",
  "auth_method",
  "activity",
  "registered_from",
  "registered_to",
  "sort",
  "direction",
] as const;
const urlEvent = "admin:location-change";
const timedSuspensionLimitMs = 90 * 24 * 60 * 60 * 1_000;
function timedSuspensionDeadline(value: string) {
  const timestamp = Date.parse(value);
  const now = Date.now();
  return Number.isFinite(timestamp) &&
    timestamp > now &&
    timestamp <= now + timedSuspensionLimitMs
    ? new Date(timestamp)
    : null;
}
function subscribe(listener: () => void) {
  window.addEventListener("popstate", listener);
  window.addEventListener(urlEvent, listener);
  return () => {
    window.removeEventListener("popstate", listener);
    window.removeEventListener(urlEvent, listener);
  };
}
const snapshot = () => window.location.href;
const serverSnapshot = () => "";
function apiDateBoundary(value: string, endOfDay = false) {
  return /^\d{4}-\d{2}-\d{2}$/.test(value)
    ? `${value}T${endOfDay ? "23:59:59.999" : "00:00:00.000"}Z`
    : value;
}
function unwrap(result: WrappedUser) {
  return "user" in result ? result.user : result;
}
function userStatus(user: UserSummary) {
  if (user.status) return user.status;
  if (user.suspended_at && !user.suspended_until) return "suspended";
  return user.is_active ? "active" : "inactive";
}
function roleText(
  t: ReturnType<typeof useTranslations>,
  copy: Record<string, string>,
  user: UserSummary,
) {
  if (user.admin_roles?.length)
    return user.admin_roles
      .map((role) => copy[roleCopyKeys[role]] || role)
      .join(", ");
  if (!user.effective_is_admin) return t("usersPanel.roleMember");
  return t(
    user.admin_source === "environment"
      ? "usersPanel.roleEnvAdmin"
      : "usersPanel.roleAdmin",
  );
}
function activitySummary(copy: Record<string, string>, user: UserSummary) {
  const activity = user.activity;
  if (!activity) return { total: 0, detail: copy.noActivity };
  const entries = [
    [copy.trips, activity.trips],
    [copy.searches, activity.searches],
    [copy.alerts, activity.alerts],
    [copy.posts, activity.community_posts],
    [copy.comments, activity.community_comments],
  ] as const;
  const visible = entries.filter(([, count]) => count > 0);
  return {
    total: entries.reduce((sum, [, count]) => sum + count, 0),
    detail: visible.length
      ? visible.map(([label, count]) => `${count} ${label}`).join(" · ")
      : copy.noActivity,
  };
}

export function AdminUsersPanel() {
  const tAdmin = useTranslations("admin");
  const locale = useLocale();
  const copy = adminUsersCopy(locale);
  const operations = useAdminOperations();
  const rawUrl = useSyncExternalStore(subscribe, snapshot, serverSnapshot);
  const url = new URL(rawUrl || "https://admin.invalid/admin/users");
  const params = url.searchParams;
  const page = Math.max(1, Number(params.get("page")) || 1);
  const selectedId = params.get("user") || "";
  const [data, setData] = useState<UserList>();
  const [selected, setSelected] = useState<UserDetail>();
  const [loading, setLoading] = useState(true);
  const [detailLoading, setDetailLoading] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [filters, setFilters] = useState(
    () =>
      Object.fromEntries(listParamNames.map((name) => [name, ""])) as Record<
        string,
        string
      >,
  );
  const [usageChange, setUsageChange] = useState("");
  const [usageReason, setUsageReason] = useState("");
  const [rolesDraft, setRolesDraft] = useState<string[]>([]);
  const [roleReason, setRoleReason] = useState("");
  const [rolesExpireAt, setRolesExpireAt] = useState("");
  const [suspensionReason, setSuspensionReason] = useState("");
  const [sessionReason, setSessionReason] = useState("");
  const [erasureReason, setErasureReason] = useState("");
  const [suspendUntil, setSuspendUntil] = useState("");
  const [sensitive, setSensitive] = useState<SensitiveAction | null>(null);
  const [stepupPassword, setStepupPassword] = useState("");
  const [confirmation, setConfirmation] = useState("");
  const dateTime = useMemo(
    () =>
      new Intl.DateTimeFormat(locale, {
        dateStyle: "medium",
        timeStyle: "short",
      }),
    [locale],
  );
  const integer = useMemo(() => new Intl.NumberFormat(locale), [locale]);
  const canManage =
    !operations || adminCan(operations.bootstrap, "users.manage");
  const canManageRoles =
    !operations || adminCan(operations.bootstrap, "roles.manage");
  const canManageUsage =
    !operations || adminCan(operations.bootstrap, "usage.manage");

  function updateUrl(values: Record<string, string | null>, push = false) {
    if (typeof window === "undefined") return;
    const next = new URL(window.location.href);
    for (const [key, value] of Object.entries(values)) {
      if (value) next.searchParams.set(key, value);
      else next.searchParams.delete(key);
    }
    window.history[push ? "pushState" : "replaceState"](null, "", next);
    window.dispatchEvent(new Event(urlEvent));
  }
  const urlFilters = useMemo(() => {
    const current = new URL(rawUrl || "https://admin.invalid/admin/users")
      .searchParams;
    return Object.fromEntries(
      listParamNames.map((name) => [name, current.get(name) || ""]),
    ) as Record<string, string>;
  }, [rawUrl]);
  const listPath = useMemo(() => {
    const current = new URL(rawUrl || "https://admin.invalid/admin/users")
      .searchParams;
    const currentPage = Math.max(1, Number(current.get("page")) || 1);
    const query = new URLSearchParams({
      page: String(currentPage),
      limit: "20",
    });
    for (const name of listParamNames) {
      const value = current.get(name);
      if (value)
        query.set(
          name,
          name === "registered_from"
            ? apiDateBoundary(value)
            : name === "registered_to"
              ? apiDateBoundary(value, true)
              : value,
        );
    }
    return `/admin/users?${query}`;
  }, [rawUrl]);
  const loadUsers = useCallback(
    async (quiet = false) => {
      if (!quiet) setLoading(true);
      setError("");
      try {
        setData(await api<UserList>(listPath));
      } catch (reason) {
        setError((reason as Error).message);
      } finally {
        if (!quiet) setLoading(false);
      }
    },
    [listPath, setData, setError, setLoading],
  );
  useEffect(() => {
    const timer = window.setTimeout(() => void loadUsers(), 0);
    return () => window.clearTimeout(timer);
  }, [loadUsers]);
  useEffect(() => {
    const timer = window.setTimeout(() => setFilters(urlFilters), 0);
    return () => window.clearTimeout(timer);
  }, [urlFilters]);
  useEffect(() => {
    let active = true;
    const timer = window.setTimeout(() => {
      if (!selectedId) {
        setSelected(undefined);
        setDetailLoading(false);
        return;
      }
      setSelected(undefined);
      setDetailLoading(true);
      setError("");
      setNotice("");
      setSensitive(null);
      setRoleReason("");
      setRolesExpireAt("");
      setSuspensionReason("");
      setSessionReason("");
      setErasureReason("");
      setUsageChange("");
      setUsageReason("");
      setSuspendUntil("");
      setStepupPassword("");
      setConfirmation("");
      api<UserDetail>(`/admin/users/${selectedId}`)
        .then((result) => {
          if (active) {
            setSelected(result);
            setRolesDraft(result.admin_roles ?? []);
            setRolesExpireAt("");
          }
        })
        .catch((reason: Error) => {
          if (active) setError(reason.message);
        })
        .finally(() => {
          if (active) setDetailLoading(false);
        });
    }, 0);
    return () => {
      active = false;
      window.clearTimeout(timer);
    };
  }, [selectedId]);

  function submitFilters(event: FormEvent) {
    event.preventDefault();
    updateUrl({ ...filters, page: "1", user: null }, true);
  }
  function openUser(userId: string) {
    setSelected(undefined);
    setError("");
    setNotice("");
    updateUrl({ user: userId }, true);
  }
  function closeUser() {
    setSelected(undefined);
    updateUrl({ user: null }, true);
  }
  async function acceptUser(result: WrappedUser, message: string) {
    const user = unwrap(result);
    const currentUserId =
      typeof window === "undefined"
        ? selectedId
        : new URL(window.location.href).searchParams.get("user");
    if (currentUserId === user.id) {
      setSelected(user);
      setRolesDraft(user.admin_roles ?? []);
    }
    setNotice(message);
    await loadUsers(true);
  }
  async function updateAccount(isActive: boolean) {
    if (!selected || selected.id !== selectedId || !isActive) return;
    setBusy(true);
    setError("");
    setNotice("");
    try {
      await acceptUser(
        await api<UserDetail>(`/admin/users/${selected.id}`, {
          method: "PUT",
          body: JSON.stringify({ is_active: isActive }),
        }),
        tAdmin(
          isActive
            ? "usersPanel.accountReactivated"
            : "usersPanel.accountDisabled",
        ),
      );
    } catch (reason) {
      setError((reason as Error).message);
    } finally {
      setBusy(false);
    }
  }
  async function adjustUsage(event: FormEvent) {
    event.preventDefault();
    if (!selected || selected.id !== selectedId || !canManageUsage) return;
    const change = Number(usageChange);
    if (!Number.isInteger(change) || change === 0) {
      setError(tAdmin("usersPanel.adjustInvalid"));
      return;
    }
    setBusy(true);
    setError("");
    setNotice("");
    try {
      const result = await api<AdjustmentResult>(
        `/admin/users/${selected.id}/usage-adjustments`,
        {
          method: "POST",
          headers: { "Idempotency-Key": `admin-${crypto.randomUUID()}` },
          body: JSON.stringify({ change, reason: usageReason }),
        },
      );
      setUsageChange("");
      setUsageReason("");
      await acceptUser(
        result.user,
        tAdmin(
          change > 0 ? "usersPanel.adjustAdded" : "usersPanel.adjustDeducted",
          {
            count: integer.format(Math.abs(change)),
            balance: integer.format(result.balance_after),
          },
        ),
      );
    } catch (reason) {
      setError((reason as Error).message);
    } finally {
      setBusy(false);
    }
  }
  async function mutate(path: string, init: RequestInit, message: string) {
    if (!selected || selected.id !== selectedId) return;
    setBusy(true);
    setError("");
    setNotice("");
    try {
      await acceptUser(await api<WrappedUser>(path, init), message);
    } catch (reason) {
      setError((reason as Error).message);
    } finally {
      setBusy(false);
    }
  }
  async function submitTimedSuspension() {
    if (!selected || selected.id !== selectedId || !suspendUntil) return;
    const deadline = timedSuspensionDeadline(suspendUntil);
    if (!deadline) {
      setError(copy.timedSuspensionLimit);
      return;
    }
    await mutate(
      `/admin/users/${selected.id}/suspension`,
      {
        method: "POST",
        headers: { "Idempotency-Key": `admin-suspend-${crypto.randomUUID()}` },
        body: JSON.stringify({
          reason: suspensionReason,
          suspended_until: deadline.toISOString(),
        }),
      },
      copy.saved,
    );
  }
  async function submitSensitive() {
    if (!selected || selected.id !== selectedId || !sensitive) return;
    setBusy(true);
    setError("");
    setNotice("");
    const scope =
      sensitive === "roles"
        ? "users.roles"
        : sensitive === "suspend"
          ? "users.suspend_permanent"
          : "users.erase";
    try {
      await api("/admin/step-up", {
        method: "POST",
        body: JSON.stringify({ password: stepupPassword, scopes: [scope] }),
      });
      const idempotency = {
        "Idempotency-Key": `admin-${sensitive}-${crypto.randomUUID()}`,
      };
      let result: WrappedUser;
      if (sensitive === "roles")
        result = await api(`/admin/users/${selected.id}/roles`, {
          method: "PATCH",
          headers: idempotency,
          body: JSON.stringify({
            roles: rolesDraft,
            reason: roleReason,
            confirmation: `ROLES ${selected.email}`,
            expires_at: rolesDraft.includes("owner")
              ? null
              : rolesExpireAt
                ? new Date(rolesExpireAt).toISOString()
                : null,
          }),
        });
      else if (sensitive === "suspend")
        result = await api(`/admin/users/${selected.id}/suspension`, {
          method: "POST",
          headers: idempotency,
          body: JSON.stringify({
            reason: suspensionReason,
            suspended_until: null,
            confirmation: `SUSPEND ${selected.email}`,
          }),
        });
      else
        result = await api(`/admin/users/${selected.id}/erasure`, {
          method: "POST",
          headers: idempotency,
          body: JSON.stringify({
            reason: erasureReason,
            confirmation: `ERASE ${selected.email}`,
          }),
        });
      await acceptUser(result, copy.saved);
      setSensitive(null);
      setStepupPassword("");
      setConfirmation("");
    } catch (reason) {
      setError((reason as Error).message);
    } finally {
      setBusy(false);
    }
  }
  const expectedConfirmation =
    !selected || !sensitive
      ? ""
      : `${sensitive === "roles" ? "ROLES" : sensitive === "suspend" ? "SUSPEND" : "ERASE"} ${selected.email}`;
  const status = userStatus;
  const entryLabel = (value: string) =>
    entryKeys.has(value) ? tAdmin(`usersPanel.entry.${value}`) : value;
  const auditText = (value: string) =>
    auditKeys[value] ? tAdmin(`usersPanel.audit.${auditKeys[value]}`) : value;

  return (
    <div className="mt-8 space-y-6">
      {error && <AdminErrorState title={copy.operationFailed} detail={error} />}
      {notice && (
        <p
          role="status"
          className="rounded-xl bg-emerald-50 p-4 text-sm font-semibold text-emerald-800"
        >
          {notice}
        </p>
      )}
      {data && (
        <section
          aria-label={tAdmin("usersPanel.statsSection")}
          className="grid gap-3 sm:grid-cols-2 xl:grid-cols-4"
        >
          {[
            ["statTotal", data.stats.total],
            ["statActive", data.stats.active],
            ["statAdmins", data.stats.administrators],
            ["statAvailable", data.stats.available_uses],
          ].map(([key, value]) => (
            <article
              key={String(key)}
              className="rounded-[1.35rem] border border-[var(--line)] bg-[var(--surface)] p-5 shadow-[var(--shadow-sm)]"
            >
              <p className="text-xs font-bold text-[var(--muted)]">
                {tAdmin(`usersPanel.${String(key)}`)}
              </p>
              <p className="mt-2 text-3xl font-black tabular-nums">
                {integer.format(Number(value))}
              </p>
            </article>
          ))}
        </section>
      )}
      <section className="rounded-[1.75rem] border border-[var(--line)] bg-[var(--surface)] p-5 shadow-[var(--shadow-sm)] md:p-7">
        <div>
          <h2 className="text-xl font-black">
            {tAdmin("usersPanel.listTitle")}
          </h2>
          <p className="mt-1 text-sm text-[var(--muted)]">
            {tAdmin("usersPanel.listHint")}
          </p>
        </div>
        <form onSubmit={submitFilters}>
          <AdminFilterBar>
            <label className="min-w-[14rem] flex-1 text-xs font-bold text-[var(--muted)]">
              {tAdmin("usersPanel.searchLabel")}
              <input
                value={filters.query}
                onChange={(event) =>
                  setFilters({ ...filters, query: event.target.value })
                }
                className="mt-1 min-h-11 w-full rounded-xl border border-[var(--line)] bg-[var(--surface)] px-3 text-sm text-[var(--ink)]"
              />
            </label>
            <label className="text-xs font-bold text-[var(--muted)]">
              {copy.status}
              <select
                value={filters.status}
                onChange={(event) =>
                  setFilters({ ...filters, status: event.target.value })
                }
                className="mt-1 min-h-11 rounded-xl border border-[var(--line)] bg-[var(--surface)] px-3 text-sm text-[var(--ink)]"
              >
                <option value="">{copy.all}</option>
                <option value="active">{copy.active}</option>
                <option value="inactive">{copy.inactive}</option>
                <option value="suspended">{copy.suspended}</option>
                <option value="erasure_pending">{copy.erasurePending}</option>
              </select>
            </label>
            <label className="text-xs font-bold text-[var(--muted)]">
              {copy.role}
              <select
                value={filters.role}
                onChange={(event) =>
                  setFilters({ ...filters, role: event.target.value })
                }
                className="mt-1 min-h-11 rounded-xl border border-[var(--line)] bg-[var(--surface)] px-3 text-sm text-[var(--ink)]"
              >
                <option value="">{copy.all}</option>
                {roles.map((role) => (
                  <option key={role} value={role}>
                    {copy[roleCopyKeys[role]]}
                  </option>
                ))}
              </select>
            </label>
            <label className="text-xs font-bold text-[var(--muted)]">
              {copy.verification}
              <select
                value={filters.verified}
                onChange={(event) =>
                  setFilters({ ...filters, verified: event.target.value })
                }
                className="mt-1 min-h-11 rounded-xl border border-[var(--line)] bg-[var(--surface)] px-3 text-sm text-[var(--ink)]"
              >
                <option value="">{copy.all}</option>
                <option value="true">{copy.verified}</option>
                <option value="false">{copy.unverified}</option>
              </select>
            </label>
            <label className="text-xs font-bold text-[var(--muted)]">
              {copy.loginMethod}
              <select
                value={filters.auth_method}
                onChange={(event) =>
                  setFilters({ ...filters, auth_method: event.target.value })
                }
                className="mt-1 min-h-11 rounded-xl border border-[var(--line)] bg-[var(--surface)] px-3 text-sm text-[var(--ink)]"
              >
                <option value="">{copy.all}</option>
                {["password", "google", "line", "apple"].map((method) => (
                  <option key={method}>{method}</option>
                ))}
              </select>
            </label>
            <label className="text-xs font-bold text-[var(--muted)]">
              {copy.activityFilter}
              <select
                value={filters.activity}
                onChange={(event) =>
                  setFilters({ ...filters, activity: event.target.value })
                }
                className="mt-1 min-h-11 rounded-xl border border-[var(--line)] bg-[var(--surface)] px-3 text-sm text-[var(--ink)]"
              >
                <option value="">{copy.all}</option>
                <option value="has_activity">{copy.hasActivity}</option>
                <option value="no_activity">{copy.noActivity}</option>
              </select>
            </label>
            <label className="text-xs font-bold text-[var(--muted)]">
              {copy.registeredFrom}
              <input
                type="date"
                value={filters.registered_from}
                onChange={(event) =>
                  setFilters({
                    ...filters,
                    registered_from: event.target.value,
                  })
                }
                className="mt-1 min-h-11 rounded-xl border border-[var(--line)] bg-[var(--surface)] px-3 text-sm text-[var(--ink)]"
              />
            </label>
            <label className="text-xs font-bold text-[var(--muted)]">
              {copy.registeredTo}
              <input
                type="date"
                value={filters.registered_to}
                onChange={(event) =>
                  setFilters({ ...filters, registered_to: event.target.value })
                }
                className="mt-1 min-h-11 rounded-xl border border-[var(--line)] bg-[var(--surface)] px-3 text-sm text-[var(--ink)]"
              />
            </label>
            <label className="text-xs font-bold text-[var(--muted)]">
              {copy.sort}
              <select
                value={filters.sort || "created_at"}
                onChange={(event) =>
                  setFilters({ ...filters, sort: event.target.value })
                }
                className="mt-1 min-h-11 rounded-xl border border-[var(--line)] bg-[var(--surface)] px-3 text-sm text-[var(--ink)]"
              >
                <option value="created_at">{copy.createdAt}</option>
                <option value="last_login_at">{copy.lastLogin}</option>
                <option value="last_activity_at">{copy.lastActivity}</option>
                <option value="activity_count">{copy.activityCount}</option>
                <option value="email">{copy.email}</option>
                <option value="updated_at">{copy.updatedAt}</option>
                <option value="remaining_uses">{copy.remainingUses}</option>
              </select>
            </label>
            <label className="sr-only" htmlFor="admin-user-direction">
              {copy.sort}
            </label>
            <select
              id="admin-user-direction"
              value={filters.direction || "desc"}
              onChange={(event) =>
                setFilters({ ...filters, direction: event.target.value })
              }
              className="min-h-11 rounded-xl border border-[var(--line)] bg-[var(--surface)] px-3 text-sm"
            >
              <option value="desc">{copy.descending}</option>
              <option value="asc">{copy.ascending}</option>
            </select>
            <button
              type="submit"
              className="inline-flex min-h-11 items-center justify-center gap-2 rounded-xl bg-[var(--ink)] px-4 text-sm font-bold text-white"
            >
              <Search aria-hidden size={16} />
              {tAdmin("usersPanel.searchButton")}
            </button>
            <button
              type="button"
              onClick={() => {
                const cleared = Object.fromEntries(
                  listParamNames.map((name) => [name, ""]),
                );
                setFilters(cleared);
                updateUrl({ ...cleared, page: null, user: null }, true);
              }}
              className="min-h-11 rounded-xl border border-[var(--line)] px-4 text-sm font-bold"
            >
              {copy.reset}
            </button>
          </AdminFilterBar>
        </form>
        {loading ? (
          <AdminSkeleton label={tAdmin("usersPanel.loadingUsers")} />
        ) : data?.items.length ? (
          <AdminDataTable
            label={tAdmin("usersPanel.listTitle")}
            headers={[
              tAdmin("usersPanel.columnMember"),
              tAdmin("usersPanel.columnStatus"),
              tAdmin("usersPanel.columnRole"),
              copy.authMethods,
              tAdmin("usersPanel.columnUses"),
              copy.activity,
              copy.lastLogin,
              tAdmin("usersPanel.columnActions"),
            ]}
          >
            {data.items.map((user) => {
              const activity = activitySummary(copy, user);
              return (
                <tr
                  key={user.id}
                  className="border-b border-[var(--line)] last:border-0"
                >
                  <td
                    className="px-4 py-4"
                    data-label={tAdmin("usersPanel.columnMember")}
                  >
                    <strong className="block break-all">{user.email}</strong>
                    {user.is_self && (
                      <span className="text-xs text-[var(--teal)]">
                        {tAdmin("usersPanel.currentAccount")}
                      </span>
                    )}
                  </td>
                  <td
                    className="px-4 py-4"
                    data-label={tAdmin("usersPanel.columnStatus")}
                  >
                    <AdminStatusPill status={status(user)}>
                      {copy[status(user)] || status(user)}
                    </AdminStatusPill>
                    {status(user) === "suspended" && user.suspended_until && (
                      <time className="mt-1 block text-xs text-[var(--muted)]">
                        {dateTime.format(new Date(user.suspended_until))}
                      </time>
                    )}
                  </td>
                  <td
                    className="px-4 py-4 text-xs"
                    data-label={tAdmin("usersPanel.columnRole")}
                  >
                    {roleText(tAdmin, copy, user)}
                  </td>
                  <td
                    className="px-4 py-4 text-xs"
                    data-label={copy.authMethods}
                  >
                    {user.auth_methods?.join(" · ") || "password"}
                    {user.email_verified === false && (
                      <span className="mt-1 block text-amber-700">
                        {copy.unverified}
                      </span>
                    )}
                  </td>
                  <td
                    className="px-4 py-4"
                    data-label={tAdmin("usersPanel.columnUses")}
                  >
                    <strong>{integer.format(user.available_uses)}</strong>
                    <span className="text-xs text-[var(--muted)]">
                      {" "}
                      {tAdmin("usersPanel.availableSuffix")}
                    </span>
                  </td>
                  <td className="px-4 py-4 text-xs" data-label={copy.activity}>
                    <strong className="block text-[var(--ink)]">
                      {integer.format(activity.total)}
                    </strong>
                    <span className="mt-1 block max-w-52 text-[var(--muted)]">
                      {activity.detail}
                    </span>
                    {user.last_activity_at && (
                      <time className="mt-1 block text-[var(--muted)]">
                        {copy.lastActivity}:{" "}
                        {dateTime.format(new Date(user.last_activity_at))}
                      </time>
                    )}
                  </td>
                  <td
                    className="px-4 py-4 text-xs text-[var(--muted)]"
                    data-label={copy.lastLogin}
                  >
                    {user.last_login_at
                      ? dateTime.format(new Date(user.last_login_at))
                      : copy.never}
                  </td>
                  <td
                    className="px-4 py-4"
                    data-label={tAdmin("usersPanel.columnActions")}
                  >
                    <button
                      type="button"
                      onClick={() => void openUser(user.id)}
                      className="min-h-11 rounded-xl border border-[var(--line)] px-3 text-sm font-bold"
                    >
                      {tAdmin("usersPanel.manage")}
                    </button>
                  </td>
                </tr>
              );
            })}
          </AdminDataTable>
        ) : (
          <AdminEmptyState title={tAdmin("usersPanel.listEmpty")} />
        )}
        {data && (
          <div className="mt-5 flex flex-col items-center justify-between gap-3 text-sm sm:flex-row">
            <span className="text-[var(--muted)]">
              {tAdmin("usersPanel.pageSummary", {
                page: data.page,
                pages: data.pages,
                total: data.total,
              })}
            </span>
            <div className="flex gap-2">
              <button
                type="button"
                aria-label={tAdmin("usersPanel.previous")}
                disabled={page <= 1 || loading}
                onClick={() =>
                  updateUrl({ page: String(page - 1), user: null }, true)
                }
                className="admin-icon-button disabled:opacity-40"
              >
                <ChevronLeft aria-hidden size={17} />
              </button>
              <button
                type="button"
                aria-label={tAdmin("usersPanel.next")}
                disabled={page >= data.pages || loading}
                onClick={() =>
                  updateUrl({ page: String(page + 1), user: null }, true)
                }
                className="admin-icon-button disabled:opacity-40"
              >
                <ChevronRight aria-hidden size={17} />
              </button>
            </div>
          </div>
        )}
      </section>
      <AdminDetailDrawer
        open={Boolean(selectedId)}
        title={
          selected?.id === selectedId ? selected.email : copy.loadingDetail
        }
        onClose={closeUser}
        closeLabel={tAdmin("usersPanel.closeDetail")}
      >
        {detailLoading && <AdminSkeleton label={copy.loadingDetail} />}
        {selected && selected.id === selectedId && (
          <div className="space-y-6">
            <div className="flex flex-wrap items-center gap-2">
              <AdminStatusPill status={status(selected)}>
                {copy[status(selected)] || status(selected)}
              </AdminStatusPill>
              {selected.admin_source === "environment" && (
                <AdminStatusPill status="healthy">
                  {copy.environmentOwner}
                </AdminStatusPill>
              )}
              <span className="text-xs text-[var(--muted)]">
                {tAdmin("usersPanel.joinedAt", {
                  time: dateTime.format(new Date(selected.created_at)),
                })}
              </span>
              {selected.last_activity_at && (
                <span className="text-xs text-[var(--muted)]">
                  {copy.lastActivity}:{" "}
                  {dateTime.format(new Date(selected.last_activity_at))}
                </span>
              )}
            </div>
            <section
              aria-label={copy.activity}
              className="grid grid-cols-2 gap-3 sm:grid-cols-5"
            >
              {[
                [copy.trips, selected.activity?.trips],
                [copy.searches, selected.activity?.searches],
                [copy.alerts, selected.activity?.alerts],
                [copy.posts, selected.activity?.community_posts],
                [copy.comments, selected.activity?.community_comments],
              ].map(([label, value]) => (
                <div
                  key={String(label)}
                  className="rounded-xl bg-[var(--paper)] p-3"
                >
                  <strong className="text-xl tabular-nums">
                    {integer.format(Number(value || 0))}
                  </strong>
                  <p className="text-xs text-[var(--muted)]">{label}</p>
                </div>
              ))}
            </section>
            <section className="grid gap-3 md:grid-cols-3">
              <article className="rounded-2xl bg-[var(--paper)] p-5">
                <UserCog aria-hidden className="text-[var(--teal)]" size={20} />
                <h3 className="mt-3 text-sm font-bold">
                  {tAdmin("usersPanel.accountStatus")}
                </h3>
                <p className="mt-1 font-black">
                  {copy[status(selected)] || status(selected)}
                </p>
                {status(selected) === "inactive" && (
                  <button
                    type="button"
                    disabled={busy || selected.is_self || !canManage}
                    onClick={() => void updateAccount(true)}
                    className="mt-4 min-h-11 w-full rounded-xl border border-[var(--line)] px-3 text-sm font-bold disabled:opacity-40"
                  >
                    {tAdmin("usersPanel.reactivate")}
                  </button>
                )}
              </article>
              <article className="rounded-2xl bg-[var(--paper)] p-5">
                <ShieldCheck
                  aria-hidden
                  className="text-[var(--coral)]"
                  size={20}
                />
                <h3 className="mt-3 text-sm font-bold">{copy.roles}</h3>
                <p className="mt-1 text-sm font-black">
                  {roleText(tAdmin, copy, selected)}
                </p>
                <p className="mt-3 text-xs text-[var(--muted)]">
                  {copy.authMethods}:{" "}
                  {selected.auth_methods?.join(" · ") || "password"}
                </p>
              </article>
              <article className="rounded-2xl bg-[var(--paper)] p-5">
                <WalletCards
                  aria-hidden
                  className="text-[var(--teal)]"
                  size={20}
                />
                <h3 className="mt-3 text-sm font-bold">
                  {tAdmin("usersPanel.usesTitle")}
                </h3>
                <p className="mt-1 text-2xl font-black">
                  {integer.format(selected.available_uses)}
                </p>
                <p className="mt-3 text-xs text-[var(--muted)]">
                  {tAdmin("usersPanel.ledgerBalance", {
                    count: integer.format(selected.remaining_uses),
                  })}
                </p>
              </article>
            </section>
            <section className="rounded-2xl border border-[var(--line)] p-5">
              <h3 className="font-black">{copy.roles}</h3>
              <p className="mt-1 text-sm text-[var(--muted)]">
                {copy.rolesHint}
              </p>
              <div className="mt-4 grid gap-2 sm:grid-cols-2">
                {roles.map((role) => (
                  <label
                    key={role}
                    className="flex min-h-11 items-center gap-3 rounded-xl bg-[var(--paper)] px-3 text-sm font-semibold"
                  >
                    <input
                      type="checkbox"
                      checked={rolesDraft.includes(role)}
                      disabled={
                        !canManageRoles ||
                        selected.admin_source === "environment" ||
                        selected.is_self
                      }
                      onChange={(event) => {
                        const next = event.target.checked
                          ? [...rolesDraft, role]
                          : rolesDraft.filter((item) => item !== role);
                        setRolesDraft(next);
                        if (role === "owner" && event.target.checked) {
                          setRolesExpireAt("");
                        }
                      }}
                    />
                    {copy[roleCopyKeys[role]]}
                  </label>
                ))}
              </div>
              <div className="mt-4 grid gap-3 sm:grid-cols-2">
                <label className="block text-sm font-bold">
                  {copy.roleReason}
                  <input
                    value={roleReason}
                    onChange={(event) => setRoleReason(event.target.value)}
                    maxLength={255}
                    className="mt-2 min-h-11 w-full rounded-xl border border-[var(--line)] px-3 font-normal"
                  />
                </label>
                <label className="block text-sm font-bold">
                  {copy.rolesExpireAt}
                  <input
                    type="datetime-local"
                    value={rolesExpireAt}
                    onChange={(event) => setRolesExpireAt(event.target.value)}
                    disabled={rolesDraft.includes("owner")}
                    className="mt-2 min-h-11 w-full rounded-xl border border-[var(--line)] px-3 font-normal disabled:opacity-50"
                  />
                  {rolesDraft.includes("owner") && (
                    <span className="mt-2 block text-xs font-normal text-[var(--muted)]">
                      {copy.ownerNoExpiry}
                    </span>
                  )}
                </label>
              </div>
              <button
                type="button"
                disabled={
                  !canManageRoles ||
                  !roleReason.trim() ||
                  selected.admin_source === "environment" ||
                  selected.is_self ||
                  busy
                }
                onClick={() => {
                  setSensitive("roles");
                  setConfirmation("");
                }}
                className="mt-4 min-h-11 rounded-xl bg-[var(--ink)] px-4 text-sm font-bold text-white disabled:opacity-40"
              >
                {copy.saveRoles}
              </button>
            </section>
            <section className="rounded-2xl border border-[var(--line)] p-5">
              <h3 className="font-black">{copy.suspension}</h3>
              {status(selected) === "suspended" && (
                <p className="mt-2 rounded-xl bg-red-50 p-3 text-sm text-red-900">
                  {selected.suspended_until
                    ? `${copy.suspendedUntil}: ${dateTime.format(new Date(selected.suspended_until))}`
                    : copy.permanent}
                  {selected.suspension_reason
                    ? ` · ${selected.suspension_reason}`
                    : ""}
                </p>
              )}
              <div className="mt-4 grid gap-3 sm:grid-cols-2">
                <label className="text-sm font-bold">
                  {copy.suspensionReason}
                  <input
                    value={suspensionReason}
                    onChange={(event) =>
                      setSuspensionReason(event.target.value)
                    }
                    className="mt-2 min-h-11 w-full rounded-xl border border-[var(--line)] px-3 font-normal"
                  />
                </label>
                <label className="text-sm font-bold">
                  {copy.suspensionUntil}
                  <input
                    type="datetime-local"
                    value={suspendUntil}
                    onChange={(event) => setSuspendUntil(event.target.value)}
                    disabled={status(selected) === "suspended"}
                    className="mt-2 min-h-11 w-full rounded-xl border border-[var(--line)] px-3 font-normal disabled:opacity-50"
                  />
                  <span className="mt-2 block text-xs font-normal text-[var(--muted)]">
                    {copy.timedSuspensionLimit}
                  </span>
                </label>
              </div>
              <div className="mt-4 flex flex-wrap gap-2">
                {status(selected) === "suspended" ? (
                  <button
                    type="button"
                    disabled={
                      !canManage ||
                      selected.is_self ||
                      !suspensionReason.trim() ||
                      busy
                    }
                    onClick={() =>
                      void mutate(
                        `/admin/users/${selected.id}/suspension`,
                        {
                          method: "DELETE",
                          body: JSON.stringify({ reason: suspensionReason }),
                        },
                        copy.saved,
                      )
                    }
                    className="min-h-11 rounded-xl border border-[var(--line)] px-4 text-sm font-bold disabled:opacity-40"
                  >
                    {copy.unsuspend}
                  </button>
                ) : (
                  <button
                    type="button"
                    disabled={
                      !canManage ||
                      selected.is_self ||
                      !suspensionReason.trim() ||
                      busy
                    }
                    onClick={() =>
                      suspendUntil
                        ? void submitTimedSuspension()
                        : (setSensitive("suspend"), setConfirmation(""))
                    }
                    className="min-h-11 rounded-xl bg-red-700 px-4 text-sm font-bold text-white disabled:opacity-40"
                  >
                    {copy.suspend}
                  </button>
                )}
              </div>
            </section>
            <section className="grid gap-4 md:grid-cols-2">
              <article className="rounded-2xl border border-[var(--line)] p-5">
                <KeyRound
                  aria-hidden
                  className="text-[var(--teal)]"
                  size={20}
                />
                <h3 className="mt-3 font-black">{copy.sessions}</h3>
                <p className="mt-1 text-sm text-[var(--muted)]">
                  {copy.lastLogin}:{" "}
                  {selected.last_login_at
                    ? dateTime.format(new Date(selected.last_login_at))
                    : copy.never}
                </p>
                <label className="mt-4 block text-sm font-bold">
                  {copy.operationReason}
                  <input
                    value={sessionReason}
                    onChange={(event) => setSessionReason(event.target.value)}
                    maxLength={255}
                    className="mt-2 min-h-11 w-full rounded-xl border border-[var(--line)] px-3 font-normal"
                  />
                </label>
                <button
                  type="button"
                  disabled={
                    !canManage ||
                    selected.is_self ||
                    !sessionReason.trim() ||
                    busy
                  }
                  onClick={() =>
                    void mutate(
                      `/admin/users/${selected.id}/sessions/revoke`,
                      {
                        method: "POST",
                        body: JSON.stringify({ reason: sessionReason }),
                      },
                      copy.revoked,
                    )
                  }
                  className="mt-4 min-h-11 rounded-xl border border-[var(--line)] px-4 text-sm font-bold disabled:opacity-40"
                >
                  {copy.revokeSessions}
                </button>
              </article>
              <article className="rounded-2xl border border-[var(--line)] p-5">
                <MailCheck
                  aria-hidden
                  className="text-[var(--teal)]"
                  size={20}
                />
                <h3 className="mt-3 font-black">{copy.verificationTitle}</h3>
                <p className="mt-1 text-sm text-[var(--muted)]">
                  {selected.email_verified ? copy.verified : copy.unverified}
                </p>
                <button
                  type="button"
                  disabled={!canManage || selected.email_verified || busy}
                  onClick={() =>
                    void mutate(
                      `/admin/users/${selected.id}/verification`,
                      { method: "POST" },
                      copy.verificationSent,
                    )
                  }
                  className="mt-4 min-h-11 rounded-xl border border-[var(--line)] px-4 text-sm font-bold disabled:opacity-40"
                >
                  {copy.resendVerification}
                </button>
              </article>
            </section>
            {selected.auth_identities?.length ? (
              <section>
                <h3 className="font-black">{copy.authMethods}</h3>
                <div className="mt-3 grid gap-2">
                  {selected.auth_identities.map((identity) => (
                    <div
                      key={`${identity.provider}-${identity.email || ""}`}
                      className="grid gap-2 rounded-xl bg-[var(--paper)] p-4 text-sm sm:grid-cols-[8rem_1fr_auto]"
                    >
                      <strong>{identity.provider}</strong>
                      <span className="break-all">
                        {identity.email || selected.email}
                      </span>
                      <span className="text-xs text-[var(--muted)]">
                        {identity.last_login_at
                          ? dateTime.format(new Date(identity.last_login_at))
                          : copy.never}
                      </span>
                    </div>
                  ))}
                </div>
              </section>
            ) : null}
            <section className="rounded-2xl border border-red-200 bg-red-50/50 p-5">
              <div className="flex items-start gap-3">
                <CalendarClock
                  aria-hidden
                  className="mt-0.5 text-red-700"
                  size={20}
                />
                <div>
                  <h3 className="font-black">{copy.erasure}</h3>
                  <p className="mt-1 text-sm leading-6 text-[var(--muted)]">
                    {copy.erasureHint}
                  </p>
                </div>
              </div>
              {selected.erasure && (
                <p className="mt-3 text-sm">
                  <strong>{copy.erasureStatus}:</strong>{" "}
                  {selected.erasure.status}
                  {selected.erasure.scheduled_for
                    ? ` · ${copy.scheduledFor} ${dateTime.format(new Date(selected.erasure.scheduled_for))}`
                    : ""}
                </p>
              )}
              <label className="mt-4 block text-sm font-bold">
                {copy.operationReason}
                <input
                  value={erasureReason}
                  onChange={(event) => setErasureReason(event.target.value)}
                  maxLength={255}
                  className="mt-2 min-h-11 w-full rounded-xl border border-red-200 bg-white px-3 font-normal"
                />
              </label>
              <div className="mt-4 flex flex-wrap gap-2">
                {selected.erasure &&
                ["scheduled", "pending"].includes(selected.erasure.status) ? (
                  <button
                    type="button"
                    disabled={!canManage || !erasureReason.trim() || busy}
                    onClick={() =>
                      void mutate(
                        `/admin/users/${selected.id}/erasure`,
                        {
                          method: "DELETE",
                          body: JSON.stringify({ reason: erasureReason }),
                        },
                        copy.saved,
                      )
                    }
                    className="min-h-11 rounded-xl border border-red-300 px-4 text-sm font-bold text-red-800 disabled:opacity-40"
                  >
                    {copy.cancelErasure}
                  </button>
                ) : (
                  <button
                    type="button"
                    disabled={
                      !canManage ||
                      selected.is_self ||
                      selected.admin_source === "environment" ||
                      !erasureReason.trim() ||
                      busy
                    }
                    onClick={() => {
                      setSensitive("erase");
                      setConfirmation("");
                    }}
                    className="min-h-11 rounded-xl bg-red-700 px-4 text-sm font-bold text-white disabled:opacity-40"
                  >
                    {copy.scheduleErasure}
                  </button>
                )}
              </div>
            </section>
            <form
              onSubmit={adjustUsage}
              className="rounded-2xl border border-[var(--line)] p-5"
            >
              <h3 className="font-black">{tAdmin("usersPanel.adjustTitle")}</h3>
              <p className="mt-1 text-sm text-[var(--muted)]">
                {tAdmin("usersPanel.adjustHint")}
              </p>
              {selected.is_self && (
                <p
                  className={`mt-2 text-xs font-bold ${selected.can_adjust_usage && canManageUsage ? "text-[var(--teal)]" : "text-[var(--coral)]"}`}
                >
                  {tAdmin(
                    selected.can_adjust_usage && canManageUsage
                      ? "usersPanel.selfAllowed"
                      : "usersPanel.selfBlocked",
                  )}
                </p>
              )}
              <div className="mt-4 grid gap-4 md:grid-cols-[10rem_1fr_auto]">
                <label className="text-sm font-bold">
                  {tAdmin("usersPanel.changeLabel")}
                  <input
                    type="number"
                    required
                    step="1"
                    min="-10000"
                    max="10000"
                    disabled={!selected.can_adjust_usage || !canManageUsage}
                    value={usageChange}
                    onChange={(event) => setUsageChange(event.target.value)}
                    className="mt-2 min-h-11 w-full rounded-xl border border-[var(--line)] px-3 font-normal disabled:opacity-50"
                  />
                </label>
                <label className="text-sm font-bold">
                  {tAdmin("usersPanel.reasonLabel")}
                  <input
                    required
                    minLength={3}
                    maxLength={255}
                    disabled={!selected.can_adjust_usage || !canManageUsage}
                    value={usageReason}
                    onChange={(event) => setUsageReason(event.target.value)}
                    className="mt-2 min-h-11 w-full rounded-xl border border-[var(--line)] px-3 font-normal disabled:opacity-50"
                  />
                </label>
                <button
                  type="submit"
                  disabled={
                    busy || !selected.can_adjust_usage || !canManageUsage
                  }
                  className="self-end min-h-11 rounded-xl bg-[var(--teal)] px-5 text-sm font-bold text-white disabled:opacity-50"
                >
                  {tAdmin(
                    busy ? "usersPanel.submitting" : "usersPanel.submitAdjust",
                  )}
                </button>
              </div>
            </form>
            <section className="grid gap-5 lg:grid-cols-2">
              <div>
                <h3 className="font-black">
                  {tAdmin("usersPanel.usageHistory")}
                </h3>
                {selected.usage_history?.length ? (
                  <ol className="mt-2 divide-y divide-[var(--line)]">
                    {selected.usage_history.map((item) => (
                      <li key={item.id} className="py-3 text-sm">
                        <div className="flex justify-between gap-3">
                          <strong>{entryLabel(item.entry_type)}</strong>
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
                          {tAdmin("usersPanel.entrySummary", {
                            summary: item.summary,
                            balance: item.balance_after,
                          })}
                        </p>
                      </li>
                    ))}
                  </ol>
                ) : (
                  <p className="mt-2 text-sm text-[var(--muted)]">
                    {tAdmin("usersPanel.usageEmpty")}
                  </p>
                )}
              </div>
              <div>
                <h3 className="font-black">
                  {tAdmin("usersPanel.adminHistory")}
                </h3>
                {selected.admin_history?.length ? (
                  <ol className="mt-2 divide-y divide-[var(--line)]">
                    {selected.admin_history.map((item) => (
                      <li key={item.id} className="py-3 text-sm">
                        <strong>{auditText(item.action)}</strong>
                        <time className="mt-1 block text-xs text-[var(--muted)]">
                          {dateTime.format(new Date(item.created_at))}
                        </time>
                      </li>
                    ))}
                  </ol>
                ) : (
                  <p className="mt-2 text-sm text-[var(--muted)]">
                    {tAdmin("usersPanel.adminEmpty")}
                  </p>
                )}
              </div>
            </section>
          </div>
        )}
      </AdminDetailDrawer>
      <AdminConfirmDialog
        open={Boolean(sensitive)}
        title={
          sensitive === "roles"
            ? copy.rolesConfirmation
            : sensitive === "suspend"
              ? copy.suspendConfirmation
              : copy.eraseConfirmation
        }
        description={copy.sensitiveDescription}
        confirmationLabel={copy.typeConfirmation}
        expectedConfirmation={expectedConfirmation}
        confirmation={confirmation}
        password={stepupPassword}
        passwordLabel={copy.stepupPassword}
        recoveryAction={
          <Link
            href="/forgot-password"
            className="inline-flex min-h-11 items-center underline"
          >
            {copy.setLocalPassword}
          </Link>
        }
        busy={busy}
        cancelLabel={tAdmin("usersPanel.confirmCancel")}
        confirmLabel={
          sensitive === "roles"
            ? copy.saveRoles
            : sensitive === "suspend"
              ? copy.confirmPermanentSuspension
              : copy.confirmErasure
        }
        onConfirmationChange={setConfirmation}
        onPasswordChange={setStepupPassword}
        onCancel={() => {
          if (!busy) {
            setSensitive(null);
            setStepupPassword("");
            setConfirmation("");
          }
        }}
        onConfirm={() => void submitSensitive()}
      />
    </div>
  );
}
