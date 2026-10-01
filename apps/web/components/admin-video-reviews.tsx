"use client";

import { ArrowLeft, CheckCircle2, Circle, Clapperboard, Upload } from "lucide-react";
import { useTranslations } from "next-intl";
import { type ReactNode, useCallback, useEffect, useMemo, useState } from "react";
import { useAdminActionGuard } from "@/components/admin-action-guard";
import { AdminErrorState, AdminStatusPill } from "@/components/admin-ui";
import { CategoryPanel, VideoBrowser } from "@/components/admin-video-browser";
import {
  CompilationDownload, control, finalApproved, isBlocked, type LocaleChoice, LOCALE_PARTS, LOCALES, mp4Retired, needsOwner, partStateLabel, type Project,
  type ProjectSummary, PublishPill, publishState, REFRESH_MS, readyToUpload, type Review, ReviewCard, SLUG, UploadPackage, UploadedForm, fileUrl,
  useRefresh, useWhen, youtubeSyncStuck,
} from "@/components/admin-video-review-card";
import { AdminVideoSeries, DocPanel, type Series } from "@/components/admin-video-series";
import { AdminVideoSettings } from "@/components/admin-video-settings";
import { AdminVideoRenewal } from "@/components/admin-video-renewal";
import { AdminVideoShorts } from "@/components/admin-video-shorts";
import { stateTone } from "@/components/admin-video-shorts-data";
import { DiscussionThread, scriptSubject } from "@/components/admin-video-thread";
import { syncRunning, useYoutubeConnection, YoutubeChannelCard, type YoutubeConnection, YoutubeLinkHint, YoutubePublishForm, YoutubeSyncPanel } from "@/components/admin-video-youtube";
import { Button, Tabs } from "@/components/community/ui";
import { useAdminQueryState, useAdminQueryValue } from "@/lib/admin-workspace-navigation";
import { api } from "@/lib/api";

// The review card, the gate bodies and the shared types live in admin-video-review-card.tsx;
// these two are re-exported so older imports keep working. The drama tab (series and one-off
// episodes) is admin-video-series.tsx; this file holds the tutorial list, the video page and the tabs.
export { REFRESH_MS, fileUrl };

function RetryVideo({ project, canManage, onRequested }: { project: Project; canManage: boolean; onRequested: () => void }) {
  const t = useTranslations("admin.videoReviews");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  if (!isBlocked(project) || project.dropped_at) return null;
  const pending = Boolean(project.retry_request_id && project.retry_request_id !== project.retry_acknowledged_id);
  const retry = async () => {
    setBusy(true);
    setError("");
    try {
      await api(`/admin/videos/${project.slug}/retry`, { method: "POST" });
      onRequested();
    } catch (problem) {
      setError(t("retryVideoError", { message: problem instanceof Error ? problem.message : "" }));
    } finally {
      setBusy(false);
    }
  };
  return <section aria-label={t("retryVideoTitle")} className="rounded-2xl border border-amber-600 bg-amber-50 p-4">
    <p className="font-bold">{t("retryVideoTitle")}</p>
    <p className="mt-2 text-sm leading-6">{pending ? t("retryVideoPending") : t("retryVideoHelp")}</p>
    {error && <p role="alert" className="mt-2 text-sm text-red-800">{error}</p>}
    {canManage && !pending && <div className="mt-3"><Button disabled={busy} onClick={() => void retry()}>{busy ? t("saving") : t("retryVideoButton")}</Button></div>}
  </section>;
}

