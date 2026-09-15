import { readdirSync } from "node:fs";
import { join } from "node:path";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { locales } from "@/i18n/routing";
import { siteUrl } from "@/lib/seo";
import { closedSiteVisibility, openSiteVisibility } from "@/lib/site-features";
import { guideSitemapEntries, guideTopicSitemapEntries, type GuideSitemapEntry } from "@/lib/guides.server";
import { getDiscoveryStatus } from "@/lib/discovery-status.server";
import { getSiteVisibility } from "@/lib/site-visibility.server";
import { getCommunityState } from "@/lib/community/server";
import { closedCommunity, type CommunityState } from "@/lib/community/types";
import sitemap, { dynamic, SITEMAP_ROUTES } from "./sitemap";

vi.mock("@/lib/site-visibility.server", () => ({ getSiteVisibility: vi.fn() }));
// Discovery is off in production, so that is the default here too: /explore is the one route
// listed behind it, and every count below is of the routes that do not depend on it.
vi.mock("@/lib/discovery-status.server", () => ({ getDiscoveryStatus: vi.fn() }));

/** The routes listed whatever the discovery and community switches say. */
const STATIC_ROUTES = SITEMAP_ROUTES.filter((route) => !route.discovery && !route.community);
// Defaulting to an unreadable enumeration is what keeps every assertion below about the
// static routes exactly as it was, including the whole-array comparison: with no complete
// publication picture every section hub stays listed in all five languages. The guide cases
// opt in, and the hub cases opt in to `complete` as well.
vi.mock("@/lib/guides.server", () => ({ guideSitemapEntries: vi.fn(), guideTopicSitemapEntries: vi.fn() }));
// The real module is `server-only`, and the community is off in production, so that is the
// default here too: /pet-friendly is the one route listed behind it.
vi.mock("@/lib/community/server", () => ({ getCommunityState: vi.fn() }));
const OPEN_COMMUNITY: CommunityState = { status: "ready", flags: { ...closedCommunity.flags, enabled: true } };

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

