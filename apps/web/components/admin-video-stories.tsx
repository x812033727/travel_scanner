"use client";

import { ArrowLeft, BookOpenText, ExternalLink, Upload } from "lucide-react";
import { useLocale, useTranslations } from "next-intl";
import { type ChangeEvent, useCallback, useEffect, useMemo, useState } from "react";
import { useAdminActionGuard } from "@/components/admin-action-guard";
import { useAdminOperations } from "@/components/admin-operations-provider";
import { AdminErrorState, AdminStatusPill } from "@/components/admin-ui";
import {
  control, list, type Project, type ProjectSummary, publishState, record, REFRESH_MS, text, UploadedForm, UploadPackage, useRefresh,
} from "@/components/admin-video-review-card";
import type { Series } from "@/components/admin-video-series";
import { syncRunning, type YoutubeConnection, useYoutubeConnection, YoutubeLinkHint, YoutubePublishForm, YoutubeSyncPanel } from "@/components/admin-video-youtube";
import { Button } from "@/components/community/ui";
import { adminUsersCopy } from "@/lib/admin-users-copy";
import { adminNavigate, useAdminQueryValue } from "@/lib/admin-workspace-navigation";
import { ApiError, api, apiProblemMessage } from "@/lib/api";
import { activeLocale } from "@/lib/locale-format";

// The brand stories (docs/videos/STORY.md): a drama series of kind "story" whose episodes are the
// planned backlog, one story each, imported from stories.json and made two a day by the worker. An
// episode's beats are the story's plan (its id, category, region, publishing slot, the question,
// six chapters, the facts to verify, the sources and the fact checker's caveats). The drama tab
// shows the story series apart (AdminVideoStorySeries), and a story series opens on its own page
// (StorySeriesPage): what holds the next story back, the daily count, pause, the stories ready to
// upload with their next free slot, the list of every story, and the import. The changes ask for
// content.manage, as the API's series endpoints do; a reader sees everything and changes nothing.
type SeriesEpisode = Series["episodes"][number];
// Where a story series stands against its limits, from the server (apps/api/app/video_automation
// series.py story_quota, the same function that decides the worker's next job). day is the
// Asia/Taipei calendar day started_today counts, as the server sees it.
export type StoryQuota = {
  day: string; started_today: number; episodes_per_day: number | null; in_flight: number; max_in_flight: number;
  started_this_month: number; episodes_per_month: number; awaiting_upload: number; upload_buffer: number; ready: number;
  hold?: string | null; hold_detail?: string | null;
};
// The story columns of a series; the other kinds leave them out or null.
export type StorySeries = Series & { episodes_per_day?: number | null; image_model?: string | null; quota?: StoryQuota | null };
type StorySummary = Omit<StorySeries, "docs" | "episodes">;
// StoryImportReport.as_dict() (apps/api/app/video_automation/stories.py): the answer to a dry run and
// to an import, and, beside the problem fields of a 422, the report of a file that was refused.
export type StoryImportReport = {
  series: string; dry_run: boolean; accepted: boolean; written: boolean; series_exists: boolean; series_created: boolean;
  stories_in_file: number; stories_imported: number; create: number; update: number; leave_alone: number; refuse: number;
  rows: Record<ImportRow, string[]>; series_differs: Record<string, { file?: unknown; series?: unknown }>; problems: string[]; notes: string[];
};

const IMPORT_ROWS = ["create", "update", "renumbered", "unchanged", "started", "refused"] as const;
type ImportRow = (typeof IMPORT_ROWS)[number];
// What a plan may say (tools/video/story-plans/plan.mjs and apps/api/app/video_automation/stories.py).
const CATEGORIES = ["everyday", "asia-brand", "tech"] as const;
const REGIONS = ["global", "jp", "kr", "tw"] as const;
const CHAPTER_KEYS = ["hook", "origin", "idea", "engine", "turn", "now"] as const;
const SOURCE_KINDS = ["official", "court", "academic", "archive", "reference", "news", "book"] as const;
const STORY_ID = /^[ABKTC][0-9]{2}$/;
// The series slug the import's path takes (SERIES_SLUG_PATTERN in the API's schemas).
const SLUG = /^[a-z0-9][a-z0-9-]{1,39}$/;
// Where a story is, from its episode and its video: not started, in the making, ready to upload,
// scheduled or public on YouTube, finished without a video to show, skipped, or its video dropped.
const STATES = ["waiting", "making", "ready", "scheduled", "published", "done", "skipped", "dropped"] as const;
type StoryState = (typeof STATES)[number];
const stateTone: Record<StoryState, string> = { waiting: "inactive", making: "running", ready: "active", scheduled: "queued", published: "ok", done: "ok", skipped: "inactive", dropped: "failed" };
const seriesTone: Record<string, string> = { setting: "pending", outline: "pending", active: "active", paused: "inactive", finished: "inactive" };
const HOLDS = ["per_day", "in_flight", "per_month", "upload_buffer", "none_ready"] as const;
// The daily count a story series takes (STORY_MAX_PER_DAY); empty lifts the limit.
const PER_DAY_CHOICES = Array.from({ length: 12 }, (_, index) => index + 1);
// The import request's cap (STORY_IMPORT_MAX_BYTES in apps/api/app/video_automation/admin_api.py).
// It is under the 5 MiB the site's relay and the API take, so a bigger file is refused here, by
// name, before it travels; a hundred stories are about 1.2 MB as a request.
export const STORY_IMPORT_MAX_BYTES = 4 * 1024 * 1024;
// The publishing slots (docs/videos/STORY.md, the daily quota and schedule): noon and eight in the
// evening, Taipei time. Taiwan keeps UTC+8 all year, so a slot is a fixed offset from UTC midnight.
const SLOT_HOURS: Record<string, number> = { "12:00": 12, "20:00": 20 };
const TAIPEI_OFFSET_MS = 8 * 3_600_000;
const HOUR_MS = 3_600_000;
const DAY_MS = 24 * HOUR_MS;
// How far ahead a suggested slot lies at least: the site sends a scheduled upload no later than
// five minutes before its time (MIN_LEAD in apps/api/app/video_youtube/sync.py), and the owner takes
// a while to upload in Studio. A video scheduled within an hour of a slot holds it.
const SLOT_LEAD_MS = HOUR_MS;
const SLOT_TOLERANCE_MS = HOUR_MS;
// The query keys of this page, cleared when the owner goes back to the list.
const QUERY_KEYS = ["story", "story_category", "story_state"] as const;
const isCategory = (value: string) => (CATEGORIES as readonly string[]).includes(value);
const isState = (value: string) => (STATES as readonly string[]).includes(value);
const isStoryId = (value: string) => STORY_ID.test(value);
// The admin roles by the key the members page labels them with (lib/admin-users-copy.ts), as the
// settings tab's permission notice names them.
const ROLE_COPY_KEYS: Record<string, string> = {
  viewer: "rolesViewer", support: "rolesSupport", content: "rolesContent", operations: "rolesOperations",
  database_operator: "rolesDatabase", deployer: "rolesDeployer", owner: "rolesOwner",
};

