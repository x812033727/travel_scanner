"use client";

import { CirclePause, CirclePlay, DatabaseZap, MapPinned, RefreshCw, Search, UtensilsCrossed } from "lucide-react";
import { useLocale, useTranslations } from "next-intl";
import { useCallback, useEffect, useMemo, useState } from "react";
import { api } from "@/lib/api";

type ScanStatus = "not_started" | "queued" | "running" | "quota_paused" | "partial" | "completed" | "failed";
type CoverageItem = {
  hotspot_id: string;
  name: string;
  city_name: string;
  country_code: string;
  candidate_count: number;
  status: ScanStatus;
  run_id: string | null;
  updated_at: string | null;
  usage: { aggregate_calls: number; details_calls: number; total_paid_calls: number };
};
type UsageItem = { used: number; feature_used: number; budget: number; percentage: number; projected_month_end: number; projected_percentage: number; alert: "normal" | "watch" | "warning" | "critical" };
type CoverageResponse = {
  total: number;
  completed: number;
  items: CoverageItem[];
  automation_enabled: boolean;
  usage: {
    period: string;
    available: boolean;
    operations: { aggregate: UsageItem; nearby: UsageItem; details: UsageItem; ids_only: { used: number; billing: "no_charge"; budget: null; operations: { text_search: number; place_id_refresh: number } } };
    skus: { sku: string; used: number; free_limit: number; free_remaining: number }[];
  };
};