describe("sitemap", () => {
  let entries: Awaited<ReturnType<typeof sitemap>>;
  beforeEach(async () => {
    vi.mocked(getSiteVisibility).mockReset().mockResolvedValue({ status: "ready", features: openSiteVisibility });
    vi.mocked(guideSitemapEntries).mockReset().mockResolvedValue({ entries: [], complete: false });
    vi.mocked(guideTopicSitemapEntries).mockReset().mockResolvedValue([]);
    vi.mocked(getDiscoveryStatus).mockReset().mockResolvedValue({ enabled: false });
    vi.mocked(getCommunityState).mockReset().mockResolvedValue(closedCommunity);
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
    const open = await sitemap();
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
    const open = await sitemap();
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
    const closed = await sitemap();
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
  // Published in one locale only, so its entry must carry a single alternate and no x-default.
  const notes = {
    kind: "life" as const, slug: "ai-notes", published_at: "2026-09-05T08:00:00Z",
    locales: ["zh-TW"] as const,
  };
  const rows = [
    ...narita.locales.map((locale) => ({ ...narita, locale, locales: [...narita.locales] })),
    ...sale.locales.map((locale) => ({ ...sale, locale, locales: [...sale.locales] })),
    ...notes.locales.map((locale) => ({ ...notes, locale, locales: [...notes.locales] })),
  ];

  async function build(entries = rows, complete = false) {
    vi.mocked(getSiteVisibility).mockReset().mockResolvedValue({ status: "ready", features: openSiteVisibility });
    vi.mocked(guideSitemapEntries).mockReset().mockResolvedValue({ entries, complete });
    vi.mocked(guideTopicSitemapEntries).mockReset().mockResolvedValue([]);
    vi.mocked(getDiscoveryStatus).mockReset().mockResolvedValue({ enabled: false });
    vi.mocked(getCommunityState).mockReset().mockResolvedValue(closedCommunity);
    return sitemap();
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

  it("advertises only the translations that exist, each at its own URL", async () => {
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

  it("leaves the static routes first and untouched when articles are appended", async () => {
    // Every other static assertion in this file runs with the guides mocked to an empty list, so
    // a change that only shows up once the API returns rows would pass all of them.
    const staticOnly = await build([]);
    const all = await build();
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

  it("adds no duplicate URL alongside the static routes, even if a row repeats", async () => {
    // The fixture's four translations are already distinct, so without the repeated row this
    // assertion cannot fail and the property it names goes unchecked.
    const urls = (await build([...rows, rows[0]])).map((entry) => entry.url);
    expect(new Set(urls).size).toBe(urls.length);
    expect(urls).toHaveLength(STATIC_ROUTES.length * locales.length + rows.length);
  });

  it("keeps the static sitemap intact when the guides API is unreachable", async () => {
    const fallback = await build([]);
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
  const zhOnly: GuideSitemapEntry[] = [
    { kind: "intel", slug: "jr-pass-sale", locale: "zh-TW", published_at: "2026-09-10T00:00:00Z", locales: ["zh-TW"] },
    { kind: "howto", slug: "narita-to-tokyo", locale: "zh-TW", published_at: "2026-09-01T00:00:00Z", locales: ["zh-TW"] },
  ];

  async function build(entries: GuideSitemapEntry[], complete: boolean) {
    vi.mocked(getSiteVisibility).mockReset().mockResolvedValue({ status: "ready", features: openSiteVisibility });
    vi.mocked(guideSitemapEntries).mockReset().mockResolvedValue({ entries, complete });
    vi.mocked(getDiscoveryStatus).mockReset().mockResolvedValue({ enabled: false });
    return (await sitemap()).map((entry) => entry.url);
  }

  it("lists a hub only where its kinds have an article", async () => {
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
    const urls = await build([{ ...zhOnly[0], locale: "ja", locales: ["ja"] }], true);
    expect(urls).toContain(`${siteUrl}/ja/guides`);
    expect(urls).toContain(`${siteUrl}/ja/guides/intel`);
    expect(urls).not.toContain(`${siteUrl}/ja/guides/howto`);
  });

  it("advertises only the languages a hub is listed in, and x-default only with English", async () => {
    vi.mocked(getSiteVisibility).mockReset().mockResolvedValue({ status: "ready", features: openSiteVisibility });
    vi.mocked(guideSitemapEntries).mockReset().mockResolvedValue({ entries: zhOnly, complete: true });
    vi.mocked(getDiscoveryStatus).mockReset().mockResolvedValue({ enabled: false });
    const all = await sitemap();
    const hub = all.find((entry) => entry.url === `${siteUrl}/zh-TW/guides/intel`);
    // Pointing hreflang at /en/guides/intel would advertise the page this file just refused
    // to list, and the page itself answers noindex.
    expect(hub!.alternates?.languages).toEqual({ "zh-TW": `${siteUrl}/zh-TW/guides/intel` });
    const foods = all.find((entry) => entry.url === `${siteUrl}/zh-TW/foods`);
    expect(Object.keys(foods!.alternates?.languages ?? {}).sort()).toEqual([...locales, "x-default"].sort());
  });

  it("keeps every hub in every language when the enumeration is not complete", async () => {
    // An unreachable or capped read cannot tell an unpublished language from an unseen one.
    const urls = await build(zhOnly, false);
    for (const path of ["/guides", "/guides/intel", "/guides/howto", "/life"]) {
      for (const locale of locales) expect(urls).toContain(`${siteUrl}/${locale}${path}`);
    }
  });
});

describe("topic hubs in the sitemap", () => {
  const hubs = [
    { section: "life" as const, slug: "ai", locales: ["zh-TW", "en"] as ("zh-TW" | "en")[] },
    { section: "life" as const, slug: "ai-terms", locales: ["zh-TW"] as "zh-TW"[] },
    { section: "travel" as const, slug: "transport", locales: ["zh-TW", "ja"] as ("zh-TW" | "ja")[] },
  ];

  async function build() {
    vi.mocked(getSiteVisibility).mockReset().mockResolvedValue({ status: "ready", features: openSiteVisibility });
    vi.mocked(guideSitemapEntries).mockReset().mockResolvedValue({ entries: [], complete: false });
    vi.mocked(guideTopicSitemapEntries).mockReset().mockResolvedValue(hubs);
    vi.mocked(getDiscoveryStatus).mockReset().mockResolvedValue({ enabled: false });
    vi.mocked(getCommunityState).mockReset().mockResolvedValue(closedCommunity);
    return (await sitemap()).filter((entry) => new URL(entry.url).pathname.includes("/topics/"));
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
    vi.mocked(guideTopicSitemapEntries).mockResolvedValue([]);
    expect((await sitemap()).some((entry) => entry.url.includes("/topics/"))).toBe(false);
  });
});