const message = (problem: unknown) => (problem instanceof Error ? problem.message : "");
const beatsOf = (episode: SeriesEpisode) => record(episode.beats);
const storyId = (episode: SeriesEpisode) => text(beatsOf(episode).id);

/** The plan's publishing slot, day N of the schedule at 12:00 or 20:00; either part may be missing. */
function publishOf(episode: SeriesEpisode): { day: number | null; slot: string } {
  const publish = record(beatsOf(episode).publish);
  const day = typeof publish.day === "number" && Number.isInteger(publish.day) ? publish.day : null;
  const slot = text(publish.slot);
  return { day, slot: Object.hasOwn(SLOT_HOURS, slot) ? slot : "" };
}

/** Where a story is: its episode's status, and once it has a video, where that video is on its way to YouTube. */
export function storyState(episode: SeriesEpisode, now: number): StoryState {
  if (episode.status === "skipped") return "skipped";
  const video = episode.video;
  if (video?.dropped_at) return "dropped";
  const publish = video ? publishState(video, now) : null;
  if (publish === "ready" || publish === "scheduled" || publish === "published") return publish;
  if (episode.status === "started" || (episode.status === "done" && video)) return "making";
  return episode.status === "done" ? "done" : "waiting";
}

/**
 * The first publishing slot from now on at this time of day (12:00 or 20:00 Taipei time; either one
 * when the plan names none) that is at least SLOT_LEAD_MS ahead and that no time in ``taken`` holds.
 */
export function nextFreeSlot(slot: string, taken: readonly number[], now: number): number {
  const hours = Object.hasOwn(SLOT_HOURS, slot) ? [SLOT_HOURS[slot]] : Object.values(SLOT_HOURS);
  const midnight = Math.floor((now + TAIPEI_OFFSET_MS) / DAY_MS) * DAY_MS - TAIPEI_OFFSET_MS;
  const free = (at: number) => at >= now + SLOT_LEAD_MS && !taken.some((other) => Math.abs(other - at) < SLOT_TOLERANCE_MS);
  // Every taken time holds at most one slot, so a free one is found within that many days and one more.
  for (let day = 0; day <= taken.length + 1; day += 1) {
    for (const hour of hours) {
      const at = midnight + day * DAY_MS + hour * HOUR_MS;
      if (free(at)) return at;
    }
  }
  return midnight + (taken.length + 2) * DAY_MS + hours[0] * HOUR_MS;
}

/**
 * The slot each story ready to upload is offered, by episode number: in the plan's order (its day,
 * then noon before evening), each story takes the next free slot at its own time of day, after the
 * times the series' videos are scheduled at (or are being sent to YouTube for) and the slots the
 * stories before it took, so no two cards offer the same one.
 */
export function planSlots(episodes: SeriesEpisode[], now: number): Map<number, number> {
  const taken: number[] = [];
  for (const episode of episodes) {
    const video = episode.video;
    if (!video || video.dropped_at) continue;
    const request = video.youtube_sync?.request;
    for (const value of [video.youtube_publish_at, request?.visibility === "scheduled" ? request.publish_at : null]) {
      const at = value ? Date.parse(value) : Number.NaN;
      if (Number.isFinite(at)) taken.push(at);
    }
  }
  const rank = (episode: SeriesEpisode) => {
    const { day, slot } = publishOf(episode);
    return [day ?? Number.MAX_SAFE_INTEGER, SLOT_HOURS[slot] ?? 24, episode.number];
  };
  const ready = episodes.filter((episode) => storyState(episode, now) === "ready")
    .sort((a, b) => {
      const [left, right] = [rank(a), rank(b)];
      return left[0] - right[0] || left[1] - right[1] || left[2] - right[2];
    });
  const slots = new Map<number, number>();
  for (const episode of ready) {
    const at = nextFreeSlot(publishOf(episode).slot, taken, now);
    slots.set(episode.number, at);
    taken.push(at);
  }
  return slots;
}

/** A datetime-local value for an instant: the viewer's wall clock, as the upload forms read it back. */
function wallClock(at: number): string {
  const value = new Date(at);
  const pad = (part: number) => String(part).padStart(2, "0");
  return `${value.getFullYear()}-${pad(value.getMonth() + 1)}-${pad(value.getDate())}T${pad(value.getHours())}:${pad(value.getMinutes())}`;
}

/** The clock, moved on once a minute: a story's state and its next free slot depend on it. */
function useNow(): number {
  const [now, setNow] = useState(() => Date.now());
  useEffect(() => {
    const timer = window.setInterval(() => setNow(Date.now()), REFRESH_MS);
    return () => window.clearInterval(timer);
  }, []);
  return now;
}

/** The server's Taipei day (YYYY-MM-DD) as the locale writes a month and day; nothing is converted. */
function useTaipeiDay() {
  const locale = useLocale();
  const format = useMemo(() => new Intl.DateTimeFormat(locale, { month: "numeric", day: "numeric", timeZone: "UTC" }), [locale]);
  return (day: string) => {
    const parts = /^(\d{4})-(\d{2})-(\d{2})$/.exec(day);
    return parts ? format.format(Date.UTC(Number(parts[1]), Number(parts[2]) - 1, Number(parts[3]))) : day;
  };
}

/** A publishing slot in Taipei time, with its weekday, whatever the viewer's own time zone. */
function useSlotTime() {
  const locale = useLocale();
  const format = useMemo(() => new Intl.DateTimeFormat(locale, { timeZone: "Asia/Taipei", month: "numeric", day: "numeric", weekday: "short", hour: "2-digit", minute: "2-digit", hourCycle: "h23" }), [locale]);
  return (at: number) => format.format(at);
}