/** Stop a video for good, with a reason; the pipeline leaves it and its topic stays taken. */
function DropVideo({ slug, onDropped }: { slug: string; onDropped: () => void }) {
  const t = useTranslations("admin.videoReviews");
  const [note, setNote] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const drop = async () => {
    if (!note.trim() || !window.confirm(t("dropConfirm"))) return;
    setBusy(true);
    setError("");
    try {
      await api(`/admin/videos/${slug}/drop`, { method: "POST", body: JSON.stringify({ note: note.trim() }) });
      onDropped();
    } catch (problem) {
      setError(t("dropError", { message: problem instanceof Error ? problem.message : "" }));
    } finally {
      setBusy(false);
    }
  };
  return <details className="rounded-2xl border border-[var(--line)] p-4">
    <summary className="cursor-pointer font-bold">{t("dropTitle")}</summary>
    <div className="mt-3 grid gap-3">
      <p className="text-sm leading-6 text-[var(--muted)]">{t("dropDetail")}</p>
      <label className="grid gap-2 text-sm font-semibold">{t("dropReason")}
        <textarea className={control} rows={2} value={note} disabled={busy} placeholder={t("dropPlaceholder")} onChange={(event) => setNote(event.target.value)} />
      </label>
      {error && <p role="alert" className="text-sm text-red-800">{error}</p>}
      <div><Button secondary disabled={busy || !note.trim()} onClick={() => void drop()}>{busy ? t("saving") : t("dropButton")}</Button></div>
    </div>
  </details>;
}

type Choices = Record<(typeof LOCALES)[number], Required<LocaleChoice>>;
const NOTHING: Required<LocaleChoice> = { metadata: false, captions: false, dub: false };

/** The owner's saved choice as a full grid, so every box has a value and the same shape compares equal. */
function choicesOf(saved: ProjectSummary["locales"]): Choices {
  return Object.fromEntries(LOCALES.map((locale) => {
    const choice = saved?.[locale] ?? {};
    return [locale, { metadata: Boolean(choice.metadata), captions: Boolean(choice.captions || choice.dub), dub: Boolean(choice.dub) }];
  })) as Choices;
}

/** What goes to the server: only the languages with something ticked, in the page's order. */
function chosenBody(choices: Choices): Record<string, Required<LocaleChoice>> {
  return Object.fromEntries(LOCALES.filter((locale) => LOCALE_PARTS.some((part) => choices[locale][part])).map((locale) => [locale, choices[locale]]));
}

// What the panel reads from the settings for "tick the defaults": the tutorial and drama lists of
// languages to pre-tick (docs/videos/LANGUAGES.md; the settings tab, admin-video-settings.tsx).
type LanguageDefaults = { caption_locales?: string[]; drama?: { drama_caption_locales?: string[] } };

/**
 * The languages this video gets on top of Traditional Chinese and what of each: titles and
 * descriptions, closed captions, a dub track (docs/videos/LANGUAGES.md). The owner decides once
 * the final cut is approved; the worker then makes only what is ticked and reports each part back,
 * and the video is not scheduled until every chosen part is made. A dub track is timed with its
 * captions, so ticking it ticks them; a drama cannot be dubbed yet (docs/videos/DUBS.md). The panel
 * stays after the video is public: more can be ticked, and unticking only holds for what is not on
 * YouTube yet.
 */
