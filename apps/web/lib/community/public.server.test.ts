import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

const { incoming, communityState } = vi.hoisted(() => ({ incoming: vi.fn(), communityState: vi.fn() }));
// The loaders forward the visitor's address so the API meters reads per source rather than
// per web container. Nothing here depends on the value; it only has to be readable.
vi.mock("next/headers", () => ({ headers: incoming }));
vi.mock("./server", () => ({ getCommunityState: communityState }));

import {
  loadPetPlace, loadPetPlaces, loadPost, loadPublicProfile, metaDescription,
  PET_PLACE_SITEMAP_BUDGET_MS, PET_PLACE_SITEMAP_PAGE_LIMIT, PET_PLACE_SITEMAP_PAGE_SIZE, petPlaceSitemapEntries,
} from "./public.server";

const OPEN = { status: "ready", flags: { enabled: true, posting_enabled: true, comments_enabled: true, messaging_enabled: true, translation_enabled: true, pet_reports_enabled: true } };
const CLOSED = { status: "ready", flags: { ...OPEN.flags, enabled: false } };
const UNAVAILABLE = { status: "unavailable", flags: CLOSED.flags };

const place = { id: "p1", name: "Café Mocha", names: { "zh-TW": "摩卡咖啡" }, kind: "cafe", destination: "Tokyo" };
const post = { id: "s1", title: "Three days in Kyoto", author: { id: "a1", handle: "mei" } };
const profile = { id: "a1", handle: "mei", display_name: "Mei", bio: "Travels with a corgi." };

function answering(payload: unknown, status = 200) {
  const fetch = vi.fn().mockResolvedValue(new Response(JSON.stringify(payload), { status }));
  vi.stubGlobal("fetch", fetch);
  return fetch;
}

beforeEach(() => {
  incoming.mockResolvedValue(new Headers({ "x-forwarded-for": "203.0.113.9" }));
  communityState.mockResolvedValue(OPEN);
  vi.stubEnv("API_INTERNAL_URL", "http://api.test");
});
afterEach(() => { vi.unstubAllGlobals(); vi.unstubAllEnvs(); vi.clearAllMocks(); });

describe("the four public community reads", () => {
  it("fetches each record from its public endpoint without caching it", async () => {
    const fetch = answering({ items: [place] });
    await expect(loadPetPlaces("ja")).resolves.toEqual({ items: [place] });
    expect(fetch).toHaveBeenCalledWith(
      "http://api.test/api/v1/pet-friendly/places",
      expect.objectContaining({ cache: "no-store", headers: expect.objectContaining({ "X-Travel-Locale": "ja" }) }),
    );
    // A moderated record can be withdrawn between two reads, so nothing here may be revalidated.
    expect(fetch.mock.calls[0][1]).not.toHaveProperty("next");
    expect(fetch.mock.calls[0][1].signal).toBeInstanceOf(AbortSignal);
  });

  it("escapes the identifier rather than pasting it into the path", async () => {
    const fetch = answering(place);
    await loadPetPlace("en", "../../admin/places");
    expect(String(fetch.mock.calls[0][0])).toBe(
      "http://api.test/api/v1/pet-friendly/places/..%2F..%2Fadmin%2Fplaces",
    );
    answering(profile);
    await loadPublicProfile("en", "a b/c");
    expect(String(vi.mocked(globalThis.fetch).mock.calls[0][0])).toContain("/profiles/a%20b%2Fc");
  });

  it("reads posts and profiles from their own endpoints", async () => {
    answering(post);
    await expect(loadPost("en", "s1")).resolves.toEqual(post);
    expect(String(vi.mocked(globalThis.fetch).mock.calls[0][0])).toBe("http://api.test/api/v1/community/posts/s1");
    answering(profile);
    await expect(loadPublicProfile("en", "mei")).resolves.toEqual(profile);
  });
});

