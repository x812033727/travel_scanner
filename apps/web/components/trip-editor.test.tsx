import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { TripEditor } from "./trip-editor";

vi.mock("next/navigation", () => ({ useRouter: () => ({ push: vi.fn() }) }));

const trip = {
  id: "00000000-0000-4000-8000-000000000001",
  name: "東京五日",
  mode: "balanced",
  total_price: 52000,
  currency: "TWD",
  data: {},
  version: 1,
  share_enabled: false,
  items: [
    {
      id: "00000000-0000-4000-8000-000000000002",
      item_type: "activity",
      day_date: "2026-11-11",
      position: 0,
      title: "淺草散步",
      location_name: "淺草",
      locked: false,
      is_estimated: false,
      data: {},
    },
  ],
};

function response(payload: unknown) {
  return { ok: true, status: 200, json: async () => payload };
}

afterEach(() => vi.unstubAllGlobals());

describe("trip editor", () => {
  it("edits and saves an itinerary with the current version", async () => {
    const fetchMock = vi.fn(async (_url: string, init?: RequestInit) => {
      if (init?.method === "PUT") {
        const body = JSON.parse(String(init.body));
        return response({ ...trip, version: 2, items: body.items });
      }
      return response(trip);
    });
    vi.stubGlobal("fetch", fetchMock);
    render(<TripEditor tripId={trip.id} />);
    const title = await screen.findByDisplayValue("淺草散步");
    fireEvent.change(title, { target: { value: "淺草與晴空塔" } });
    fireEvent.click(screen.getByRole("button", { name: "儲存變更" }));
    expect(await screen.findByText("行程已儲存")).toBeTruthy();
    await waitFor(() => {
      const call = fetchMock.mock.calls.find(([, init]) => init?.method === "PUT");
      expect(call).toBeTruthy();
      const body = JSON.parse(String(call?.[1]?.body));
      expect(body.version).toBe(1);
      expect(body.items[0].title).toBe("淺草與晴空塔");
    });
  });
});