/** Why no story starts now, in the owner's words; the server's own sentence for a reason this page does not know. */
function useHoldReason() {
  const t = useTranslations("admin.videoStories");
  const taipeiDay = useTaipeiDay();
  return (quota: StoryQuota, status: string): string => {
    const hold = quota.hold ?? "";
    if (!hold) return "";
    if (hold === "not_active") return status === "paused" ? t("holds.paused") : t("holds.notActive");
    if (!(HOLDS as readonly string[]).includes(hold)) return quota.hold_detail || hold;
    return t(`holds.${hold}`, {
      day: taipeiDay(quota.day), started: quota.started_today, perDay: quota.episodes_per_day ?? 0, inFlight: quota.in_flight, maxInFlight: quota.max_in_flight,
      month: quota.started_this_month, perMonth: quota.episodes_per_month, awaiting: quota.awaiting_upload, buffer: quota.upload_buffer,
    });
  };
}

/** Today's count against the daily limit, as the server counts the Taipei day. */
function useTodayText() {
  const t = useTranslations("admin.videoStories");
  const taipeiDay = useTaipeiDay();
  return (quota: StoryQuota) => (quota.episodes_per_day == null
    ? t("quota.todayNoLimit", { day: taipeiDay(quota.day), count: quota.started_today })
    : t("quota.today", { day: taipeiDay(quota.day), count: quota.started_today, limit: quota.episodes_per_day }));
}

/** An admin role's name as the members page shows it, where the owner grants roles. */
function useRoleLabel() {
  const locale = useLocale();
  const copy = adminUsersCopy(locale) as unknown as Record<string, string>;
  return (role: string) => copy[ROLE_COPY_KEYS[role] ?? ""] || role;
}

/** Why this account can look but not change anything here, and which roles can. */
function StoryPermissionNote() {
  const t = useTranslations("admin.videoStories");
  const locale = useLocale();
  const label = useRoleLabel();
  const operations = useAdminOperations();
  if (!operations) return null;
  const roles = operations.bootstrap.admin_roles.map(label);
  return <aside role="note" className="grid gap-1 rounded-xl border border-[var(--line)] bg-[var(--paper)] p-4 text-sm leading-6">
    <p className="font-semibold">{t("permission.title")}</p>
    <p>{t("permission.needs", { content: label("content"), owner: label("owner"), capability: "content.manage" })}</p>
    <p>{roles.length ? t("permission.roles", { roles: new Intl.ListFormat(locale, { type: "conjunction" }).format(roles) }) : t("permission.noRoles")}</p>
  </aside>;
}

/** Started today against the daily limit, in flight, cleared for upload against the buffer, and why no story starts. */
function StoryQuotaPanel({ quota, status }: { quota: StoryQuota; status: string }) {
  const t = useTranslations("admin.videoStories");
  const today = useTodayText();
  const holdReason = useHoldReason();
  const reason = holdReason(quota, status);
  const figures = [
    [t("quota.todayLabel"), today(quota)],
    [t("quota.inFlightLabel"), t("quota.of", { count: quota.in_flight, limit: quota.max_in_flight })],
    [t("quota.awaitingLabel"), t("quota.of", { count: quota.awaiting_upload, limit: quota.upload_buffer })],
    [t("quota.monthLabel"), t("quota.of", { count: quota.started_this_month, limit: quota.episodes_per_month })],
    [t("quota.readyLabel"), t("quota.count", { count: quota.ready })],
  ];
  return <section aria-label={t("quota.title")} className="grid gap-3 rounded-2xl border border-[var(--line)] bg-[var(--surface)] p-4">
    <p className="font-bold">{t("quota.title")}</p>
    <dl className="grid gap-3 text-sm sm:grid-cols-2 lg:grid-cols-5">{figures.map(([label, value]) => <div key={label} className="grid gap-0.5">
      <dt className="text-[var(--muted)]">{label}</dt><dd className="font-semibold">{value}</dd>
    </div>)}</dl>
    {reason
      ? <p role="status" className="rounded-xl bg-amber-50 p-3 text-sm leading-6 text-amber-900"><strong>{t("quota.holdTitle")}</strong> {reason}</p>
      : <p role="status" className="text-sm text-[var(--muted)]">{t("quota.go")}</p>}
  </section>;
}

/** Pause or resume the series, and how many stories may start a day. */
function StoryControls({ series, onChanged }: { series: StorySeries; onChanged: () => void }) {
  const t = useTranslations("admin.videoStories");
  const ts = useTranslations("admin.videoSeries");
  const [busy, setBusy] = useState("");
  const [error, setError] = useState("");
  // The owner's pick, kept only while the server still has the value it was picked over: a save,
  // or another admin's, brings the select back to what the server says.
  const current = series.episodes_per_day == null ? "" : String(series.episodes_per_day);
  const [pick, setPick] = useState<{ over: string; value: string } | null>(null);
  const perDay = pick && pick.over === current ? pick.value : current;
  const patch = async (what: string, body: Record<string, unknown>) => {
    setBusy(what);
    setError("");
    try {
      await api(`/admin/video-automation/series/${series.slug}`, { method: "PATCH", body: JSON.stringify(body) });
      onChanged();
    } catch (problem) {
      setError(ts("actionError", { message: message(problem) }));
    } finally {
      setBusy("");
    }
  };
  return <div className="grid gap-3">
    <div className="flex flex-wrap items-end gap-3">
      {series.status === "active" && <Button secondary disabled={busy === "status"} onClick={() => void patch("status", { status: "paused" })}>{ts("pause")}</Button>}
      {series.status === "paused" && <Button secondary disabled={busy === "status"} onClick={() => void patch("status", { status: "active" })}>{ts("resume")}</Button>}
      <form className="flex flex-wrap items-end gap-3" aria-label={t("perDay.label")} onSubmit={(event) => { event.preventDefault(); void patch("per-day", { episodes_per_day: perDay ? Number(perDay) : null }); }}>
        <label className="grid gap-2 text-sm font-semibold">{t("perDay.label")}
          <select className={control} value={perDay} disabled={busy === "per-day"} onChange={(event) => setPick({ over: current, value: event.target.value })}>
            <option value="">{t("perDay.none")}</option>
            {PER_DAY_CHOICES.map((count) => <option key={count} value={String(count)}>{t("perDay.option", { count })}</option>)}
          </select>
        </label>
        <Button type="submit" secondary disabled={busy === "per-day" || perDay === current}>{busy === "per-day" ? ts("saving") : t("perDay.save")}</Button>
      </form>
    </div>
    <p className="text-sm leading-6 text-[var(--muted)]">{t("perDay.help")}</p>
    {error && <p role="alert" className="text-sm text-red-800">{error}</p>}
  </div>;
}

