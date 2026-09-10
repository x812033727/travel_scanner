import { afterEach, describe, expect, it, vi } from "vitest";
import { loadInitialHotspots } from "./hotspots.server";

const ranking = { items: [{ id: "1", name: "淺草寺" }] };
const facets = { countries: [], cities: [], areas: [] };

afterEach(() => { vi.unstubAllGlobals(); vi.unstubAllEnvs(); });

describe("loadInitialHotspots", () => {
  it("caches the public ranking rather than going back to origin every request", async () => {
    const fetch = vi.fn()
      .mockResolvedValueOnce(new Response(JSON.stringify(ranking)))
      .mockResolvedValueOnce(new Response(JSON.stringify(facets)));
    vi.stubGlobal("fetch", fetch);
    vi.stubEnv("API_INTERNAL_URL", "http://api.test");

    expect((await loadInitialHotspots("ja")).ranking).toEqual(ranking);
    for (const call of fetch.mock.calls) {
      expect(call[1]).toMatchObject({ next: { revalidate: 900 }, headers: { "X-Travel-Locale": "ja" } });
      expect(call[1]).not.toHaveProperty("cache");
    }
  });

  it("passes the reader's filters through to the ranking query", async () => {
    const fetch = vi.fn().mockResolvedValue(new Response(JSON.stringify(ranking)));
    vi.stubGlobal("fetch", fetch);
    vi.stubEnv("API_INTERNAL_URL", "http://api.test");
    await loadInitialHotspots("en", { destinationId: "tokyo", area: "shinjuku", category: "food" });
    const url = String(fetch.mock.calls[0][0]);
    expect(url).toContain("destination_id=tokyo");
    expect(url).toContain("area=shinjuku");
    expect(url).toContain("category=food");
  });

  it("reports an unreachable ranking as empty so the page still renders", async () => {
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new Error("offline")));
    expect(await loadInitialHotspots("en")).toEqual({ ranking: null, facets: null });
  });
});
