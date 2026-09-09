"use client";

import { ChevronLeft, ChevronRight, Filter, Search } from "lucide-react";
import { useLocale } from "next-intl";
import { useSearchParams } from "next/navigation";
import { FormEvent, useCallback, useEffect, useMemo, useState } from "react";
import { AdminDataTable, AdminDetailDrawer, AdminEmptyState, AdminErrorState, AdminFilterBar, AdminSkeleton, AdminStatusPill } from "@/components/admin-ui";
import { usePathname, useRouter } from "@/i18n/navigation";
import { adminAuditCopy, auditFormat } from "@/lib/admin-audit-copy";
import { api } from "@/lib/api";

type AuditEvent = { id: string; actor_user_id?: string; actor_email?: string; action: string; target?: string; result: string; metadata: Record<string, unknown>; created_at: string };
type AuditList = { items: AuditEvent[]; total: number; page: number; limit: number; pages: number };
const allowedMetadata = new Set(["reason", "fields", "roles", "scope", "duration_minutes", "request_id", "status", "replayed"]);
function apiDateBoundary(value: string | null, endOfDay = false) {
  if (!value || !/^\d{4}-\d{2}-\d{2}$/.test(value)) return value;
  return `${value}T${endOfDay ? "23:59:59.999" : "00:00:00.000"}Z`;
}

