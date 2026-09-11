import { readdirSync } from "node:fs";
import { join } from "node:path";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { locales, type Locale } from "@/i18n/routing";
import { GUIDE_SITEMAP_LIMIT, guideSitemapEntries, type GuideSitemapEntry } from "@/lib/guides.server";
import { localeUrl, siteUrl } from "@/lib/seo";
import { closedSiteVisibility, openSiteVisibility } from "@/lib/site-features";
import { getSiteVisibility } from "@/lib/site-visibility.server";
import sitemap, { dynamic, SITEMAP_ROUTES } from "./sitemap";

vi.mock("@/lib/site-visibility.server", () => ({ getSiteVisibility: vi.fn() }));
// Only the loader the sitemap calls is replaced. The rest of the module stays real, so the
// outage and cap tests can drive the actual loader through a stubbed fetch.
vi.mock("@/lib/guides.server", async (importOriginal) => ({
  ...(await importOriginal<typeof import("@/lib/guides.server")>()),
  guideSitemapEntries: vi.fn(),
}));

const APP = import.meta.dirname;
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
    const candidates = names.includes(head) ? [head] : names.filter((name) => name.startsWith("["));
    return candidates.some((name) => walk(join(directory, name), tail));
  };
  return ROOTS.some((root) => walk(root, segments));
}

/** Every URL the static routes produce with all public switches open. */
const STATIC_URLS = new Set(SITEMAP_ROUTES.flatMap((route) => locales.map((locale) => localeUrl(locale, route.path))));

/** One published translation, shaped as `GET /guides/sitemap` returns it. */
function translation(slug: string, locale: Locale, overrides: Partial<GuideSitemapEntry> = {}): GuideSitemapEntry {
  return { kind: "howto", slug, locale, published_at: "2026-09-01T00:00:00Z", ...overrides };
}

/** The real loader, for the tests that drive it through a stubbed fetch. */
async function realGuideSitemapEntries() {
  const actual = await vi.importActual<typeof import("@/lib/guides.server")>("@/lib/guides.server");
  return actual.guideSitemapEntries;
}

