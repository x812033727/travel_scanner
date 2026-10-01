import { act, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { modalFocusTargets } from "@/lib/modal-sheet";
import { HotspotRestaurantsPanel } from "./hotspot-restaurants-panel";

const occupiedResponse = () => new Response(JSON.stringify({ code: "meal_slot_occupied", detail: "Occupied meal" }), { status: 409 });
const selectionBody = { trip_id: "trip-1", version: 4, day_date: "2026-10-01", mode: "replace_meal", meal: "lunch" };

async function openMealPicker(select: (url: string, body: Record<string, unknown>) => Promise<Response>) {
  const requests: { url: string; body: Record<string, unknown> }[] = [];
  vi.stubGlobal("fetch", vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
    const url = String(input);
    if (url.endsWith("/trip-selections")) {
      const body = JSON.parse(String(init?.body)) as Record<string, unknown>;
      requests.push({ url, body });
      return select(url, body);
    }
    if (url.endsWith("/restaurants/favorites")) return new Response(JSON.stringify({ place_ids: [] }));
    if (url.endsWith("/restaurants/trip-options")) return new Response(JSON.stringify({ items: [
      { trip_id: "trip-1", name: "廣島三日", version: 4, start_date: "2026-10-01", end_date: "2026-10-03" },
      { trip_id: "trip-2", name: "京都三日", version: 7, start_date: "2026-11-01", end_date: "2026-11-03" },
    ] }));
    if (url.endsWith("/restaurant-searches")) return new Response(JSON.stringify({
      items: ["ChIJ-food", "ChIJ-other"].map((place_id, index) => ({
        place_id, name: index ? "另一間店" : "廣島燒名店", address: null, latitude: 34.39, longitude: 132.45,
        distance_km: 1, rating: 4.6, review_count: 2345, recommendation_score: 4.42, opening_hours: [],
        open_now: true, official_website_url: null, google_maps_url: null, primary_type: null,
        observed_at: "2026-09-01T12:00:00Z", editorial: null,
      })),
      next_cursor: null, coverage: { status: "completed", cells_completed: 1, cells_total: 1, candidate_count: 2 },
      attribution: "Google Maps",
    }));
    throw new Error(`Unexpected fetch: ${url}`);
  }));
  render(<HotspotRestaurantsPanel hotspot={{ id: "hotspot-1", name: "平和紀念公園" }} onClose={vi.fn()} />);
  fireEvent.click((await screen.findAllByRole("button", { name: "加入行程" }))[0]);
  await screen.findByRole("dialog", { name: "選擇要加入的旅程" });
  return requests;
}

async function changeMealContext(context: string) {
  if (context === "trip") fireEvent.change(screen.getByLabelText("我的旅行"), { target: { value: "trip-2" } });
  else if (context === "day") fireEvent.change(screen.getByLabelText("日期"), { target: { value: "2026-10-02" } });
  else if (context === "meal") fireEvent.change(screen.getByLabelText("餐食"), { target: { value: "dinner" } });
  else {
    if (context === "escape") fireEvent.keyDown(document.activeElement as HTMLElement, { key: "Escape" });
    else fireEvent.click(screen.getByRole("button", { name: "關閉行程選擇" }));
    fireEvent.click(screen.getAllByRole("button", { name: "加入行程" })[context === "restaurant" ? 1 : 0]);
    await screen.findByRole("dialog", { name: "選擇要加入的旅程" });
  }
}

