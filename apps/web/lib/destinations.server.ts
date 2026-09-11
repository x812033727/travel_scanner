import { cache } from "react";

/**
 * Public destination data for the guide pages.
 *
 * `GET /api/v1/destinations` answers with the reader's locale already applied -- city name,
 * country label, area labels and the "why go" line all come back translated, for all 33
 * destinations in all five locales, checked upstream by validate_localized_catalog(). So these
 * pages do not need a translation table of their own for anything but section headings.
 *
 * Unlike the other *.server.ts helpers these responses are cached rather than `no-store`. None of
 * it is personalized, and going back to origin on every request lands straight in TTFB and
 * therefore in LCP. The catalog moves about once a quarter; rankings and merchant listings move
 * daily, so they get a shorter window.
 */

const CATALOG_TTL = 3600;
const LISTING_TTL = 900;

export type DestinationSummary = {
  id: string;
  city: string;
  localName: string | null;
  englishName: string | null;
  country: string;
  countryCode: string;
  role: "primary" | "secondary" | "extension";
  parentDestinationId: string | null;
  extensionIds: string[];
  areas: string[];
  recommendedDays: { min: number; max: number } | null;
  timezone: string;
  currency: string;
  center: { latitude: number; longitude: number } | null;
  reason: string;
};

export type GuideEntry = { id: string; name: string; detail: string | null };

function apiBase() {
  return (process.env.API_INTERNAL_URL || "http://localhost:8000").replace(/\/$/, "");
}

async function fetchJson(path: string, locale: string, revalidate: number): Promise<unknown | null> {
  try {
    const response = await fetch(`${apiBase()}/api/v1${path}`, {
      next: { revalidate },
      headers: { Accept: "application/json", "X-Travel-Locale": locale },
    });
    if (!response.ok) return null;
    return (await response.json()) as unknown;
  } catch {
    // The pages decide what a miss means: the index degrades to the offline catalog, a guide
    // without its own record refuses to render a blank document.
    return null;
  }
}

const text = (value: unknown) => (typeof value === "string" && value.trim() ? value.trim() : null);

function toSummary(value: unknown): DestinationSummary | null {
  if (typeof value !== "object" || value === null) return null;
  const row = value as Record<string, unknown>;
  const id = text(row.id);
  const city = text(row.city);
  if (!id || !city) return null;
  const days = (row.recommended_days ?? {}) as Record<string, unknown>;
  const center = row.center as Record<string, unknown> | null;
  const role = row.role === "secondary" || row.role === "extension" ? row.role : "primary";
  return {
    id,
    city,
    localName: text(row.local_name),
    englishName: text(row.english_name),
    country: text(row.country) ?? "",
    countryCode: text(row.country_code) ?? "",
    role,
    parentDestinationId: text(row.parent_destination_id),
    extensionIds: Array.isArray(row.extension_ids) ? row.extension_ids.filter((value): value is string => typeof value === "string") : [],
    areas: Array.isArray(row.areas) ? row.areas.map(text).filter((value): value is string => value !== null) : [],
    // Null rather than zeroes: a partial `{min: 3}` used to render "3–0 days" on the
    // destination index, which guards on min alone. Absent and zero are different facts.
    recommendedDays:
      typeof days.min === "number" && typeof days.max === "number"
        ? { min: days.min, max: days.max }
        : null,
    timezone: text(row.timezone) ?? "",
    currency: text(row.currency) ?? "",
    center:
      center && typeof center.latitude === "number" && typeof center.longitude === "number"
        ? { latitude: center.latitude, longitude: center.longitude }
        : null,
    reason: text(row.reason) ?? "",
  };
}

export async function loadDestinations(locale: string): Promise<DestinationSummary[] | null> {
  const payload = (await fetchJson("/destinations", locale, CATALOG_TTL)) as Record<string, unknown> | null;
  const items = payload?.items;
  if (!Array.isArray(items)) return null;
  const rows = items.map(toSummary).filter((row): row is DestinationSummary => row !== null);
  return rows.length ? rows : null;
}

export async function loadDestination(locale: string, id: string): Promise<DestinationSummary | null> {
  const rows = await loadDestinations(locale);
  return rows?.find((row) => row.id === id) ?? null;
}

/** Top reviewed places, server-rendered so the list is in the HTML rather than fetched on mount. */
export async function loadPlaces(locale: string, id: string): Promise<GuideEntry[]> {
  const payload = (await fetchJson(`/hotspots/rankings?destination_id=${encodeURIComponent(id)}&limit=12`, locale, LISTING_TTL)) as Record<string, unknown> | null;
  const items = Array.isArray(payload?.items) ? payload.items : [];
  return items
    .map((item, index) => {
      if (typeof item !== "object" || item === null) return null;
      const row = item as Record<string, unknown>;
      const name = text(row.name);
      if (!name) return null;
      const area = row.area as Record<string, unknown> | null;
      // Chains share a name within one city, so the name is not a usable React key.
      return { id: text(row.id) ?? `${name}-${index}`, name, detail: text(area?.name) ?? text(row.category) };
    })
    .filter((entry): entry is GuideEntry => entry !== null);
}

export async function loadMerchants(locale: string, id: string): Promise<GuideEntry[]> {
  const payload = (await fetchJson(`/foods/merchants?destination_id=${encodeURIComponent(id)}&limit=12`, locale, LISTING_TTL)) as Record<string, unknown> | null;
  const items = Array.isArray(payload?.items) ? payload.items : [];
  return items
    .map((item, index) => {
      if (typeof item !== "object" || item === null) return null;
      const row = item as Record<string, unknown>;
      const name = text(row.name);
      if (!name) return null;
      const area = row.area as Record<string, unknown> | null;
      const categories = Array.isArray(row.categories) ? row.categories : [];
      const first = categories[0] as Record<string, unknown> | undefined;
      return { id: text(row.id) ?? `${name}-${index}`, name, detail: text(area?.name) ?? text(first?.name) };
    })
    .filter((entry): entry is GuideEntry => entry !== null);
}

export const getDestinations = cache(loadDestinations);
export const getDestination = cache(loadDestination);
export const getGuidePlaces = cache(loadPlaces);
export const getGuideMerchants = cache(loadMerchants);
