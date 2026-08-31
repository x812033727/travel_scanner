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

  it("keeps current edits, shows planning provenance and regenerates with the saved version", async () => {
    const plannedTrip = {
      ...trip,
      planning: {
        status: "fallback",
        provider: "catalog",
        model: null,
        generated_at: "2026-08-31T10:00:00Z",
        warnings: ["已改用內建目的地資料產生備援草稿"],
      },
      items: [
        {
          ...trip.items[0],
          data: {
            generated_by: "ai_planner",
            reason: "符合文化與散步偏好",
            needs_place_confirmation: true,
          },
        },
      ],
    };
    const fetchMock = vi.fn(async (url: string, init?: RequestInit) => {
      if (init?.method === "PUT") {
        const body = JSON.parse(String(init.body));
        return response({ ...plannedTrip, version: 2, items: body.items });
      }
      if (url.includes("/itinerary/generate")) {
        const body = JSON.parse(String(init?.body));
        expect(body.version).toBe(2);
        return response({
          ...plannedTrip,
          version: 3,
          usage: { status: "released", uses: 1, reference: "reservation-1" },
        });
      }
      return response(plannedTrip);
    });
    vi.stubGlobal("fetch", fetchMock);
    vi.stubGlobal("confirm", vi.fn(() => true));

    render(<TripEditor tripId={trip.id} />);
    expect(await screen.findByText("已使用內建備援草稿")).toBeTruthy();
    expect(screen.getByText("AI 建議")).toBeTruthy();
    expect(screen.getByText("地點待確認")).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "AI 重新排行程" }));

    expect(await screen.findByText(/已使用內建備援重新排行程，本次未扣次/)).toBeTruthy();
    const generateCall = fetchMock.mock.calls.find(([url]) =>
      String(url).includes("/itinerary/generate"),
    );
    expect(generateCall?.[1]?.headers).toMatchObject({ "Idempotency-Key": expect.any(String) });
  });
});