/** Everything a story's plan says, read-only: what the video will say before it is made. */
function StoryPlan({ episode }: { episode: SeriesEpisode }) {
  const t = useTranslations("admin.videoStories");
  const beats = beatsOf(episode);
  const chapters = list(beats.chapters).map(record);
  const facts = list(beats.must_verify).map(record);
  const sources = list(beats.sources).map(record);
  const caveats = text(beats.caveats);
  const chapterLabel = (key: string) => ((CHAPTER_KEYS as readonly string[]).includes(key) ? t(`chapters.${key}`) : key);
  const kindLabel = (kind: string) => ((SOURCE_KINDS as readonly string[]).includes(kind) ? t(`sourceKinds.${kind}`) : kind);
  const id = storyId(episode) || String(episode.number);
  return <div role="region" aria-label={t("plan.title", { id })} className="mt-3 grid gap-4 border-t border-[var(--line)] pt-3 text-sm leading-6">
    {episode.logline && <p>{episode.logline}</p>}
    <div><p className="font-bold">{t("plan.question")}</p><p>{text(beats.question)}</p></div>
    {chapters.length > 0 && <div><p className="font-bold">{t("plan.chapters")}</p>
      <ol className="mt-1 grid gap-2">{chapters.map((chapter, index) => <li key={index}><span className="block font-semibold">{chapterLabel(text(chapter.key))}</span>{text(chapter.point)}</li>)}</ol>
    </div>}
    {text(beats.takeaway) && <div><p className="font-bold">{t("plan.takeaway")}</p><p>{text(beats.takeaway)}</p></div>}
    {facts.length > 0 && <div><p className="font-bold">{t("plan.facts", { count: facts.length })}</p>
      <ol className="mt-1 grid list-decimal gap-2 pl-5">{facts.map((fact, index) => {
        const cited = list(fact.sources).filter((each): each is number => typeof each === "number").map((each) => each + 1);
        return <li key={index}>
          {text(fact.claim)}
          <span className="mt-1 flex flex-wrap items-center gap-2 text-xs text-[var(--muted)]">
            {cited.length > 0 && <span>{t("plan.cites", { sources: cited.join(", ") })}</span>}
            {fact.core === true && <AdminStatusPill status="active">{t("plan.core")}</AdminStatusPill>}
            {fact.attributed === true && <AdminStatusPill status="pending">{t("plan.attributed")}</AdminStatusPill>}
            {fact.reviewer_only === true && <AdminStatusPill status="inactive">{t("plan.reviewerOnly")}</AdminStatusPill>}
          </span>
        </li>;
      })}</ol>
    </div>}
    {sources.length > 0 && <div><p className="font-bold">{t("plan.sources", { count: sources.length })}</p>
      <ol className="mt-1 grid list-decimal gap-2 pl-5">{sources.map((source, index) => {
        const url = text(source.url);
        const name = text(source.publisher) || url;
        return <li key={index} className="break-words">
          {url.startsWith("https://") ? <a href={url} target="_blank" rel="noreferrer" className="font-semibold text-[var(--teal)] underline">{name}</a> : <span className="font-semibold">{name}</span>}
          <span className="text-xs text-[var(--muted)]"> · {kindLabel(text(source.kind))}{text(source.checked) ? ` · ${t("plan.checked", { date: text(source.checked) })}` : ""}</span>
          {text(source.supports) && <span className="block text-[var(--muted)]">{text(source.supports)}</span>}
        </li>;
      })}</ol>
    </div>}
    {caveats && <div><p className="font-bold">{t("plan.caveats")}</p><p className="whitespace-pre-wrap">{caveats}</p></div>}
  </div>;
}

/**
 * The list of stories: each one's id, title, category and region, its slot in the plan, where it
 * is and its video once there is one; filtered by category and by where they are (both in the
 * URL), with the plan of one story opened under its row. A story not started yet may be skipped
 * and a skipped one that never started brought back.
 */