function LanguagePanel({ slug, project, canManage, onSaved }: { slug: string; project: Project; canManage: boolean; onSaved: () => void }) {
  const t = useTranslations("admin.videoReviews");
  const drama = (project.format ?? "slides") === "drama";
  // The boxes follow the saved choice whenever it changes (a save, or another admin's), while an
  // edit in progress survives the page's minute-by-minute reads that bring the same choice back.
  const saved = choicesOf(project.locales);
  const savedKey = JSON.stringify(saved);
  const [chosen, setChosen] = useState<Choices>(saved);
  const [seen, setSeen] = useState(savedKey);
  if (seen !== savedKey) {
    setSeen(savedKey);
    setChosen(saved);
  }
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const decided = Boolean(project.locales_decided_at);
  const changed = JSON.stringify(chosen) !== savedKey;
  const nothingSaved = Object.keys(chosenBody(saved)).length === 0;
  const toggle = (locale: (typeof LOCALES)[number], part: (typeof LOCALE_PARTS)[number], on: boolean) => setChosen((current) => {
    const next = { ...current[locale], [part]: on };
    if (part === "dub" && on) next.captions = true;
    if (part === "captions" && !on) next.dub = false;
    return { ...current, [locale]: next };
  });
  const put = async (locales: Record<string, Required<LocaleChoice>>) => {
    setBusy(true);
    setError("");
    setMessage("");
    try {
      await api(`/admin/videos/${slug}/languages`, { method: "PUT", body: JSON.stringify({ locales }) });
      setMessage(t("languagesSaved"));
      onSaved();
    } catch (problem) {
      setError(t("languagesError", { message: problem instanceof Error ? problem.message : "" }));
    } finally {
      setBusy(false);
    }
  };
  const tickDefaults = async () => {
    setBusy(true);
    setError("");
    try {
      const settings = await api<LanguageDefaults>("/admin/video-automation/settings");
      const defaults = (drama ? settings.drama?.drama_caption_locales : settings.caption_locales) ?? [];
      setChosen(Object.fromEntries(LOCALES.map((locale) => [locale, defaults.includes(locale) ? { metadata: true, captions: true, dub: false } : NOTHING])) as Choices);
    } catch (problem) {
      setError(t("languagesError", { message: problem instanceof Error ? problem.message : "" }));
    } finally {
      setBusy(false);
    }
  };
  const locked = !canManage || busy;
  return <section aria-label={t("languagesTitle")} className="rounded-2xl border border-[var(--line)] bg-[var(--surface)] p-4">
    <p className="font-bold">{t("languagesTitle")}</p>
    {!finalApproved(project) ? <p className="mt-1 text-sm leading-6 text-[var(--muted)]">{t("languagesLater")}</p> : <>
      <p className="mt-1 text-sm leading-6 text-[var(--muted)]">{t("languagesHelp")}</p>
      {project.youtube_video_id && <p className="mt-1 text-sm leading-6 text-[var(--muted)]">{t("languagesAfterPublish")}</p>}
      <table className="mt-3 w-full text-sm">
        <thead><tr><th scope="col" className="sr-only">{t("languageColumn")}</th>{LOCALE_PARTS.map((part) => <th key={part} scope="col" className="py-1 text-left font-semibold">{t(`parts.${part}`)}</th>)}</tr></thead>
        <tbody>{LOCALES.map((locale) => <tr key={locale} className="border-t border-[var(--line)]">
          <th scope="row" className="py-2 pr-3 text-left font-semibold">{t(`locales.${locale}`)}</th>
          {LOCALE_PARTS.map((part) => {
            const dubOff = part === "dub" && drama;
            const state = saved[locale][part] ? project.languages?.[locale]?.[part] : undefined;
            return <td key={part} className="py-2 align-top">
              <label className="inline-flex min-h-8 flex-wrap items-center gap-2" title={dubOff ? t("dubDramaLater") : undefined}>
                <input type="checkbox" aria-label={`${t(`locales.${locale}`)} ${t(`parts.${part}`)}`} checked={chosen[locale][part]} disabled={locked || dubOff} onChange={(event) => toggle(locale, part, event.target.checked)} />
                {state && <span className="text-xs text-[var(--muted)]">{partStateLabel(t, state.state, state.reason)}</span>}
              </label>
            </td>;
          })}
        </tr>)}</tbody>
      </table>
      {error && <p role="alert" className="mt-2 text-sm text-red-800">{error}</p>}
      {message && !error && <p role="status" className="mt-2 text-sm text-[var(--muted)]">{message}</p>}
      <div className="mt-3 flex flex-wrap gap-3">
        <Button secondary disabled={locked} onClick={() => void tickDefaults()}>{t("tickDefaults")}</Button>
        <Button secondary disabled={locked || (decided && nothingSaved)} onClick={() => void put({})}>{t("zhOnly")}</Button>
        <Button disabled={locked || (decided && !changed)} onClick={() => void put(chosenBody(chosen))}>{busy ? t("saving") : t("languagesSave")}</Button>
      </div>
    </>}
  </section>;
}

/**
 * Whether a series read is a one-off's: the API's kind, which every series response carries
 * (SeriesSummary.kind in apps/api/app/video_automation/schemas.py, "series" by default). A response
 * without it (an API older than one-off series) counts as one only when it has a bible document.
 */
const isOneOff = (series: Series) => (series.kind ? series.kind === "one-off" : Boolean(series.docs?.some((doc) => doc.kind === "bible")));

