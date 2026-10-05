"use client";

import { useTranslations } from "next-intl";
import { useEffect, useState } from "react";
import { FilterPills } from "@/components/admin-filter-pills";
import { AdminDataTable, AdminEmptyState, AdminErrorState, AdminFilterBar, AdminStatusPill } from "@/components/admin-ui";
import {
  control, isBlocked, type ProjectSummary, ProductionPill, PublishPill, publishState, REFRESH_MS, useWhen, VIDEO_CATEGORIES, type VideoCategory, type VideoPage, youtubeSyncStuck,
} from "@/components/admin-video-review-card";
import { syncRunning } from "@/components/admin-video-youtube";
import { Button } from "@/components/community/ui";
import { updateAdminQuery, useAdminQueryValue } from "@/lib/admin-workspace-navigation";
import { api } from "@/lib/api";
import { isPageNumber } from "@/lib/guides-admin";

// Where a tutorial stands, the catalog's second filter (apps/api/app/video_reviews/schemas.py
// BrowseState): still being made, on YouTube, or dropped by the owner.
export const BROWSE_STATES = ["working", "published", "dropped"] as const;
type BrowseState = (typeof BROWSE_STATES)[number];
const PAGE_SIZE = 30;
const COLUMNS = ["title", "category", "state", "pending", "progress", "youtube", "synced"] as const;
const STATE_KEYS: Record<BrowseState, string> = { working: "inProgress", published: "publishedSection", dropped: "dropped" };
// Module-level so useAdminQueryValue sees one validator across renders.
const isCategoryFilter = (value: string) => value === "none" || (VIDEO_CATEGORIES as readonly string[]).includes(value);
const isBrowseState = (value: string) => (BROWSE_STATES as readonly string[]).includes(value);
const countsOf = (facets: { code: string; count: number }[] | undefined) => Object.fromEntries((facets ?? []).map((facet) => [facet.code, facet.count])) as Partial<Record<string, number>>;
const sumOf = (facets: { code: string; count: number }[] | undefined) => (facets ? facets.reduce((sum, facet) => sum + facet.count, 0) : undefined);

/** The category as a pill: its label, or "uncategorized" for a video nobody filed yet. */
export function CategoryPill({ category }: { category: VideoCategory | null | undefined }) {
  const t = useTranslations("admin.videoReviews");
  return <AdminStatusPill status={category ? "queued" : "inactive"}>{category ? t(`categories.${category}`) : t("uncategorized")}</AdminStatusPill>;
}

/** One line of the catalog: the title (and the series a drama episode belongs to), its category, where it stands, and the numbers the cards showed. */
function VideoRow({ project, onOpen }: { project: ProjectSummary; onOpen: (slug: string) => void }) {
  const t = useTranslations("admin.videoReviews");
  const ty = useTranslations("admin.videoYoutube");
  const when = useWhen();
  const done = project.checklist.filter((item) => item.done).length;
  const step = project.checklist.find((item) => !item.done)?.label ?? project.stage;
  const dropped = Boolean(project.dropped_at);
  return <tr className="border-t border-[var(--line)] align-top">
    <td data-label={t("table.title")} className="px-4 py-3">
      <button type="button" className="text-left font-semibold underline-offset-2 hover:underline" onClick={() => onOpen(project.slug)}>{project.title}</button>
      <span className="block text-xs text-[var(--muted)]">{project.slug}</span>
      {project.series_slug && <span className="block text-xs text-[var(--muted)]">{project.compilation ? t("compilationOf", { series: project.series_slug }) : t("episodeOf", { series: project.series_slug, number: project.episode_number ?? 0 })}</span>}
    </td>
    <td data-label={t("table.category")} className="px-4 py-3"><CategoryPill category={project.category} /></td>
    <td data-label={t("table.state")} className="px-4 py-3">
      <span className="flex flex-wrap items-center gap-1">
        {dropped ? <AdminStatusPill status="inactive">{t("dropped")}</AdminStatusPill> : <PublishPill project={project} production={false} />}
        <ProductionPill project={project} compact />
        {!dropped && isBlocked(project) && <AdminStatusPill status="failed">{t("stuck")}</AdminStatusPill>}
        {syncRunning(project.youtube_sync) && <AdminStatusPill status="running">{ty("sendingPill")}</AdminStatusPill>}
        {youtubeSyncStuck(project.youtube_sync) && <AdminStatusPill status="failed">{ty("stuckPill")}</AdminStatusPill>}
        {!dropped && !project.youtube_video_id && !publishState(project) && <span className="text-xs text-[var(--muted)]">{step}</span>}
      </span>
    </td>
    <td data-label={t("table.pending")} className="px-4 py-3">
      {project.pending ? <AdminStatusPill status="pending">{t("pending", { count: project.pending })}</AdminStatusPill> : <span className="text-[var(--muted)]">{t("noPendingShort")}</span>}
    </td>
    <td data-label={t("table.progress")} className="px-4 py-3">{t("progress", { done, total: project.checklist.length })}</td>
    <td data-label={t("table.youtube")} className="px-4 py-3">
      {project.youtube_video_id
        ? <>{t("youtube", { id: project.youtube_video_id })}{project.youtube_publish_at && <span className="block text-xs text-[var(--muted)]">{t("scheduledAt", { time: when(project.youtube_publish_at) })}</span>}</>
        : <span className="text-[var(--muted)]">{t("notOnYoutube")}</span>}
    </td>
    <td data-label={t("table.synced")} className="px-4 py-3"><time dateTime={project.last_synced_at}>{when(project.last_synced_at)}</time></td>
  </tr>;
}

