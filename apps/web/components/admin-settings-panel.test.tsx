import { act, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { AdminSettingsPanel } from "./admin-settings-panel";
import { AdminOperationsProvider } from "./admin-operations-provider";
import { klookAffiliateCopy } from "@/lib/klook-affiliate-copy";
import type { AdminBootstrap } from "@/lib/admin-operations";

const sessionIdentity = vi.hoisted(() => ({ user: null as { id: string; email: string; preferred_currency?: string } | null, key: undefined as object | undefined }));
vi.mock("@/components/header-session", () => ({ useHeaderSession: () => ({ user: sessionIdentity.user, sessionIdentity: sessionIdentity.key ?? sessionIdentity.user }) }));

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
      config: { route_cache_ttl_seconds: 900, google_maps_javascript_enabled: false },
      config_sources: { route_cache_ttl_seconds: "environment", google_maps_javascript_enabled: "environment" },
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
        period_kind: "month",
        scope: "server_requests",
        billing_timezone: "America/Los_Angeles",
        pricing_region: "global",
      },
    },
    {
      provider: "youtube_guides",
      label: "YouTube 景點介紹",
      description: "多語景點影片搜尋",
      enabled: true,
      configured: true,
      status: "ready",
      status_message: "YouTube Data API 已設定",
      config: {
        hotspot_guide_youtube_daily_search_budget: 80,
        hotspot_guide_youtube_search_daily_free_limit: 100,
        hotspot_guide_youtube_core_daily_free_limit: 10000,
      },
      config_sources: {
        hotspot_guide_youtube_daily_search_budget: "environment",
        hotspot_guide_youtube_search_daily_free_limit: "environment",
        hotspot_guide_youtube_core_daily_free_limit: "environment",
      },
      secrets: {
        hotspot_guide_youtube_api_key: { configured: true, masked: "••••••••tube", source: "database" },
      },
      usage: {
        period: "2026-09-01",
        period_start: "2026-09-01",
        period_end: "2026-09-01",
        used: 13,
        monthly_limit: 10100,
        remaining: 10087,
        percentage: 0.1,
        free_limit: 10100,
        free_usage: 13,
        free_remaining: 10087,
        billable_overage: 0,
        breakdown: { search_list: 8, videos_list: 5 },
        sku_usage: [
          { sku: "search_queries", label: "Search Queries (search.list)", category: "search", operations: ["search_list"], used: 8, free_limit: 100, free_usage: 8, free_remaining: 92, billable_overage: 0, percentage: 8 },
          { sku: "core_api_units", label: "Core API units (videos.list)", category: "core", operations: ["videos_list"], used: 5, free_limit: 10000, free_usage: 5, free_remaining: 9995, billable_overage: 0, percentage: 0.1 },
        ],
        monthly_history: [],
        tracking_started_at: "2026-09-01T00:00:00Z",
        observed_at: "2026-09-01T12:00:00Z",
        available: true,
        period_kind: "day",
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

const braveProvider = {
  provider: "brave_guides",
  label: "Brave 多語文章搜尋",
  description: "多語文章搜尋",
  enabled: false,
  configured: false,
  status: "disabled",
  status_message: "已停用",
  config: {},
  config_sources: {},
  secrets: {},
};

const providerTabsSnapshot = {
  ...snapshot,
  providers: [...snapshot.providers, bookingProvider, braveProvider],
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

const modelOptions = {
  openai_model: [{ value: "openai-model-a", label: "OpenAI Model A" }, { value: "openai-model-b", label: "OpenAI Model B" }],
  anthropic_model: [{ value: "claude-model-a", label: "Claude Model A" }],
  minimax_model: [{ value: "minimax-model-a", label: "MiniMax Model A" }],
  gemini_model: [{ value: "gemini-model-a", label: "Gemini Model A" }],
};

const aiVendorsProvider = {
  provider: "ai_vendors",
  label: "AI 供應商與金鑰",
  description: "AI 金鑰集中管理",
  enabled: true,
  configured: true,
  status: "ready",
  status_message: "已設定：OpenAI",
  config: {
    openai_api_base_url: "https://api.openai.com/v1",
    anthropic_api_base_url: "https://api.anthropic.com/v1",
    minimax_api_base_url: "https://api.minimaxi.com/v1",
    hotspot_guide_gemini_base_url: "https://generativelanguage.googleapis.com",
  },
  config_sources: {
    openai_api_base_url: "environment",
    anthropic_api_base_url: "environment",
    minimax_api_base_url: "environment",
    hotspot_guide_gemini_base_url: "environment",
  },
  secrets: {
    openai_api_key: { configured: true, masked: "••••••••1234", source: "database" },
    anthropic_api_key: { configured: false, source: "none" },
    minimax_api_key: { configured: false, source: "none" },
    hotspot_guide_gemini_api_key: { configured: false, source: "none" },
  },
};

const aiPlannerProvider = {
  provider: "ai_planner",
  label: "AI 行程規劃",
  description: "行程規劃",
  enabled: true,
  configured: true,
  status: "ready",
  status_message: "自動備援",
  config: {
    ai_planner_mode: "auto",
    ai_planner_priority: "minimax,openai,anthropic",
    openai_model: "openai-model-a",
    anthropic_model: "claude-model-a",
    minimax_model: "minimax-model-a",
    gemini_model: "gemini-model-a",
    ai_planner_timeout_seconds: 15,
  },
  config_sources: {
    ai_planner_mode: "environment",
    ai_planner_priority: "environment",
    openai_model: "environment",
    anthropic_model: "environment",
    minimax_model: "environment",
    gemini_model: "environment",
    ai_planner_timeout_seconds: "environment",
  },
  secrets: {},
  field_options: modelOptions,
};

const aiGuideSearchProvider = {
  provider: "ai_guide_search",
  label: "AI 景點介紹搜尋",
  description: "景點介紹搜尋",
  enabled: true,
  configured: true,
  status: "ready",
  status_message: "預設 minimax",
  config: {
    hotspot_guide_ai_default_provider: "minimax",
    hotspot_guide_ai_openai_model: null,
    hotspot_guide_ai_anthropic_model: null,
    hotspot_guide_ai_minimax_model: null,
    hotspot_guide_ai_gemini_model: null,
    hotspot_guide_ai_timeout_seconds: 90,
  },
  config_sources: {
    hotspot_guide_ai_default_provider: "environment",
    hotspot_guide_ai_openai_model: "environment",
    hotspot_guide_ai_anthropic_model: "environment",
    hotspot_guide_ai_minimax_model: "environment",
    hotspot_guide_ai_gemini_model: "environment",
    hotspot_guide_ai_timeout_seconds: "environment",
  },
  secrets: {},
  field_options: {
    hotspot_guide_ai_openai_model: modelOptions.openai_model,
    hotspot_guide_ai_anthropic_model: modelOptions.anthropic_model,
    hotspot_guide_ai_minimax_model: modelOptions.minimax_model,
    hotspot_guide_ai_gemini_model: modelOptions.gemini_model,
  },
};

const introWriterProvider = {
  provider: "hotspot_intros",
  label: "AI 景點介紹撰寫",
  description: "景點介紹撰寫",
  enabled: true,
  configured: true,
  status: "ready",
  status_message: "預設 minimax",
  config: {
    hotspot_intro_ai_default_provider: "minimax",
    hotspot_intro_ai_openai_model: null,
    hotspot_intro_ai_anthropic_model: null,
    hotspot_intro_ai_minimax_model: null,
    hotspot_intro_ai_gemini_model: null,
    hotspot_intro_ai_daily_call_budget: 200,
  },
  config_sources: {
    hotspot_intro_ai_default_provider: "environment",
    hotspot_intro_ai_openai_model: "environment",
    hotspot_intro_ai_anthropic_model: "environment",
    hotspot_intro_ai_minimax_model: "environment",
    hotspot_intro_ai_gemini_model: "environment",
    hotspot_intro_ai_daily_call_budget: "environment",
  },
  secrets: {},
  field_options: {
    hotspot_intro_ai_openai_model: modelOptions.openai_model,
    hotspot_intro_ai_anthropic_model: modelOptions.anthropic_model,
    hotspot_intro_ai_minimax_model: modelOptions.minimax_model,
    hotspot_intro_ai_gemini_model: modelOptions.gemini_model,
  },
};

const geminiProvider = {
  provider: "gemini_guides",
  label: "Gemini 多語文章搜尋",
  description: "Gemini 文章搜尋",
  enabled: true,
  configured: true,
  status: "ready",
  status_message: "Gemini API 已設定",
  config: { hotspot_guide_gemini_model: "gemini-model-a", hotspot_guide_gemini_timeout_seconds: 45 },
  config_sources: { hotspot_guide_gemini_model: "environment", hotspot_guide_gemini_timeout_seconds: "environment" },
  secrets: {},
  field_options: {
    hotspot_guide_gemini_model: [
      { value: "gemini-model-a", label: "Gemini Model A", description: "目前預設" },
      { value: "gemini-model-b", label: "Gemini Model B" },
    ],
  },
};

const aiSnapshot = {
  ...snapshot,
  providers: [aiVendorsProvider, aiPlannerProvider, aiGuideSearchProvider, introWriterProvider, geminiProvider, ...snapshot.providers],
};

function stubAiFetch(value: unknown) {
  const fetchMock = vi.fn(() => Promise.resolve(new Response(JSON.stringify(value), { status: 200 })));
  vi.stubGlobal("fetch", fetchMock);
  return fetchMock;
}

async function openAiCard(name: string) {
  await screen.findByRole("heading", { name: "AI 供應商與金鑰" });
  fireEvent.click(screen.getByRole("tab", { name }));
  return screen.getByRole("heading", { name }).closest("section")!;
}

function savedBody(fetchMock: ReturnType<typeof vi.fn>) {
  const request = fetchMock.mock.calls[1][1] as RequestInit;
  return JSON.parse(String(request.body));
}

afterEach(() => {
  vi.unstubAllGlobals();
  vi.restoreAllMocks();
  sessionIdentity.user = null;
  sessionIdentity.key = undefined;
  window.history.replaceState(null, "", "/");
});

describe("AdminSettingsPanel", () => {
  it("deep-links to the single bounded catalog budget editor and saves only its changed value", async () => {
    const provider = { ...geminiProvider, updated_at: "2026-09-09T08:00:00Z", config: { ...geminiProvider.config, catalog_review_max_calls: 80, hotspot_guide_gemini_daily_search_budget: 300 } };
    const initial = { ...snapshot, providers: [provider] };
    const saved = { ...initial, providers: [{ ...provider, config: { ...provider.config, catalog_review_max_calls: 200 } }] };
    const fetchMock = vi.fn().mockResolvedValueOnce(new Response(JSON.stringify(initial), { status: 200 })).mockResolvedValueOnce(new Response(JSON.stringify(saved), { status: 200 }));
    vi.stubGlobal("fetch", fetchMock);
    render(<AdminSettingsPanel provider="gemini_guides" field="catalog_review_max_calls" />);
    const input = await screen.findByRole("spinbutton", { name: /目錄審核每個工作累計呼叫上限/ });
    expect((input as HTMLInputElement).value).toBe("80");
    expect(input.getAttribute("min")).toBe("1");
    expect(input.getAttribute("max")).toBe("1000");
    expect(input.getAttribute("step")).toBe("1");
    expect(document.getElementById(input.getAttribute("aria-describedby")!)?.textContent).toContain("不是 Gemini 專案配額");
    expect(screen.getByText(/儲存只影響新工作，不會自動續跑/)).toBeTruthy();
    fireEvent.change(input, { target: { value: "200" } });
    fireEvent.click(screen.getByRole("button", { name: "儲存設定" }));
    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(2));
    expect(fetchMock.mock.calls[1][0]).toBe("/api/travel/admin/provider-settings/gemini_guides");
    expect(savedBody(fetchMock)).toEqual({ config: { catalog_review_max_calls: 200 }, secrets: {}, expected_updated_at: "2026-09-09T08:00:00Z" });
    expect((screen.getByRole("spinbutton", { name: /^每日搜尋上限/ }) as HTMLInputElement).value).toBe("300");
  });

  it.each(["", "0", "1001", "1.5"])("refuses invalid catalog budget %s without writing or dropping the draft", async (value) => {
    const fetchMock = stubAiFetch({ ...snapshot, providers: [{ ...geminiProvider, config: { ...geminiProvider.config, catalog_review_max_calls: 80 } }] });
    render(<AdminSettingsPanel provider="gemini_guides" field="catalog_review_max_calls" />);
    const input = await screen.findByRole("spinbutton", { name: /目錄審核每個工作累計呼叫上限/ });
    fireEvent.change(input, { target: { value } });
    fireEvent.click(screen.getByRole("button", { name: "儲存設定" }));
    expect(await screen.findByText("每個工作呼叫上限必須是 1–1000 的整數。")).toBeTruthy();
    expect(input.getAttribute("aria-invalid")).toBe("true");
    expect((input as HTMLInputElement).value).toBe(value);
    expect(fetchMock).toHaveBeenCalledTimes(1);
  });

  it("saves a direct Klook affiliate ID as text without requiring or calling a pricing API", async () => {
    const data = { ...snapshot, providers: [{ provider: "klook", label: "Klook", description: "Affiliate links", enabled: true,
      configured: true, status: "ready", status_message: "Affiliate links ready", config: { klook_affiliate_id: "12345" },
      config_sources: { klook_affiliate_id: "database" }, secrets: { klook_api_key: { configured: false, source: "none" } }, updated_at: null }] };
    const fetchMock = vi.fn().mockImplementation(async () => new Response(JSON.stringify(data), { status: 200 }));
    vi.stubGlobal("fetch", fetchMock);
    render(<AdminSettingsPanel provider="klook" field="klook_affiliate_id" />);
    const field = await screen.findByLabelText(/^Klook Affiliate ID/);
    expect(screen.getByText(klookAffiliateCopy("zh-TW").noApi)).toBeTruthy();
    expect(fetchMock).toHaveBeenCalledTimes(1);
    fireEvent.change(field, { target: { value: "67890" } });
    fireEvent.click(screen.getByRole("button", { name: "儲存設定" }));
    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(2));
    expect(String(fetchMock.mock.calls[1][0])).toContain("/admin/provider-settings/klook");
    expect(JSON.parse(String(fetchMock.mock.calls[1][1].body))).toEqual({ config: { klook_affiliate_id: "67890" }, secrets: {}, expected_updated_at: null });
    expect(fetchMock.mock.calls.some(([url]) => String(url).includes("test-connection") || String(url).includes("hotel-quotes"))).toBe(false);
  });
  it("keeps active and retained drafts when currency/profile updates replace the user object", async () => {
    sessionIdentity.key = {};
    sessionIdentity.user = { id: "profile-admin", email: "admin@example.com", preferred_currency: "TWD" };
    const fetchMock = stubAiFetch(snapshot);
    const first = render(<AdminSettingsPanel />);
    fireEvent.change(await screen.findByLabelText("伺服器 API Key"), { target: { value: "same-login-key" } });
    fireEvent.change(screen.getByLabelText(/^路線快取秒數/), { target: { value: "1200" } });
    sessionIdentity.user = { ...sessionIdentity.user, preferred_currency: "USD" };
    first.rerender(<AdminSettingsPanel />);
    expect((screen.getByLabelText("伺服器 API Key") as HTMLInputElement).value).toBe("same-login-key");
    expect(fetchMock).toHaveBeenCalledTimes(1);
    first.unmount();
    sessionIdentity.user = { ...sessionIdentity.user, email: "updated@example.com" };
    render(<AdminSettingsPanel />);
    expect((await screen.findByLabelText("伺服器 API Key") as HTMLInputElement).value).toBe("same-login-key");
    expect((screen.getByLabelText(/^路線快取秒數/) as HTMLInputElement).value).toBe("1200");
  });

  it("does not resurrect discarded secret drafts when a late usage refresh completes", async () => {
    sessionIdentity.user = { id: "discard-race-admin", email: "admin@example.com" };
    vi.spyOn(window, "confirm").mockReturnValue(true);
    let finishRefresh!: (response: Response) => void;
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(new Response(JSON.stringify(snapshot), { status: 200 }))
      .mockImplementationOnce(() => new Promise<Response>((resolve) => { finishRefresh = resolve; }))
      .mockResolvedValueOnce(new Response(JSON.stringify(snapshot), { status: 200 }));
    vi.stubGlobal("fetch", fetchMock);
    const first = render(<AdminSettingsPanel />);
    fireEvent.change(await screen.findByLabelText("伺服器 API Key"), { target: { value: "discard-this-key" } });
    fireEvent.click(screen.getByRole("button", { name: "重新整理用量" }));
    window.dispatchEvent(new CustomEvent("admin:before-navigate", { cancelable: true, detail: { url: "/admin/foods" } }));
    await act(async () => { finishRefresh(new Response(JSON.stringify(snapshot), { status: 200 })); });
    first.unmount();
    render(<AdminSettingsPanel />);
    expect((await screen.findByLabelText("伺服器 API Key") as HTMLInputElement).value).toBe("");
  });

  it("ignores a stale usage snapshot arriving after a successful save", async () => {
    const newer = { ...snapshot, providers: snapshot.providers.map((item) => item.provider === "google_maps" ? { ...item, updated_at: "2026-09-08T02:00:00Z", config: { ...item.config, route_cache_ttl_seconds: 1200 } } : item) };
    let finishRefresh!: (response: Response) => void;
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(new Response(JSON.stringify(snapshot), { status: 200 }))
      .mockImplementationOnce(() => new Promise<Response>((resolve) => { finishRefresh = resolve; }))
      .mockResolvedValueOnce(new Response(JSON.stringify(newer), { status: 200 }));
    vi.stubGlobal("fetch", fetchMock);
    render(<AdminSettingsPanel />);
    fireEvent.change(await screen.findByLabelText(/^路線快取秒數/), { target: { value: "1200" } });
    fireEvent.click(screen.getByRole("button", { name: "重新整理用量" }));
    fireEvent.click(screen.getByRole("button", { name: "儲存設定" }));
    await screen.findByText("Google Maps 設定已加密儲存並立即套用。");
    await act(async () => { finishRefresh(new Response(JSON.stringify(snapshot), { status: 200 })); });
    expect((screen.getByLabelText(/^路線快取秒數/) as HTMLInputElement).value).toBe("1200");
    expect((screen.getByRole("button", { name: "儲存設定" }) as HTMLButtonElement).disabled).toBe(true);
  });

  it("restores Back/Forward drafts in memory with their original version and never persists secrets", async () => {
    sessionIdentity.user = { id: "back-forward-admin", email: "admin@example.com" };
    const storage = vi.spyOn(Storage.prototype, "setItem");
    const initial = { ...snapshot, providers: snapshot.providers.map((item) => ({ ...item, updated_at: "2026-09-08T00:00:00Z" })) };
    const newer = { ...initial, providers: initial.providers.map((item) => ({ ...item, updated_at: "2026-09-08T02:00:00Z" })) };
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(new Response(JSON.stringify(initial), { status: 200 }))
      .mockResolvedValueOnce(new Response(JSON.stringify(newer), { status: 200 }))
      .mockResolvedValueOnce(new Response(JSON.stringify(newer), { status: 200 }));
    vi.stubGlobal("fetch", fetchMock);
    const first = render(<AdminSettingsPanel />);
    fireEvent.change(await screen.findByLabelText(/^路線快取秒數/), { target: { value: "1200" } });
    fireEvent.change(screen.getByLabelText("伺服器 API Key"), { target: { value: "memory-only-key" } });
    window.dispatchEvent(new PopStateEvent("popstate"));
    first.unmount();
    render(<AdminSettingsPanel />);
    expect((await screen.findByLabelText(/^路線快取秒數/) as HTMLInputElement).value).toBe("1200");
    expect((screen.getByLabelText("伺服器 API Key") as HTMLInputElement).value).toBe("memory-only-key");
    expect(storage.mock.calls.some((call) => String(call).includes("memory-only-key"))).toBe(false);
    fireEvent.click(screen.getByRole("button", { name: "儲存設定" }));
    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(3));
    expect(JSON.parse(String((fetchMock.mock.calls[2][1] as RequestInit).body)).expected_updated_at).toBe("2026-09-08T00:00:00Z");
  });

  it.each(["new-login", "confirmed-discard"])("does not restore secret drafts after %s", async (reason) => {
    sessionIdentity.user = { id: "same-account", email: "admin@example.com" };
    const confirm = vi.spyOn(window, "confirm").mockReturnValue(true);
    stubAiFetch(snapshot);
    const first = render(<AdminSettingsPanel />);
    fireEvent.change(await screen.findByLabelText("伺服器 API Key"), { target: { value: "do-not-restore" } });
    if (reason === "confirmed-discard") {
      window.dispatchEvent(new CustomEvent("admin:before-navigate", { cancelable: true, detail: { url: "/admin/foods" } }));
      expect(confirm).toHaveBeenCalledTimes(1);
    }
    first.unmount();
    if (reason === "new-login") sessionIdentity.user = { id: "same-account", email: "admin@example.com" };
    render(<AdminSettingsPanel />);
    expect((await screen.findByLabelText("伺服器 API Key") as HTMLInputElement).value).toBe("");
    expect((screen.getByRole("button", { name: "儲存設定" }) as HTMLButtonElement).disabled).toBe(true);
  });

  it("edits only food-owned fields and links shared credentials without a paid call", async () => {
    const foodSnapshot = {
      ...snapshot,
      providers: [{ ...snapshot.providers[0], updated_at: "2026-09-08T00:00:00Z", config: {
        ...snapshot.providers[0].config, restaurant_scan_enabled: true, restaurant_aggregate_monthly_budget: 4000,
      } }],
    };
    const fetchMock = stubAiFetch(foodSnapshot);
    render(<AdminSettingsPanel scope="foods" />);
    const budget = await screen.findByLabelText(/^餐廳 Aggregate 每月安全上限/);
    expect(screen.queryByLabelText(/^路線快取秒數/)).toBeNull();
    expect(screen.queryByLabelText("伺服器 API Key")).toBeNull();
    expect(screen.queryByRole("button", { name: "測試連線" })).toBeNull();
    expect(fetchMock).toHaveBeenCalledTimes(1);
    expect(document.querySelector('[data-settings-field="google_maps_api_key"] a')?.getAttribute("href")).toBe("/admin/settings?provider=google_maps&field=google_maps_api_key");
    fireEvent.change(budget, { target: { value: "3500" } });
    fireEvent.click(screen.getByRole("button", { name: "儲存設定" }));
    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(2));
    expect(savedBody(fetchMock)).toEqual({ config: { restaurant_aggregate_monthly_budget: 3500 }, secrets: {}, expected_updated_at: "2026-09-08T00:00:00Z" });
  });

  it("does not duplicate editable hotspot fields on the shared provider page", async () => {
    stubAiFetch(aiSnapshot);
    render(<AdminSettingsPanel provider="ai_guide_search" field="hotspot_guide_ai_default_provider" />);
    const heading = await screen.findByRole("heading", { name: "AI 景點介紹搜尋" });
    const section = heading.closest("section")!;
    expect(within(section).queryByLabelText(/^景點 AI 搜尋預設供應商/)).toBeNull();
    expect(within(section).queryByLabelText("啟用")).toBeNull();
    expect(within(section).queryByRole("button", { name: "儲存設定" })).toBeNull();
    const link = section.querySelector('[data-settings-field="hotspot_guide_ai_default_provider"] a');
    expect(link?.getAttribute("href")).toBe("/admin/hotspots?tab=settings&provider=ai_guide_search&field=hotspot_guide_ai_default_provider");
    await waitFor(() => expect(document.activeElement).toBe(link));
  });

  it("saving one card preserves other drafts and their original version tokens", async () => {
    const initial = { ...snapshot, providers: snapshot.providers.map((item) => ({ ...item, updated_at: "2026-09-08T00:00:00Z" })) };
    const updated = { ...initial, providers: initial.providers.map((item) => ({ ...item, updated_at: "2026-09-08T01:00:00Z", config: item.provider === "youtube_guides" ? { ...item.config, hotspot_guide_youtube_daily_search_budget: 70 } : item.config })) };
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(new Response(JSON.stringify(initial), { status: 200 }))
      .mockResolvedValueOnce(new Response(JSON.stringify(updated), { status: 200 }))
      .mockResolvedValueOnce(new Response(JSON.stringify(updated), { status: 200 }));
    vi.stubGlobal("fetch", fetchMock);
    render(<AdminSettingsPanel />);
    fireEvent.change(await screen.findByLabelText(/^路線快取秒數/), { target: { value: "1200" } });
    fireEvent.change(screen.getByLabelText("伺服器 API Key"), { target: { value: "pending-key" } });
    fireEvent.click(screen.getByRole("tab", { name: /景點內容/ }));
    fireEvent.change(screen.getByLabelText(/^每日自動搜尋上限/), { target: { value: "70" } });
    fireEvent.click(screen.getByRole("button", { name: "儲存設定" }));
    await screen.findByText("YouTube 景點介紹 設定已加密儲存並立即套用。");
    fireEvent.click(screen.getByRole("tab", { name: /地圖與路線/ }));
    expect((screen.getByLabelText(/^路線快取秒數/) as HTMLInputElement).value).toBe("1200");
    expect((screen.getByLabelText("伺服器 API Key") as HTMLInputElement).value).toBe("pending-key");
    fireEvent.click(screen.getByRole("button", { name: "儲存設定" }));
    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(3));
    expect(JSON.parse(String((fetchMock.mock.calls[2][1] as RequestInit).body))).toEqual({ config: { route_cache_ttl_seconds: 1200 }, secrets: { google_maps_api_key: "pending-key" }, expected_updated_at: "2026-09-08T00:00:00Z" });
  });

  it("refreshing usage or explicitly testing another provider preserves drafts", async () => {
    const initial = { ...snapshot, providers: snapshot.providers.map((item) => ({ ...item, updated_at: "2026-09-08T00:00:00Z" })) };
    const newer = { ...initial, providers: initial.providers.map((item) => ({ ...item, updated_at: "2026-09-08T02:00:00Z" })) };
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(new Response(JSON.stringify(initial), { status: 200 }))
      .mockResolvedValueOnce(new Response(JSON.stringify(newer), { status: 200 }))
      .mockResolvedValueOnce(new Response(JSON.stringify({ status: "success", message: "Test OK", latency_ms: 5 }), { status: 200 }))
      .mockResolvedValueOnce(new Response(JSON.stringify(newer), { status: 200 }))
      .mockResolvedValueOnce(new Response(JSON.stringify(newer), { status: 200 }));
    vi.stubGlobal("fetch", fetchMock);
    render(<AdminSettingsPanel />);
    fireEvent.change(await screen.findByLabelText(/^路線快取秒數/), { target: { value: "1200" } });
    expect((screen.getByRole("button", { name: "測試連線" }) as HTMLButtonElement).disabled).toBe(true);
    fireEvent.click(within(screen.getByLabelText("Google Maps 本月用量")).getByRole("button", { name: "重新整理用量" }));
    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(2));
    fireEvent.click(screen.getByRole("tab", { name: /景點內容/ }));
    fireEvent.click(screen.getByRole("button", { name: "測試連線" }));
    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(4));
    fireEvent.click(screen.getByRole("tab", { name: /地圖與路線/ }));
    expect((screen.getByLabelText(/^路線快取秒數/) as HTMLInputElement).value).toBe("1200");
    await waitFor(() => expect((screen.getByRole("button", { name: "儲存設定" }) as HTMLButtonElement).disabled).toBe(false));
    fireEvent.click(screen.getByRole("button", { name: "儲存設定" }));
    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(5));
    expect(JSON.parse(String((fetchMock.mock.calls[4][1] as RequestInit).body)).expected_updated_at).toBe("2026-09-08T00:00:00Z");
  });

  it("retains drafts on 409 and reloads only the conflicting card after confirmation", async () => {
    const newer = { ...snapshot, providers: snapshot.providers.map((item) => ({ ...item, updated_at: "2026-09-08T02:00:00Z", config: item.provider === "google_maps" ? { ...item.config, route_cache_ttl_seconds: 1500 } : item.config })) };
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(new Response(JSON.stringify(snapshot), { status: 200 }))
      .mockResolvedValueOnce(new Response(JSON.stringify({ code: "provider_setting_conflict", detail: "Conflict" }), { status: 409 }))
      .mockResolvedValueOnce(new Response(JSON.stringify(newer), { status: 200 }));
    vi.stubGlobal("fetch", fetchMock);
    const confirm = vi.spyOn(window, "confirm").mockReturnValue(false);
    render(<AdminSettingsPanel />);
    fireEvent.change(await screen.findByLabelText(/^路線快取秒數/), { target: { value: "1200" } });
    fireEvent.click(screen.getByRole("tab", { name: /景點內容/ }));
    fireEvent.change(screen.getByLabelText(/^每日自動搜尋上限/), { target: { value: "60" } });
    fireEvent.click(screen.getByRole("tab", { name: /地圖與路線/ }));
    fireEvent.click(screen.getByRole("button", { name: "儲存設定" }));
    expect((await screen.findByRole("alert")).textContent).toContain("你的草稿仍保留");
    expect((screen.getByLabelText(/^路線快取秒數/) as HTMLInputElement).value).toBe("1200");
    await waitFor(() => expect((screen.getByRole("button", { name: "重新載入這張卡片" }) as HTMLButtonElement).disabled).toBe(false));
    fireEvent.click(screen.getByRole("button", { name: "重新載入這張卡片" }));
    expect(fetchMock).toHaveBeenCalledTimes(2);
    confirm.mockReturnValue(true);
    fireEvent.click(screen.getByRole("button", { name: "重新載入這張卡片" }));
    await waitFor(() => expect((screen.getByLabelText(/^路線快取秒數/) as HTMLInputElement).value).toBe("1500"));
    fireEvent.click(screen.getByRole("tab", { name: /景點內容/ }));
    expect((screen.getByLabelText(/^每日自動搜尋上限/) as HTMLInputElement).value).toBe("60");
  });

  it("guards leaving the settings pathname but allows retained settings tabs", async () => {
    const oldPath = window.location.pathname + window.location.search;
    window.history.replaceState({}, "", "/zh-TW/admin/hotspots?tab=settings");
    const confirm = vi.spyOn(window, "confirm").mockReturnValue(false);
    stubAiFetch(aiSnapshot);
    const { unmount } = render(<AdminSettingsPanel scope="hotspots" />);
    try {
      const section = (await screen.findByRole("heading", { name: "AI 景點介紹搜尋" })).closest("section")!;
      fireEvent.change(within(section).getByLabelText(/^景點 AI 搜尋預設供應商/), { target: { value: "openai" } });
      const staying = new CustomEvent("admin:before-navigate", { cancelable: true, detail: { url: "/zh-TW/admin/hotspots?tab=catalog" } });
      expect(window.dispatchEvent(staying)).toBe(true);
      expect(confirm).not.toHaveBeenCalled();
      const leaving = new CustomEvent("admin:before-navigate", { cancelable: true, detail: { url: "/zh-TW/admin/foods?tab=settings" } });
      expect(window.dispatchEvent(leaving)).toBe(false);
      const unload = new Event("beforeunload", { cancelable: true });
      expect(window.dispatchEvent(unload)).toBe(false);
      const link = section.querySelector('a[href^="/admin/settings"]');
      // This card has no secrets itself. A dependency link also leaves the page.
      const shared = link || screen.getAllByRole("link", { name: "共用供應商設定" })[0];
      expect(fireEvent.click(shared)).toBe(false);
      expect(confirm).toHaveBeenCalledTimes(2);
    } finally { unmount(); window.history.replaceState({}, "", oldPath); }
  });

  it("updates the selected provider and focuses the field when deep-link props change", async () => {
    stubAiFetch(snapshot);
    const { rerender } = render(<AdminSettingsPanel provider="google_maps" field="google_maps_api_key" />);
    const key = await screen.findByLabelText("伺服器 API Key");
    await waitFor(() => expect(document.activeElement).toBe(key));
    fireEvent.change(key, { target: { value: "unsaved" } });
    rerender(<AdminSettingsPanel provider="youtube_guides" field="hotspot_guide_youtube_daily_search_budget" />);
    const budget = await screen.findByLabelText(/^每日自動搜尋上限/);
    await waitFor(() => expect(document.activeElement).toBe(budget));
    fireEvent.click(screen.getByRole("tab", { name: /地圖與路線/ }));
    expect((screen.getByLabelText("伺服器 API Key") as HTMLInputElement).value).toBe("unsaved");
  });

  it("groups providers by category and preserves unsaved drafts across tabs", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(
      new Response(JSON.stringify(providerTabsSnapshot), { status: 200 }),
    ));
    render(<AdminSettingsPanel scope="providers" />);

    const googleHeading = await screen.findByRole("heading", { name: "Google Maps" });
    const categoryTabs = screen.getByRole("tablist", { name: "API 供應商分類" });
    expect(within(categoryTabs).getAllByRole("tab").map((tab) => tab.textContent)).toEqual([
      "地圖與路線1/1",
      "景點內容1/2",
      "航班與住宿資料1/1",
      "最近管理紀錄",
    ]);
    expect(within(categoryTabs).getByRole("tab", { name: /地圖與路線/ }).getAttribute("aria-selected")).toBe("true");
    const providerTabs = screen.getByRole("tablist", { name: "API 供應商設定分頁" });
    expect(within(providerTabs).getAllByRole("tab").map((tab) => tab.textContent)).toEqual(["Google Maps"]);
    expect(screen.queryByRole("tab", { name: "Booking.com Demand API" })).toBeNull();

    fireEvent.change(within(googleHeading.closest("section")!).getByLabelText(/^路線快取秒數/), {
      target: { value: "1200" },
    });
    fireEvent.click(within(categoryTabs).getByRole("tab", { name: /航班與住宿資料/ }));
    expect(screen.queryByRole("heading", { name: "Google Maps" })).toBeNull();
    expect(screen.getByRole("heading", { name: "Booking.com Demand API" })).toBeTruthy();
    expect(screen.getByRole("tab", { name: "Booking.com Demand API" }).getAttribute("aria-selected")).toBe("true");

    fireEvent.click(within(categoryTabs).getByRole("tab", { name: /景點內容/ }));
    expect(screen.getByRole("heading", { name: "YouTube 景點介紹" })).toBeTruthy();
    fireEvent.click(screen.getByRole("tab", { name: "Brave 多語文章搜尋" }));
    expect(screen.queryByRole("heading", { name: "YouTube 景點介紹" })).toBeNull();
    expect(screen.getByRole("heading", { name: "Brave 多語文章搜尋" })).toBeTruthy();

    fireEvent.click(within(categoryTabs).getByRole("tab", { name: /地圖與路線/ }));
    expect((screen.getByLabelText(/^路線快取秒數/) as HTMLInputElement).value).toBe("1200");
    fireEvent.click(within(categoryTabs).getByRole("tab", { name: "最近管理紀錄" }));
    expect(screen.queryByRole("heading", { name: "Google Maps" })).toBeNull();
    expect(screen.queryByRole("tablist", { name: "API 供應商設定分頁" })).toBeNull();
    expect(screen.getByRole("heading", { name: "最近管理紀錄" })).toBeTruthy();
  });

  it("restores provider, field focus and audit panel from Back/Forward URL state", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(
      new Response(JSON.stringify(providerTabsSnapshot), { status: 200 }),
    ));
    window.history.replaceState(null, "", "/zh-TW/admin/settings?provider=google_maps&field=route_cache_ttl_seconds");
    render(<AdminSettingsPanel scope="providers" />);
    const timeout = await screen.findByLabelText(/^路線快取秒數/);
    await waitFor(() => expect(document.activeElement).toBe(timeout));

    window.history.pushState(null, "", "/zh-TW/admin/settings?provider=google_maps&field=google_maps_api_key");
    window.dispatchEvent(new PopStateEvent("popstate"));
    const key = screen.getByLabelText("伺服器 API Key");
    await waitFor(() => expect(document.activeElement).toBe(key));

    window.history.pushState(null, "", "/zh-TW/admin/settings?provider=__audit");
    window.dispatchEvent(new PopStateEvent("popstate"));
    await screen.findByRole("heading", { name: "最近管理紀錄" });

    window.history.pushState(null, "", "/zh-TW/admin/settings");
    window.dispatchEvent(new PopStateEvent("popstate"));
    await screen.findByRole("heading", { name: "Google Maps" });
    expect(screen.queryByRole("heading", { name: "最近管理紀錄" })).toBeNull();
  });

  it("keeps provider mutations disabled for a settings viewer", async () => {
    const fetchMock = vi.fn().mockResolvedValue(
      new Response(JSON.stringify(providerTabsSnapshot), { status: 200 }),
    );
    vi.stubGlobal("fetch", fetchMock);
    const bootstrap: AdminBootstrap = {
      admin_roles: ["viewer"],
      admin_capabilities: ["settings.read"],
      navigation: [],
      pending_counts: {},
      system_status: {},
      environment: "test",
      can_deploy: false,
      can_manage_database: false,
    };
    render(<AdminOperationsProvider bootstrap={bootstrap}><AdminSettingsPanel scope="providers" /></AdminOperationsProvider>);
    await screen.findByRole("heading", { name: "Google Maps" });
    const save = screen.getByRole("button", { name: "儲存設定" }) as HTMLButtonElement;
    const test = screen.getByRole("button", { name: "測試連線" }) as HTMLButtonElement;
    expect(save.disabled).toBe(true);
    expect(test.disabled).toBe(true);
    fireEvent.click(save);
    fireEvent.click(test);
    expect(fetchMock.mock.calls.filter(([, init]) => init?.method && init.method !== "GET")).toHaveLength(0);
  });

  it("moves between categories and providers with the keyboard", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(
      new Response(JSON.stringify(providerTabsSnapshot), { status: 200 }),
    ));
    render(<AdminSettingsPanel scope="providers" />);
    await screen.findByRole("heading", { name: "Google Maps" });

    fireEvent.keyDown(screen.getByRole("tab", { name: /地圖與路線/ }), { key: "ArrowRight" });
    expect(screen.getByRole("heading", { name: "YouTube 景點介紹" })).toBeTruthy();
    fireEvent.keyDown(screen.getByRole("tab", { name: "YouTube 景點介紹" }), { key: "ArrowRight" });
    expect(screen.getByRole("heading", { name: "Brave 多語文章搜尋" })).toBeTruthy();
    fireEvent.keyDown(screen.getByRole("tab", { name: /景點內容/ }), { key: "End" });
    expect(screen.getByRole("heading", { name: "最近管理紀錄" })).toBeTruthy();
  });

  it("switches category and provider with the mobile selectors", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(
      new Response(JSON.stringify(providerTabsSnapshot), { status: 200 }),
    ));
    render(<AdminSettingsPanel scope="providers" />);
    await screen.findByRole("heading", { name: "Google Maps" });

    const categorySelect = screen.getByLabelText("選擇設定分類") as HTMLSelectElement;
    expect(categorySelect.value).toBe("maps");
    expect(Array.from((screen.getByLabelText("選擇 API 供應商") as HTMLSelectElement).options).map((option) => option.textContent)).toEqual(["Google Maps"]);

    fireEvent.change(categorySelect, { target: { value: "travelData" } });
    expect(screen.queryByRole("heading", { name: "Google Maps" })).toBeNull();
    expect(screen.getByRole("heading", { name: "Booking.com Demand API" })).toBeTruthy();

    fireEvent.change(categorySelect, { target: { value: "content" } });
    expect(screen.getByRole("heading", { name: "YouTube 景點介紹" })).toBeTruthy();
    fireEvent.change(screen.getByLabelText("選擇 API 供應商"), { target: { value: "brave_guides" } });
    expect(screen.getByRole("heading", { name: "Brave 多語文章搜尋" })).toBeTruthy();

    fireEvent.change(categorySelect, { target: { value: "__audit" } });
    expect(screen.queryByLabelText("選擇 API 供應商")).toBeNull();
    expect(screen.getByRole("heading", { name: "最近管理紀錄" })).toBeTruthy();
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
    expect(screen.getAllByRole("switch")).toHaveLength(5);
    expect(screen.getAllByText("環境預設")).toHaveLength(5);
    expect(screen.queryByRole("switch", { name: /熱門景點/ })).toBeNull();
    expect(document.querySelector('[data-settings-field="hotspots_enabled"] a')?.getAttribute("href")).toBe("/admin/hotspots?tab=settings&provider=layout&field=hotspots_enabled");
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

  it("shows NAVER server usage separately from browser map and billing data", async () => {
    const naverProvider = {
      provider: "naver_maps",
      label: "NAVER Maps",
      description: "韓國地點與汽車路線",
      enabled: true,
      configured: true,
      status: "ready",
      status_message: "NAVER Maps 已設定",
      config: { naver_place_cache_ttl_seconds: 900, naver_maps_monthly_request_limit: 1000 },
      config_sources: { naver_place_cache_ttl_seconds: "environment", naver_maps_monthly_request_limit: "database" },
      secrets: {
        naver_maps_client_id: { configured: true, masked: "••••••••id12", source: "database" },
        naver_maps_client_secret: { configured: true, masked: "••••••••sec3", source: "database" },
      },
      usage: {
        period: "2026-09",
        period_start: "2026-09-01",
        period_end: "2026-09-30",
        used: 27,
        monthly_limit: 1000,
        remaining: 973,
        percentage: 2.7,
        free_limit: 1000,
        free_usage: 27,
        free_remaining: 973,
        billable_overage: 0,
        breakdown: { local_search: 12, geocode: 5, directions: 10 },
        sku_usage: [],
        monthly_history: [{ period: "2026-09", period_start: "2026-09-01", period_end: "2026-09-30", used: 27, free_limit: 1000, free_usage: 27, free_remaining: 973, billable_overage: 0, breakdown: {}, sku_usage: [] }],
        observed_at: "2026-09-01T10:00:00Z",
        available: true,
        scope: "server_requests",
        billing_timezone: "Asia/Seoul",
        pricing_region: "kr",
      },
    };
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify({
      ...snapshot,
      providers: [...snapshot.providers, naverProvider],
    }), { status: 200 })));
    render(<AdminSettingsPanel />);
    await screen.findByRole("heading", { name: "Google Maps" });
    fireEvent.click(screen.getByRole("tab", { name: "NAVER Maps" }));

    const usage = await screen.findByLabelText("NAVER Maps 本月用量");
    expect(within(usage).getAllByText("27").length).toBeGreaterThan(0);
    expect(within(usage).getAllByText("973").length).toBeGreaterThan(0);
    expect(within(usage).getByText(/不含瀏覽器 Dynamic Map/)).toBeTruthy();
    fireEvent.click(within(usage).getByText("查看站內操作明細"));
    expect(within(usage).getByText("Directions 5")).toBeTruthy();
    expect(screen.getByLabelText(/^NAVER Cloud Client ID/)).toBeTruthy();
  });

  it("shows the NAVITIME monthly cap and remaining requests", async () => {
    const navitimeProvider = {
      provider: "navitime",
      label: "NAVITIME",
      description: "日本大眾運輸班次",
      enabled: true,
      configured: true,
      status: "ready",
      status_message: "NAVITIME 憑證已設定（RapidAPI）",
      config: { navitime_api_base_url: "https://navitime-route-totalnavi.p.rapidapi.com", navitime_monthly_request_limit: 450 },
      config_sources: { navitime_api_base_url: "database", navitime_monthly_request_limit: "environment" },
      secrets: {
        navitime_client_id: { configured: false, masked: null, source: "none" },
        navitime_api_key: { configured: true, masked: "••••••••key1", source: "database" },
      },
      usage: {
        period: "2026-09",
        period_start: "2026-09-01",
        period_end: "2026-09-30",
        used: 120,
        monthly_limit: 450,
        remaining: 330,
        percentage: 26.7,
        free_limit: 450,
        free_usage: 120,
        free_remaining: 330,
        billable_overage: 0,
        breakdown: { route_transit: 120 },
        sku_usage: [],
        monthly_history: [{ period: "2026-09", period_start: "2026-09-01", period_end: "2026-09-30", used: 120, free_limit: 450, free_usage: 120, free_remaining: 330, billable_overage: 0, breakdown: {}, sku_usage: [] }],
        observed_at: "2026-09-01T10:00:00Z",
        available: true,
        scope: "server_requests",
        billing_timezone: "Asia/Tokyo",
        pricing_region: "jp",
      },
    };
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify({
      ...snapshot,
      providers: [...snapshot.providers, navitimeProvider],
    }), { status: 200 })));
    render(<AdminSettingsPanel />);
    await screen.findByRole("heading", { name: "Google Maps" });
    fireEvent.click(screen.getByRole("tab", { name: "NAVITIME" }));

    const usage = await screen.findByLabelText("NAVITIME 本月用量");
    expect(within(usage).getAllByText("120").length).toBeGreaterThan(0);
    expect(within(usage).getAllByText("330").length).toBeGreaterThan(0);
    expect(within(usage).getByRole("progressbar", { name: "NAVITIME 月用量" }).getAttribute("aria-valuenow")).toBe("120");
    expect(within(usage).getByText(/停止呼叫 NAVITIME/)).toBeTruthy();
    fireEvent.click(within(usage).getByText("查看站內操作明細"));
    expect(within(usage).getByText("NAVITIME 路線查詢")).toBeTruthy();
    expect(screen.getByLabelText(/^站內每月請求上限/)).toBeTruthy();
  });

  it("shows separate Ekispert monthly and ODsay daily hard caps", async () => {
    const usageBase = {
      period_start: "2026-09-01",
      period_end: "2026-09-30",
      free_usage: 12,
      billable_overage: 0,
      sku_usage: [],
      monthly_history: [],
      observed_at: "2026-09-01T10:00:00Z",
      available: true,
      scope: "server_requests",
    };
    const ekispertProvider = {
      provider: "ekispert",
      label: "Ekispert（駅すぱあと）",
      description: "日本大眾運輸路線",
      enabled: true,
      configured: true,
      status: "ready",
      status_message: "Ekispert 憑證已設定（平均等待時間模式）",
      config: { ekispert_api_base_url: "https://api.ekispert.jp", ekispert_search_type: "plain", ekispert_monthly_request_limit: 450 },
      config_sources: { ekispert_api_base_url: "environment", ekispert_search_type: "environment", ekispert_monthly_request_limit: "environment" },
      secrets: { ekispert_api_key: { configured: true, masked: "••••••••key1", source: "database" } },
      usage: { ...usageBase, period: "2026-09", used: 12, monthly_limit: 450, remaining: 438, percentage: 2.7, free_limit: 450, free_remaining: 438, breakdown: { search_course: 12 }, billing_timezone: "Asia/Tokyo", pricing_region: "jp", period_kind: "month" },
    };
    const odsayProvider = {
      provider: "odsay",
      label: "ODsay",
      description: "韓國大眾運輸多路線",
      enabled: true,
      configured: true,
      status: "ready",
      status_message: "ODsay Server Key 已設定",
      config: { odsay_api_base_url: "https://api.odsay.com/v1/api", odsay_language: "0", odsay_daily_request_limit: 25 },
      config_sources: { odsay_api_base_url: "environment", odsay_language: "environment", odsay_daily_request_limit: "environment" },
      secrets: { odsay_api_key: { configured: true, masked: "••••••••key2", source: "database" } },
      usage: { ...usageBase, period: "2026-09-01", period_end: "2026-09-01", used: 8, monthly_limit: 25, remaining: 17, percentage: 32, free_limit: 25, free_usage: 8, free_remaining: 17, breakdown: { search_pub_trans_path: 8 }, billing_timezone: "Asia/Seoul", pricing_region: "kr", period_kind: "day" },
    };
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify({
      ...snapshot,
      providers: [...snapshot.providers, ekispertProvider, odsayProvider],
    }), { status: 200 })));
    render(<AdminSettingsPanel />);

    await screen.findByRole("heading", { name: "Google Maps" });
    fireEvent.click(screen.getByRole("tab", { name: "Ekispert（駅すぱあと）" }));
    const ekispertUsage = await screen.findByLabelText("Ekispert 本月用量");
    expect(within(ekispertUsage).getAllByText("438").length).toBeGreaterThan(0);
    expect(screen.getByLabelText(/^路線資料模式/)).toBeTruthy();
    fireEvent.click(within(ekispertUsage).getByText("查看站內操作明細"));
    expect(within(ekispertUsage).getByText("Ekispert 路線查詢")).toBeTruthy();

    fireEvent.click(screen.getByRole("tab", { name: "ODsay" }));
    const odsayUsage = await screen.findByLabelText("ODsay 今日用量");
    expect(within(odsayUsage).getByText("今日站內請求")).toBeTruthy();
    expect(within(odsayUsage).getAllByText("17").length).toBeGreaterThan(0);
    fireEvent.click(within(odsayUsage).getByText("查看站內操作明細"));
    expect(within(odsayUsage).getByText("ODsay 大眾運輸查詢")).toBeTruthy();
    expect(screen.getByLabelText(/^站內每日請求上限/)).toBeTruthy();
  });

  it("shows YouTube daily allowance, current usage, and automatic reserve", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(
      new Response(JSON.stringify(snapshot), { status: 200 }),
    ));
    render(<AdminSettingsPanel />);

    await screen.findByRole("heading", { name: "Google Maps" });
    fireEvent.click(screen.getByRole("tab", { name: /景點內容/ }));
    const usage = await screen.findByLabelText("YouTube Data API 今日用量");
    const searchUsed = within(usage).getByText("今日搜尋使用量").parentElement;
    const searchRemaining = within(usage).getByText("搜尋額度剩餘").parentElement;
    expect(within(searchUsed!).getByText("8")).toBeTruthy();
    expect(within(searchRemaining!).getByText("92")).toBeTruthy();
    expect(within(usage).getByText(/每日最多 80 次搜尋/)).toBeTruthy();
    expect(within(usage).getByText(/保留 20 次/)).toBeTruthy();
    expect(within(usage).getByRole("progressbar", { name: "Search Queries (search.list) 日用量" }).getAttribute("aria-valuenow")).toBe("8");
    fireEvent.click(within(usage).getByText("查看站內操作明細"));
    expect(within(usage).getByText("影片搜尋（search.list）")).toBeTruthy();
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

  it("saves the browser map safety gate as a boolean", async () => {
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(new Response(JSON.stringify(snapshot), { status: 200 }))
      .mockResolvedValueOnce(new Response(JSON.stringify(snapshot), { status: 200 }));
    vi.stubGlobal("fetch", fetchMock);
    render(<AdminSettingsPanel />);

    const section = (await screen.findByRole("heading", { name: "Google Maps" })).closest("section");
    const safetyGate = within(section!).getByRole("switch", { name: /啟用瀏覽器路線地圖/ });
    expect((safetyGate as HTMLInputElement).checked).toBe(false);
    fireEvent.click(safetyGate);
    fireEvent.click(within(section!).getByRole("button", { name: "儲存設定" }));

    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(2));
    const request = fetchMock.mock.calls[1][1] as RequestInit;
    const body = JSON.parse(String(request.body));
    expect(body.config.google_maps_javascript_enabled).toBe(true);
  });

  it("explains when the account is not an administrator", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify({
      code: "admin_required",
      detail: "此功能僅限系統管理員使用",
    }), { status: 403 })));
    render(<AdminSettingsPanel />);
    expect(await screen.findByText("無法開啟管理後台")).toBeTruthy();
    expect(screen.getByText("此功能僅限系統管理員使用")).toBeTruthy();
    // 403 is the one case the ADMIN_EMAILS hint is actually about.
    expect(screen.getByText(/ADMIN_EMAILS/)).toBeTruthy();
    // Nothing to retry: a reload will be refused the same way.
    expect(screen.queryByRole("button", { name: "重新載入" })).toBeNull();
  });

  it("does not send an offline administrator to edit an environment variable", async () => {
    // fetch itself rejects, so nothing reached the server. The panel used to print this
    // browser string verbatim — untranslated in every locale — and follow it with the
    // ADMIN_EMAILS hint, which has nothing to do with a dropped connection.
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new TypeError("Failed to fetch")));
    render(<AdminSettingsPanel />);
    expect(await screen.findByText("無法開啟管理後台")).toBeTruthy();
    expect(screen.getByText("連不到伺服器。請確認網路連線，或稍後再試。")).toBeTruthy();
    expect(screen.queryByText(/Failed to fetch/)).toBeNull();
    expect(screen.queryByText(/ADMIN_EMAILS/)).toBeNull();
  });

  it("offers to load again after a server error, and succeeds on the retry", async () => {
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(new Response(JSON.stringify({ detail: "伺服器發生錯誤" }), { status: 500 }))
      .mockResolvedValueOnce(new Response(JSON.stringify(snapshot), { status: 200 }));
    vi.stubGlobal("fetch", fetchMock);
    render(<AdminSettingsPanel />);
    expect(await screen.findByText("伺服器發生錯誤")).toBeTruthy();
    // A 500 says nothing about who is signed in.
    expect(screen.queryByText(/ADMIN_EMAILS/)).toBeNull();

    fireEvent.click(screen.getByRole("button", { name: "重新載入" }));
    expect(await screen.findByRole("heading", { name: "Google Maps" })).toBeTruthy();
    expect(screen.queryByText("無法開啟管理後台")).toBeNull();
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
    render(<AdminSettingsPanel scope="hotels" />);

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
    expect(within(section!).queryByLabelText("Demand API Bearer Token")).toBeNull();
    expect(document.querySelector('[data-settings-field="booking_demand_api_token"] a')?.getAttribute("href")).toBe("/admin/settings?provider=booking_demand&field=booking_demand_api_token");
    fireEvent.click(within(section!).getByRole("button", { name: "儲存設定" }));

    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(2));
    const request = fetchMock.mock.calls[1][1] as RequestInit;
    const body = JSON.parse(String(request.body));
    expect(body.enabled).toBe(true);
    expect(body.config.booking_demand_env).toBe("production");
    expect(body.config.booking_demand_affiliate_id).toBe("affiliate-456");
    expect(body.secrets).toEqual({});
    expect(body.config).toEqual({ booking_demand_env: "production", booking_demand_affiliate_id: "affiliate-456" });
  });

  it("groups the four AI cards under AI services and hides the enable switch on the vendor card", async () => {
    stubAiFetch(aiSnapshot);
    render(<AdminSettingsPanel scope="providers" />);

    const heading = await screen.findByRole("heading", { name: "AI 供應商與金鑰" });
    const categoryTabs = screen.getByRole("tablist", { name: "API 供應商分類" });
    expect(within(categoryTabs).getAllByRole("tab").map((tab) => tab.textContent)).toEqual([
      "AI 服務5/5",
      "地圖與路線1/1",
      "景點內容1/1",
      "最近管理紀錄",
    ]);
    const providerTabs = screen.getByRole("tablist", { name: "API 供應商設定分頁" });
    expect(within(providerTabs).getAllByRole("tab").map((tab) => tab.textContent)).toEqual([
      "AI 供應商與金鑰",
      "AI 行程規劃",
      "AI 景點介紹搜尋",
      "AI 景點介紹撰寫",
      "Gemini 多語文章搜尋",
    ]);
    const section = heading.closest("section")!;
    expect(within(section).queryByLabelText("啟用")).toBeNull();
    expect((within(section).getByRole("button", { name: "測試連線" }) as HTMLButtonElement).disabled).toBe(false);
    expect(within(section).getByLabelText("OpenAI API Key")).toBeTruthy();
    expect(within(section).getByLabelText("Gemini API Key")).toBeTruthy();
    expect(within(section).getByLabelText(/^Gemini API Base URL/)).toBeTruthy();

    fireEvent.click(within(providerTabs).getByRole("tab", { name: "Gemini 多語文章搜尋" }));
    const gemini = screen.getByRole("heading", { name: "Gemini 多語文章搜尋" }).closest("section")!;
    expect(within(gemini).queryByLabelText("Gemini API Key")).toBeNull();
    expect(within(gemini).queryByLabelText(/^Gemini API Base URL/)).toBeNull();
    expect(within(gemini).getByLabelText("啟用")).toBeTruthy();
  });

  it("saves vendor keys and only the changed base URL from the shared card", async () => {
    const fetchMock = stubAiFetch(aiSnapshot);
    render(<AdminSettingsPanel />);

    const section = (await screen.findByRole("heading", { name: "AI 供應商與金鑰" })).closest("section")!;
    fireEvent.change(within(section).getByLabelText("Anthropic API Key"), { target: { value: "sk-ant-new" } });
    fireEvent.change(within(section).getByLabelText(/^OpenAI API Base URL/), { target: { value: "https://api.openai.com/v2" } });
    fireEvent.click(within(section).getByRole("button", { name: "儲存設定" }));

    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(2));
    const body = savedBody(fetchMock);
    expect(body.enabled).toBeUndefined();
    expect(body.config).toEqual({ openai_api_base_url: "https://api.openai.com/v2" });
    expect(body.secrets).toEqual({ anthropic_api_key: "sk-ant-new" });
    expect((await screen.findByRole("status")).textContent).toContain("AI 供應商與金鑰 設定已加密儲存並立即套用。");
  });

  it("orders planner model dropdowns by the automatic priority and hides them for single vendors", async () => {
    stubAiFetch(aiSnapshot);
    render(<AdminSettingsPanel />);

    const section = await openAiCard("AI 行程規劃");
    const modelLabels = () => within(section).getAllByLabelText(/^(OpenAI|Claude|MiniMax|Gemini) 模型/).map((element) => element.closest("label")!.textContent!.split(" ")[0]);
    expect(modelLabels()).toEqual(["MiniMax", "OpenAI", "Claude", "Gemini"]);
    const openaiSelect = within(section).getByLabelText(/^OpenAI 模型/) as HTMLSelectElement;
    expect(openaiSelect.tagName).toBe("SELECT");
    expect(Array.from(openaiSelect.options).map((option) => option.textContent)).toEqual(["OpenAI Model A", "OpenAI Model B", "自訂…"]);

    fireEvent.change(within(section).getByLabelText(/^自動備援順序/), { target: { value: "openai,anthropic,minimax" } });
    expect(modelLabels()).toEqual(["OpenAI", "Claude", "MiniMax", "Gemini"]);
    fireEvent.change(within(section).getByLabelText(/^AI 行程來源/), { target: { value: "anthropic" } });
    expect(modelLabels()).toEqual(["Claude"]);
    fireEvent.change(within(section).getByLabelText(/^AI 行程來源/), { target: { value: "fallback" } });
    expect(within(section).queryAllByLabelText(/^(OpenAI|Claude|MiniMax|Gemini) 模型/)).toHaveLength(0);
  });

  it("sends only the chosen model changes and leaves hidden vendor models untouched", async () => {
    const fetchMock = stubAiFetch(aiSnapshot);
    render(<AdminSettingsPanel />);

    const section = await openAiCard("AI 行程規劃");
    fireEvent.change(within(section).getByLabelText(/^AI 行程來源/), { target: { value: "openai" } });
    fireEvent.change(within(section).getByLabelText(/^OpenAI 模型/), { target: { value: "openai-model-b" } });
    fireEvent.click(within(section).getByRole("button", { name: "儲存設定" }));

    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(2));
    const body = savedBody(fetchMock);
    expect(body.config.ai_planner_mode).toBe("openai");
    expect(body.config.openai_model).toBe("openai-model-b");
    expect(body.config.anthropic_model).toBeUndefined();
    expect(body.config.minimax_model).toBeUndefined();
  });

  it("reveals a text input for a custom model id and sends the typed value", async () => {
    const fetchMock = stubAiFetch(aiSnapshot);
    render(<AdminSettingsPanel />);

    const section = await openAiCard("AI 行程規劃");
    fireEvent.change(within(section).getByLabelText(/^AI 行程來源/), { target: { value: "openai" } });
    fireEvent.change(within(section).getByLabelText(/^OpenAI 模型/), { target: { value: "__custom__" } });
    const custom = within(section).getByLabelText("自訂模型 ID：OpenAI 模型") as HTMLInputElement;
    expect(custom.value).toBe("");
    expect(custom.placeholder).toBe("輸入模型 ID");
    fireEvent.change(custom, { target: { value: "openai-model-preview" } });
    expect((within(section).getByLabelText(/^OpenAI 模型/) as HTMLSelectElement).value).toBe("__custom__");

    fireEvent.change(within(section).getByLabelText(/^OpenAI 模型/), { target: { value: "openai-model-a" } });
    expect(within(section).queryByLabelText("自訂模型 ID：OpenAI 模型")).toBeNull();

    fireEvent.change(within(section).getByLabelText(/^OpenAI 模型/), { target: { value: "__custom__" } });
    fireEvent.change(within(section).getByLabelText("自訂模型 ID：OpenAI 模型"), { target: { value: "openai-model-preview" } });
    fireEvent.click(within(section).getByRole("button", { name: "儲存設定" }));

    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(2));
    expect(savedBody(fetchMock).config.openai_model).toBe("openai-model-preview");
  });

  it("shows a stored model id outside the catalog as a custom entry instead of snapping to the first option", async () => {
    const legacyPlanner = { ...aiPlannerProvider, config: { ...aiPlannerProvider.config, ai_planner_mode: "openai", openai_model: "openai-model-legacy" } };
    const fetchMock = stubAiFetch({ ...aiSnapshot, providers: [aiVendorsProvider, legacyPlanner, aiGuideSearchProvider, geminiProvider] });
    render(<AdminSettingsPanel />);

    const section = await openAiCard("AI 行程規劃");
    expect((within(section).getByLabelText(/^OpenAI 模型/) as HTMLSelectElement).value).toBe("__custom__");
    expect((within(section).getByLabelText("自訂模型 ID：OpenAI 模型") as HTMLInputElement).value).toBe("openai-model-legacy");
    expect((within(section).getByRole("button", { name: "儲存設定" }) as HTMLButtonElement).disabled).toBe(true);
    expect(fetchMock).toHaveBeenCalledTimes(1);
  });

  it("lets guide search inherit or override the planner model per vendor", async () => {
    const fetchMock = stubAiFetch(aiSnapshot);
    render(<AdminSettingsPanel scope="hotspots" />);

    const section = (await screen.findByRole("heading", { name: "AI 景點介紹搜尋" })).closest("section")!;
    const minimax = within(section).getByLabelText(/^MiniMax 模型/) as HTMLSelectElement;
    expect(Array.from(minimax.options).map((option) => option.textContent)).toEqual(["沿用行程規劃的模型", "MiniMax Model A", "自訂…"]);
    expect(minimax.value).toBe("");
    expect(within(section).queryByLabelText(/^OpenAI 模型/)).toBeNull();

    fireEvent.change(within(section).getByLabelText(/^景點 AI 搜尋預設供應商/), { target: { value: "openai" } });
    expect(within(section).queryByLabelText(/^MiniMax 模型/)).toBeNull();
    fireEvent.change(within(section).getByLabelText(/^OpenAI 模型/), { target: { value: "openai-model-b" } });
    fireEvent.click(within(section).getByRole("button", { name: "儲存設定" }));

    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(2));
    const body = savedBody(fetchMock);
    expect(body.config.hotspot_guide_ai_default_provider).toBe("openai");
    expect(body.config.hotspot_guide_ai_openai_model).toBe("openai-model-b");
    expect(body.config.hotspot_guide_ai_minimax_model).toBeUndefined();
    expect(body.config.hotspot_guide_ai_anthropic_model).toBeUndefined();
  });

  it("lets the introduction writer inherit the guide search model or take its own", async () => {
    const fetchMock = stubAiFetch(aiSnapshot);
    render(<AdminSettingsPanel scope="hotspots" />);

    const section = (await screen.findByRole("heading", { name: "AI 景點介紹撰寫" })).closest("section")!;
    const minimax = within(section).getByLabelText(/^MiniMax 模型/) as HTMLSelectElement;
    // Blank means the guide search's model, not the planner's: introductions run through
    // the guide search adapters, and the empty option has to say which one it inherits.
    expect(Array.from(minimax.options).map((option) => option.textContent)).toEqual(["沿用景點 AI 搜尋的模型", "MiniMax Model A", "自訂…"]);
    expect(minimax.value).toBe("");
    expect(within(section).queryByLabelText(/^Gemini 模型/)).toBeNull();

    fireEvent.change(within(section).getByLabelText(/^介紹撰寫預設供應商/), { target: { value: "gemini" } });
    expect(within(section).queryByLabelText(/^MiniMax 模型/)).toBeNull();
    fireEvent.change(within(section).getByLabelText(/^Gemini 模型/), { target: { value: "gemini-model-a" } });
    fireEvent.click(within(section).getByRole("button", { name: "儲存設定" }));

    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(2));
    const body = savedBody(fetchMock);
    expect(body.config.hotspot_intro_ai_default_provider).toBe("gemini");
    expect(body.config.hotspot_intro_ai_gemini_model).toBe("gemini-model-a");
    expect(body.config.hotspot_intro_ai_minimax_model).toBeUndefined();
  });

  it("lets the planner pin Gemini and sends its model through the shared vendor key", async () => {
    const fetchMock = stubAiFetch(aiSnapshot);
    render(<AdminSettingsPanel />);

    const section = await openAiCard("AI 行程規劃");
    fireEvent.change(within(section).getByLabelText(/^AI 行程來源/), { target: { value: "gemini" } });
    expect(within(section).getAllByLabelText(/^(OpenAI|Claude|MiniMax|Gemini) 模型/)).toHaveLength(1);
    const gemini = within(section).getByLabelText(/^Gemini 模型/) as HTMLSelectElement;
    expect(Array.from(gemini.options).map((option) => option.textContent)).toEqual(["Gemini Model A", "自訂…"]);
    fireEvent.click(within(section).getByRole("button", { name: "儲存設定" }));

    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(2));
    const body = savedBody(fetchMock);
    expect(body.config.ai_planner_mode).toBe("gemini");
    expect(body.config.gemini_model).toBeUndefined();
  });

  it("lets guide search default to Gemini with its own optional model", async () => {
    const fetchMock = stubAiFetch(aiSnapshot);
    render(<AdminSettingsPanel scope="hotspots" />);

    const section = (await screen.findByRole("heading", { name: "AI 景點介紹搜尋" })).closest("section")!;
    fireEvent.change(within(section).getByLabelText(/^景點 AI 搜尋預設供應商/), { target: { value: "gemini" } });
    expect(within(section).queryByLabelText(/^MiniMax 模型/)).toBeNull();
    const gemini = within(section).getByLabelText(/^Gemini 模型/) as HTMLSelectElement;
    expect(Array.from(gemini.options).map((option) => option.textContent)).toEqual(["沿用行程規劃的模型", "Gemini Model A", "自訂…"]);
    expect(gemini.value).toBe("");
    fireEvent.click(within(section).getByRole("button", { name: "儲存設定" }));

    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(2));
    const body = savedBody(fetchMock);
    expect(body.config.hotspot_guide_ai_default_provider).toBe("gemini");
    expect(body.config.hotspot_guide_ai_gemini_model).toBeUndefined();
  });

  it("renders the Gemini model as a catalog dropdown with the option note", async () => {
    stubAiFetch(aiSnapshot);
    render(<AdminSettingsPanel />);

    const section = await openAiCard("Gemini 多語文章搜尋");
    const gemini = within(section).getByLabelText(/^Gemini 模型/) as HTMLSelectElement;
    expect(gemini.tagName).toBe("SELECT");
    expect(Array.from(gemini.options).map((option) => option.textContent)).toEqual(["Gemini Model A", "Gemini Model B", "自訂…"]);
    expect(within(section).getByText("目前預設")).toBeTruthy();
    expect(within(section).getByLabelText(/^單次搜尋逾時/)).toBeTruthy();
  });
});