/**
 * A one-off episode's series (docs/videos/DRAMA-FLOW.md, section 2): its story bible is the one
 * document, shown on the episode's page above the gates, with its discussion. The server knows a
 * one-off by its series' kind, not by its slug (the owner may pick one), so every drama episode's
 * series is read once. A long series or a brand story never has a bible document (its first
 * document is the setting book) and a series never changes its kind, so the first read that says
 * so is the last: those reads carry every episode's plan (about 1.2 MB for a hundred stories) and
 * would otherwise repeat every minute for nothing. A one-off keeps refreshing, so its bible and
 * thread follow the worker.
 */
function OneOffBible({ seriesSlug, canManage, onChanged }: { seriesSlug: string; canManage: boolean; onChanged: () => void }) {
  const t = useTranslations("admin.videoSeries");
  const [series, setSeries] = useState<Series | null>(null);
  // The slug last read as not a one-off; keyed by slug so another series on the same page reads again.
  const [notOneOff, setNotOneOff] = useState<string | null>(null);
  const settled = notOneOff === seriesSlug;
  const load = useCallback(() => {
    api<Series>(`/admin/video-automation/series/${seriesSlug}`).then((value) => {
      if (isOneOff(value)) { setSeries(value); return; }
      setSeries(null);
      setNotOneOff(seriesSlug);
    }).catch(() => setSeries(null));
  }, [seriesSlug]);
  // useRefresh's timer, but stopped for good once the series is known not to be a one-off.
  useEffect(() => {
    if (settled) return undefined;
    load();
    const timer = window.setInterval(load, REFRESH_MS);
    return () => window.clearInterval(timer);
  }, [load, settled]);
  if (settled || !series) return null;
  const bible = series.docs?.find((doc) => doc.kind === "bible");
  if (bible) return <DocPanel slug={seriesSlug} doc={bible} canManage={canManage} onChanged={() => { load(); onChanged(); }} />;
  // A one-off whose worker has not written the bible yet: say so instead of showing nothing.
  return <p className="text-sm text-[var(--muted)]">{t("bibleEmpty")}</p>;
}

/** The newest approved upload confirmation: the package the site sends to YouTube. */
const approvedPackage = (reviews: Review[] | undefined) => reviews?.find((review) => review.gate === "publish" && review.status === "approved") ?? null;

/**
 * How a video that is ready gets to YouTube: with the channel linked, the site sends the approved
 * package itself (apps/web/components/admin-video-youtube.tsx); without it, the owner uploads in
 * Studio and records the address here, as before.
 */
function SendToYoutube({ slug, confirmation, connection, sync, mp4Gone, onSent }: {
  slug: string; confirmation: Review | null; connection: YoutubeConnection | null; sync: ProjectSummary["youtube_sync"]; mp4Gone: boolean; onSent: () => void;
}) {
  if (syncRunning(sync)) return null;
  if (!connection?.linked) return <><YoutubeLinkHint /><UploadedForm slug={slug} onLinked={onSent} /></>;
  const canUpload = !mp4Gone && Boolean(confirmation?.files.some((file) => file.role === "final"));
  // Keyed by the package and the last run: the form fills itself from them once, when it mounts.
  return <YoutubePublishForm key={`${confirmation?.id ?? "none"}-${sync?.finished_at ?? "new"}`} slug={slug} review={confirmation} connection={connection} canUpload={canUpload} previous={sync?.request ?? null} onSent={onSent} />;
}

/**
 * What makes a video a Short, under its title (docs/videos/SHORTS.md): its content line and series,
 * where it stands, the slot it holds, and the video it was cut from, which opens from here.
 */
