"use client";

import { Download, Smartphone } from "lucide-react";
import { useTranslations } from "next-intl";
import { type ReactNode, useCallback, useEffect, useMemo, useState } from "react";
import { useAdminActionGuard } from "@/components/admin-action-guard";
import { AdminEmptyState, AdminErrorState, AdminStatusPill } from "@/components/admin-ui";
import { type Project, type ProjectSummary, type Review, fileFor, fileUrl, isBlocked, list, record, text, useRefresh, useWhen } from "@/components/admin-video-review-card";
import { ShortsCalendar } from "@/components/admin-video-shorts-calendar";
import { ShortsCosts } from "@/components/admin-video-shorts-costs";
import {
  autopublishTone, type ClaimAnswer, dollars, message, type Need, type Overview, type RecallAnswer, SHORTS_STATES, type ShortsState, sizeOf, type Slot, slotTone,
  stateTone, type Uploads, type View, VIEWS,
} from "@/components/admin-video-shorts-data";
import { ShortsMetrics } from "@/components/admin-video-shorts-metrics";
import { ShortsReport } from "@/components/admin-video-shorts-report";
import { ShortsSettingsPanel } from "@/components/admin-video-shorts-settings";
import { ShortsTopics } from "@/components/admin-video-shorts-topics";
import { Button, Tabs } from "@/components/community/ui";
import { adminNavigate, useAdminQueryState } from "@/lib/admin-workspace-navigation";
import { api } from "@/lib/api";

// The Shorts tab of /admin/videos (docs/videos/SHORTS.md): the top row says where publishing
// stands, "needs you" lists what waits for the owner with the button that does it, the files to
// upload are listed until the API audit passes, and seven views hold the rest: the calendar
// (admin-video-shorts-calendar.tsx), the library, the numbers (…-metrics.tsx), the ledger
// (…-costs.tsx), the topic library with the owner's material (…-topics.tsx), the weekly report
// (…-report.tsx) and the settings with the standing consent (…-settings.tsx). One Short opens
// on the video page, like every other video (admin-video-reviews.tsx).

// Where the batch of files to upload downloads from: a route of its own, since the generic
// proxy reads a response as text and caps it (apps/web/app/api/admin-video-shorts/batch).
export const BATCH_URL = "/api/admin-video-shorts/batch";
const UPLOADS_ID = "shorts-uploads";
// How many cards of a group the library shows before "more": each card reads its video once.
const GROUP_PAGE = 12;

function open(change: (target: URL) => void) {
  const target = new URL(window.location.href);
  change(target);
  adminNavigate(target);
}

/** The page's own settings tab, where the YouTube channel is linked. */
const openChannel = () => open((target) => { target.searchParams.set("tab", "settings"); target.searchParams.delete("view"); target.searchParams.delete("section"); });

function Tile({ label, children }: { label: string; children: ReactNode }) {
  return <div className="grid content-start gap-1 rounded-2xl border border-[var(--line)] bg-[var(--surface)] p-4">
    <dt className="text-xs font-black tracking-[.12em] text-[var(--teal)]">{label}</dt>
    <dd className="grid gap-1 text-sm leading-6">{children}</dd>
  </div>;
}

function SlotLine({ slot }: { slot: Slot }) {
  const t = useTranslations("admin.videoShorts");
  // A slot that was missed or is not publishing waits for no Short: its pill says all there is.
  const waits = slot.status !== "skipped" && slot.status !== "missed";
  return <span className="flex flex-wrap items-center gap-2">
    <span className="font-mono">{slot.local_time}</span>
    {slot.project_title ? <span className="font-semibold">{slot.project_title}</span> : waits && <span className="text-[var(--muted)]">{t("top.emptySlot")}</span>}
    <AdminStatusPill status={slotTone[slot.status]}>{t(`slotStatuses.${slot.status}`)}</AdminStatusPill>
  </span>;
}

