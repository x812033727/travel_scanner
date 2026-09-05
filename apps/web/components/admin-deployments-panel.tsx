"use client";

import { AlertTriangle, CheckCircle2, CloudCog, ExternalLink, LoaderCircle, RefreshCw, RotateCcw, ServerCog, ShieldCheck, X } from "lucide-react";
import { FormEvent, useEffect, useMemo, useRef, useState } from "react";
import { api } from "@/lib/api";

type Status = "queued" | "preflight" | "building" | "backing_up" | "migrating" | "activating" | "verifying" | "rolling_back" | "succeeded" | "failed" | "rolled_back" | "manual_intervention_required";
type Check = { name: string; status: "ok" | "warning" | "failed"; detail: string };
type Event = { sequence: number; stage: string; status: string; message: string; created_at: string };
type Run = { id: string; requested_by_email?: string; status: Status; stage: string; previous_sha?: string; target_sha: string; target_commit_subject?: string; ci_url?: string; backup_name?: string; rollback_status?: string; failure_code?: string; failure_detail?: string; started_at?: string; finished_at?: string; created_at: string; updated_at: string; events: Event[] };
type Overview = { enabled: boolean; agent_connected: boolean; deployed_sha?: string; target_sha?: string; target_commit_subject?: string; update_available: boolean; ci_status: string; ci_url?: string; commits: { sha: string; subject: string }[]; checks: Check[]; active_run?: Run; last_success?: Run; cooldown_until?: string };
type RunList = { items: Run[] };
type Preflight = { ok: boolean; checked_at: string; checks: Check[]; target_sha?: string };

const terminal = new Set<Status>(["succeeded", "failed", "rolled_back", "manual_intervention_required"]);
const stages = ["queued", "preflight", "building", "backing_up", "migrating", "activating", "verifying"];
const labels: Record<string, string> = { queued: "已排入", preflight: "環境檢查", building: "建置映像", backing_up: "資料庫備份", migrating: "資料庫升級", activating: "啟動服務", verifying: "健康驗證", rolling_back: "自動回退", succeeded: "部署成功", failed: "部署失敗", rolled_back: "已回退", manual_intervention_required: "需要人工處理", git: "Git", docker: "Docker", compose: "Docker Compose", disk: "磁碟空間", runtime_env: "Runtime 環境", database: "PostgreSQL", pg_dump: "備份工具", github_ci: "GitHub CI", api: "API", web: "Web" };
const dateTime = new Intl.DateTimeFormat("zh-TW", { dateStyle: "medium", timeStyle: "medium" });
const shortSha = (value?: string) => value ? value.slice(0, 7) : "尚無";
const ciUrl = (value?: string) => value?.startsWith("https://github.com/") ? value : undefined;
const elapsed = (run: Run) => {
  if (!run.started_at || !run.finished_at) return "—";
  const seconds = Math.max(0, Math.round((Date.parse(run.finished_at) - Date.parse(run.started_at)) / 1000));
  return seconds < 60 ? `${seconds} 秒` : `${Math.floor(seconds / 60)} 分 ${seconds % 60} 秒`;
};

function StatusPill({ status }: { status: Status }) {
  const tone = status === "succeeded" ? "bg-emerald-50 text-emerald-800" : status === "rolling_back" || status === "rolled_back" ? "bg-amber-50 text-amber-800" : terminal.has(status) ? "bg-red-50 text-red-800" : "bg-sky-50 text-sky-800";
  return <span className={`inline-flex items-center gap-1 rounded-full px-2.5 py-1 text-xs font-bold ${tone}`}>{status === "succeeded" ? <CheckCircle2 size={13} /> : terminal.has(status) ? <AlertTriangle size={13} /> : <LoaderCircle size={13} className="animate-spin" />}{labels[status] || status}</span>;
}

