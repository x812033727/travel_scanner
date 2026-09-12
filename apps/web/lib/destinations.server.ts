import { cache } from "react";
import { getTranslations } from "next-intl/server";
import { publicServerHeaders } from "@/lib/public-server-fetch";

/**
 * Public destination data for the guide pages.
 *
 * `GET /api/v1/destinations` answers with the reader's locale already applied -- city name,
 * country label, area labels and the "why go" line all come back translated, for all 33
 * destinations in all five locales, checked upstream by validate_localized_catalog(). So these
 * pages do not need a translation table of their own for anything but section headings.
 *
 * Only the source-controlled destination catalog is cached across requests. Place and merchant
 * listings contain current moderation decisions, so those are always read fresh.
 */

const CATALOG_TTL = 3600;

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

async function fetchJson(path: string, locale: string, revalidate?: number): Promise<unknown | null> {
  try {
    // Only the uncached reads carry the visitor's address. A revalidated response is shared
    // between readers, and a per-visitor header would split it into one entry each; reading
    // the request at all would also stop the page that depends on it rendering statically.
    // The catalogue behind those reads is a fixed list of cities, which is not worth metering.
    const response = await fetch(`${apiBase()}/api/v1${path}`, {
      ...(revalidate === undefined ? { cache: "no-store" as const } : { next: { revalidate } }),
      signal: AbortSignal.timeout(3000),
      headers:
        revalidate === undefined
          ? await publicServerHeaders(locale)
          : { Accept: "application/json", "X-Travel-Locale": locale },
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
  const rows = await getDestinations(locale);
  return rows?.find((row) => row.id === id) ?? null;
}

/** Top reviewed places, server-rendered so the list is in the HTML rather than fetched on mount. */
export async function loadPlaces(locale: string, id: string): Promise<GuideEntry[] | null> {
  const [payload, t] = await Promise.all([
    fetchJson(`/hotspots/rankings?destination_id=${encodeURIComponent(id)}&limit=12`, locale) as Promise<Record<string, unknown> | null>,
    getTranslations({ locale, namespace: "hotspots" }),
  ]);
  if (!Array.isArray(payload?.items)) return null;
  const items = payload.items;
  return items
    .map((item, index) => {
      if (typeof item !== "object" || item === null) return null;
      const row = item as Record<string, unknown>;
      const name = text(row.name);
      if (!name) return null;
      const area = row.area as Record<string, unknown> | null;
      // Chains share a name within one city, so the name is not a usable React key.
      const category = text(row.category);
      const categoryLabel = category && t.has(`categories.${category}`) ? t(`categories.${category}`) : null;
      return { id: text(row.id) ?? `${name}-${index}`, name, detail: text(area?.name) ?? categoryLabel };
    })
    .filter((entry): entry is GuideEntry => entry !== null);
}

export async function loadMerchants(locale: string, id: string): Promise<GuideEntry[] | null> {
  const payload = (await fetchJson(`/foods/merchants?destination_id=${encodeURIComponent(id)}&limit=12`, locale)) as Record<string, unknown> | null;
  if (!Array.isArray(payload?.items)) return null;
  const items = payload.items;
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