/** Where publishing stands, in tiles, with the three switches a reviewer has: pause, resume, recall. */
function TopRow({ overview, canManage, onChanged }: { overview: Overview; canManage: boolean; onChanged: () => void }) {
  const t = useTranslations("admin.videoShorts");
  const when = useWhen();
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [recalled, setRecalled] = useState<RecallAnswer | null>(null);
  const act = async (path: "pause" | "resume" | "recall") => {
    if (path === "recall" && !window.confirm(t("top.recallConfirm"))) return;
    setBusy(true);
    setError("");
    try {
      const answer = await api<RecallAnswer>(`/admin/video-shorts/${path}`, { method: "POST" });
      setRecalled(path === "recall" ? answer : null);
      onChanged();
    } catch (problem) {
      setError(t("top.actionError", { message: message(problem) }));
    } finally {
      setBusy(false);
    }
  };
  const { budget, stock, channel, campaign } = overview;
  const paused = Boolean(overview.paused_at);
  return <section aria-label={t("top.title")} className="grid gap-3">
    <dl className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
      <Tile label={t("top.autopublish")}>
        <span><AdminStatusPill status={autopublishTone[overview.autopublish]}>{t(`top.autopublishStates.${overview.autopublish}`)}</AdminStatusPill></span>
        {overview.autopublish_problem && <span>{overview.autopublish_problem}</span>}
        {overview.consent_expires_at && overview.autopublish !== "off" && <span className="text-[var(--muted)]">{t("top.consentUntil", { time: when(overview.consent_expires_at) })}</span>}
        {canManage && <span className="mt-1 flex flex-wrap gap-2">
          {paused
            ? <Button secondary disabled={busy} onClick={() => void act("resume")}>{t("top.resume")}</Button>
            : <Button secondary disabled={busy} onClick={() => void act("pause")}>{t("top.pause")}</Button>}
          <Button secondary disabled={busy} onClick={() => void act("recall")}>{t("top.recall")}</Button>
        </span>}
      </Tile>
      <Tile label={t("top.today")}>{overview.today.length ? overview.today.map((slot) => <SlotLine key={slot.id} slot={slot} />) : <span className="text-[var(--muted)]">{t("top.noSlots")}</span>}</Tile>
      <Tile label={t("top.tomorrow")}>{overview.tomorrow.length ? overview.tomorrow.map((slot) => <SlotLine key={slot.id} slot={slot} />) : <span className="text-[var(--muted)]">{t("top.noSlots")}</span>}</Tile>
      <Tile label={t("top.stock")}>
        <span className="font-semibold">{t("top.stockCount", { count: stock.count })}</span>
        <span className="text-[var(--muted)]">{stock.days === null ? t("top.stockBefore") : t("top.stockDays", { days: stock.days, wanted: stock.wanted_days })}</span>
      </Tile>
      <Tile label={t("top.budget")}>
        <span className="font-semibold">{t("top.budgetSpent", { spent: dollars(budget.spent_ntd), limit: dollars(budget.limit_ntd) })}</span>
        {budget.reserved_ntd > 0 && <span className="text-[var(--muted)]">{t("top.budgetReserved", { reserved: dollars(budget.reserved_ntd) })}</span>}
        {budget.unknown > 0 && <span className="text-amber-800">{t("top.budgetUnknown", { count: budget.unknown })}</span>}
        {!budget.paid_work_allowed && <span><AdminStatusPill status="failed">{t("top.budgetStopped")}</AdminStatusPill></span>}
      </Tile>
      <Tile label={t("top.channel")}>
        {channel.linked ? <span className="font-semibold">{channel.title ?? t("top.channelLinked")}</span> : <span className="text-amber-800">{t("top.channelNotLinked")}</span>}
        {channel.problem && <span className="text-red-800">{channel.problem}</span>}
        {channel.linked && <span className="text-[var(--muted)]">{channel.audited ? t("top.channelAudited") : t("top.channelNotAudited")}</span>}
        {(!channel.linked || channel.problem) && <span><Button secondary onClick={openChannel}>{t("top.openChannel")}</Button></span>}
      </Tile>
      <Tile label={t("top.worker")}><span className={overview.worker_seen_at ? "" : "text-[var(--muted)]"}>{overview.worker_seen_at ? t("top.workerSeen", { time: when(overview.worker_seen_at) }) : t("top.workerNever")}</span></Tile>
      <Tile label={t("top.campaign")}>
        {campaign.start && campaign.last_day
          ? <><span className="font-semibold">{t("top.campaignRange", { start: campaign.start, end: campaign.last_day })}</span><span className="text-[var(--muted)]">{t("top.campaignCounts", { slots: campaign.slots, published: campaign.published, missed: campaign.missed })}</span></>
          : <span className="text-[var(--muted)]">{t("top.campaignNone")}</span>}
      </Tile>
    </dl>
    <p className="rounded-2xl border border-[var(--line)] bg-[var(--paper)] p-4 text-sm leading-6"><strong>{t("top.goal")}</strong> {t("top.goalText")} <span className="text-[var(--muted)]">{t("top.goalViews")}</span></p>
    {error && <p role="alert" className="text-sm text-red-800">{error}</p>}
    {recalled && <div role="status" className="rounded-2xl border border-[var(--line)] p-4 text-sm leading-6">
      <p className="font-semibold">{recalled.items.length ? t("top.recallDone", { count: recalled.recalled }) : t("top.recallNone")}</p>
      {recalled.items.length > 0 && <ul className="mt-1 grid gap-1">{recalled.items.map((item) => <li key={item.slug}><span className="font-mono">{item.slug}</span> · {item.detail}</li>)}</ul>}
    </div>}
  </section>;
}