describe("what keeps a page out of the index", () => {
  it("reads nothing at all while the community switch is off", async () => {
    const fetch = answering({ items: [place] });
    communityState.mockResolvedValue(CLOSED);
    await expect(loadPetPlaces("en")).resolves.toBeNull();
    await expect(loadPost("en", "s1")).resolves.toBeNull();
    await expect(loadPublicProfile("en", "mei")).resolves.toBeNull();
    await expect(loadPetPlace("en", "p1")).resolves.toBeNull();
    expect(fetch).not.toHaveBeenCalled();
  });

  it("treats an unavailable community as closed", async () => {
    const fetch = answering(place);
    communityState.mockResolvedValue(UNAVAILABLE);
    await expect(loadPetPlace("en", "p1")).resolves.toBeNull();
    expect(fetch).not.toHaveBeenCalled();
  });

  it("reports a 404, an outage and a malformed payload alike as no content", async () => {
    answering({ detail: "community_not_found" }, 404);
    await expect(loadPost("en", "missing")).resolves.toBeNull();

    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new Error("offline")));
    await expect(loadPetPlaces("en")).resolves.toBeNull();

    // A problem document is still JSON. Without a shape check the route would publish a
    // title of "undefined" on a page it had just declared indexable.
    answering({ id: "s1" });
    await expect(loadPost("en", "s1")).resolves.toBeNull();
    answering({ items: [{ id: "p1" }] });
    await expect(loadPetPlaces("en")).resolves.toBeNull();
    answering({ id: "a1", handle: "mei" });
    await expect(loadPublicProfile("en", "mei")).resolves.toBeNull();
  });
});

describe("metaDescription", () => {
  it("flattens prose onto one line", () => {
    expect(metaDescription("  Kyoto\n\nin  autumn ")).toBe("Kyoto in autumn");
  });

  it("says nothing rather than publishing an empty description", () => {
    expect(metaDescription("")).toBeUndefined();
    expect(metaDescription(null)).toBeUndefined();
    expect(metaDescription("   \n ")).toBeUndefined();
  });

  it("truncates on a word boundary and marks the cut", () => {
    const cut = metaDescription(`${"word ".repeat(60)}`, 40);
    expect(cut).toBe("word word word word word word word…");
    expect(cut!.length).toBeLessThanOrEqual(40);
    expect(cut!.endsWith("…")).toBe(true);
    expect(cut).not.toContain("wor…");
  });

  it("cuts unspaced scripts by length, since there is no word boundary to find", () => {
    const cut = metaDescription("京都的秋天非常美麗而且遊客很多".repeat(20), 20);
    expect(cut!.length).toBeLessThanOrEqual(20);
    expect(cut!.endsWith("…")).toBe(true);
  });

  it("leaves a short description exactly as written", () => {
    expect(metaDescription("Travels with a corgi.")).toBe("Travels with a corgi.");
  });
});

