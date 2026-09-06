import { api } from "@/lib/api";

/**
 * Public holidays for the three markets the product plans trips between.
 *
 * The API answers from a calendar vendored in the repository — no key, no upstream call —
 * and has already put every name in the reader's language, so nothing here belongs in the
 * message catalogue. A country the API does not cover simply returns nothing.
 */
export type HolidayKind = "public_holiday" | "substitute" | "bridge_holiday" | "makeup_workday";

export type Holiday = {
  date: string;
  key: string;
  kind: HolidayKind;
  is_working_day: boolean;
  name: string;
  country: string;
  country_name: string;
  source: string;
};

export type HolidayCalendar = {
  country: string;
  country_name: string;
  locale: string;
  coverage_start: string | null;
  coverage_end: string | null;
  attribution: string;
  holidays: Holiday[];
};

/** The markets with a vendored calendar; anything else answers 404. */
export const holidayCountries = ["TW", "JP", "KR"] as const;

export async function holidayCalendar(country: string, from: string, to: string): Promise<HolidayCalendar> {
  const query = new URLSearchParams({ country, from, to });
  return api<HolidayCalendar>(`/holidays?${query.toString()}`);
}

/**
 * One request per country, and a country that fails is left out rather than taking the
 * calendar down with it: a missing dot is a smaller failure than a picker that will not open.
 */
export async function holidayCalendars(countries: readonly string[], from: string, to: string): Promise<HolidayCalendar[]> {
  const settled = await Promise.allSettled(countries.map((country) => holidayCalendar(country, from, to)));
  return settled.flatMap((result) => (result.status === "fulfilled" ? [result.value] : []));
}

/** Every holiday of every calendar, keyed by ISO day, in the order the countries were asked for. */
export function holidaysByDate(calendars: HolidayCalendar[]): Map<string, Holiday[]> {
  const byDate = new Map<string, Holiday[]>();
  for (const calendar of calendars) {
    for (const holiday of calendar.holidays) {
      byDate.set(holiday.date, [...(byDate.get(holiday.date) || []), holiday]);
    }
  }
  return byDate;
}

/** "日本 憲法紀念日, 臺灣 勞動節" — what a screen reader adds to the day's own label. */
export function holidayLabel(holidays: Holiday[] | undefined): string | undefined {
  if (!holidays?.length) return undefined;
  return holidays.map((holiday) => `${holiday.country_name} ${holiday.name}`).join(", ");
}

/** Locale to the market a reader most likely takes leave in. English and Simplified have none. */
const HOME_MARKETS: Record<string, string> = { "zh-TW": "TW", ja: "JP", ko: "KR" };

/**
 * Whose holidays a trip cares about: the country being travelled to, and the reader's own
 * market. A destination the catalogue does not recognise leaves every market marked, which
 * is the honest answer while the form only knows what the traveller typed.
 */
export function holidayCountriesFor(
  destinationName: string,
  locale: string,
  cities: readonly { id: string; country: string; name: string }[],
): readonly string[] {
  const typed = destinationName.trim().toLowerCase();
  const supported: readonly string[] = holidayCountries;
  const match = typed.length >= 2
    ? cities.find((city) => {
      const name = city.name.trim().toLowerCase();
      return typed.includes(city.id) || (name.length >= 2 && (typed.includes(name) || name.includes(typed)));
    })
    : undefined;
  if (!match || !supported.includes(match.country)) return holidayCountries;
  const home = HOME_MARKETS[locale];
  return home && home !== match.country ? [match.country, home] : [match.country];
}
