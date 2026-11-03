"use client";

import { BarChart3, LoaderCircle } from "lucide-react";
import { useLocale } from "next-intl";
import { useCallback, useEffect, useState } from "react";
import { useAdminActionGuard } from "@/components/admin-action-guard";
import { AdminStatusPill } from "@/components/admin-ui";
import { useWhen } from "@/components/admin-video-review-card";
import { Button } from "@/components/community/ui";
import { api } from "@/lib/api";
import { fill, youtubeReportsCopy } from "@/lib/youtube-reports-copy";

// The channel reports line on the YouTube card (docs/videos/YOUTUBE-REPORTS.md;
// apps/api/app/video_youtube/reports.py): whether the grant reads YouTube Analytics, how far the
// site's copy of the daily reports reaches, and a button that fetches them now. Paired AI sessions
// read the rows themselves with their video tool token (skill youtube-channel-reports).
export type ReportsOverview = {
  linked: boolean;
  analytics_granted: boolean;
  synced_at: string | null;
  problem: string | null;
  reports: { report_type_id: string; days: number; first_day: string | null; last_day: string | null }[];
  waiting_for_first_report: { report_type_id: string }[];
};
type SyncOut = { status: string; downloaded: number; replaced: number; problem: string | null };

/** ``reloadKey`` changes when the connection does (a link or an unlink), so the line reads again. */
export function YoutubeChannelReports({ reloadKey, analyticsGranted }: { reloadKey: string; analyticsGranted: boolean }) {
  const locale = useLocale();
  const copy = youtubeReportsCopy(locale);
  const when = useWhen();
  const manage = useAdminActionGuard("content.manage");
  const [overview, setOverview] = useState<ReportsOverview | null>(null);
  const [loadError, setLoadError] = useState("");
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const load = useCallback(() => {
    api<ReportsOverview>("/admin/video-youtube/reports")
      .then((value) => { setOverview(value); setLoadError(""); })
      .catch((problem: unknown) => setLoadError(problem instanceof Error ? problem.message : ""));
  }, []);
  useEffect(() => { load(); }, [load, reloadKey]);

  const sync = async () => {
    setBusy(true);
    setError("");
    setMessage("");
    try {
      const result = await api<SyncOut>("/admin/video-youtube/reports/sync", { method: "POST" });
      if (result.problem && result.status !== "partial") setError(result.problem);
      else if (result.status === "partial") setMessage(fill(copy.partial, { downloaded: result.downloaded }));
      else if (result.status === "running") setMessage(copy.running);
      else if (result.status === "not_due") setMessage(copy.notDue);
      else setMessage(fill(copy.synced, { downloaded: result.downloaded, replaced: result.replaced }));
      load();
    } catch (problem) {
      setError(problem instanceof Error ? problem.message : String(problem));
    } finally {
      setBusy(false);
    }
  };

  const days = (overview?.reports ?? []).flatMap((item) => [item.first_day, item.last_day]).filter((day): day is string => Boolean(day)).sort();
  return <div className="grid gap-2 rounded-xl border border-[var(--line)] p-4" aria-label={copy.title}>
    <p className="flex flex-wrap items-center gap-2 font-semibold"><BarChart3 aria-hidden size={18} />{copy.title}</p>
    <p className="text-sm leading-6 text-[var(--muted)]">{copy.help}</p>
    {!analyticsGranted
      ? <p role="alert" className="flex flex-wrap items-center gap-2 text-sm text-amber-800"><AdminStatusPill status="inactive">Analytics</AdminStatusPill>{copy.needsRelink}</p>
      : <>
        {loadError && <p role="alert" className="text-sm text-red-800">{fill(copy.loadError, { message: loadError })}</p>}
        {overview && <p className="text-sm">
          {overview.synced_at ? fill(copy.syncedAt, { time: when(overview.synced_at) }) : copy.notSynced}
          {overview.reports.length > 0 && days.length > 0 && ` · ${fill(copy.coverage, { count: overview.reports.length, first: days[0], last: days[days.length - 1] })}`}
        </p>}
        {overview && overview.waiting_for_first_report.length > 0 && <p className="text-sm text-[var(--muted)]">{fill(copy.waiting, { count: overview.waiting_for_first_report.length })}</p>}
        {overview?.problem && <p role="alert" className="text-sm text-red-800">{overview.problem}</p>}
        <div><Button secondary disabled={!manage.allowed || busy} onClick={() => void sync()}>{busy ? <LoaderCircle aria-hidden size={16} className="animate-spin" /> : <BarChart3 aria-hidden size={16} />}{busy ? copy.syncing : copy.sync}</Button></div>
      </>}
    {error && <p role="alert" className="text-sm text-red-800">{error}</p>}
    {message && !error && <p role="status" className="text-sm text-[var(--teal)]">{message}</p>}
  </div>;
}

/** The scope step's second line: the analytics scope the link asks for besides YouTube's own. */
export function analyticsScopeLine(locale: string, scope: string): string | null {
  const analytics = scope.split(/\s+/).find((item) => item.includes("yt-analytics"));
  return analytics ? fill(youtubeReportsCopy(locale).scopeStep, { scope: analytics }) : null;
}
