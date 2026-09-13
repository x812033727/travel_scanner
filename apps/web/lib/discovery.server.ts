import { cache } from "react";
import { publicServerHeaders } from "@/lib/public-server-fetch";

/**
 * The first page of the discovery feed, fetched on the server so `/explore` answers with its
 * actual items instead of three grey rectangles.
 *
 * The feed is a public GET. The client asked for it after hydration, which cost the reader a
 * skeleton, a round trip and a full-page shift when the real cards replaced it -- and left the
 * response body with nothing for a crawler to read.
 *
 * Two deliberate limits:
 *
 * - **No search.** Only the unfiltered feed is fetched here. `GET /discovery/search` records a
 *   `discovery_search` event on its first page, and a logged-in reader's client refetches under
 *   their own identity, so serving both would count one search twice. A query URL canonicalises
 *   to `/explore` anyway, so there is nothing to index in it.
 * - **Anonymous.** `publicServerHeaders` forwards the address and user agent and no cookies, so
 *   this is the public ranking. A signed-in reader's client refetches their own once the session
 *   resolves, exactly as it does today.
 */

export type InitialDiscoveryFeed = { path: string; page: unknown } | null;

/** The query parameters the explorer reads out of the URL, in the order it writes them. */
const KEYS = ["q", "type", "category", "destination", "topic", "locale", "mode"] as const;
export const DISCOVERY_MODES = ["recommended", "latest", "most_saved", "following"] as const;

export type DiscoverySearchParams = Partial<Record<typeof KEYS[number], string | string[]>>;

/**
 * The client's own query string, rebuilt here.
 *
 * It has to match `discoveryQuery` in `lib/discovery.ts` character for character: the component
 * uses the path as the cache key, so anything else simply means the browser fetches again and
 * the reader sees the swap this module exists to remove. That file is `"use client"`, so a
 * server module cannot call into it -- `lib/discovery.server.test.ts` compares the two outputs
 * instead, which is what keeps them from drifting apart.
 */
function queryString(search: DiscoverySearchParams, mode: string): string {
  const params = new URLSearchParams();
  for (const key of KEYS) {
    const raw = key === "mode" ? mode : search[key];
    const text = (Array.isArray(raw) ? raw[0] : raw)?.trim();
    if (text && !(["type", "category"].includes(key) && text === "all")) params.set(key, text);
  }
  return params.toString();
}

/** The mode the explorer settles on for this URL, including its default. */
export function discoveryMode(search: DiscoverySearchParams): string {
  const raw = search.mode;
  const value = Array.isArray(raw) ? raw[0] : raw;
  return DISCOVERY_MODES.includes(value as typeof DISCOVERY_MODES[number]) ? value! : "recommended";
}

/**
 * The feed request this URL should be answered with, or `null` when the server must not make
 * one. Separate from the fetch so both callers -- `generateMetadata` and the page body -- key
 * React's per-request cache on a string rather than on whatever object `searchParams` resolved
 * to, which is what makes one request fetch the feed once.
 */
export function discoveryFeedPath(search: DiscoverySearchParams, enabled: boolean): string | null {
  const q = Array.isArray(search.q) ? search.q[0] : search.q;
  const mode = discoveryMode(search);
  // `following` is a signed-in ranking; the server render shows the sign-in prompt instead of a
  // feed, so there is nothing to prefetch and the request would be answered for nobody.
  if (!enabled || q?.trim() || mode === "following") return null;
  return `/discovery/feed?${queryString(search, mode)}`;
}

export async function loadInitialDiscoveryFeed(
  locale: string, path: string | null,
): Promise<InitialDiscoveryFeed> {
  if (!path) return null;
  const apiBase = (process.env.API_INTERNAL_URL || "http://localhost:8000").replace(/\/$/, "");
  try {
    const response = await fetch(`${apiBase}/api/v1${path}`, {
      // A feed of moderated rows an editor can withdraw, and a switch an owner can close.
      cache: "no-store",
      signal: AbortSignal.timeout(3000),
      headers: await publicServerHeaders(locale),
    });
    if (!response.ok) return null;
    return { path, page: (await response.json()) as unknown };
  } catch {
    // The client fetches the same path on mount, so a miss costs the reader the skeleton they
    // used to get every time and nothing else.
    return null;
  }
}

export const getInitialDiscoveryFeed = cache(loadInitialDiscoveryFeed);
