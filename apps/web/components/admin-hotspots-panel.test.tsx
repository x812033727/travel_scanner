import { fireEvent, render, screen, waitFor } from "@testing-library/react";
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
  plus_code_global: null,
  coordinate_source_type: "official_tourism",
  coordinate_source_url: "https://www.oceanpark.com.hk/",
  google_place_id: "ChIJ-ocean-park",
  naver_map_url: null,
  map_match_status: "unverified",
};

describe("AdminHotspotsPanel", () => {
  it("previews Plus Code and saves an exact reviewed place", async () => {
    const fetchMock = vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      if (url.includes("plus-code-preview")) {
        return new Response(JSON.stringify({ plus_code_global: "7PJP65WG+M7" }));
      }
      if (init?.method === "POST" && url.includes("/review")) {
        const body = JSON.parse(String(init.body));
        expect(body.google_place_id).toBe("ChIJ-ocean-park");
        expect(body.map_match_status).toBe("verified");
        expect(body.coordinate_source_url).toBe("https://www.oceanpark.com.hk/");
        return new Response(JSON.stringify({ updated: 1, status: "pending" }));
      }
      return new Response(JSON.stringify({ items: [item], total: 1, page: 1, pages: 1 }));
    });
    vi.stubGlobal("fetch", fetchMock);

    render(<AdminHotspotsPanel />);
    expect(await screen.findByText("香港海洋公園")).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "編輯地點" }));
    fireEvent.click(screen.getByRole("button", { name: "預覽 Plus Code" }));
    expect(await screen.findByText("7PJP65WG+M7")).toBeTruthy();
    fireEvent.change(screen.getByLabelText("比對狀態"), { target: { value: "verified" } });
    fireEvent.click(screen.getByRole("button", { name: "儲存地點" }));
    expect(await screen.findByText("已儲存精準地點，Plus Code 已由伺服器重算。")).toBeTruthy();
    await waitFor(() => expect(fetchMock).toHaveBeenCalled());
  });
});
