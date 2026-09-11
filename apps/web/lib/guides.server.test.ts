import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
const { incoming } = vi.hoisted(() => ({ incoming: vi.fn() }));
// The loaders read the visitor's address out of the request so the API can meter reads
// per source. Nothing here depends on the value; it just has to be readable.
vi.mock("next/headers", () => ({ headers: incoming }));
incoming.mockResolvedValue(new Headers({ "x-forwarded-for": "203.0.113.9" }));
import { loadGuideArticle, loadGuideList, loadGuideTopics } from "./guides.server";

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
