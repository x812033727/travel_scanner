export type ThemeKind = "season" | "shop";
export type HotspotTheme = { slug: string; kind: ThemeKind; name: string; months: number[] };
export type ThemeFacet = HotspotTheme & { count: number };

// Any leap year works; the 15th at noon UTC stays inside the month in every time zone.
const ANCHOR_YEAR = 2024;

/** Sorted, de-duplicated months in 1–12; anything else is dropped. */
export function normalizeMonths(months: readonly number[] | null | undefined): number[] {
  const clean = (months ?? []).filter((month) => Number.isInteger(month) && month >= 1 && month <= 12);
  return [...new Set(clean)].sort((first, second) => first - second);
}

/**
 * Contiguous runs of months. A run ending in December joins one starting in January,
 * so an illumination season of [11, 12, 1, 2] reads as one span rather than two.
 */
export function monthRuns(months: readonly number[]): number[][] {
  const runs: number[][] = [];
  for (const month of normalizeMonths(months)) {
    const last = runs[runs.length - 1];
    if (last && last[last.length - 1] === month - 1) last.push(month);
    else runs.push([month]);
  }
  const first = runs[0];
  const tail = runs[runs.length - 1];
  if (runs.length > 1 && first[0] === 1 && tail[tail.length - 1] === 12) {
    runs.pop();
    runs[0] = [...tail, ...first];
  }
  return runs;
}

/**
 * "3月–4月" in Chinese, Japanese and Korean, "Mar–Apr" in English; separate runs join
 * with a middle dot. Empty for no months and for all twelve, so the caller decides
 * between saying nothing and saying "all year".
 */
export function monthRangeLabel(months: readonly number[], locale: string): string {
  const runs = monthRuns(months);
  if (!runs.length || runs.flat().length === 12) return "";
  const format = new Intl.DateTimeFormat(locale, { month: "short", timeZone: "UTC" });
  const name = (month: number) => format.format(new Date(Date.UTC(ANCHOR_YEAR, month - 1, 15, 12)));
  return runs
    .map((run) => (run.length === 1 ? name(run[0]) : `${name(run[0])}–${name(run[run.length - 1])}`))
    .join(" · ");
}

/** A season theme whose months include this month; shop types are never "in season". */
export function isInSeason(
  theme: Pick<HotspotTheme, "kind" | "months">,
  month = new Date().getMonth() + 1,
): boolean {
  return theme.kind === "season" && (theme.months ?? []).includes(month);
}
