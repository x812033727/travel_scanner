import { readdirSync } from "node:fs";
import { join } from "node:path";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { locales } from "@/i18n/routing";
import { siteUrl } from "@/lib/seo";
import { closedSiteVisibility, openSiteVisibility } from "@/lib/site-features";
import {
  guideSitemapEntries, guideSitemapSummary, guideTopicSitemapEntries,
  type GuideSitemapCount, type GuideSitemapEntry, type GuideSitemapFilters,
} from "@/lib/guides.server";
import { getDiscoveryStatus } from "@/lib/discovery-status.server";
import { getSiteVisibility } from "@/lib/site-visibility.server";
import { getCommunityState } from "@/lib/community/server";
import { closedCommunity, type CommunityState } from "@/lib/community/types";
import { petPlaceSitemapEntries, type PetPlaceSitemapEntry } from "@/lib/community/public.server";
import sitemap, {
  dynamic, generateSitemaps, listedSitemapChildren, parseSitemapChild, SITEMAP_CHILDREN, SITEMAP_ROUTES,
  sitemapChildId, sitemapChildPath, sitemapChildren,
} from "./sitemap";
import { guideSection } from "@/lib/guides";

vi.mock("@/lib/site-visibility.server", () => ({ getSiteVisibility: vi.fn() }));
// Discovery is off in production, so that is the default here too: /explore is the one route
// listed behind it, and every count below is of the routes that do not depend on it.
vi.mock("@/lib/discovery-status.server", () => ({ getDiscoveryStatus: vi.fn() }));

/** The routes listed whatever the discovery and community switches say. */
const STATIC_ROUTES = SITEMAP_ROUTES.filter((route) => !route.discovery && !route.community);
// Defaulting to an unreadable summary is what keeps every assertion below about the static
// routes exactly as it was, including the whole-array comparison: with no publication picture
// every section hub stays listed in all five languages. The hub cases opt in to a summary.
// The reads are stubbed; the slice size stays the real constant the children are cut by.
vi.mock("@/lib/guides.server", async (original) => ({
  ...await original<typeof import("@/lib/guides.server")>(),
  guideSitemapEntries: vi.fn(), guideSitemapSummary: vi.fn(), guideTopicSitemapEntries: vi.fn(),
}));

/** One child of the index, as Next calls it: the id arrives as a promise. */
const child = (id: string) => sitemap({ id: Promise.resolve(id) });
/** Every child concatenated, for the properties that hold across the whole index. */
const everything = async () => (await Promise.all(SITEMAP_CHILDREN.map(child))).flat();
/** The article enumeration answers each child with its own section and locale only, as the
 *  API does; `complete` is what the child was told about the picture it got. */
const mockEntries = (rows: GuideSitemapEntry[], complete = true) =>
  vi.mocked(guideSitemapEntries).mockReset().mockImplementation(async ({ section, locale }: GuideSitemapFilters = {}) => ({
    entries: rows.filter((row) => (!section || guideSection(row.kind) === section) && (!locale || row.locale === locale)),
    complete,
  }));
const unavailableSummary = { counts: [] as GuideSitemapCount[], available: false };
// The real module is `server-only`, and the community is off in production, so that is the
// default here too: /pet-friendly is the one route listed behind it.
vi.mock("@/lib/community/server", () => ({ getCommunityState: vi.fn() }));
const OPEN_COMMUNITY: CommunityState = { status: "ready", flags: { ...closedCommunity.flags, enabled: true } };
// The place enumeration is stubbed like the guide reads, and empty by default, so every count
// below is of the routes. The place cases at the bottom opt in to rows.
vi.mock("@/lib/community/public.server", async (original) => ({
  ...await original<typeof import("@/lib/community/public.server")>(),
  petPlaceSitemapEntries: vi.fn(async () => ({ entries: [], complete: true })),
}));
/** What the enumeration read: the places, and whether it read the whole directory. */
const mockPlaces = (rows: PetPlaceSitemapEntry[], complete = true) =>
  vi.mocked(petPlaceSitemapEntries).mockReset().mockResolvedValue({ entries: rows, complete });

const APP = join(import.meta.dirname, "..");
// Both trees serve /{locale}/…: the second is a route group with its own root layout.
const ROOTS = [join(APP, "[locale]"), join(APP, "(stay22-public)", "[locale]")];

function directories(parent: string): string[] {
  try {
    return readdirSync(parent, { withFileTypes: true }).filter((entry) => entry.isDirectory()).map((entry) => entry.name);
  } catch {
    return [];
  }
}

/** Walks a sitemap path down the app directory, letting a `[dynamic]` folder stand in for a
 *  literal segment, and reports whether it lands on a real page.tsx. */
