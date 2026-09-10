import { cache } from "react";

/**
 * The city chooser the food page used to fetch after hydration.
 *
 * On a phone that list is 2,492 pixels tall — seven countries and thirty-three cities —
 * and it arrived about four seconds in, pushing everything the reader was already looking
 * at that far down the page. Reserving its space with a skeleton cannot work: the height
 * depends on the answer. The data is a public GET, so the server hands it over with the
 * HTML and there is nothing left to shift.
 *
 * Both shapes stay `unknown` here on purpose: the component owns the types, and everything
 * this module promises is "either the API's payload or null".
 */
export type InitialFoods = {
  cities: unknown | null;
  categories: unknown | null;
  merchants: unknown | null;
};

const EMPTY: InitialFoods = { cities: null, categories: null, merchants: null };

/**
 * Cached, not `no-store`. Cities, categories and the unfiltered merchant page are public and
 * identical for every reader, so going back to origin on each request only adds to TTFB, which
 * lands in LCP. The taxonomy moves rarely; the merchant listing moves daily.
 */
const TAXONOMY_TTL = 3600;
const LISTING_TTL = 900;

async function fetchJson(url: string, locale: string, revalidate: number): Promise<unknown | null> {
  try {
    const response = await fetch(url, {
      next: { revalidate },
      headers: { Accept: "application/json", "X-Travel-Locale": locale },
    });
    if (!response.ok) return null;
    return (await response.json()) as unknown;
  } catch {
    // The client asks for the same two endpoints on mount, so a server-side miss costs the
    // reader the old late-arriving list and nothing else.
    return null;
  }
}

export async function loadInitialFoods(locale: string): Promise<InitialFoods> {
  const apiBase = (process.env.API_INTERNAL_URL || "http://localhost:8000").replace(/\/$/, "");
  const [cities, categories, merchants] = await Promise.all([
    fetchJson(`${apiBase}/api/v1/foods/cities`, locale, TAXONOMY_TTL),
    fetchJson(`${apiBase}/api/v1/foods/categories`, locale, TAXONOMY_TTL),
    // Only the unfiltered first page. A reader arriving with filters in the address bar gets
    // their own query on mount, and a crawler -- which arrives without any -- gets the merchants
    // in the HTML instead of a page of filter controls with nothing behind them.
    fetchJson(`${apiBase}/api/v1/foods/merchants?limit=20`, locale, LISTING_TTL),
  ]);
  if (!cities) return EMPTY;
  return { cities, categories, merchants };
}

export const getInitialFoods = cache(loadInitialFoods);
