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

  it("searches and renders a complete back-to-back comparison", async () => {
    const wrapper = {
      role: "wrapper",
      quote: {
        id: "wrapper-1",
        airline_code: "JX",
        airline_name: "星宇航空",
        origin: "TPE",
        destination: "NRT",
        departure_date: "2026-11-10",
        return_date: "2026-12-15",
        total_price: "14000",
        currency: "TWD",
        source_url: "https://www.starlux-airlines.com/example",
      },
      estimated_twd: "14000",
    };
    const reverse = {
      role: "reverse",
      quote: {
        id: "reverse-1",
        airline_code: "CI",
        airline_name: "中華航空",
        origin: "NRT",
        destination: "TPE",
        departure_date: "2026-11-15",
        return_date: "2026-12-10",
        total_price: "20000",
        currency: "JPY",
        source_url: "https://flights.china-airlines.com/example",
      },
      estimated_twd: "4000",
      fx_rate: { base_currency: "JPY", quote_currency: "TWD", rate: "0.2", as_of: "2026-08-30", source_url: "https://api.frankfurter.dev/v2/rates", is_stale: false },
    };
    const comparison = {
      mode: "mixed_airlines",
      conventional: { tickets: [], original_currency_totals: { TWD: "20000" }, estimated_twd: "20000" },
      back_to_back: { tickets: [wrapper, reverse], original_currency_totals: { TWD: "14000", JPY: "20000" }, estimated_twd: "18000" },
      savings_twd: "2000",
      savings_percent: "10.0",
      verdict: "back_to_back_cheaper",
      detail: "混搭航空公司的倒買法估算較省。",
    };
    const response = {
      queried_at: "2026-08-30T10:00:00Z",
      pricing_capability: "full_back_to_back",
      comparisons: [
        comparison,
        { ...comparison, mode: "same_airline", savings_twd: "1000", savings_percent: "5.0" },
      ],
      candidates: [],
      fx_rates: [reverse.fx_rate],
      warnings: ["長榮航空：依政策暫停抓取"],
    };
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(ok(status))
      .mockResolvedValueOnce(ok(response));
    vi.stubGlobal("fetch", fetchMock);
    render(<AirlineFareLab />);
    await screen.findByText("政策停用");
    fireEvent.click(screen.getByRole("tab", { name: "倒買法" }));
    fireEvent.click(screen.getByRole("button", { name: "比較倒買價格" }));

    expect(await screen.findByText("最低混搭")).toBeTruthy();
    expect(screen.getByText("最低同航空公司")).toBeTruthy();
    expect(screen.getByText(/倒買法估算省下.*2,000/)).toBeTruthy();
    expect(screen.getAllByText("外站始發倒買票").length).toBeGreaterThan(0);
    expect(screen.getByText(/JPY 2026-08-30/)).toBeTruthy();
    const [url, init] = fetchMock.mock.calls[1];
    expect(url).toBe("/api/travel/crawlers/airlines/back-to-back-fares");
    expect(JSON.parse(String(init.body))).toMatchObject({
      origin: "TPE",
      first_destination: "TYO",
      second_destination: "TYO",
      first_trip: { departure_date: "2026-11-10", return_date: "2026-11-15" },
      second_trip: { departure_date: "2026-12-10", return_date: "2026-12-15" },
    });
  });

  it("allows different destination countries without inventing open-jaw prices", async () => {
    const conventionalTicket = (role: string, destination: string, price: string) => ({
      role,
      quote: {
        id: `${role}-1`,
        airline_code: "CI",
        airline_name: "中華航空",
        origin: "TPE",
        destination,
        departure_date: role === "conventional_first" ? "2026-11-10" : "2026-12-10",
        return_date: role === "conventional_first" ? "2026-11-15" : "2026-12-15",
        total_price: price,
        currency: "TWD",
        source_url: "https://flights.china-airlines.com/example",
      },
      estimated_twd: price,
    });
    const first = conventionalTicket("conventional_first", "NRT", "10000");
    const second = conventionalTicket("conventional_second", "ICN", "8000");
    const unavailable = {
      conventional: {
        tickets: [first, second],
        original_currency_totals: { TWD: "18000" },
        estimated_twd: "18000",
      },
      verdict: "comparison_unavailable",
      detail: "已計算一般票；不同目的地需要開口票價格來源。",
    };
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(ok(status))
      .mockResolvedValueOnce(ok({
        queried_at: "2026-08-30T10:00:00Z",
        pricing_capability: "open_jaw_provider_required",
        comparisons: [
          { ...unavailable, mode: "mixed_airlines" },
          { ...unavailable, mode: "same_airline" },
        ],
        candidates: [],
        fx_rates: [],
        warnings: [],
      }));
    vi.stubGlobal("fetch", fetchMock);
    render(<AirlineFareLab />);
    await screen.findByText("政策停用");
    fireEvent.click(screen.getByRole("tab", { name: "倒買法" }));
    fireEvent.change(screen.getByLabelText("第二次目的地"), { target: { value: "SEL" } });
    fireEvent.click(screen.getByRole("button", { name: "比較倒買價格" }));

    expect(await screen.findByText("兩次目的地不同，倒買票會變成開口票")).toBeTruthy();
    expect(screen.getAllByText("需串接開口票價格來源")).toHaveLength(2);
    expect(screen.getAllByText(/TPE/).length).toBeGreaterThan(0);
    const [, init] = fetchMock.mock.calls[1];
    expect(JSON.parse(String(init.body))).toMatchObject({
      first_destination: "TYO",
      second_destination: "SEL",
    });
  });

  it("validates the strict order of all four back-to-back dates", async () => {
    const fetchMock = vi.fn().mockResolvedValue(ok(status));
    vi.stubGlobal("fetch", fetchMock);
    render(<AirlineFareLab />);
    await screen.findByText("政策停用");
    fireEvent.click(screen.getByRole("tab", { name: "倒買法" }));
    fireEvent.change(screen.getByLabelText("第二次出發日"), { target: { value: "2026-11-14" } });
    fireEvent.click(screen.getByRole("button", { name: "比較倒買價格" }));
    expect((await screen.findByRole("alert")).textContent).toContain("日期必須依序");
    expect(fetchMock).toHaveBeenCalledTimes(1);
  });
});
