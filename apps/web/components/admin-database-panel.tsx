"use client";

import { Activity, Archive, CheckCircle2, Database, HardDrive, LoaderCircle, RefreshCw, ServerCog, Wrench } from "lucide-react";
import { useLocale } from "next-intl";
import { useCallback, useEffect, useMemo, useState } from "react";
import { useAdminOperations } from "@/components/admin-operations-provider";
import { AdminConfirmDialog, AdminDataTable, AdminEmptyState, AdminErrorState, AdminSkeleton, AdminStatusPill } from "@/components/admin-ui";
import { adminDatabaseCopy, copyValue } from "@/lib/admin-database-copy";
import { api } from "@/lib/api";
import { Link } from "@/i18n/navigation";

type OperationStatus = "queued" | "running" | "succeeded" | "failed";
type Operation = { id: string; operation_type: "backup" | "analyze" | string; status: OperationStatus; requested_by_email?: string; backup_name?: string; checksum_sha256?: string; size_bytes?: number; schema_revision?: string; release_sha?: string; failure_detail?: string; started_at?: string; finished_at?: string; created_at: string; updated_at: string };
type SchemaSnapshot = { current_revision?: string; expected_revision?: string; is_current?: boolean };
type Overview = { status: "ok" | "unavailable"; checked_at: string; postgres: { version?: string; database_size_bytes?: number; connections?: { active?: number; idle?: number; waiting?: number; maximum?: number }; long_transactions?: number; lock_waits?: number; cache_hit_ratio?: number } | null; schema?: SchemaSnapshot | null; schema_info?: SchemaSnapshot | null; agent: { connected: boolean; available?: boolean; release_sha?: string; active_job?: Record<string, unknown> } | null; active_operation?: Operation | null; maintenance_enabled: boolean; retention_count: number };
type TableInfo = { name: string; estimated_rows: number; data_bytes: number; index_bytes: number; total_bytes: number; dead_rows: number; last_vacuum?: string; last_autovacuum?: string; last_analyze?: string; last_autoanalyze?: string };

const terminal = new Set<OperationStatus>(["succeeded", "failed"]);
function formatBytes(value?: number) {
  if (value == null || !Number.isFinite(value)) return "—";
  const units = ["B", "KB", "MB", "GB", "TB"];
  let amount = Math.max(0, value), unit = 0;
  while (amount >= 1024 && unit < units.length - 1) { amount /= 1024; unit += 1; }
  return `${amount.toLocaleString(undefined, { maximumFractionDigits: amount >= 10 ? 1 : 2 })} ${units[unit]}`;
}

