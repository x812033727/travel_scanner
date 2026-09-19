import { cache } from "react";
import { defaultLocale } from "@/i18n/routing";
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

/** Whether any of this is public. Every read below stands behind it. */
async function communityOpen(): Promise<boolean> {
  const community = await getCommunityState();
  return community.status === "ready" && community.flags.enabled;
}

/**
 * One public GET, with nothing in front of it. `publicJson` puts the switch there for a
 * page's record; `petPlaceSitemapEntries` reads the switch once and then pages through here,
 * with a timeout that shrinks to what is left of its budget.
 */
async function publicRead<T>(
  path: string,
  locale: string,
  valid: (value: unknown) => value is T,
  timeoutMs = TIMEOUT_MS,
): Promise<T | null> {
  const base = (process.env.API_INTERNAL_URL || "http://localhost:8000").replace(/\/$/, "");
  try {
    const response = await fetch(`${base}${path}`, {
      // Moderated records: a post is hidden and a pet rule withdrawn between two reads, and
      // a shared cache entry would keep handing out the withdrawn copy. Same reasoning as
      // `hotspots.server.ts`, and the same reason none of these set `next.revalidate`.
      cache: "no-store",
      signal: AbortSignal.timeout(timeoutMs),
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

async function publicJson<T>(
  path: string,
  locale: string,
  valid: (value: unknown) => value is T,
): Promise<T | null> {
  // The switch decides whether any of this is public, so it is read before the record and
  // not after: a closed community answers without four API calls per crawl, and `robots`
  // and the rendered HTML can never disagree about whether there was content to show.
  if (!await communityOpen()) return null;
  return publicRead(path, locale, valid);
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

/** One published place, as `app/sitemaps/sitemap.ts` lists it. */
export type PetPlaceSitemapEntry = {
  /** A URL segment as it stands: the enumeration keeps only ids made of unreserved
   *  characters, so nothing pastes it into `<loc>` escaped. Today's ids are UUIDs. */
  id: string;
  /** When its rules were last verified, when the API sent a real date -- the one honest
   *  `lastmod` a place has. Absent otherwise, and the sitemap then omits the field rather
   *  than inventing one. */
  verified_at?: string;
};

/**
 * The enumeration, plus whether it is the whole directory.
 *
 * `complete` is false after a failed or timed-out page, and when the page cap or the time
 * budget stopped the read with a cursor still in hand. The entries read so far are kept
 * either way, because a sitemap with most of the places beats one with none -- but a caller
 * must not read an absence here as "not published". A closed community is complete and
 * empty: nothing is public, which is the truth and not a failure.
 */
export type PetPlaceSitemapResult = { entries: PetPlaceSitemapEntry[]; complete: boolean };

/** The API's page maximum: `GET /pet-friendly/places` caps `limit` at 50 (`pets.py`). */
export const PET_PLACE_SITEMAP_PAGE_SIZE = 50;
/**
 * The most directory pages one sitemap build follows: 1,000 places, five rows each, a tenth
 * of Google's per-file limit. A cap on the read and not on the directory: past it the read
 * says `complete: false` and the first thousand still list, and the number is raised, or the
 * places given a child of their own, when the count approaches it.
 */
export const PET_PLACE_SITEMAP_PAGE_LIMIT = 20;
/**
 * How long the whole enumeration may take. Each page has `TIMEOUT_MS` of its own, but twenty
 * slow pages that each just made it would hold `sitemap.xml` for a minute, which is the hang
 * the cap exists to prevent. Past this the read stops with what it has, and the last page
 * gets only what is left rather than a full timeout of its own.
 */
export const PET_PLACE_SITEMAP_BUDGET_MS = 10_000;

/** The characters an id may contain and still be pasted into a URL, and into XML, as it is:
 *  RFC 3986's unreserved set. A UUID is well inside it; anything else is one row skipped. */
const URL_SAFE_ID = /^[A-Za-z0-9._~-]+$/;

/** Enough of a directory page to walk it. Rows are checked one at a time below, because a
 *  half-shaped row should cost one URL and not the page it came on. */
const isPetPlaceListing = (value: unknown): value is { items: unknown[]; next_cursor?: unknown } =>
  isObject(value) && Array.isArray(value.items);

/**
 * Every published place, for the sitemap: the same public directory `/pet-friendly` renders,
 * followed through `next_cursor`, with `include_uncertain` off so the set is the places whose
 * rules are currently verified -- what the directory shows without a "needs confirmation"
 * label, and what a place page has to say for itself.
 *
 * Never throws. The switch off, an unreachable API, a malformed page, a timeout and the caps
 * all end the read with what it has, so the sitemap can always fall back to its routes.
 */
export async function petPlaceSitemapEntries(): Promise<PetPlaceSitemapResult> {
  if (!await communityOpen()) return { entries: [], complete: true };
  const deadline = Date.now() + PET_PLACE_SITEMAP_BUDGET_MS;
  const entries: PetPlaceSitemapEntry[] = [];
  let cursor: string | null = null;
  for (let page = 0; page < PET_PLACE_SITEMAP_PAGE_LIMIT; page += 1) {
    const remaining = deadline - Date.now();
    if (remaining <= 0) return { entries, complete: false };
    const params = new URLSearchParams({ limit: String(PET_PLACE_SITEMAP_PAGE_SIZE), include_uncertain: "false" });
    if (cursor) params.set("cursor", cursor);
    const listing = await publicRead(
      `/api/v1/pet-friendly/places?${params.toString()}`, defaultLocale, isPetPlaceListing, Math.min(TIMEOUT_MS, remaining),
    );
    if (!listing) return { entries, complete: false };
    for (const item of listing.items) {
      // Neither guard is reachable through today's API (UUID ids, a datetime column). They are
      // here because either one costs the whole file rather than one row: Next writes the id
      // into <loc> and into every alternate's href with no escaping, so an `&` in it makes
      // the document unparseable, and it serialises a date by calling toISOString() on it,
      // which throws on an Invalid Date -- a 500 for the child rather than a missing entry.
      if (!isObject(item) || typeof item.id !== "string" || !URL_SAFE_ID.test(item.id)) continue;
      const verified = typeof item.verified_at === "string" && Number.isFinite(Date.parse(item.verified_at))
        ? { verified_at: item.verified_at } : {};
      entries.push({ id: item.id, ...verified });
    }
    const next = listing.next_cursor;
    cursor = typeof next === "number" || (typeof next === "string" && next !== "") ? String(next) : null;
    if (!cursor) return { entries, complete: true };
  }
  // Every page the cap allows read, and a cursor still in hand: the rest stays unlisted.
  return { entries, complete: false };
}

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
