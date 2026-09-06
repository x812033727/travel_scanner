"use client";

import { ChevronLeft, ChevronRight } from "lucide-react";
import { useLocale, useTranslations } from "next-intl";
import { useEffect, useId, useMemo, useRef, useState } from "react";
import { addDays, addMonths, clampToMonth, dayCount, monthGrid, monthOf, monthTitle, parseDay, tripDayFormatter, weekStartFor, weekdayLabels } from "@/lib/calendar";
import { HolidayCalendar, holidayCalendars, holidayCountries, holidayLabel, holidaysByDate } from "@/lib/holidays";

export type DateRange = { start: string; end: string };

const keyDeltas = new Map<string, number>([["ArrowLeft", -1], ["ArrowRight", 1], ["ArrowUp", -7], ["ArrowDown", 7]]);

// Selected days use --teal-fill rather than --teal: the dark-theme remap in
// globals.css only matches the bare `bg-[var(--teal)]` token, and --teal is a
// light colour in dark mode where white text would vanish.
// The holiday dot sits under the number, and turns white on a selected day where the teal
// one would vanish into the fill.
const holidayDot = "relative after:absolute after:bottom-1 after:hidden after:h-1 after:w-1 after:rounded-full after:bg-[var(--teal)] after:content-[''] data-[holiday=true]:after:block data-[range=edge]:after:bg-white";
const cellClass = "grid h-11 w-full place-items-center rounded-xl text-sm font-medium tabular-nums outline-none transition hover:bg-[var(--paper)] focus-visible:ring-4 focus-visible:ring-[var(--teal-soft)] aria-disabled:cursor-not-allowed aria-disabled:opacity-40 aria-disabled:hover:bg-transparent aria-[current=date]:font-bold aria-[current=date]:text-[var(--teal-dark)] data-[range=edge]:bg-[var(--teal-fill)] data-[range=edge]:font-semibold data-[range=edge]:text-white data-[range=inside]:bg-[var(--teal-soft)] data-[range=inside]:text-[var(--teal-dark)] data-[range=preview]:bg-[var(--teal-soft)]";

