import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { AdminSettingsPanel } from "./admin-settings-panel";

const snapshot = {
  encryption_source: "SETTINGS_ENCRYPTION_KEY",
  providers: [
    {
      provider: "google_maps",
      label: "Google Maps",
      description: "地點與路線",
      enabled: true,
      configured: true,
      status: "ready",
      status_message: "Places 與 Routes 已設定",
      config: { route_cache_ttl_seconds: 900 },
      config_sources: { route_cache_ttl_seconds: "environment" },
      secrets: {
        google_maps_api_key: { configured: true, masked: "••••••••abcd", source: "database" },
        next_public_google_maps_browser_key: { configured: false, source: "none" },
      },
      usage: {
        period: "2026-08",
        period_start: "2026-08-01",
        period_end: "2026-08-31",
        used: 321,
        monthly_limit: 33000,
        remaining: 32679,
        percentage: 1,
        free_limit: 33000,
        free_usage: 321,
        free_remaining: 32679,
        billable_overage: 0,
        breakdown: {
          places_autocomplete: 200,
          place_details: 80,
          places_text_search: 20,
          places_photo: 11,
          routes: 10,
          weather_current: 0,
          weather_daily_forecast: 0,
        },
        sku_usage: [
          { sku: "autocomplete_requests", label: "Autocomplete Requests", category: "essentials", operations: ["places_autocomplete"], used: 200, free_limit: 10000, free_usage: 200, free_remaining: 9800, billable_overage: 0, percentage: 2 },
          { sku: "place_details_enterprise", label: "Place Details Enterprise", category: "enterprise", operations: ["place_details"], used: 80, free_limit: 1000, free_usage: 80, free_remaining: 920, billable_overage: 0, percentage: 8 },
          { sku: "text_search_enterprise", label: "Text Search Enterprise", category: "enterprise", operations: ["places_text_search"], used: 20, free_limit: 1000, free_usage: 20, free_remaining: 980, billable_overage: 0, percentage: 2 },
          { sku: "place_details_photos", label: "Place Details Photos", category: "enterprise", operations: ["places_photo"], used: 11, free_limit: 1000, free_usage: 11, free_remaining: 989, billable_overage: 0, percentage: 1.1 },
          { sku: "compute_routes_essentials", label: "Compute Routes Essentials", category: "essentials", operations: ["routes"], used: 10, free_limit: 10000, free_usage: 10, free_remaining: 9990, billable_overage: 0, percentage: 0.1 },
          { sku: "weather_usage", label: "Weather Usage", category: "essentials", operations: ["weather_current", "weather_daily_forecast"], used: 0, free_limit: 10000, free_usage: 0, free_remaining: 10000, billable_overage: 0, percentage: 0 },
        ],
        monthly_history: [
          { period: "2026-08", period_start: "2026-08-01", period_end: "2026-08-31", used: 321, free_limit: 33000, free_usage: 321, free_remaining: 32679, billable_overage: 0, breakdown: {}, sku_usage: [], tracking_started_at: "2026-08-01T00:00:00Z" },
          { period: "2026-07", period_start: "2026-07-01", period_end: "2026-07-31", used: 120, free_limit: 33000, free_usage: 120, free_remaining: 32880, billable_overage: 0, breakdown: {}, sku_usage: [], tracking_started_at: "2026-07-10T00:00:00Z" },
        ],
        tracking_started_at: "2026-08-01T00:00:00Z",
        observed_at: "2026-08-31T12:00:00Z",
        available: true,
        scope: "server_requests",
        billing_timezone: "America/Los_Angeles",
        pricing_region: "global",
      },
    },
  ],
  audit: [],
};

const systemSnapshot = {
  ...snapshot,
  providers: [
    {
      provider: "runtime",
      label: "執行模式與保護設定",
      description: "系統執行設定",
      enabled: true,
      configured: true,
      status: "ready",
      status_message: "目前設定已套用",
      config: {
        registration_enabled: true,
        travel_provider_mode: "amadeus",
        provider_timeout_seconds: 8,
      },
      config_sources: {
        registration_enabled: "environment",
        travel_provider_mode: "environment",
        provider_timeout_seconds: "database",
      },
      secrets: {},
    },
    ...snapshot.providers,
  ],
  audit: [
    {
      id: "audit-system",
      action: "system_settings_updated",
      target: "runtime",
      metadata: { registration_enabled: false },
      created_at: "2026-09-01T12:00:00Z",
    },
    {
      id: "audit-provider",
      action: "provider_settings_updated",
      target: "google_maps",
      metadata: { enabled: true },
      created_at: "2026-09-01T11:00:00Z",
    },
  ],
};

