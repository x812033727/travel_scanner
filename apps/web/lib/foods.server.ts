import { cache } from "react";
import { emptyFoodBrowserFilters, merchantsQuery, type FoodBrowserFilters } from "@/lib/foods";
import { publicServerHeaders } from "@/lib/public-server-fetch";

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

// These lists include current publication decisions and counts. Request memoization saves
// duplicate reads without continuing to expose a merchant or category after moderation.
async function fetchJson(url: string, locale: string): Promise<unknown | null> {
  try {
    const response = await fetch(url, {
      cache: "no-store",
      signal: AbortSignal.timeout(3000),
      headers: await publicServerHeaders(locale),
    });
    if (!response.ok) return null;
    return (await response.json()) as unknown;
  } catch {
    // The client asks for the same two endpoints on mount, so a server-side miss costs the
    // reader the old late-arriving list and nothing else.
    return null;
  }
}

export async function loadInitialFoods(
  locale: string,
  filters: FoodBrowserFilters = emptyFoodBrowserFilters,
): Promise<InitialFoods> {
  const apiBase = (process.env.API_INTERNAL_URL || "http://localhost:8000").replace(/\/$/, "");
  const [cities, categories, merchants] = await Promise.all([
    fetchJson(`${apiBase}/api/v1/foods/cities`, locale),
    fetchJson(`${apiBase}/api/v1/foods/categories`, locale),
    fetchJson(`${apiBase}/api/v1/foods/merchants?${merchantsQuery(filters)}`, locale),
  ]);
  return { cities, categories, merchants };
}

export const getInitialFoods = cache(loadInitialFoods);
