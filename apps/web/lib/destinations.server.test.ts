import { afterEach, describe, expect, it, vi } from "vitest";
import { loadDestination, loadDestinations, loadMerchants, loadPlaces } from "./destinations.server";

const tokyo = {
  id: "tokyo", code: "NRT", city: "東京", local_name: "東京", english_name: "Tokyo",
  country: "日本", country_code: "JP", role: "primary", parent_destination_id: null,
  extension_ids: ["yokohama", "kamakura"], areas: ["新宿", "澀谷"],
  recommended_days: { min: 4, max: 6 }, timezone: "Asia/Tokyo", currency: "JPY",
  center: { latitude: 35.68, longitude: 139.76 }, reason: "第一次去日本最順的城市。", searchable: true,
};

const respond = (payload: unknown) => vi.fn().mockResolvedValue(new Response(JSON.stringify(payload)));

afterEach(() => { vi.unstubAllGlobals(); vi.unstubAllEnvs(); });

describe("loadDestinations", () => {
  it("asks the API in the reader's locale and caches instead of going back every request", async () => {
    const fetch = respond({ total: 1, items: [tokyo] });
    vi.stubGlobal("fetch", fetch);
    vi.stubEnv("API_INTERNAL_URL", "http://api.test/");

    const rows = await loadDestinations("ja");
    expect(rows).toHaveLength(1);
    expect(rows?.[0]).toMatchObject({
      id: "tokyo", city: "東京", country: "日本", localName: "東京", englishName: "Tokyo",
      areas: ["新宿", "澀谷"], recommendedDays: { min: 4, max: 6 },
      center: { latitude: 35.68, longitude: 139.76 }, extensionIds: ["yokohama", "kamakura"],
    });
    // None of this is personalized, and a round trip per request lands in TTFB and so in LCP.
    expect(fetch).toHaveBeenCalledWith(
      "http://api.test/api/v1/destinations",
      expect.objectContaining({
        next: { revalidate: 3600 },
        headers: { Accept: "application/json", "X-Travel-Locale": "ja" },
      }),
    );
  });

  it("drops rows with no id or no name rather than rendering a blank card", async () => {
    vi.stubGlobal("fetch", respond({ items: [tokyo, { id: "broken" }, { city: "No id" }] }));
    expect(await loadDestinations("en")).toHaveLength(1);
  });

  it.each([
    ["a transport failure", vi.fn().mockRejectedValue(new Error("offline"))],
    ["an error status", vi.fn().mockResolvedValue(new Response("nope", { status: 503 }))],
    ["an empty catalog", respond({ items: [] })],
    ["an unexpected shape", respond({ items: "not-an-array" })],
  ])("reports %s as no catalog, so the caller can decide", async (_label, fetch) => {
    vi.stubGlobal("fetch", fetch);
    expect(await loadDestinations("en")).toBeNull();
  });
});

describe("loadDestination", () => {
  it("finds one destination and reports an unknown id as missing", async () => {
    vi.stubGlobal("fetch", respond({ items: [tokyo] }));
    expect((await loadDestination("ja", "tokyo"))?.city).toBe("東京");
    expect(await loadDestination("ja", "atlantis")).toBeNull();
  });
});

describe("guide listings", () => {
  it("server-renders the ranked places, labelled by area", async () => {
    const fetch = respond({ items: [{ name: "淺草寺", area: { code: "asakusa", name: "上野／淺草" }, category: "landmark" }] });
    vi.stubGlobal("fetch", fetch);
    vi.stubEnv("API_INTERNAL_URL", "http://api.test");
    expect(await loadPlaces("zh-TW", "tokyo")).toEqual([{ name: "淺草寺", detail: "上野／淺草" }]);
    expect(fetch.mock.calls[0][0]).toBe("http://api.test/api/v1/hotspots/rankings?destination_id=tokyo&limit=12");
  });

  it("falls back to the category when a place has no area", async () => {
    vi.stubGlobal("fetch", respond({ items: [{ name: "Shibuya Sky", area: null, category: "viewpoint" }] }));
    expect(await loadPlaces("en", "tokyo")).toEqual([{ name: "Shibuya Sky", detail: "viewpoint" }]);
  });

  it("labels merchants by area, then by their first category", async () => {
    vi.stubGlobal("fetch", respond({
      items: [
        { name: "一蘭", area: { name: "新宿" }, categories: [{ name: "拉麵" }] },
        { name: "Nakamura", area: null, categories: [{ name: "Sushi" }] },
        { name: "No name at all", area: null, categories: [] },
      ],
    }));
    expect(await loadMerchants("zh-TW", "tokyo")).toEqual([
      { name: "一蘭", detail: "新宿" },
      { name: "Nakamura", detail: "Sushi" },
      { name: "No name at all", detail: null },
    ]);
  });

  it("returns an empty list when the listing is unreachable, so the guide still renders", async () => {
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new Error("offline")));
    expect(await loadPlaces("en", "tokyo")).toEqual([]);
    expect(await loadMerchants("en", "tokyo")).toEqual([]);
  });
});
