import { cache } from "react";
import { publicServerHeaders } from "@/lib/public-server-fetch";
import { getCommunityState } from "./server";
import type { Page, PetPlace, Post, PublicProfile } from "./types";

/**
 * Server-side reads of the four public community endpoints.
 *
 * These routes carry the only long-form original content the site has -- verified pet
 * rules, traveller stories, public profiles -- and every one of them used to ship an
 * empty shell: the client components fetch in `useEffect`, so the server sent a heading
 * and a gate and nothing else. Handing the first copy over with the HTML is what makes
 * the pages worth indexing at all, which is why each route's `robots` keys on whether
 * the loader here returned anything: a failed read stays `noindex` rather than offering
 * a crawler a page with no content on it.
 *
 * Every endpoint below is a public GET. No cookie and no authorization is forwarded, so
 * what comes back is the signed-out copy of the record -- `liked`, `saved` and
 * `following` belong to the reader and arrive with the client's own fetch after
 * hydration, exactly as before.
 */

/** Long enough for a warm API, short enough that a slow one costs a blank page and not a
 *  timed-out render. The client asks for the same record on mount either way. */
const TIMEOUT_MS = 3000;

const isObject = (value: unknown): value is Record<string, unknown> =>
  typeof value === "object" && value !== null;

/**
 * Enough of each payload to know the API answered with the record rather than a problem
 * document or a redirect body. The components own the full types; what is checked here is
 * what the metadata and the first paint read, because a half-shaped object would produce a
 * `<title>` of "undefined" on a page this module has just declared indexable.
 */
const isPetPlace = (value: unknown): value is PetPlace =>
  isObject(value) && typeof value.id === "string" && typeof value.name === "string";

const isPetPlacePage = (value: unknown): value is Page<PetPlace> =>
  isObject(value) && Array.isArray(value.items) && value.items.every(isPetPlace);

const isPost = (value: unknown): value is Post =>
  isObject(value) && typeof value.id === "string" && typeof value.title === "string"
  && isObject(value.author);

const isPublicProfile = (value: unknown): value is PublicProfile =>
  isObject(value) && typeof value.id === "string" && typeof value.handle === "string"
  && typeof value.display_name === "string";

async function publicJson<T>(
  path: string,
  locale: string,
  valid: (value: unknown) => value is T,
): Promise<T | null> {
  // The switch decides whether any of this is public, so it is read before the record and
  // not after: a closed community answers without four API calls per crawl, and `robots`
  // and the rendered HTML can never disagree about whether there was content to show.
  const community = await getCommunityState();
  if (community.status !== "ready" || !community.flags.enabled) return null;
  const base = (process.env.API_INTERNAL_URL || "http://localhost:8000").replace(/\/$/, "");
  try {
    const response = await fetch(`${base}${path}`, {
      // Moderated records: a post is hidden and a pet rule withdrawn between two reads, and
      // a shared cache entry would keep handing out the withdrawn copy. Same reasoning as
      // `hotspots.server.ts`, and the same reason none of these set `next.revalidate`.
      cache: "no-store",
      signal: AbortSignal.timeout(TIMEOUT_MS),
      headers: await publicServerHeaders(locale),
    });
    if (!response.ok) return null;
    const payload: unknown = await response.json();
    return valid(payload) ? payload : null;
  } catch {
    // A miss costs the reader the old blank first paint and costs the page its place in the
    // index. Neither is worth an error page for content the client is about to fetch anyway.
    return null;
  }
}

export const loadPetPlaces = (locale: string): Promise<Page<PetPlace> | null> =>
  publicJson("/api/v1/pet-friendly/places", locale, isPetPlacePage);

export const loadPetPlace = (locale: string, id: string): Promise<PetPlace | null> =>
  publicJson(`/api/v1/pet-friendly/places/${encodeURIComponent(id)}`, locale, isPetPlace);

export const loadPost = (locale: string, id: string): Promise<Post | null> =>
  publicJson(`/api/v1/community/posts/${encodeURIComponent(id)}`, locale, isPost);

export const loadPublicProfile = (locale: string, handle: string): Promise<PublicProfile | null> =>
  publicJson(`/api/v1/community/profiles/${encodeURIComponent(handle)}`, locale, isPublicProfile);

/**
 * Request-scoped, because every route here reads the same record twice: once in
 * `generateMetadata` to title the page after its content, and once in the body to render
 * it. Without this the API would see two identical reads for one page view.
 */
export const getPetPlaces = cache(loadPetPlaces);
export const getPetPlace = cache(loadPetPlace);
export const getPost = cache(loadPost);
export const getPublicProfile = cache(loadPublicProfile);

/**
 * A meta description out of prose. Bodies and bios are written for readers, so they arrive
 * with newlines and run past any length a result snippet will show; what is wanted is one
 * unbroken line that ends on a word rather than mid-syllable.
 *
 * An empty source returns `undefined` rather than `""`, so the route omits the field and
 * inherits the site description instead of publishing an empty one.
 */
export function metaDescription(value: string | null | undefined, limit = 160): string | undefined {
  const text = (value || "").replace(/\s+/g, " ").trim();
  if (!text) return undefined;
  if (text.length <= limit) return text;
  const cut = text.slice(0, limit - 1);
  const space = cut.lastIndexOf(" ");
  // Chinese and Japanese have no spaces to break on, so a cut with none is kept whole.
  return `${(space > limit / 2 ? cut.slice(0, space) : cut).trimEnd()}…`;
}
