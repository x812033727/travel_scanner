import { afterEach, describe, expect, it, vi } from "vitest";
const { incoming } = vi.hoisted(() => ({ incoming: vi.fn() }));
// The loaders read the visitor's address out of the request so the API can meter reads
// per source. Nothing here depends on the value; it just has to be readable.
vi.mock("next/headers", () => ({ headers: incoming }));
incoming.mockResolvedValue(new Headers({ "x-forwarded-for": "203.0.113.9" }));
import { loadInitialFoods } from "./foods.server";

const cities = { countries: [{ code: "JP", name: "日本", cities: [] }] };
const categories = { items: [{ slug: "ramen", name: "拉麵" }] };
const merchants = { items: [{ id: "1", name: "一蘭" }], next_cursor: null };

afterEach(() => { vi.unstubAllGlobals(); vi.unstubAllEnvs(); });

function stub(...payloads: unknown[]) {
  const fetch = vi.fn();
  for (const payload of payloads) fetch.mockResolvedValueOnce(new Response(JSON.stringify(payload)));
  vi.stubGlobal("fetch", fetch);
  vi.stubEnv("API_INTERNAL_URL", "http://api.test");
  return fetch;
}

describe("loadInitialFoods", () => {
  it("hands the merchant list to the server render, not just the filters", async () => {
    // /foods used to server-render the city and category pickers over an empty list: the
    // merchants themselves arrived in a useEffect, so a crawler saw filter controls and nothing
    // to filter.
    const fetch = stub(cities, categories, merchants);
    const initial = await loadInitialFoods("zh-TW");
    expect(initial.merchants).toEqual(merchants);
    expect(fetch.mock.calls.map((call) => call[0])).toEqual([
      "http://api.test/api/v1/foods/cities",
      "http://api.test/api/v1/foods/categories",
      "http://api.test/api/v1/foods/merchants?limit=20",
    ]);
  });

  it("keeps moderated lists and counts fresh with a bounded request", async () => {
    const fetch = stub(cities, categories, merchants);
    await loadInitialFoods("en");
    const options = fetch.mock.calls.map((call) => call[1]);
    for (const option of options) {
      expect(option.cache).toBe("no-store");
      expect(option).not.toHaveProperty("next");
      expect(option.signal).toBeInstanceOf(AbortSignal);
      expect(option.headers).toMatchObject({ "X-Travel-Locale": "en" });
    }
  });

  it("requests the same normalized filters as the server-rendered controls", async () => {
    const fetch = stub(cities, categories, merchants);
    await loadInitialFoods("en", { destinationId: "tokyo", area: "shibuya", category: "ramen", style: "artsy", query: "tea & cakes" });
    const query = new URL(fetch.mock.calls[2][0]).searchParams;
    expect(Object.fromEntries(query)).toEqual({ destination_id: "tokyo", area: "shibuya", category: "ramen", style: "artsy", q: "tea & cakes", limit: "20" });
  });

  it("gives up the whole seed when the city list is unavailable", async () => {
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new Error("offline")));
    expect(await loadInitialFoods("en")).toEqual({ cities: null, categories: null, merchants: null });
  });

  it("still seeds cities and merchants when only the categories call fails", async () => {
    const fetch = vi.fn()
      .mockResolvedValueOnce(new Response(JSON.stringify(cities)))
      .mockResolvedValueOnce(new Response("nope", { status: 500 }))
      .mockResolvedValueOnce(new Response(JSON.stringify(merchants)));
    vi.stubGlobal("fetch", fetch);
    const initial = await loadInitialFoods("en");
    expect(initial.cities).toEqual(cities);
    expect(initial.categories).toBeNull();
    expect(initial.merchants).toEqual(merchants);
  });

  it("keeps a valid merchant seed when only the city list fails", async () => {
    vi.stubGlobal("fetch", vi.fn()
      .mockResolvedValueOnce(new Response("unavailable", { status: 503 }))
      .mockResolvedValueOnce(new Response(JSON.stringify(categories)))
      .mockResolvedValueOnce(new Response(JSON.stringify(merchants))));
    expect(await loadInitialFoods("en")).toEqual({ cities: null, categories, merchants });
  });

  it("asks again after a moderation change instead of reusing a previous response", async () => {
    const fetch = vi.fn(async (input: string) => new Response(JSON.stringify(
      input.includes("/merchants?") ? merchants : categories,
    )));
    vi.stubGlobal("fetch", fetch);
    expect((await loadInitialFoods("en")).merchants).toEqual(merchants);
    fetch.mockImplementation(async () => new Response(JSON.stringify({ items: [] })));
    expect((await loadInitialFoods("en")).merchants).toEqual({ items: [] });
    expect(fetch).toHaveBeenCalledTimes(6);
  });
});