/** What waits for the owner, one sentence each, with the button that goes and does it. */
function Needs({ needs, onView, onOpenVideo }: { needs: Need[]; onView: (view: View) => void; onOpenVideo: (slug: string) => void }) {
  const t = useTranslations("admin.videoShorts");
  const act = (need: Need): (() => void) | null => {
    if ((need.kind === "review" || need.kind === "blocked") && need.slug) return () => onOpenVideo(String(need.slug));
    if (need.kind === "consent") return () => onView("settings");
    if (need.kind === "channel") return openChannel;
    if (need.kind === "upload") return () => document.getElementById(UPLOADS_ID)?.scrollIntoView({ block: "start" });
    if (need.kind === "budget") return () => onView("costs");
    if (need.kind === "missed") return () => onView("calendar");
    if (need.kind === "stock") return () => onView("library");
    return null;
  };
  return <section aria-label={t("needs.title")} className="grid gap-3">
    <h2 className="text-xs font-black tracking-[.16em] text-[var(--teal)]">{t("needs.title")}{needs.length > 0 && ` · ${needs.length}`}</h2>
    {needs.length === 0 ? <p className="text-sm text-[var(--muted)]">{t("needs.none")}</p> : <ul className="grid gap-2">{needs.map((need, index) => {
      const action = act(need);
      return <li key={`${need.kind}-${need.slug ?? index}`} className="flex flex-wrap items-center gap-3 rounded-2xl border border-amber-600 bg-amber-50 p-4 text-sm leading-6">
        <span className="min-w-0 flex-1">{need.detail}</span>
        {action && <Button secondary onClick={action}>{t(`needs.actions.${need.kind}`)}</Button>}
      </li>;
    })}</ul>}
  </section>;
}

/**
 * Until the API audit passes the owner uploads the files themselves (docs/videos/SHORTS.md, the
 * section on what happens before the audit): the batch as one archive, three steps in Studio, and
 * "I uploaded them", after which the site finds each file on the channel and says what it found.
 */
