"use client";

import { Check, Copy, History, Link2, LoaderCircle, Unlink } from "lucide-react";
import { Link } from "@/i18n/navigation";
import { useLocale, useTranslations } from "next-intl";
import { useEffect, useState } from "react";
import { useSiteVisibility } from "@/components/site-visibility-provider";
import { api } from "@/lib/api";
import { activeLocale } from "@/lib/locale-format";
import { featureEnabled } from "@/lib/site-features";

type Provider = "google" | "line" | "apple";
type Me = { id: string; email: string; has_password?: boolean; auth_methods?: string[]; identity_count?: number };
type Identity = { id: string; provider: Provider; email?: string | null; linked_at: string; last_login_at?: string | null };
type ProviderStatus = { providers: Record<Provider, boolean> };
type Usage = {
  remaining_uses: number;
  reserved_uses: number;
  available_uses: number;
  limits: { saved_trips: number; price_alerts: number };
};
type HistoryKind = "all" | "charged" | "granted" | "released";
type UsageHistoryItem = {
  id: string;
  occurred_at: string;
  type: string;
  status: string;
  operation?: string;
  summary: string;
  change: number;
  balance_after: number;
  reference: string;
  unit: string;
  is_legacy: boolean;
};
type UsageHistory = { items: UsageHistoryItem[]; next_cursor?: string };

const inputClass =
  "mt-2 w-full rounded-xl border border-[var(--line)] p-3 font-normal";
const historyFilters: Array<{ key: HistoryKind; label: string }> = [
  { key: "all", label: "全部" },
  { key: "charged", label: "成功扣次" },
  { key: "granted", label: "加值／贈送" },
  { key: "released", label: "失敗未扣" },
];

function statusLabel(item: UsageHistoryItem) {
  if (item.is_legacy) {
    if (item.status === "charged") return "舊制扣點";
    if (item.status === "released") return "舊制退回";
    if (item.status === "granted") return "舊制發放";
    if (item.status === "expired") return "舊制到期";
    return "舊制紀錄";
  }
  if (item.status === "charged") return "成功扣次";
  if (item.status === "released") return "失敗未扣次";
  if (item.status === "granted") return "次數入帳";
  if (item.status === "migrated") return "舊制轉換";
  if (item.status === "expired") return "舊制到期";
  return "人工調整";
}

function statusClass(item: UsageHistoryItem) {
  if (item.status === "charged") return "bg-[#fff4ef] text-[#7e4439]";
  if (item.status === "released") return "bg-emerald-50 text-emerald-800";
  return "bg-[var(--teal-soft)] text-[var(--teal-dark)]";
}

function changeLabel(item: UsageHistoryItem) {
  if (item.change === 0) return "0 次";
  const suffix = item.is_legacy ? " credits" : " 次";
  return `${item.change > 0 ? "+" : ""}${item.change}${suffix}`;
}

function maskEmail(email?: string | null) {
  if (!email) return undefined;
  const [name, domain] = email.split("@");
  if (!domain) return email;
  const visible = name.slice(0, Math.min(2, name.length));
  return `${visible}${"*".repeat(Math.max(3, name.length - visible.length))}@${domain}`;
}