function ShortFacts({ project, onOpen }: { project: Project; onOpen: (slug: string) => void }) {
  const t = useTranslations("admin.videoShorts");
  const when = useWhen();
  if (!project.shorts_line) return null;
  const state = project.shorts_state ?? "making";
  return <div className="grid gap-2 text-sm" aria-label={t("detail.title")}>
    <p className="flex flex-wrap items-center gap-2">
      <AdminStatusPill status="inactive">{t(`lines.${project.shorts_line}`)}</AdminStatusPill>
      <AdminStatusPill status={stateTone[state]}>{t(`states.${state}`)}</AdminStatusPill>
      {project.shorts_series && <span className="text-[var(--muted)]">{t("library.series", { series: project.shorts_series })}</span>}
      <span className="text-[var(--muted)]">{project.slot_at ? t("library.slotAt", { time: when(project.slot_at) }) : t("library.noSlot")}</span>
    </p>
    {project.youtube_removed_at && <p><AdminStatusPill status="failed">{t("metrics.removed", { time: when(project.youtube_removed_at) })}</AdminStatusPill></p>}
    {project.source_slug && <p className="flex flex-wrap items-center gap-2">{t("detail.source")}<Button secondary onClick={() => onOpen(String(project.source_slug))}>{t("detail.openSource", { slug: project.source_slug })}</Button></p>}
  </div>;
}