function UploadsPanel({ canManage, onClaimed }: { canManage: boolean; onClaimed: () => void }) {
  const t = useTranslations("admin.videoShorts");
  const when = useWhen();
  const [uploads, setUploads] = useState<Uploads | null>(null);
  const [answer, setAnswer] = useState<ClaimAnswer | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const load = useCallback(() => {
    api<Uploads>("/admin/video-shorts/uploads").then((value) => setUploads(value)).catch(() => setUploads(null));
  }, []);
  useRefresh(load);
  const claim = async () => {
    setBusy(true);
    setError("");
    try {
      setAnswer(await api<ClaimAnswer>("/admin/video-shorts/uploads/claim", { method: "POST" }));
      load();
      onClaimed();
    } catch (problem) {
      setError(t("uploads.claimError", { message: message(problem) }));
    } finally {
      setBusy(false);
    }
  };
  if (!uploads || (uploads.items.length === 0 && !answer)) return null;
  return <section id={UPLOADS_ID} aria-label={t("uploads.title")} className="grid gap-4 rounded-[1.5rem] border border-[var(--teal)] bg-[var(--surface)] p-5 shadow-[var(--shadow-sm)]">
    <h2 className="text-lg font-bold">{t("uploads.title")}</h2>
    <p className="text-sm leading-6 text-[var(--muted)]">{t("uploads.help", { days: uploads.ahead_days })}</p>
    {uploads.items.length > 0 && <div className="overflow-x-auto"><table className="w-full min-w-[36rem] text-left text-sm">
      <thead><tr className="text-xs text-[var(--muted)]">{(["short", "file", "length", "size", "slot"] as const).map((column) => <th key={column} scope="col" className="py-1 pr-3 font-semibold">{t(`uploads.columns.${column}`)}</th>)}</tr></thead>
      <tbody>{uploads.items.map((item) => <tr key={item.slug} className="border-t border-[var(--line)]">
        <th scope="row" className="py-2 pr-3 font-semibold">{item.title}{item.line && <span className="ml-2 text-xs font-normal text-[var(--muted)]">{t(`lines.${item.line}`)}</span>}</th>
        <td className="py-2 pr-3 font-mono text-xs">{item.file_name}</td>
        <td className="py-2 pr-3">{item.seconds === null ? "—" : t("seconds", { seconds: item.seconds })}</td>
        <td className="py-2 pr-3">{item.size === null ? "—" : sizeOf(item.size)}</td>
        <td className="py-2">{when(item.slot_at)}</td>
      </tr>)}</tbody>
    </table></div>}
    <ol className="grid list-decimal gap-1 pl-5 text-sm leading-6">{(["one", "two", "three"] as const).map((step) => <li key={step}>{t(`uploads.steps.${step}`)}</li>)}</ol>
    {canManage && <div className="flex flex-wrap gap-3">
      {uploads.items.length > 0 && <a href={BATCH_URL} download="mokaair-shorts.zip" className="inline-flex min-h-11 items-center gap-2 rounded-xl border border-[var(--teal)] bg-[var(--surface)] px-4 text-sm font-semibold hover:bg-[var(--paper)]"><Download aria-hidden size={16} />{t("uploads.download")}</a>}
      <Button disabled={busy} onClick={() => void claim()}>{busy ? t("uploads.claiming") : t("uploads.claim")}</Button>
    </div>}
    {error && <p role="alert" className="text-sm text-red-800">{error}</p>}
    {answer && <div role="status" className="grid gap-2 text-sm leading-6">
      <p className="font-semibold">{t("uploads.claimed", { count: answer.claimed })}</p>
      <ul className="grid gap-1">{answer.items.map((item) => <li key={item.slug} className="flex flex-wrap items-center gap-2">
        <AdminStatusPill status={item.result === "matched" ? "ok" : item.result === "duplicate" ? "warning" : "failed"}>{t(`uploads.results.${item.result}`)}</AdminStatusPill>
        <span className="font-mono text-xs">{item.file_name}</span><span>{item.detail}</span>
      </li>)}</ul>
    </div>}
  </section>;
}

/** What a card shows of a Short beyond its summary, read from its reviews: newest first. */
function cardFacts(project: Project | null) {
  const reviews: Review[] = project?.reviews ?? [];
  const final = reviews.find((review) => review.gate === "final");
  const items = list(record(final?.payload.qa).items).map(record);
  return {
    cover: final && project ? fileUrl(project.slug, fileFor(final, "thumbnail")) : undefined,
    seconds: typeof final?.payload.duration_seconds === "number" ? final.payload.duration_seconds : null,
    checked: items.length,
    failed: items.filter((item) => item.ok !== true).map((item) => text(item.id)),
  };
}