export function AccountPanel() {
  const locale = useLocale();
  const accountT = useTranslations("account");
  const visibility = useSiteVisibility();
  const dateFormat = new Intl.DateTimeFormat(activeLocale(), { dateStyle: "medium", timeStyle: "short" });
  const [me, setMe] = useState<Me>();
  const [usage, setUsage] = useState<Usage>();
  const [history, setHistory] = useState<UsageHistoryItem[]>([]);
  const [nextCursor, setNextCursor] = useState<string>();
  const [historyKind, setHistoryKind] = useState<HistoryKind>("all");
  const [historyBusy, setHistoryBusy] = useState(true);
  const [historyError, setHistoryError] = useState<string>();
  const [loadError, setLoadError] = useState<string>();
  const [formError, setFormError] = useState<string>();
  const [done, setDone] = useState(false);
  const [busy, setBusy] = useState(false);
  const [identities, setIdentities] = useState<Identity[]>([]);
  const [oauthProviders, setOauthProviders] = useState<ProviderStatus>();
  const [identityError, setIdentityError] = useState<string>();

  useEffect(() => {
    api<Me>("/auth/me")
      .then(setMe)
      .catch((reason: Error) => setLoadError(reason.message));
    api<Usage>("/usage")
      .then(setUsage)
      .catch(() => undefined);
    api<Identity[]>("/auth/identities").then(setIdentities).catch(() => undefined);
    api<ProviderStatus>("/auth/oauth/providers").then(setOauthProviders).catch(() => undefined);
  }, []);

  async function unlinkIdentity(identity: Identity) {
    setIdentityError(undefined);
    try {
      const result = await api<{ user: Me }>(`/auth/identities/${identity.id}`, { method: "DELETE" });
      setMe(result.user);
      setIdentities((current) => current.filter((item) => item.id !== identity.id));
    } catch (reason) {
      setIdentityError((reason as Error).message);
    }
  }

  useEffect(() => {
    api<UsageHistory>(`/usage/history?kind=${historyKind}`)
      .then((result) => {
        setHistory(result.items);
        setNextCursor(result.next_cursor);
        setHistoryError(undefined);
      })
      .catch(() => {
        setHistory([]);
        setNextCursor(undefined);
        setHistoryError("目前無法載入使用紀錄，請稍後再試。");
      })
      .finally(() => setHistoryBusy(false));
  }, [historyKind]);

  function selectHistoryKind(kind: HistoryKind) {
    if (kind === historyKind) return;
    setHistoryBusy(true);
    setHistory([]);
    setHistoryError(undefined);
    setHistoryKind(kind);
  }

  async function loadMore() {
    if (!nextCursor) return;
    setHistoryBusy(true);
    try {
      const result = await api<UsageHistory>(
        `/usage/history?kind=${historyKind}&cursor=${encodeURIComponent(nextCursor)}`,
      );
      setHistory((current) => [...current, ...result.items]);
      setNextCursor(result.next_cursor);
    } catch {
      setHistoryError("目前無法載入更多使用紀錄，請稍後再試。");
    } finally {
      setHistoryBusy(false);
    }
  }

  async function changePassword(form: FormData) {
    setBusy(true);
    setFormError(undefined);
    setDone(false);
    const newPassword = form.get("new_password");
    if (newPassword !== form.get("confirm_password")) {
      setFormError("兩次輸入的新密碼不一致");
      setBusy(false);
      return;
    }
    try {
      await api("/auth/change-password", {
        method: "POST",
        body: JSON.stringify({
          current_password: form.get("current_password"),
          new_password: newPassword,
        }),
      });
      setDone(true);
    } catch (reason) {
      setFormError((reason as Error).message);
    } finally {
      setBusy(false);
    }
  }

  if (loadError)
    return (
      <p className="rounded-xl bg-red-50 p-4 text-red-700">
        {loadError}，請先
        <Link className="underline" href="/login">
          登入
        </Link>
        。
      </p>
    );
  if (!me) return <p className="text-[var(--muted)]">正在載入帳號資料…</p>;
  const hasPassword = me.has_password !== false;
  const oauthLinkError = typeof window !== "undefined"
    && new URLSearchParams(window.location.search).has("oauth_error")
    ? accountT("linkFailed")
    : undefined;

  return (
    <div className="space-y-6">
      <section className="rounded-[2rem] border border-[var(--line)] bg-white p-6 md:p-8">
        <div className="flex flex-wrap items-start justify-between gap-4">
          <div>
            <h2 className="text-xl font-bold">帳號與使用次數</h2>
            <p className="mt-1 text-sm text-[var(--muted)]">
              次數不會按月歸零，成功取得可用查價結果才扣除。
            </p>
          </div>
          {featureEnabled(visibility, "pricing") && <Link
            href="/pricing"
            className="rounded-xl border border-[var(--teal)] px-4 py-2.5 text-sm font-semibold text-[var(--teal)]"
          >
            查看次數包
          </Link>}
        </div>
        <dl className="mt-6 grid gap-4 sm:grid-cols-3">
          <div className="rounded-2xl bg-[var(--paper)] p-4">
            <dt className="text-sm text-[var(--muted)]">會員 Email</dt>
            <dd className="mt-1 break-all font-semibold">{me.email}</dd>
          </div>
          <div className="rounded-2xl bg-[var(--teal-soft)] p-4">
            <dt className="text-sm text-[var(--teal-dark)]">目前可用</dt>
            <dd className="mt-1 text-3xl font-bold text-[var(--teal-dark)]">
              {usage ? `${usage.available_uses} 次` : "—"}
            </dd>
          </div>
          <div className="rounded-2xl bg-[var(--paper)] p-4">
            <dt className="text-sm text-[var(--muted)]">處理中保留</dt>
            <dd className="mt-1 text-2xl font-bold">
              {usage ? `${usage.reserved_uses} 次` : "—"}
            </dd>
          </div>
        </dl>
        {usage && (
          <p className="mt-4 text-sm text-[var(--muted)]">
            帳面剩餘 {usage.remaining_uses} 次；可儲存{" "}
            {usage.limits.saved_trips} 份旅程及建立 {usage.limits.price_alerts}{" "}
            個價格通知。
          </p>
        )}
      </section>

      <section className="rounded-[2rem] border border-[var(--line)] bg-white p-6 md:p-8">
        <h2 className="flex items-center gap-2 text-xl font-bold"><Link2 size={21} className="text-[var(--teal)]" />{accountT("signInMethods")}</h2>
        <p className="mt-1 text-sm text-[var(--muted)]">{accountT("signInMethodsHelp")}</p>
        {(identityError || oauthLinkError) && <p role="alert" className="mt-4 rounded-xl bg-red-50 p-3 text-sm text-red-800">{identityError || oauthLinkError}</p>}
        <div className="mt-5 space-y-3">
          {hasPassword && <div className="flex min-h-14 items-center justify-between rounded-2xl border border-[var(--line)] px-4"><span className="font-semibold">Email</span><span className="text-sm text-[var(--muted)]">{accountT("connected")}</span></div>}
          {identities.map((identity) => {
            const canUnlink = hasPassword || identities.length > 1;
            return <div key={identity.id} className="flex min-h-16 items-center justify-between gap-3 rounded-2xl border border-[var(--line)] px-4 py-3"><div className="min-w-0"><p className="font-semibold">{accountT(`providers.${identity.provider}`)}</p><p className="truncate text-xs text-[var(--muted)]">{maskEmail(identity.email) || accountT("emailUnavailable")}</p></div><button type="button" disabled={!canUnlink} onClick={() => void unlinkIdentity(identity)} className="flex min-h-11 shrink-0 items-center gap-2 rounded-xl px-3 text-sm font-semibold text-red-700 disabled:cursor-not-allowed disabled:opacity-40" title={!canUnlink ? accountT("keepOneMethod") : undefined}><Unlink size={16} />{accountT("disconnect")}</button></div>;
          })}
        </div>
        <div className="mt-5 grid gap-3 sm:grid-cols-3">
          {(["google", "line", "apple"] as Provider[]).filter((provider) => oauthProviders?.providers[provider]).map((provider) => <a key={provider} href={`/api/auth/oauth/${provider}/start?intent=link&locale=${locale}&next=%2Faccount`} className="flex min-h-12 items-center justify-center rounded-xl border border-[var(--line)] px-3 text-sm font-semibold text-[var(--teal)]">{accountT("connectProvider", { provider: accountT(`providers.${provider}`) })}</a>)}
        </div>
      </section>

      <section className="rounded-[2rem] border border-[var(--line)] bg-white p-6 md:p-8">
        <div className="flex flex-wrap items-start justify-between gap-4">
          <div>
            <h2 className="flex items-center gap-2 text-xl font-bold">
              <History size={21} className="text-[var(--teal)]" />
              使用紀錄
            </h2>
            <p className="mt-1 text-sm text-[var(--muted)]">
              每筆成功、失敗未扣與加值都有獨立流水號。
            </p>
          </div>
          <div className="flex flex-wrap gap-2">
            {historyFilters.map((item) => (
              <button
                key={item.key}
                onClick={() => selectHistoryKind(item.key)}
                aria-pressed={historyKind === item.key}
                className={`rounded-full border px-3 py-1.5 text-sm font-semibold ${historyKind === item.key ? "border-[var(--teal)] bg-[var(--teal)] text-white" : "border-[var(--line)] text-[var(--muted)]"}`}
              >
                {item.label}
              </button>
            ))}
          </div>
        </div>

        {historyBusy && history.length === 0 && (
          <p className="mt-6 flex items-center gap-2 text-sm text-[var(--muted)]">
            <LoaderCircle className="animate-spin" size={17} />
            正在載入使用紀錄…
          </p>
        )}
        {historyError && (
          <p
            role="alert"
            className="mt-6 rounded-xl bg-red-50 p-4 text-sm text-red-800"
          >
            {historyError}
          </p>
        )}
        {!historyBusy && !historyError && history.length === 0 && (
          <div className="mt-6 rounded-2xl border border-dashed border-[var(--line)] p-8 text-center text-[var(--muted)]">
            這個分類目前沒有紀錄。
          </div>
        )}
        {history.length > 0 && (
          <div className="mt-6 overflow-hidden rounded-2xl border border-[var(--line)]">
            <div className="hidden grid-cols-[9rem_1fr_8rem_6rem] gap-4 bg-[var(--paper)] px-4 py-3 text-xs font-semibold text-[var(--muted)] md:grid">
              <span>時間／狀態</span>
              <span>查詢摘要／流水號</span>
              <span>次數變動</span>
              <span>扣後餘額</span>
            </div>
            <ol className="divide-y divide-[var(--line)]">
              {history.map((item) => (
                <li
                  key={item.id}
                  className="grid gap-3 p-4 md:grid-cols-[9rem_1fr_8rem_6rem] md:items-center md:gap-4"
                >
                  <div>
                    <span
                      className={`inline-flex rounded-full px-2.5 py-1 text-xs font-semibold ${statusClass(item)}`}
                    >
                      {statusLabel(item)}
                    </span>
                    <time className="mt-2 block text-xs text-[var(--muted)]">
                      {dateFormat.format(new Date(item.occurred_at))}
                    </time>
                  </div>
                  <div className="min-w-0">
                    <p className="font-semibold">{item.summary}</p>
                    <p className="mt-1 flex min-w-0 items-center gap-1 text-xs text-[var(--muted)]">
                      <span className="truncate">流水號 {item.reference}</span>
                      <button
                        title="複製流水號"
                        aria-label={`複製流水號 ${item.reference}`}
                        onClick={() =>
                          navigator.clipboard?.writeText(item.reference)
                        }
                        className="shrink-0 rounded p-1 hover:bg-[var(--paper)]"
                      >
                        <Copy size={13} />
                      </button>
                    </p>
                  </div>
                  <strong
                    className={
                      item.change > 0
                        ? "text-[var(--teal)]"
                        : item.change < 0
                          ? "text-[#9d4e3f]"
                          : "text-emerald-700"
                    }
                  >
                    {changeLabel(item)}
                  </strong>
                  <span className="text-sm">
                    <span className="md:hidden text-[var(--muted)]">
                      扣後餘額{" "}
                    </span>
                    {item.balance_after} 次
                  </span>
                </li>
              ))}
            </ol>
          </div>
        )}
        {nextCursor && (
          <button
            onClick={loadMore}
            disabled={historyBusy}
            className="mt-4 w-full rounded-xl border border-[var(--line)] py-3 text-sm font-semibold disabled:opacity-50"
          >
            {historyBusy ? "載入中…" : "載入更多紀錄"}
          </button>
        )}
      </section>

      {hasPassword && <section className="rounded-[2rem] border border-[var(--line)] bg-white p-6 md:p-8">
        <h2 className="text-xl font-bold">修改密碼</h2>
        <form action={changePassword} className="mt-5 max-w-md space-y-4">
          <label className="block text-sm font-semibold">
            目前密碼
            <input
              required
              type="password"
              name="current_password"
              autoComplete="current-password"
              className={inputClass}
            />
          </label>
          <label className="block text-sm font-semibold">
            新密碼（至少 10 個字元）
            <input
              required
              minLength={10}
              maxLength={128}
              type="password"
              name="new_password"
              autoComplete="new-password"
              className={inputClass}
            />
          </label>
          <label className="block text-sm font-semibold">
            確認新密碼
            <input
              required
              minLength={10}
              maxLength={128}
              type="password"
              name="confirm_password"
              autoComplete="new-password"
              className={inputClass}
            />
          </label>
          {formError && (
            <p role="alert" className="text-sm text-red-700">
              {formError}
            </p>
          )}
          {done && (
            <p
              className="flex items-center gap-2 text-sm text-[var(--teal)]"
              role="status"
            >
              <Check size={16} />
              密碼已更新，下次登入請使用新密碼。
            </p>
          )}
          <button
            disabled={busy}
            className="rounded-xl bg-[var(--teal)] px-6 py-3.5 font-semibold text-white disabled:opacity-50"
          >
            {busy ? "處理中…" : "更新密碼"}
          </button>
        </form>
      </section>}
    </div>
  );
}
