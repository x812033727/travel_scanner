"use client";

import { useLocale, useTranslations } from "next-intl";
import { useCallback, useMemo, useState } from "react";
import { AdminEmptyState, AdminErrorState, AdminStatusPill } from "@/components/admin-ui";
import { control, type ProjectSummary, useRefresh } from "@/components/admin-video-review-card";
import { addDays, CHANGEABLE, dayIn, localInput, message, type Slot, type SlotAction, type SlotsView, slotTone, zonedInstant } from "@/components/admin-video-shorts-data";
import { Button } from "@/components/community/ui";
import { useAdminQueryValue } from "@/lib/admin-workspace-navigation";
import { api } from "@/lib/api";

// The calendar of the Shorts tab (docs/videos/SHORTS.md, the section on slots): a row a day, a
// card a slot, two weeks at a time. A slot's time is a time of day in the calendar's zone, so what
// the owner types is read in that zone, whatever zone their browser is in. Every change is one
// PATCH of /admin/video-shorts/slots/{id} with one action; a slot that is on YouTube or past is
// not changed here.
const DAYS = 14;
const DAY = /^\d{4}-\d{2}-\d{2}$/;
// The Shorts a slot can be given (apps/api/app/video_shorts/slots.py _assign).
const ASSIGNABLE = ["library", "missed", "slotted"];
type Change = { action: SlotAction; starts_at?: string; project_slug?: string; note?: string };

function SlotCard({ slot, timezone, shorts, canManage, onChanged, onOpenVideo }: {
  slot: Slot; timezone: string; shorts: ProjectSummary[]; canManage: boolean; onChanged: () => void; onOpenVideo: (slug: string) => void;
}) {
  const t = useTranslations("admin.videoShorts");
  const [moveTo, setMoveTo] = useState(() => localInput(slot.starts_at, timezone));
  const [pick, setPick] = useState("");
  const [note, setNote] = useState(slot.note ?? "");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const changeable = canManage && CHANGEABLE.includes(slot.status);
  const candidates = shorts.filter((short) => short.slug !== slot.project_slug);
  const target = zonedInstant(moveTo, timezone);
  const moved = target !== null && target.getTime() !== Date.parse(slot.starts_at);
  const change = async (body: Change) => {
    setBusy(true);
    setError("");
    try {
      await api(`/admin/video-shorts/slots/${slot.id}`, { method: "PATCH", body: JSON.stringify(body) });
      onChanged();
    } catch (problem) {
      setError(t("calendar.changeError", { message: message(problem) }));
    } finally {
      setBusy(false);
    }
  };
  const title = slot.project_title ?? (slot.topic_slug ? t("calendar.topic", { topic: slot.topic_slug }) : t("calendar.emptySlot"));
  const line = slot.project_line ?? slot.line;
  return <li className="grid content-start gap-2 rounded-2xl border border-[var(--line)] bg-[var(--surface)] p-4" aria-label={`${slot.local_date} ${slot.local_time}`}>
    <p className="flex flex-wrap items-center gap-2">
      <span className="font-mono font-bold">{slot.local_time}</span>
      <AdminStatusPill status={slotTone[slot.status]}>{t(`slotStatuses.${slot.status}`)}</AdminStatusPill>
      {line && <AdminStatusPill status="inactive">{t(`lines.${line}`)}</AdminStatusPill>}
    </p>
    <p className={slot.project_title ? "font-semibold" : "text-[var(--muted)]"}>{title}</p>
    {slot.note && <p className="text-sm leading-6 text-[var(--muted)]">{slot.note}</p>}
    {slot.project_slug && <div><Button secondary onClick={() => onOpenVideo(String(slot.project_slug))}>{t("calendar.open")}</Button></div>}
    {canManage && !changeable && <p className="text-xs leading-5 text-[var(--muted)]">{t("calendar.fixed")}</p>}
    {changeable && <details className="rounded-xl border border-[var(--line)] p-3">
      <summary className="cursor-pointer text-sm font-semibold">{t("calendar.change")}</summary>
      <div className="mt-3 grid gap-3 text-sm">
        {slot.status === "skipped"
          ? <div><Button secondary disabled={busy} onClick={() => void change({ action: "reopen" })}>{t("calendar.reopenButton")}</Button></div>
          : <>
            <label className="grid gap-1 font-semibold">{t("calendar.moveTo", { timezone })}
              <input type="datetime-local" className={control} value={moveTo} disabled={busy} onChange={(event) => setMoveTo(event.target.value)} />
            </label>
            <div><Button secondary disabled={busy || !moved} onClick={() => target && void change({ action: "move", starts_at: target.toISOString() })}>{t("calendar.moveButton")}</Button></div>
            <label className="grid gap-1 font-semibold">{t("calendar.assignPick")}
              <select className={control} value={pick} disabled={busy || candidates.length === 0} onChange={(event) => setPick(event.target.value)}>
                <option value="">{candidates.length ? t("calendar.assignChoose") : t("calendar.assignNone")}</option>
                {candidates.map((short) => <option key={short.slug} value={short.slug}>{short.title}{short.shorts_line ? ` · ${t(`lines.${short.shorts_line}`)}` : ""}</option>)}
              </select>
            </label>
            <div className="flex flex-wrap gap-2">
              <Button secondary disabled={busy || !pick} onClick={() => void change({ action: "assign", project_slug: pick })}>{t("calendar.assignButton")}</Button>
              {slot.project_slug && <Button secondary disabled={busy} onClick={() => void change({ action: "clear" })}>{t("calendar.clearButton")}</Button>}
              <Button secondary disabled={busy} onClick={() => void change({ action: "skip" })}>{t("calendar.skipButton")}</Button>
            </div>
          </>}
        <label className="grid gap-1 font-semibold">{t("calendar.noteLabel")}
          <input className={control} value={note} maxLength={500} disabled={busy} onChange={(event) => setNote(event.target.value)} />
        </label>
        <div><Button secondary disabled={busy || note.trim() === (slot.note ?? "")} onClick={() => void change({ action: "note", note: note.trim() })}>{t("calendar.noteButton")}</Button></div>
        {error && <p role="alert" className="text-red-800">{error}</p>}
      </div>
    </details>}
  </li>;
}

