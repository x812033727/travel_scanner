import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { TripWeatherPanel } from "./trip-weather-panel";

const weather = {
  attribution: "Google Weather",
  location_name: "東京車站",
  current: {
    observed_at: "2026-09-01T03:15:00Z",
    is_daytime: true,
    condition: { description: "晴時多雲", type: "PARTLY_CLOUDY" },
    temperature_c: 28.4,
    feels_like_c: 30.1,
    relative_humidity_percent: 66,
    precipitation_probability_percent: 20,
    wind_speed_kph: 12,
    uv_index: 5,
  },
  days: [{
    date: "2026-09-01",
    condition: { description: "局部短暫雨", type: "SHOWERS" },
    min_temperature_c: 24.8,
    max_temperature_c: 31.2,
    relative_humidity_percent: 82,
    precipitation_probability_percent: 60,
    wind_speed_kph: 14,
    uv_index: 6,
  }],
  retrieved_at: "2026-09-01T03:15:00Z",
  cache_status: "fresh",
  warnings: [],
};

function response(payload: unknown, status = 200) {
  return { ok: status < 400, status, json: async () => payload };
}

// These are theme contracts, not simulated contrast measurements: browser
// readability tests verify the computed colours against the real stylesheet.
function expectThemeAwarePanel() {
  const panel = screen.getByRole("region", { name: "旅程天氣" });
  expect(panel.classList.contains("bg-[var(--surface)]")).toBe(true);
  expect(panel.classList.contains("text-[var(--ink)]")).toBe(true);
  const classes = [panel, ...panel.querySelectorAll("[class]")]
    .map((node) => node.getAttribute("class") || "").join(" ");
  expect(classes).not.toMatch(/(?:^|\s)(?:bg-white(?:\/\S+)?|border-white(?:\/\S+)?|bg-\[linear-gradient\S+|bg-slate-100)(?=\s|$)/);
  expect(classes).not.toContain("--surface-raised");
  expect(classes).not.toContain("--surface-tint");
  return panel;
}

afterEach(() => vi.unstubAllGlobals());

describe("trip weather panel", () => {
  it("uses semantic surfaces for the loading panel and skeleton", () => {
    vi.stubGlobal("fetch", vi.fn(() => new Promise(() => {})));

    render(<TripWeatherPanel tripId="trip-1" activeDay="2026-09-01" />);

    const panel = expectThemeAwarePanel();
    expect([...panel.children].filter((node) => node.classList.contains("bg-[var(--paper)]")).length).toBe(2);
  });

  it("shows current weather and highlights the selected trip day", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(response(weather)));

    render(<TripWeatherPanel tripId="trip-1" activeDay="2026-09-01" />);

    expect(await screen.findByText("東京車站天氣")).toBeTruthy();
    expect(screen.getByText("28°C")).toBeTruthy();
    expect(screen.getByLabelText("2026-09-01 天氣摘要").textContent).toContain("降雨 60%");
    expect(screen.getByLabelText("10 日天氣預報").querySelector("[aria-current='date']")).toBeTruthy();
    expectThemeAwarePanel();
    expect(screen.getByLabelText("2026-09-01 天氣摘要").classList.contains("bg-[var(--paper)]")).toBe(true);
  });

  it("explains when a trip date is outside the ten-day forecast window", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(response(weather)));

    render(<TripWeatherPanel tripId="trip-1" activeDay="2026-12-20" />);

    expect(await screen.findByText(/尚未進入 10 日預報範圍/)).toBeTruthy();
    expectThemeAwarePanel();
  });

  it("shows nothing but the explanation when the whole trip is beyond the forecast", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(response(weather)));

    render(<TripWeatherPanel tripId="trip-1" activeDay="2026-12-20" startDate="2026-12-20" endDate="2026-12-25" />);

    expect(await screen.findByText(/尚未進入 10 日預報範圍/)).toBeTruthy();
    // Ten cards and a big "28°C" for days nobody is travelling read as this
    // trip's weather; only the sentence saying it is too early belongs here.
    expect(screen.queryByLabelText("10 日天氣預報")).toBeNull();
    expect(screen.queryByText("28°C")).toBeNull();
    expectThemeAwarePanel();
  });

  it("keeps only the days that fall inside the trip", async () => {
    const spread = {
      ...weather,
      days: [
        { ...weather.days[0], date: "2026-08-30" },
        { ...weather.days[0], date: "2026-09-01" },
        { ...weather.days[0], date: "2026-09-02" },
        { ...weather.days[0], date: "2026-09-09" },
      ],
    };
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(response(spread)));

    render(<TripWeatherPanel tripId="trip-1" activeDay="2026-09-01" startDate="2026-09-01" endDate="2026-09-02" />);

    const rail = await screen.findByLabelText("10 日天氣預報");
    expect(rail.querySelectorAll("article").length).toBe(2);
    expectThemeAwarePanel();
    expect(rail.querySelector("article:not([aria-current])")?.classList.contains("bg-[var(--paper)]")).toBe(true);
  });

  it("names the provider that answered and shows rainfall when no probability is given", async () => {
    const met = {
      ...weather,
      attribution: "MET Norway",
      days: [{ ...weather.days[0], precipitation_probability_percent: null, precipitation_mm: 4.6 }],
      warnings: ["山區天氣變化較快，請留意即時資訊。"],
    };
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(response(met)));

    render(<TripWeatherPanel tripId="trip-1" activeDay="2026-09-01" />);

    expect(await screen.findByText("MET NORWAY")).toBeTruthy();
    expect(screen.getByLabelText("2026-09-01 天氣摘要").textContent).toContain("降雨 4.6 mm");
    expect(screen.getByText(/MET Norway · 剛剛更新/)).toBeTruthy();
    expect(screen.getByText("山區天氣變化較快，請留意即時資訊。")).toBeTruthy();
    expectThemeAwarePanel();
  });

  it("shows setup guidance without retrying a disabled API", async () => {
    const fetchMock = vi.fn().mockResolvedValue(response({
      code: "weather_api_not_enabled",
      detail: "Google Weather API 尚未啟用",
    }, 503));
    vi.stubGlobal("fetch", fetchMock);

    render(<TripWeatherPanel tripId="trip-1" activeDay="2026-09-01" />);

    expect(await screen.findByText("天氣服務尚未啟用")).toBeTruthy();
    expect(screen.queryByRole("button", { name: "重試" })).toBeNull();
    expect(fetchMock).toHaveBeenCalledTimes(1);
    expectThemeAwarePanel();
  });

  it("lets the user retry a temporary weather failure", async () => {
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(response({ detail: "暫時無法取得" }, 502))
      .mockResolvedValueOnce(response(weather));
    vi.stubGlobal("fetch", fetchMock);

    render(<TripWeatherPanel tripId="trip-1" activeDay="2026-09-01" />);
    const retry = await screen.findByRole("button", { name: "重試" });
    expectThemeAwarePanel();
    expect(retry.classList.contains("bg-[var(--paper)]")).toBe(true);
    fireEvent.click(retry);

    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(2));
    expect(await screen.findByText("東京車站天氣")).toBeTruthy();
    expectThemeAwarePanel();
  });
});
