import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { AdminHotspotsPanel } from "./admin-hotspots-panel";
import { hotspotIdentityListHref } from "@/lib/admin-catalog-copy";

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
  it.each([{ initialHotspotId: item.id }, { initialMissingLocation: true }])("offers a way out of canonical location filters %o", async (props) => {
    vi.stubGlobal("fetch", vi.fn(async () => new Response(JSON.stringify(listing))));
    render(<AdminHotspotsPanel initialStatus="" {...props} />);
    await screen.findByText(item.name);
    expect(screen.getByRole("link", { name: "顯示全部地點" }).getAttribute("href")).toBe("/admin/hotspots?tab=places&section=identity");
  });

  it("clears only identity filters and preserves unrelated search parameters", () => {
    const href = hotspotIdentityListHref(new URLSearchParams({
      tab: "places", section: "identity", hotspot_id: item.id, missing_location: "true", country: "JP", q: "Atomic Bomb", provider: "google_maps",
    }));
    const params = new URL(href, "https://test.local").searchParams;
    expect(params.has("hotspot_id")).toBe(false);
    expect(params.has("missing_location")).toBe(false);
    expect(params.get("country")).toBe("JP");
    expect(params.get("q")).toBe("Atomic Bomb");
    expect(params.get("provider")).toBe("google_maps");
    expect(params.get("tab")).toBe("places");
    expect(params.get("section")).toBe("identity");
  });

  it.each(["", "pending"])("sends the requested catalog/review status %s", async (initialStatus) => {
    const fetchMock = vi.fn<(input: RequestInfo | URL, init?: RequestInit) => Promise<Response>>(
      async () => new Response(JSON.stringify(listing)),
    );
    vi.stubGlobal("fetch", fetchMock);
    render(<AdminHotspotsPanel initialStatus={initialStatus} />);
    await screen.findByText(item.name);
    const url = new URL(String(fetchMock.mock.calls[0][0]), "https://test.local");
    expect(url.searchParams.get("status")).toBe(initialStatus || null);
  });

  it("jumps from catalog to the one location editor without opening an inline editor", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => new Response(JSON.stringify(listing))));
    render(<AdminHotspotsPanel initialStatus="" locationEditing="link" />);
    await screen.findByText(item.name);
    expect(screen.getByRole("link", { name: "管理精準地點" }).getAttribute("href")).toBe(
      `/admin/hotspots?tab=places&section=identity&hotspot_id=${item.id}`,
    );
    expect(screen.queryByRole("button", { name: "編輯地點" })).toBeNull();
    expect(screen.queryByLabelText("Google Place ID")).toBeNull();
  });

  it("constrains the canonical editor by exact ID and missing-coordinate filters", async () => {
    const fetchMock = vi.fn<(input: RequestInfo | URL, init?: RequestInit) => Promise<Response>>(
      async () => new Response(JSON.stringify(listing)),
    );
    vi.stubGlobal("fetch", fetchMock);
    render(<AdminHotspotsPanel initialStatus="" initialHotspotId={item.id} initialMissingLocation />);
    await screen.findByText(item.name);
    const url = new URL(String(fetchMock.mock.calls[0][0]), "https://test.local");
    expect(url.searchParams.get("hotspot_id")).toBe(item.id);
    expect(url.searchParams.get("missing_location")).toBe("true");
    fireEvent.click(screen.getByRole("button", { name: "編輯地點" }));
    expect(screen.getByLabelText("Google Place ID")).toBeTruthy();
  });

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

  it("opens a Korean candidate in NAVER search for manual review", async () => {
    const koreanItem = {
      ...item,
      name: "해운대 암소갈비집",
      destination_id: "busan",
      city_code: "PUS",
      city_name: "釜山",
      country_code: "KR",
      country_name: "韓國",
      google_place_id: null,
      naver_map_url: null,
    };
    vi.stubGlobal(
      "fetch",
      vi.fn(async () =>
        new Response(
          JSON.stringify({
            ...listing,
            items: [koreanItem],
            facets: {
              countries: [{ code: "KR", name: "韓國", count: 1 }],
              categories: listing.facets.categories,
            },
          }),
        ),
      ),
    );

    render(<AdminHotspotsPanel />);
    expect(await screen.findByText("해운대 암소갈비집")).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "編輯地點" }));
    expect(
      screen
        .getByRole("link", { name: "開啟 Naver 搜尋並人工核對" })
        .getAttribute("href"),
    ).toBe(
      `https://map.naver.com/p/search/${encodeURIComponent("해운대 암소갈비집 부산")}`,
    );
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
