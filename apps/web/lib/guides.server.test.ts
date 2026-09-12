import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
const { incoming } = vi.hoisted(() => ({ incoming: vi.fn() }));
// The loaders read the visitor's address out of the request so the API can meter reads
// per source. Nothing here depends on the value; it just has to be readable.
vi.mock("next/headers", () => ({ headers: incoming }));
incoming.mockResolvedValue(new Headers({ "x-forwarded-for": "203.0.113.9" }));
import {
  guideSitemapEntries,
  loadGuideArticle,
  loadGuideList,
  loadGuideTopics,
  SITEMAP_GUIDE_ENTRY_LIMIT,
} from "./guides.server";

const article = {
  slug: "narita-to-tokyo", kind: "howto", locale: "zh-TW", status: "published",
  destination_id: "tokyo", destination_label: "東京",
  topics: [{ slug: "transport", label: "交通" }], valid_until: null, expired: false,
  document: {
    title: "怎麼走", description: "三種選擇", version: 2, published_at: "2026-09-01T00:00:00Z",
    blocks: [{ type: "paragraph", text: "Skyliner 最快。" }], sources: [],
  },
  published_locales: ["zh-TW", "ja"],
};

const summary = {
  slug: "narita-to-tokyo", kind: "howto", destination_id: "tokyo", destination_label: "東京",
  topics: [{ slug: "transport", label: "交通" }], title: "怎麼走", description: "三種選擇",
  published_at: "2026-09-01T00:00:00Z", valid_until: null, featured: false,
};

function respond(body: unknown, ok = true) {
  return vi.fn().mockResolvedValue({ ok, json: async () => body });
}

beforeEach(() => {
  vi.stubGlobal("fetch", respond({}));
});

afterEach(() => {
  vi.unstubAllGlobals();
});

describe("request discipline", () => {
  it("never caches a moderated listing and gives up rather than hanging the page", async () => {
    const fetchMock = respond({ articles: [], next_cursor: null });
    vi.stubGlobal("fetch", fetchMock);
    await loadGuideList("zh-TW");
    const [, init] = fetchMock.mock.calls[0];
    expect(init.cache).toBe("no-store");
    expect(init.signal).toBeInstanceOf(AbortSignal);
    expect(init.headers["X-Travel-Locale"]).toBe("zh-TW");
  });

  it("passes the filters through as query parameters", async () => {
    const fetchMock = respond({ articles: [], next_cursor: null });
    vi.stubGlobal("fetch", fetchMock);
    await loadGuideList("ja", { kind: "intel", topic: "transport", cursor: "abc" }, 5);
    const url = new URL(fetchMock.mock.calls[0][0]);
    expect(url.pathname).toBe("/api/v1/guides");
    expect(url.searchParams.get("kind")).toBe("intel");
    expect(url.searchParams.get("topic")).toBe("transport");
    expect(url.searchParams.get("cursor")).toBe("abc");
    expect(url.searchParams.get("limit")).toBe("5");
    expect(url.searchParams.get("locale")).toBe("ja");
  });
});

describe("a failing or malformed API", () => {
  it("degrades a listing to empty rather than throwing", async () => {
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new Error("connection reset")));
    await expect(loadGuideList("zh-TW")).resolves.toEqual({ articles: [], next_cursor: null });
    await expect(loadGuideTopics("zh-TW")).resolves.toEqual([]);
  });

  it("drops rows that do not match the contract instead of rendering them", async () => {
    vi.stubGlobal("fetch", respond({
      articles: [summary, { slug: "broken" }],
      next_cursor: null,
    }));
    const list = await loadGuideList("zh-TW");
    expect(list.articles).toHaveLength(1);
    expect(list.articles[0].slug).toBe("narita-to-tokyo");
  });

  it("calls an article unavailable when the API answers 500", async () => {
    vi.stubGlobal("fetch", respond(null, false));
    const state = await loadGuideArticle("howto", "narita-to-tokyo", "zh-TW");
    expect(state.status).toBe("unavailable");
    expect(state.document).toBeNull();
  });

  it("refuses to render a published article whose body is unreadable", async () => {
    vi.stubGlobal("fetch", respond({ ...article, document: { title: "怎麼走" } }));
    const state = await loadGuideArticle("howto", "narita-to-tokyo", "zh-TW");
    expect(state.status).toBe("unavailable");
  });

  it("ignores a response for a different article or locale", async () => {
    vi.stubGlobal("fetch", respond({ ...article, slug: "something-else" }));
    expect((await loadGuideArticle("howto", "narita-to-tokyo", "zh-TW")).status).toBe("unavailable");
    vi.stubGlobal("fetch", respond({ ...article, locale: "ja" }));
    expect((await loadGuideArticle("howto", "narita-to-tokyo", "zh-TW")).status).toBe("unavailable");
  });
});

describe("per-locale publication", () => {
  it("reports an unwritten translation as unpublished, not as a fault", async () => {
    vi.stubGlobal("fetch", respond({
      slug: "narita-to-tokyo", kind: "howto", locale: "ko", status: "unpublished",
      document: null, published_locales: ["zh-TW", "ja"],
    }));
    const state = await loadGuideArticle("howto", "narita-to-tokyo", "ko");
    expect(state.status).toBe("unpublished");
    expect(state.document).toBeNull();
    expect(state.published_locales).toEqual(["zh-TW", "ja"]);
  });

  it("keeps only real locales, so hreflang cannot advertise a made-up one", async () => {
    vi.stubGlobal("fetch", respond({ ...article, published_locales: ["zh-TW", "ja", "xx", 7] }));
    const state = await loadGuideArticle("howto", "narita-to-tokyo", "zh-TW");
    expect(state.published_locales).toEqual(["zh-TW", "ja"]);
  });

  it("carries the expiry flag through so the page can date the notice", async () => {
    vi.stubGlobal("fetch", respond({ ...article, kind: "intel", expired: true, valid_until: "2026-08-01" }));
    const state = await loadGuideArticle("intel", "narita-to-tokyo", "zh-TW");
    expect(state.status).toBe("published");
    expect(state.expired).toBe(true);
    expect(state.valid_until).toBe("2026-08-01");
  });
});

