import { act, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { AdminHotspotsPanel } from "./admin-hotspots-panel";
import { hotspotIdentityListHref } from "@/lib/admin-catalog-copy";

const item = {
  id: "11111111-1111-4111-8111-111111111111",
  name: "香港海洋公園",
  qid: "Q194776",
  updated_at: "2026-09-10T01:00:00Z",
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
  it("fills a missing QID and category with a rationale without approving or changing map data", async () => {
    const candidate = { ...item, qid: null, category: "culture", reason: null };
    let body: Record<string, unknown> | undefined;
    vi.stubGlobal("fetch", vi.fn(async (_input: RequestInfo | URL, init?: RequestInit) => {
      if (init?.method === "POST") { body = JSON.parse(String(init.body)); return new Response("{\"updated\":1}"); }
      return new Response(JSON.stringify({ ...listing, items: [candidate] }));
    }));
    render(<AdminHotspotsPanel />);
    await screen.findByText(item.name);
    fireEvent.click(screen.getByRole("button", { name: "編輯地點" }));
    fireEvent.change(screen.getByLabelText("景點分類"), { target: { value: "family" } });
    fireEvent.change(screen.getByLabelText("Wikidata ID"), { target: { value: "Q194776" } });
    fireEvent.click(screen.getByRole("button", { name: "儲存地點" }));
    expect(await screen.findByText("修改分類或 Wikidata ID 前，請填寫審核理由與來源。")).toBeTruthy();
    expect(body).toBeUndefined();
    fireEvent.change(screen.getByLabelText("審核理由與來源"), { target: { value: "確認同一海洋公園 https://www.oceanpark.com.hk/" } });
    fireEvent.click(screen.getByRole("button", { name: "儲存地點" }));
    await screen.findByText("已儲存精準地點。");
    expect(body).toEqual({ ids: [item.id], action: "update", category: "family", wikidata_item_id: "Q194776", reason: "確認同一海洋公園 https://www.oceanpark.com.hk/", expected_updated_at: item.updated_at });
  });

  it("keeps existing QIDs read-only and keeps a conflicting draft until explicitly discarded", async () => {
    const fetchMock = vi.fn(async (_input: RequestInfo | URL, init?: RequestInit) => init?.method === "POST"
      ? new Response(JSON.stringify({ code: "hotspot_review_conflict", detail: "資料已更新" }), { status: 409 })
      : new Response(JSON.stringify(listing)));
    vi.stubGlobal("fetch", fetchMock);
    const confirm = vi.fn(() => false);
    vi.stubGlobal("confirm", confirm);
    render(<AdminHotspotsPanel />);
    await screen.findByText(item.name);
    fireEvent.click(screen.getByRole("button", { name: "編輯地點" }));
    expect(screen.getByLabelText("Wikidata ID").hasAttribute("readonly")).toBe(true);
    fireEvent.change(screen.getByLabelText("審核理由與來源"), { target: { value: "草稿來源 https://www.oceanpark.com.hk/" } });
    fireEvent.click(screen.getByRole("button", { name: "儲存地點" }));
    await screen.findByRole("alert");
    expect((screen.getByLabelText("審核理由與來源") as HTMLTextAreaElement).value).toBe("草稿來源 https://www.oceanpark.com.hk/");
    expect((screen.getByRole("button", { name: "儲存地點" }) as HTMLButtonElement).disabled).toBe(true);
    fireEvent.click(screen.getByRole("button", { name: "重新載入最新資料" }));
    expect(confirm).toHaveBeenCalled();
    expect((screen.getByLabelText("審核理由與來源") as HTMLTextAreaElement).value).toBe("草稿來源 https://www.oceanpark.com.hk/");
    confirm.mockReturnValue(true);
    fireEvent.click(screen.getByRole("button", { name: "重新載入最新資料" }));
    await waitFor(() => expect(screen.queryByRole("alert")).toBeNull());
    expect((screen.getByLabelText("審核理由與來源") as HTMLTextAreaElement).value).toBe(item.reason);
  });

  it.each([200, 409])("locks the editor while a deferred save is pending, including a %s response", async (status) => {
    const candidate = { ...item, qid: null, reason: null };
    const other = { ...item, id: "22222222-2222-4222-8222-222222222222", name: "另一個景點" };
    const rationale = "確認官方來源 https://www.oceanpark.com.hk/";
    let body: Record<string, unknown> | undefined;
    let finishSave!: (response: Response) => void;
    const pendingSave = new Promise<Response>((resolve) => { finishSave = resolve; });
    const fetchMock = vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
      if (init?.method === "POST" && String(input).includes("/map-candidates")) {
        return new Response(JSON.stringify({ configured: true, candidates: [{
          place_id: "ChIJ-new-candidate", name: "待核對地圖候選", address: "香港",
          temporary_match_coordinates: { latitude: 22.247, longitude: 114.176 },
        }] }));
      }
      if (init?.method === "POST") {
        body = JSON.parse(String(init.body));
        return pendingSave;
      }
      return new Response(JSON.stringify({ ...listing, items: [candidate, other], total: 2 }));
    });
    vi.stubGlobal("fetch", fetchMock);
    const confirm = vi.fn(() => true);
    vi.stubGlobal("confirm", confirm);
    render(<AdminHotspotsPanel />);
    await screen.findByText(item.name);
    const firstEdit = within(screen.getByText(item.name).closest("tr")!).getByRole("button", { name: "編輯地點" });
    const secondEdit = within(screen.getByText(other.name).closest("tr")!).getByRole("button", { name: "編輯地點" });
    fireEvent.click(firstEdit);
    fireEvent.click(screen.getByRole("button", { name: "搜尋 Google 候選" }));
    const applyPlaceId = await screen.findByRole("button", { name: "套用 Place ID，仍需人工確認" });
    await waitFor(() => expect(applyPlaceId.matches(":disabled")).toBe(false));
    fireEvent.change(screen.getByLabelText("審核理由與來源"), { target: { value: rationale } });
    const save = screen.getByRole("button", { name: "儲存地點" });
    const form = save.closest("form")!;
    const close = screen.getByRole("button", { name: "關閉" });
    const fields = [...form.querySelectorAll("input, select, textarea")];
    expect(fields.length).toBeGreaterThan(3);
    expect(fields.every((field) => !field.matches(":disabled"))).toBe(true);
    fireEvent.click(save);
    await waitFor(() => expect(body).toBeDefined());

    for (const control of [close, firstEdit, secondEdit, save, applyPlaceId, ...fields]) {
      // :disabled includes inherited fieldset disabling, unlike the input.disabled property.
      expect(control.matches(":disabled")).toBe(true);
    }
    fireEvent.click(close);
    fireEvent.click(secondEdit);
    fireEvent.click(applyPlaceId);
    expect(confirm).not.toHaveBeenCalled();
    expect(screen.getByRole("heading", { name: `精準地點：${item.name}` })).toBeTruthy();
    expect((screen.getByLabelText("審核理由與來源") as HTMLTextAreaElement).value).toBe(rationale);
    expect((screen.getByLabelText("Google Place ID") as HTMLInputElement).value).toBe(item.google_place_id);
    expect(body).toEqual({ ids: [item.id], action: "update", reason: rationale, expected_updated_at: item.updated_at });

    await act(async () => {
      finishSave(new Response(JSON.stringify(status === 409
        ? { code: "hotspot_review_conflict", detail: "資料已更新" }
        : { updated: 1, status: "pending" }), { status }));
    });
    await waitFor(() => expect(secondEdit.matches(":disabled")).toBe(false));
    if (status === 409) {
      expect(await screen.findByRole("alert")).toBeTruthy();
      expect((screen.getByLabelText("審核理由與來源") as HTMLTextAreaElement).value).toBe(rationale);
      expect(screen.getByLabelText("審核理由與來源").matches(":disabled")).toBe(false);
      expect(save.matches(":disabled")).toBe(true);
      fireEvent.click(close);
      expect(confirm).toHaveBeenCalledTimes(1);
    } else {
      expect(await screen.findByText("已儲存精準地點。")).toBeTruthy();
    }
    expect(screen.queryByLabelText("審核理由與來源")).toBeNull();
    fireEvent.click(secondEdit);
    expect(screen.getByRole("heading", { name: `精準地點：${other.name}` })).toBeTruthy();
    expect((screen.getByLabelText("審核理由與來源") as HTMLTextAreaElement).value).toBe(other.reason);
    expect(screen.queryByRole("alert")).toBeNull();
  });

  it("lets a reviewer fill a whitespace-only QID without modifying unrelated fields", async () => {
    const candidate = { ...item, qid: "   ", reason: null };
    let body: Record<string, unknown> | undefined;
    vi.stubGlobal("fetch", vi.fn(async (_input: RequestInfo | URL, init?: RequestInit) => {
      if (init?.method === "POST") { body = JSON.parse(String(init.body)); return new Response("{\"updated\":1}"); }
      return new Response(JSON.stringify({ ...listing, items: [candidate] }));
    }));
    render(<AdminHotspotsPanel />);
    await screen.findByText(item.name);
    fireEvent.click(screen.getByRole("button", { name: "編輯地點" }));
    const qid = screen.getByLabelText("Wikidata ID");
    expect(qid.hasAttribute("readonly")).toBe(false);
    fireEvent.change(qid, { target: { value: item.qid } });
    fireEvent.change(screen.getByLabelText("審核理由與來源"), { target: { value: "已核對同一 Wikidata 實體" } });
    fireEvent.click(screen.getByRole("button", { name: "儲存地點" }));
    await screen.findByText("已儲存精準地點。");
    expect(body).toEqual({ ids: [item.id], action: "update", wikidata_item_id: item.qid, reason: "已核對同一 Wikidata 實體", expected_updated_at: item.updated_at });
  });

  it("submits a decision with the selected version and rationale", async () => {
    let body: Record<string, unknown> | undefined;
    vi.stubGlobal("fetch", vi.fn(async (_input: RequestInfo | URL, init?: RequestInit) => {
      if (init?.method === "POST") { body = JSON.parse(String(init.body)); return new Response("{\"updated\":1}"); }
      return new Response(JSON.stringify(listing));
    }));
    render(<AdminHotspotsPanel />);
    await screen.findByText(item.name);
    fireEvent.click(screen.getByRole("checkbox", { name: `選取 ${item.name}` }));
    fireEvent.change(screen.getByLabelText("本次審核理由與來源"), { target: { value: "依官方地址完成查證" } });
    fireEvent.click(screen.getByRole("button", { name: "核准" }));
    await screen.findByText(/已更新 1 筆景點候選/);
    expect(body).toEqual({ ids: [item.id], action: "approve", reason: "依官方地址完成查證", expected_updated_ats: { [item.id]: item.updated_at } });
  });

  it("edits a Korean Google identity without clearing its NAVER identity", async () => {
    const korean = { ...item, country_code: "KR", google_place_id: "ChIJ-korea", naver_map_url: "https://map.naver.com/p/entry/place/123" };
    const fetchMock = vi.fn(async (_input: RequestInfo | URL, init?: RequestInit) => {
      if (init?.method === "POST") return new Response(JSON.stringify({ updated: 1 }));
      return new Response(JSON.stringify({ ...listing, items: [korean] }));
    });
    vi.stubGlobal("fetch", fetchMock);
    render(<AdminHotspotsPanel />);
    await screen.findByText(korean.name);
    fireEvent.click(screen.getByRole("button", { name: "編輯地點" }));
    fireEvent.change(screen.getByLabelText("Google Place ID"), { target: { value: "ChIJ-correct-branch" } });
    fireEvent.click(screen.getByRole("button", { name: "儲存地點" }));
    await screen.findByText("已儲存精準地點。");
    const [, init] = fetchMock.mock.calls.find(([, init]) => init?.method === "POST")!;
    expect(JSON.parse(String(init?.body))).toMatchObject({ google_place_id: "ChIJ-correct-branch" });
    expect(JSON.parse(String(init?.body))).not.toHaveProperty("naver_map_url");
  });

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
        expect(body.google_place_id).toBeUndefined();
        expect(body.map_match_status).toBe("verified");
        expect(body.coordinate_source_url).toBeUndefined();
        expect(body.expected_updated_at).toBe(item.updated_at);
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
