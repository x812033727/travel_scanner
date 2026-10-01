"use client";

import { useFormatter, useTranslations } from "next-intl";
import { useCallback, useState } from "react";
import { AdminEmptyState, AdminErrorState, AdminStatusPill } from "@/components/admin-ui";
import { useRefresh, useWhen } from "@/components/admin-video-review-card";
import { blankReason, message, type Metric, METRIC_PERIODS, type MetricPeriod, type Metrics, type ShortMetrics } from "@/components/admin-video-shorts-data";
import { Button } from "@/components/community/ui";
import { api } from "@/lib/api";

// The numbers view of the Shorts tab (docs/videos/SHORTS.md, the section on results): every
// public Short with the snapshot of day 1, 3 and 7 and the latest read, each number as YouTube
// reported it, with where it came from and when it was read. YouTube's developer policies do not
// let a client derive metrics from API data before its audit covers that, so nothing here is
// added up, averaged, ranked or turned into a rate: a cell is a number YouTube gave, or it is
// empty and says why.
const COUNTS = ["views", "likes", "comments"] as const;

function Snapshot({ snapshot }: { snapshot: Metric }) {
  const t = useTranslations("admin.videoShorts");
  const format = useFormatter();
  const when = useWhen();
  return <div className="grid gap-1">
    <dl className="grid gap-0.5">{COUNTS.map((name) => <div key={name} className="flex items-baseline justify-between gap-3">
      <dt className="text-xs text-[var(--muted)]">{t(`metrics.${name}`)}</dt>
      <dd className="font-mono">{snapshot[name] === null ? <span className="text-xs text-[var(--muted)]">{t("metrics.hidden")}</span> : format.number(snapshot[name] ?? 0)}</dd>
    </div>)}</dl>
    <p className="text-xs leading-5 text-[var(--muted)]">{t("metrics.readAt", { source: t(`metrics.sources.${snapshot.source}`), time: when(snapshot.captured_at) })}</p>
  </div>;
}

function Row({ short, onOpenVideo }: { short: ShortMetrics; onOpenVideo: (slug: string) => void }) {
  const t = useTranslations("admin.videoShorts");
  const when = useWhen();
  const cell = (period: MetricPeriod) => {
    const snapshots = short.snapshots.filter((snapshot) => snapshot.period === period);
    if (snapshots.length) return <div className="grid gap-3">{snapshots.map((snapshot) => <Snapshot key={snapshot.source} snapshot={snapshot} />)}</div>;
    return <p className="text-xs leading-5 text-[var(--muted)]">{t(`metrics.blank.${blankReason(period, short)}`)}</p>;
  };
  return <tr className="border-t border-[var(--line)] align-top">
    <th scope="row" className="py-3 pr-3 text-left"><div className="grid gap-1">
      <span className="font-semibold">{short.title}</span>
      <span className="flex flex-wrap items-center gap-2 text-xs font-normal text-[var(--muted)]">
        {short.line && <span>{t(`lines.${short.line}`)}</span>}
        {short.published_at && <span>{t("metrics.publishedAt", { time: when(short.published_at) })}</span>}
      </span>
      {short.removed_at && <span><AdminStatusPill status="failed">{t("metrics.removed", { time: when(short.removed_at) })}</AdminStatusPill></span>}
      {short.dropped_at && <span><AdminStatusPill status="inactive">{t("metrics.dropped", { time: when(short.dropped_at) })}</AdminStatusPill></span>}
      <span><Button secondary onClick={() => onOpenVideo(short.slug)}>{t("metrics.open")}</Button></span>
    </div></th>
    {METRIC_PERIODS.map((period) => <td key={period} className="py-3 pr-3" data-period={period}>{cell(period)}</td>)}
  </tr>;
}

export function ShortsMetrics({ onOpenVideo }: { onOpenVideo: (slug: string) => void }) {
  const t = useTranslations("admin.videoShorts");
  const [metrics, setMetrics] = useState<Metrics | null>(null);
  const [error, setError] = useState("");
  const load = useCallback(() => {
    api<Metrics>("/admin/video-shorts/metrics").then((value) => { setMetrics(value); setError(""); }).catch((problem: unknown) => setError(message(problem)));
  }, []);
  useRefresh(load);
  if (error) return <AdminErrorState title={t("loadError")} detail={error} retry={load} retryLabel={t("retry")} />;
  if (!metrics) return <p className="text-[var(--muted)]">{t("loading")}</p>;
  return <section aria-label={t("views.metrics")} className="grid gap-4">
    <p className="text-sm leading-6 text-[var(--muted)]">{t("metrics.help")}</p>
    {metrics.items.length === 0 ? <AdminEmptyState title={t("metrics.empty")} detail={t("metrics.emptyDetail")} /> : <div className="overflow-x-auto rounded-2xl border border-[var(--line)] bg-[var(--surface)] p-4">
      <table className="w-full min-w-[52rem] text-left text-sm" aria-label={t("views.metrics")}>
        <thead><tr className="text-xs text-[var(--muted)]">
          <th scope="col" className="py-1 pr-3 font-semibold">{t("metrics.columns.short")}</th>
          {/* Four columns of one width: an empty one would otherwise shrink to a word a line. */}
          {METRIC_PERIODS.map((period) => <th key={period} scope="col" className="w-[18%] py-1 pr-3 font-semibold">{t(`metrics.columns.${period}`)}</th>)}
        </tr></thead>
        <tbody>{metrics.items.map((short) => <Row key={short.slug} short={short} onOpenVideo={onOpenVideo} />)}</tbody>
      </table>
    </div>}
  </section>;
}