function StoryList({ series, now, canManage, onOpenVideo, onChanged }: { series: StorySeries; now: number; canManage: boolean; onOpenVideo: (slug: string) => void; onChanged: () => void }) {
  const t = useTranslations("admin.videoStories");
  const ts = useTranslations("admin.videoSeries");
  const [category, setCategory] = useAdminQueryValue("story_category", "", isCategory);
  const [state, setState] = useAdminQueryValue("story_state", "", isState);
  const [opened, setOpened] = useAdminQueryValue("story", "", isStoryId);
  const [busy, setBusy] = useState("");
  const [error, setError] = useState("");
  const rows = useMemo(() => series.episodes.map((episode) => ({ episode, id: storyId(episode), category: text(beatsOf(episode).category), state: storyState(episode, now) })), [series.episodes, now]);
  const byCategory = rows.filter((row) => !category || row.category === category);
  const shown = byCategory.filter((row) => !state || row.state === state);
  const count = (items: typeof rows, pick: (row: (typeof rows)[number]) => boolean) => items.filter(pick).length;
  const act = async (what: string, episode: SeriesEpisode) => {
    const id = storyId(episode) || String(episode.number);
    if (what === "skip" && !window.confirm(t("list.skipConfirm", { id, title: episode.title }))) return;
    setBusy(`${what}-${episode.number}`);
    setError("");
    try {
      await api(`/admin/video-automation/series/${series.slug}/episodes/${episode.number}/${what}`, { method: "POST" });
      onChanged();
    } catch (problem) {
      setError(ts("actionError", { message: message(problem) }));
    } finally {
      setBusy("");
    }
  };
  const label = (key: string, known: readonly string[], prefix: string) => (known.includes(key) ? t(`${prefix}.${key}`) : key);
  return <section aria-label={t("list.title")} className="grid gap-3">
    <h3 className="text-lg font-bold">{t("list.title")}</h3>
    <div className="grid gap-3 sm:grid-cols-2 md:max-w-2xl">
      <label className="grid gap-2 text-sm font-semibold">{t("list.category")}
        <select className={control} value={category} onChange={(event) => setCategory(event.target.value, true)}>
          <option value="">{t("list.all", { count: rows.length })}</option>
          {CATEGORIES.map((each) => <option key={each} value={each}>{t("list.option", { label: t(`categories.${each}`), count: count(rows, (row) => row.category === each) })}</option>)}
        </select>
      </label>
      <label className="grid gap-2 text-sm font-semibold">{t("list.state")}
        <select className={control} value={state} onChange={(event) => setState(event.target.value, true)}>
          <option value="">{t("list.all", { count: byCategory.length })}</option>
          {STATES.map((each) => <option key={each} value={each}>{t("list.option", { label: t(`states.${each}`), count: count(byCategory, (row) => row.state === each) })}</option>)}
        </select>
      </label>
    </div>
    {error && <p role="alert" className="text-sm text-red-800">{error}</p>}
    {rows.length === 0 && <p className="text-sm text-[var(--muted)]">{t("list.none")}</p>}
    {rows.length > 0 && shown.length === 0 && <p className="text-sm text-[var(--muted)]">{t("list.noMatch")}</p>}
    {shown.length > 0 && <ul className="grid gap-2" aria-label={t("list.title")}>{shown.map(({ episode, id, category: kind, state: where }) => {
      const { day, slot } = publishOf(episode);
      const video = episode.video;
      const open = Boolean(id) && opened === id;
      const facts = [
        label(kind, CATEGORIES, "categories"), label(text(beatsOf(episode).region), REGIONS, "regions"),
        day !== null && slot ? t("list.slot", { day, slot }) : "", t("list.number", { number: episode.number }),
      ].filter(Boolean);
      const working = busy.endsWith(`-${episode.number}`);
      return <li key={episode.number} className="rounded-2xl border border-[var(--line)] bg-[var(--surface)] p-3">
        <div className="flex flex-wrap items-start gap-x-3 gap-y-2">
          <span className="font-mono text-sm font-bold">{id || `#${episode.number}`}</span>
          <span className="min-w-0 flex-1 basis-48 font-semibold">{episode.title}</span>
          <AdminStatusPill status={stateTone[where]}>{t(`states.${where}`)}</AdminStatusPill>
        </div>
        <p className="mt-1 text-sm text-[var(--muted)]">{facts.join(" · ")}</p>
        <div className="mt-2 flex flex-wrap items-center gap-2">
          {id && <Button secondary aria-expanded={open} onClick={() => setOpened(open ? "" : id)}>{open ? t("list.closePlan") : t("list.openPlan")}</Button>}
          {video && <Button secondary onClick={() => onOpenVideo(video.slug)}>{t("list.openVideo")}</Button>}
          {video?.youtube_video_id && <a href={`https://www.youtube.com/watch?v=${encodeURIComponent(video.youtube_video_id)}`} target="_blank" rel="noreferrer" className="inline-flex min-h-11 items-center gap-1 rounded-xl border border-[var(--line)] px-3 text-sm font-semibold hover:border-[var(--teal)]">{t("list.youtube")}<ExternalLink aria-hidden size={14} /></a>}
          {canManage && (episode.status === "planned" || episode.status === "ready") && <Button secondary disabled={working} onClick={() => void act("skip", episode)}>{t("list.skip")}</Button>}
          {canManage && episode.status === "skipped" && !episode.started_at && <Button secondary disabled={working} onClick={() => void act("restore", episode)}>{t("list.restore")}</Button>}
          {episode.status === "skipped" && episode.started_at && <span className="text-sm text-[var(--muted)]">{t("list.startedSkipped")}</span>}
        </div>
        {open && <StoryPlan episode={episode} />}
      </li>;
    })}</ul>}
  </section>;
}

/**
 * A story whose video may be uploaded: its package, and the form that records the upload (or sends
 * it to the linked channel) with the story's next free publishing slot filled in as the scheduled
 * time. A run to YouTube in progress is read again from this video alone, not the whole series.
 */
function StoryReadyCard({ episode, video, slot, canManage, connection, onOpenVideo, onChanged }: {
  episode: SeriesEpisode; video: ProjectSummary; slot: number | null; canManage: boolean; connection: YoutubeConnection | null; onOpenVideo: (slug: string) => void; onChanged: () => void;
}) {
  const t = useTranslations("admin.videoStories");
  const slotTime = useSlotTime();
  const [detail, setDetail] = useState<Project | null>(null);
  const [error, setError] = useState("");
  const [round, setRound] = useState(0);
  const reread = useCallback(() => setRound((value) => value + 1), []);
  useEffect(() => {
    let current = true;
    api<Project>(`/admin/videos/${video.slug}`)
      .then((value) => { if (current) { setDetail(value); setError(""); } })
      .catch((problem: unknown) => { if (current) setError(message(problem)); });
    return () => { current = false; };
  }, [video.slug, video.last_synced_at, round]);
  // Reviews come newest first, so the first approved upload confirmation is the current package.
  const confirmation = detail?.reviews.find((review) => review.gate === "publish" && review.status === "approved") ?? null;
  const sync = detail ? detail.youtube_sync : video.youtube_sync;
  const { day, slot: planned } = publishOf(episode);
  const suggested = slot === null ? "" : wallClock(slot);
  const id = storyId(episode);
  return <li>
    <article aria-label={`${id} ${episode.title}`.trim()} className="grid gap-4 rounded-[1.5rem] border border-[var(--teal)] bg-[var(--surface)] p-5 shadow-[var(--shadow-sm)]">
      <header className="flex flex-wrap items-center gap-3">
        <Upload aria-hidden size={20} className="text-[var(--teal)]" />
        <h4 className="min-w-0 flex-1 font-bold"><span className="font-mono">{id}</span> {episode.title}</h4>
        <Button secondary onClick={() => onOpenVideo(video.slug)}>{t("list.openVideo")}</Button>
      </header>
      <p className="text-sm leading-6">
        {slot !== null && <strong>{t("ready.slot", { time: slotTime(slot) })}</strong>}
        {day !== null && planned && <span className="block text-[var(--muted)]">{t("ready.planned", { day, slot: planned })}</span>}
      </p>
      {error && <p role="alert" className="text-sm text-red-800">{error}</p>}
      {!detail && !error && <p className="text-sm text-[var(--muted)]">{t("ready.loading")}</p>}
      {confirmation && <UploadPackage slug={video.slug} review={confirmation} />}
      {sync && <YoutubeSyncPanel slug={video.slug} sync={sync} canManage={canManage} onChange={reread} />}
      {canManage && detail && !syncRunning(sync) && (connection?.linked
        ? <YoutubePublishForm key={suggested} slug={video.slug} review={confirmation} connection={connection} canUpload={Boolean(confirmation?.files.some((file) => file.role === "final"))} previous={sync?.request ?? null} publishAt={suggested} onSent={onChanged} />
        : <><YoutubeLinkHint /><UploadedForm key={suggested} slug={video.slug} publishAt={suggested} onLinked={onChanged} /></>)}
    </article>
  </li>;
}

