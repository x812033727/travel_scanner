"use client";

import { AlertTriangle, CheckCircle2, Copy, ExternalLink, LoaderCircle, LogIn, LogOut, Plus, RefreshCw, Star, TerminalSquare, X } from "lucide-react";
import { useLocale, useTranslations } from "next-intl";
import { FormEvent, useCallback, useEffect, useMemo, useState } from "react";
import { api } from "@/lib/api";
import { useModalSheet } from "@/lib/modal-sheet";

type Tool = "claude" | "codex";
type Slot = "a" | "b" | "c" | "d" | "e";
type LoginStatus = "pending" | "verifying" | "succeeded" | "failed" | "cancelled" | "expired";
type Login = { id: string; tool: Tool; slot: Slot; kind: "device_code" | "paste_code"; status: LoginStatus; url?: string | null; user_code?: string | null; error?: string | null; expires_at: number };
type UsageWindow = { window_minutes?: number | null; used_percent: number; resets_at?: number | null };
type Usage = { source: "live" | "snapshot"; recorded_at?: number | null; windows: UsageWindow[] };
export type AiAccount = { tool: Tool; slot: Slot; is_default: boolean; logged_in: boolean | null; auth_method?: string | null; email?: string | null; organization?: string | null; plan?: string | null; email_allowed?: boolean | null; usage?: Usage | null; usage_error?: string | null; recorder_installed?: boolean | null; checked_at?: number | null; error?: string | null; login?: Login | null };
export type AiAccountsOverview = { enabled: boolean; agent_reachable: boolean; agent_error?: string | null; slots: AiAccount[]; defaults: Partial<Record<Tool, Slot>>; allowlist_configured: boolean };