function routeExists(path: string): boolean {
  const segments = path.split("/").filter(Boolean);
  const walk = (directory: string, rest: string[]): boolean => {
    if (!rest.length) return readdirSync(directory).includes("page.tsx");
    const [head, ...tail] = rest;
    const names = directories(directory);
    // A catch-all ([...rest]) matches every remaining segment, so counting it here would
    // make routeExists answer true for any address and this guard would stop guarding.
    // The locale segment has one, so that a mistyped URL reaches the localised 404.
    const candidates = names.includes(head)
      ? [head]
      : names.filter((name) => name.startsWith("[") && !/^\[{1,2}\.\.\./.test(name));
    return candidates.some((name) => walk(join(directory, name), tail));
  };
  return ROOTS.some((root) => walk(root, segments));
}

describe("the index's children", () => {
  it("names one static child and one per section and locale when the summary cannot be read", async () => {
    // `next build` calls generateSitemaps with no API to reach: the read fails and the
    // list is the eleven base children, every one of which always exists.
    vi.mocked(guideSitemapSummary).mockReset().mockResolvedValue(unavailableSummary);
    vi.mocked(guideSitemapEntries).mockReset();
    expect(await generateSitemaps()).toEqual(SITEMAP_CHILDREN.map((id) => ({ id })));
    expect(SITEMAP_CHILDREN).toEqual([
      "static",
      "travel-en", "travel-ja", "travel-ko", "travel-zh-TW", "travel-zh-CN",
      "life-en", "life-ja", "life-ko", "life-zh-TW", "life-zh-CN",
    ]);
    expect(guideSitemapEntries).not.toHaveBeenCalled();
  });

  it("adds a numbered child per further 5,000 rows a section publishes in a language, so no row is ever left out", async () => {
    // 12,000 lifestyle rows in zh-TW need three children; 5,000 exactly still fit in one;
    // a section with nothing keeps its base child (an empty file, never a 404) and no more.
    const summary = {
      counts: [
        { kind: "life" as const, locale: "zh-TW" as const, count: 12_000 },
        { kind: "intel" as const, locale: "zh-TW" as const, count: 2_000 },
        { kind: "howto" as const, locale: "zh-TW" as const, count: 3_000 },
        { kind: "howto" as const, locale: "en" as const, count: 1 },
      ],
      available: true,
    };
    expect(sitemapChildren(summary)).toEqual([
      "static",
      "travel-en", "travel-ja", "travel-ko", "travel-zh-TW", "travel-zh-CN",
      "life-en", "life-ja", "life-ko", "life-zh-TW", "life-zh-TW-2", "life-zh-TW-3", "life-zh-CN",
    ]);
    // The index lists only what has rows: every slice of a publishing section, no empty child.
    expect(listedSitemapChildren(summary)).toEqual([
      "static", "travel-en", "travel-zh-TW", "life-zh-TW", "life-zh-TW-2", "life-zh-TW-3",
    ]);
    expect(listedSitemapChildren(unavailableSummary)).toEqual([...SITEMAP_CHILDREN]);
    // Next answers 404 for an id generateSitemaps did not return, so the numbered children
    // have to come from it at request time -- from the same summary the index reads.
    vi.mocked(guideSitemapSummary).mockReset().mockResolvedValue(summary);
    expect((await generateSitemaps()).map((item) => item.id)).toEqual(sitemapChildren(summary));
  });

  it("serves each child under /sitemaps/sitemap/<id>.xml, the .xml keeping it out of the locale proxy", () => {
    expect(sitemapChildPath("life-zh-TW")).toBe("/sitemaps/sitemap/life-zh-TW.xml");
    expect(parseSitemapChild("life-zh-TW")).toEqual({ section: "life", locale: "zh-TW", page: 1 });
    expect(parseSitemapChild("travel-en")).toEqual({ section: "travel", locale: "en", page: 1 });
    expect(parseSitemapChild("life-zh-TW-2")).toEqual({ section: "life", locale: "zh-TW", page: 2 });
    expect(parseSitemapChild("life-zh-TW-12")).toEqual({ section: "life", locale: "zh-TW", page: 12 });
    expect(sitemapChildId({ section: "life", locale: "zh-TW", page: 1 })).toBe("life-zh-TW");
    expect(sitemapChildId({ section: "life", locale: "zh-TW", page: 3 })).toBe("life-zh-TW-3");
    expect(parseSitemapChild("static")).toBeNull();
    expect(parseSitemapChild("life-xx")).toBeNull();
    // Only the spelling sitemapChildId produces: the first slice has no number, and no zeros.
    for (const id of ["life-zh-TW-1", "life-zh-TW-0", "life-zh-TW-02", "life-zh-TW-2x", "life-zh-TW-"]) {
      expect(parseSitemapChild(id), id).toBeNull();
    }
  });

  it("answers an unknown id with nothing rather than a guess", async () => {
    vi.mocked(guideSitemapEntries).mockReset().mockResolvedValue({ entries: [], complete: true });
    vi.mocked(guideTopicSitemapEntries).mockReset().mockResolvedValue([]);
    expect(await child("recipes-zh-TW")).toEqual([]);
    expect(guideSitemapEntries).not.toHaveBeenCalled();
  });
});

describe("sitemap", () => {
  let entries: Awaited<ReturnType<typeof sitemap>>;
  beforeEach(async () => {
    vi.mocked(getSiteVisibility).mockReset().mockResolvedValue({ status: "ready", features: openSiteVisibility });
    mockEntries([]);
    vi.mocked(guideSitemapSummary).mockReset().mockResolvedValue(unavailableSummary);
    vi.mocked(guideTopicSitemapEntries).mockReset().mockResolvedValue([]);
    vi.mocked(getDiscoveryStatus).mockReset().mockResolvedValue({ enabled: false });
    vi.mocked(getCommunityState).mockReset().mockResolvedValue(closedCommunity);
    mockPlaces([]);
    entries = await child("static");
  });

  it("reads current visibility once instead of freezing switches during the build", () => {
    expect(dynamic).toBe("force-dynamic");
    expect(getSiteVisibility).toHaveBeenCalledTimes(1);
  });

  it("keeps the static child to the routes: no article and no topic hub ever lands in it", async () => {
    mockEntries([{ kind: "life", slug: "ai-notes", locale: "zh-TW", published_at: "2026-09-05T08:00:00Z", locales: ["zh-TW"] }]);
    vi.mocked(guideTopicSitemapEntries).mockResolvedValue([{ section: "life", slug: "ai", locales: ["zh-TW"] }]);
    expect(await child("static")).toEqual(entries);
    expect(guideSitemapEntries).not.toHaveBeenCalled();
  });

  it.each([
    ["/hotspots", "hotspots_enabled"],
    ["/pricing", "pricing_enabled"],
    ["/flights/status", "flight_status_enabled"],
    ["/labs/airlines", "airline_fares_enabled"],
  ] as const)("omits %s in every language immediately when its switch closes", async (path, key) => {
    vi.mocked(getSiteVisibility).mockResolvedValue({ status: "ready", features: { ...openSiteVisibility, [key]: false } });
    const closed = await child("static");
    expect(closed).toHaveLength(entries.length - locales.length);
    for (const locale of locales) {
      expect(closed.map((entry) => entry.url)).not.toContain(`${siteUrl}/${locale}${path}`);
    }
    vi.mocked(getSiteVisibility).mockResolvedValue({ status: "ready", features: openSiteVisibility });
    expect(await child("static")).toEqual(entries);
  });

  it.each(["ready", "unavailable"] as const)("keeps core pages but not gated pages when visibility is %s and closed", async (status) => {
    // Even a stale open feature set must not make an unavailable state indexable.
    vi.mocked(getSiteVisibility).mockResolvedValue({ status, features: status === "unavailable" ? openSiteVisibility : closedSiteVisibility });
    const closed = await child("static");
    const expectedPaths = STATIC_ROUTES.filter((route) => !route.feature).map((route) => route.path);
    expect(closed.map((entry) => entry.url)).toEqual(expectedPaths.flatMap((path) => locales.map((locale) => `${siteUrl}/${locale}${path === "/" ? "" : path}`)));
    expect(closed.map((entry) => entry.url)).toContain(`${siteUrl}/en/foods`);
    expect(closed.map((entry) => entry.url)).toContain(`${siteUrl}/en/destinations/tokyo`);
  });

  it("publishes one entry per locale per route", () => {
    expect(entries).toHaveLength(STATIC_ROUTES.length * locales.length);
  });

  it("lists /explore only while discovery is on, and never its saved-items workspace", async () => {
    // With the switch off the route falls back to a grid of links to pages already listed
    // here. With it on it server-renders the feed's first page, which is its own content.
    for (const locale of locales) expect(entries.map((entry) => entry.url)).not.toContain(`${siteUrl}/${locale}/explore`);
    vi.mocked(getDiscoveryStatus).mockResolvedValue({ enabled: true });
    const open = await child("static");
    expect(open).toHaveLength(entries.length + locales.length);
    for (const locale of locales) expect(open.map((entry) => entry.url)).toContain(`${siteUrl}/${locale}/explore`);
    // /explore/collections is every reader's own saved items behind a sign-in prompt. It is
    // not thin content waiting for server rendering; it is a member page.
    expect(open.map((entry) => entry.url)).not.toContain(`${siteUrl}/en/explore/collections`);
  });

  it("has no duplicate URLs", () => {
    const urls = entries.map((entry) => entry.url);
    expect(new Set(urls).size).toBe(urls.length);
  });

  // Scoped to the static routes, not the whole file. A guide article carries a real
  // `lastModified` because the API returns its actual publication date; for a city guide the
  // route still has no idea when its places moved, so an invented "now" would be the lie this
  // assertion was written to prevent. See the guide-article cases at the bottom.
  it("publishes no lastmod for the routes whose update date it cannot know", () => {
    // A `lastmod` of "now" on every crawl is worse than none: Google honours the field only
    // where it tracks real content change, and this route has no access to that -- the city
    // guides' content lives behind the API it deliberately does not call.
    for (const entry of entries) expect(entry.lastModified).toBeUndefined();
  });

  it("uses absolute URLs on the canonical origin", () => {
    for (const entry of entries) expect(entry.url.startsWith(`${siteUrl}/`)).toBe(true);
  });

  // Also scoped to the static routes. An article publishes one locale at a time and declares
  // only the translations that exist, so requiring all five of it would force the sitemap to
  // advertise pages nobody has written.
  it("gives every static entry all five locales plus x-default", () => {
    for (const entry of entries) {
      const languages = entry.alternates?.languages ?? {};
      expect(Object.keys(languages).sort()).toEqual([...locales, "x-default"].sort());
    }
  });

  // The guard that matters: without it a rename quietly turns the sitemap into a list of 404s,
  // and nothing else in the suite would notice.
  it.each(SITEMAP_ROUTES.map((route) => route.path))("%s resolves to a real page", (path) => {
    expect(routeExists(path), `${path} has no page.tsx under app/`).toBe(true);
  });

  it("would notice a path that has no page", () => {
    // A guard on the guard: if the walk stopped matching the app directory, the check above
    // would pass by testing nothing. Same reasoning as app/[locale]/metadata.test.ts.
    expect(routeExists("/hotspots")).toBe(true);
    expect(routeExists("/not-a-route")).toBe(false);
    expect(routeExists("/destinations/tokyo/nope")).toBe(false);
  });

  it("lists /pet-friendly only while the community switch is on", async () => {
    // With the switch off the route renders the "closed" notice and its own metadata says
    // noindex, so the sitemap must not advertise it either.
    for (const locale of locales) expect(entries.map((entry) => entry.url)).not.toContain(`${siteUrl}/${locale}/pet-friendly`);
    vi.mocked(getCommunityState).mockResolvedValue(OPEN_COMMUNITY);
    const open = await child("static");
    expect(open).toHaveLength(entries.length + locales.length);
    for (const locale of locales) expect(open.map((entry) => entry.url)).toContain(`${siteUrl}/${locale}/pet-friendly`);
    // The rest of the community stays out: those routes are a member feed and a sign-in
    // prompt, not content waiting on server rendering.
    for (const path of ["/community", "/community/collections", "/community/drafts", "/community/settings"]) {
      expect(open.map((entry) => entry.url)).not.toContain(`${siteUrl}/en${path}`);
    }
  });

  it("treats an unreachable community as closed", async () => {
    // Failing open would advertise a directory that answers with the closed notice.
    vi.mocked(getCommunityState).mockResolvedValue({ status: "unavailable", flags: { ...closedCommunity.flags, enabled: true } });
    const closed = await child("static");
    expect(closed.map((entry) => entry.url)).not.toContain(`${siteUrl}/en/pet-friendly`);
  });

  it("leaves out routes that are still noindex", () => {
    // Managed documents are noindex until published; explore/collections and the member
    // community routes send an empty shell. Listing any would collect "Excluded by noindex".
    const paths = SITEMAP_ROUTES.map((route) => route.path);
    for (const path of ["/about", "/privacy", "/terms", "/contact", "/explore/collections", "/community"]) {
      expect(paths).not.toContain(path);
    }
  });

  it("carries every public destination", () => {
    const paths = SITEMAP_ROUTES.map((route) => route.path);
    expect(paths).toContain("/destinations/tokyo");
    expect(paths.filter((path) => path.startsWith("/destinations/")).length).toBeGreaterThanOrEqual(33);
  });

  it("leaves out the services page of every one of them", () => {
    // One template per city with the name in its title and the lodging drawn by Stay22 after
    // hydration: Search Console read 23 of them as duplicates and overrode the canonical each
    // declared. They carry `noindex` now, and a sitemap that still named them would be the
    // site contradicting itself. The destination page above links to each one.
    const paths = SITEMAP_ROUTES.map((route) => route.path);
    expect(paths.filter((path) => path.endsWith("/services"))).toEqual([]);
  });
});

describe("guide articles in the section children", () => {
  const narita = {
    kind: "howto" as const, slug: "narita-to-tokyo", published_at: "2026-09-01T00:00:00Z",
    locales: ["zh-TW", "ja"] as const,
  };
  const sale = {
    kind: "intel" as const, slug: "jr-pass-sale", published_at: "2026-09-10T00:00:00Z",
    locales: ["zh-TW", "en"] as const,
  };
  // Published in one locale only, so its entry must carry a single alternate and no x-default.
  const notes = {
    kind: "life" as const, slug: "ai-notes", published_at: "2026-09-05T08:00:00Z",
    locales: ["zh-TW"] as const,
  };
  const rows: GuideSitemapEntry[] = [
    ...narita.locales.map((locale) => ({ ...narita, locale, locales: [...narita.locales] })),
    ...sale.locales.map((locale) => ({ ...sale, locale, locales: [...sale.locales] })),
    ...notes.locales.map((locale) => ({ ...notes, locale, locales: [...notes.locales] })),
  ];

  function arrange(entries = rows, complete = true) {
    vi.mocked(getSiteVisibility).mockReset().mockResolvedValue({ status: "ready", features: openSiteVisibility });
    mockEntries(entries, complete);
    vi.mocked(guideSitemapSummary).mockReset().mockResolvedValue(unavailableSummary);
    vi.mocked(guideTopicSitemapEntries).mockReset().mockResolvedValue([]);
    vi.mocked(getDiscoveryStatus).mockReset().mockResolvedValue({ enabled: false });
    vi.mocked(getCommunityState).mockReset().mockResolvedValue(closedCommunity);
    mockPlaces([]);
  }
  async function build(entries = rows, complete = true) {
    arrange(entries, complete);
    return everything();
  }

  /** Articles only. `/guides/intel` and `/guides/howto` are static hub routes and belong to
   *  the checks above, so matching on "/guides/" alone would sweep them in here. */
  const guideEntries = (all: Awaited<ReturnType<typeof sitemap>>) =>
    all.filter((entry) => (entry.url.split("/guides/")[1] ?? "").includes("/"));

  /** Lifestyle articles only. `/life` itself is a static hub, so a slug must follow it. */
  const lifeEntries = (all: Awaited<ReturnType<typeof sitemap>>) =>
    all.filter((entry) => /\/life\/[^/]+$/.test(new URL(entry.url).pathname));

  it("publishes one entry per published locale and none for the others", async () => {
    const guides = guideEntries(await build());
    expect(guides.map((entry) => entry.url).sort()).toEqual([
      `${siteUrl}/en/guides/intel/jr-pass-sale`,
      `${siteUrl}/ja/guides/howto/narita-to-tokyo`,
      `${siteUrl}/zh-TW/guides/howto/narita-to-tokyo`,
      `${siteUrl}/zh-TW/guides/intel/jr-pass-sale`,
    ]);
    // The two locales nobody wrote must not appear anywhere.
    for (const entry of guides) expect(entry.url).not.toContain("/ko/guides/");
  });

  it("files each row in the child of its own section and language, and asks the API for exactly that", async () => {
    arrange();
    expect((await child("travel-ja")).map((entry) => entry.url)).toEqual([`${siteUrl}/ja/guides/howto/narita-to-tokyo`]);
    expect(guideSitemapEntries).toHaveBeenLastCalledWith({ section: "travel", locale: "ja", offset: 0 });
    expect((await child("life-zh-TW")).map((entry) => entry.url)).toEqual([`${siteUrl}/zh-TW/life/ai-notes`]);
    expect((await child("life-en")).map((entry) => entry.url)).toEqual([]);
    expect((await child("travel-zh-TW")).map((entry) => entry.url).sort()).toEqual([
      `${siteUrl}/zh-TW/guides/howto/narita-to-tokyo`,
      `${siteUrl}/zh-TW/guides/intel/jr-pass-sale`,
    ]);
  });

  it("starts a numbered child 5,000 rows down the same order, with the articles only", async () => {
    // The topic hubs live in the first child; the second is the next slice of articles.
    arrange();
    vi.mocked(guideTopicSitemapEntries).mockResolvedValue([{ section: "life", slug: "ai", locales: ["zh-TW"] }]);
    const first = await child("life-zh-TW");
    expect(first.map((entry) => entry.url)).toEqual([`${siteUrl}/zh-TW/life/topics/ai`, `${siteUrl}/zh-TW/life/ai-notes`]);
    const second = await child("life-zh-TW-2");
    expect(guideSitemapEntries).toHaveBeenLastCalledWith({ section: "life", locale: "zh-TW", offset: 5000 });
    expect(second.map((entry) => entry.url)).toEqual([`${siteUrl}/zh-TW/life/ai-notes`]);
    expect(guideTopicSitemapEntries).toHaveBeenCalledTimes(1);
  });

  it("keeps a row the API filed under the wrong child out of it", async () => {
    // Defence in depth: the filters are the API's, and the child re-checks them.
    arrange();
    vi.mocked(guideSitemapEntries).mockResolvedValue({ entries: rows, complete: true });
    expect((await child("life-en")).map((entry) => entry.url)).toEqual([]);
    expect((await child("travel-ja")).map((entry) => entry.url)).toEqual([`${siteUrl}/ja/guides/howto/narita-to-tokyo`]);
  });

  it("advertises only the translations that exist, each at its own URL, across children", async () => {
    const guides = guideEntries(await build());
    const japanese = guides.find((entry) => entry.url.endsWith("/ja/guides/howto/narita-to-tokyo"));
    expect(Object.keys(japanese!.alternates!.languages!).sort()).toEqual(["ja", "zh-TW"]);
    // The href matters as much as the key set: checking keys alone leaves a wrong target -- some
    // other locale's prefix, or the hub path -- invisible on every entry.
    for (const entry of guides) {
      const path = new URL(entry.url).pathname.replace(/^\/[^/]+/, "");
      const languages = (entry.alternates?.languages ?? {}) as Record<string, string>;
      for (const [language, href] of Object.entries(languages)) {
        expect(href).toBe(`${siteUrl}/${language === "x-default" ? "en" : language}${path}`);
      }
    }
  });

  it("leaves the static child untouched by the articles, which live in their own children", async () => {
    // Every other static assertion in this file runs with the guides mocked to an empty list, so
    // a change that only shows up once the API returns rows would pass all of them.
    arrange([]);
    const staticOnly = await child("static");
    arrange();
    expect(await child("static")).toEqual(staticOnly);
    const all = await everything();
    expect(all.slice(0, staticOnly.length)).toEqual(staticOnly);
    expect(all).toHaveLength(staticOnly.length + rows.length);
  });

  it("offers x-default only where the English version is published", async () => {
    const guides = guideEntries(await build());
    const withDefault = guides.filter((entry) => "x-default" in (entry.alternates?.languages ?? {}));
    expect(withDefault.map((entry) => entry.url).sort()).toEqual([
      `${siteUrl}/en/guides/intel/jr-pass-sale`,
      `${siteUrl}/zh-TW/guides/intel/jr-pass-sale`,
    ]);
  });

  it("carries the real publication date, which is the point for a dated notice", async () => {
    const guides = guideEntries(await build());
    const notice = guides.find((entry) => entry.url.endsWith("/en/guides/intel/jr-pass-sale"));
    expect(notice!.lastModified).toEqual(new Date("2026-09-10T00:00:00Z"));
  });

  it("moves lastmod to the republication when the API reports one, so a corrected notice is recrawled", async () => {
    const corrected = rows.map((row) => (
      row.slug === "jr-pass-sale" && row.locale === "en" ? { ...row, modified_at: "2026-09-12T09:00:00Z" } : row
    ));
    const guides = guideEntries(await build(corrected));
    expect(guides.find((entry) => entry.url.endsWith("/en/guides/intel/jr-pass-sale"))!.lastModified)
      .toEqual(new Date("2026-09-12T09:00:00Z"));
    // The sibling without one keeps its first publication date.
    expect(guides.find((entry) => entry.url.endsWith("/zh-TW/guides/intel/jr-pass-sale"))!.lastModified)
      .toEqual(new Date("2026-09-10T00:00:00Z"));
  });

  it("adds no duplicate URL across the children, even if a row repeats", async () => {
    // The fixture's four translations are already distinct, so without the repeated row this
    // assertion cannot fail and the property it names goes unchecked.
    const urls = (await build([...rows, rows[0]])).map((entry) => entry.url);
    expect(new Set(urls).size).toBe(urls.length);
    expect(urls).toHaveLength(STATIC_ROUTES.length * locales.length + rows.length);
  });

  it("keeps the static child intact and the section children empty when the guides API is unreachable", async () => {
    const fallback = await build([], false);
    expect(fallback.length).toBe(STATIC_ROUTES.length * locales.length);
    expect(guideEntries(fallback)).toEqual([]);
  });

  it("files a lifestyle article under /life, in its own locale only, on the evergreen cadence", async () => {
    const all = await build();
    const life = lifeEntries(all);
    expect(life.map((entry) => entry.url)).toEqual([`${siteUrl}/zh-TW/life/ai-notes`]);
    expect(life[0].changeFrequency).toBe("monthly");
    expect(life[0].lastModified).toEqual(new Date("2026-09-05T08:00:00Z"));
    // One published locale and no English: a single self-referencing alternate, no x-default.
    expect(life[0].alternates?.languages).toEqual({ "zh-TW": `${siteUrl}/zh-TW/life/ai-notes` });
    // The kind never leaks into the travel folder, which is a 404 for it.
    for (const entry of all) expect(entry.url).not.toContain("/guides/life/");
    expect(guideEntries(all)).toHaveLength(4);
  });

  it("lists the section hubs, which are static routes and stay in the exact-array checks", () => {
    const paths = SITEMAP_ROUTES.map((route) => route.path);
    expect(paths).toContain("/guides");
    expect(paths).toContain("/guides/intel");
    expect(paths).toContain("/guides/howto");
    expect(paths).toContain("/life");
    for (const path of ["/guides", "/guides/intel", "/guides/howto", "/life"]) {
      expect(routeExists(path), path).toBe(true);
    }
    // A hub of evergreen articles, like /guides/howto: weekly, not the intel hub's daily.
    expect(SITEMAP_ROUTES.find((route) => route.path === "/life")).toEqual({
      path: "/life", priority: 0.6, changeFrequency: "weekly", hub: ["life"],
    });
  });
});

describe("section hubs in a language with nothing published", () => {
  /** The live shape on 2026-09-13: every article is zh-TW, so four of the five /guides pages
   *  answer 200 with one sentence saying the section is empty. */
  const zhOnly: GuideSitemapCount[] = [
    { kind: "intel", locale: "zh-TW", count: 1 },
    { kind: "howto", locale: "zh-TW", count: 3 },
  ];

  async function build(counts: GuideSitemapCount[], available: boolean) {
    vi.mocked(getSiteVisibility).mockReset().mockResolvedValue({ status: "ready", features: openSiteVisibility });
    mockEntries([]);
    vi.mocked(guideSitemapSummary).mockReset().mockResolvedValue({ counts, available });
    vi.mocked(guideTopicSitemapEntries).mockReset().mockResolvedValue([]);
    vi.mocked(getDiscoveryStatus).mockReset().mockResolvedValue({ enabled: false });
    vi.mocked(getCommunityState).mockReset().mockResolvedValue(closedCommunity);
    mockPlaces([]);
    return (await child("static")).map((entry) => entry.url);
  }

  it("lists a hub only where its kinds have an article, per the summary", async () => {
    const urls = await build(zhOnly, true);
    for (const path of ["/guides", "/guides/intel", "/guides/howto"]) {
      expect(urls).toContain(`${siteUrl}/zh-TW${path}`);
      for (const locale of locales.filter((value) => value !== "zh-TW")) {
        expect(urls).not.toContain(`${siteUrl}/${locale}${path}`);
      }
    }
  });

  it("drops a section whose own kind has nothing, even where its siblings publish", async () => {
    // /life is the case that matters today: zero lifestyle articles in any language, while
    // /guides is full in zh-TW. Reading "the language has articles" would have kept it.
    const urls = await build(zhOnly, true);
    for (const locale of locales) expect(urls).not.toContain(`${siteUrl}/${locale}/life`);
  });

  it("keeps a hub whose own kind publishes there while the other kind does not", async () => {
    const urls = await build([{ kind: "intel", locale: "ja", count: 1 }], true);
    expect(urls).toContain(`${siteUrl}/ja/guides`);
    expect(urls).toContain(`${siteUrl}/ja/guides/intel`);
    expect(urls).not.toContain(`${siteUrl}/ja/guides/howto`);
  });

  it("reads a zero count as nothing published, not as a hub", async () => {
    const urls = await build([{ kind: "life", locale: "ja", count: 0 }], true);
    expect(urls).not.toContain(`${siteUrl}/ja/life`);
  });

  it("advertises only the languages a hub is listed in, and x-default only with English", async () => {
    vi.mocked(getSiteVisibility).mockReset().mockResolvedValue({ status: "ready", features: openSiteVisibility });
    mockEntries([]);
    vi.mocked(guideSitemapSummary).mockReset().mockResolvedValue({ counts: zhOnly, available: true });
    vi.mocked(guideTopicSitemapEntries).mockReset().mockResolvedValue([]);
    vi.mocked(getDiscoveryStatus).mockReset().mockResolvedValue({ enabled: false });
    vi.mocked(getCommunityState).mockReset().mockResolvedValue(closedCommunity);
    mockPlaces([]);
    const all = await child("static");
    const hub = all.find((entry) => entry.url === `${siteUrl}/zh-TW/guides/intel`);
    // Pointing hreflang at /en/guides/intel would advertise the page this file just refused
    // to list, and the page itself answers noindex.
    expect(hub!.alternates?.languages).toEqual({ "zh-TW": `${siteUrl}/zh-TW/guides/intel` });
    const foods = all.find((entry) => entry.url === `${siteUrl}/zh-TW/foods`);
    expect(Object.keys(foods!.alternates?.languages ?? {}).sort()).toEqual([...locales, "x-default"].sort());
  });

  it("keeps every hub in every language when the summary could not be read", async () => {
    // An outage cannot tell an unpublished language from an unseen one.
    const urls = await build(zhOnly, false);
    for (const path of ["/guides", "/guides/intel", "/guides/howto", "/life"]) {
      for (const locale of locales) expect(urls).toContain(`${siteUrl}/${locale}${path}`);
    }
  });
});

describe("topic hubs in the section children", () => {
  const hubs = [
    { section: "life" as const, slug: "ai", locales: ["zh-TW", "en"] as ("zh-TW" | "en")[] },
    { section: "life" as const, slug: "ai-terms", locales: ["zh-TW"] as "zh-TW"[] },
    { section: "travel" as const, slug: "transport", locales: ["zh-TW", "ja"] as ("zh-TW" | "ja")[] },
  ];

  async function build() {
    vi.mocked(getSiteVisibility).mockReset().mockResolvedValue({ status: "ready", features: openSiteVisibility });
    mockEntries([]);
    vi.mocked(guideSitemapSummary).mockReset().mockResolvedValue(unavailableSummary);
    vi.mocked(guideTopicSitemapEntries).mockReset().mockResolvedValue(hubs);
    vi.mocked(getDiscoveryStatus).mockReset().mockResolvedValue({ enabled: false });
    vi.mocked(getCommunityState).mockReset().mockResolvedValue(closedCommunity);
    mockPlaces([]);
    return (await everything()).filter((entry) => new URL(entry.url).pathname.includes("/topics/"));
  }

  it("lists a hub only in the languages that publish something under its topic", async () => {
    const topics = await build();
    expect(topics.map((entry) => entry.url).sort()).toEqual([
      `${siteUrl}/en/life/topics/ai`,
      `${siteUrl}/ja/guides/topics/transport`,
      `${siteUrl}/zh-TW/guides/topics/transport`,
      `${siteUrl}/zh-TW/life/topics/ai`,
      `${siteUrl}/zh-TW/life/topics/ai-terms`,
    ]);
  });

  it("files each hub in the child of its own section and language, ahead of that child's articles", async () => {
    await build();
    expect((await child("life-zh-TW")).map((entry) => entry.url)).toEqual([
      `${siteUrl}/zh-TW/life/topics/ai`, `${siteUrl}/zh-TW/life/topics/ai-terms`,
    ]);
    expect((await child("life-en")).map((entry) => entry.url)).toEqual([`${siteUrl}/en/life/topics/ai`]);
    expect((await child("travel-en")).map((entry) => entry.url)).toEqual([]);
    expect((await child("static")).some((entry) => entry.url.includes("/topics/"))).toBe(false);
  });

  it("carries alternates for those languages only, x-default only with English, and no lastmod", async () => {
    const topics = await build();
    const ai = topics.find((entry) => entry.url.endsWith("/zh-TW/life/topics/ai"));
    expect(ai!.alternates!.languages).toEqual({
      "zh-TW": `${siteUrl}/zh-TW/life/topics/ai`, en: `${siteUrl}/en/life/topics/ai`, "x-default": `${siteUrl}/en/life/topics/ai`,
    });
    const transport = topics.find((entry) => entry.url.endsWith("/ja/guides/topics/transport"));
    expect(Object.keys(transport!.alternates!.languages!).sort()).toEqual(["ja", "zh-TW"]);
    for (const entry of topics) {
      expect(entry.lastModified).toBeUndefined();
      expect(entry.changeFrequency).toBe("weekly");
    }
  });

  it("lists nothing when the vocabulary could not be read", async () => {
    await build();
    vi.mocked(guideTopicSitemapEntries).mockResolvedValue([]);
    expect((await everything()).some((entry) => entry.url.includes("/topics/"))).toBe(false);
  });
});

describe("pet-friendly place pages in the static child", () => {
  // One verified on a real date and one the API has no date for: the first carries lastmod,
  // the second must carry none rather than "now".
  const cafe: PetPlaceSitemapEntry = { id: "5b6c0b1e-9a4e-4f1c-8c3e-2f4d1a7b9c01", verified_at: "2026-09-01T09:30:00Z" };
  const park: PetPlaceSitemapEntry = { id: "5b6c0b1e-9a4e-4f1c-8c3e-2f4d1a7b9c02" };
  const places = [cafe, park];

  function arrange(rows: PetPlaceSitemapEntry[] = places, complete = true, community: CommunityState = OPEN_COMMUNITY) {
    vi.mocked(getSiteVisibility).mockReset().mockResolvedValue({ status: "ready", features: openSiteVisibility });
    mockEntries([]);
    vi.mocked(guideSitemapSummary).mockReset().mockResolvedValue(unavailableSummary);
    vi.mocked(guideTopicSitemapEntries).mockReset().mockResolvedValue([]);
    vi.mocked(getDiscoveryStatus).mockReset().mockResolvedValue({ enabled: false });
    vi.mocked(getCommunityState).mockReset().mockResolvedValue(community);
    mockPlaces(rows, complete);
  }
  /** Place pages only. `/pet-friendly` itself is a static route and belongs to the checks above. */
  const placeEntries = (all: Awaited<ReturnType<typeof sitemap>>) =>
    all.filter((entry) => /\/pet-friendly\/[^/]+$/.test(new URL(entry.url).pathname));
  const placeUrl = (locale: string, place: PetPlaceSitemapEntry) => `${siteUrl}/${locale}/pet-friendly/${place.id}`;

  it("lists every place once per locale, after the routes, with all five locales and x-default", async () => {
    arrange([]);
    const routesOnly = await child("static");
    arrange();
    const all = await child("static");
    // The routes first and unchanged -- /pet-friendly among them, since the switch is on --
    // and then the places, in the directory's order, each in every locale.
    expect(all.slice(0, routesOnly.length)).toEqual(routesOnly);
    expect(routesOnly.map((entry) => entry.url)).toContain(`${siteUrl}/en/pet-friendly`);
    const listed = placeEntries(all);
    expect(listed).toEqual(all.slice(routesOnly.length));
    expect(listed.map((entry) => entry.url)).toEqual(places.flatMap((place) => locales.map((locale) => placeUrl(locale, place))));
    for (const entry of listed) {
      const languages = (entry.alternates?.languages ?? {}) as Record<string, string>;
      expect(Object.keys(languages).sort()).toEqual([...locales, "x-default"].sort());
      // The href matters as much as the key set, as with the articles: a wrong target would be
      // invisible to a check of the keys alone.
      const path = new URL(entry.url).pathname.replace(/^\/[^/]+/, "");
      for (const [language, href] of Object.entries(languages)) {
        expect(href).toBe(`${siteUrl}/${language === "x-default" ? "en" : language}${path}`);
      }
      expect(entry.changeFrequency).toBe("monthly");
      expect(entry.priority).toBe(0.5);
    }
    expect(routeExists(`/pet-friendly/${cafe.id}`)).toBe(true);
  });

  it("lists no place while the community switch is off or unreachable, whatever the read returned", async () => {
    // Behind a closed switch the page itself answers noindex, so a read that raced the switch
    // must not put its rows in the file either.
    const unreachable: CommunityState = { status: "unavailable", flags: { ...closedCommunity.flags, enabled: true } };
    for (const community of [closedCommunity, unreachable]) {
      arrange(places, true, community);
      const all = await child("static");
      expect(placeEntries(all)).toEqual([]);
      expect(all.map((entry) => entry.url)).not.toContain(`${siteUrl}/en/pet-friendly`);
    }
  });

  it("keeps the routes when the read failed, and the places it did read when it stopped early", async () => {
    arrange([]);
    const routesOnly = await child("static");
    arrange([], false);
    expect(await child("static")).toEqual(routesOnly);
    arrange([cafe], false);
    const partial = await child("static");
    expect(partial.slice(0, routesOnly.length)).toEqual(routesOnly);
    expect(placeEntries(partial).map((entry) => entry.url)).toEqual(locales.map((locale) => placeUrl(locale, cafe)));
  });

  it("dates a place by its verification and never by the crawl", async () => {
    arrange();
    const all = await child("static");
    for (const locale of locales) {
      expect(all.find((entry) => entry.url === placeUrl(locale, cafe))!.lastModified).toEqual(new Date("2026-09-01T09:30:00Z"));
      // No date of any kind: the omitted field is a missing signal, an invented one is the lie
      // the static routes' own lastmod check exists to prevent.
      expect(all.find((entry) => entry.url === placeUrl(locale, park))).not.toHaveProperty("lastModified");
    }
  });

  it("lists a repeated place once", async () => {
    arrange([cafe, cafe, park]);
    const urls = placeEntries(await child("static")).map((entry) => entry.url);
    expect(urls).toHaveLength(places.length * locales.length);
    expect(new Set(urls).size).toBe(urls.length);
  });

  it("never reads the directory for a section child, whose rows are articles", async () => {
    arrange();
    const sections = (await Promise.all(SITEMAP_CHILDREN.filter((id) => id !== "static").map(child))).flat();
    expect(placeEntries(sections)).toEqual([]);
    expect(petPlaceSitemapEntries).not.toHaveBeenCalled();
  });
});