/** One Short of the library: its cover, length, line, what the checks said and the slot it holds. */
function ShortCard({ project, onOpen }: { project: ProjectSummary; onOpen: (slug: string) => void }) {
  const t = useTranslations("admin.videoShorts");
  const when = useWhen();
  const [detail, setDetail] = useState<Project | null>(null);
  useEffect(() => {
    let current = true;
    api<Project>(`/admin/videos/${project.slug}`).then((value) => { if (current) setDetail(value); }).catch(() => undefined);
    return () => { current = false; };
  }, [project.slug, project.last_synced_at]);
  const facts = cardFacts(detail);
  const state = project.shorts_state ?? "making";
  return <li>
    <button type="button" onClick={() => onOpen(project.slug)} aria-label={t("library.open", { title: project.title })}
      className="grid w-full grid-cols-[4.5rem_1fr] gap-4 rounded-[1.5rem] border border-[var(--line)] bg-[var(--surface)] p-4 text-left shadow-[var(--shadow-sm)] hover:border-[var(--teal)]">
      {/* Nine by sixteen from a height of its own (the column is 4.5rem wide), not from
          aspect-ratio: that box, inside a button, stopped the page in one embedded Chromium 152. */}
      <span data-testid="shorts-card-cover" className="grid h-32 w-full place-items-center overflow-hidden rounded-xl bg-[var(--paper)]">
        {/* A private, session-bound preview: the image optimizer cannot fetch it. */}
        {/* eslint-disable-next-line @next/next/no-img-element */}
        {facts.cover ? <img src={facts.cover} alt={t("library.cover", { title: project.title })} className="h-full w-full object-contain" loading="lazy" /> : <Smartphone aria-hidden size={24} className="text-[var(--muted)]" />}
      </span>
      <span className="grid content-start gap-2">
        <span className="flex flex-wrap items-center gap-2"><span className="font-bold">{project.title}</span>
          <AdminStatusPill status={stateTone[state]}>{t(`states.${state}`)}</AdminStatusPill>
          {project.shorts_line && <AdminStatusPill status="inactive">{t(`lines.${project.shorts_line}`)}</AdminStatusPill>}
          {isBlocked(project) && <AdminStatusPill status="failed">{t("library.blocked")}</AdminStatusPill>}
        </span>
        <span className="text-sm text-[var(--muted)]">
          {[
            project.shorts_series && t("library.series", { series: project.shorts_series }),
            project.source_slug && t("library.source", { slug: project.source_slug }),
            facts.seconds !== null && t("seconds", { seconds: facts.seconds }),
          ].filter(Boolean).join(" · ")}
        </span>
        <span className="flex flex-wrap items-center gap-2 text-sm">
          {facts.checked > 0 && <AdminStatusPill status={facts.failed.length ? "failed" : "ok"}>{facts.failed.length ? t("library.qaFailed", { count: facts.failed.length }) : t("library.qaPassed", { count: facts.checked })}</AdminStatusPill>}
          {project.pending > 0 && <AdminStatusPill status="pending">{t("library.pending", { count: project.pending })}</AdminStatusPill>}
          <span className="text-[var(--muted)]">{project.slot_at ? t("library.slotAt", { time: when(project.slot_at) }) : t("library.noSlot")}</span>
        </span>
      </span>
    </button>
  </li>;
}

/**
 * The Shorts in hand, grouped by where each stands (the server's shorts_state): what waits for the
 * owner first, then the making, the library (with the ones that missed a slot), what holds a slot
 * and what is scheduled. The public ones are on the numbers view; the latest of them close the list.
 */
