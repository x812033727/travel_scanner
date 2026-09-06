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

afterEach(() => vi.unstubAllGlobals());

describe("trip weather panel", () => {
  it("shows current weather and highlights the selected trip day", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(response(weather)));

    render(<TripWeatherPanel tripId="trip-1" activeDay="2026-09-01" />);

    expect(await screen.findByText("東京車站天氣")).toBeTruthy();
    expect(screen.getByText("28°C")).toBeTruthy();
    expect(screen.getByLabelText("2026-09-01 天氣摘要").textContent).toContain("降雨 60%");
    expect(screen.getByLabelText("10 日天氣預報").querySelector("[aria-current='date']")).toBeTruthy();
  });

  it("explains when a trip date is outside the ten-day forecast window", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(response(weather)));

    render(<TripWeatherPanel tripId="trip-1" activeDay="2026-12-20" />);

    expect(await screen.findByText(/尚未進入 10 日預報範圍/)).toBeTruthy();
  });

  it("names the provider that answered and shows rainfall when no probability is given", async () => {
    const met = {
      ...weather,
      attribution: "MET Norway",
      days: [{ ...weather.days[0], precipitation_probability_percent: null, precipitation_mm: 4.6 }],
    };
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(response(met)));

    render(<TripWeatherPanel tripId="trip-1" activeDay="2026-09-01" />);

    expect(await screen.findByText("MET NORWAY")).toBeTruthy();
    expect(screen.getByLabelText("2026-09-01 天氣摘要").textContent).toContain("降雨 4.6 mm");
    expect(screen.getByText(/MET Norway · 剛剛更新/)).toBeTruthy();
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
  });

  it("lets the user retry a temporary weather failure", async () => {
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(response({ detail: "暫時無法取得" }, 502))
      .mockResolvedValueOnce(response(weather));
    vi.stubGlobal("fetch", fetchMock);

    render(<TripWeatherPanel tripId="trip-1" activeDay="2026-09-01" />);
    fireEvent.click(await screen.findByRole("button", { name: "重試" }));

    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(2));
    expect(await screen.findByText("東京車站天氣")).toBeTruthy();
  });
});