export function AdminDatabasePanel() {
  const locale = useLocale();
  const copy = adminDatabaseCopy(locale);
  const operations = useAdminOperations();
  const [overview, setOverview] = useState<Overview>();
  const [tables, setTables] = useState<TableInfo[]>([]);
  const [backups, setBackups] = useState<Operation[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [tablesError, setTablesError] = useState("");
  const [backupsError, setBackupsError] = useState("");
  const [notice, setNotice] = useState("");
  const [action, setAction] = useState<"backup" | "analyze" | null>(null);
  const [password, setPassword] = useState("");
  const [confirmation, setConfirmation] = useState("");
  const [busy, setBusy] = useState(false);
  const formatter = useMemo(() => new Intl.DateTimeFormat(locale, { dateStyle: "medium", timeStyle: "short" }), [locale]);
  const integer = useMemo(() => new Intl.NumberFormat(locale), [locale]);
  const percent = (value?: number) => value == null ? "—" : `${value.toLocaleString(locale, { maximumFractionDigits: 2 })}%`;
  const operationLabel = (value: string) => value === "backup" ? copy.operationBackup : value === "analyze" ? copy.operationAnalyze : value;
  const operationStatus = (value: string) => copy[`status${value.charAt(0).toUpperCase()}${value.slice(1)}`] || value;

  const load = useCallback(async (quiet = false) => {
    if (!quiet) setLoading(true);
    const [nextOverview, nextTables, nextBackups] = await Promise.allSettled([
        api<Overview>("/admin/database/overview"), api<{ items: TableInfo[] }>("/admin/database/tables"), api<{ items: Operation[] }>("/admin/database/backups"),
    ]);
    if (nextOverview.status === "fulfilled") { setOverview(nextOverview.value); setError(""); }
    else setError((nextOverview.reason as Error).message);
    if (nextTables.status === "fulfilled") { setTables(nextTables.value.items ?? []); setTablesError(""); }
    else setTablesError((nextTables.reason as Error).message);
    if (nextBackups.status === "fulfilled") { setBackups(nextBackups.value.items ?? []); setBackupsError(""); }
    else setBackupsError((nextBackups.reason as Error).message);
    if (!quiet) setLoading(false);
  }, []);
  useEffect(() => {
    const timer = window.setTimeout(() => void load(), 0);
    return () => window.clearTimeout(timer);
  }, [load]);
  const activeOperation = overview?.active_operation;
  useEffect(() => {
    if (!activeOperation || terminal.has(activeOperation.status)) return;
    const timer = window.setInterval(() => void load(true), 2_500);
    return () => window.clearInterval(timer);
  }, [activeOperation, load]);

  async function submitAction() {
    if (!action) return;
    setBusy(true); setError(""); setNotice("");
    try {
      const scope = action === "backup" ? "database.backup" : "database.analyze";
      await api("/admin/step-up", { method: "POST", body: JSON.stringify({ password, scopes: [scope] }) });
      const result = await api<Operation | { operation: Operation }>(action === "backup" ? "/admin/database/backups" : "/admin/database/maintenance", {
        method: "POST", headers: { "Idempotency-Key": `database-${action}-${crypto.randomUUID()}` },
        body: JSON.stringify(action === "backup" ? { confirmation } : { action: "analyze", confirmation }),
      });
      const operation = "operation" in result ? result.operation : result;
      if (overview) setOverview({ ...overview, active_operation: operation });
      setNotice(copy.successQueued); setAction(null); setPassword(""); setConfirmation(""); await load(true);
    } catch (reason) { setError((reason as Error).message); }
    finally { setBusy(false); }
  }

  if (loading) return <AdminSkeleton label={copy.loading} />;
  if (error && !overview) return <AdminErrorState title={copy.loadError} detail={error} retry={() => void load()} retryLabel={copy.retry} />;
  if (!overview) return null;
  const postgres = overview.postgres ?? {};
  const schema = overview.schema_info ?? overview.schema ?? {};
  const agent = overview.agent;
  const canMaintain = Boolean(overview.status === "ok" && operations?.bootstrap.can_manage_database && overview.maintenance_enabled && agent?.connected && agent.available !== false);
  const connection = postgres.connections ?? {};
  return <div className="mt-7 space-y-6">
    {error && <AdminErrorState title={copy.loadError} detail={error} retry={() => void load()} retryLabel={copy.retry} />}
    {notice && <p role="status" className="rounded-2xl bg-emerald-50 p-4 text-sm font-semibold text-emerald-900">{notice}</p>}
    <section className="overflow-hidden rounded-[1.8rem] bg-[var(--ink)] p-6 text-white shadow-lg md:p-8"><div className="flex flex-col justify-between gap-6 lg:flex-row lg:items-end"><div><div className="flex items-center gap-3"><span className="grid size-12 place-items-center rounded-2xl bg-white/10"><Database aria-hidden size={24} /></span><div><p className="text-xs font-bold uppercase tracking-[.14em] text-white/55">{copy.status}</p><h2 className="mt-1 text-2xl font-black">{postgres.version || copy.unavailable}</h2></div></div><p className="mt-5 text-4xl font-black tabular-nums">{formatBytes(postgres.database_size_bytes)}</p><p className="mt-1 text-sm text-white/55">{copy.size}</p></div><div className="flex flex-col gap-2 sm:flex-row"><button type="button" onClick={() => { setAction("analyze"); setConfirmation(""); }} disabled={!canMaintain || Boolean(activeOperation && !terminal.has(activeOperation.status))} className="inline-flex min-h-12 items-center justify-center gap-2 rounded-xl border border-white/20 px-5 font-bold disabled:opacity-40"><Wrench aria-hidden size={18} />{copy.analyze}</button><button type="button" onClick={() => { setAction("backup"); setConfirmation(""); }} disabled={!canMaintain || Boolean(activeOperation && !terminal.has(activeOperation.status))} className="inline-flex min-h-12 items-center justify-center gap-2 rounded-xl bg-[var(--coral-fill)] px-5 font-black disabled:opacity-40"><Archive aria-hidden size={18} />{copy.backupNow}</button></div></div>{!canMaintain && <p className="mt-5 rounded-xl bg-white/10 p-3 text-xs text-white/70">{!overview.maintenance_enabled ? copy.maintenanceOff : !agent?.connected || agent.available === false ? copy.agentUnavailable : copy.operatorRequired}</p>}</section>
    {activeOperation && !terminal.has(activeOperation.status) && <section role="status" className="flex items-center gap-3 rounded-2xl border border-sky-200 bg-sky-50 p-4 text-sky-950"><LoaderCircle aria-hidden className="animate-spin motion-reduce:animate-none" size={20} /><div><strong>{copy.operationRunning}</strong><p className="text-sm">{operationLabel(activeOperation.operation_type)} · {operationStatus(activeOperation.status)}</p></div></section>}
    <section aria-label={copy.status} className="grid gap-3 sm:grid-cols-2 xl:grid-cols-4">{[
      { label: copy.connections, value: `${integer.format(connection.active ?? 0)} / ${integer.format(connection.maximum ?? 0)}`, detail: `${copy.idle} ${connection.idle ?? 0} · ${copy.waiting} ${connection.waiting ?? 0}`, icon: ServerCog },
      { label: copy.cacheHit, value: percent(postgres.cache_hit_ratio), detail: `${copy.lockWaits} ${postgres.lock_waits ?? 0}`, icon: Activity },
      { label: copy.revision, value: schema.current_revision || "—", detail: schema.is_current ? copy.currentRevision : `${copy.expected} ${schema.expected_revision || "—"}`, icon: CheckCircle2 },
      { label: copy.longTransactions, value: integer.format(postgres.long_transactions ?? 0), detail: `${copy.lockWaits} ${integer.format(postgres.lock_waits ?? 0)}`, icon: HardDrive },
    ].map((card) => { const Icon = card.icon; const compact = card.label === copy.revision; return <article key={card.label} className="min-w-0 rounded-[1.35rem] border border-[var(--line)] bg-[var(--surface)] p-5 shadow-[var(--shadow-sm)]"><Icon aria-hidden className="text-[var(--teal)]" size={20} /><p className="mt-4 text-xs font-bold text-[var(--muted)]">{card.label}</p><p title={String(card.value)} className={`mt-1 break-words font-black tabular-nums ${compact ? "font-mono text-base leading-6 sm:text-lg" : "text-2xl"}`}>{card.value}</p><p className="mt-2 text-xs text-[var(--muted)]">{card.detail}</p></article>; })}</section>
    <section className="rounded-[1.7rem] border border-[var(--line)] bg-[var(--surface)] p-5 shadow-[var(--shadow-sm)] md:p-6"><div className="flex items-center justify-between gap-3"><div><h2 className="text-xl font-black">{copy.tables}</h2><p className="mt-1 text-xs text-[var(--muted)]">{copyValue(copy.tablesCount, { count: tables.length })}</p></div><button type="button" onClick={() => void load()} className="admin-icon-button" aria-label={copy.retry}><RefreshCw aria-hidden size={17} /></button></div>{tablesError && <div className="mt-4"><AdminErrorState title={copy.tables} detail={tablesError} retry={() => void load()} retryLabel={copy.retry} /></div>}{tables.length ? <AdminDataTable label={copy.tables} headers={[copy.table, copy.rows, copy.data, copy.indexes, copy.total, copy.deadRows, copy.vacuumed, copy.analyzed]}>{tables.map((table) => <tr key={table.name} className="border-b border-[var(--line)] last:border-0"><td className="px-4 py-4 font-mono text-xs font-bold" data-label={copy.table}>{table.name}</td><td className="px-4 py-4 tabular-nums" data-label={copy.rows}>{integer.format(table.estimated_rows)}</td><td className="px-4 py-4 tabular-nums" data-label={copy.data}>{formatBytes(table.data_bytes)}</td><td className="px-4 py-4 tabular-nums" data-label={copy.indexes}>{formatBytes(table.index_bytes)}</td><td className="px-4 py-4 font-bold tabular-nums" data-label={copy.total}>{formatBytes(table.total_bytes)}</td><td className="px-4 py-4 tabular-nums" data-label={copy.deadRows}>{integer.format(table.dead_rows)}</td><td className="px-4 py-4 text-xs text-[var(--muted)]" data-label={copy.vacuumed}>{table.last_autovacuum || table.last_vacuum ? formatter.format(new Date(table.last_autovacuum || table.last_vacuum!)) : "—"}</td><td className="px-4 py-4 text-xs text-[var(--muted)]" data-label={copy.analyzed}>{table.last_autoanalyze || table.last_analyze ? formatter.format(new Date(table.last_autoanalyze || table.last_analyze!)) : "—"}</td></tr>)}</AdminDataTable> : !tablesError && <AdminEmptyState title={copy.tables} detail={copy.unavailable} />}</section>
    <section className="rounded-[1.7rem] border border-[var(--line)] bg-[var(--surface)] p-5 shadow-[var(--shadow-sm)] md:p-6"><div className="flex flex-col justify-between gap-2 sm:flex-row sm:items-end"><div><h2 className="text-xl font-black">{copy.backups}</h2><p className="mt-1 text-xs text-[var(--muted)]">{copyValue(copy.backupsRetained, { count: overview.retention_count })}</p></div></div>{backupsError && <div className="mt-4"><AdminErrorState title={copy.backups} detail={backupsError} retry={() => void load()} retryLabel={copy.retry} /></div>}{backups.length ? <AdminDataTable label={copy.backups} headers={[copy.createdAt, copy.requestedBy, copy.statusLabel, copy.size, copy.revision, copy.checksum]}>{backups.map((backup) => <tr key={backup.id} className="border-b border-[var(--line)] last:border-0"><td className="px-4 py-4" data-label={copy.createdAt}>{formatter.format(new Date(backup.created_at))}</td><td className="px-4 py-4" data-label={copy.requestedBy}>{backup.requested_by_email || "—"}</td><td className="px-4 py-4" data-label={copy.statusLabel}><AdminStatusPill status={backup.status}>{operationStatus(backup.status)}</AdminStatusPill>{backup.failure_detail && <p className="mt-1 max-w-xs text-xs text-red-700">{backup.failure_detail}</p>}</td><td className="px-4 py-4 tabular-nums" data-label={copy.size}>{formatBytes(backup.size_bytes)}</td><td className="px-4 py-4 font-mono text-xs" data-label={copy.revision}>{backup.schema_revision || "—"}</td><td className="px-4 py-4 font-mono text-[.68rem]" data-label={copy.checksum}>{backup.checksum_sha256 ? `${backup.checksum_sha256.slice(0, 12)}…` : "—"}</td></tr>)}</AdminDataTable> : !backupsError && <AdminEmptyState title={copy.noBackups} />}</section>
    <aside className="rounded-2xl border border-amber-200 bg-amber-50 p-5 text-sm leading-6 text-amber-950">{copy.safeNote}</aside>
    <AdminConfirmDialog open={Boolean(action)} title={action === "backup" ? copy.backupTitle : copy.analyzeTitle} description={action === "backup" ? copy.backupDescription : copy.analyzeDescription} confirmationLabel={copy.typeConfirmation} expectedConfirmation={action === "backup" ? "BACKUP" : "ANALYZE"} confirmation={confirmation} password={password} passwordLabel={copy.password} recoveryAction={<Link href="/forgot-password" className="inline-flex min-h-11 items-center underline">{copy.setLocalPassword}</Link>} busy={busy} cancelLabel={copy.cancel} confirmLabel={copy.confirm} onConfirmationChange={setConfirmation} onPasswordChange={setPassword} onCancel={() => { if (!busy) { setAction(null); setPassword(""); setConfirmation(""); } }} onConfirm={() => void submitAction()} />
  </div>;
}