export function AdminDeploymentsPanel() {
  const [overview, setOverview] = useState<Overview>();
  const [history, setHistory] = useState<Run[]>([]);
  const [preflight, setPreflight] = useState<Preflight>();
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string>();
  const [reconnecting, setReconnecting] = useState(false);
  const [confirmOpen, setConfirmOpen] = useState(false);
  const [password, setPassword] = useState("");
  const [confirmation, setConfirmation] = useState("");
  const deployButtonRef = useRef<HTMLButtonElement>(null);
  const passwordRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (confirmOpen) passwordRef.current?.focus();
  }, [confirmOpen]);

  function closeConfirmation() {
    if (busy) return;
    setConfirmOpen(false);
    requestAnimationFrame(() => deployButtonRef.current?.focus());
  }

  useEffect(() => {
    let active = true;
    Promise.all([api<Overview>("/admin/deployments/overview"), api<RunList>("/admin/deployments?limit=20")])
      .then(([next, runs]) => { if (active) { setOverview(next); setHistory(runs.items); setError(undefined); } })
      .catch((reason: Error) => { if (active) setError(reason.message); })
      .finally(() => { if (active) setLoading(false); });
    return () => { active = false; };
  }, []);

  useEffect(() => {
    if (!overview?.active_run || terminal.has(overview.active_run.status)) return;
    let cancelled = false;
    let delay = 2_000;
    // No deadline: a real deploy (image build + backup + migration + health
    // checks) routinely outlives the old 5-minute cap, after which the panel
    // silently froze mid-stage and the spinner span forever. Poll until the
    // run reaches a terminal state, easing off after the first five minutes.
    const startedAt = Date.now();
    let timer: ReturnType<typeof setTimeout>;
    const poll = async () => {
      if (cancelled) return;
      try {
        const next = await api<Overview>("/admin/deployments/overview");
        if (cancelled) return;
        setOverview(next); setReconnecting(false);
        delay = Date.now() - startedAt > 5 * 60_000 ? 10_000 : 2_000;
        if (!next.active_run || terminal.has(next.active_run.status)) {
          const runs = await api<RunList>("/admin/deployments?limit=20");
          if (!cancelled) setHistory(runs.items);
          return;
        }
      } catch { setReconnecting(true); delay = Math.min(10_000, delay * 2); }
      timer = setTimeout(poll, delay);
    };
    timer = setTimeout(poll, delay);
    return () => { cancelled = true; clearTimeout(timer); };
  }, [overview?.active_run]);

  const disabledReason = useMemo(() => {
    if (!overview) return "正在讀取部署狀態";
    if (!overview.enabled) return "主機尚未啟用部署功能";
    if (!overview.agent_connected) return "部署代理未連線";
    if (overview.active_run && !terminal.has(overview.active_run.status)) return "已有部署正在執行";
    if (overview.cooldown_until) return `冷卻至 ${dateTime.format(new Date(overview.cooldown_until))}`;
    if (overview.ci_status !== "success") return "最新 main 尚未通過 CI";
    if (!overview.update_available) return "目前已是最新綠燈版本";
    return undefined;
  }, [overview]);

  async function runPreflight() {
    setBusy(true); setError(undefined);
    try { setPreflight(await api<Preflight>("/admin/deployments/preflight", { method: "POST" })); }
    catch (reason) { setError((reason as Error).message); }
    finally { setBusy(false); }
  }
  async function submit(event: FormEvent) {
    event.preventDefault();
    if (!overview?.target_sha) return;
    setBusy(true); setError(undefined);
    try {
      const run = await api<Run>("/admin/deployments", { method: "POST", headers: { "Idempotency-Key": `deploy-${crypto.randomUUID()}` }, body: JSON.stringify({ expected_target_sha: overview.target_sha, password, confirmation }) });
      setOverview({ ...overview, active_run: run, update_available: false });
      setHistory((items) => [run, ...items.filter((item) => item.id !== run.id)]);
      setPassword(""); setConfirmation(""); setConfirmOpen(false);
    } catch (reason) { setError((reason as Error).message); }
    finally { setBusy(false); }
  }

  if (loading) return <div className="mt-8 flex items-center gap-2 rounded-2xl border border-[var(--line)] bg-white p-6 text-sm text-[var(--muted)]"><LoaderCircle size={18} className="animate-spin" />正在連線部署代理…</div>;
  const checks = preflight?.checks || overview?.checks || [];
  const active = overview?.active_run;

  return <div className="mt-8 space-y-6">
    {error && <div role="alert" className="flex items-start justify-between gap-3 rounded-2xl bg-red-50 p-4 text-sm text-red-900"><span>{error}</span><button type="button" aria-label="關閉錯誤" onClick={() => setError(undefined)}><X size={18} /></button></div>}
    {reconnecting && <p role="status" className="rounded-2xl bg-amber-50 p-4 text-sm text-amber-900">服務正在重新啟動，部署紀錄仍保存在主機代理；系統會繼續重新連線。</p>}
    <section className="overflow-hidden rounded-[2rem] bg-[var(--ink)] p-6 text-white shadow-lg md:p-8"><div className="grid gap-8 lg:grid-cols-[1.2fr_.8fr] lg:items-end"><div><p className="text-xs font-bold tracking-[.18em] text-white/60">PRODUCTION RELEASE</p><div className="mt-4 flex flex-wrap items-center gap-3"><span className="font-mono text-4xl font-black">{shortSha(overview?.deployed_sha)}</span><span className="text-white/40">→</span><span className="font-mono text-4xl font-black text-[var(--coral)]">{shortSha(overview?.target_sha)}</span></div><p className="mt-3 max-w-2xl text-sm leading-6 text-white/70">{overview?.target_commit_subject || "尚未取得最新 main commit 摘要"}</p></div><div className="flex flex-col gap-3 sm:flex-row lg:justify-end"><button type="button" onClick={() => void runPreflight()} disabled={busy} className="inline-flex min-h-11 items-center justify-center gap-2 rounded-xl border border-white/25 px-4 py-3 text-sm font-bold disabled:opacity-40"><RefreshCw size={17} className={busy ? "animate-spin motion-reduce:animate-none" : ""} />重新檢查環境</button><button ref={deployButtonRef} type="button" onClick={() => setConfirmOpen(true)} disabled={Boolean(disabledReason) || busy} title={disabledReason} className="inline-flex min-h-11 items-center justify-center gap-2 rounded-xl bg-[var(--coral)] px-5 py-3 text-sm font-black text-[var(--ink)] disabled:cursor-not-allowed disabled:opacity-45"><CloudCog size={18} />部署最新版本</button></div></div>{disabledReason && <p className="mt-4 text-xs text-white/55">{disabledReason}</p>}</section>
    <section aria-label="部署環境狀態" className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">{checks.map((check) => <div key={`${check.name}-${check.detail}`} className="rounded-2xl border border-[var(--line)] bg-white p-5"><div className="flex items-center justify-between"><span className="text-xs font-bold text-[var(--muted)]">{labels[check.name] || check.name}</span>{check.status === "ok" ? <CheckCircle2 size={18} className="text-emerald-600" /> : <AlertTriangle size={18} className={check.status === "failed" ? "text-red-600" : "text-amber-600"} />}</div><p className="mt-3 text-sm font-semibold">{check.detail}</p></div>)}<div className="rounded-2xl border border-[var(--line)] bg-white p-5"><div className="flex items-center justify-between"><span className="text-xs font-bold text-[var(--muted)]">GitHub CI</span><ShieldCheck size={18} className={overview?.ci_status === "success" ? "text-emerald-600" : "text-amber-600"} /></div><p className="mt-3 text-sm font-semibold">{overview?.ci_status === "success" ? "最新 main 已通過" : `狀態：${overview?.ci_status || "unknown"}`}</p>{ciUrl(overview?.ci_url) && <a className="mt-2 inline-flex items-center gap-1 text-xs font-bold text-[var(--teal)]" href={overview?.ci_url} target="_blank" rel="noreferrer">查看 CI <ExternalLink size={12} /></a>}</div></section>
    {active && <section className="rounded-[1.75rem] border border-[var(--line)] bg-white p-6 shadow-sm md:p-8"><div className="flex flex-wrap items-center justify-between gap-3"><div><p className="text-xs font-bold tracking-[.14em] text-[var(--teal)]">ACTIVE DEPLOYMENT</p><h2 className="mt-2 text-2xl font-bold">正在部署 {shortSha(active.target_sha)}</h2></div><StatusPill status={active.status} /></div><div className="mt-7 grid grid-cols-2 gap-y-5 sm:grid-cols-4 lg:grid-cols-7">{stages.map((stage, index) => { const currentIndex = stages.indexOf(active.stage); const done = terminal.has(active.status) || index < currentIndex; const current = stage === active.stage; return <div key={stage}><span className={`flex size-8 items-center justify-center rounded-full text-xs font-black ${done ? "bg-emerald-600 text-white" : current ? "bg-[var(--coral)] text-[var(--ink)]" : "bg-slate-100 text-slate-500"}`}>{done ? "✓" : index + 1}</span><p className="mt-2 text-xs font-bold">{labels[stage]}</p></div>; })}</div><div className="mt-7 space-y-2 border-t border-[var(--line)] pt-5">{active.events.slice(-6).map((event) => <div key={event.sequence} className="flex gap-3 text-sm"><time className="shrink-0 text-xs text-[var(--muted)]">{dateTime.format(new Date(event.created_at))}</time><p>{event.message}</p></div>)}</div></section>}
    {overview?.commits?.length ? <section className="rounded-[1.75rem] border border-[var(--line)] bg-white p-6 md:p-8"><h2 className="text-xl font-bold">待部署變更</h2><div className="mt-4 divide-y divide-[var(--line)]">{overview.commits.map((commit) => <div key={commit.sha} className="grid gap-1 py-3 sm:grid-cols-[7rem_1fr]"><code className="text-sm font-bold text-[var(--teal)]">{shortSha(commit.sha)}</code><p className="text-sm">{commit.subject}</p></div>)}</div></section> : null}
    <section className="rounded-[1.75rem] border border-[var(--line)] bg-white p-6 md:p-8"><div className="flex items-center gap-3"><ServerCog className="text-[var(--teal)]" /><div><h2 className="text-xl font-bold">部署歷史</h2><p className="text-sm text-[var(--muted)]">只顯示安全清理後的階段與結果，不公開主機原始 log。</p></div></div>{history.length ? <div className="mt-5 overflow-x-auto"><table className="w-full min-w-[820px] text-left text-sm"><thead><tr className="border-b border-[var(--line)] text-xs text-[var(--muted)]"><th className="px-3 py-3">時間</th><th className="px-3 py-3">版本</th><th className="px-3 py-3">請求人</th><th className="px-3 py-3">結果</th><th className="px-3 py-3">耗時</th><th className="px-3 py-3">備份／回退</th></tr></thead><tbody>{history.map((run) => <tr key={run.id} className="border-b border-[var(--line)] last:border-0"><td className="px-3 py-4 text-[var(--muted)]">{dateTime.format(new Date(run.created_at))}</td><td className="px-3 py-4 font-mono font-bold">{shortSha(run.target_sha)}</td><td className="px-3 py-4">{run.requested_by_email || "已刪除帳號"}</td><td className="px-3 py-4"><StatusPill status={run.status} /></td><td className="px-3 py-4">{elapsed(run)}</td><td className="px-3 py-4 text-xs"><span>{run.backup_name ? "已備份" : "未建立備份"}</span>{run.rollback_status && <span className="ml-2 inline-flex items-center gap-1 text-amber-800"><RotateCcw size={12} />{run.rollback_status}</span>}</td></tr>)}</tbody></table></div> : <p className="mt-5 rounded-xl bg-[var(--paper)] p-5 text-sm text-[var(--muted)]">目前沒有部署紀錄。</p>}</section>
    {confirmOpen && overview?.target_sha && <div role="presentation" className="fixed inset-0 z-50 grid place-items-center bg-black/55 p-4" onMouseDown={(event) => { if (event.currentTarget === event.target) closeConfirmation(); }}><form role="dialog" aria-modal="true" aria-labelledby="deploy-confirm-title" onKeyDown={(event) => { if (event.key === "Escape") closeConfirmation(); }} onSubmit={submit} className="max-h-[90vh] w-full max-w-xl overflow-y-auto rounded-[1.75rem] bg-white p-6 shadow-2xl md:p-8"><div className="flex items-start justify-between gap-4"><div><p className="text-xs font-bold tracking-[.14em] text-[var(--coral)]">PRODUCTION CHANGE</p><h2 id="deploy-confirm-title" className="mt-2 text-2xl font-black">確認部署 {shortSha(overview.target_sha)}</h2></div><button type="button" aria-label="關閉部署確認" disabled={busy} onClick={closeConfirmation} className="rounded-lg p-2 hover:bg-slate-100"><X /></button></div><div className="mt-5 rounded-2xl bg-amber-50 p-4 text-sm leading-6 text-amber-950"><strong>可能有短暫中斷。</strong>部署前會建立 PostgreSQL 備份；新版本健康檢查失敗時只回退應用程式，不會降級 migration 或自動還原資料庫。</div><label className="mt-6 block text-sm font-bold" htmlFor="deploy-password">目前密碼</label><input ref={passwordRef} id="deploy-password" type="password" autoComplete="current-password" required maxLength={128} value={password} onChange={(event) => setPassword(event.target.value)} className="mt-2 w-full rounded-xl border border-[var(--line)] px-4 py-3" /><label className="mt-5 block text-sm font-bold" htmlFor="deploy-confirmation">輸入 <code>DEPLOY {shortSha(overview.target_sha)}</code></label><input id="deploy-confirmation" required maxLength={32} value={confirmation} onChange={(event) => setConfirmation(event.target.value)} className="mt-2 w-full rounded-xl border border-[var(--line)] px-4 py-3 font-mono" /><button type="submit" disabled={busy || !password || confirmation !== `DEPLOY ${shortSha(overview.target_sha)}`} className="mt-6 flex min-h-12 w-full items-center justify-center gap-2 rounded-xl bg-[var(--coral)] px-5 py-3 font-black text-[var(--ink)] disabled:opacity-40">{busy ? <LoaderCircle size={18} className="animate-spin motion-reduce:animate-none" /> : <CloudCog size={18} />}確認並開始部署</button></form></div>}
  </div>;
}
