import { cache } from "react";

/**
 * The city list the food browser used to fetch from the browser after hydration.
 * It renders above the merchant list, so inserting it a second later pushed the
 * merchants down the page — one 0.29 layout shift on every first visit, at the
 * default text size. It is a public GET, so the server can send it with the HTML.
 *
 * Shapes stay `unknown`: the component owns them, and all this promises is "the
 * API's payload, or null".
 */
export type InitialFoods = {
  cities: unknown | null;
  categories: unknown | null;
};

const EMPTY: InitialFoods = { cities: null, categories: null };

async function fetchJson(url: string, locale: string): Promise<unknown | null> {
  try {
    const response = await fetch(url, {
      cache: "no-store",
      headers: { Accept: "application/json", "X-Travel-Locale": locale },
    });
    if (!response.ok) return null;
    return (await response.json()) as unknown;
  } catch {
    // The client asks for the same two endpoints on mount, so a miss here costs
    // the reader the old late-arriving city list and nothing else.
    return null;
  }
}

export async function loadInitialFoods(locale: string): Promise<InitialFoods> {
  const apiBase = (process.env.API_INTERNAL_URL || "http://localhost:8000").replace(/\/$/, "");
  const [cities, categories] = await Promise.all([
    fetchJson(`${apiBase}/api/v1/foods/cities`, locale),
    fetchJson(`${apiBase}/api/v1/foods/categories`, locale),
  ]);
  if (!cities) return EMPTY;
  return { cities, categories };
}

export const getInitialFoods = cache(loadInitialFoods);
