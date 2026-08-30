import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { AirlineFareLab } from "./airline-fare-lab";

const { routerPush } = vi.hoisted(() => ({ routerPush: vi.fn() }));
vi.mock("next/navigation", () => ({ useRouter: () => ({ push: routerPush }) }));

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

afterEach(() => {
  vi.unstubAllGlobals();
  routerPush.mockReset();
});

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
        usage: { status: "charged", uses: 1, reference: "usage-1" },
      }));
    vi.stubGlobal("fetch", fetchMock);
    render(<AirlineFareLab />);
    await screen.findByText("政策停用");
    fireEvent.click(screen.getByRole("button", { name: "搜尋公開票價" }));
    expect(await screen.findByText(/14,075/)).toBeTruthy();
    expect(screen.getByText("非即時 · 不可直接訂位 · 3 hours ago")).toBeTruthy();
    expect(screen.getByText("本次已扣除 1 次")).toBeTruthy();
    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(2));
    expect(fetchMock.mock.calls[1][1].headers).toMatchObject({
      "Idempotency-Key": expect.any(String),
    });
  });

  it("validates that return date is not before departure", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(ok(status)));
    render(<AirlineFareLab />);
    await screen.findByText("政策停用");
    fireEvent.change(screen.getByLabelText("回程日期"), { target: { value: "2026-11-01" } });
    fireEvent.click(screen.getByRole("button", { name: "搜尋公開票價" }));
    expect((await screen.findByRole("alert")).textContent).toContain("回程日期不能早於出發日期");
  });

  it("routes to usage packages when no uses remain", async () => {
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(ok(status))
      .mockResolvedValueOnce({
        ok: false,
        status: 402,
        json: async () => ({ code: "insufficient_uses", detail: "可用次數不足" }),
      });
    vi.stubGlobal("fetch", fetchMock);
    render(<AirlineFareLab />);
    await screen.findByText("政策停用");
    fireEvent.click(screen.getByRole("button", { name: "搜尋公開票價" }));
    await waitFor(() => expect(routerPush).toHaveBeenCalledWith("/pricing"));
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
    fireEvent.click(screen.getByRole("radio", { name: /包覆倒買/ }));
    fireEvent.click(screen.getByRole("button", { name: "比較倒買價格" }));

    expect(await screen.findByText("最低混搭")).toBeTruthy();
    expect(screen.getByText("最低同航空公司")).toBeTruthy();
    expect(screen.getByText(/包覆倒買估算省下.*2,000/)).toBeTruthy();
    expect(screen.getAllByText("外站始發倒買票").length).toBeGreaterThan(0);
    expect(screen.getByText(/JPY 2026-08-30/)).toBeTruthy();
    const [url, init] = fetchMock.mock.calls[1];
    expect(url).toBe("/api/travel/crawlers/airlines/back-to-back-fares");
    const payload = JSON.parse(String(init.body));
    expect(payload).toMatchObject({
      origin: "TPE",
      first_destination: "TYO",
      second_destination: "TYO",
      strategy: "nested_round_trips",
    });
    expect(init.headers).toMatchObject({ "Idempotency-Key": expect.any(String) });
    const dates = [
      payload.first_trip.departure_date,
      payload.first_trip.return_date,
      payload.second_trip.departure_date,
      payload.second_trip.return_date,
    ];
    expect(dates.every((date) => /^\d{4}-\d{2}-\d{2}$/.test(date))).toBe(true);
    expect(dates.every((date, index) => index === 0 || dates[index - 1] < date)).toBe(true);
  });

  it("prices an external-station two-segment ticket with manual head and tail fares", async () => {
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
    };
    const supplementalFares = [
      { role: "head_one_way", origin: "TPE", destination: "TYO", departure_date: "2026-11-10", amount: "3000", currency: "TWD", airline_code: "CI", estimated_twd: "3000", source: "manual", is_live: false },
      { role: "tail_one_way", origin: "TYO", destination: "TPE", departure_date: "2026-12-15", amount: "4000", currency: "TWD", airline_code: "CI", estimated_twd: "4000", source: "manual", is_live: false },
    ];
    const comparison = {
      mode: "mixed_airlines",
      conventional: { tickets: [], original_currency_totals: { TWD: "20000" }, estimated_twd: "20000" },
      back_to_back: { tickets: [reverse], supplemental_fares: supplementalFares, original_currency_totals: { JPY: "20000", TWD: "7000" }, estimated_twd: "11000" },
      savings_twd: "9000",
      savings_percent: "45.0",
      verdict: "back_to_back_cheaper",
      detail: "混搭航空公司的外站兩段票估算較省。",
    };
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(ok(status))
      .mockResolvedValueOnce(ok({
        queried_at: "2026-08-30T10:00:00Z",
        query: {
          strategy: "reverse_two_segment",
          first_destination: "TYO",
          second_destination: "TYO",
        },
        pricing_capability: "full_back_to_back",
        comparisons: [comparison, { ...comparison, mode: "same_airline" }],
        candidates: [],
        fx_rates: [],
        warnings: [],
      }));
    vi.stubGlobal("fetch", fetchMock);
    render(<AirlineFareLab />);
    await screen.findByText("政策停用");
    fireEvent.click(screen.getByRole("tab", { name: "倒買法" }));
    fireEvent.change(screen.getByLabelText("頭段單程每人價格"), { target: { value: "3000" } });
    fireEvent.change(screen.getByLabelText("尾段單程每人價格"), { target: { value: "4000" } });
    fireEvent.change(screen.getByLabelText("頭段單程航空公司"), { target: { value: "CI" } });
    fireEvent.change(screen.getByLabelText("尾段單程航空公司"), { target: { value: "CI" } });
    fireEvent.click(screen.getByRole("button", { name: "比較倒買價格" }));

    expect((await screen.findAllByText(/外站兩段票估算省下.*9,000/)).length).toBe(2);
    expect(screen.getAllByText(/頭段單程票.*手動輸入/).length).toBeGreaterThan(0);
    expect(screen.getAllByText(/尾段單程票.*手動輸入/).length).toBeGreaterThan(0);
    const payload = JSON.parse(String(fetchMock.mock.calls[1][1].body));
    expect(payload).toMatchObject({
      strategy: "reverse_two_segment",
      head_one_way_fare: { amount: "3000", currency: "TWD", airline_code: "CI" },
      tail_one_way_fare: { amount: "4000", currency: "TWD", airline_code: "CI" },
    });
  });

  it("supports different destinations with a manual middle multi-city fare", async () => {
    const manualFare = (role: string, amount: string, segments: Array<{ origin: string; destination: string; departure_date: string }>) => ({
      role,
      origin: segments[0].origin,
      destination: segments.at(-1)?.destination,
      departure_date: segments[0].departure_date,
      amount,
      currency: "TWD",
      airline_code: "CI",
      estimated_twd: amount,
      source: "manual",
      is_live: false,
      segments,
    });
    const firstConventional = manualFare("conventional_first_manual", "12000", [
      { origin: "TPE", destination: "TYO", departure_date: "2026-11-10" },
      { origin: "TYO", destination: "TPE", departure_date: "2026-11-15" },
    ]);
    const secondConventional = manualFare("conventional_second_manual", "10000", [
      { origin: "TPE", destination: "SEL", departure_date: "2026-12-10" },
      { origin: "SEL", destination: "TPE", departure_date: "2026-12-15" },
    ]);
    const head = manualFare("head_one_way", "3000", [
      { origin: "TPE", destination: "TYO", departure_date: "2026-11-10" },
    ]);
    const middle = manualFare("middle_two_segment", "9000", [
      { origin: "TYO", destination: "TPE", departure_date: "2026-11-15" },
      { origin: "TPE", destination: "SEL", departure_date: "2026-12-10" },
    ]);
    const tail = manualFare("tail_one_way", "4000", [
      { origin: "SEL", destination: "TPE", departure_date: "2026-12-15" },
    ]);
    const comparison = {
      conventional: {
        tickets: [],
        supplemental_fares: [firstConventional, secondConventional],
        original_currency_totals: { TWD: "22000" },
        estimated_twd: "22000",
      },
      back_to_back: {
        tickets: [],
        supplemental_fares: [head, middle, tail],
        original_currency_totals: { TWD: "16000" },
        estimated_twd: "16000",
      },
      savings_twd: "6000",
      savings_percent: "27.3",
      verdict: "back_to_back_cheaper",
      detail: "外站兩段票估算較省。",
    };
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(ok(status))
      .mockResolvedValueOnce(ok({
        queried_at: "2026-08-30T10:00:00Z",
        query: {
          strategy: "reverse_two_segment",
          first_destination: "TYO",
          second_destination: "SEL",
        },
        pricing_capability: "full_back_to_back",
        comparisons: [
          { ...comparison, mode: "mixed_airlines" },
          { ...comparison, mode: "same_airline" },
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
    for (const [label, value] of [
      ["頭段單程每人價格", "3000"],
      ["中段反向兩航段每人價格", "9000"],
      ["尾段單程每人價格", "4000"],
      ["第一次一般來回每人價格", "12000"],
      ["第二次一般來回每人價格", "10000"],
    ]) {
      fireEvent.change(screen.getByLabelText(label), { target: { value } });
    }
    fireEvent.click(screen.getByRole("button", { name: "比較倒買價格" }));

    expect((await screen.findAllByText(/外站兩段票估算省下.*6,000/)).length).toBe(2);
    expect(screen.getByText("不同目的地的外站兩段票已支援")).toBeTruthy();
    expect(screen.getAllByText(/中段反向兩航段票.*手動輸入/).length).toBeGreaterThan(0);
    expect(screen.getAllByText("SEL").length).toBeGreaterThan(0);
    expect(screen.queryByText("需串接開口票價格來源")).toBeNull();
    const [, init] = fetchMock.mock.calls[1];
    expect(JSON.parse(String(init.body))).toMatchObject({
      first_destination: "TYO",
      second_destination: "SEL",
      middle_two_segment_fare: { amount: "9000" },
      conventional_first_fare: { amount: "12000" },
      conventional_second_fare: { amount: "10000" },
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

  it("warns that a STARLUX-only full comparison needs four matching cached fares", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(ok(status)));
    render(<AirlineFareLab />);
    await screen.findByText("政策停用");
    fireEvent.click(screen.getByRole("tab", { name: "倒買法" }));

    for (const airline of ["華航CI", "長榮BR"]) {
      fireEvent.click(screen.getByRole("checkbox", { name: airline }));
    }

    expect(screen.getByText("單選星宇可能沒有完整倒買組合")).toBeTruthy();
    expect(screen.getByText(/若要先驗證完整流程，可同時勾選華航/)).toBeTruthy();
  });
});