/** The stories ready to upload, each offered its next free publishing slot. */
function StoryReadyGroup({ series, now, canManage, onOpenVideo, onChanged }: { series: StorySeries; now: number; canManage: boolean; onOpenVideo: (slug: string) => void; onChanged: () => void }) {
  const t = useTranslations("admin.videoStories");
  const { connection } = useYoutubeConnection();
  const slots = useMemo(() => planSlots(series.episodes, now), [series.episodes, now]);
  const ready = series.episodes.filter((episode) => episode.video && slots.has(episode.number));
  if (ready.length === 0) return null;
  return <section aria-label={t("ready.title")} className="grid gap-3">
    <h3 className="text-lg font-bold">{t("ready.title")}</h3>
    <p className="text-sm leading-6 text-[var(--muted)]">{t("ready.help")}</p>
    <ul className="grid gap-4">{ready.map((episode) => <StoryReadyCard key={episode.number} episode={episode} video={episode.video as ProjectSummary} slot={slots.get(episode.number) ?? null} canManage={canManage} connection={connection} onOpenVideo={onOpenVideo} onChanged={onChanged} />)}</ul>
  </section>;
}

/** Whether a parsed answer is an import report, as a 200 and a refusing 422 carry one. */
const isReport = (value: unknown): value is StoryImportReport => {
  const answer = record(value);
  return typeof answer.accepted === "boolean" && Array.isArray(answer.problems) && typeof answer.rows === "object" && answer.rows !== null;
};

/**
 * Send the import through the site's relay. The page reads the answer itself: a refused file is a
 * 422 whose body is the whole report, every problem listed, which api() would reduce to one line.
 */
async function postStoryImport(slug: string, body: string): Promise<StoryImportReport> {
  const response = await fetch(`/api/travel/admin/video-automation/series/${encodeURIComponent(slug)}/stories/import`, {
    method: "POST",
    body,
    cache: "no-store",
    headers: { "Content-Type": "application/json", "X-Travel-Locale": activeLocale() },
  });
  const answer: unknown = await response.json().catch(() => undefined);
  if ((response.ok || response.status === 422) && isReport(answer)) return answer;
  const code = record(answer).code;
  throw new ApiError(apiProblemMessage(answer, response.status), response.status, typeof code === "string" ? code : undefined);
}

/** The file as the page read it: the parsed JSON, how many stories, and the series it names. */
function parseStoryFile(source: string): { document: unknown; stories: number | null; slug: string; invalid: string } | null {
  if (!source.trim()) return null;
  try {
    const document: unknown = JSON.parse(source);
    const root = record(document);
    return { document, stories: Array.isArray(root.stories) ? root.stories.length : null, slug: text(record(root.series).slug), invalid: "" };
  } catch (problem) {
    return { document: null, stories: null, slug: "", invalid: message(problem) || String(problem) };
  }
}

const megabytes = (bytes: number) => (bytes / 1_048_576).toFixed(2);
// Rounded up, so a request just over the cap never reads as the cap itself.
const megabytesUp = (bytes: number) => (Math.ceil(bytes / 10_485.76) / 100).toFixed(2);
/** A series field as the report gives it, cut short: the premise and the look run long. */
const brief = (value: unknown) => {
  const written = typeof value === "string" ? value : JSON.stringify(value) ?? "";
  return written.length > 160 ? `${written.slice(0, 160)}…` : written;
};

/** A dry run's or an import's report: the counts, the stories by what happens to them, and every problem and note. */
function ImportReportView({ report, stale }: { report: StoryImportReport; stale: boolean }) {
  const t = useTranslations("admin.videoStories");
  const differs = Object.entries(report.series_differs ?? {});
  const title = report.dry_run ? t("import.dryRunTitle") : report.written ? t("import.writtenTitle") : t("import.unchangedTitle");
  // A file refused before the series was looked up says nothing about the series.
  const seriesLine = report.series_exists ? t("import.seriesExists", { slug: report.series })
    : !report.series_created ? ""
      : report.dry_run ? t("import.seriesWouldBeCreated", { slug: report.series }) : t("import.seriesCreated", { slug: report.series });
  return <section aria-label={t("import.reportTitle")} className="grid gap-3 rounded-2xl border border-[var(--line)] bg-[var(--paper)] p-4 text-sm leading-6">
    <p className="font-bold">{title}</p>
    {stale && <p className="text-amber-800">{t("import.stale")}</p>}
    {seriesLine && <p>{seriesLine}</p>}
    <p>{t("import.counts", { inFile: report.stories_in_file, imported: report.stories_imported, create: report.create, update: report.update, leave: report.leave_alone, refuse: report.refuse })}</p>
    {IMPORT_ROWS.map((row) => {
      const ids = report.rows?.[row] ?? [];
      return ids.length > 0 && <p key={row} className="break-words"><span className="font-semibold">{t(`import.rows.${row}`, { count: ids.length })}</span> <span className="font-mono text-xs">{ids.join(", ")}</span></p>;
    })}
    {differs.length > 0 && <div>
      <p className="font-semibold">{t("import.differsTitle")}</p>
      <ul className="mt-1 grid gap-1">{differs.map(([key, value]) => <li key={key} className="break-words"><code>{key}</code>: {t("import.differs", { file: brief(value?.file), series: brief(value?.series) })}</li>)}</ul>
    </div>}
    {report.problems.length > 0 && <div role="alert">
      <p className="font-semibold text-red-800">{t("import.problemsTitle", { count: report.problems.length })}</p>
      <ul className="mt-1 grid list-disc gap-1 pl-5">{report.problems.map((problem, index) => <li key={index} className="break-words">{problem}</li>)}</ul>
    </div>}
    {report.notes.length > 0 && <div>
      <p className="font-semibold">{t("import.notesTitle")}</p>
      <ul className="mt-1 grid list-disc gap-1 pl-5">{report.notes.map((note, index) => <li key={index} className="break-words">{note}</li>)}</ul>
    </div>}
  </section>;
}

/**
 * The import of a compiled stories.json (docs/videos/STORY.md, the backlog and its episode rows),
 * pasted or chosen as a file. The first answer is always a dry run, which writes nothing; only once
 * it came back without a problem, for exactly the file and choices on the form, may the owner
 * confirm and write it. ``limit`` imports only the first stories (the pilot takes two), and the
 * daily count applies when the import creates the series. On a series' page the file must name
 * that series; on the list, the file names the series it creates or fills.
 */
