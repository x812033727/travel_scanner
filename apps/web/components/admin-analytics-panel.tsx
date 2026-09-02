"use client";

import { Activity, ArrowDownRight, ArrowUpRight, BarChart3, RefreshCw, ShieldCheck } from "lucide-react";
import { useLocale, useTranslations } from "next-intl";
import { useCallback, useEffect, useMemo, useState } from "react";
import { Area, AreaChart, Bar, BarChart, CartesianGrid, Cell, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { api } from "@/lib/api";

type Range = "24h" | "7d" | "30d" | "90d" | "12m";
type Metric = Record<string, number | null | Record<string, number | null>>;
type Row = { key: string; value: number };
type Dashboard = {
  range: Range;
  timezone: string;
  source: string;
  summary: Metric & { previous?: Metric | null; changes?: Record<string, number | null> };
  timeseries: Array<Record<string, string | number>>;
  funnel: Array<{ step: string; sessions: number; conversion_rate: number }>;
  top_pages: Row[];
  referrers: Row[];
  utm_sources: Row[];
  devices: Row[];
  locales: Row[];
  countries: Row[];
  heatmap: Array<{ weekday: number; hour: number; value: number }>;
  authoritative: Record<string, number>;
  data_quality: Record<string, string | number | boolean | null>;
};

const ranges: Range[] = ["24h", "7d", "30d", "90d", "12m"];
const summaryKeys = ["live_sessions_30m", "page_views", "avg_daily_visitors", "sessions", "pages_per_session", "registration_completed", "search_completed", "trip_created", "outbound_click"];
const colors = ["#147d76", "#e48a4a", "#5674b9", "#b15f8d", "#6d8f44", "#8d6b50"];

function Ranking({ title, rows }: { title: string; rows: Row[] }) {
  const total = rows.reduce((sum, row) => sum + row.value, 0);
  return <section className="min-w-0 max-w-full overflow-hidden rounded-[1.75rem] border border-[var(--line)] bg-white p-5 shadow-sm">
    <h3 className="font-bold">{title}</h3>
    {rows.length ? <><div className="mt-4 max-w-full overflow-x-auto"><div className="h-52 min-w-[420px]" aria-hidden="true"><ResponsiveContainer width="100%" height="100%"><BarChart data={rows} layout="vertical" margin={{ left: 16, right: 16 }}><CartesianGrid strokeDasharray="3 3" horizontal={false} /><XAxis type="number" allowDecimals={false} /><YAxis dataKey="key" type="category" width={105} tick={{ fontSize: 11 }} /><Tooltip /><Bar dataKey="value" radius={[0, 8, 8, 0]}>{rows.map((row, index) => <Cell key={row.key} fill={colors[index % colors.length]} />)}</Bar></BarChart></ResponsiveContainer></div></div><table className="sr-only"><caption>{title}</caption><tbody>{rows.map((row) => <tr key={row.key}><th>{row.key}</th><td>{row.value}</td><td>{total ? Math.round(row.value * 100 / total) : 0}%</td></tr>)}</tbody></table></> : <p className="mt-6 text-sm text-[var(--muted)]">—</p>}
  </section>;
}

export function AdminAnalyticsPanel() {
  const t = useTranslations("admin.analytics");
  const locale = useLocale();
  const [range, setRange] = useState<Range>("30d");
  const [includeBots, setIncludeBots] = useState(false);
  const [data, setData] = useState<Dashboard>();
  const [error, setError] = useState<string>();
  const [loading, setLoading] = useState(true);
  const number = useMemo(() => new Intl.NumberFormat(locale, { maximumFractionDigits: 1 }), [locale]);
  const date = useMemo(() => new Intl.DateTimeFormat(locale, { dateStyle: "medium", timeStyle: "short", timeZone: "Asia/Taipei" }), [locale]);
  const weekdays = useMemo(() => Array.from({ length: 7 }, (_, index) => new Intl.DateTimeFormat(locale, { weekday: "short", timeZone: "UTC" }).format(new Date(Date.UTC(2026, 7, 31 + index)))), [locale]);
  const load = useCallback(async () => {
    setLoading(true);
    try {
      setData(await api<Dashboard>(`/admin/analytics/dashboard?range=${range}&compare=true&include_bots=${includeBots}`));
      setError(undefined);
    } catch (reason) { setError(reason instanceof Error ? reason.message : t("loadError")); }
    finally { setLoading(false); }
  }, [includeBots, range, t]);
  useEffect(() => {
    const first = window.setTimeout(() => void load(), 0);
    const timer = window.setInterval(load, 60_000);
    return () => { window.clearTimeout(first); window.clearInterval(timer); };
  }, [load]);

  if (error && !data) return <div role="alert" className="mt-7 rounded-2xl border border-red-200 bg-red-50 p-5 text-red-800">{error}<button className="ml-3 font-semibold underline" onClick={load}>{t("retry")}</button></div>;
  return <div className="analytics-dashboard mt-7 min-w-0 max-w-full space-y-6 overflow-x-clip">
    <div className="sticky top-2 z-10 flex flex-wrap items-center justify-between gap-3 rounded-2xl border border-[var(--line)] bg-white/95 p-3 shadow-sm backdrop-blur">
      <div role="group" aria-label={t("rangeLabel")} className="flex max-w-full gap-1 overflow-x-auto">{ranges.map((value) => <button key={value} onClick={() => setRange(value)} aria-pressed={range === value} className={`shrink-0 rounded-xl px-3 py-2 text-sm font-semibold ${range === value ? "bg-[var(--ink)] text-white" : "hover:bg-[var(--paper)]"}`}>{t(`ranges.${value}`)}</button>)}</div>
      <div className="flex items-center gap-3"><label className="flex items-center gap-2 text-sm font-semibold"><input type="checkbox" checked={includeBots} onChange={(event) => setIncludeBots(event.target.checked)} />{t("includeBots")}</label><button onClick={load} disabled={loading} className="grid h-10 w-10 place-items-center rounded-xl border border-[var(--line)]" aria-label={t("refresh")}><RefreshCw size={17} className={loading ? "animate-spin" : ""} /></button></div>
    </div>

    {!data ? <div className="grid min-h-72 place-items-center rounded-[2rem] bg-white"><Activity className="animate-pulse text-[var(--teal)]" /></div> : <>
      <section className="grid gap-3 sm:grid-cols-2 xl:grid-cols-5">{summaryKeys.map((key) => {
        const value = Number(data.summary[key] || 0); const change = data.summary.changes?.[key];
        return <article key={key} className="rounded-2xl border border-[var(--line)] bg-white p-4 shadow-sm"><p className="text-xs font-semibold text-[var(--muted)]">{t(`metrics.${key}`)}</p><p className="mt-2 text-2xl font-bold tabular-nums">{number.format(value)}</p>{change == null ? <p className="mt-1 text-xs text-[var(--muted)]">{t("noComparison")}</p> : <p className={`mt-1 flex items-center gap-1 text-xs font-semibold ${change >= 0 ? "text-emerald-700" : "text-rose-700"}`}>{change >= 0 ? <ArrowUpRight size={13} /> : <ArrowDownRight size={13} />}{number.format(Math.abs(change))}%</p>}</article>;
      })}</section>

      <section className="rounded-[1.75rem] border border-[var(--line)] bg-white p-5 shadow-sm md:p-6"><div className="flex items-center justify-between"><div><h2 className="text-xl font-bold">{t("trend")}</h2><p className="mt-1 text-xs text-[var(--muted)]">{t("timezone", { timezone: data.timezone })}</p></div><BarChart3 className="text-[var(--teal)]" /></div><div className="mt-5 overflow-x-auto"><div className="h-72 min-w-[620px]"><ResponsiveContainer width="100%" height="100%"><AreaChart data={data.timeseries}><defs><linearGradient id="analyticsFill" x1="0" y1="0" x2="0" y2="1"><stop offset="5%" stopColor="#147d76" stopOpacity={0.35}/><stop offset="95%" stopColor="#147d76" stopOpacity={0}/></linearGradient></defs><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="bucket" tick={{ fontSize: 11 }} /><YAxis allowDecimals={false} /><Tooltip /><Area type="monotone" dataKey="page_view" stroke="#147d76" strokeWidth={3} fill="url(#analyticsFill)" /></AreaChart></ResponsiveContainer></div></div><table className="sr-only"><caption>{t("trend")}</caption><thead><tr><th>{t("period")}</th><th>{t("metrics.page_views")}</th></tr></thead><tbody>{data.timeseries.map((row) => <tr key={String(row.bucket)}><th>{String(row.bucket)}</th><td>{row.page_view}</td></tr>)}</tbody></table></section>

      <section className="grid gap-6 xl:grid-cols-[1.15fr_.85fr]"><div className="rounded-[1.75rem] border border-[var(--line)] bg-[var(--ink)] p-5 text-white shadow-sm"><h2 className="text-xl font-bold">{t("funnel")}</h2><p className="mt-1 text-sm text-white/65">{t(data.source === "raw" ? "funnelRaw" : "funnelRollup")}</p><ol className="mt-5 space-y-3">{data.funnel.map((item, index) => <li key={item.step}><div className="mb-1 flex justify-between text-sm"><span>{index + 1}. {t(`funnelSteps.${item.step}`)}</span><strong>{number.format(item.sessions)} · {item.conversion_rate}%</strong></div><div className="h-3 overflow-hidden rounded-full bg-white/10"><div className="h-full rounded-full bg-[var(--coral)]" style={{ width: `${Math.max(2, item.conversion_rate)}%` }} /></div></li>)}</ol></div><div className="rounded-[1.75rem] border border-[var(--line)] bg-white p-5 shadow-sm"><h2 className="text-xl font-bold">{t("authoritative")}</h2><p className="mt-1 text-sm text-[var(--muted)]">{t("authoritativeHelp")}</p><dl className="mt-5 grid grid-cols-2 gap-3">{Object.entries(data.authoritative).map(([key, value]) => <div key={key} className="rounded-xl bg-[var(--paper)] p-3"><dt className="text-xs text-[var(--muted)]">{t(`authoritativeMetrics.${key}`)}</dt><dd className="mt-1 text-xl font-bold">{number.format(value)}</dd></div>)}</dl></div></section>

      <div className="grid min-w-0 max-w-full gap-6 lg:grid-cols-2"><Ranking title={t("rankings.pages")} rows={data.top_pages} /><Ranking title={t("rankings.sources")} rows={data.referrers} /><Ranking title={t("rankings.devices")} rows={data.devices} /><Ranking title={t("rankings.locales")} rows={data.locales} /><Ranking title={t("rankings.countries")} rows={data.countries} /><Ranking title={t("rankings.utm")} rows={data.utm_sources} /></div>

      <section className="rounded-[1.75rem] border border-[var(--line)] bg-white p-5 shadow-sm"><h2 className="text-xl font-bold">{t("heatmap")}</h2><p className="mt-1 text-sm text-[var(--muted)]">{t("heatmapHelp")}</p>{data.heatmap.length ? <div className="mt-5 overflow-x-auto"><div className="grid min-w-[720px] grid-cols-[3.5rem_repeat(24,minmax(1.4rem,1fr))] gap-1" aria-hidden="true"><span />{Array.from({ length: 24 }, (_, hour) => <span key={hour} className="text-center text-[.6rem] text-[var(--muted)]">{hour}</span>)}{weekdays.flatMap((day, weekday) => [<span key={`${day}-label`} className="self-center text-xs font-semibold">{day}</span>, ...Array.from({ length: 24 }, (_, hour) => { const value = data.heatmap.find((cell) => cell.weekday === weekday && cell.hour === hour)?.value || 0; return <span key={`${day}-${hour}`} title={`${day} ${hour}:00 · ${value}`} className="aspect-square rounded-sm" style={{ backgroundColor: `color-mix(in srgb, var(--teal) ${Math.min(90, 8 + value * 8)}%, white)` }} />; })])}</div><table className="sr-only"><caption>{t("heatmap")}</caption><thead><tr><th>{t("weekday")}</th>{Array.from({ length: 24 }, (_, hour) => <th key={hour}>{hour}:00</th>)}</tr></thead><tbody>{weekdays.map((day, weekday) => <tr key={day}><th>{day}</th>{Array.from({ length: 24 }, (_, hour) => <td key={hour}>{data.heatmap.find((cell) => cell.weekday === weekday && cell.hour === hour)?.value || 0}</td>)}</tr>)}</tbody></table></div> : <p className="mt-5 text-sm text-[var(--muted)]">{t("heatmapUnavailable")}</p>}</section>

      <section className="rounded-[1.75rem] border border-[var(--line)] bg-white p-5 shadow-sm"><div className="flex items-center gap-2"><ShieldCheck className="text-[var(--teal)]" /><h2 className="text-xl font-bold">{t("quality")}</h2></div><dl className="mt-5 grid gap-3 sm:grid-cols-2 lg:grid-cols-4"><div><dt className="text-xs text-[var(--muted)]">{t("qualityFields.ga4")}</dt><dd className="font-semibold">{data.data_quality.ga4_enabled && data.data_quality.ga4_configured ? t("enabled") : t("disabled")}</dd></div><div><dt className="text-xs text-[var(--muted)]">{t("qualityFields.started")}</dt><dd className="font-semibold">{data.data_quality.tracking_started_at ? date.format(new Date(String(data.data_quality.tracking_started_at))) : "—"}</dd></div><div><dt className="text-xs text-[var(--muted)]">{t("qualityFields.lastEvent")}</dt><dd className="font-semibold">{data.data_quality.last_event_at ? date.format(new Date(String(data.data_quality.last_event_at))) : "—"}</dd></div><div><dt className="text-xs text-[var(--muted)]">{t("qualityFields.lastRollup")}</dt><dd className="font-semibold">{String(data.data_quality.last_rollup_day || "—")}</dd></div><div><dt className="text-xs text-[var(--muted)]">{t("qualityFields.country")}</dt><dd className="font-semibold">{number.format(Number(data.data_quality.country_coverage_percent || 0))}%</dd></div><div><dt className="text-xs text-[var(--muted)]">{t("qualityFields.bots")}</dt><dd className="font-semibold">{data.data_quality.bots_excluded ? t("excluded") : t("included")}</dd></div><div><dt className="text-xs text-[var(--muted)]">{t("qualityFields.rawRetention")}</dt><dd className="font-semibold">{data.data_quality.raw_retention_days} {t("days")}</dd></div><div><dt className="text-xs text-[var(--muted)]">{t("qualityFields.rollupRetention")}</dt><dd className="font-semibold">{data.data_quality.rollup_retention_months} {t("months")}</dd></div></dl></section>
    </>}
  </div>;
}