export function ShortsLibrary({ onOpenVideo }: { onOpenVideo: (slug: string) => void }) {
  const t = useTranslations("admin.videoShorts");
  const [projects, setProjects] = useState<ProjectSummary[] | null>(null);
  const [error, setError] = useState("");
  const [shown, setShown] = useState<Partial<Record<ShortsState, number>>>({});
  const load = useCallback(() => {
    api<ProjectSummary[]>("/admin/videos?shorts=only").then((value) => { setProjects(value); setError(""); }).catch((problem: unknown) => setError(message(problem)));
  }, []);
  useRefresh(load);
  const groups = useMemo(() => SHORTS_STATES.map((state) => ({ state, items: (projects ?? []).filter((project) => (project.shorts_state ?? "making") === state) })).filter((group) => group.items.length > 0), [projects]);
  if (error) return <AdminErrorState title={t("loadError")} detail={error} retry={load} retryLabel={t("retry")} />;
  if (!projects) return <p className="text-[var(--muted)]">{t("loading")}</p>;
  if (projects.length === 0) return <AdminEmptyState title={t("library.empty")} detail={t("library.emptyDetail")} />;
  return <div className="grid gap-6" aria-label={t("views.library")}>{groups.map(({ state, items }) => {
    const limit = shown[state] ?? GROUP_PAGE;
    return <section key={state} aria-label={t(`library.groups.${state}`)} className="grid gap-3">
      <h2 className="text-xs font-black tracking-[.16em] text-[var(--teal)]">{t(`library.groups.${state}`)} · {items.length}</h2>
      <ul className="grid gap-4 xl:grid-cols-2">{items.slice(0, limit).map((project) => <ShortCard key={project.slug} project={project} onOpen={onOpenVideo} />)}</ul>
      {items.length > limit && <div><Button secondary onClick={() => setShown((current) => ({ ...current, [state]: limit + GROUP_PAGE }))}>{t("library.more", { count: Math.min(GROUP_PAGE, items.length - limit) })}</Button></div>}
    </section>;
  })}</div>;
}

export function AdminVideoShorts({ onOpenVideo }: { onOpenVideo: (slug: string) => void }) {
  const t = useTranslations("admin.videoShorts");
  const manage = useAdminActionGuard("content.manage");
  const [view, setView] = useAdminQueryState("view", VIEWS, "calendar");
  const [overview, setOverview] = useState<Overview | null>(null);
  const [error, setError] = useState("");
  const load = useCallback(() => {
    api<Overview>("/admin/video-shorts/overview").then((value) => { setOverview(value); setError(""); }).catch((problem: unknown) => setError(message(problem)));
  }, []);
  useRefresh(load);
  return <div className="mt-6 grid gap-6">
    {error && <AdminErrorState title={t("loadError")} detail={error} retry={load} retryLabel={t("retry")} />}
    {!overview && !error && <p className="text-[var(--muted)]">{t("loading")}</p>}
    {overview && <TopRow overview={overview} canManage={manage.allowed} onChanged={load} />}
    {overview && <Needs needs={overview.needs} onView={setView} onOpenVideo={onOpenVideo} />}
    {overview?.channel.linked && !overview.channel.audited && <UploadsPanel canManage={manage.allowed} onClaimed={load} />}
    <Tabs value={view} onChange={(value) => setView(value as View)} label={t("viewsLabel")} items={VIEWS.map((each) => ({ value: each, label: t(`views.${each}`) }))}>
      {view === "calendar" && <ShortsCalendar canManage={manage.allowed} onChanged={load} onOpenVideo={onOpenVideo} />}
      {view === "library" && <ShortsLibrary onOpenVideo={onOpenVideo} />}
      {view === "metrics" && <ShortsMetrics onOpenVideo={onOpenVideo} />}
      {view === "costs" && <ShortsCosts canManage={manage.allowed} onChanged={load} />}
      {view === "topics" && <ShortsTopics canManage={manage.allowed} />}
      {view === "report" && <ShortsReport />}
      {view === "settings" && <ShortsSettingsPanel onChanged={load} />}
    </Tabs>
  </div>;
}