export function DateRangePicker({ start, end, today, maxDays, countries = holidayCountries, onChange }: DateRange & {
  today: string;
  maxDays: number;
  /** Whose public holidays to mark. Defaults to every market the API has a calendar for. */
  countries?: readonly string[];
  onChange: (range: DateRange) => void;
}) {
  const locale = useLocale();
  const t = useTranslations("newTrip.calendar");
  const titleId = useId();
  const statusId = useId();
  const gridRef = useRef<HTMLTableElement>(null);
  // Set by keyboard navigation so the effect below moves focus only then, not
  // when a pointer click or an external `start` change updates the cursor.
  const focusPending = useRef(false);
  const [monthOverride, setMonthOverride] = useState<string>();
  const [focusDay, setFocusDay] = useState<string>();
  const [hoverDay, setHoverDay] = useState<string>();
  const [gridFocused, setGridFocused] = useState(false);
  const [calendars, setCalendars] = useState<HolidayCalendar[]>([]);

  const todayMonth = monthOf(today);
  // Explicit navigation wins; otherwise follow the start date (a restored
  // draft sets it after mount) and fall back to the current month.
  const visibleMonth = monthOverride ?? monthOf(start || today);
  const weekStart = weekStartFor(locale);
  const headers = useMemo(() => weekdayLabels(locale, weekStart), [locale, weekStart]);
  const formatter = useMemo(() => tripDayFormatter(locale), [locale]);
  const rows = useMemo(() => monthGrid(visibleMonth, weekStart), [visibleMonth, weekStart]);
  const days = rows.flat().filter((day): day is string => day !== null);
  const canGoBack = visibleMonth > todayMonth;
  // While the end is still open, the latest day that keeps the trip within maxDays.
  const latestEnd = start && !end ? addDays(start, maxDays - 1) : undefined;

  function isAvailable(day: string) {
    return day >= today && (!latestEnd || day <= latestEnd);
  }

  const candidate = hoverDay ?? (gridFocused ? focusDay : undefined);
  const previewEnd = latestEnd && candidate && candidate >= start && isAvailable(candidate) ? candidate : undefined;
  const tabStop = [focusDay, start, today].find((day) => day && monthOf(day) === visibleMonth) ?? days.find(isAvailable) ?? days[0];

  // One request per country, once, covering every month the picker can reach. A national
  // calendar is a few dozen rows a year, and re-fetching while someone pages through months
  // would rewrite the grid under their pointer for no gain.
  const countryList = countries.join(",");
  useEffect(() => {
    if (!countryList) return;
    let current = true;
    void holidayCalendars(countryList.split(","), today, addDays(today, 730)).then((loaded) => {
      if (current) setCalendars(loaded);
    });
    return () => {
      current = false;
    };
  }, [countryList, today]);

  useEffect(() => {
    if (!focusPending.current || !focusDay) return;
    focusPending.current = false;
    gridRef.current?.querySelector<HTMLButtonElement>(`[data-date="${focusDay}"]`)?.focus();
  }, [focusDay]);

  function pick(day: string) {
    if (!isAvailable(day)) return;
    if (!start || end || day < start) onChange({ start: day, end: "" });
    else onChange({ start, end: day });
    setHoverDay(undefined);
    setFocusDay(day);
  }

  function goMonth(delta: -1 | 1) {
    const next = addMonths(visibleMonth, delta);
    if (next >= todayMonth) setMonthOverride(next);
  }

  function clear() {
    onChange({ start: "", end: "" });
    setMonthOverride(visibleMonth);
    setHoverDay(undefined);
  }

  function moveFocus(event: React.KeyboardEvent<HTMLButtonElement>, day: string) {
    let target: string | undefined;
    const delta = keyDeltas.get(event.key);
    if (delta !== undefined) target = addDays(day, delta);
    else if (event.key === "Home" || event.key === "End") {
      const offset = (parseDay(day).getUTCDay() - (weekStart % 7) + 7) % 7;
      target = addDays(day, event.key === "Home" ? -offset : 6 - offset);
    } else if (event.key === "PageUp" || event.key === "PageDown") {
      target = clampToMonth(day, addMonths(monthOf(day), event.key === "PageUp" ? -1 : 1));
    }
    if (!target) return;
    event.preventDefault();
    if (monthOf(target) < todayMonth) return;
    if (monthOf(target) !== visibleMonth) setMonthOverride(monthOf(target));
    focusPending.current = true;
    setFocusDay(target);
  }

  const holidays = useMemo(() => holidaysByDate(calendars), [calendars]);
  const attributions = calendars.filter((calendar) => calendar.holidays.length > 0).map((calendar) => calendar.attribution);
  const status = latestEnd
    ? t("pickEnd", { date: formatter.format(parseDay(latestEnd)) })
    : start && end
      ? t("selected", { start: formatter.format(parseDay(start)), end: formatter.format(parseDay(end)), days: dayCount(start, end) })
      : t("pickStart");

  return <div className="rounded-2xl border border-[var(--line)] bg-[var(--surface)] p-3">
    <div className="flex items-center justify-between gap-2">
      <button type="button" className="app-icon-button" aria-label={t("previousMonth")} disabled={!canGoBack} onClick={() => goMonth(-1)}><ChevronLeft size={18} aria-hidden="true" /></button>
      <p id={titleId} className="text-sm font-semibold">{monthTitle(locale, visibleMonth)}</p>
      <button type="button" className="app-icon-button" aria-label={t("nextMonth")} onClick={() => goMonth(1)}><ChevronRight size={18} aria-hidden="true" /></button>
    </div>
    <table ref={gridRef} role="grid" aria-labelledby={titleId} aria-describedby={statusId} onMouseLeave={() => setHoverDay(undefined)} onFocus={() => setGridFocused(true)} onBlur={(event) => { if (!event.currentTarget.contains(event.relatedTarget as Node | null)) setGridFocused(false); }} className="mt-2 w-full table-fixed border-separate border-spacing-0">
      <thead><tr>{headers.map((header) => <th key={header.long} scope="col" abbr={header.long} className="py-1 text-center text-xs font-semibold text-[var(--muted)]">{header.short}</th>)}</tr></thead>
      <tbody>{rows.map((row, rowIndex) => <tr key={rowIndex}>{row.map((day, columnIndex) => {
        if (!day) return <td key={`blank-${rowIndex}-${columnIndex}`} />;
        const edge = day === start || day === end;
        const inside = Boolean(start && end && day > start && day < end);
        const preview = Boolean(previewEnd && day > start && day <= previewEnd);
        const available = isAvailable(day);
        const named = holidayLabel(holidays.get(day));
        const dayLabel = formatter.format(parseDay(day));
        return <td key={day} className="p-0.5">
          <button type="button" data-date={day} data-holiday={named ? "true" : undefined} data-range={edge ? "edge" : inside ? "inside" : preview ? "preview" : undefined} tabIndex={day === tabStop ? 0 : -1} aria-label={named ? `${dayLabel} ${named}` : dayLabel} aria-pressed={edge || inside} aria-current={day === today ? "date" : undefined} aria-disabled={available ? undefined : true} onClick={() => pick(day)} onFocus={() => setFocusDay(day)} onMouseEnter={() => { if (latestEnd) setHoverDay(day); }} onKeyDown={(event) => moveFocus(event, day)} className={`${cellClass} ${holidayDot}`}>{Number(day.slice(8, 10))}</button>
        </td>;
      })}</tr>)}</tbody>
    </table>
    <div className="mt-2 flex items-start justify-between gap-3">
      <p id={statusId} role="status" className="text-sm text-[var(--muted)]">{status}</p>
      <button type="button" onClick={clear} disabled={!start && !end} className="shrink-0 text-sm font-semibold text-[var(--teal)] disabled:opacity-40">{t("clear")}</button>
    </div>
    {attributions.length > 0 && <p className="mt-2 break-all text-[11px] leading-4 text-[var(--muted)]">{attributions.join(" ")}</p>}
  </div>;
}