function StoryImportForm({ seriesSlug, canManage, onImported }: { seriesSlug?: string; canManage: boolean; onImported: (slug: string) => void }) {
  const t = useTranslations("admin.videoStories");
  const roleLabel = useRoleLabel();
  const [pasted, setPasted] = useState("");
  const [file, setFile] = useState<{ name: string; bytes: number; text: string } | null>(null);
  // Bumped whenever the file changes, so a report answers only the file it was asked about.
  const [version, setVersion] = useState(0);
  const [limit, setLimit] = useState("");
  const [perDay, setPerDay] = useState("");
  const [answer, setAnswer] = useState<{ key: string; report: StoryImportReport } | null>(null);
  const [busy, setBusy] = useState<"" | "check" | "apply">("");
  const [error, setError] = useState("");
  const source = pasted.trim() ? pasted : file?.text ?? "";
  const parsed = useMemo(() => parseStoryFile(source), [source]);
  const target = seriesSlug ?? parsed?.slug ?? "";
  const limitValue = limit.trim() ? Number(limit) : null;
  const limitOk = limitValue === null || (Number.isInteger(limitValue) && limitValue >= 1);
  const perDayValue = !seriesSlug && perDay ? Number(perDay) : null;
  const key = JSON.stringify([version, target, limitValue, perDayValue]);
  const ready = Boolean(parsed && !parsed.invalid && SLUG.test(target)) && limitOk;
  const report = answer?.report ?? null;
  const current = answer?.key === key;
  // A clean dry run of exactly what is on the form, with something to write.
  const confirmable = Boolean(report && current && report.dry_run && report.accepted && (report.create > 0 || report.update > 0 || report.series_created));
  const changeFile = () => { setVersion((value) => value + 1); setError(""); };
  const pick = (event: ChangeEvent<HTMLInputElement>) => {
    const chosen = event.target.files?.[0];
    if (!chosen) return;
    void chosen.text().then((value) => {
      setFile({ name: chosen.name, bytes: chosen.size, text: value });
      setPasted("");
      changeFile();
    }).catch((problem: unknown) => setError(t("import.readError", { message: message(problem) })));
  };
  const run = async (apply: boolean) => {
    if (!parsed || parsed.invalid || !ready) return;
    const body = JSON.stringify({ file: parsed.document, apply, limit: limitValue, episodes_per_day: perDayValue });
    const bytes = new Blob([body]).size;
    if (bytes > STORY_IMPORT_MAX_BYTES) {
      setError(t("import.tooLarge", { size: megabytesUp(bytes), max: megabytes(STORY_IMPORT_MAX_BYTES) }));
      return;
    }
    setBusy(apply ? "apply" : "check");
    setError("");
    try {
      const answered = await postStoryImport(target, body);
      setAnswer({ key, report: answered });
      if (apply && answered.written) onImported(answered.series);
    } catch (problem) {
      setError(t("import.error", { message: message(problem) }));
    } finally {
      setBusy("");
    }
  };
  return <form className="grid gap-3" aria-label={t("import.title")} onSubmit={(event) => { event.preventDefault(); void run(false); }}>
    <p className="text-sm leading-6 text-[var(--muted)]">{seriesSlug ? t("import.helpSeries", { slug: seriesSlug }) : t("import.help")}</p>
    <label className="grid gap-2 text-sm font-semibold">{t("import.file")}
      <input type="file" accept=".json,application/json" className="text-sm font-normal" disabled={busy !== ""} onChange={pick} />
    </label>
    {file && !pasted.trim() && <p className="text-sm text-[var(--muted)]">{t("import.fileChosen", { name: file.name, size: megabytes(file.bytes) })}</p>}
    <label className="grid gap-2 text-sm font-semibold">{t("import.paste")}
      <textarea className={`${control} font-mono text-xs`} rows={4} value={pasted} disabled={busy !== ""} spellCheck={false} placeholder={t("import.pastePlaceholder")} onChange={(event) => { setPasted(event.target.value); changeFile(); }} />
    </label>
    {parsed?.invalid && <p className="text-sm text-red-800">{t("import.invalidJson", { message: parsed.invalid })}</p>}
    {parsed && !parsed.invalid && <p className="text-sm text-[var(--muted)]">{parsed.stories === null ? t("import.noStories") : t("import.parsed", { count: parsed.stories, slug: parsed.slug || "—" })}</p>}
    {!seriesSlug && parsed && !parsed.invalid && !SLUG.test(parsed.slug) && <p className="text-sm text-red-800">{t("import.noSlug")}</p>}
    {seriesSlug && parsed?.slug && parsed.slug !== seriesSlug && <p className="text-sm text-amber-800">{t("import.otherSeries", { file: parsed.slug, series: seriesSlug })}</p>}
    <div className="grid gap-3 md:grid-cols-2">
      <label className="grid gap-2 text-sm font-semibold">{t("import.limit")}
        <input className={control} type="number" min={1} max={500} inputMode="numeric" value={limit} disabled={busy !== ""} placeholder={t("import.limitPlaceholder")} aria-invalid={!limitOk} onChange={(event) => setLimit(event.target.value)} />
      </label>
      {!seriesSlug && <label className="grid gap-2 text-sm font-semibold">{t("import.perDay")}
        <select className={control} value={perDay} disabled={busy !== ""} onChange={(event) => setPerDay(event.target.value)}>
          <option value="">{t("import.perDayFile")}</option>
          {PER_DAY_CHOICES.map((count) => <option key={count} value={String(count)}>{t("perDay.option", { count })}</option>)}
        </select>
      </label>}
    </div>
    <p className="text-xs leading-5 text-[var(--muted)]">{seriesSlug ? t("import.limitHelp") : `${t("import.limitHelp")} ${t("import.perDayHelp")}`}</p>
    {error && <p role="alert" className="text-sm text-red-800">{error}</p>}
    <div className="flex flex-wrap gap-3">
      <Button type="submit" secondary={confirmable} disabled={!ready || busy !== ""}>{busy === "check" ? t("import.checking") : t("import.check")}</Button>
      {confirmable && canManage && report && <Button disabled={busy !== ""} onClick={() => void run(true)}>{busy === "apply" ? t("import.writing") : t("import.apply", { create: report.create, update: report.update })}</Button>}
    </div>
    {confirmable && !canManage && <p className="text-sm text-[var(--muted)]">{t("import.applyNeedsRole", { capability: "content.manage", content: roleLabel("content"), owner: roleLabel("owner") })}</p>}
    {report && current && report.dry_run && report.accepted && !confirmable && <p className="text-sm text-[var(--muted)]">{t("import.nothingToWrite")}</p>}
    {report && <ImportReportView report={report} stale={!current} />}
  </form>;
}

