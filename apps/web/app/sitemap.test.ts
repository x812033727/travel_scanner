import { readdirSync } from "node:fs";
import { join } from "node:path";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { locales } from "@/i18n/routing";
import { siteUrl } from "@/lib/seo";
import { closedSiteVisibility, openSiteVisibility } from "@/lib/site-features";
import { guideSitemapEntries } from "@/lib/guides.server";
import { getSiteVisibility } from "@/lib/site-visibility.server";
import sitemap, { dynamic, SITEMAP_ROUTES } from "./sitemap";

vi.mock("@/lib/site-visibility.server", () => ({ getSiteVisibility: vi.fn() }));
// Defaulting to no articles is what keeps every assertion below about the static routes
// exactly as it was, including the whole-array comparison. The guide cases opt in.
vi.mock("@/lib/guides.server", () => ({ guideSitemapEntries: vi.fn() }));

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

describe("sitemap", () => {
  let entries: Awaited<ReturnType<typeof sitemap>>;
  beforeEach(async () => {
    vi.mocked(getSiteVisibility).mockReset().mockResolvedValue({ status: "ready", features: openSiteVisibility });
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

describe("guide articles in the sitemap", () => {
  const narita = {
    kind: "howto" as const, slug: "narita-to-tokyo", published_at: "2026-09-01T00:00:00Z",
    locales: ["zh-TW", "ja"] as const,
  };
  const sale = {
    kind: "intel" as const, slug: "jr-pass-sale", published_at: "2026-09-10T00:00:00Z",
    locales: ["zh-TW", "en"] as const,
  };
  const rows = [
    ...narita.locales.map((locale) => ({ ...narita, locale, locales: [...narita.locales] })),
    ...sale.locales.map((locale) => ({ ...sale, locale, locales: [...sale.locales] })),
  ];

  async function build(entries = rows) {
    vi.mocked(getSiteVisibility).mockReset().mockResolvedValue({ status: "ready", features: openSiteVisibility });
    vi.mocked(guideSitemapEntries).mockReset().mockResolvedValue(entries);
    return sitemap();
  }

  /** Articles only. `/guides/intel` and `/guides/howto` are static hub routes and belong to
   *  the checks above, so matching on "/guides/" alone would sweep them in here. */
  const guideEntries = (all: Awaited<ReturnType<typeof sitemap>>) =>
    all.filter((entry) => (entry.url.split("/guides/")[1] ?? "").includes("/"));

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

  it("advertises only the translations that exist", async () => {
    const guides = guideEntries(await build());
    const japanese = guides.find((entry) => entry.url.endsWith("/ja/guides/howto/narita-to-tokyo"));
    expect(Object.keys(japanese!.alternates!.languages!).sort()).toEqual(["ja", "zh-TW"]);
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

  it("adds no duplicate URL alongside the static routes", async () => {
    const urls = (await build()).map((entry) => entry.url);
    expect(new Set(urls).size).toBe(urls.length);
  });

  it("keeps the static sitemap intact when the guides API is unreachable", async () => {
    vi.mocked(guideSitemapEntries).mockReset().mockResolvedValue([]);
    const fallback = await build([]);
    expect(fallback.length).toBe(SITEMAP_ROUTES.length * locales.length);
    expect(guideEntries(fallback)).toEqual([]);
  });

  it("lists the section hubs, which are static routes and stay in the exact-array checks", () => {
    const paths = SITEMAP_ROUTES.map((route) => route.path);
    expect(paths).toContain("/guides");
    expect(paths).toContain("/guides/intel");
    expect(paths).toContain("/guides/howto");
    for (const path of ["/guides", "/guides/intel", "/guides/howto"]) {
      expect(routeExists(path), path).toBe(true);
    }
  });
});