describe("sitemap", () => {
  let entries: Awaited<ReturnType<typeof sitemap>>;
  beforeEach(async () => {
    vi.mocked(getSiteVisibility).mockReset().mockResolvedValue({ status: "ready", features: openSiteVisibility });
    // No published guides: this block is about the static routes, and every assertion in it reads
    // as it did before guide articles existed. The articles have their own block below.
    vi.mocked(guideSitemapEntries).mockReset().mockResolvedValue([]);
    entries = await sitemap();
  });

  it("reads current visibility once instead of freezing switches during the build", () => {
    expect(dynamic).toBe("force-dynamic");
    expect(getSiteVisibility).toHaveBeenCalledTimes(1);
  });

  it.each([
    ["/hotspots", "hotspots_enabled"],
    ["/pricing", "pricing_enabled"],
    ["/flights/status", "flight_status_enabled"],
    ["/labs/airlines", "airline_fares_enabled"],
  ] as const)("omits %s in every language immediately when its switch closes", async (path, key) => {
    vi.mocked(getSiteVisibility).mockResolvedValue({ status: "ready", features: { ...openSiteVisibility, [key]: false } });
    const closed = await sitemap();
    expect(closed).toHaveLength(entries.length - locales.length);
    for (const locale of locales) {
      expect(closed.map((entry) => entry.url)).not.toContain(`${siteUrl}/${locale}${path}`);
    }
    vi.mocked(getSiteVisibility).mockResolvedValue({ status: "ready", features: openSiteVisibility });
    expect(await sitemap()).toEqual(entries);
  });

  it.each(["ready", "unavailable"] as const)("keeps core pages but not gated pages when visibility is %s and closed", async (status) => {
    // Even a stale open feature set must not make an unavailable state indexable.
    vi.mocked(getSiteVisibility).mockResolvedValue({ status, features: status === "unavailable" ? openSiteVisibility : closedSiteVisibility });
    const closed = await sitemap();
    const expectedPaths = SITEMAP_ROUTES.filter((route) => !route.feature).map((route) => route.path);
    expect(closed.map((entry) => entry.url)).toEqual(expectedPaths.flatMap((path) => locales.map((locale) => `${siteUrl}/${locale}${path === "/" ? "" : path}`)));
    expect(closed.map((entry) => entry.url)).toContain(`${siteUrl}/en/foods`);
    expect(closed.map((entry) => entry.url)).toContain(`${siteUrl}/en/destinations/tokyo`);
  });

  it("publishes one entry per locale per route", () => {
    expect(entries).toHaveLength(SITEMAP_ROUTES.length * locales.length);
  });

  it("has no duplicate URLs", () => {
    const urls = entries.map((entry) => entry.url);
    expect(new Set(urls).size).toBe(urls.length);
  });

  it("publishes no lastmod on the static routes, even beside guide articles that do", async () => {
    // A `lastmod` of "now" on every crawl is worse than none: Google honours the field only
    // where it tracks real content change, and for the static routes this sitemap has no access
    // to that -- the city guides' places live behind the APIs it deliberately does not call.
    // Guide articles are the one exception, because the guides API returns each translation's
    // real publication date; "guide articles" below holds them to it. This assertion is scoped
    // to the static routes accordingly, and runs with an article present so that the split is
    // tested rather than assumed.
    vi.mocked(guideSitemapEntries).mockResolvedValue([translation("narita-to-tokyo", "en")]);
    const withArticle = await sitemap();
    const staticEntries = withArticle.filter((entry) => STATIC_URLS.has(entry.url));
    expect(staticEntries).toHaveLength(STATIC_URLS.size);
    expect(withArticle).toHaveLength(STATIC_URLS.size + 1);
    for (const entry of staticEntries) expect(entry.lastModified).toBeUndefined();
  });

  it("uses absolute URLs on the canonical origin", () => {
    for (const entry of entries) expect(entry.url.startsWith(`${siteUrl}/`)).toBe(true);
  });

  it("gives every entry all five locales plus x-default", () => {
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

  it("leaves out routes that are still noindex", () => {
    // Managed documents are noindex until published; explore, pet-friendly and community send an
    // empty shell. Listing any of them would only collect "Excluded by noindex".
    const paths = SITEMAP_ROUTES.map((route) => route.path);
    for (const path of ["/about", "/privacy", "/terms", "/contact", "/explore", "/explore/collections", "/pet-friendly"]) {
      expect(paths).not.toContain(path);
    }
  });

  it("carries every public destination", () => {
    const paths = SITEMAP_ROUTES.map((route) => route.path);
    expect(paths).toContain("/destinations/tokyo/services");
    expect(paths.filter((path) => path.startsWith("/destinations/")).length).toBeGreaterThanOrEqual(33);
  });
});

describe("guide articles", () => {
  // Rows as the API sends them: newest first, one per published translation. Deliberately uneven
  // so that no two articles share an alternate set: a notice in Traditional Chinese and Japanese
  // but not English, a how-to in Korean and English, and a how-to in English alone.
  const rows: GuideSitemapEntry[] = [
    translation("jr-pass-price-change", "zh-TW", { kind: "intel", published_at: "2026-09-10T08:30:00Z" }),
    translation("jr-pass-price-change", "ja", { kind: "intel", published_at: "2026-09-09T02:15:00Z" }),
    translation("narita-to-tokyo", "ko", { published_at: "2026-09-06T00:00:00Z" }),
    translation("narita-to-tokyo", "en", { published_at: "2026-09-05T12:00:00Z" }),
    translation("suica-on-iphone", "en"),
  ];
  const publishedLocales: Record<string, Locale[]> = {
    "/guides/intel/jr-pass-price-change": ["ja", "zh-TW"],
    "/guides/howto/narita-to-tokyo": ["en", "ko"],
    "/guides/howto/suica-on-iphone": ["en"],
  };
  const pathOf = (row: GuideSitemapEntry) => `/guides/${row.kind}/${row.slug}`;
  let staticOnly: Awaited<ReturnType<typeof sitemap>>;

  beforeEach(async () => {
    vi.mocked(getSiteVisibility).mockReset().mockResolvedValue({ status: "ready", features: openSiteVisibility });
    vi.mocked(guideSitemapEntries).mockReset().mockResolvedValue([]);
    staticOnly = await sitemap();
    vi.mocked(guideSitemapEntries).mockResolvedValue(rows);
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  /** The article entries: everything after the static prefix. */
  const articleEntries = async () => (await sitemap()).slice(staticOnly.length);

  it("keeps the static routes first and exactly as they were", async () => {
    const all = await sitemap();
    expect(all.slice(0, staticOnly.length)).toEqual(staticOnly);
    expect(all).toHaveLength(staticOnly.length + rows.length);
  });

  it("lists one entry per published translation and none for the others", async () => {
    const urls = (await articleEntries()).map((entry) => entry.url);
    expect(urls).toEqual(rows.map((row) => localeUrl(row.locale, pathOf(row))));
    for (const [path, published] of Object.entries(publishedLocales)) {
      for (const locale of locales.filter((value) => !published.includes(value))) {
        expect(urls).not.toContain(localeUrl(locale, path));
      }
    }
  });

  it("gives each entry exactly its own article's published translations as alternates", async () => {
    const entries = await articleEntries();
    rows.forEach((row, index) => {
      const path = pathOf(row);
      const languages = (entries[index].alternates?.languages ?? {}) as Record<string, string>;
      expect(Object.keys(languages).filter((key) => key !== "x-default").sort()).toEqual(publishedLocales[path]);
      for (const locale of publishedLocales[path]) expect(languages[locale]).toBe(localeUrl(locale, path));
    });
  });

  it("offers x-default only when the English translation is published", async () => {
    const entries = await articleEntries();
    rows.forEach((row, index) => {
      const path = pathOf(row);
      const languages = (entries[index].alternates?.languages ?? {}) as Record<string, string>;
      expect(languages["x-default"]).toBe(publishedLocales[path].includes("en") ? localeUrl("en", path) : undefined);
    });
  });

  it("dates each entry with the publication date the API returned", async () => {
    expect((await articleEntries()).map((entry) => entry.lastModified)).toEqual(rows.map((row) => new Date(row.published_at)));
  });

  it("adds no duplicate URL to the static list, even if the API repeated a row", async () => {
    vi.mocked(guideSitemapEntries).mockResolvedValue([...rows, rows[0]]);
    const urls = (await sitemap()).map((entry) => entry.url);
    expect(new Set(urls).size).toBe(urls.length);
    expect(urls).toHaveLength(staticOnly.length + rows.length);
  });

  it.each([
    { failure: "rejects", stub: () => vi.fn().mockRejectedValue(new TypeError("fetch failed")) },
    { failure: "answers HTTP 500", stub: () => vi.fn().mockResolvedValue({ ok: false, status: 500, json: async () => ({ detail: "boom" }) }) },
  ])("leaves exactly the static list when the guides fetch $failure", async ({ stub }) => {
    vi.mocked(guideSitemapEntries).mockImplementation(await realGuideSitemapEntries());
    const fetchMock = stub();
    vi.stubGlobal("fetch", fetchMock);
    expect(await sitemap()).toEqual(staticOnly);
    // A guard on the guard: the real loader ran and asked the right endpoint, so this is not the
    // mock's empty default passing in its place.
    expect(String(fetchMock.mock.calls[0][0])).toMatch(/\/api\/v1\/guides\/sitemap$/);
  });

  it("truncates entries beyond the cap", async () => {
    vi.mocked(guideSitemapEntries).mockImplementation(await realGuideSitemapEntries());
    const flood = Array.from({ length: GUIDE_SITEMAP_LIMIT + 5 }, (_, index) => translation(`guide-${index}`, "en"));
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ ok: true, json: async () => ({ entries: flood }) }));
    const articles = (await sitemap()).slice(staticOnly.length);
    expect(articles).toHaveLength(GUIDE_SITEMAP_LIMIT);
    // Rows arrive newest first, so the ones kept are the head of the list.
    expect(articles[GUIDE_SITEMAP_LIMIT - 1].url).toBe(localeUrl("en", `/guides/howto/guide-${GUIDE_SITEMAP_LIMIT - 1}`));
  });
});