function ProjectDetail({ slug, onBack, onOpen }: { slug: string; onBack: () => void; onOpen: (slug: string) => void }) {
  const t = useTranslations("admin.videoReviews");
  const ty = useTranslations("admin.videoYoutube");
  const when = useWhen();
  const manage = useAdminActionGuard("content.manage");
  const { connection } = useYoutubeConnection();
  const [project, setProject] = useState<Project | null>(null);
  const [error, setError] = useState("");
  const load = useCallback(() => {
    api<Project>(`/admin/videos/${slug}`).then((value) => { setProject(value); setError(""); }).catch((problem: unknown) => setError(problem instanceof Error ? problem.message : ""));
  }, [slug]);
  useRefresh(load);
  const live = project?.reviews.filter((review) => review.status === "pending") ?? [];
  const past = project?.reviews.filter((review) => review.status !== "pending") ?? [];
  const dropped = Boolean(project?.dropped_at);
  // A drama episode's screenplay has a thread on its series (docs/videos/DRAMA-FLOW.md, section 3);
  // the live card takes the owner's lines, an approved one in the history keeps them as a record.
  const discussion = (review: Review) => (review.gate === "script" && project?.series_slug && project.episode_number && (review.status === "pending" || review.status === "approved")
    ? <DiscussionThread seriesSlug={project.series_slug} subject={scriptSubject(project.episode_number)} canManage={manage.allowed && !dropped} readOnly={review.status !== "pending"} />
    : undefined);
  const retired = project ? mp4Retired(project) : false;
  const state = project ? publishState(project) : null;
  // A Short is nine by sixteen, and its languages are the Shorts settings', not this video's.
  const short = Boolean(project?.shorts_line);
  // The owner may upload the final cut as private as soon as the upload confirmation is approved;
  // only its scheduling waits for the languages (docs/videos/LANGUAGES.md).
  return <section className="mt-6 grid gap-5">
    <div><Button secondary onClick={onBack}><ArrowLeft aria-hidden size={18} />{t("back")}</Button></div>
    {error && <AdminErrorState title={t("loadError")} detail={error} retry={load} retryLabel={t("retry")} />}
    {project && <>
      <header className="grid gap-2">
        <div className="flex flex-wrap items-center gap-3"><h2 className="text-2xl font-bold">{project.title}</h2><PublishPill project={project} /></div>
        {state === "making" && <p className="text-sm text-[var(--muted)]">{t("scheduleWaits")}</p>}
        {project.series_slug && !project.compilation && <p className="text-sm text-[var(--muted)]">{t("episodeOf", { series: project.series_slug, number: project.episode_number ?? 0 })}</p>}
        {project.series_slug && project.compilation && <p className="text-sm text-[var(--muted)]">{t("compilationOf", { series: project.series_slug })}</p>}
        <ShortFacts project={project} onOpen={onOpen} />
        {!short && <CategoryPanel slug={slug} project={project} canManage={manage.allowed} onSaved={load} />}
        <CompilationDownload project={project} canManage={manage.allowed} />
        {project.youtube_video_id && <p className="text-sm">
          {t("youtube", { id: project.youtube_video_id })}
          {project.youtube_publish_at && ` · ${t("scheduledAt", { time: when(project.youtube_publish_at) })}`}
          <span className="block text-[var(--muted)]">{retired ? t("mp4Retired") : t("previewsGone")}</span>
        </p>}
        {project.dropped_at && <p role="status" className="rounded-xl bg-[var(--paper)] p-3 text-sm leading-6">
          <strong>{t("droppedAt", { time: when(project.dropped_at) })}</strong>
          {project.dropped_note && <span className="block whitespace-pre-wrap">{project.dropped_note}</span>}
        </p>}
      </header>
      {project.series_slug && <OneOffBible seriesSlug={project.series_slug} canManage={manage.allowed && !dropped} onChanged={load} />}
      {project.checklist.length > 0 && <section aria-label={t("checklist")} className="rounded-2xl border border-[var(--line)] bg-[var(--surface)] p-4">
        <p className="font-bold">{t("checklist")}</p>
        <ul className="mt-2 grid gap-1 text-sm sm:grid-cols-2">{project.checklist.map((item) => <li key={item.key} className="flex items-center gap-2">{item.done ? <CheckCircle2 aria-hidden size={16} className="text-[var(--teal)]" /> : <Circle aria-hidden size={16} className="text-[var(--muted)]" />}<span className={item.done ? "" : "text-[var(--muted)]"}>{item.label}</span></li>)}</ul>
      </section>}
      <RetryVideo project={project} canManage={manage.allowed} onRequested={load} />
      <AdminVideoRenewal key={project.slug} project={project} canManage={manage.allowed} onSubmitted={load} />
      {project.youtube_sync && <YoutubeSyncPanel slug={slug} sync={project.youtube_sync} canManage={manage.allowed && !dropped} onChange={load} />}
      {readyToUpload(project) && manage.allowed && <SendToYoutube slug={slug} confirmation={approvedPackage(project.reviews)} connection={connection} sync={project.youtube_sync} mp4Gone={retired} onSent={load} />}
      {project.youtube_video_id && !dropped && manage.allowed && connection?.linked && !syncRunning(project.youtube_sync) && <details className="rounded-2xl border border-[var(--line)] p-4">
        <summary className="cursor-pointer font-bold">{ty("resendTitle")}</summary>
        <p className="mt-2 text-sm leading-6 text-[var(--muted)]">{ty("resendHelp")}</p>
        <div className="mt-3"><YoutubePublishForm key={project.youtube_sync?.finished_at ?? "resend"} slug={slug} review={approvedPackage(project.reviews)} connection={connection} canUpload={false} videoId={project.youtube_video_id} previous={project.youtube_sync?.request ?? null} onSent={load} /></div>
      </details>}
      {!dropped && !short && <LanguagePanel slug={slug} project={project} canManage={manage.allowed} onSaved={load} />}
      {live.length === 0 && !dropped && <p className="text-[var(--muted)]">{t("noPending")}</p>}
      {live.map((review) => <ReviewCard key={review.id} slug={slug} review={review} canManage={manage.allowed && !dropped} onDecided={load} mp4Gone={retired} discussion={discussion(review)} vertical={short} />)}
      {past.length > 0 && <details className="grid gap-4" open={readyToUpload(project)}><summary className="cursor-pointer font-bold">{t("history")}</summary>
        <div className="mt-4 grid gap-4">{past.map((review) => <ReviewCard key={review.id} slug={slug} review={review} canManage={false} onDecided={load} mp4Gone={retired} discussion={discussion(review)} vertical={short} />)}</div>
      </details>}
      {manage.allowed && !dropped && !project.youtube_video_id && <DropVideo slug={slug} onDropped={load} />}
    </>}
  </section>;
}