const bookingProvider = {
  provider: "booking_demand",
  label: "Booking.com Demand API",
  description: "飯店即時查價",
  enabled: true,
  configured: true,
  status: "ready",
  status_message: "Demand API 已設定",
  config: { booking_demand_env: "sandbox" },
  config_sources: { booking_demand_env: "environment" },
  secrets: {},
};

const providerTabsSnapshot = {
  ...snapshot,
  providers: [...snapshot.providers, bookingProvider],
  audit: [{
    id: "audit-provider",
    action: "provider_settings_updated",
    target: "google_maps",
    metadata: { config_fields: ["route_cache_ttl_seconds"] },
    created_at: "2026-09-01T11:00:00Z",
  }],
};

const layoutSnapshot = {
  ...snapshot,
  providers: [{
    provider: "layout",
    label: "前台版面管理",
    description: "控制公開前台功能入口",
    enabled: true,
    configured: true,
    status: "ready",
    status_message: "目前開放 6／6 個前台模組",
    config: {
      hotspots_enabled: true,
      trips_enabled: true,
      alerts_enabled: true,
      flight_status_enabled: true,
      airline_fares_enabled: true,
      pricing_enabled: true,
    },
    config_sources: {
      hotspots_enabled: "environment",
      trips_enabled: "environment",
      alerts_enabled: "environment",
      flight_status_enabled: "environment",
      airline_fares_enabled: "environment",
      pricing_enabled: "environment",
    },
    secrets: {},
  }],
  audit: [],
};

afterEach(() => vi.unstubAllGlobals());