const TOOLS: Tool[] = ["claude", "codex"];
const TOOL_NAMES: Record<Tool, string> = { claude: "Claude Code", codex: "Codex" };
// The sign-in methods billed to a subscription; anything else is API billing.
const SUBSCRIPTION_METHODS: Record<Tool, string> = { claude: "claude.ai", codex: "chatgpt" };
const ACTIVE = new Set<LoginStatus>(["pending", "verifying"]);
// What the Claude callback page shows: base64url pieces joined by `#`. The API and the host
// agent check the same pattern.
const CODE_PATTERN = /^[A-Za-z0-9._~#-]{10,1024}$/;
const REFRESH_MS = 60_000;
const LOGIN_POLL_MS = 3_000;
type Translator = ReturnType<typeof useTranslations>;

const loginOpen = (account: AiAccount) => Boolean(account.login && ACTIVE.has(account.login.status));
const slotLabel = (slot: Slot) => slot.toUpperCase();
const planLabel = (plan?: string | null) => plan ? plan.charAt(0).toUpperCase() + plan.slice(1) : undefined;

/** Signed-in accounts, the default, and any with a login open; the rest are free slots. */
export function visibleAccounts(accounts: AiAccount[]) {
  return accounts.filter((account) => account.logged_in !== false || account.is_default || loginOpen(account));
}

export function nextFreeSlot(accounts: AiAccount[]): Slot | undefined {
  const shown = new Set(visibleAccounts(accounts).map((account) => account.slot));
  return accounts.find((account) => !shown.has(account.slot))?.slot;
}

function windowLabel(t: Translator, minutes?: number | null) {
  if (minutes === 10_080) return t("windowWeekly");
  if (!minutes) return t("window");
  if (minutes % 1_440 === 0) return t("windowDays", { days: minutes / 1_440 });
  return t("windowHours", { hours: Math.round(minutes / 60) });
}

function relativeTime(format: Intl.RelativeTimeFormat, seconds: number) {
  const size = Math.abs(seconds);
  if (size < 60) return format.format(Math.round(seconds), "second");
  if (size < 3_600) return format.format(Math.round(seconds / 60), "minute");
  if (size < 86_400) return format.format(Math.round(seconds / 3_600), "hour");
  return format.format(Math.round(seconds / 86_400), "day");
}

function UsageBars({ usage, now }: { usage: Usage; now: number }) {
  const t = useTranslations("admin.aiAccountsPanel");
  const locale = useLocale();
  const dateTime = useMemo(() => new Intl.DateTimeFormat(locale, { month: "numeric", day: "numeric", hour: "2-digit", minute: "2-digit" }), [locale]);
  const relative = useMemo(() => new Intl.RelativeTimeFormat(locale, { numeric: "auto" }), [locale]);
  return <div className="mt-4 space-y-3">
    {usage.windows.map((window) => {
      const reset = Boolean(window.resets_at && window.resets_at * 1000 <= now);
      const remaining = reset ? 100 : Math.max(0, Math.min(100, Math.round(100 - window.used_percent)));
      const tone = remaining < 10 ? "bg-red-500" : remaining < 30 ? "bg-amber-500" : "bg-emerald-500";
      return <div key={`${window.window_minutes}-${window.resets_at}`}>
        <div className="flex items-baseline justify-between gap-3 text-sm">
          <span className="font-semibold">{windowLabel(t, window.window_minutes)}</span>
          <span className={`font-bold tabular-nums ${remaining < 10 ? "text-red-600" : ""}`}>{t("remaining", { percent: remaining })}</span>
        </div>
        <div className="mt-1.5 h-2 overflow-hidden rounded-full bg-slate-100" role="progressbar" aria-label={windowLabel(t, window.window_minutes)} aria-valuemin={0} aria-valuemax={100} aria-valuenow={remaining}>
          <div className={`h-full rounded-full ${tone}`} style={{ width: `${remaining}%` }} />
        </div>
        {window.resets_at ? <p className="mt-1 text-xs text-[var(--muted)]">{reset ? t("resetDone") : `${t("resetsAt", { time: dateTime.format(new Date(window.resets_at * 1000)) })} · ${relativeTime(relative, window.resets_at - now / 1000)}`}</p> : null}
      </div>;
    })}
    {usage.source === "snapshot" && usage.recorded_at ? <p className="text-xs text-[var(--muted)]">{t("snapshotAge", { relative: relativeTime(relative, usage.recorded_at - now / 1000) })}</p> : null}
  </div>;
}

type CardProps = {
  account: AiAccount; now: number; busy: boolean;
  onLogin: (account: AiAccount) => void; onLogout: (account: AiAccount) => void; onDefault: (account: AiAccount) => void;
};

function AccountCard({ account, now, busy, onLogin, onLogout, onDefault }: CardProps) {
  const t = useTranslations("admin.aiAccountsPanel");
  const [confirming, setConfirming] = useState(false);
  const signedIn = account.logged_in === true;
  const pending = loginOpen(account);
  const apiBilling = signedIn && account.auth_method && account.auth_method !== SUBSCRIPTION_METHODS[account.tool];
  return <article className="flex flex-col rounded-2xl border border-[var(--line)] bg-white p-5" aria-label={`${TOOL_NAMES[account.tool]} ${t("slotTitle", { slot: slotLabel(account.slot) })}`}>
    <div className="flex flex-wrap items-center gap-2">
      <h3 className="text-base font-bold">{t("slotTitle", { slot: slotLabel(account.slot) })}</h3>
      {account.is_default && <span className="inline-flex items-center gap-1 rounded-full bg-[var(--teal)]/10 px-2 py-0.5 text-xs font-bold text-[var(--teal)]"><Star size={12} />{t("default")}</span>}
      {signedIn && planLabel(account.plan) && <span className="rounded-full bg-slate-100 px-2 py-0.5 text-xs font-bold">{planLabel(account.plan)}</span>}
    </div>
    <p className="mt-2 break-all text-sm font-semibold">{signedIn ? account.email || account.organization || "—" : account.logged_in === null ? t("unknownState") : t("notSignedIn")}</p>
    {account.email_allowed === false && <p className="mt-2 flex items-center gap-1 text-xs font-bold text-red-700"><AlertTriangle size={13} />{t("notAllowed")}</p>}
    {apiBilling && <p className="mt-2 flex items-center gap-1 text-xs font-bold text-amber-800"><AlertTriangle size={13} />{t("apiBilling")}</p>}
    {account.error && <p className="mt-2 text-xs text-red-700">{account.error}</p>}
    {signedIn && account.usage?.windows.length ? <UsageBars usage={account.usage} now={now} /> : null}
    {signedIn && account.tool === "claude" && !account.usage && <p className="mt-4 rounded-xl bg-[var(--paper)] p-3 text-xs leading-5 text-[var(--muted)]">{t("snapshotMissing")}</p>}
    {signedIn && account.tool === "claude" && account.recorder_installed === false && <p className="mt-2 text-xs text-amber-800">{t("recorderMissing")}</p>}
    {signedIn && account.usage_error && <p className="mt-2 text-xs text-amber-800">{t("usageUnavailable", { detail: account.usage_error })}</p>}
    <div className="mt-auto flex flex-wrap gap-2 pt-5">
      {pending ? <button type="button" onClick={() => onLogin(account)} className="inline-flex min-h-10 items-center gap-1.5 rounded-xl bg-[var(--coral-fill)] px-3.5 text-sm font-bold text-white"><LoaderCircle size={15} className="animate-spin motion-reduce:animate-none" />{t("resume")}</button>
        : <button type="button" disabled={busy} onClick={() => onLogin(account)} className="inline-flex min-h-10 items-center gap-1.5 rounded-xl border border-[var(--line)] px-3.5 text-sm font-bold disabled:opacity-40"><LogIn size={15} />{signedIn ? t("signInAgain") : t("signIn")}</button>}
      {signedIn && !account.is_default && <button type="button" disabled={busy} onClick={() => onDefault(account)} className="inline-flex min-h-10 items-center gap-1.5 rounded-xl border border-[var(--line)] px-3.5 text-sm font-bold disabled:opacity-40"><Star size={15} />{t("makeDefault")}</button>}
      {signedIn && (confirming
        ? <><button type="button" disabled={busy} onClick={() => { setConfirming(false); onLogout(account); }} className="inline-flex min-h-10 items-center gap-1.5 rounded-xl bg-red-600 px-3.5 text-sm font-bold text-white disabled:opacity-40"><LogOut size={15} />{t("confirmSignOut")}</button><button type="button" onClick={() => setConfirming(false)} className="min-h-10 rounded-xl px-3 text-sm font-bold text-[var(--muted)]">{t("cancel")}</button></>
        : <button type="button" disabled={busy} onClick={() => setConfirming(true)} className="inline-flex min-h-10 items-center gap-1.5 rounded-xl px-3 text-sm font-bold text-red-700 disabled:opacity-40"><LogOut size={15} />{t("signOut")}</button>)}
    </div>
  </article>;
}

function LoginDialog({ login, busy, onClose, onCancel, onSubmitCode }: { login: Login; busy: boolean; onClose: () => void; onCancel: () => void; onSubmitCode: (code: string) => void }) {
  const t = useTranslations("admin.aiAccountsPanel");
  const locale = useLocale();
  const [code, setCode] = useState("");
  const [copied, setCopied] = useState(false);
  const sheetRef = useModalSheet<HTMLDivElement>(true, onClose);
  const timeFormat = useMemo(() => new Intl.DateTimeFormat(locale, { hour: "2-digit", minute: "2-digit" }), [locale]);
  const active = ACTIVE.has(login.status);
  const slot = slotLabel(login.slot);
  const trimmed = code.trim();

  function submit(event: FormEvent) {
    event.preventDefault();
    if (CODE_PATTERN.test(trimmed)) onSubmitCode(trimmed);
  }
  async function copy() {
    if (!login.user_code) return;
    try { await navigator.clipboard.writeText(login.user_code); setCopied(true); } catch { setCopied(false); }
  }

  return <div role="presentation" className="fixed inset-0 z-50 grid place-items-center bg-black/55 p-4" onMouseDown={(event) => { if (event.currentTarget === event.target) onClose(); }}>
    <div role="dialog" aria-modal="true" aria-labelledby="ai-login-title" ref={sheetRef} className="max-h-[90vh] w-full max-w-lg overflow-y-auto rounded-[1.75rem] bg-white p-6 shadow-2xl md:p-8">
      <div className="flex items-start justify-between gap-4">
        <h2 id="ai-login-title" className="text-xl font-black">{login.tool === "codex" ? t("loginTitleCodex", { slot }) : t("loginTitleClaude", { slot })}</h2>
        <button type="button" aria-label={t("closeLogin")} onClick={onClose} className="rounded-lg p-2 hover:bg-slate-100"><X /></button>
      </div>
      {login.status === "pending" && login.url && <ol className="mt-5 space-y-5 text-sm leading-6">
        <li><p>{login.kind === "device_code" ? t("codexStep1") : t("claudeStep1")}</p><a href={login.url} target="_blank" rel="noreferrer noopener" className="mt-2 inline-flex min-h-11 items-center gap-2 rounded-xl bg-[var(--ink)] px-4 font-bold text-white">{t("openLoginPage")}<ExternalLink size={15} /></a></li>
        {login.kind === "device_code" && login.user_code ? <li>
          <p>{t("codexStep2")}</p>
          <div className="mt-2 flex flex-wrap items-center gap-3"><code className="rounded-xl bg-[var(--paper)] px-4 py-3 font-mono text-2xl font-black tracking-widest">{login.user_code}</code><button type="button" onClick={() => void copy()} className="inline-flex min-h-10 items-center gap-1.5 rounded-xl border border-[var(--line)] px-3 font-bold">{copied ? <CheckCircle2 size={15} /> : <Copy size={15} />}{copied ? t("copied") : t("copyCode")}</button></div>
          <p className="mt-3 text-xs text-[var(--muted)]">{t("codexDeviceHint")}</p>
        </li> : <li>
          <form onSubmit={submit}>
            <label htmlFor="ai-login-code">{t("claudeStep2")}</label>
            <input id="ai-login-code" value={code} onChange={(event) => setCode(event.target.value)} autoComplete="off" spellCheck={false} maxLength={1100} className="mt-2 w-full rounded-xl border border-[var(--line)] px-4 py-3 font-mono text-sm" />
            <button type="submit" disabled={busy || !CODE_PATTERN.test(trimmed)} className="mt-3 inline-flex min-h-11 items-center gap-2 rounded-xl bg-[var(--coral-fill)] px-4 font-bold text-white disabled:opacity-40">{busy ? <LoaderCircle size={16} className="animate-spin motion-reduce:animate-none" /> : <LogIn size={16} />}{t("submitCode")}</button>
          </form>
        </li>}
      </ol>}
      <div role="status" aria-live="polite" className="mt-6 text-sm">
        {login.status === "pending" && <p className="flex items-center gap-2 text-[var(--muted)]"><LoaderCircle size={16} className="animate-spin motion-reduce:animate-none" />{login.kind === "device_code" ? t("waitingBrowser") : t("waitingCode")} · {t("expiresAt", { time: timeFormat.format(new Date(login.expires_at * 1000)) })}</p>}
        {login.status === "verifying" && <p className="flex items-center gap-2 text-[var(--muted)]"><LoaderCircle size={16} className="animate-spin motion-reduce:animate-none" />{t("verifying")}</p>}
        {login.status === "succeeded" && <p className="flex items-center gap-2 font-bold text-emerald-700"><CheckCircle2 size={16} />{t("succeeded")}</p>}
        {login.status === "failed" && <p className="font-bold text-red-700">{t("failed", { detail: login.error || "—" })}</p>}
        {login.status === "cancelled" && <p className="text-[var(--muted)]">{t("cancelled")}</p>}
        {login.status === "expired" && <p className="text-[var(--muted)]">{t("expired")}</p>}
        {(login.status === "failed" || login.status === "expired") && <p className="mt-2 flex items-start gap-1.5 text-xs text-[var(--muted)]"><TerminalSquare size={14} className="mt-0.5 shrink-0" />{login.tool === "codex" ? t("fallbackCodex", { slot: login.slot }) : t("fallbackClaude", { slot: login.slot })}</p>}
      </div>
      <div className="mt-6 flex justify-end gap-2">
        {active ? <button type="button" disabled={busy} onClick={onCancel} className="min-h-11 rounded-xl border border-[var(--line)] px-4 font-bold disabled:opacity-40">{t("cancelLogin")}</button>
          : <button type="button" onClick={onClose} className="min-h-11 rounded-xl bg-[var(--ink)] px-5 font-bold text-white">{t("done")}</button>}
      </div>
    </div>
  </div>;
}

export function AdminAiAccountsPanel() {
  const t = useTranslations("admin.aiAccountsPanel");
  const locale = useLocale();
  const dateTime = useMemo(() => new Intl.DateTimeFormat(locale, { dateStyle: "medium", timeStyle: "short" }), [locale]);
  const [overview, setOverview] = useState<AiAccountsOverview>();
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string>();
  const [login, setLogin] = useState<Login>();
  const [loadedAt, setLoadedAt] = useState(() => Date.now());

  const load = useCallback(async (fresh = false) => {
    if (fresh) setRefreshing(true);
    try {
      setOverview(await api<AiAccountsOverview>(`/admin/ai-accounts${fresh ? "?fresh=true" : ""}`));
      setLoadedAt(Date.now());
      setError(undefined);
    } catch (reason) {
      setError((reason as Error).message);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, []);

  useEffect(() => {
    // Deferred a tick so the first render commits before the request state changes.
    const first = setTimeout(() => void load(), 0);
    const timer = setInterval(() => void load(), REFRESH_MS);
    return () => { clearTimeout(first); clearInterval(timer); };
  }, [load]);

  const loginId = login?.id;
  const loginActive = login ? ACTIVE.has(login.status) : false;
  useEffect(() => {
    if (!loginId || !loginActive) return;
    let cancelled = false;
    const timer = setTimeout(async () => {
      try {
        const next = await api<Login>(`/admin/ai-accounts/logins/${loginId}`);
        if (cancelled) return;
        setLogin(next);
        if (next.status === "succeeded") void load(true);
      } catch (reason) {
        // Try again on the next tick; a login outlives one failed poll.
        if (!cancelled) setError((reason as Error).message);
        if (!cancelled) setLogin((current) => current ? { ...current } : current);
      }
    }, LOGIN_POLL_MS);
    return () => { cancelled = true; clearTimeout(timer); };
  }, [loginId, loginActive, login, load]);

  async function run<T>(action: () => Promise<T>): Promise<T | undefined> {
    setBusy(true); setError(undefined);
    try { return await action(); }
    catch (reason) { setError((reason as Error).message); return undefined; }
    finally { setBusy(false); }
  }

  async function startLogin(account: AiAccount) {
    if (account.login && ACTIVE.has(account.login.status)) { setLogin(account.login); return; }
    const started = await run(() => api<Login>(`/admin/ai-accounts/${account.tool}/${account.slot}/login`, { method: "POST" }));
    if (started) setLogin(started);
  }
  async function submitCode(code: string) {
    if (!login) return;
    const next = await run(() => api<Login>(`/admin/ai-accounts/logins/${login.id}/code`, { method: "POST", body: JSON.stringify({ code }) }));
    if (next) setLogin(next);
  }
  async function cancelLogin() {
    if (!login) return;
    const next = await run(() => api<Login>(`/admin/ai-accounts/logins/${login.id}/cancel`, { method: "POST" }));
    if (next) setLogin(next);
    void load();
  }
  async function signOut(account: AiAccount) {
    const done = await run(() => api(`/admin/ai-accounts/${account.tool}/${account.slot}/logout`, { method: "POST" }));
    if (done) void load(true);
  }
  async function makeDefault(account: AiAccount) {
    const done = await run(() => api(`/admin/ai-accounts/defaults/${account.tool}`, { method: "PUT", body: JSON.stringify({ slot: account.slot }) }));
    if (done) void load();
  }
  function closeLogin() {
    setLogin(undefined);
    void load();
  }

  if (loading) return <div className="mt-8 flex items-center gap-2 rounded-2xl border border-[var(--line)] bg-white p-6 text-sm text-[var(--muted)]"><LoaderCircle size={18} className="animate-spin motion-reduce:animate-none" />{t("loading")}</div>;

  const now = loadedAt;
  return <div className="mt-8 space-y-6">
    {error && <div role="alert" className="flex items-start justify-between gap-3 rounded-2xl bg-red-50 p-4 text-sm text-red-900"><span>{error}</span><button type="button" aria-label={t("closeError")} onClick={() => setError(undefined)}><X size={18} /></button></div>}
    {overview && !overview.enabled && <section className="rounded-2xl bg-amber-50 p-5 text-sm leading-6 text-amber-950"><h2 className="font-bold">{t("disabledTitle")}</h2><p className="mt-1">{t("disabledBody")}</p></section>}
    {overview?.enabled && !overview.agent_reachable && <p role="status" className="rounded-2xl bg-amber-50 p-4 text-sm text-amber-950">{t("agentOffline", { detail: overview.agent_error || "—" })}</p>}
    {overview?.enabled && overview.agent_reachable && !overview.allowlist_configured && <p className="flex items-start gap-2 rounded-2xl bg-amber-50 p-4 text-sm text-amber-950"><AlertTriangle size={16} className="mt-0.5 shrink-0" />{t("allowlistMissing")}</p>}
    {overview?.enabled && <div className="flex flex-wrap items-center justify-between gap-3">
      <p className="text-xs text-[var(--muted)]">{t("checkedAt", { time: dateTime.format(new Date(loadedAt)) })}</p>
      <button type="button" disabled={refreshing} onClick={() => void load(true)} className="inline-flex min-h-10 items-center gap-2 rounded-xl border border-[var(--line)] bg-white px-4 text-sm font-bold disabled:opacity-40"><RefreshCw size={15} className={refreshing ? "animate-spin motion-reduce:animate-none" : ""} />{refreshing ? t("refreshing") : t("refresh")}</button>
    </div>}
    {overview?.enabled && overview.agent_reachable && TOOLS.map((tool) => {
      const accounts = overview.slots.filter((account) => account.tool === tool);
      const shown = visibleAccounts(accounts);
      const free = nextFreeSlot(accounts);
      return <section key={tool} aria-labelledby={`ai-${tool}-title`} className="rounded-[1.75rem] border border-[var(--line)] bg-[var(--paper)] p-5 md:p-7">
        <h2 id={`ai-${tool}-title`} className="text-xl font-bold">{TOOL_NAMES[tool]}</h2>
        <p className="mt-1 flex items-start gap-1.5 text-sm text-[var(--muted)]"><TerminalSquare size={15} className="mt-0.5 shrink-0" />{tool === "claude" ? t("sshHintClaude") : t("sshHintCodex")}</p>
        <div className="mt-5 grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
          {shown.map((account) => <AccountCard key={account.slot} account={account} now={now} busy={busy} onLogin={(item) => void startLogin(item)} onLogout={(item) => void signOut(item)} onDefault={(item) => void makeDefault(item)} />)}
          <div className="flex flex-col items-start justify-center rounded-2xl border border-dashed border-[var(--line)] p-5">
            {free ? <>
              <button type="button" disabled={busy} onClick={() => void startLogin({ tool, slot: free, is_default: false, logged_in: false })} className="inline-flex min-h-10 items-center gap-1.5 rounded-xl bg-[var(--ink)] px-4 text-sm font-bold text-white disabled:opacity-40"><Plus size={15} />{t("addAccount")}</button>
              <p className="mt-2 text-xs text-[var(--muted)]">{t("addAccountHint", { slot: slotLabel(free) })}</p>
            </> : <p className="text-xs text-[var(--muted)]">{t("noFreeSlot")}</p>}
          </div>
        </div>
      </section>;
    })}
    {login && <LoginDialog login={login} busy={busy} onClose={closeLogin} onCancel={() => void cancelLogin()} onSubmitCode={(code) => void submitCode(code)} />}
  </div>;
}