describe("HotspotRestaurantsPanel", () => {
  it("sends the documented meal selection without an overwrite for an available slot", async () => {
    const requests = await openMealPicker(async () => new Response("{}"));
    fireEvent.click(screen.getByRole("button", { name: "確認加入行程" }));
    expect(await screen.findByText("已加入「廣島三日」。")).toBeTruthy();
    expect(requests).toEqual([{ url: "/api/travel/restaurants/ChIJ-food/trip-selections", body: selectionBody }]);
  });

  it("only overwrites an occupied meal after explicit confirmation of the original selection", async () => {
    const requests = await openMealPicker(async (_url, body) => body.overwrite ? new Response("{}") : occupiedResponse());
    fireEvent.change(screen.getByLabelText("我的旅行"), { target: { value: "trip-2" } });
    fireEvent.change(screen.getByLabelText("日期"), { target: { value: "2026-11-02" } });
    fireEvent.change(screen.getByLabelText("餐食"), { target: { value: "dinner" } });
    fireEvent.click(screen.getByRole("button", { name: "確認加入行程" }));
    const overwrite = await screen.findByRole("button", { name: "換成這個" });
    const dialog = screen.getByRole("dialog", { name: "選擇要加入的旅程" });
    expect(within(dialog).getByText("這一餐已經有你選好的店家，要換成這個地點嗎？")).toBeTruthy();
    expect(requests).toHaveLength(1);
    expect(requests[0].body).toEqual({ ...selectionBody, trip_id: "trip-2", version: 7, day_date: "2026-11-02", meal: "dinner" });
    fireEvent.click(overwrite);
    expect(await screen.findByText("已加入「京都三日」。")).toBeTruthy();
    expect(requests[1]).toEqual({ url: requests[0].url, body: { ...requests[0].body, overwrite: true } });
    expect(screen.queryByRole("dialog", { name: "選擇要加入的旅程" })).toBeNull();
  });

  it.each([[409, "trip_version_conflict"], [400, "meal_slot_occupied"], [500, "server_error"]])(
    "does not authorize overwrite for %s %s", async (status, code) => {
      const requests = await openMealPicker(async () => new Response(JSON.stringify({ code, detail: "Specific error" }), { status }));
      fireEvent.click(screen.getByRole("button", { name: "確認加入行程" }));
      expect(await screen.findByText("Specific error")).toBeTruthy();
      expect(screen.queryByRole("button", { name: "換成這個" })).toBeNull();
      expect(requests).toHaveLength(1);
    },
  );

  it.each(["trip", "day", "meal", "restaurant", "cancel", "escape"])(
    "discards occupied confirmation when the %s context changes", async (context) => {
      const requests = await openMealPicker(async () => occupiedResponse());
      fireEvent.click(screen.getByRole("button", { name: "確認加入行程" }));
      await screen.findByRole("button", { name: "換成這個" });
      await changeMealContext(context);
      expect(screen.queryByRole("button", { name: "換成這個" })).toBeNull();
      fireEvent.click(screen.getByRole("button", { name: "確認加入行程" }));
      await screen.findByRole("button", { name: "換成這個" });
      expect(requests).toHaveLength(2);
      expect(requests[1].body).toEqual({
        ...selectionBody,
        ...(context === "trip" ? { trip_id: "trip-2", version: 7, day_date: "2026-11-01" } : {}),
        ...(context === "day" ? { day_date: "2026-10-02" } : {}),
        ...(context === "meal" ? { meal: "dinner" } : {}),
      });
      expect(requests[1].url).toBe(`/api/travel/restaurants/${context === "restaurant" ? "ChIJ-other" : "ChIJ-food"}/trip-selections`);
    },
  );

  it.each(["meal", "restaurant", "cancel", "escape"])(
    "ignores a delayed occupied response after changing %s, even if the same choice is reopened", async (context) => {
      let respond!: (response: Response) => void;
      const response = new Promise<Response>((resolve) => { respond = resolve; });
      const requests = await openMealPicker(async () => response);
      fireEvent.click(screen.getByRole("button", { name: "確認加入行程" }));
      await waitFor(() => expect(requests).toHaveLength(1));
      await changeMealContext(context);
      if (context === "meal") fireEvent.change(screen.getByLabelText("餐食"), { target: { value: "lunch" } });
      await act(async () => { respond(occupiedResponse()); await response; });
      await waitFor(() => expect(screen.getByRole("button", { name: "確認加入行程" }).hasAttribute("disabled")).toBe(false));
      expect(screen.queryByRole("button", { name: "換成這個" })).toBeNull();
      expect(screen.queryByText("Occupied meal")).toBeNull();
      expect(requests).toHaveLength(1);
    },
  );

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
  it("keeps the keyboard inside the nested add-to-trip dialog", async () => {
    vi.stubGlobal("fetch", vi.fn(async (input: RequestInfo | URL) => {
      const url = String(input);
      if (url.endsWith("/restaurants/favorites")) return new Response(JSON.stringify({ place_ids: [] }));
      if (url.endsWith("/restaurants/trip-options")) {
        return new Response(JSON.stringify({ items: [{
          trip_id: "trip-1",
          name: "廣島三日",
          version: 4,
          start_date: "2026-10-01",
          end_date: "2026-10-03",
        }] }));
      }
      return new Response(JSON.stringify({
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
          opening_hours: [],
          open_now: true,
          official_website_url: null,
          google_maps_url: null,
          primary_type: "japanese_restaurant",
          observed_at: "2026-09-01T12:00:00Z",
          editorial: null,
        }],
        next_cursor: null,
        coverage: { status: "completed", cells_completed: 7, cells_total: 7, candidate_count: 42 },
        attribution: "Google Maps",
      }));
    }));

    const onClose = vi.fn();
    render(<HotspotRestaurantsPanel hotspot={{ id: "hotspot-1", name: "平和紀念公園" }} onClose={onClose} />);

    const opener = await screen.findByRole("button", { name: "加入行程" });
    // jsdom does not focus a button on click the way a browser does, and where focus
    // returns to when the nested dialog closes is exactly what this asserts.
    opener.focus();
    fireEvent.click(opener);

    const inner = await screen.findByRole("dialog", { name: "選擇要加入的旅程" });
    // The panel re-runs its own focus on every state change, so opening the nested dialog
    // used to pull focus back to the close button of the sheet behind it.
    await waitFor(() => expect(inner.contains(document.activeElement)).toBe(true));

    // The nested dialog is the last child of the sheet, so a trap scoped to the sheet puts
    // its own controls at the end of one long list and wraps out into the restaurant list.
    const stops = modalFocusTargets(inner);
    expect(stops.length).toBeGreaterThan(3);
    const [first] = stops;
    const last = stops[stops.length - 1];

    last.focus();
    fireEvent.keyDown(last, { key: "Tab" });
    expect(document.activeElement).toBe(first);

    first.focus();
    fireEvent.keyDown(first, { key: "Tab", shiftKey: true });
    expect(document.activeElement).toBe(last);

    // Escape closes the layer on top, not the sheet under it.
    fireEvent.keyDown(document.activeElement as HTMLElement, { key: "Escape" });
    await waitFor(() => expect(screen.queryByRole("dialog", { name: "選擇要加入的旅程" })).toBeNull());
    expect(onClose).not.toHaveBeenCalled();
    expect(screen.getByRole("dialog", { name: "平和紀念公園 附近吃什麼" })).toBeTruthy();
    expect(document.activeElement).toBe(opener);

    fireEvent.keyDown(document.body, { key: "Escape" });
    expect(onClose).toHaveBeenCalledTimes(1);
  });
});