describe("petPlaceSitemapEntries, the enumeration behind the sitemap", () => {
  const verified = { ...place, id: "p1", verified_at: "2026-09-01T09:30:00Z" };
  const undated = { ...place, id: "p2", verified_at: null };
  const first = { items: [verified, undated], next_cursor: "c1" };
  const last = { items: [{ ...place, id: "p3", verified_at: "2026-09-10T00:00:00Z" }], next_cursor: null };
  /** What the first page reads as: the id, and the date only where there was a real one. */
  const read = [{ id: "p1", verified_at: "2026-09-01T09:30:00Z" }, { id: "p2" }];

  /** Answers each call with a fresh Response for the next payload, repeating the last one. A
   *  Response body reads once, so `answering` above cannot serve two pages. */
  function answeringPages(...payloads: unknown[]) {
    let call = 0;
    const fetch = vi.fn().mockImplementation(
      async () => new Response(JSON.stringify(payloads[Math.min(call++, payloads.length - 1)])),
    );
    vi.stubGlobal("fetch", fetch);
    return fetch;
  }

  it("follows next_cursor through the public directory at the API's page maximum, verified places only", async () => {
    const fetch = answeringPages(first, last);
    await expect(petPlaceSitemapEntries()).resolves.toEqual({
      entries: [...read, { id: "p3", verified_at: "2026-09-10T00:00:00Z" }], complete: true,
    });
    // `include_uncertain` is the API's default, sent anyway: the set listed is the places whose
    // rules are verified, and that must not change under a change of default.
    expect(fetch.mock.calls.map((call) => String(call[0]))).toEqual([
      "http://api.test/api/v1/pet-friendly/places?limit=50&include_uncertain=false",
      "http://api.test/api/v1/pet-friendly/places?limit=50&include_uncertain=false&cursor=c1",
    ]);
    expect(PET_PLACE_SITEMAP_PAGE_SIZE).toBe(50);
    // The same treatment as the directory page's own read: no store, the locale header, and a
    // timeout on every page.
    for (const [, init] of fetch.mock.calls) {
      expect(init).toMatchObject({ cache: "no-store", headers: expect.objectContaining({ "X-Travel-Locale": "zh-TW" }) });
      expect(init).not.toHaveProperty("next");
      expect(init.signal).toBeInstanceOf(AbortSignal);
    }
  });

  it("reads nothing while the switch is off or unreadable, and that is complete", async () => {
    // Nothing is public, which is the truth and not a failure -- the same answer the directory
    // page gives, with no API call behind it.
    const fetch = answeringPages(first, last);
    communityState.mockResolvedValue(CLOSED);
    await expect(petPlaceSitemapEntries()).resolves.toEqual({ entries: [], complete: true });
    communityState.mockResolvedValue(UNAVAILABLE);
    await expect(petPlaceSitemapEntries()).resolves.toEqual({ entries: [], complete: true });
    expect(fetch).not.toHaveBeenCalled();
  });

  it("keeps the pages it read when a later one fails, and says the picture is not whole", async () => {
    const failures = [
      () => new Response("upstream", { status: 502 }),
      () => new Response(JSON.stringify({ detail: "community_unavailable" })),
      // A timed-out page rejects, as an aborted fetch does.
      () => Promise.reject(new DOMException("timed out", "TimeoutError")),
    ];
    for (const failure of failures) {
      vi.stubGlobal("fetch", vi.fn()
        .mockResolvedValueOnce(new Response(JSON.stringify(first)))
        .mockImplementationOnce(async () => failure()));
      await expect(petPlaceSitemapEntries()).resolves.toEqual({ entries: read, complete: false });
    }
    // A failed first page: nothing, and not complete -- an outage is not an empty directory.
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new Error("offline")));
    await expect(petPlaceSitemapEntries()).resolves.toEqual({ entries: [], complete: false });
  });

  it("stops at the page cap with a cursor still in hand", async () => {
    const full = {
      items: Array.from({ length: PET_PLACE_SITEMAP_PAGE_SIZE }, (_, index) => ({ ...place, id: `p${index}` })),
      next_cursor: "more",
    };
    const fetch = answeringPages(full);
    const result = await petPlaceSitemapEntries();
    expect(fetch).toHaveBeenCalledTimes(PET_PLACE_SITEMAP_PAGE_LIMIT);
    expect(result.entries).toHaveLength(PET_PLACE_SITEMAP_PAGE_LIMIT * PET_PLACE_SITEMAP_PAGE_SIZE);
    expect(result.complete).toBe(false);
    // Twenty pages of fifty: a thousand places, five sitemap rows each.
    expect(PET_PLACE_SITEMAP_PAGE_LIMIT).toBe(20);
  });

  it("gives up on the time budget before the page cap, and gives the last page only what is left", async () => {
    // Each page takes four seconds of a ten-second budget: the third starts with two left and
    // gets a two-second timeout rather than the usual three; a fourth never starts.
    expect(PET_PLACE_SITEMAP_BUDGET_MS).toBe(10_000);
    const step = 4_000;
    vi.useFakeTimers({ toFake: ["Date"] });
    const timeout = vi.spyOn(AbortSignal, "timeout");
    try {
      let call = 0;
      vi.stubGlobal("fetch", vi.fn().mockImplementation(async () => {
        vi.setSystemTime(Date.now() + step);
        const page = call++;
        return new Response(JSON.stringify({ items: [{ ...place, id: `p${page}` }], next_cursor: `c${page + 1}` }));
      }));
      await expect(petPlaceSitemapEntries()).resolves.toEqual({
        entries: [{ id: "p0" }, { id: "p1" }, { id: "p2" }], complete: false,
      });
      expect(globalThis.fetch).toHaveBeenCalledTimes(3);
      expect(timeout.mock.calls.map(([ms]) => ms)).toEqual([3000, 3000, PET_PLACE_SITEMAP_BUDGET_MS - 2 * step]);
    } finally {
      timeout.mockRestore();
      vi.useRealTimers();
    }
  });

  it("skips a row it cannot put into a URL, and a date it cannot parse, rather than the file", async () => {
    // Next writes the id into <loc> unescaped and calls toISOString() on the date, so a bad id
    // would cost the whole file and a bad date a 500; each here costs one row or one field.
    answeringPages({
      items: [
        { ...place, id: "a&b" }, { ...place, id: "../admin" }, { ...place, id: 42 }, { name: "no id" }, null,
        { ...place, id: "ok-1", verified_at: "yesterday" }, { ...place, id: "ok-2", verified_at: 1_700_000_000 },
      ],
      next_cursor: null,
    });
    await expect(petPlaceSitemapEntries()).resolves.toEqual({ entries: [{ id: "ok-1" }, { id: "ok-2" }], complete: true });
  });
});