/**
 * The catalog of every tutorial under the two groups that wait for the owner (the category section
 * of docs/videos/HANDS-OFF.md): one line a video, narrowed by a category, a state and a search, a page at a time. The
 * filters live in the URL, so a view can be bookmarked and the back button undoes a filter; the counts
 * on the pills come from the server with the other filters kept. The page reads the site again every
 * REFRESH_MS like the groups above it, for the same query, and again when `revision` changes (the groups
 * above changed something); the search box keeps what the owner is typing until they submit it.
 */
export function VideoBrowser({ onOpen, revision = 0 }: { onOpen: (slug: string) => void; revision?: number }) {
  const t = useTranslations("admin.videoReviews");
  const [category] = useAdminQueryValue("category", "", isCategoryFilter);
  const [state] = useAdminQueryValue("state", "", isBrowseState);
  const [query] = useAdminQueryValue("q");
  const [pageValue] = useAdminQueryValue("page", "1", isPageNumber);
  const page = Number(pageValue);
  const params = new URLSearchParams({ page: String(page), limit: String(PAGE_SIZE) });
  if (category) params.set("category", category);
  if (state) params.set("state", state);
  if (query) params.set("q", query);
  const suffix = params.toString();
  const filtered = Boolean(category || state || query);
  const [reload, setReload] = useState(0);
  // The page is keyed by what it was loaded for: a filter change shows the loading state without an
  // effect resetting anything, and a refresh for the same key replaces it in place.
  const key = `${suffix}#${reload}#${revision}`;
  const [loaded, setLoaded] = useState<{ key: string; data: VideoPage | null; error: string }>();
  const data = loaded?.key === key ? loaded.data : undefined;
  const error = loaded?.key === key ? loaded.error : "";
  const [draft, setDraft] = useState({ seen: query, text: query });
  const text = draft.seen === query ? draft.text : query;

  useEffect(() => {
    let controller = new AbortController();
    const load = () => {
      controller.abort();
      controller = new AbortController();
      const { signal } = controller;
      api<VideoPage>(`/admin/videos/browse?${suffix}`, { signal }).then((value) => {
        if (signal.aborted) return;
        if (!value || !Array.isArray(value.items)) throw new TypeError("not a page of videos");
        setLoaded({ key, data: value, error: "" });
        // A page past the last one (a filter narrowed the list, or a video was dropped) falls back to the last.
        if (value.pages > 0 && page > value.pages) updateAdminQuery({ page: value.pages > 1 ? String(value.pages) : "" });
      }).catch((problem: unknown) => {
        if (!signal.aborted) setLoaded({ key, data: null, error: problem instanceof Error ? problem.message : "" });
      });
    };
    load();
    const timer = window.setInterval(load, REFRESH_MS);
    return () => { window.clearInterval(timer); controller.abort(); };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [suffix, reload, revision]);

  const categoryCounts = countsOf(data?.facets.category);
  const stateCounts = countsOf(data?.facets.state);
  return <section aria-label={t("browserTitle")} className="grid gap-3">
    <h2 className="text-xs font-black tracking-[.16em] text-[var(--teal)]">{t("browserTitle")}</h2>
    <FilterPills
      label={t("categoryFilter")}
      allLabel={t("categoryAll")}
      allCount={sumOf(data?.facets.category)}
      options={[
        ...VIDEO_CATEGORIES.map((code) => ({ code, label: t(`categories.${code}`), count: categoryCounts[code] })),
        { code: "none", label: t("uncategorized"), count: categoryCounts.none },
      ]}
      value={category}
      onChange={(code) => updateAdminQuery({ category: code, page: "" })}
    />
    <AdminFilterBar>
      <FilterPills
        label={t("stateFilter")}
        allLabel={t("stateAll")}
        allCount={sumOf(data?.facets.state)}
        options={BROWSE_STATES.map((code) => ({ code, label: t(STATE_KEYS[code]), count: stateCounts[code] }))}
        value={state}
        onChange={(code) => updateAdminQuery({ state: code, page: "" })}
      />
      <form className="flex flex-wrap items-end gap-3 sm:ml-auto" onSubmit={(event) => { event.preventDefault(); updateAdminQuery({ q: text.trim(), page: "" }); }}>
        <label className="grid gap-2 text-sm font-semibold">{t("search")}
          <input type="search" className={control} value={text} placeholder={t("searchPlaceholder")} onChange={(event) => setDraft({ seen: query, text: event.target.value })} />
        </label>
        <Button type="submit" secondary>{t("search")}</Button>
      </form>
    </AdminFilterBar>
    {error && <AdminErrorState title={t("loadError")} detail={error} retry={() => setReload((value) => value + 1)} retryLabel={t("retry")} />}
    {data === undefined && !error && <p role="status" className="text-sm text-[var(--muted)]">{t("browserLoading")}</p>}
    {data && data.total === 0 && (filtered ? <p role="status">{t("noMatches")}</p> : <AdminEmptyState title={t("empty")} detail={t("emptyDetail")} />)}
    {data && data.total > 0 && <>
      <AdminDataTable label={t("browserTitle")} headers={COLUMNS.map((column) => t(`table.${column}`))}>
        {data.items.map((project) => <VideoRow key={project.slug} project={project} onOpen={onOpen} />)}
      </AdminDataTable>
      <p className="text-sm text-[var(--muted)]">{t("browserCount", { total: data.total })}</p>
      {data.pages > 1 && <nav className="flex flex-wrap items-center gap-3" aria-label={t("page", { page: data.page, pages: data.pages })}>
        <Button secondary disabled={page <= 1} onClick={() => updateAdminQuery({ page: page - 1 > 1 ? String(page - 1) : "" })}>{t("previous")}</Button>
        <span className="text-sm">{t("page", { page: data.page, pages: data.pages })}</span>
        <Button secondary disabled={page >= data.pages} onClick={() => updateAdminQuery({ page: String(page + 1) })}>{t("next")}</Button>
      </nav>}
    </>}
  </section>;
}

/**
 * The owner files a video under a category on its page, or under none. The select follows the saved
 * value whenever it changes (a save, the worker's first report), while a choice in progress survives
 * the page's minute-by-minute reads that bring the same value back. A reader sees the value and no save.
 */
export function CategoryPanel({ slug, project, canManage, onSaved }: { slug: string; project: ProjectSummary; canManage: boolean; onSaved: () => void }) {
  const t = useTranslations("admin.videoReviews");
  const saved = project.category ?? "";
  const [draft, setDraft] = useState({ seen: saved, value: saved });
  const value = draft.seen === saved ? draft.value : saved;
  const [busy, setBusy] = useState(false);
  const [notice, setNotice] = useState("");
  const [error, setError] = useState("");
  const save = async () => {
    setBusy(true);
    setNotice("");
    setError("");
    try {
      await api(`/admin/videos/${slug}/category`, { method: "PUT", body: JSON.stringify({ category: value || null }) });
      setNotice(t("categorySaved"));
      onSaved();
    } catch (problem) {
      setError(t("categoryError", { message: problem instanceof Error ? problem.message : "" }));
    } finally {
      setBusy(false);
    }
  };
  return <form aria-label={t("categoryTitle")} className="flex flex-wrap items-end gap-3 text-sm" onSubmit={(event) => { event.preventDefault(); void save(); }}>
    <label className="grid min-w-[14rem] gap-2 font-semibold">{t("categoryTitle")}
      <select className={control} value={value} disabled={!canManage || busy} onChange={(event) => setDraft({ seen: saved, value: event.target.value })}>
        <option value="">{t("uncategorized")}</option>
        {VIDEO_CATEGORIES.map((code) => <option key={code} value={code}>{t(`categories.${code}`)}</option>)}
      </select>
    </label>
    {canManage && <Button type="submit" secondary disabled={busy || value === saved}>{busy ? t("saving") : t("categorySave")}</Button>}
    <span className="basis-full leading-6 text-[var(--muted)]">{t("categoryHelp")}</span>
    {notice && <span role="status" className="basis-full">{notice}</span>}
    {error && <span role="alert" className="basis-full text-red-800">{error}</span>}
  </form>;
}