export function AdminRestaurantScansPanel() {
  const t = useTranslations("restaurants");
  const locale = useLocale();
  const [data, setData] = useState<CoverageResponse | null>(null);
  const [query, setQuery] = useState("");
  const [status, setStatus] = useState<ScanStatus | "">("");
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");
  const number = new Intl.NumberFormat(locale);

  const load = useCallback(async (quiet = false) => {
    if (!quiet) setLoading(true);
    try {
      setData(await api<CoverageResponse>("/admin/hotspots/restaurants/coverage"));
    } catch (reason) {
      setMessage((reason as Error).message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    const timer = window.setTimeout(() => void load(), 0);
    return () => window.clearTimeout(timer);
  }, [load]);

  const active = data?.items?.some((item) => item.status === "queued" || item.status === "running");
  useEffect(() => {
    if (!active) return;
    const timer = window.setInterval(() => void load(true), 3_000);
    return () => window.clearInterval(timer);
  }, [active, load]);

  const filtered = useMemo(() => data?.items?.filter((item) => {
    const matchesQuery = !query.trim() || `${item.name} ${item.city_name}`.toLocaleLowerCase().includes(query.trim().toLocaleLowerCase());
    return matchesQuery && (!status || item.status === status);
  }) ?? [], [data, query, status]);

  async function scan(payload: { hotspot_ids?: string[]; all_missing?: boolean }) {
    setLoading(true);
    setMessage("");
    try {
      const result = await api<{ status: string; runs: { run_id: string }[] }>("/admin/hotspots/restaurants/scans", {
        method: "POST",
        headers: { "Idempotency-Key": crypto.randomUUID() },
        body: JSON.stringify({ hotspot_ids: payload.hotspot_ids ?? [], all_missing: payload.all_missing ?? false }),
      });
      setMessage(result.runs.length ? t("admin.scanStarted", { count: result.runs.length }) : t("admin.nothingToScan"));
      await load(true);
    } catch (reason) {
      setMessage((reason as Error).message);
    } finally {
      setLoading(false);
    }
  }

  async function toggleAutomation() {
    if (!data) return;
    setLoading(true);
    setMessage("");
    try {
      const result = await api<{ enabled: boolean; message: string }>("/admin/hotspots/restaurants/automation", {
        method: "PATCH",
        body: JSON.stringify({ enabled: !data.automation_enabled }),
      });
      setMessage(result.message);
      await load(true);
    } catch (reason) {
      setMessage((reason as Error).message);
    } finally {
      setLoading(false);
    }
  }

  return <section className="mt-10 border-t border-[var(--line)] pt-8">
    <div className="flex flex-wrap items-end justify-between gap-4">
      <div><p className="flex items-center gap-2 text-sm font-bold text-[var(--coral)]"><UtensilsCrossed size={17} />{t("admin.eyebrow")}</p><h2 className="mt-2 text-2xl font-bold">{t("admin.title")}</h2><p className="mt-1 text-sm leading-6 text-[var(--muted)]">{t("admin.description")}</p></div>
      <div className="flex flex-wrap gap-2"><button type="button" disabled={loading} onClick={() => void toggleAutomation()} className={`inline-flex min-h-11 items-center gap-2 rounded-xl border px-4 text-sm font-semibold ${data?.automation_enabled ? "border-amber-300 bg-amber-50 text-amber-900" : "border-emerald-300 bg-emerald-50 text-emerald-900"}`}>{data?.automation_enabled ? <CirclePause size={16} /> : <CirclePlay size={16} />}{t(data?.automation_enabled ? "admin.pauseAutomation" : "admin.resumeAutomation")}</button><button type="button" disabled={loading || !data?.automation_enabled} onClick={() => void scan({ all_missing: true })} className="inline-flex min-h-11 items-center gap-2 rounded-xl bg-[var(--ink)] px-4 text-sm font-semibold text-white disabled:opacity-50"><DatabaseZap size={16} />{t("admin.scanMissing")}</button><button type="button" onClick={() => void load()} aria-label={t("admin.refresh")} className="grid h-11 w-11 place-items-center rounded-xl border border-[var(--line)] bg-white"><RefreshCw size={17} className={loading ? "animate-spin" : ""} /></button></div>
    </div>
    <div className="mt-5 grid gap-3 md:grid-cols-2 xl:grid-cols-4">{data && (["aggregate", "nearby", "details"] as const).map((operation) => {
      const usage = data.usage.operations[operation];
      const percentage = Math.min(100, Math.round(usage.percentage));
      return <article key={operation} className={`rounded-2xl border bg-white p-4 ${usage.alert === "critical" ? "border-red-300" : usage.alert === "warning" ? "border-amber-300" : "border-[var(--line)]"}`}><div className="flex items-center justify-between gap-2 text-sm"><strong>{t(`admin.usage.${operation}`)}</strong><span>{number.format(usage.feature_used)} / {number.format(usage.budget)}</span></div><div className="mt-3 h-2 overflow-hidden rounded-full bg-slate-100"><div className={`h-full rounded-full ${percentage >= 90 ? "bg-[var(--coral)]" : percentage >= 70 ? "bg-amber-500" : "bg-[var(--teal)]"}`} style={{ width: `${percentage}%` }} /></div><p className="mt-2 text-xs text-[var(--muted)]">{t("admin.projectedUsage", { projected: number.format(usage.projected_month_end), percent: number.format(usage.projected_percentage) })}</p><p className="mt-1 text-xs font-semibold">{t(`admin.alert.${usage.alert}`)}</p></article>;
    })}{data && <article className="rounded-2xl border border-emerald-200 bg-emerald-50/50 p-4"><div className="flex items-center justify-between gap-2 text-sm"><strong>{t("admin.usage.idsOnly")}</strong><span>{number.format(data.usage.operations.ids_only.used)}</span></div><p className="mt-3 text-xs font-semibold text-emerald-800">{t("admin.idsOnlyFree")}</p><p className="mt-2 text-xs text-[var(--muted)]">{t("admin.idsOnlyBreakdown", { search: number.format(data.usage.operations.ids_only.operations.text_search), refresh: number.format(data.usage.operations.ids_only.operations.place_id_refresh) })}</p></article>}</div>
    {data?.usage.skus.length ? <div className="mt-3 rounded-2xl bg-[var(--paper)] px-4 py-3 text-xs text-[var(--muted)]"><strong className="text-[var(--ink)]">{t("admin.googleFreeTier")}</strong> {data.usage.skus.map((item) => `${item.sku}: ${number.format(item.used)}/${number.format(item.free_limit)}`).join(" · ")}</div> : null}
    <div className="mt-5 grid gap-3 rounded-2xl border border-[var(--line)] bg-white p-4 md:grid-cols-[1fr_13rem_auto]">
      <label className="relative"><span className="sr-only">{t("admin.search")}</span><Search className="pointer-events-none absolute left-3 top-3 text-[var(--muted)]" size={18} /><input value={query} onChange={(event) => setQuery(event.target.value)} placeholder={t("admin.search")} className="h-11 w-full rounded-xl border border-[var(--line)] pl-10 pr-3" /></label>
      <select aria-label={t("admin.statusFilter")} value={status} onChange={(event) => setStatus(event.target.value as ScanStatus | "")} className="h-11 rounded-xl border border-[var(--line)] px-3"><option value="">{t("admin.allStatuses")}</option>{(["not_started", "queued", "running", "quota_paused", "partial", "completed", "failed"] as ScanStatus[]).map((value) => <option key={value} value={value}>{t(`coverage.${value}`)}</option>)}</select>
      <span className="self-center text-sm text-[var(--muted)]">{t("admin.coverage", { completed: data?.completed ?? 0, total: data?.total ?? 0 })}</span>
    </div>
    {message && <p role="status" className="mt-3 rounded-xl bg-[var(--paper)] px-4 py-3 text-sm text-[var(--muted)]">{message}</p>}
    <div className="mt-3 overflow-hidden rounded-2xl border border-[var(--line)] bg-white"><div className="divide-y divide-[var(--line)]">{filtered.slice(0, 100).map((item) => <article key={item.hotspot_id} className="grid gap-3 p-4 md:grid-cols-[1fr_auto_auto] md:items-center"><div><h3 className="font-semibold">{item.name}</h3><p className="mt-1 flex items-center gap-1 text-xs text-[var(--muted)]"><MapPinned size={13} />{item.city_name} · {item.country_code}</p><p className="mt-1 text-xs text-[var(--muted)]">{t("admin.hotspotCalls", { aggregate: number.format(item.usage.aggregate_calls), details: number.format(item.usage.details_calls) })}</p></div><div className="md:text-right"><span className="rounded-full bg-[var(--paper)] px-2.5 py-1 text-xs font-semibold">{t(`coverage.${item.status}`)}</span><p className="mt-2 text-xs text-[var(--muted)]">{t("admin.placeIds", { count: number.format(item.candidate_count) })}</p></div><button type="button" disabled={loading || !data?.automation_enabled || item.status === "queued" || item.status === "running"} onClick={() => void scan({ hotspot_ids: [item.hotspot_id] })} className="min-h-11 rounded-xl border border-[var(--teal)] px-4 text-sm font-semibold text-[var(--teal)] disabled:opacity-40">{t("admin.scanOne")}</button></article>)}</div>{!loading && !filtered.length && <p className="p-7 text-center text-[var(--muted)]">{t("admin.empty")}</p>}</div>
  </section>;
}