describe("the sitemap enumeration", () => {
  const rows = [
    { kind: "howto", slug: "narita-to-tokyo", locale: "zh-TW", published_at: "2026-09-01T00:00:00Z" },
    { kind: "howto", slug: "narita-to-tokyo", locale: "ja", published_at: "2026-09-02T00:00:00Z" },
    { kind: "intel", slug: "jr-pass-sale", locale: "en", published_at: "2026-09-10T00:00:00Z" },
  ];

  it("tells each row which locales its article is published in", async () => {
    vi.stubGlobal("fetch", respond({ entries: rows }));
    const entries = await guideSitemapEntries();
    expect(entries).toHaveLength(3);
    const narita = entries.filter((entry) => entry.slug === "narita-to-tokyo");
    for (const entry of narita) expect(entry.locales).toEqual(["ja", "zh-TW"]);
    expect(entries.find((entry) => entry.slug === "jr-pass-sale")!.locales).toEqual(["en"]);
  });

  it("orders the alternates by the site's locale list, not the API's row order", async () => {
    vi.stubGlobal("fetch", respond({ entries: [...rows].reverse() }));
    const entries = await guideSitemapEntries();
    for (const entry of entries.filter((row) => row.slug === "narita-to-tokyo")) {
      expect(entry.locales).toEqual(["ja", "zh-TW"]);
    }
  });

  it("drops a malformed row instead of putting a broken URL in the sitemap", async () => {
    vi.stubGlobal("fetch", respond({
      entries: [
        ...rows,
        { kind: "recipes", slug: "not-a-section", locale: "zh-TW", published_at: "2026-09-01T00:00:00Z" },
        { kind: "howto", slug: "no-locale", locale: "xx", published_at: "2026-09-01T00:00:00Z" },
        { kind: "howto", slug: "no-date", locale: "en" },
        { kind: "howto", locale: "en", published_at: "2026-09-01T00:00:00Z" },
        // Next writes <loc> and every alternate href unescaped, so a slug outside the grammar the
        // API enforces on write costs the whole document rather than one URL.
        { kind: "howto", slug: "fares&rules", locale: "en", published_at: "2026-09-01T00:00:00Z" },
        { kind: "howto", slug: "Narita-To-Tokyo", locale: "en", published_at: "2026-09-01T00:00:00Z" },
        { kind: "howto", slug: "", locale: "en", published_at: "2026-09-01T00:00:00Z" },
        // A date that does not parse reaches Next as an Invalid Date, which is truthy and is a
        // Date, so its serialiser calls toISOString() and throws: a 500 on /sitemap.xml.
        { kind: "howto", slug: "bad-date", locale: "en", published_at: "sometime" },
      ],
    }));
    const entries = await guideSitemapEntries();
    expect(entries).toHaveLength(3);
    expect(entries.some((entry) => entry.slug.startsWith("no-"))).toBe(false);
    expect(entries.some((entry) => String(entry.kind) === "recipes")).toBe(false);
    expect(entries.some((entry) => entry.slug === "bad-date")).toBe(false);
    for (const entry of entries) expect(entry.slug).toMatch(/^[a-z0-9]+(?:-[a-z0-9]+)*$/);
  });

  it("returns nothing rather than an exception when the API is unreachable", async () => {
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new Error("connection reset")));
    await expect(guideSitemapEntries()).resolves.toEqual([]);
    vi.stubGlobal("fetch", respond(null, false));
    await expect(guideSitemapEntries()).resolves.toEqual([]);
    vi.stubGlobal("fetch", respond({ entries: "not-an-array" }));
    await expect(guideSitemapEntries()).resolves.toEqual([]);
  });

  it("caps the list so one large response cannot dominate the sitemap", async () => {
    const many = Array.from({ length: SITEMAP_GUIDE_ENTRY_LIMIT + 25 }, (_, index) => ({
      kind: "intel", slug: `deal-${index}`, locale: "zh-TW", published_at: "2026-09-01T00:00:00Z",
    }));
    vi.stubGlobal("fetch", respond({ entries: many }));
    const entries = await guideSitemapEntries();
    expect(entries).toHaveLength(SITEMAP_GUIDE_ENTRY_LIMIT);
    // Which rows survive matters as much as how many. The API orders newest first, so a cap that
    // kept the tail would discard exactly the articles it exists to keep, and a count-only
    // assertion passes either way.
    expect(entries[0].slug).toBe("deal-0");
    expect(entries[SITEMAP_GUIDE_ENTRY_LIMIT - 1].slug).toBe(`deal-${SITEMAP_GUIDE_ENTRY_LIMIT - 1}`);
  });

  it("does not cache a list an editor can withdraw from", async () => {
    const fetchMock = respond({ entries: [] });
    vi.stubGlobal("fetch", fetchMock);
    await guideSitemapEntries();
    const [url, init] = fetchMock.mock.calls[0];
    // This path appears once on the web side, at the call site, so nothing else would catch a
    // typo in it until a crawler did.
    expect(new URL(url).pathname).toBe("/api/v1/guides/sitemap");
    expect(init.cache).toBe("no-store");
  });
});
