"use client";

import { useEffect, useState } from "react";
import { useLocale } from "next-intl";
import { Link } from "@/i18n/navigation";
import { api } from "@/lib/api";
import { fillNewsCopy } from "@/lib/admin-news-copy";
import { newsEditorialCopy, type FreshnessReport } from "@/lib/news-editorial";
import { panelClass } from "@/components/community/ui";

export function AdminNewsEditorial() {
  const locale = useLocale();
  const copy = newsEditorialCopy(locale);
  const [view, setView] = useState("all");
  const [page, setPage] = useState(1);
  const [loaded, setLoaded] = useState<{ key: string; data: FreshnessReport }>();
  const [failedKey, setFailedKey] = useState("");
  const [reload, setReload] = useState(0);
  const key = `${view}:${page}:${reload}`;
  const data = loaded?.key === key ? loaded.data : undefined;
  const failed = failedKey === key;
  useEffect(() => {
    const controller = new AbortController();
    api<FreshnessReport>(`/admin/news/freshness?view=${view}&page=${page}`, { signal: controller.signal })
      .then((value) => { if (!controller.signal.aborted) { setLoaded({ key, data: value }); setFailedKey(""); } })
      .catch(() => { if (!controller.signal.aborted) setFailedKey(key); });
    return () => controller.abort();
  }, [key, page, view]);

  return <details className={`${panelClass} mt-6`}>
    <summary className="cursor-pointer font-bold">{copy.title}{data ? ` · ${copy.due}: ${data.due_count}` : ""}</summary>
    <div className="mt-4 space-y-3">
      <p className="text-sm text-[var(--muted)]">{copy.explanation}</p>
      <label className="flex items-center gap-2">{copy.filter}<select className="min-h-11 rounded border border-[var(--line)] bg-[var(--surface)] px-3" value={view} onChange={(event) => { setView(event.target.value); setPage(1); }}>
        <option value="all">{copy.all}</option><option value="due">{copy.due}</option><option value="changed">{copy.changed}</option>
      </select></label>
      {failed ? <p role="status">{copy.unavailable}</p> : !data ? <p role="status">{copy.loading}</p> : <>
        <p>{data.enabled ? copy.enabled : copy.disabled}</p>
        <p className="text-sm">{fillNewsCopy(copy.coverage, { days: data.coverage_days, interval: data.interval_days, limit: data.daily_limit })}</p>
        <p>{fillNewsCopy(copy.counts, { total: data.eligible_count, due: data.due_count, shown: data.items.length })}</p>
        {!data.items.length ? <p>{copy.empty}</p> : <ul className="divide-y divide-[var(--line)]">
          {data.items.map((item) => <li key={item.candidate_id} className="py-3">
            <Link className="font-medium underline underline-offset-4" href={`/admin/news?tab=review&queue=published&candidate=${encodeURIComponent(item.candidate_id)}`}>{item.title}</Link>
            <p className="mt-1 text-sm">{copy[item.status]}{item.review_due ? ` · ${copy.due}` : ""}{item.validity_expired ? ` · ${copy.expired}` : ""}</p>
            {item.checked_at && <p className="text-xs text-[var(--muted)]">{copy.checked}: <time dateTime={item.checked_at}>{new Date(item.checked_at).toLocaleString(locale)}</time></p>}
          </li>)}
        </ul>}
        <nav className="flex flex-wrap items-center gap-3" aria-label={copy.pagination}>
          <button className="min-h-11 rounded border px-3 disabled:opacity-40" type="button" disabled={page <= 1} onClick={() => setPage((value) => value - 1)}>{copy.previous}</button>
          <span>{fillNewsCopy(copy.page, { page: data.page, pages: data.pages, total: data.total_count })}</span>
          <button className="min-h-11 rounded border px-3 disabled:opacity-40" type="button" disabled={page >= data.pages} onClick={() => setPage((value) => value + 1)}>{copy.next}</button>
        </nav>
      </>}
      <button type="button" className="min-h-11 rounded border border-[var(--line)] px-4 text-sm" onClick={() => setReload((value) => value + 1)}>{copy.reload}</button>
    </div>
  </details>;
}
