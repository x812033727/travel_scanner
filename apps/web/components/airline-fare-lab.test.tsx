import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { AirlineFareLab } from "./airline-fare-lab";

const status = {
  sources: [
    { airline_code: "CI", airline_name: "中華航空", host: "flights.china-airlines.com", state: "ready", policy: "robots", detail: "ok", quote_count: 0, cache_hit: false },
    { airline_code: "BR", airline_name: "長榮航空", host: "flights.evaair.com", state: "disabled", policy: "fail_closed", detail: "robots unavailable", quote_count: 0, cache_hit: false },
    { airline_code: "JX", airline_name: "星宇航空", host: "www.starlux-airlines.com", state: "ready", policy: "robots", detail: "ok", quote_count: 0, cache_hit: false },
  ],
  safety_rules: [],
};

function ok(payload: unknown) {
  return { ok: true, status: 200, json: async () => payload };
}

afterEach(() => vi.unstubAllGlobals());

describe("airline fare lab", () => {
  it("shows crawler source readiness", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(ok(status)));
    render(<AirlineFareLab />);
    expect(await screen.findByText("政策停用")).toBeTruthy();
    expect(screen.getAllByText("可查詢")).toHaveLength(2);
  });

  it("renders normalized public fare results", async () => {
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(ok(status))
      .mockResolvedValueOnce(ok({
        queried_at: "2026-08-30T10:00:00Z",
        warnings: ["長榮航空：依政策暫停抓取"],
        sources: status.sources,
        quotes: [{
          id: "quote-1",
          airline_code: "JX",
          airline_name: "星宇航空",
          origin: "TPE",
          destination: "NRT",
          departure_date: "2026-11-10",
          return_date: "2026-11-15",
          trip_type: "round_trip",
          cabin_class: "economy",
          total_price: "14075",
          currency: "TWD",
          price_last_seen: "3 hours ago",
          source_url: "https://www.starlux-airlines.com/example",
          is_live: false,
          is_bookable: false,
          disclaimer: "cached",
        }],
      }));
    vi.stubGlobal("fetch", fetchMock);
    render(<AirlineFareLab />);
    await screen.findByText("政策停用");
    fireEvent.click(screen.getByRole("button", { name: "搜尋公開票價" }));
    expect(await screen.findByText(/14,075/)).toBeTruthy();
    expect(screen.getByText("非即時 · 不可直接訂位 · 3 hours ago")).toBeTruthy();
    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(2));
  });

  it("validates that return date is not before departure", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(ok(status)));
    render(<AirlineFareLab />);
    await screen.findByText("政策停用");
    fireEvent.change(screen.getByLabelText("回程日期"), { target: { value: "2026-11-01" } });
    fireEvent.click(screen.getByRole("button", { name: "搜尋公開票價" }));
    expect((await screen.findByRole("alert")).textContent).toContain("回程日期不能早於出發日期");
  });
});
