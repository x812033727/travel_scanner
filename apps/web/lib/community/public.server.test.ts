import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

const { incoming, communityState } = vi.hoisted(() => ({ incoming: vi.fn(), communityState: vi.fn() }));
// The loaders forward the visitor's address so the API meters reads per source rather than
// per web container. Nothing here depends on the value; it only has to be readable.
vi.mock("next/headers", () => ({ headers: incoming }));
vi.mock("./server", () => ({ getCommunityState: communityState }));

import {
  loadPetPlace, loadPetPlaces, loadPost, loadPublicProfile, metaDescription,
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