/** One row of the list: the title, what state it is in, and where the worker is. */
function ProjectItem({ project, onOpen }: { project: ProjectSummary; onOpen: (slug: string) => void }) {
  const t = useTranslations("admin.videoReviews");
  const ty = useTranslations("admin.videoYoutube");
  const when = useWhen();
  return <li>
    <button type="button" onClick={() => onOpen(project.slug)} className="grid w-full gap-2 rounded-[1.5rem] border border-[var(--line)] bg-[var(--surface)] p-5 text-left shadow-[var(--shadow-sm)] hover:border-[var(--teal)]">
      <span className="flex flex-wrap items-center gap-3"><Clapperboard aria-hidden size={20} className="text-[var(--teal)]" /><span className="text-lg font-bold">{project.title}</span>
        {project.dropped_at
          ? <AdminStatusPill status="inactive">{t("dropped")}</AdminStatusPill>
          : <AdminStatusPill status={project.pending ? "pending" : "inactive"}>{project.pending ? t("pending", { count: project.pending }) : t("noPendingShort")}</AdminStatusPill>}
        {!project.dropped_at && isBlocked(project) && <AdminStatusPill status="failed">{t("stuck")}</AdminStatusPill>}
        <PublishPill project={project} />
        {syncRunning(project.youtube_sync) && <AdminStatusPill status="running">{ty("sendingPill")}</AdminStatusPill>}
        {youtubeSyncStuck(project.youtube_sync) && <AdminStatusPill status="failed">{ty("stuckPill")}</AdminStatusPill>}
      </span>
      <span className="text-sm text-[var(--muted)]">{t("progress", { done: project.checklist.filter((item) => item.done).length, total: project.checklist.length })} · {t("lastSynced", { time: when(project.last_synced_at) })}</span>
      {project.youtube_video_id && <span className="text-sm text-[var(--muted)]">{t("youtube", { id: project.youtube_video_id })}{project.youtube_publish_at && ` · ${t("scheduledAt", { time: when(project.youtube_publish_at) })}`}</span>}
      {project.stage && !project.youtube_video_id && !project.dropped_at && <span className="text-sm text-[var(--muted)]">{t("currentStep", { step: project.checklist.find((item) => !item.done)?.label ?? project.stage })}</span>}
    </button>
  </li>;
}

/**
 * A video whose upload confirmation is approved and that is not on YouTube yet: its package,
 * read from the approved publish review, and the form the owner fills in after uploading.
 */
function ReadyCard({ project, canManage, connection, onOpen, onLinked }: { project: ProjectSummary; canManage: boolean; connection: YoutubeConnection | null; onOpen: (slug: string) => void; onLinked: () => void }) {
  const t = useTranslations("admin.videoReviews");
  const [detail, setDetail] = useState<Project | null>(null);
  const [error, setError] = useState("");
  useEffect(() => {
    let current = true;
    api<Project>(`/admin/videos/${project.slug}`)
      .then((value) => { if (current) { setDetail(value); setError(""); } })
      .catch((problem: unknown) => { if (current) setError(problem instanceof Error ? problem.message : ""); });
    return () => { current = false; };
  }, [project.slug, project.last_synced_at]);
  // Reviews come newest first, so the first approved confirmation is the current package.
  const confirmation = approvedPackage(detail?.reviews);
  return <li>
    <article className="grid gap-4 rounded-[1.5rem] border border-[var(--teal)] bg-[var(--surface)] p-5 shadow-[var(--shadow-sm)]" aria-label={project.title}>
      <header className="flex flex-wrap items-center gap-3">
        <Upload aria-hidden size={20} className="text-[var(--teal)]" />
        <h3 className="text-lg font-bold">{project.title}</h3>
        <PublishPill project={project} />
        <Button secondary className="ml-auto" onClick={() => onOpen(project.slug)}>{t("openVideo", { slug: project.slug })}</Button>
      </header>
      {error && <p role="alert" className="text-sm text-red-800">{error}</p>}
      {!detail && !error && <p className="text-sm text-[var(--muted)]">{t("readyLoading")}</p>}
      {confirmation && <UploadPackage slug={project.slug} review={confirmation} />}
      <CompilationDownload project={project} canManage={canManage} />
      {project.youtube_sync && <YoutubeSyncPanel slug={project.slug} sync={project.youtube_sync} canManage={canManage} onChange={onLinked} />}
      {canManage && detail && <SendToYoutube slug={project.slug} confirmation={confirmation} connection={connection} sync={project.youtube_sync} mp4Gone={false} onSent={onLinked} />}
    </article>
  </li>;
}

