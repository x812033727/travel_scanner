import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { TripInboxPanel } from "./trip-inbox-panel";

const apiMock = vi.fn();
vi.mock("@/lib/api", async () => {
  const actual = await vi.importActual<typeof import("@/lib/api")>("@/lib/api");
  return { ...actual, api: (...args: unknown[]) => apiMock(...args) };
});

const pasted = {
  id: "candidate-1",
  status: "inbox",
  source: "maps_url",
  raw_input: "https://maps.app.goo.gl/abc",
  title: "淺草寺",
  location_name: "東京",
  google_place_id: "ChIJ8T1",
  maps_url: "https://www.google.com/maps/place/?q=place_id:ChIJ8T1",
  latitude: 35.7148,
  longitude: 139.7967,
  hotspot_id: "hotspot-1",
  names: { title: { "zh-TW": "淺草寺", en: "Sensoji" } },
  data: { matched: "hotspot" },
};

describe("TripInboxPanel", () => {
  beforeEach(() => apiMock.mockReset());

  it("reads a paste into the waiting list and says what matched the catalogue", async () => {
    apiMock.mockImplementation(async (path: string, init?: RequestInit) => {
      if (init?.method === "POST") return { created: [pasted], matched: 1, items: [pasted] };
      return { items: [] };
    });
    render(<TripInboxPanel tripId="trip-1" onAdd={() => true} />);

    fireEvent.change(await screen.findByLabelText("貼上地點"), {
      target: { value: "https://maps.app.goo.gl/abc" },
    });
    fireEvent.click(screen.getByRole("button", { name: "讀進待安排" }));

    expect(await screen.findByText("淺草寺")).toBeTruthy();
    expect(screen.getByText("已加入 1 個地點，其中 1 個對到目錄。")).toBeTruthy();
    expect(screen.getByText("目錄景點 · 東京")).toBeTruthy();
  });

  it("only takes a place off the list once the day has accepted it", async () => {
    apiMock.mockImplementation(async (path: string) => {
      if (String(path).endsWith("/places")) return { items: [pasted] };
      return {};
    });
    const onAdd = vi.fn().mockReturnValue(false);
    render(<TripInboxPanel tripId="trip-1" onAdd={onAdd} />);

    fireEvent.click(await screen.findByRole("button", { name: "加到這一天" }));

    await waitFor(() => expect(onAdd).toHaveBeenCalledWith(pasted));
    expect(screen.getByText("淺草寺")).toBeTruthy();
    expect(apiMock.mock.calls.some(([path]) => String(path).includes("/used"))).toBe(false);

    onAdd.mockReturnValue(true);
    fireEvent.click(screen.getByRole("button", { name: "加到這一天" }));
    await waitFor(() => expect(screen.queryByText("淺草寺")).toBeNull());
    expect(apiMock.mock.calls.some(([path]) => String(path).endsWith("/used"))).toBe(true);
  });

  it("removes a place the traveller does not want", async () => {
    apiMock.mockImplementation(async (path: string) => (String(path).endsWith("/places") ? { items: [pasted] } : {}));
    render(<TripInboxPanel tripId="trip-1" onAdd={() => true} />);

    fireEvent.click(await screen.findByRole("button", { name: "移除 淺草寺" }));

    await waitFor(() => expect(screen.queryByText("淺草寺")).toBeNull());
    expect(apiMock.mock.calls.some(([path, init]) => String(path).endsWith("/candidate-1") && (init as RequestInit)?.method === "DELETE")).toBe(true);
  });
});