/**
 * The story series on the drama tab: each one with where it stands against its limits and why no
 * story starts, opened on its own page; and the import, which also creates a series from its file.
 */
export function AdminVideoStorySeries({ onOpenSeries }: { onOpenSeries: (slug: string) => void }) {
  const t = useTranslations("admin.videoStories");
  const ts = useTranslations("admin.videoSeries");
  const manage = useAdminActionGuard("content.manage");
  const today = useTodayText();
  const holdReason = useHoldReason();
  const [series, setSeries] = useState<StorySummary[] | null>(null);
  const [error, setError] = useState("");
  const load = useCallback(() => {
    // An older site ignores the filter and is filtered here.
    api<{ series?: StorySummary[] }>("/admin/video-automation/series?kind=story")
      .then((value) => { setSeries((value?.series ?? []).filter((each) => each.kind === "story")); setError(""); })
      .catch((problem: unknown) => setError(message(problem)));
  }, []);
  useRefresh(load);
  return <section aria-label={t("title")} className="grid gap-3">
    <h3 className="text-lg font-bold">{t("title")}</h3>
    <p className="text-sm leading-6 text-[var(--muted)]">{t("intro")}</p>
    {error && <p role="alert" className="text-sm text-red-800">{t("loadError", { message: error })}</p>}
    {series && series.length > 0 && <ul className="grid gap-4" aria-label={t("title")}>{series.map((each) => {
      const quota = each.quota;
      const reason = quota ? holdReason(quota, each.status) : "";
      return <li key={each.slug}>
        <button type="button" onClick={() => onOpenSeries(each.slug)} className="grid w-full gap-2 rounded-[1.5rem] border border-[var(--line)] bg-[var(--surface)] p-5 text-left shadow-[var(--shadow-sm)] hover:border-[var(--teal)]">
          <span className="flex flex-wrap items-center gap-3"><BookOpenText aria-hidden size={20} className="text-[var(--teal)]" /><span className="text-lg font-bold">{each.title}</span>
            <AdminStatusPill status="active">{t("kind")}</AdminStatusPill>
            <AdminStatusPill status={seriesTone[each.status] ?? "inactive"}>{ts(`statuses.${each.status}`)}</AdminStatusPill>
          </span>
          {quota && <span className="text-sm text-[var(--muted)]">{t("quota.line", { today: today(quota), inFlight: quota.in_flight, maxInFlight: quota.max_in_flight, awaiting: quota.awaiting_upload, buffer: quota.upload_buffer, ready: quota.ready })}</span>}
          {reason && <span className="text-sm text-amber-900">{t("quota.holdTitle")} {reason}</span>}
        </button>
      </li>;
    })}</ul>}
    <details className="rounded-[1.5rem] border border-[var(--line)] bg-[var(--surface)] p-5 shadow-[var(--shadow-sm)]" open={series !== null && series.length === 0}>
      <summary className="cursor-pointer text-lg font-bold">{t("import.title")}</summary>
      <div className="mt-4"><StoryImportForm canManage={manage.allowed} onImported={(slug) => { load(); onOpenSeries(slug); }} /></div>
    </details>
  </section>;
}

/**
 * A story series' own page, in place of a long series' documents and chapters: what holds the next
 * story back, pause and the daily count, the stories ready to upload with their next free slot,
 * every story with its plan, and the import again (it updates only the stories not started yet).
 */
export function StorySeriesPage({ series, error, onBack, onOpenVideo, onChanged }: { series: StorySeries; error: string; onBack: () => void; onOpenVideo: (slug: string) => void; onChanged: () => void }) {
  const t = useTranslations("admin.videoStories");
  const ts = useTranslations("admin.videoSeries");
  const manage = useAdminActionGuard("content.manage");
  const now = useNow();
  const back = () => {
    // The page's own filters and the opened story stay behind with it.
    const target = new URL(window.location.href);
    for (const key of QUERY_KEYS) target.searchParams.delete(key);
    adminNavigate(target, true);
    onBack();
  };
  const done = series.episodes.filter((episode) => episode.status === "done").length;
  return <section className="mt-6 grid gap-5">
    <div><Button secondary onClick={back}><ArrowLeft aria-hidden size={18} />{ts("back")}</Button></div>
    {error && <AdminErrorState title={ts("loadError")} detail={error} retry={onChanged} retryLabel={ts("retry")} />}
    <header className="grid gap-2">
      <h2 className="flex flex-wrap items-center gap-3 text-2xl font-bold">{series.title}<AdminStatusPill status="active">{t("kind")}</AdminStatusPill><AdminStatusPill status={seriesTone[series.status] ?? "inactive"}>{ts(`statuses.${series.status}`)}</AdminStatusPill></h2>
      <p className="text-sm text-[var(--muted)]">{t("page.facts", { stories: series.episodes.length, done, minutes: series.target_minutes, usd: Number(series.media_usd ?? 0).toFixed(2) })}{series.image_model ? ` · ${t("page.imageModel", { model: series.image_model })}` : ""}</p>
      <p className="whitespace-pre-wrap text-sm leading-6">{series.premise}</p>
    </header>
    {!manage.allowed && <StoryPermissionNote />}
    {series.quota && <StoryQuotaPanel quota={series.quota} status={series.status} />}
    {manage.allowed && <StoryControls series={series} onChanged={onChanged} />}
    <StoryReadyGroup series={series} now={now} canManage={manage.allowed} onOpenVideo={onOpenVideo} onChanged={onChanged} />
    <StoryList series={series} now={now} canManage={manage.allowed} onOpenVideo={onOpenVideo} onChanged={onChanged} />
    <details className="rounded-[1.5rem] border border-[var(--line)] bg-[var(--surface)] p-5 shadow-[var(--shadow-sm)]" open={series.episodes.length === 0}>
      <summary className="cursor-pointer text-lg font-bold">{t("import.again")}</summary>
      <div className="mt-4"><StoryImportForm seriesSlug={series.slug} canManage={manage.allowed} onImported={onChanged} /></div>
    </details>
  </section>;
}