function Group({ title, children }: { title: string; children: ReactNode }) {
  return <section aria-label={title} className="grid gap-3">
    <h2 className="text-xs font-black tracking-[.16em] text-[var(--teal)]">{title}</h2>
    <ul className="grid gap-4">{children}</ul>
  </section>;
}

/**
 * The tutorials (slides videos): dramas and Shorts live on their own tabs, and the list is asked
 * for without the Shorts, which would otherwise crowd the tutorials out of it. What waits for the owner
 * comes first (a decision, a stopped video, a finished cut whose languages are not chosen), then what is
 * ready to upload (docs/videos/HANDS-OFF.md, docs/videos/LANGUAGES.md); under the two, every tutorial
 * is in the catalog, one line each, with the category and state filters, a search and pages
 * (VideoBrowser). A video that needs the owner is in both: the group is the reminder, the catalog the
 * record.
 */
function ProjectList({ onOpen }: { onOpen: (slug: string) => void }) {
  const t = useTranslations("admin.videoReviews");
  const manage = useAdminActionGuard("content.manage");
  const { connection } = useYoutubeConnection();
  const [projects, setProjects] = useState<ProjectSummary[] | null>(null);
  const [error, setError] = useState("");
  const load = useCallback(() => {
    api<ProjectSummary[]>("/admin/videos?shorts=exclude").then((value) => { setProjects(value.filter((project) => project.format !== "drama" && !project.shorts_line)); setError(""); }).catch((problem: unknown) => setError(problem instanceof Error ? problem.message : ""));
  }, []);
  useRefresh(load);
  // A video sent or linked from its card changes its line in the catalog too: both read again.
  const [revision, setRevision] = useState(0);
  const changed = useCallback(() => { load(); setRevision((value) => value + 1); }, [load]);
  const groups = useMemo(() => {
    const listed = projects ?? [];
    return { needs: listed.filter(needsOwner), ready: listed.filter((project) => !needsOwner(project) && readyToUpload(project)) };
  }, [projects]);
  return <div className="grid gap-6" aria-label={t("listTitle")}>
    {error && <AdminErrorState title={t("loadError")} detail={error} retry={load} retryLabel={t("retry")} />}
    {groups.needs.length > 0 && <Group title={t("needsYou")}>{groups.needs.map((project) => <ProjectItem key={project.slug} project={project} onOpen={onOpen} />)}</Group>}
    {groups.ready.length > 0 && <Group title={t("readyToUpload")}>{groups.ready.map((project) => <ReadyCard key={project.slug} project={project} canManage={manage.allowed} connection={connection} onOpen={onOpen} onLinked={changed} />)}</Group>}
    <VideoBrowser onOpen={onOpen} revision={revision} />
  </div>;
}

const TABS = ["reviews", "drama", "shorts", "settings"] as const;

export function AdminVideoReviews() {
  const t = useTranslations("admin.videoReviews");
  const [slug, setSlug] = useAdminQueryValue("video", "", (value) => SLUG.test(value));
  const [tab, setTab] = useAdminQueryState("tab", TABS, "reviews");
  if (slug) return <ProjectDetail slug={slug} onBack={() => setSlug("")} onOpen={setSlug} />;
  return <div className="mt-6">
    <Tabs value={tab} onChange={(value) => setTab(value as (typeof TABS)[number])} label={t("tabsLabel")}
      items={[{ value: "reviews", label: t("tabReviews") }, { value: "drama", label: t("tabDrama") }, { value: "shorts", label: t("tabShorts") }, { value: "settings", label: t("tabSettings") }]}>
      {tab === "reviews" && <ProjectList onOpen={setSlug} />}
      {tab === "drama" && <AdminVideoSeries onOpenVideo={setSlug} />}
      {tab === "shorts" && <AdminVideoShorts onOpenVideo={setSlug} />}
      {tab === "settings" && <><div className="mt-6"><YoutubeChannelCard /></div><AdminVideoSettings /></>}
    </Tabs>
  </div>;
}
