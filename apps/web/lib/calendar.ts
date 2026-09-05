// Day-level date helpers for the trip calendar. Every value is an ISO day
// ("YYYY-MM-DD") or month ("YYYY-MM") string, which compare correctly with
// plain string operators; Date objects only exist in UTC for arithmetic so a
// traveller west of UTC never sees a day shift.

export type WeekStart = 1 | 7;

const DAY_MS = 86_400_000;

export function parseDay(iso: string): Date {
  return new Date(`${iso}T00:00:00Z`);
}

export function isoDay(date: Date): string {
  return date.toISOString().slice(0, 10);
}

export function addDays(iso: string, delta: number): string {
  const date = parseDay(iso);
  date.setUTCDate(date.getUTCDate() + delta);
  return isoDay(date);
}

export function dayCount(start: string, end: string): number {
  if (!start || !end || end < start) return 0;
  return Math.round((parseDay(end).getTime() - parseDay(start).getTime()) / DAY_MS) + 1;
}

export function monthOf(iso: string): string {
  return iso.slice(0, 7);
}

function monthParts(month: string): [number, number] {
  const [year, monthNumber] = month.split("-").map(Number);
  return [year, monthNumber];
}

function padDay(month: string, day: number): string {
  return `${month}-${String(day).padStart(2, "0")}`;
}

export function addMonths(month: string, delta: number): string {
  const [year, monthNumber] = monthParts(month);
  return monthOf(isoDay(new Date(Date.UTC(year, monthNumber - 1 + delta, 1))));
}

export function daysInMonth(month: string): number {
  const [year, monthNumber] = monthParts(month);
  return new Date(Date.UTC(year, monthNumber, 0)).getUTCDate();
}

export function clampToMonth(iso: string, month: string): string {
  return padDay(month, Math.min(Number(iso.slice(8, 10)), daysInMonth(month)));
}

export function monthGrid(month: string, weekStart: WeekStart): (string | null)[][] {
  const [year, monthNumber] = monthParts(month);
  const firstWeekday = new Date(Date.UTC(year, monthNumber - 1, 1)).getUTCDay();
  const leading = (firstWeekday - (weekStart % 7) + 7) % 7;
  const cells: (string | null)[] = Array.from({ length: leading }, () => null);
  const total = daysInMonth(month);
  for (let day = 1; day <= total; day += 1) cells.push(padDay(month, day));
  while (cells.length % 7) cells.push(null);
  const rows: (string | null)[][] = [];
  for (let index = 0; index < cells.length; index += 7) rows.push(cells.slice(index, index + 7));
  return rows;
}

// CLDR first day of the week for the app's locales. A fixed map keeps every
// browser in agreement; Intl.Locale week info is missing in Firefox and Node.
export function weekStartFor(locale: string): WeekStart {
  return locale === "zh-CN" ? 1 : 7;
}

export function weekdayLabels(locale: string, weekStart: WeekStart): { short: string; long: string }[] {
  const short = new Intl.DateTimeFormat(locale, { weekday: "short", timeZone: "UTC" });
  const long = new Intl.DateTimeFormat(locale, { weekday: "long", timeZone: "UTC" });
  // 2024-01-07 is a Sunday.
  return Array.from({ length: 7 }, (_, index) => {
    const date = parseDay(addDays("2024-01-07", (weekStart % 7) + index));
    return { short: short.format(date), long: long.format(date) };
  });
}

export function monthTitle(locale: string, month: string): string {
  return new Intl.DateTimeFormat(locale, { year: "numeric", month: "long", timeZone: "UTC" }).format(parseDay(`${month}-01`));
}

export function tripDayFormatter(locale: string): Intl.DateTimeFormat {
  return new Intl.DateTimeFormat(locale, { year: "numeric", month: "long", day: "numeric", weekday: "short", timeZone: "UTC" });
}

export function formatTripDay(locale: string, iso: string): string {
  return iso ? tripDayFormatter(locale).format(parseDay(iso)) : "";
}