describe("AdminSettingsPanel", () => {
  it("renders one provider tab at a time and preserves unsaved drafts", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(
      new Response(JSON.stringify(providerTabsSnapshot), { status: 200 }),
    ));
    render(<AdminSettingsPanel scope="providers" />);

    const googleHeading = await screen.findByRole("heading", { name: "Google Maps" });
    fireEvent.change(within(googleHeading.closest("section")!).getByLabelText(/^路線快取秒數/), {
      target: { value: "1200" },
    });
    fireEvent.click(screen.getByRole("tab", { name: "Booking.com Demand API" }));
    expect(screen.queryByRole("heading", { name: "Google Maps" })).toBeNull();
    expect(screen.getByRole("heading", { name: "Booking.com Demand API" })).toBeTruthy();

    fireEvent.click(screen.getByRole("tab", { name: "Google Maps" }));
    expect((screen.getByLabelText(/^路線快取秒數/) as HTMLInputElement).value).toBe("1200");
    fireEvent.click(screen.getByRole("tab", { name: "最近管理紀錄" }));
    expect(screen.queryByRole("heading", { name: "Google Maps" })).toBeNull();
    expect(screen.getByRole("heading", { name: "最近管理紀錄" })).toBeTruthy();
  });

  it("switches the single visible provider with the mobile selector", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(
      new Response(JSON.stringify(providerTabsSnapshot), { status: 200 }),
    ));
    render(<AdminSettingsPanel scope="providers" />);
    await screen.findByRole("heading", { name: "Google Maps" });

    fireEvent.change(screen.getByLabelText("選擇 API 供應商"), {
      target: { value: "booking_demand" },
    });
    expect(screen.queryByRole("heading", { name: "Google Maps" })).toBeNull();
    expect(screen.getByRole("heading", { name: "Booking.com Demand API" })).toBeTruthy();
  });

  it("loads and saves all layout switches without provider-only controls", async () => {
    const updated = {
      ...layoutSnapshot,
      providers: layoutSnapshot.providers.map((provider) => ({
        ...provider,
        config: { ...provider.config, trips_enabled: false, pricing_enabled: false },
        config_sources: { ...provider.config_sources, trips_enabled: "database", pricing_enabled: "database" },
      })),
    };
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(new Response(JSON.stringify(layoutSnapshot), { status: 200 }))
      .mockResolvedValueOnce(new Response(JSON.stringify(updated), { status: 200 }));
    vi.stubGlobal("fetch", fetchMock);
    render(<AdminSettingsPanel scope="layout" />);

    const trips = await screen.findByRole("switch", { name: /我的旅行/ });
    const pricing = screen.getByRole("switch", { name: /方案與次數包/ });
    expect(screen.getAllByRole("switch")).toHaveLength(6);
    expect(screen.getAllByText("環境預設")).toHaveLength(6);
    expect(screen.queryByRole("button", { name: "測試連線" })).toBeNull();
    expect(screen.queryByLabelText("啟用")).toBeNull();
    fireEvent.click(trips);
    fireEvent.click(pricing);
    fireEvent.click(screen.getByRole("button", { name: "儲存設定" }));

    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(2));
    const request = fetchMock.mock.calls[1][1] as RequestInit;
    expect(JSON.parse(String(request.body)).config).toEqual({
      trips_enabled: false,
      pricing_enabled: false,
    });
    expect(await screen.findByText("版面設定已儲存，前台狀態已更新。")).toBeTruthy();
  });

  it("separates runtime settings from provider credentials", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(
      new Response(JSON.stringify(systemSnapshot), { status: 200 }),
    ));

    const { rerender } = render(<AdminSettingsPanel scope="providers" />);
    expect(await screen.findByRole("heading", { name: "Google Maps" })).toBeTruthy();
    expect(screen.queryByRole("heading", { name: "執行模式與保護設定" })).toBeNull();

    rerender(<AdminSettingsPanel scope="system" />);
    expect(await screen.findByRole("heading", { name: "執行模式與保護設定" })).toBeTruthy();
    expect(screen.queryByRole("heading", { name: "Google Maps" })).toBeNull();
    expect(screen.getByText(/更新系統設定/)).toBeTruthy();
    expect(screen.queryByText(/更新供應商設定/)).toBeNull();
  });

  it("loads and saves the public registration switch as a boolean", async () => {
    const disabledSnapshot = {
      ...systemSnapshot,
      providers: systemSnapshot.providers.map((provider) => provider.provider === "runtime" ? {
        ...provider,
        config: { ...provider.config, registration_enabled: false },
        config_sources: { ...provider.config_sources, registration_enabled: "database" },
      } : provider),
    };
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(new Response(JSON.stringify(systemSnapshot), { status: 200 }))
      .mockResolvedValueOnce(new Response(JSON.stringify(disabledSnapshot), { status: 200 }));
    vi.stubGlobal("fetch", fetchMock);
    render(<AdminSettingsPanel scope="system" />);

    const registrationSwitch = await screen.findByRole("switch", { name: /開放公開註冊/ });
    expect((registrationSwitch as HTMLInputElement).checked).toBe(true);
    fireEvent.click(registrationSwitch);
    fireEvent.click(screen.getByRole("button", { name: "儲存設定" }));

    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(2));
    const request = fetchMock.mock.calls[1][1] as RequestInit;
    const body = JSON.parse(String(request.body));
    expect(body.config).toEqual({ registration_enabled: false });
    expect(await screen.findByText("系統設定已儲存並立即套用。")).toBeTruthy();
  });

  it("shows the current Google Maps monthly usage and remaining free allowance", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(
      new Response(JSON.stringify(snapshot), { status: 200 }),
    ));
    render(<AdminSettingsPanel />);

    const usage = await screen.findByLabelText("Google Maps 本月用量");
    expect(within(usage).getAllByText("321").length).toBeGreaterThan(0);
    expect(within(usage).getAllByText("免費額度內使用").length).toBe(2);
    expect(within(usage).getByText("Autocomplete Requests")).toBeTruthy();
    expect(within(usage).getByText("最近 6 個帳務月份")).toBeTruthy();
    expect(within(usage).getByText("2026-07")).toBeTruthy();
    expect(within(usage).getByRole("progressbar", { name: "Autocomplete Requests 月用量" }).getAttribute("aria-valuenow")).toBe("200");
    fireEvent.click(within(usage).getByText("查看站內操作明細"));
    expect(within(usage).getByText("地點自動完成")).toBeTruthy();
  });

  it("shows only masked secrets and sends a newly entered key", async () => {
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(new Response(JSON.stringify(snapshot), { status: 200 }))
      .mockResolvedValueOnce(new Response(JSON.stringify(snapshot), { status: 200 }));
    vi.stubGlobal("fetch", fetchMock);
    render(<AdminSettingsPanel />);

    const heading = await screen.findByRole("heading", { name: "Google Maps" });
    const section = heading.closest("section");
    expect(section).toBeTruthy();
    expect(within(section!).getByPlaceholderText("••••••••abcd")).toBeTruthy();
    expect(screen.queryByDisplayValue("existing-full-key")).toBeNull();

    fireEvent.change(within(section!).getByLabelText("伺服器 API Key"), {
      target: { value: "new-server-key" },
    });
    fireEvent.click(within(section!).getByRole("button", { name: "儲存設定" }));
    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(2));
    const request = fetchMock.mock.calls[1][1] as RequestInit;
    const body = JSON.parse(String(request.body));
    expect(body.secrets.google_maps_api_key).toBe("new-server-key");
    expect(body.secrets.next_public_google_maps_browser_key).toBeUndefined();
  });

  it("explains when the account is not an administrator", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify({
      code: "admin_required",
      detail: "此功能僅限系統管理員使用",
    }), { status: 403 })));
    render(<AdminSettingsPanel />);
    expect(await screen.findByText("無法開啟管理後台")).toBeTruthy();
    expect(screen.getByText("此功能僅限系統管理員使用")).toBeTruthy();
  });

  it("shows a failed connection check as an error", async () => {
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(new Response(JSON.stringify(snapshot), { status: 200 }))
      .mockResolvedValueOnce(new Response(JSON.stringify({
        status: "failed",
        message: "API key 無效",
        latency_ms: 42,
      }), { status: 200 }))
      .mockResolvedValueOnce(new Response(JSON.stringify(snapshot), { status: 200 }));
    vi.stubGlobal("fetch", fetchMock);
    render(<AdminSettingsPanel />);

    const heading = await screen.findByRole("heading", { name: "Google Maps" });
    const section = heading.closest("section");
    fireEvent.click(within(section!).getByRole("button", { name: "測試連線" }));

    expect((await screen.findByRole("alert")).textContent).toContain("API key 無效（42 ms）");
  });

  it("edits Booking Demand search settings separately from affiliate links", async () => {
    const bookingSnapshot = {
      ...snapshot,
      providers: [{
        provider: "booking_demand",
        label: "Booking.com Demand API",
        description: "飯店即時查價",
        enabled: false,
        configured: false,
        status: "not_configured",
        status_message: "請啟用並設定憑證",
        config: {
          booking_demand_env: "sandbox",
          booking_demand_api_base_url: "https://demandapi-sandbox.booking.com/3.1",
          booking_demand_affiliate_id: "",
          booking_booker_country: "tw",
          booking_language: "zh-tw",
          booking_location_cache_ttl_seconds: 2592000,
        },
        config_sources: {
          booking_demand_env: "environment",
          booking_demand_api_base_url: "environment",
          booking_demand_affiliate_id: "environment",
          booking_booker_country: "environment",
          booking_language: "environment",
          booking_location_cache_ttl_seconds: "environment",
        },
        secrets: {
          booking_demand_api_token: { configured: false, source: "none" },
        },
      }],
    };
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(new Response(JSON.stringify(bookingSnapshot), { status: 200 }))
      .mockResolvedValueOnce(new Response(JSON.stringify(bookingSnapshot), { status: 200 }));
    vi.stubGlobal("fetch", fetchMock);
    render(<AdminSettingsPanel />);

    const heading = await screen.findByRole("heading", { name: "Booking.com Demand API" });
    const section = heading.closest("section");
    expect(section).toBeTruthy();
    fireEvent.click(within(section!).getByLabelText("啟用"));
    fireEvent.change(within(section!).getByLabelText(/^Demand API 環境/), {
      target: { value: "production" },
    });
    fireEvent.change(within(section!).getByLabelText(/^Demand API Affiliate ID/), {
      target: { value: "affiliate-456" },
    });
    fireEvent.change(within(section!).getByLabelText("Demand API Bearer Token"), {
      target: { value: "new-booking-token" },
    });
    fireEvent.click(within(section!).getByRole("button", { name: "儲存設定" }));

    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(2));
    const request = fetchMock.mock.calls[1][1] as RequestInit;
    const body = JSON.parse(String(request.body));
    expect(body.enabled).toBe(true);
    expect(body.config.booking_demand_env).toBe("production");
    expect(body.config.booking_demand_affiliate_id).toBe("affiliate-456");
    expect(body.secrets.booking_demand_api_token).toBe("new-booking-token");
  });
});
