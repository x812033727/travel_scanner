import { cache } from "react";

/**
 * The ranking the explorer used to fetch from the browser after hydration. On a
 * phone that left the flagship page showing "0 / 0 results" and a "sorting the
 * latest ranking" sentence for two to four seconds; the data is a public GET, so
 * the server can hand the first page over with the HTML.
 *
 * Both shapes stay `unknown` here on purpose: the component owns the types, and
 * everything this module promises is "either the API's payload or null".
 */
export type InitialHotspots = {
  ranking: unknown | null;
  facets: unknown | null;
};

export type HotspotFilters = {
  category?: string;
  destinationId?: string;
  area?: string;
};

const EMPTY: InitialHotspots = { ranking: null, facets: null };

async function fetchJson(url: string, locale: string): Promise<unknown | null> {
  try {
    const response = await fetch(url, {
      cache: "no-store",
      headers: { Accept: "application/json", "X-Travel-Locale": locale },
    });
    if (!response.ok) return null;
    return (await response.json()) as unknown;
  } catch {
    // The client fetches the same endpoints on mount, so a server-side miss costs
    // the reader the old blank first paint and nothing else.
    return null;
  }
}

export async function loadInitialHotspots(
  locale: string,
  filters: HotspotFilters = {},
): Promise<InitialHotspots> {
  const apiBase = (process.env.API_INTERNAL_URL || "http://localhost:8000").replace(/\/$/, "");
  const params = new URLSearchParams({ limit: "30" });
  if (filters.category) params.set("category", filters.category);
  if (filters.destinationId) params.set("destination_id", filters.destinationId);
  // An area only means something inside its destination, exactly as on the client.
  if (filters.destinationId && filters.area) params.set("area", filters.area);
  const [ranking, facets] = await Promise.all([
    fetchJson(`${apiBase}/api/v1/hotspots/rankings?${params}`, locale),
    fetchJson(`${apiBase}/api/v1/hotspots/facets`, locale),
  ]);
  if (!ranking) return EMPTY;
  return { ranking, facets };
}

export const getInitialHotspots = cache(loadInitialHotspots);
