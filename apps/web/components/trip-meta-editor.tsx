"use client";

import { CalendarDays, CircleAlert, Edit3, Loader2, Save } from "lucide-react";
import { useTranslations } from "next-intl";
import { useMemo, useState } from "react";
import { PlannerOverlay } from "@/components/planner-overlay";
import { api, ApiError } from "@/lib/api";
import type { Trip, TripStatus } from "@/lib/trip-types";

const DAY_MS = 86_400_000;
const MAX_TRIP_DAYS = 61;
const STATUS_VALUES: readonly TripStatus[] = ["planning", "ready", "travelling", "closed"];

const fieldClass = "mt-2 min-h-11 w-full rounded-xl border border-[var(--line)] bg-white px-3 py-2.5 text-sm text-[var(--ink)] outline-none transition focus:border-[var(--teal)] focus:ring-4 focus:ring-[var(--teal-soft)]";

function isoDays(start?: string | null, end?: string | null): string[] {
  if (!start || !end || end < start) return [];
  const days: string[] = [];
  const cursor = new Date(`${start}T00:00:00Z`);
  const last = new Date(`${end}T00:00:00Z`);
  while (cursor <= last && days.length < 62) {
    days.push(cursor.toISOString().slice(0, 10));
    cursor.setUTCDate(cursor.getUTCDate() + 1);
  }
  return days;
}

function spanDays(start: string, end: string): number {
  return Math.round((Date.parse(`${end}T00:00:00Z`) - Date.parse(`${start}T00:00:00Z`)) / DAY_MS) + 1;
}

/** Rows a shrink would destroy that the traveller created, mirroring the API's protected classification. */
function ownArrangements(trip: Trip, droppedDays: string[]): number {
  if (!droppedDays.length) return 0;
  const dropped = new Set(droppedDays);
  return trip.items.filter((item) => {
    if (!dropped.has(item.day_date)) return false;
    if (!item.system_role) return true;
    if (item.system_role === "lunch" || item.system_role === "dinner") {
      return item.data.meal_selection_source === "user";
    }
    if (item.system_role === "outbound_flight" || item.system_role === "return_flight") {
      return Boolean(item.data.flight_info);
    }
    return false;
  }).length;
}

function bookedFlightDays(trip: Trip): { outbound?: string; back?: string } {
  const result: { outbound?: string; back?: string } = {};
  for (const item of trip.items) {
    if (!item.data.flight_info) continue;
    if (item.system_role === "outbound_flight") result.outbound = item.day_date;
    if (item.system_role === "return_flight") result.back = item.day_date;
  }
  return result;
}

