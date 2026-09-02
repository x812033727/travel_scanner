import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { HotspotRestaurantsPanel } from "./hotspot-restaurants-panel";

describe("HotspotRestaurantsPanel", () => {
  it("shows only qualified live restaurant data and safe external links", async () => {
    let searchCalls = 0;
    const fetchMock = vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
      if (String(input).endsWith("/restaurants/favorites")) {
        return new Response(JSON.stringify({ code: "authentication_required" }), { status: 401 });
      }
      searchCalls += 1;
      expect(init?.method).toBe("POST");
      expect(init?.headers).toMatchObject({ "Idempotency-Key": expect.any(String) });
      const body = JSON.parse(String(init?.body));
      expect(body).toMatchObject({
        radius_km: searchCalls === 1 ? 5 : 10,
        sort: "recommended",
      });
      return new Response(JSON.stringify({
        hotspot_id: "hotspot-1",
        hotspot_name: "平和紀念公園",
        radius_km: 5,
        sort: "recommended",
        filters: { min_rating: 3.8, min_review_count: 1000 },
        items: [{
          place_id: "ChIJ-food",
          name: "廣島燒名店",
          address: "日本廣島縣廣島市",
          latitude: 34.39712,
          longitude: 132.45531,
          distance_km: 1.25,
          rating: 4.6,
          review_count: 2345,
          recommendation_score: 4.42,
          opening_hours: ["週一: 11:00–22:00"],
          open_now: true,
          official_website_url: "https://restaurant.example/",
          google_maps_url: "https://maps.google.com/?cid=1",
          plus_code: "9FW3+5C 廣島市 日本廣島縣",
          primary_type: "japanese_restaurant",
          observed_at: "2026-09-01T12:00:00Z",
          editorial: null,
        }],
        next_cursor: null,
        coverage: { status: "completed", cells_completed: 7, cells_total: 7, candidate_count: 42 },
        observed_at: "2026-09-01T12:00:00Z",
        attribution: "Google Maps",
        persistence: {
          place_id: "durable",
          generated_maps_url: "durable",
          location_cache_ttl_days: 30,
          other_google_fields: "live_only",
        },
      }));
    });
    vi.stubGlobal("fetch", fetchMock);

    render(<HotspotRestaurantsPanel hotspot={{ id: "hotspot-1", name: "平和紀念公園" }} onClose={vi.fn()} />);

    expect(await screen.findByRole("heading", { name: "平和紀念公園 附近吃什麼" })).toBeTruthy();
    expect(await screen.findByRole("heading", { name: "廣島燒名店" })).toBeTruthy();
    expect(screen.getByText("4.6")).toBeTruthy();
    expect(screen.getByText("2,345")).toBeTruthy();
    expect(screen.getByText(/9FW3\+5C/)).toBeTruthy();
    expect(screen.getByText("34.39712, 132.45531")).toBeTruthy();
    expect(screen.getByText(/3.8 以上且至少 1,000/)).toBeTruthy();
    const map = screen.getByRole("link", { name: /Google Maps/ });
    const website = screen.getByRole("link", { name: /官方網站/ });
    expect(map.getAttribute("target")).toBe("_blank");
    expect(map.getAttribute("rel")).toContain("noopener");
    expect(website.getAttribute("href")).toBe("https://restaurant.example/");

    const sort = screen.getByLabelText("排序方式") as HTMLSelectElement;
    fireEvent.change(sort, { target: { value: "rating" } });
    expect(sort.value).toBe("rating");
    expect(searchCalls).toBe(1);

    const radius = screen.getByLabelText("搜尋範圍") as HTMLSelectElement;
    fireEvent.change(radius, { target: { value: "10" } });
    expect(radius.value).toBe("10");
    await waitFor(() => expect(searchCalls).toBe(2));
  });

  it("shows a sign-in action without retrying when the session expires", async () => {
    const fetchMock = vi.fn(async (input: RequestInfo | URL) => {
      if (String(input).endsWith("/restaurants/favorites")) {
        return new Response(JSON.stringify({ place_ids: [] }));
      }
      return new Response(
        JSON.stringify({ code: "authentication_required", message: "請先登入" }),
        { status: 401 },
      );
    });
    vi.stubGlobal("fetch", fetchMock);

    render(
      <HotspotRestaurantsPanel
        hotspot={{ id: "hotspot-1", name: "平和紀念公園" }}
        loginHref="/login?next=%2Fhotspots%3Fcategory%3Dfood"
        onClose={vi.fn()}
      />,
    );

    expect(await screen.findByText("登入已失效")).toBeTruthy();
    expect(screen.queryByRole("button", { name: "再試一次" })).toBeNull();
    expect(screen.getByRole("link", { name: "重新登入" }).getAttribute("href")).toBe(
      "/login?next=%2Fhotspots%3Fcategory%3Dfood",
    );
    expect(fetchMock.mock.calls.filter(([input]) => String(input).includes("restaurant-searches"))).toHaveLength(1);
  });
});
