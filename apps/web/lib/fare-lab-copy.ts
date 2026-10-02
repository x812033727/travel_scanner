import en from "./fare-lab-messages/en.json";
import ja from "./fare-lab-messages/ja.json";
import ko from "./fare-lab-messages/ko.json";
import zhCN from "./fare-lab-messages/zh-CN.json";
import zhTW from "./fare-lab-messages/zh-TW.json";
import { formatDateTime } from "@/lib/locale-format";
import { translateWarnings } from "@/lib/warnings";

/**
 * The airline fare lab's copy, for its three screens: public fares, back-to-back and
 * live back-to-back.
 *
 * A feature catalog rather than a `messages/` namespace, the way itinerary-copy is: the
 * lab is one of the features the owner keeps closed, and a namespace would put its
 * keys into the shared catalogs every other change edits. TypeScript checks that each
 * locale has every key; fare-lab-copy.test.ts checks the placeholders.
 */
export type FareLabCopy = Record<keyof typeof en, string>;
export type FareLabKey = keyof FareLabCopy;

const catalogs: Record<string, FareLabCopy> = { en, ja, ko, "zh-TW": zhTW, "zh-CN": zhCN };

export function fareLabCopy(locale: string): FareLabCopy {
  return catalogs[locale] || en;
}

export function fareLabText(text: string, values: Record<string, string | number> = {}) {
  return text.replace(/\{(\w+)\}/g, (match, key: string) => String(values[key] ?? match));
}

/**
 * Copy for a key built from a value the API sent (an airline code, a ticket role, a
 * city), or undefined when this build has none for it, so the caller can fall back to
 * the value itself rather than print a key.
 */
export function fareLabLabel(copy: FareLabCopy, key: string): string | undefined {
  return Object.hasOwn(copy, key) ? copy[key as FareLabKey] : undefined;
}

/** The airline's name in the reader's language; the one the API sends is Chinese. */
export function airlineName(copy: FareLabCopy, code: string, fallback?: string) {
  return fareLabLabel(copy, `airline.${code}`) ?? fallback ?? code;
}

export function cityName(copy: FareLabCopy, code: string) {
  return fareLabLabel(copy, `city.${code}`) ?? code;
}

type Option = { value: string; label: string };

/** The choices every fare form in the lab offers, in the same order. */
export function originOptions(copy: FareLabCopy): Option[] {
  return ["TPE", "TSA"].map((code) => ({ value: code, label: `${cityName(copy, code)} ${code}` }));
}

export function flexOptions(copy: FareLabCopy): Option[] {
  return ["0", "3", "7", "14"].map((days) => ({
    value: days,
    label: days === "0" ? copy["flex.exact"] : fareLabText(copy["flex.around"], { days }),
  }));
}

export function cabinOptions(copy: FareLabCopy): Option[] {
  return (["economy", "premium_economy", "business", "first"] as const).map((cabin) => ({
    value: cabin,
    label: copy[`cabin.${cabin}`],
  }));
}

/** A fare's travel date, which is a calendar day and so is formatted in UTC. */
export function fareDate(value?: string) {
  if (!value) return "—";
  return formatDateTime(`${value}T00:00:00Z`, { year: "numeric", month: "short", day: "numeric", timeZone: "UTC" });
}

const WARNING = "warning.";
const KNOWN_WARNINGS = new Set(
  Object.keys(en).filter((key) => key.startsWith(WARNING)).map((key) => key.slice(WARNING.length)),
);

/**
 * The API's warnings for these screens, in the reader's language.
 *
 * They arrive as codes (`fare_page_unavailable?airline=CI&page=reverse`), and some of
 * their values are themselves things to name: the airline, which ticket, which page.
 * `roles` says whose ticket names to use, because the live comparison calls its five
 * tickets something different from the cached one's four. Free text from an older
 * response or another source passes through untouched; see lib/warnings.ts.
 */
export function fareLabWarnings(
  warnings: readonly string[] | undefined,
  copy: FareLabCopy,
  roles: "ticketRole" | "liveRole",
): string[] {
  return translateWarnings(warnings, KNOWN_WARNINGS, (key, values = {}) => {
    const named: Record<string, string> = { ...values };
    if (values.airline) named.airline = fareLabLabel(copy, `airline.${values.airline}`) ?? values.airline;
    if (values.role) named.role = fareLabLabel(copy, `${roles}.${values.role}`) ?? values.role;
    if (values.page) named.page = fareLabLabel(copy, `page.${values.page}`) ?? values.page;
    return fareLabText(fareLabLabel(copy, key) ?? key, named);
  });
}