export function TripMetaEditor({
  trip,
  variant,
  disabled = false,
  prepare,
  onUpdated,
}: {
  trip: Trip;
  variant: "hero" | "tools";
  disabled?: boolean;
  /** Flush pending itinerary edits first; resolves to the fresh trip, or undefined when blocked by a conflict. */
  prepare?: () => Promise<Trip | undefined>;
  onUpdated: (updated: Trip) => void;
}) {
  const t = useTranslations("trips");
  const [open, setOpen] = useState(false);
  const [name, setName] = useState(trip.name);
  const [status, setStatus] = useState<TripStatus>(trip.status || "planning");
  const [dateMode, setDateMode] = useState<"range" | "shift">("range");
  const [start, setStart] = useState(trip.start_date || "");
  const [end, setEnd] = useState(trip.end_date || "");
  const [shiftStart, setShiftStart] = useState(trip.start_date || "");
  const [confirmRemoval, setConfirmRemoval] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string>();

  const hasDates = Boolean(trip.start_date && trip.end_date);
  const currentDays = useMemo(() => isoDays(trip.start_date, trip.end_date), [trip.start_date, trip.end_date]);

  const shiftDays = dateMode === "shift" && hasDates && shiftStart && trip.start_date
    ? Math.round((Date.parse(`${shiftStart}T00:00:00Z`) - Date.parse(`${trip.start_date}T00:00:00Z`)) / DAY_MS)
    : 0;
  const rangeChanged = dateMode === "range" && Boolean(start && end)
    && (start !== (trip.start_date || "") || end !== (trip.end_date || ""));
  const datesChanged = dateMode === "shift" ? shiftDays !== 0 : rangeChanged;
  const rangeInvalid = dateMode === "range" && Boolean(start && end) && end < start;
  const rangeTooLong = dateMode === "range" && Boolean(start && end) && !rangeInvalid
    && spanDays(start, end) > MAX_TRIP_DAYS;
  const droppedDays = useMemo(() => {
    if (!datesChanged || dateMode !== "range" || rangeInvalid) return [];
    return currentDays.filter((day) => day < start || day > end);
  }, [currentDays, dateMode, datesChanged, end, rangeInvalid, start]);
  const droppedArrangements = useMemo(() => ownArrangements(trip, droppedDays), [droppedDays, trip]);
  const flightDays = useMemo(() => bookedFlightDays(trip), [trip]);
  const flightsReset = datesChanged && (
    dateMode === "shift"
      ? Boolean(flightDays.outbound || flightDays.back)
      : Boolean(
        (flightDays.outbound && start !== trip.start_date) || (flightDays.back && end !== trip.end_date),
      )
  );
  const routesReset = datesChanged && Boolean(trip.route_segments?.length);
  // The API refuses both a shrink and a flight reset without confirm_removed_days:
  // a pure extension that re-dates the return flight clears a hand-typed booking
  // just as irreversibly as a dropped day deletes its plans.
  const needsConfirmation = droppedDays.length > 0 || flightsReset;

  const nameChanged = name.trim().length > 0 && name.trim() !== trip.name;
  const statusChanged = status !== (trip.status || "planning");
  const anythingChanged = nameChanged || statusChanged || datesChanged;
  const blocked = rangeInvalid || rangeTooLong || (needsConfirmation && !confirmRemoval);

  function openEditor() {
    setName(trip.name);
    setStatus(trip.status || "planning");
    setDateMode("range");
    setStart(trip.start_date || "");
    setEnd(trip.end_date || "");
    setShiftStart(trip.start_date || "");
    setConfirmRemoval(false);
    setError(undefined);
    setOpen(true);
  }

  async function submit() {
    if (busy || blocked) return;
    if (!anythingChanged) {
      setOpen(false);
      return;
    }
    setBusy(true);
    setError(undefined);
    try {
      let base: Trip | undefined = trip;
      if (prepare) base = await prepare();
      if (!base) {
        setError(t("meta.conflictBlocked"));
        return;
      }
      const body: Record<string, unknown> = { version: base.version };
      if (nameChanged) body.name = name.trim();
      if (statusChanged) body.status = status;
      if (datesChanged && dateMode === "shift") body.shift_days = shiftDays;
      if (datesChanged && dateMode === "range") {
        body.start_date = start;
        body.end_date = end;
      }
      if (needsConfirmation) body.confirm_removed_days = true;
      const updated = await api<Trip>(`/trips/${trip.id}`, {
        method: "PATCH",
        body: JSON.stringify(body),
      });
      onUpdated(updated);
      setOpen(false);
    } catch (reason) {
      if (reason instanceof ApiError && reason.code === "trip_version_conflict") {
        setError(t("meta.conflictBlocked"));
      } else if (reason instanceof ApiError && reason.code === "trip_shrink_confirmation_required") {
        // The local preview and the server disagreed about what the change destroys;
        // say so in the reader's language instead of echoing the Chinese detail.
        setError(t("meta.confirmRequired"));
      } else {
        setError(reason instanceof Error ? reason.message : String(reason));
      }
    } finally {
      setBusy(false);
    }
  }

  const trigger = variant === "hero"
    ? <button
        type="button"
        aria-label={t("meta.edit")}
        title={t("meta.edit")}
        onClick={openEditor}
        disabled={disabled}
        className="grid h-9 w-9 shrink-0 place-items-center rounded-xl border border-[var(--line)] bg-white/75 text-[var(--muted)] transition hover:text-[var(--ink)] disabled:opacity-40"
      >
        <Edit3 size={16} />
      </button>
    : <button
        type="button"
        onClick={openEditor}
        disabled={disabled}
        className="flex min-h-12 w-full items-center justify-between gap-3 rounded-xl border border-[var(--line)] bg-white px-4 py-3 text-left disabled:opacity-40"
      >
        <span className="min-w-0">
          <strong className="block text-sm">{t("meta.toolsTitle")}</strong>
          <span className="mt-0.5 block text-xs text-[var(--muted)]">{t("meta.toolsDescription")}</span>
        </span>
        <Edit3 size={17} className="shrink-0 text-[var(--muted)]" />
      </button>;

  return <>
    {trigger}
    <PlannerOverlay
      open={open}
      onClose={() => { if (!busy) setOpen(false); }}
      title={t("meta.title")}
      description={t("meta.description")}
      footer={<div className="flex gap-3">
        <button
          type="button"
          onClick={() => setOpen(false)}
          disabled={busy}
          className="min-h-12 flex-1 rounded-xl border border-[var(--line)] font-semibold disabled:opacity-40"
        >
          {t("meta.cancel")}
        </button>
        <button
          type="button"
          onClick={() => void submit()}
          disabled={busy || blocked || !anythingChanged}
          className="flex min-h-12 flex-[1.4] items-center justify-center gap-2 rounded-xl bg-[var(--teal)] px-4 font-semibold text-white disabled:opacity-45"
        >
          {busy ? <Loader2 size={17} className="animate-spin" /> : <Save size={17} />}
          {busy ? t("meta.saving") : t("meta.save")}
        </button>
      </div>}
    >
      <div className="grid gap-5">
        <label className="text-sm font-semibold">
          {t("meta.nameLabel")}
          <input
            value={name}
            maxLength={255}
            onChange={(event) => setName(event.target.value)}
            className={fieldClass}
          />
        </label>
        <label className="text-sm font-semibold">
          {t("meta.statusLabel")}
          <select
            value={status}
            onChange={(event) => setStatus(event.target.value as TripStatus)}
            className={fieldClass}
          >
            {STATUS_VALUES.map((value) => (
              <option key={value} value={value}>{t(`meta.status.${value}`)}</option>
            ))}
          </select>
        </label>
        <fieldset className="rounded-2xl border border-[var(--line)] bg-[var(--paper)]/60 p-4">
          <legend className="flex items-center gap-1.5 px-1 text-sm font-bold">
            <CalendarDays size={15} />
            {t("meta.datesLegend")}
          </legend>
          {hasDates && <div className="mb-3 grid grid-cols-2 gap-2" role="radiogroup" aria-label={t("meta.datesLegend")}>
            <button
              type="button"
              role="radio"
              aria-checked={dateMode === "range"}
              onClick={() => setDateMode("range")}
              className={`min-h-11 rounded-xl border px-3 text-sm font-bold ${dateMode === "range" ? "border-[var(--teal)] bg-[var(--teal-soft)] text-[var(--teal-dark)]" : "border-[var(--line)] bg-white"}`}
            >
              {t("meta.modeRange")}
            </button>
            <button
              type="button"
              role="radio"
              aria-checked={dateMode === "shift"}
              onClick={() => setDateMode("shift")}
              className={`min-h-11 rounded-xl border px-3 text-sm font-bold ${dateMode === "shift" ? "border-[var(--teal)] bg-[var(--teal-soft)] text-[var(--teal-dark)]" : "border-[var(--line)] bg-white"}`}
            >
              {t("meta.modeShift")}
            </button>
          </div>}
          {dateMode === "range" && <>
            <p className="mb-3 text-xs leading-5 text-[var(--muted)]">{t("meta.modeRangeHint")}</p>
            <div className="grid grid-cols-2 gap-3">
              <label className="text-sm font-semibold">
                {t("meta.startDate")}
                <input type="date" value={start} onChange={(event) => { setStart(event.target.value); setConfirmRemoval(false); }} className={fieldClass} />
              </label>
              <label className="text-sm font-semibold">
                {t("meta.endDate")}
                <input type="date" value={end} onChange={(event) => { setEnd(event.target.value); setConfirmRemoval(false); }} className={fieldClass} />
              </label>
            </div>
          </>}
          {dateMode === "shift" && <>
            <p className="mb-3 text-xs leading-5 text-[var(--muted)]">{t("meta.modeShiftHint")}</p>
            <label className="text-sm font-semibold">
              {t("meta.shiftStart")}
              <input type="date" value={shiftStart} onChange={(event) => setShiftStart(event.target.value)} className={fieldClass} />
            </label>
            <p className="mt-2 text-xs text-[var(--muted)]">{t("meta.lengthNote", { days: currentDays.length })}</p>
          </>}
          {rangeInvalid && <p role="alert" className="mt-3 rounded-xl bg-red-50 px-3 py-2 text-xs font-semibold text-red-800">{t("meta.rangeInvalid")}</p>}
          {rangeTooLong && <p role="alert" className="mt-3 rounded-xl bg-red-50 px-3 py-2 text-xs font-semibold text-red-800">{t("meta.rangeTooLong")}</p>}
        </fieldset>
        {needsConfirmation && <section role="alert" className="rounded-2xl border border-amber-200 bg-amber-50 p-4 text-sm text-amber-950">
          {droppedDays.length > 0 && <>
            <p className="flex items-start gap-2 font-semibold">
              <CircleAlert size={17} className="mt-0.5 shrink-0" />
              {t("meta.removedWarning", { days: droppedDays.length, items: droppedArrangements })}
            </p>
            <p className="mt-2 text-xs leading-5">{droppedDays.join(" · ")}</p>
          </>}
          {flightsReset && <p className={`flex items-start gap-2 font-semibold${droppedDays.length > 0 ? " mt-3" : ""}`}>
            <CircleAlert size={17} className="mt-0.5 shrink-0" />
            {t("meta.flightNotice")}
          </p>}
          <label className="mt-3 flex min-h-11 items-center gap-2 text-sm font-semibold">
            <input
              type="checkbox"
              checked={confirmRemoval}
              onChange={(event) => setConfirmRemoval(event.target.checked)}
              className="h-4 w-4"
            />
            {droppedDays.length > 0 ? t("meta.removedConfirm") : t("meta.flightConfirm")}
          </label>
        </section>}
        {routesReset && <p className="rounded-xl bg-[var(--paper)] px-3 py-2.5 text-xs leading-5 text-[var(--muted)]">{t("meta.routesNotice")}</p>}
        {error && <p role="alert" className="rounded-xl bg-red-50 px-3 py-2.5 text-sm font-semibold text-red-800">{error}</p>}
      </div>
    </PlannerOverlay>
  </>;
}
