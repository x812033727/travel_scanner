import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { ItineraryPlaceBrowser, type PlaceOption } from "./itinerary-place-browser";

const option: PlaceOption = {
  key: "hotspot:a", id: "a", kind: "hotspot", title: "淺草寺", subtitle: "東京",
  is_saved: true, distance_km: 0.42,
  item: { item_type: "activity", title: "淺草寺", latitude: 35.71, longitude: 139.79,
    provider_place_id: "asakusa", duration_minutes: 90, locked: false, is_estimated: false, data: { catalog_selection: { kind: "hotspot", id: "a" } } },
};
function setup(empty = false) {
  const fetchMock = vi.fn(async (url: RequestInfo | URL) => ({ ok: String(url).includes("/place-options?"), json: async () => ({ items: empty ? [] : [option], next_offset: null, context: "nearby" }) }));
  vi.stubGlobal("fetch", fetchMock);
  const onAdd = vi.fn(() => true), onManual = vi.fn(), onUndo = vi.fn();
  render(<ItineraryPlaceBrowser tripId="trip" reference={{ latitude: 35.7, longitude: 139.8 }}
    following={{ latitude: 35.72, longitude: 139.82 }} countryCodes={["jp"]} items={[]}
    onAdd={onAdd} onManual={onManual} onUndo={onUndo} canUndo />);
  return { fetchMock, onAdd, onManual, onUndo };
}
afterEach(() => { vi.unstubAllGlobals(); });

describe("contextual place browser", () => {
  it("loads saved and nearby catalog options, never paid place search on open", async () => {
    const { fetchMock, onAdd, onUndo } = setup();
    fireEvent.click(await screen.findByRole("button", { name: "加入 淺草寺" }));
    expect(onAdd).toHaveBeenCalledWith(option.item);
    expect(screen.getByRole("tab", { name: "我的收藏" })).toBeTruthy();
    expect(screen.getByText("已加入 淺草寺")).toBeTruthy();
    expect(fetchMock.mock.calls.every(([url]) => String(url).includes("/place-options?"))).toBe(true);
    fireEvent.click(screen.getByRole("button", { name: "復原" }));
    expect(onUndo).toHaveBeenCalledOnce();
  });
  it("switches sources with the keyboard and keeps query and radius scoped to the current context", async () => {
    const { fetchMock } = setup(true);
    await screen.findByText("附近暫時沒有符合的地點。");
    fireEvent.keyDown(screen.getByRole("tab", { name: "為你挑選" }), { key: "ArrowRight" });
    await waitFor(() => expect(fetchMock.mock.calls.some(([url]) => String(url).includes("source=favorites"))).toBe(true));
    expect(document.activeElement).toBe(screen.getByRole("tab", { name: "我的收藏" }));
    fireEvent.click(screen.getByRole("checkbox", { name: "也顯示其他城市的收藏" }));
    await waitFor(() => expect(fetchMock.mock.calls.some(([url]) => String(url).includes("all_cities=true"))).toBe(true));
    expect(fetchMock.mock.calls.some(([url]) => String(url).includes("next_latitude=35.72"))).toBe(true);
  });
  it("keeps manual entry available when offline", async () => {
    const { fetchMock, onManual } = setup();
    fetchMock.mockRejectedValue(new TypeError("offline"));
    Object.defineProperty(window.navigator, "onLine", { value: false, configurable: true });
    expect((await screen.findByRole("alert")).textContent).toContain("目前離線");
    fireEvent.click(screen.getByRole("button", { name: "自行填寫行程" }));
    expect(onManual).toHaveBeenCalledOnce();
    Object.defineProperty(window.navigator, "onLine", { value: true, configurable: true });
  });
});