export function AdminAuditPanel() {
  const locale = useLocale();
  const copy = adminAuditCopy(locale);
  const searchParams = useSearchParams();
  const pathname = usePathname();
  const router = useRouter();
  const [data, setData] = useState<AuditList>();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [detailState, setDetailState] = useState<{ id: string; item?: AuditEvent; error?: string }>();
  const [detailRetry, setDetailRetry] = useState(0);
  const [draft, setDraft] = useState(() => ({ actor: searchParams.get("actor") || "", action: searchParams.get("action") || "", target: searchParams.get("target") || "", result: searchParams.get("result") || "", date_from: searchParams.get("date_from") || "", date_to: searchParams.get("date_to") || "" }));
  const query = searchParams.toString();
  const formatter = useMemo(() => new Intl.DateTimeFormat(locale, { dateStyle: "medium", timeStyle: "medium" }), [locale]);
  const selectedId = searchParams.get("event");
  const listedSelection = data?.items.find((item) => item.id === selectedId);
  const selectedDetail = detailState?.id === selectedId ? detailState.item : undefined;
  const detailError = detailState?.id === selectedId ? detailState.error || "" : "";
  const selected = listedSelection ?? selectedDetail;
  const detailLoading = Boolean(selectedId && !listedSelection && !selectedDetail && !detailError);
  const load = useCallback(async () => {
    setLoading(true); setError("");
    const params = new URLSearchParams(query);
    params.delete("event"); if (!params.has("limit")) params.set("limit", "25");
    const dateFrom = apiDateBoundary(params.get("date_from"));
    const dateTo = apiDateBoundary(params.get("date_to"), true);
    if (dateFrom) params.set("date_from", dateFrom);
    if (dateTo) params.set("date_to", dateTo);
    try { setData(await api<AuditList>(`/admin/audit?${params}`)); }
    catch (reason) { setError((reason as Error).message); }
    finally { setLoading(false); }
  }, [query]);
  useEffect(() => {
    const timer = window.setTimeout(() => void load(), 0);
    return () => window.clearTimeout(timer);
  }, [load]);
  useEffect(() => {
    const current = new URLSearchParams(query);
    const timer = window.setTimeout(() => {
      setDraft({
        actor: current.get("actor") || "",
        action: current.get("action") || "",
        target: current.get("target") || "",
        result: current.get("result") || "",
        date_from: current.get("date_from") || "",
        date_to: current.get("date_to") || "",
      });
    }, 0);
    return () => window.clearTimeout(timer);
  }, [query]);
  useEffect(() => {
    if (!selectedId || listedSelection) return;
    const controller = new AbortController();
    api<AuditEvent>(`/admin/audit/${selectedId}`, { signal: controller.signal })
      .then((item) => setDetailState({ id: selectedId, item }))
      .catch((reason: Error) => {
        if (!controller.signal.aborted) setDetailState({ id: selectedId, error: reason.message });
      });
    return () => controller.abort();
  }, [detailRetry, listedSelection, selectedId]);

  function replace(mutator: (params: URLSearchParams) => void) {
    const params = new URLSearchParams(searchParams.toString()); mutator(params);
    router.replace(`${pathname}${params.size ? `?${params}` : ""}`);
  }
  function submit(event: FormEvent) {
    event.preventDefault();
    replace((params) => { for (const [key, value] of Object.entries(draft)) { if (value) params.set(key, value); else params.delete(key); } params.set("page", "1"); params.delete("event"); });
  }
  const metadata = selected ? Object.fromEntries(Object.entries(selected.metadata || {}).filter(([key]) => allowedMetadata.has(key))) : {};

  return <div className="mt-7">
    <form onSubmit={submit}><AdminFilterBar>
      <label className="min-w-0 flex-1 text-xs font-bold text-[var(--muted)]">{copy.actor}<input value={draft.actor} onChange={(event) => setDraft({ ...draft, actor: event.target.value })} placeholder={copy.actorPlaceholder} className="mt-1 min-h-11 w-full rounded-xl border border-[var(--line)] bg-[var(--surface)] px-3 text-sm text-[var(--ink)]" /></label>
      <label className="min-w-0 flex-1 text-xs font-bold text-[var(--muted)]">{copy.action}<input value={draft.action} onChange={(event) => setDraft({ ...draft, action: event.target.value })} placeholder={copy.actionPlaceholder} className="mt-1 min-h-11 w-full rounded-xl border border-[var(--line)] bg-[var(--surface)] px-3 text-sm text-[var(--ink)]" /></label>
      <label className="min-w-0 flex-1 text-xs font-bold text-[var(--muted)]">{copy.target}<input value={draft.target} onChange={(event) => setDraft({ ...draft, target: event.target.value })} placeholder={copy.targetPlaceholder} className="mt-1 min-h-11 w-full rounded-xl border border-[var(--line)] bg-[var(--surface)] px-3 text-sm text-[var(--ink)]" /></label>
      <label className="text-xs font-bold text-[var(--muted)]">{copy.result}<select value={draft.result} onChange={(event) => setDraft({ ...draft, result: event.target.value })} className="mt-1 min-h-11 rounded-xl border border-[var(--line)] bg-[var(--surface)] px-3 text-sm text-[var(--ink)]"><option value="">{copy.allResults}</option><option value="succeeded">{copy.success}</option><option value="failed">{copy.failure}</option></select></label>
      <label className="text-xs font-bold text-[var(--muted)]">{copy.from}<input type="date" value={draft.date_from} onChange={(event) => setDraft({ ...draft, date_from: event.target.value })} className="mt-1 min-h-11 rounded-xl border border-[var(--line)] bg-[var(--surface)] px-3 text-sm text-[var(--ink)]" /></label>
      <label className="text-xs font-bold text-[var(--muted)]">{copy.to}<input type="date" value={draft.date_to} onChange={(event) => setDraft({ ...draft, date_to: event.target.value })} className="mt-1 min-h-11 rounded-xl border border-[var(--line)] bg-[var(--surface)] px-3 text-sm text-[var(--ink)]" /></label>
      <button type="submit" className="inline-flex min-h-11 items-center justify-center gap-2 rounded-xl bg-[var(--ink)] px-4 text-sm font-bold text-white"><Search aria-hidden size={16} />{copy.search}</button>
      <button type="button" onClick={() => { setDraft({ actor: "", action: "", target: "", result: "", date_from: "", date_to: "" }); replace((params) => { for (const key of ["actor", "action", "target", "result", "date_from", "date_to", "page", "event"]) params.delete(key); }); }} className="inline-flex min-h-11 items-center justify-center gap-2 rounded-xl border border-[var(--line)] px-4 text-sm font-bold"><Filter aria-hidden size={16} />{copy.clear}</button>
    </AdminFilterBar></form>
    {loading ? <AdminSkeleton label={copy.loading} /> : error ? <AdminErrorState title={copy.error} detail={error} retry={() => void load()} retryLabel={copy.retry} /> : data?.items.length ? <>
      <AdminDataTable label={copy.details} headers={[copy.time, copy.actor, copy.action, copy.target, copy.result, copy.details]}>{data.items.map((item) => <tr key={item.id} className="border-b border-[var(--line)] last:border-0"><td className="px-4 py-4 text-xs text-[var(--muted)]" data-label={copy.time}>{formatter.format(new Date(item.created_at))}</td><td className="px-4 py-4" data-label={copy.actor}><strong className="block break-all text-sm">{item.actor_email || copy.deletedAccount}</strong>{item.actor_user_id && <span className="text-[.68rem] text-[var(--muted)]">{item.actor_user_id.slice(0, 8)}</span>}</td><td className="px-4 py-4 font-mono text-xs font-bold" data-label={copy.action}>{item.action}</td><td className="px-4 py-4 text-xs" data-label={copy.target}>{item.target || "—"}</td><td className="px-4 py-4" data-label={copy.result}><AdminStatusPill status={item.result}>{item.result === "succeeded" ? copy.success : item.result === "failed" ? copy.failure : item.result}</AdminStatusPill></td><td className="px-4 py-4" data-label={copy.details}><button type="button" onClick={() => replace((params) => params.set("event", item.id))} className="min-h-11 rounded-xl border border-[var(--line)] px-3 text-xs font-bold">{copy.open}</button></td></tr>)}</AdminDataTable>
      <div className="mt-4 flex flex-col items-center justify-between gap-3 text-sm sm:flex-row"><p className="text-[var(--muted)]">{auditFormat(copy.page, { page: data.page, pages: data.pages, total: data.total })}</p><div className="flex gap-2"><button type="button" aria-label={copy.previous} disabled={data.page <= 1} onClick={() => replace((params) => params.set("page", String(data.page - 1)))} className="admin-icon-button disabled:opacity-40"><ChevronLeft aria-hidden size={17} /></button><button type="button" aria-label={copy.next} disabled={data.page >= data.pages} onClick={() => replace((params) => params.set("page", String(data.page + 1)))} className="admin-icon-button disabled:opacity-40"><ChevronRight aria-hidden size={17} /></button></div></div>
    </> : <AdminEmptyState title={copy.noRecords} />}
    <AdminDetailDrawer open={Boolean(selectedId)} title={copy.eventDetail} closeLabel={copy.close} onClose={() => replace((params) => params.delete("event"))}>{detailLoading ? <AdminSkeleton label={copy.loading} /> : detailError ? <AdminErrorState title={copy.error} detail={detailError} retry={() => { if (selectedId) setDetailState({ id: selectedId }); setDetailRetry((value) => value + 1); }} retryLabel={copy.retry} /> : selected ? <div className="space-y-5"><div><p className="text-xs font-bold text-[var(--muted)]">{copy.action}</p><p className="mt-1 break-all font-mono text-sm font-bold">{selected.action}</p></div><div className="grid gap-4 sm:grid-cols-2"><div><p className="text-xs font-bold text-[var(--muted)]">{copy.actor}</p><p className="mt-1 break-all text-sm">{selected.actor_email || copy.deletedAccount}</p></div><div><p className="text-xs font-bold text-[var(--muted)]">{copy.time}</p><p className="mt-1 text-sm">{formatter.format(new Date(selected.created_at))}</p></div><div><p className="text-xs font-bold text-[var(--muted)]">{copy.target}</p><p className="mt-1 break-all text-sm">{selected.target || "—"}</p></div><div><p className="text-xs font-bold text-[var(--muted)]">{copy.result}</p><div className="mt-1"><AdminStatusPill status={selected.result}>{selected.result === "succeeded" ? copy.success : selected.result === "failed" ? copy.failure : selected.result}</AdminStatusPill></div></div></div><section><h3 className="text-sm font-bold">{copy.metadata}</h3>{Object.keys(metadata).length ? <dl className="mt-3 divide-y divide-[var(--line)] rounded-xl bg-[var(--paper)] px-4">{Object.entries(metadata).map(([key, value]) => <div key={key} className="grid gap-1 py-3 sm:grid-cols-[10rem_1fr]"><dt className="text-xs font-bold text-[var(--muted)]">{key}</dt><dd className="break-words text-sm">{Array.isArray(value) ? value.join(", ") : typeof value === "object" ? "…" : String(value)}</dd></div>)}</dl> : <p className="mt-2 text-sm text-[var(--muted)]">{copy.noMetadata}</p>}</section></div> : null}</AdminDetailDrawer>
  </div>;
}