export function ShortsCalendar({ canManage, onChanged, onOpenVideo }: { canManage: boolean; onChanged: () => void; onOpenVideo: (slug: string) => void }) {
  const t = useTranslations("admin.videoShorts");
  const locale = useLocale();
  const [from, setFrom] = useAdminQueryValue("from", "", (value) => DAY.test(value));
  const [view, setView] = useState<SlotsView | null>(null);
  const [shorts, setShorts] = useState<ProjectSummary[]>([]);
  const [error, setError] = useState("");
  // Before the first answer names the calendar's zone, the browser's day is close enough.
  const first = from || dayIn(view?.timezone ?? Intl.DateTimeFormat().resolvedOptions().timeZone);
  const last = addDays(first, DAYS - 1);
  const load = useCallback(() => {
    api<SlotsView>(`/admin/video-shorts/slots?from=${first}&to=${last}`).then((value) => { setView(value); setError(""); }).catch((problem: unknown) => setError(message(problem)));
    if (canManage) api<ProjectSummary[]>("/admin/videos?shorts=only").then((value) => setShorts(value.filter((short) => ASSIGNABLE.includes(short.shorts_state ?? "")))).catch(() => setShorts([]));
  }, [first, last, canManage]);
  useRefresh(load);
  const changed = () => { load(); onChanged(); };
  const weekday = useMemo(() => new Intl.DateTimeFormat(locale, { weekday: "short", month: "numeric", day: "numeric", timeZone: "UTC" }), [locale]);
  const days = useMemo(() => {
    const byDay = new Map<string, Slot[]>();
    for (const slot of view?.slots ?? []) byDay.set(slot.local_date, [...(byDay.get(slot.local_date) ?? []), slot]);
    return [...byDay.entries()].sort(([a], [b]) => a.localeCompare(b));
  }, [view]);
  if (error) return <AdminErrorState title={t("loadError")} detail={error} retry={load} retryLabel={t("retry")} />;
  if (!view) return <p className="text-[var(--muted)]">{t("loading")}</p>;
  return <section aria-label={t("views.calendar")} className="grid gap-4">
    <div className="flex flex-wrap items-center gap-3">
      <Button secondary onClick={() => setFrom(addDays(first, -DAYS))}>{t("calendar.earlier")}</Button>
      <Button secondary onClick={() => setFrom("")}>{t("calendar.today")}</Button>
      <Button secondary onClick={() => setFrom(addDays(first, DAYS))}>{t("calendar.later")}</Button>
      <span className="text-sm text-[var(--muted)]">{t("calendar.range", { start: first, end: last })} · {t("calendar.timezone", { timezone: view.timezone })}</span>
    </div>
    {days.length === 0 && <AdminEmptyState title={t("calendar.empty")} detail={t("calendar.emptyDetail")} />}
    <ol className="grid gap-4">{days.map(([day, slots]) => <li key={day} className="grid gap-2 md:grid-cols-[8rem_1fr]">
      <h3 className="text-sm font-bold">{weekday.format(new Date(`${day}T00:00:00Z`))}</h3>
      <ul className="grid gap-3 md:grid-cols-2">{slots.map((slot) => <SlotCard key={`${slot.id}-${slot.starts_at}-${slot.status}-${slot.project_slug ?? ""}-${slot.note ?? ""}`} slot={slot} timezone={view.timezone} shorts={shorts} canManage={canManage} onChanged={changed} onOpenVideo={onOpenVideo} />)}</ul>
    </li>)}</ol>
  </section>;
}
