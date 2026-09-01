"use client";

import { DatabaseZap, MapPinned, RefreshCw, Search, UtensilsCrossed } from "lucide-react";
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
};
type UsageItem = { used: number; feature_used: number; budget: number };
type CoverageResponse = {
  total: number;
  completed: number;
  items: CoverageItem[];
  usage: {
    period: string;
    available: boolean;
    operations: { aggregate: UsageItem; nearby: UsageItem; details: UsageItem };
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

  const active = data?.items.some((item) => item.status === "queued" || item.status === "running");
  useEffect(() => {
    if (!active) return;
    const timer = window.setInterval(() => void load(true), 3_000);
    return () => window.clearInterval(timer);
  }, [active, load]);

  const filtered = useMemo(() => data?.items.filter((item) => {
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

  return <section className="mt-10 border-t border-[var(--line)] pt-8">
    <div className="flex flex-wrap items-end justify-between gap-4">
      <div><p className="flex items-center gap-2 text-sm font-bold text-[var(--coral)]"><UtensilsCrossed size={17} />{t("admin.eyebrow")}</p><h2 className="mt-2 text-2xl font-bold">{t("admin.title")}</h2><p className="mt-1 text-sm leading-6 text-[var(--muted)]">{t("admin.description")}</p></div>
      <div className="flex gap-2"><button type="button" disabled={loading} onClick={() => void scan({ all_missing: true })} className="inline-flex min-h-11 items-center gap-2 rounded-xl bg-[var(--ink)] px-4 text-sm font-semibold text-white disabled:opacity-50"><DatabaseZap size={16} />{t("admin.scanMissing")}</button><button type="button" onClick={() => void load()} aria-label={t("admin.refresh")} className="grid h-11 w-11 place-items-center rounded-xl border border-[var(--line)] bg-white"><RefreshCw size={17} className={loading ? "animate-spin" : ""} /></button></div>
    </div>
    <div className="mt-5 grid gap-3 md:grid-cols-3">{data && (Object.entries(data.usage.operations) as ["aggregate" | "nearby" | "details", UsageItem][]).map(([operation, usage]) => {
      const percentage = usage.budget ? Math.min(100, Math.round(usage.used / usage.budget * 100)) : 0;
      return <article key={operation} className="rounded-2xl border border-[var(--line)] bg-white p-4"><div className="flex items-center justify-between gap-2 text-sm"><strong>{t(`admin.usage.${operation}`)}</strong><span>{number.format(usage.used)} / {number.format(usage.budget)}</span></div><div className="mt-3 h-2 overflow-hidden rounded-full bg-slate-100"><div className={`h-full rounded-full ${percentage >= 90 ? "bg-[var(--coral)]" : "bg-[var(--teal)]"}`} style={{ width: `${percentage}%` }} /></div><p className="mt-2 text-xs text-[var(--muted)]">{t("admin.safetyBudget", { period: data.usage.period, remaining: number.format(Math.max(0, usage.budget - usage.used)) })}</p><p className="mt-1 text-xs text-[var(--muted)]">{t("admin.featureUsage", { used: number.format(usage.feature_used) })}</p></article>;
    })}</div>
    {data?.usage.skus.length ? <div className="mt-3 rounded-2xl bg-[var(--paper)] px-4 py-3 text-xs text-[var(--muted)]"><strong className="text-[var(--ink)]">{t("admin.googleFreeTier")}</strong> {data.usage.skus.map((item) => `${item.sku}: ${number.format(item.used)}/${number.format(item.free_limit)}`).join(" · ")}</div> : null}
    <div className="mt-5 grid gap-3 rounded-2xl border border-[var(--line)] bg-white p-4 md:grid-cols-[1fr_13rem_auto]">
      <label className="relative"><span className="sr-only">{t("admin.search")}</span><Search className="pointer-events-none absolute left-3 top-3 text-[var(--muted)]" size={18} /><input value={query} onChange={(event) => setQuery(event.target.value)} placeholder={t("admin.search")} className="h-11 w-full rounded-xl border border-[var(--line)] pl-10 pr-3" /></label>
      <select aria-label={t("admin.statusFilter")} value={status} onChange={(event) => setStatus(event.target.value as ScanStatus | "")} className="h-11 rounded-xl border border-[var(--line)] px-3"><option value="">{t("admin.allStatuses")}</option>{(["not_started", "queued", "running", "quota_paused", "partial", "completed", "failed"] as ScanStatus[]).map((value) => <option key={value} value={value}>{t(`coverage.${value}`)}</option>)}</select>
      <span className="self-center text-sm text-[var(--muted)]">{t("admin.coverage", { completed: data?.completed ?? 0, total: data?.total ?? 0 })}</span>
    </div>
    {message && <p role="status" className="mt-3 rounded-xl bg-[var(--paper)] px-4 py-3 text-sm text-[var(--muted)]">{message}</p>}
    <div className="mt-3 overflow-hidden rounded-2xl border border-[var(--line)] bg-white"><div className="divide-y divide-[var(--line)]">{filtered.slice(0, 100).map((item) => <article key={item.hotspot_id} className="grid gap-3 p-4 md:grid-cols-[1fr_auto_auto] md:items-center"><div><h3 className="font-semibold">{item.name}</h3><p className="mt-1 flex items-center gap-1 text-xs text-[var(--muted)]"><MapPinned size={13} />{item.city_name} · {item.country_code}</p></div><div className="md:text-right"><span className="rounded-full bg-[var(--paper)] px-2.5 py-1 text-xs font-semibold">{t(`coverage.${item.status}`)}</span><p className="mt-2 text-xs text-[var(--muted)]">{t("admin.placeIds", { count: number.format(item.candidate_count) })}</p></div><button type="button" disabled={loading || item.status === "queued" || item.status === "running"} onClick={() => void scan({ hotspot_ids: [item.hotspot_id] })} className="min-h-11 rounded-xl border border-[var(--teal)] px-4 text-sm font-semibold text-[var(--teal)] disabled:opacity-40">{t("admin.scanOne")}</button></article>)}</div>{!loading && !filtered.length && <p className="p-7 text-center text-[var(--muted)]">{t("admin.empty")}</p>}</div>
  </section>;
}
