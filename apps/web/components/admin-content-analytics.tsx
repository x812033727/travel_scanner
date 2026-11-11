"use client";

import { useLocale } from "next-intl";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { contentAnalyticsCopy, isContentAnalyticsReport, type ContentAnalyticsReport } from "@/lib/content-analytics";

/** A separate read: missing capability or a failed report never replaces the dashboard. */
export function AdminContentAnalytics({ range, includeBots, refreshKey = 0 }: {
  range: string;
  includeBots: boolean;
  refreshKey?: number;
}) {
  const locale = useLocale();
  const copy = contentAnalyticsCopy(locale);
  const [attempt, setAttempt] = useState(0);
  const [result, setResult] = useState<{ key: string; data?: ContentAnalyticsReport; failed?: boolean }>();
  const key = `${range}:${includeBots}:${refreshKey}:${attempt}`;
  useEffect(() => {
    const controller = new AbortController();
    api<unknown>(`/admin/analytics/content?range=${encodeURIComponent(range)}&include_bots=${includeBots}`, { signal: controller.signal })
      .then((data) => {
        if (!controller.signal.aborted) setResult(isContentAnalyticsReport(data) ? { key, data } : { key, failed: true });
      })
      .catch(() => { if (!controller.signal.aborted) setResult({ key, failed: true }); });
    return () => controller.abort();
  }, [includeBots, key, range]);
  const current = result?.key === key ? result : undefined;
  const data = current?.data;
  const date = new Intl.DateTimeFormat(locale, { dateStyle: "medium", timeStyle: "short", timeZone: "Asia/Taipei" });
  const number = new Intl.NumberFormat(locale);
  return (
    <section aria-labelledby="content-clicks-heading" className="min-w-0 rounded-[1.75rem] border border-[var(--line)] bg-[var(--surface)] p-5 md:p-6" data-testid="content-analytics">
      <h2 id="content-clicks-heading" className="text-xl font-bold">{copy.title}</h2>
      <p className="mt-2 text-sm leading-6 text-[var(--muted)]">{copy.help}</p>
      {!current ? <p role="status" className="mt-4">{copy.loading}</p> : current.failed ? (
        <div className="mt-4"><p role="status">{copy.unavailable}</p><button type="button" onClick={() => setAttempt((value) => value + 1)} className="mt-2 min-h-11 rounded-xl border border-[var(--line)] px-4 font-semibold">{copy.retry}</button></div>
      ) : data && !data.available ? <p className="mt-4" role="status">{copy.rawOnly}</p> : data ? (
        <>
          <p className="mt-4 text-3xl font-bold tabular-nums" data-testid="content-clicks-total">{number.format(data.total_clicks)}</p>
          <p className="mt-2 text-sm leading-6 text-[var(--muted)]">{copy.window}: {date.format(new Date(data.from))} — {date.format(new Date(data.to))} · Asia/Taipei</p>
          {data.window_clipped ? <p className="mt-2 text-sm leading-6">{copy.clipped}</p> : null}
          <p className="mt-2 text-sm leading-6 text-[var(--muted)]">{copy.firstRecorded}: {data.first_recorded_at ? date.format(new Date(data.first_recorded_at)) : copy.unknown}</p>
          {!data.total_clicks ? <p className="mt-4 leading-7">{copy.empty}</p> : null}
          {data.rows.length ? <>
            <h3 className="mt-6 font-semibold">{copy.pairs}</h3>
            <ol className="mt-3 divide-y divide-[var(--line)]">
              {data.rows.map((row) => <li key={`${row.source_path}:${row.target_path}:${row.placement}:${row.locale}`} className="py-4">
                <dl className="grid min-w-0 gap-2 text-sm sm:grid-cols-2">
                  <div className="min-w-0"><dt className="text-[var(--muted)]">{copy.source}</dt><dd className="mt-1 [overflow-wrap:anywhere]">{row.source_path}</dd></div>
                  <div className="min-w-0"><dt className="text-[var(--muted)]">{copy.target}</dt><dd className="mt-1 [overflow-wrap:anywhere]">{row.target_path}</dd></div>
                  <div><dt className="text-[var(--muted)]">{copy.placement}</dt><dd>{copy[row.placement]}</dd></div>
                  <div><dt className="text-[var(--muted)]">{copy.locale}</dt><dd>{row.locale}</dd></div>
                  <div><dt className="text-[var(--muted)]">{copy.clicks}</dt><dd className="font-bold tabular-nums">{number.format(row.clicks)}</dd></div>
                </dl>
              </li>)}
            </ol>
          </> : null}
        </>
      ) : null}
    </section>
  );
}
