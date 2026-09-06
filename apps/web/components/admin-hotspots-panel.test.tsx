import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { AdminHotspotsPanel } from "./admin-hotspots-panel";

const item = {
  id: "11111111-1111-4111-8111-111111111111",
  name: "香港海洋公園",
  qid: "Q194776",
  destination_id: "hong-kong",
  city_code: "HKG",
  city_name: "香港",
  country_code: "HK",
  country_name: "香港",
  destination_role: "primary",
  parent_destination_id: null,
  category: "family",
  origin: "curated",
  status: "pending",
  reason: "map_identity_required",
  distance_km: 2,
  pageviews_30d: 19170,
  source_urls: ["https://www.oceanpark.com.hk/"],
  is_active: false,
  is_deep_travel: false,
  depth_kind: null,
  depth_score: null,
  depth_reason: null,
  access_minutes: null,
  recommended_duration_minutes: 360,
  latitude: 22.2467,
  longitude: 114.1757,
  coordinate_source_type: "official_tourism",
  coordinate_source_url: "https://www.oceanpark.com.hk/",
  google_place_id: "ChIJ-ocean-park",
  naver_map_url: null,
  map_match_status: "unverified",
};

const listing = {
  items: [item],
  total: 1,
  page: 1,
  pages: 1,
  facets: {
    countries: [{ code: "HK", name: "香港", count: 1 }],
    categories: [{ code: "family", count: 1 }],
  },
};

describe("AdminHotspotsPanel", () => {
  it("saves an exact reviewed place with durable coordinates", async () => {
    const fetchMock = vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      if (init?.method === "POST" && url.includes("/review")) {
        const body = JSON.parse(String(init.body));
        expect(body.google_place_id).toBe("ChIJ-ocean-park");
        expect(body.map_match_status).toBe("verified");
        expect(body.coordinate_source_url).toBe("https://www.oceanpark.com.hk/");
        return new Response(JSON.stringify({ updated: 1, status: "pending" }));
      }
      return new Response(JSON.stringify(listing));
    });
    vi.stubGlobal("fetch", fetchMock);

    render(<AdminHotspotsPanel />);
    expect(await screen.findByText("香港海洋公園")).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "編輯地點" }));
    fireEvent.change(screen.getByLabelText("比對狀態"), { target: { value: "verified" } });
    fireEvent.click(screen.getByRole("button", { name: "儲存地點" }));
    expect(await screen.findByText("已儲存精準地點。")).toBeTruthy();
    await waitFor(() => expect(fetchMock).toHaveBeenCalled());
  });

  it("groups candidates by country and city, filters by category, and selects a group", async () => {
    const fetchMock = vi.fn<(input: RequestInfo | URL, init?: RequestInit) => Promise<Response>>(
      async () => new Response(JSON.stringify(listing)),
    );
    vi.stubGlobal("fetch", fetchMock);

    render(<AdminHotspotsPanel />);
    expect(await screen.findByText("香港海洋公園")).toBeTruthy();
    expect(screen.getByText(/香港 \(HK\) · 本頁 1 筆/)).toBeTruthy();
    expect(screen.getByText(/香港 \(HKG\) · hong-kong · 主要城市 · 本頁 1 筆/)).toBeTruthy();
    const firstUrl = String(fetchMock.mock.calls[0][0]);
    expect(firstUrl).toContain("limit=50");
    expect(firstUrl).toContain("page=1");

    // The filters start folded away: a reviewer clearing hundreds of rows needs the first
    // candidate on screen, not thirty controls above it.
    expect(screen.queryByRole("group", { name: "景點分類" })).toBeNull();
    fireEvent.click(screen.getByRole("button", { name: "展開篩選條件" }));

    const categories = screen.getByRole("group", { name: "景點分類" });
    const family = within(categories).getByRole("button", { name: /親子/ });
    expect(family.getAttribute("aria-pressed")).toBe("false");
    expect(within(categories).getByRole("button", { name: /海灘/ }).hasAttribute("disabled")).toBe(true);
    fireEvent.click(family);
    await waitFor(() =>
      expect(fetchMock.mock.calls.some(([input]) => String(input).includes("category=family"))).toBe(true),
    );
    expect(within(categories).getByRole("button", { name: /親子/ }).getAttribute("aria-pressed")).toBe("true");
    const countries = screen.getByRole("group", { name: "國家／地區" });
    expect(within(countries).getByRole("button", { name: /^香港/ })).toBeTruthy();

    fireEvent.click(screen.getByRole("checkbox", { name: "全選 香港（HKG）" }));
    expect((screen.getByRole("checkbox", { name: "選取 香港海洋公園" }) as HTMLInputElement).checked).toBe(true);
    expect((screen.getByRole("checkbox", { name: "全選 香港（HK）" }) as HTMLInputElement).checked).toBe(true);
    expect(screen.getByText("共 1 筆，已選 1 筆")).toBeTruthy();
    fireEvent.click(screen.getByRole("checkbox", { name: "全選 香港（HK）" }));
    expect((screen.getByRole("checkbox", { name: "選取 香港海洋公園" }) as HTMLInputElement).checked).toBe(false);
  });
  it("keeps the first candidate above the batch controls until something is selected", async () => {
    const fetchMock = vi.fn<(input: RequestInfo | URL, init?: RequestInit) => Promise<Response>>(
      async () => new Response(JSON.stringify(listing)),
    );
    vi.stubGlobal("fetch", fetchMock);

    render(<AdminHotspotsPanel />);
    expect(await screen.findByText("香港海洋公園")).toBeTruthy();
    expect(screen.queryByRole("button", { name: "核准" })).toBeNull();
    expect(screen.queryByRole("button", { name: "標記深度旅遊" })).toBeNull();

    fireEvent.click(screen.getByRole("checkbox", { name: "選取 香港海洋公園" }));
    expect(screen.getByRole("button", { name: "核准" })).toBeTruthy();
  });
});
