"use client";

import { useLocale, useTranslations } from "next-intl";
import { useCallback, useEffect, useState } from "react";
import { AdminEmptyState, AdminErrorState } from "@/components/admin-ui";
import { useWhen } from "@/components/admin-video-review-card";
import { addDays, message, type Report, REPORT_VALUES, type ReportRow, type ReportValue, type Reports } from "@/components/admin-video-shorts-data";
import { api } from "@/lib/api";

// The weekly report of the Shorts tab (docs/videos/SHORTS.md, the section on the numbers and the
// weekly report): one a week, the newest first. The planner model writes the text, shown as plain
// text; under it are the numbers it cites, each as YouTube reported it with its source and the time
// it was read, and the coming week's plan. Until the API audit grants the Analytics & Reporting
// exception nothing may be derived from those numbers, so the page adds, ranks, averages and
// compares nothing: it only writes the values out.

/** A value as YouTube gave it: a whole number with its thousands marked, anything else as it came. */
function Value({ value, locale }: { value: number | null | undefined; locale: string }) {
  if (typeof value !== "number") return <span className="text-[var(--muted)]">—</span>;
  return <>{Number.isInteger(value) ? value.toLocaleString(locale) : String(value)}</>;
}

function RowsTable({ rows }: { rows: ReportRow[] }) {
  const t = useTranslations("admin.videoShorts");
  const locale = useLocale();
  const when = useWhen();
  // A column only for a value some row carries: the Data API gives three of the nine.
  const columns = REPORT_VALUES.filter((field) => rows.some((row) => typeof row[field] === "number"));
  return <div className="overflow-x-auto"><table className="w-full min-w-[40rem] text-left text-sm">
    <caption className="pb-2 text-left text-xs font-black tracking-[.12em] text-[var(--teal)]">{t("report.rowsTitle")}</caption>
    <thead><tr className="text-xs text-[var(--muted)]">
      <th scope="col" className="py-1 pr-3 font-semibold">{t("report.columns.short")}</th>
      <th scope="col" className="py-1 pr-3 font-semibold">{t("report.columns.period")}</th>
      {columns.map((field: ReportValue) => <th key={field} scope="col" className="py-1 pr-3 font-semibold">{t(`report.values.${field}`)}</th>)}
      <th scope="col" className="py-1 font-semibold">{t("report.columns.read")}</th>
    </tr></thead>
    <tbody>{rows.map((row) => <tr key={`${row.youtube_video_id}-${row.source}-${row.period}`} className="border-t border-[var(--line)] align-top">
      <th scope="row" className="py-2 pr-3 font-semibold">{row.title ?? row.slug}<span className="block font-mono text-xs font-normal text-[var(--muted)]">{row.youtube_video_id}</span></th>
      <td className="py-2 pr-3">{t(`metrics.columns.${row.period}`)}{row.range_start && row.range_end && <span className="block text-xs text-[var(--muted)]">{t("report.range", { start: row.range_start, end: row.range_end })}</span>}</td>
      {columns.map((field) => <td key={field} className="py-2 pr-3"><Value value={row[field]} locale={locale} /></td>)}
      <td className="py-2 text-xs text-[var(--muted)]">{t("metrics.readAt", { source: t(`metrics.sources.${row.source}`), time: when(row.captured_at) })}</td>
    </tr>)}</tbody>
  </table></div>;
}

function ReportCard({ report }: { report: Report }) {
  const t = useTranslations("admin.videoShorts");
  const when = useWhen();
  const week = t("report.week", { start: report.week_start, end: addDays(report.week_start, 6) });
  const model = [report.provider, report.model].filter(Boolean).join(" ");
  return <article aria-label={week} className="grid gap-4 rounded-[1.5rem] border border-[var(--line)] bg-[var(--surface)] p-5 shadow-[var(--shadow-sm)]">
    <header className="grid gap-1">
      <h2 className="text-lg font-bold">{week}</h2>
      <p className="text-sm text-[var(--muted)]">{t("report.writtenBy", { model: model || t("report.modelUnknown"), time: when(report.generated_at) })}</p>
    </header>
    {/* The model's text, never markup: React writes it as text, and pre-wrap keeps its lines. */}
    <div data-testid="shorts-report-body" className="whitespace-pre-wrap break-words text-sm leading-7">{report.body_md}</div>
    {report.rows.length > 0 ? <RowsTable rows={report.rows} /> : <p className="text-sm text-[var(--muted)]">{t("report.noRows")}</p>}
    <section aria-label={t("report.planTitle")} className="grid gap-2">
      <h3 className="text-xs font-black tracking-[.12em] text-[var(--teal)]">{t("report.planTitle")}</h3>
      {report.plan.length === 0 ? <p className="text-sm text-[var(--muted)]">{t("report.planEmpty")}</p> : <ul className="grid gap-1 text-sm leading-6">{report.plan.map((item, index) => <li key={index}>
        {[item.starts_at && when(item.starts_at), item.line && t(`lines.${item.line}`), item.topic_slug].filter(Boolean).join(" · ")}
        {item.note && <span className="text-[var(--muted)]">{item.starts_at || item.line || item.topic_slug ? " — " : ""}{item.note}</span>}
      </li>)}</ul>}
    </section>
  </article>;
}

export function ShortsReport() {
  const t = useTranslations("admin.videoShorts");
  const [reports, setReports] = useState<Report[] | null>(null);
  const [error, setError] = useState("");
  const load = useCallback(() => {
    api<Reports>("/admin/video-shorts/reports").then((value) => { setReports(value.items); setError(""); }).catch((problem: unknown) => setError(message(problem)));
  }, []);
  useEffect(load, [load]);
  if (error) return <AdminErrorState title={t("loadError")} detail={error} retry={load} retryLabel={t("retry")} />;
  if (!reports) return <p className="text-[var(--muted)]">{t("loading")}</p>;
  return <div className="grid gap-5" aria-label={t("views.report")}>
    <p className="text-sm leading-6 text-[var(--muted)]">{t("report.help")}</p>
    {reports.length === 0 ? <AdminEmptyState title={t("report.empty")} detail={t("report.emptyDetail")} /> : reports.map((report) => <ReportCard key={report.id} report={report} />)}
  </div>;
}
