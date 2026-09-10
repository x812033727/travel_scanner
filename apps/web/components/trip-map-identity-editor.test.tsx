import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { TripMapIdentityEditor } from "./trip-map-identity-editor";
import type { TripItem } from "@/lib/trip-types";

vi.mock("./place-picker", () => ({ PlacePicker: ({ provider, onSelect }: { provider: string; onSelect: (value: unknown) => void }) =>
  <button onClick={() => onSelect({ provider, place_id: "ChIJ-test", name: "경복궁", address: "서울 종로구 사직로 161" })}>選擇 Google 候選</button>,
}));
const item: TripItem = {
  id: "item", title: "景福宮", day_date: "2026-11-11", item_type: "activity", position: 0,
  latitude: 37.5796, longitude: 126.977, locked: false, is_estimated: false, data: {},
  map_identities: { naver_maps: { provider: "naver_maps", place_id: "12345", map_url: "https://map.naver.com/p/entry/place/12345", status: "verified" } },
};
afterEach(() => vi.unstubAllGlobals());
describe("trip map identity supplement", () => {
  it("sends only identity after explicit comparison, never coordinates or timing", async () => {
    const saved = vi.fn();
    const fetcher = vi.fn().mockResolvedValue(new Response(JSON.stringify({ id: "trip", version: 2 }), { status: 200 }));
    vi.stubGlobal("fetch", fetcher);
    render(<TripMapIdentityEditor tripId="trip" version={1} item={item} canSave onSaved={saved} />);
    expect(screen.getByRole("link", { name: "NAVER Maps" }).getAttribute("href")).toContain("12345");
    fireEvent.click(screen.getByRole("button", { name: "補充 Google 地圖身分" }));
    fireEvent.click(screen.getByText("選擇 Google 候選"));
    const apply = screen.getByRole("button", { name: "只儲存 Google 身分" }) as HTMLButtonElement;
    expect(apply.disabled).toBe(true);
    fireEvent.click(screen.getByRole("checkbox"));
    fireEvent.click(apply);
    await waitFor(() => expect(saved).toHaveBeenCalled());
    const [url, request] = fetcher.mock.calls[0];
    expect(String(url)).toContain("/trips/trip/items/item/map-identities");
    expect(JSON.parse(request.body)).toEqual({ version: 1, provider: "google_places", place_id: "ChIJ-test", confirmed_same_place: true });
    expect(new Headers(request.headers).get("Idempotency-Key")).toBeTruthy();
  });
  it("retains comparison and operation key after failure and requires saving other edits first", async () => {
    const fetcher = vi.fn().mockResolvedValue(new Response(JSON.stringify({ detail: "服務暫時無法連線", code: "unavailable" }), { status: 503 }));
    vi.stubGlobal("fetch", fetcher);
    const { rerender } = render(<TripMapIdentityEditor tripId="trip" version={1} item={item} canSave={false} onSaved={vi.fn()} />);
    expect((screen.getByRole("button", { name: "補充 Google 地圖身分" }) as HTMLButtonElement).disabled).toBe(true);
    rerender(<TripMapIdentityEditor tripId="trip" version={1} item={item} canSave onSaved={vi.fn()} />);
    fireEvent.click(screen.getByRole("button", { name: "補充 Google 地圖身分" }));
    fireEvent.click(screen.getByText("選擇 Google 候選"));
    fireEvent.click(screen.getByRole("checkbox"));
    fireEvent.click(screen.getByRole("button", { name: "只儲存 Google 身分" }));
    expect(await screen.findByRole("alert")).toBeTruthy();
    expect(screen.getByText("서울 종로구 사직로 161")).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "只儲存 Google 身分" }));
    await waitFor(() => expect(fetcher).toHaveBeenCalledTimes(2));
    expect(new Headers(fetcher.mock.calls[0][1].headers).get("Idempotency-Key"))
      .toBe(new Headers(fetcher.mock.calls[1][1].headers).get("Idempotency-Key"));
  });
});
