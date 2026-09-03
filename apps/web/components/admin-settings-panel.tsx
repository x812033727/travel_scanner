"use client";

import { Check, EyeOff, Gauge, KeyRound, LoaderCircle, PlugZap, RefreshCw, Save, ShieldCheck, Trash2 } from "lucide-react";
import { useTranslations } from "next-intl";
import { useEffect, useState } from "react";
import { useRouter } from "@/i18n/navigation";
import { api } from "@/lib/api";

type Scalar = string | number | boolean;
type SecretState = { configured: boolean; masked?: string | null; source: string };
type ProviderSkuUsage = {
  sku: string;
  label: string;
  category: string;
  operations: string[];
  used: number;
  free_limit: number;
  free_usage: number;
  free_remaining: number;
  billable_overage: number;
  percentage: number;
};
type ProviderMonthlyUsage = {
  period: string;
  period_start: string;
  period_end: string;
  used: number;
  free_limit: number;
  free_usage: number;
  free_remaining: number;
  billable_overage: number;
  breakdown: Record<string, number>;
  sku_usage: ProviderSkuUsage[];
  tracking_started_at?: string | null;
};
type ProviderUsage = {
  period: string;
  period_start: string;
  period_end: string;
  used?: number | null;
  monthly_limit: number;
  remaining?: number | null;
  percentage?: number | null;
  free_limit: number;
  free_usage?: number | null;
  free_remaining?: number | null;
  billable_overage?: number | null;
  breakdown: Record<string, number>;
  sku_usage: ProviderSkuUsage[];
  monthly_history: ProviderMonthlyUsage[];
  tracking_started_at?: string | null;
  observed_at: string;
  available: boolean;
  period_kind?: "month" | "day";
  scope: string;
  billing_timezone: string;
  pricing_region: string;
};
type ProviderView = {
  provider: string;
  label: string;
  description: string;
  enabled: boolean;
  configured: boolean;
  status: string;
  status_message: string;
  config: Record<string, Scalar | null>;
  config_sources: Record<string, string>;
  secrets: Record<string, SecretState>;
  last_tested_at?: string | null;
  last_test_status?: string | null;
  last_test_message?: string | null;
  updated_at?: string | null;
  usage?: ProviderUsage | null;
  requests_24h?: number;
  errors_24h?: number;
  last_error_at?: string | null;
};
type Audit = { id: string; action: string; target: string; metadata: Record<string, unknown>; created_at: string };
type Snapshot = { providers: ProviderView[]; audit: Audit[]; encryption_source: string };
type Draft = { enabled: boolean; config: Record<string, string>; secrets: Record<string, string>; clearSecrets: string[] };
type FieldMeta = { label: string; type?: "text" | "number" | "url" | "boolean"; options?: Array<{ value: string; label: string }>; help?: string };
type AdminSettingsScope = "providers" | "system" | "layout";

const fieldMeta: Record<string, FieldMeta> = {
  auth_google_client_id: { label: "Google OAuth Client ID", help: "Google Cloud OAuth 2.0 Web Client ID。" },
  auth_line_channel_id: { label: "LINE Login Channel ID", help: "需在 LINE Developers 申請 OpenID Connect Email 權限。" },
  auth_apple_services_id: { label: "Apple Services ID" },
  auth_apple_team_id: { label: "Apple Team ID" },
  auth_apple_key_id: { label: "Apple Key ID" },
  auth_oauth_flow_ttl_seconds: { label: "登入流程有效秒數", type: "number", help: "一次性 state、nonce 與 PKCE 預設保留 10 分鐘。" },
  auth_oauth_ip_limit: { label: "每 IP 每小時啟動上限", type: "number" },
  ga4_enabled: { label: "同步送出 GA4 cookieless 事件", type: "boolean", help: "只在 Consent Mode 全部 denied 下送出清洗後事件，不在站內保存 GA Cookie。" },
  ga4_measurement_id: { label: "GA4 Measurement ID", help: "格式為 G-...；這是公開識別碼，不是 Data API 金鑰。" },
  analytics_trust_country_header: { label: "信任代理伺服器國碼", type: "boolean", help: "只讀取 BFF 從設定好的可信代理標頭轉送的兩碼國碼；未設定時一律為未知。" },
  analytics_event_ip_limit: { label: "每 IP 每分鐘事件上限", type: "number" },
  analytics_event_session_limit: { label: "每工作階段每分鐘事件上限", type: "number" },
  analytics_retention_days: { label: "原始事件保存天數", type: "number", help: "預設 90 天；到期後由維護工作刪除。" },
  analytics_rollup_retention_months: { label: "每日彙總保存月數", type: "number", help: "預設 25 個月。" },
  registration_enabled: { label: "開放公開註冊", type: "boolean", help: "關閉後所有新帳號（包含環境管理員 Email）都無法自行註冊；既有會員仍可正常登入。" },
  hotspots_enabled: { label: "", type: "boolean" },
  trips_enabled: { label: "", type: "boolean" },
  alerts_enabled: { label: "", type: "boolean" },
  flight_status_enabled: { label: "", type: "boolean" },
  airline_fares_enabled: { label: "", type: "boolean" },
  pricing_enabled: { label: "", type: "boolean" },
  ai_planner_mode: { label: "AI 行程來源", options: [{ value: "auto", label: "自動備援" }, { value: "openai", label: "OpenAI／ChatGPT" }, { value: "anthropic", label: "Claude" }, { value: "minimax", label: "MiniMax" }, { value: "fallback", label: "只用內建備援" }, { value: "disabled", label: "停用真實 AI" }] },
  ai_planner_priority: { label: "自動備援順序", help: "用逗號分隔，例如 openai,anthropic,minimax。" },
  ai_planner_timeout_seconds: { label: "每家 AI 逾時（秒）", type: "number" },
  ai_planner_total_timeout_seconds: { label: "整體 AI 逾時（秒）", type: "number" },
  ai_planner_max_output_tokens: { label: "最大輸出 Tokens", type: "number" },
  hotspot_guide_ai_default_provider: { label: "景點 AI 搜尋預設供應商", options: [{ value: "minimax", label: "MiniMax" }, { value: "openai", label: "OpenAI" }, { value: "anthropic", label: "Claude" }] },
  hotspot_guide_ai_timeout_seconds: { label: "景點 AI 搜尋逾時（秒）", type: "number" },
  hotspot_guide_ai_max_output_tokens: { label: "景點 AI 最大輸出 Tokens", type: "number" },
  hotspot_guide_ai_daily_run_limit: { label: "每日 AI 搜尋執行上限", type: "number" },
  hotspot_guide_ai_daily_call_budget: { label: "每日 AI 模型呼叫上限", type: "number", help: "管理員搜尋不扣會員次數，但會記錄於後台配額與稽核紀錄。" },
  openai_api_base_url: { label: "OpenAI API Base URL", type: "url" },
  openai_model: { label: "OpenAI 模型" },
  anthropic_api_base_url: { label: "Claude API Base URL", type: "url" },
  anthropic_model: { label: "Claude 模型" },
  minimax_api_base_url: { label: "MiniMax API Base URL", type: "url" },
  minimax_model: { label: "MiniMax 模型" },
  travel_provider_mode: { label: "旅遊資料供應商", options: [{ value: "amadeus", label: "Amadeus" }, { value: "mock", label: "Mock（僅開發）" }, { value: "disabled", label: "停用" }] },
  flight_provider_mode: { label: "航空查詢來源", options: [{ value: "auto", label: "自動：Skyscanner → Duffel → Amadeus" }, { value: "skyscanner", label: "Skyscanner" }, { value: "duffel", label: "Duffel" }, { value: "amadeus", label: "Amadeus" }, { value: "mock", label: "Mock（僅開發）" }, { value: "disabled", label: "停用" }], help: "混合模式會依序補查，直到行程組數達到門檻；追加來源不另扣搜尋次數。" },
  flight_search_strategy: { label: "航空搜尋策略", options: [{ value: "hybrid", label: "混合節流" }, { value: "single", label: "只查首選來源" }] },
  flight_min_result_count: { label: "自動補查門檻", type: "number", help: "去重後少於此行程組數時查詢下一家。" },
  hotel_provider_mode: { label: "飯店查詢來源", options: [{ value: "auto", label: "自動：Booking.com → Amadeus" }, { value: "booking", label: "Booking.com Demand API" }, { value: "amadeus", label: "Amadeus" }, { value: "mock", label: "Mock（僅開發）" }, { value: "disabled", label: "停用" }], help: "自動模式會在 Booking.com Demand API 尚未核准時先使用 Amadeus。" },
  provider_timeout_seconds: { label: "供應商逾時（秒）", type: "number", help: "單次外部請求等待上限。" },
  provider_failure_threshold: { label: "斷路器失敗門檻", type: "number" },
  provider_circuit_seconds: { label: "斷路器暫停秒數", type: "number" },
  route_cache_ttl_seconds: { label: "路線快取秒數", type: "number" },
  naver_place_cache_ttl_seconds: { label: "NAVER 地點快取秒數", type: "number", help: "地點詳情以不透明 ID 暫存在 Redis；預設 15 分鐘。" },
  naver_maps_monthly_request_limit: { label: "站內每月提醒額度", type: "number", help: "選填的內部提醒門檻，不代表 NAVER 免費額度或帳單上限；0 表示不設定。" },
  weather_cache_ttl_seconds: { label: "天氣快取秒數", type: "number", help: "Google Weather 預設快取 15 分鐘，降低重複查詢。" },
  google_maps_essentials_free_limit: { label: "Essentials 每 SKU 免費額度", type: "number", help: "全球公開定價預設每個 SKU 每月 10,000 次；若合約不同可在此調整。" },
  google_maps_pro_free_limit: { label: "Pro 每 SKU 免費額度", type: "number", help: "全球公開定價預設每個 SKU 每月 5,000 次。" },
  google_maps_enterprise_free_limit: { label: "Enterprise 每 SKU 免費額度", type: "number", help: "全球公開定價預設每個 SKU 每月 1,000 次。" },
  restaurant_scan_enabled: { label: "啟用景點周邊餐廳掃描", type: "boolean", help: "關閉後不再發送 Nearby、Aggregate 或餐廳 Details 請求。" },
  restaurant_aggregate_monthly_budget: { label: "餐廳 Aggregate 每月安全上限", type: "number", help: "預設 4,000 次，保留 Places Aggregate 公開免費額度的 20%。" },
  restaurant_nearby_monthly_budget: { label: "餐廳 Nearby 每月安全上限", type: "number", help: "預設 800 次，用於前台即時熱門餐廳。" },
  restaurant_details_monthly_budget: { label: "餐廳 Details 每月安全上限", type: "number", help: "預設 800 次；與其他 Place Details 共用計算，接近免費額度前就停止。" },
  restaurant_scan_refresh_days: { label: "餐廳覆蓋重掃週期（天）", type: "number" },
  restaurant_scan_max_depth: { label: "餐廳網格最大細分層數", type: "number" },
  restaurant_scan_batch_call_limit: { label: "每批餐廳掃描呼叫上限", type: "number", help: "預設每六小時最多 50 次，保留進度後輪替景點續掃。" },
  restaurant_location_cache_days: { label: "餐廳經緯度 Redis TTL（天）", type: "number", help: "只暫存經緯度，預設與上限皆為 30 天；Redis 到期後自動失效。" },
  hotspot_guide_youtube_daily_search_budget: { label: "每日自動搜尋上限", type: "number", help: "預設 80 次，自每日 Search Queries 額度中保留 20 次供管理員操作。" },
  hotspot_guide_youtube_search_daily_free_limit: { label: "Search Queries 每日額度", type: "number", help: "YouTube 預設每日 100 次 search.list 查詢；若 Cloud 專案核准額度不同可在此調整。" },
  hotspot_guide_youtube_core_daily_free_limit: { label: "Core API 每日額度", type: "number", help: "YouTube 預設每日 10,000 單位；目前 videos.list 每次請求計 1 單位。" },
  hotspot_guide_refresh_days: { label: "Metadata 更新週期（天）", type: "number" },
  amadeus_env: { label: "Amadeus 環境", options: [{ value: "test", label: "Test" }, { value: "production", label: "Production" }] },
  skyscanner_base_url: { label: "API Base URL", type: "url" },
  skyscanner_market: { label: "市場代碼" },
  skyscanner_locale: { label: "語系" },
  skyscanner_currency: { label: "顯示幣別" },
  skyscanner_poll_attempts: { label: "輪詢次數", type: "number" },
  skyscanner_poll_interval_seconds: { label: "輪詢間隔（秒）", type: "number" },
  duffel_env: { label: "Duffel 環境", options: [{ value: "test", label: "Test" }, { value: "live", label: "Live" }] },
  duffel_base_url: { label: "Duffel API Base URL", type: "url" },
  duffel_supplier_timeout_ms: { label: "供應商等待上限（毫秒）", type: "number" },
  flightaware_base_url: { label: "AeroAPI Base URL", type: "url" },
  flightaware_enrich_offer_limit: { label: "自動補充最便宜行程組", type: "number" },
  flightaware_cache_ttl_seconds: { label: "航班動態快取秒數", type: "number" },
  flightaware_track_cache_ttl_seconds: { label: "航跡快取秒數", type: "number" },
  google_travel_impact_base_url: { label: "Travel Impact API Base URL", type: "url" },
  travel_impact_cache_ttl_seconds: { label: "碳排快取秒數", type: "number" },
  navitime_api_base_url: { label: "API Base URL", type: "url" },
  travelpayouts_api_base_url: { label: "Partner Links API Base URL", type: "url" },
  travelpayouts_marker: { label: "Marker" },
  travelpayouts_project_id: { label: "Project ID" },
  travelpayouts_static_url_template: { label: "安全備援合作連結", type: "url", help: "Partner Links API 失敗時才使用；可包含 {destination}、{departure_date}、{return_date}、{sub_id}。" },
  travelpayouts_flight_target_url: { label: "航班原始目標網址", type: "url" },
  travelpayouts_hotel_target_url: { label: "住宿原始目標網址", type: "url" },
  travelpayouts_activities_target_url: { label: "活動原始目標網址", type: "url" },
  travelpayouts_transport_target_url: { label: "交通原始目標網址", type: "url" },
  travelpayouts_allowed_hosts: { label: "允許跳轉網域", help: "以逗號分隔；只允許 HTTPS 且符合清單的網址。" },
  kkday_cid: { label: "KKpartners CID" },
  kkday_affiliate_url_template: { label: "合作連結範本", type: "url" },
  kkday_allowed_hosts: { label: "允許跳轉網域" },
  kkday_api_base_url: { label: "核准後 API Base URL", type: "url" },
  klook_affiliate_url_template: { label: "合作連結範本", type: "url" },
  klook_allowed_hosts: { label: "允許跳轉網域" },
  klook_api_base_url: { label: "核准後 API Base URL", type: "url" },
  airalo_affiliate_url_template: { label: "Impact／Affiliate 合作連結", type: "url" },
  airalo_allowed_hosts: { label: "允許跳轉網域" },
  trip_com_affiliate_url_template: { label: "後台產生的完整合作連結", type: "url", help: "系統不會覆寫既有 Trip.com 追蹤參數。" },
  trip_com_allowed_hosts: { label: "允許跳轉網域" },
  agoda_cid: { label: "Agoda CID" },
  agoda_affiliate_url_template: { label: "合作連結範本", type: "url" },
  agoda_allowed_hosts: { label: "允許跳轉網域" },
  agoda_api_base_url: { label: "核准後 API Base URL", type: "url" },
  booking_affiliate_id: { label: "Booking.com Affiliate ID" },
  booking_affiliate_url_template: { label: "合作連結範本", type: "url" },
  booking_allowed_hosts: { label: "允許跳轉網域" },
  booking_demand_env: { label: "Demand API 環境", options: [{ value: "sandbox", label: "Sandbox" }, { value: "production", label: "Production" }], help: "切換 production 後請儲存並重新執行連線測試。" },
  booking_demand_api_base_url: { label: "Demand API v3.1 Base URL", type: "url", help: "僅允許 Booking.com 官方 sandbox 或 production 網域。" },
  booking_demand_affiliate_id: { label: "Demand API Affiliate ID", help: "與分潤導流 ID 分開保存；留空時才沿用 Affiliate 區塊的 ID。" },
  booking_booker_country: { label: "Booker 國家代碼", help: "兩碼小寫國家代碼；台灣使用 tw。" },
  booking_language: { label: "Booking 回傳語系", help: "例如 zh-tw 或 en-gb。" },
  booking_location_cache_ttl_seconds: { label: "目的地 ID 快取秒數", type: "number" },
  skyscanner_affiliate_url_template: { label: "Impact Affiliate 合作連結", type: "url" },
  skyscanner_affiliate_allowed_hosts: { label: "允許跳轉網域" },
};

const secretLabels: Record<string, { label: string; help?: string }> = {
  auth_google_client_secret: { label: "Google OAuth Client Secret", help: "只在伺服器端加密保存。" },
  auth_line_channel_secret: { label: "LINE Channel Secret", help: "只用於 LINE Login token exchange。" },
  auth_apple_private_key: { label: "Apple .p8 Private Key", help: "可貼上 PEM 或將換行寫成 \\n；只在伺服器端加密保存。" },
  openai_api_key: { label: "OpenAI API Key", help: "只在伺服器端加密保存，不會傳到瀏覽器。" },
  anthropic_api_key: { label: "Anthropic API Key", help: "用於 Claude Messages API。" },
  minimax_api_key: { label: "MiniMax API Key", help: "用於 MiniMax Responses API。" },
  google_maps_api_key: { label: "伺服器 API Key", help: "啟用 Places API (New)、Routes API 與 Weather API；建議限制主機出口 IP。" },
  next_public_google_maps_browser_key: { label: "瀏覽器地圖 Key", help: "用於 Maps JavaScript 路線地圖；請啟用 Maps JavaScript API，並放行 https://mokaair.com/* 與 https://www.mokaair.com/* 兩個 HTTP referrer。" },
  naver_maps_client_id: { label: "NAVER Cloud Client ID", help: "伺服器 API 與瀏覽器 Dynamic Map 使用；瀏覽器公開值必須限制正式網站來源。" },
  naver_maps_client_secret: { label: "NAVER Cloud Client Secret", help: "只在伺服器端加密保存，絕不回傳瀏覽器。" },
  amadeus_client_id: { label: "Client ID" },
  amadeus_client_secret: { label: "Client Secret" },
  skyscanner_api_key: { label: "API Key" },
  duffel_access_token: { label: "Access Token" },
  flightaware_api_key: { label: "AeroAPI Key" },
  google_travel_impact_api_key: { label: "Travel Impact API Key" },
  navitime_client_id: { label: "Client ID" },
  navitime_api_key: { label: "API Key" },
  travelpayouts_api_token: { label: "API Token" },
  kkday_api_key: { label: "核准後 API Key" },
  klook_api_key: { label: "核准後 API Key" },
  agoda_api_key: { label: "核准後 API Key" },
  booking_demand_api_token: { label: "Demand API Bearer Token" },
};

const sourceLabel: Record<string, string> = { database: "後台加密設定", environment: "主機環境", none: "未設定", disabled: "已停用" };
const auditActionLabel: Record<string, string> = {
  system_settings_updated: "更新系統設定",
  provider_settings_updated: "更新供應商設定",
  provider_connection_tested: "執行連線測試",
  "admin_role.updated": "更新管理員權限",
};
const dateTime = new Intl.DateTimeFormat("zh-TW", { dateStyle: "medium", timeStyle: "short" });
const dateOnly = new Intl.DateTimeFormat("zh-TW", { dateStyle: "medium", timeZone: "UTC" });
const usageOperationLabel: Record<string, string> = {
  places_autocomplete: "地點自動完成",
  place_details: "地點詳細資料",
  places_text_search: "地點文字搜尋",
  places_photo: "地點照片",
  routes: "路線計算",
  weather_current: "目前天氣",
  weather_daily_forecast: "10 日預報",
  local_search: "Local Search",
  geocode: "Geocoding",
  directions: "Directions 5",
  search_list: "影片搜尋（search.list）",
  videos_list: "影片詳細資料（videos.list）",
};
const usageCategoryLabel: Record<string, string> = {
  essentials: "Essentials",
  pro: "Pro",
  enterprise: "Enterprise",
};
const numberFormat = new Intl.NumberFormat("zh-TW");

function auditSummary(metadata: Record<string, unknown>): string {
  for (const field of ["registration_enabled", "status", "enabled", "is_admin"]) {
    if (field in metadata) return String(metadata[field]);
  }
  if (Array.isArray(metadata.config_fields)) return metadata.config_fields.join(", ");
  return "";
}

function makeDrafts(snapshot: Snapshot): Record<string, Draft> {
  return Object.fromEntries(snapshot.providers.map((provider) => [provider.provider, {
    enabled: provider.enabled,
    config: Object.fromEntries(Object.entries(provider.config).map(([key, value]) => [key, value == null ? "" : String(value)])),
    secrets: Object.fromEntries(Object.keys(provider.secrets).map((key) => [key, ""])),
    clearSecrets: [],
  }]));
}

function valueForApi(key: string, value: string): Scalar {
  if (fieldMeta[key]?.type === "number") return Number(value);
  if (fieldMeta[key]?.type === "boolean") return value === "true";
  return value;
}

function statusClass(status: string) {
  if (status === "ready" || status === "success") return "bg-emerald-50 text-emerald-800";
  if (status === "disabled") return "bg-slate-100 text-slate-700";
  return "bg-amber-50 text-amber-800";
}

function GoogleUsagePanel({ usage, refreshing, onRefresh }: {
  usage: ProviderUsage;
  refreshing: boolean;
  onRefresh: () => void;
}) {
  return <div className="mt-6 rounded-2xl border border-[var(--line)] bg-[var(--paper)] p-5" aria-label="Google Maps 本月用量">
    <div className="flex flex-wrap items-start justify-between gap-4">
      <div>
        <p className="flex items-center gap-2 text-sm font-bold text-[var(--teal)]"><Gauge size={17} />Google API 每月用量</p>
        {usage.available
          ? <p className="mt-2 text-3xl font-bold tabular-nums">{numberFormat.format(usage.used || 0)} <span className="text-base font-medium text-[var(--muted)]">次站內觀測請求</span></p>
          : <p className="mt-2 font-semibold text-amber-800">目前無法讀取用量計數</p>}
      </div>
      <button type="button" onClick={onRefresh} disabled={refreshing} className="flex items-center gap-2 rounded-xl border border-[var(--line)] bg-white px-3 py-2 text-sm font-semibold disabled:opacity-50"><RefreshCw size={15} className={refreshing ? "animate-spin" : ""} />重新整理用量</button>
    </div>

    {usage.available && <>
      <dl className="mt-4 grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
        <div className="rounded-xl bg-white p-3"><dt className="text-xs text-[var(--muted)]">本月站內請求</dt><dd className="mt-1 text-xl font-bold tabular-nums">{numberFormat.format(usage.used || 0)}</dd></div>
        <div className="rounded-xl bg-white p-3"><dt className="text-xs text-[var(--muted)]">免費額度內使用</dt><dd className="mt-1 text-xl font-bold tabular-nums">{numberFormat.format(usage.free_usage || 0)}</dd></div>
        <div className="rounded-xl bg-white p-3"><dt className="text-xs text-[var(--muted)]">各 SKU 剩餘合計</dt><dd className="mt-1 text-xl font-bold tabular-nums">{numberFormat.format(usage.free_remaining || 0)}</dd></div>
        <div className={`rounded-xl p-3 ${usage.billable_overage ? "bg-red-50 text-red-800" : "bg-emerald-50 text-emerald-800"}`}><dt className="text-xs">可能超出免費額度</dt><dd className="mt-1 text-xl font-bold tabular-nums">{numberFormat.format(usage.billable_overage || 0)}</dd></div>
      </dl>

      <div className="mt-5">
        <h3 className="text-sm font-bold">本月各 SKU 免費額度</h3>
        <p className="mt-1 text-xs leading-5 text-[var(--muted)]">免費額度由各 SKU 獨立計算，不能用其他 SKU 的剩餘量抵銷超額。</p>
        <div className="mt-3 grid gap-3 md:grid-cols-2 xl:grid-cols-3">
          {usage.sku_usage.map((item) => {
            const width = Math.min(100, Math.max(0, item.percentage));
            return <article key={item.sku} className="rounded-xl bg-white p-4">
              <div className="flex items-start justify-between gap-3"><div><h4 className="text-sm font-bold">{item.label}</h4><p className="mt-0.5 text-[.68rem] text-[var(--muted)]">{usageCategoryLabel[item.category] || item.category}</p></div><span className="text-sm font-bold tabular-nums">{numberFormat.format(item.used)} / {numberFormat.format(item.free_limit)}</span></div>
              <div className="mt-3 h-2 overflow-hidden rounded-full bg-[var(--paper)]" role="progressbar" aria-label={`${item.label} 月用量`} aria-valuemin={0} aria-valuemax={item.free_limit} aria-valuenow={Math.min(item.used, item.free_limit)}><div className={`h-full rounded-full ${item.billable_overage ? "bg-red-500" : item.percentage >= 75 ? "bg-amber-500" : "bg-[var(--teal)]"}`} style={{ width: `${width}%` }} /></div>
              <p className={`mt-2 text-xs ${item.billable_overage ? "font-semibold text-red-700" : "text-[var(--muted)]"}`}>{item.billable_overage ? `可能超額 ${numberFormat.format(item.billable_overage)} 次` : `剩餘免費 ${numberFormat.format(item.free_remaining)} 次`}</p>
            </article>;
          })}
        </div>
      </div>

      <div className="mt-5">
        <h3 className="text-sm font-bold">最近 6 個帳務月份</h3>
        <div className="mt-3 overflow-x-auto rounded-xl border border-[var(--line)] bg-white">
          <table className="min-w-[42rem] w-full text-left text-sm">
            <thead className="bg-[var(--paper)] text-xs text-[var(--muted)]"><tr><th className="px-3 py-2 font-semibold">月份</th><th className="px-3 py-2 font-semibold">站內請求</th><th className="px-3 py-2 font-semibold">免費額度內使用</th><th className="px-3 py-2 font-semibold">各 SKU 剩餘合計</th><th className="px-3 py-2 font-semibold">可能超額</th></tr></thead>
            <tbody className="divide-y divide-[var(--line)]">{usage.monthly_history.map((month) => <tr key={month.period}><th className="px-3 py-2.5 font-semibold">{month.period}</th><td className="px-3 py-2.5 tabular-nums">{numberFormat.format(month.used)}</td><td className="px-3 py-2.5 tabular-nums">{numberFormat.format(month.free_usage)}</td><td className="px-3 py-2.5 tabular-nums">{numberFormat.format(month.free_remaining)}</td><td className={`px-3 py-2.5 tabular-nums ${month.billable_overage ? "font-semibold text-red-700" : ""}`}>{numberFormat.format(month.billable_overage)}</td></tr>)}</tbody>
          </table>
        </div>
      </div>

      <details className="mt-4 rounded-xl bg-white px-4 py-3"><summary className="cursor-pointer text-sm font-semibold">查看站內操作明細</summary><dl className="mt-3 grid gap-2 sm:grid-cols-2 lg:grid-cols-4">{Object.entries(usage.breakdown).map(([operation, count]) => <div key={operation}><dt className="text-[.68rem] text-[var(--muted)]">{usageOperationLabel[operation] || operation}</dt><dd className="mt-0.5 font-bold tabular-nums">{numberFormat.format(count)}</dd></div>)}</dl></details>
    </>}
    <p className="mt-4 text-xs leading-5 text-[var(--muted)]">帳務期間依 Google Pacific Time：{dateOnly.format(new Date(`${usage.period_start}T00:00:00Z`))} 至 {dateOnly.format(new Date(`${usage.period_end}T00:00:00Z`))}。本站會保守計入送出的伺服器請求（包含失敗請求），不含瀏覽器 Embed 與計數啟用前的歷史；實際成功計費事件、優惠與帳單仍以 Google Cloud Console 為準。</p>
  </div>;
}

function NaverUsagePanel({ usage, refreshing, onRefresh }: {
  usage: ProviderUsage;
  refreshing: boolean;
  onRefresh: () => void;
}) {
  const hasLimit = usage.monthly_limit > 0;
  const width = hasLimit ? Math.min(100, Math.max(0, usage.percentage || 0)) : 0;
  return <div className="mt-6 rounded-2xl border border-[#b8e7ca] bg-[#f2fbf5] p-5" aria-label="NAVER Maps 本月用量">
    <div className="flex flex-wrap items-start justify-between gap-4">
      <div><p className="flex items-center gap-2 text-sm font-bold text-[#087a3f]"><Gauge size={17} />NAVER Maps 本月伺服器用量</p>{usage.available ? <p className="mt-2 text-3xl font-bold tabular-nums">{numberFormat.format(usage.used || 0)} <span className="text-base font-medium text-[var(--muted)]">次站內請求</span></p> : <p className="mt-2 font-semibold text-amber-800">目前無法讀取用量計數</p>}</div>
      <button type="button" onClick={onRefresh} disabled={refreshing} className="flex items-center gap-2 rounded-xl border border-[#b8e7ca] bg-white px-3 py-2 text-sm font-semibold disabled:opacity-50"><RefreshCw size={15} className={refreshing ? "animate-spin" : ""} />重新整理用量</button>
    </div>
    {usage.available && <>
      <dl className="mt-4 grid gap-3 sm:grid-cols-3">
        <div className="rounded-xl bg-white p-3"><dt className="text-xs text-[var(--muted)]">本月站內請求</dt><dd className="mt-1 text-xl font-bold tabular-nums">{numberFormat.format(usage.used || 0)}</dd></div>
        <div className="rounded-xl bg-white p-3"><dt className="text-xs text-[var(--muted)]">內部提醒門檻</dt><dd className="mt-1 text-xl font-bold tabular-nums">{hasLimit ? numberFormat.format(usage.monthly_limit) : "未設定"}</dd></div>
        <div className="rounded-xl bg-white p-3"><dt className="text-xs text-[var(--muted)]">門檻內剩餘</dt><dd className="mt-1 text-xl font-bold tabular-nums">{hasLimit ? numberFormat.format(usage.remaining || 0) : "—"}</dd></div>
      </dl>
      {hasLimit && <div className="mt-4 h-2 overflow-hidden rounded-full bg-white" role="progressbar" aria-label="NAVER Maps 月用量" aria-valuemin={0} aria-valuemax={usage.monthly_limit} aria-valuenow={Math.min(usage.used || 0, usage.monthly_limit)}><div className={`h-full rounded-full ${(usage.percentage || 0) >= 100 ? "bg-red-500" : (usage.percentage || 0) >= 75 ? "bg-amber-500" : "bg-[#03c75a]"}`} style={{ width: `${width}%` }} /></div>}
      <details className="mt-4 rounded-xl bg-white px-4 py-3"><summary className="cursor-pointer text-sm font-semibold">查看站內操作明細</summary><dl className="mt-3 grid gap-2 sm:grid-cols-3">{Object.entries(usage.breakdown).map(([operation, count]) => <div key={operation}><dt className="text-[.68rem] text-[var(--muted)]">{usageOperationLabel[operation] || operation}</dt><dd className="mt-0.5 font-bold tabular-nums">{numberFormat.format(count)}</dd></div>)}</dl></details>
      <div className="mt-4 overflow-x-auto rounded-xl border border-[#d7eee0] bg-white"><table className="min-w-[32rem] w-full text-left text-sm"><thead className="bg-[#f2fbf5] text-xs text-[var(--muted)]"><tr><th className="px-3 py-2 font-semibold">月份</th><th className="px-3 py-2 font-semibold">站內請求</th><th className="px-3 py-2 font-semibold">內部門檻</th><th className="px-3 py-2 font-semibold">剩餘</th></tr></thead><tbody className="divide-y divide-[var(--line)]">{usage.monthly_history.map((month) => <tr key={month.period}><th className="px-3 py-2.5 font-semibold">{month.period}</th><td className="px-3 py-2.5 tabular-nums">{numberFormat.format(month.used)}</td><td className="px-3 py-2.5 tabular-nums">{hasLimit ? numberFormat.format(month.free_limit) : "—"}</td><td className="px-3 py-2.5 tabular-nums">{hasLimit ? numberFormat.format(month.free_remaining) : "—"}</td></tr>)}</tbody></table></div>
    </>}
    <p className="mt-4 text-xs leading-5 text-[var(--muted)]">帳務月份以韓國時間統計。本站只記錄 Local Search、Geocoding 與 Directions 5 的伺服器請求，不含瀏覽器 Dynamic Map 載入，也不等同 NAVER 帳務；實際用量與費用請以 NAVER Cloud Console 為準。</p>
  </div>;
}

function YouTubeUsagePanel({ usage, automaticSearchBudget, refreshing, onRefresh }: {
  usage: ProviderUsage;
  automaticSearchBudget: number;
  refreshing: boolean;
  onRefresh: () => void;
}) {
  const search = usage.sku_usage.find((item) => item.sku === "search_queries");
  const core = usage.sku_usage.find((item) => item.sku === "core_api_units");
  const manualReserve = search ? Math.max(0, search.free_limit - automaticSearchBudget) : 0;
  const automaticBudgetExceedsAllowance = Boolean(search && automaticSearchBudget > search.free_limit);

  return <div className="mt-6 rounded-2xl border border-[var(--line)] bg-[var(--paper)] p-5" aria-label="YouTube Data API 今日用量">
    <div className="flex flex-wrap items-start justify-between gap-4">
      <div>
        <p className="flex items-center gap-2 text-sm font-bold text-[var(--teal)]"><Gauge size={17} />YouTube Data API 每日用量</p>
        {usage.available
          ? <p className="mt-2 text-3xl font-bold tabular-nums">{numberFormat.format(usage.used || 0)} <span className="text-base font-medium text-[var(--muted)]">次站內觀測請求</span></p>
          : <p className="mt-2 font-semibold text-amber-800">目前無法讀取用量計數</p>}
      </div>
      <button type="button" onClick={onRefresh} disabled={refreshing} className="flex items-center gap-2 rounded-xl border border-[var(--line)] bg-white px-3 py-2 text-sm font-semibold disabled:opacity-50"><RefreshCw size={15} className={refreshing ? "animate-spin" : ""} />重新整理用量</button>
    </div>

    {usage.available && <>
      <dl className="mt-4 grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
        <div className="rounded-xl bg-white p-3"><dt className="text-xs text-[var(--muted)]">今日搜尋使用量</dt><dd className="mt-1 text-xl font-bold tabular-nums">{numberFormat.format(search?.used || 0)}</dd></div>
        <div className="rounded-xl bg-white p-3"><dt className="text-xs text-[var(--muted)]">搜尋額度剩餘</dt><dd className="mt-1 text-xl font-bold tabular-nums">{numberFormat.format(search?.free_remaining || 0)}</dd></div>
        <div className="rounded-xl bg-white p-3"><dt className="text-xs text-[var(--muted)]">今日 Core API 使用量</dt><dd className="mt-1 text-xl font-bold tabular-nums">{numberFormat.format(core?.used || 0)}</dd></div>
        <div className="rounded-xl bg-white p-3"><dt className="text-xs text-[var(--muted)]">Core API 額度剩餘</dt><dd className="mt-1 text-xl font-bold tabular-nums">{numberFormat.format(core?.free_remaining || 0)}</dd></div>
      </dl>

      <div className="mt-5">
        <h3 className="text-sm font-bold">今日各額度池</h3>
        <p className="mt-1 text-xs leading-5 text-[var(--muted)]">Search Queries 與 Core API 額度分開計算，不能互相抵用。</p>
        <div className="mt-3 grid gap-3 md:grid-cols-2">
          {usage.sku_usage.map((item) => {
            const width = Math.min(100, Math.max(0, item.percentage));
            return <article key={item.sku} className="rounded-xl bg-white p-4">
              <div className="flex items-start justify-between gap-3"><div><h4 className="text-sm font-bold">{item.label}</h4><p className="mt-0.5 text-[.68rem] text-[var(--muted)]">Google 預設每日額度</p></div><span className="text-sm font-bold tabular-nums">{numberFormat.format(item.used)} / {numberFormat.format(item.free_limit)}</span></div>
              <div className="mt-3 h-2 overflow-hidden rounded-full bg-[var(--paper)]" role="progressbar" aria-label={`${item.label} 日用量`} aria-valuemin={0} aria-valuemax={item.free_limit} aria-valuenow={Math.min(item.used, item.free_limit)}><div className={`h-full rounded-full ${item.billable_overage ? "bg-red-500" : item.percentage >= 75 ? "bg-amber-500" : "bg-[var(--teal)]"}`} style={{ width: `${width}%` }} /></div>
              <p className={`mt-2 text-xs ${item.billable_overage ? "font-semibold text-red-700" : "text-[var(--muted)]"}`}>{item.billable_overage ? `高於設定額度 ${numberFormat.format(item.billable_overage)}` : `剩餘 ${numberFormat.format(item.free_remaining)}`}</p>
            </article>;
          })}
        </div>
      </div>

      <div className="mt-4 rounded-xl border border-teal-100 bg-teal-50 px-4 py-3 text-sm leading-6 text-teal-950">
        <p className="font-bold">自動探索預算</p>
        <p>{automaticBudgetExceedsAllowance
          ? `每日自動搜尋上限 ${numberFormat.format(automaticSearchBudget)} 次，高於目前 Search Queries 額度 ${numberFormat.format(search?.free_limit || 0)}；請調低自動搜尋上限。`
          : `每日最多 ${numberFormat.format(automaticSearchBudget)} 次搜尋；依目前設定保留 ${numberFormat.format(manualReserve)} 次給管理員搜尋與連線測試。`}</p>
      </div>

      <details className="mt-4 rounded-xl bg-white px-4 py-3"><summary className="cursor-pointer text-sm font-semibold">查看站內操作明細</summary><dl className="mt-3 grid gap-2 sm:grid-cols-2">{Object.entries(usage.breakdown).map(([operation, count]) => <div key={operation}><dt className="text-[.68rem] text-[var(--muted)]">{usageOperationLabel[operation] || operation}</dt><dd className="mt-0.5 font-bold tabular-nums">{numberFormat.format(count)}</dd></div>)}</dl></details>
    </>}
    <p className="mt-4 text-xs leading-5 text-[var(--muted)]">每日額度依 Google Pacific Time 重設，目前帳務日為 {dateOnly.format(new Date(`${usage.period_start}T00:00:00Z`))}。本站會保守計入送出的伺服器 search.list 與 videos.list 請求（包含失敗請求），不含計數啟用前、其他服務或其他 Cloud 專案的流量；實際配額與調整結果仍以 Google Cloud Console 為準。</p>
  </div>;
}

export function AdminSettingsPanel({ scope = "providers" }: { scope?: AdminSettingsScope }) {
  const t = useTranslations("admin");
  const router = useRouter();
  const [snapshot, setSnapshot] = useState<Snapshot>();
  const [drafts, setDrafts] = useState<Record<string, Draft>>({});
  const [loadError, setLoadError] = useState<string>();
  const [busyProvider, setBusyProvider] = useState<string>();
  const [notice, setNotice] = useState<string>();
  const [actionError, setActionError] = useState<string>();
  const [usageRefreshing, setUsageRefreshing] = useState(false);
  const [activePanel, setActivePanel] = useState<string>();

  useEffect(() => {
    let active = true;
    api<Snapshot>("/admin/provider-settings")
      .then((result) => {
        if (!active) return;
        setSnapshot(result);
        setDrafts(makeDrafts(result));
        setActivePanel((current) => current || result.providers.find((provider) => provider.provider !== "runtime" && provider.provider !== "layout")?.provider);
      })
      .catch((reason: Error) => { if (active) setLoadError(reason.message); });
    return () => { active = false; };
  }, []);

  function patchDraft(provider: string, patch: Partial<Draft>) {
    setDrafts((current) => ({ ...current, [provider]: { ...current[provider], ...patch } }));
  }

  function patchConfig(provider: string, field: string, value: string) {
    const draft = drafts[provider];
    patchDraft(provider, { config: { ...draft.config, [field]: value } });
  }

  function patchSecret(provider: string, field: string, value: string) {
    const draft = drafts[provider];
    patchDraft(provider, {
      secrets: { ...draft.secrets, [field]: value },
      clearSecrets: draft.clearSecrets.filter((item) => item !== field),
    });
  }

  function clearSecret(provider: string, field: string) {
    const draft = drafts[provider];
    patchDraft(provider, {
      secrets: { ...draft.secrets, [field]: "" },
      clearSecrets: [...new Set([...draft.clearSecrets, field])],
    });
  }

  async function refreshUsage() {
    setUsageRefreshing(true); setActionError(undefined);
    try {
      setSnapshot(await api<Snapshot>("/admin/provider-settings"));
    } catch (reason) { setActionError((reason as Error).message); }
    finally { setUsageRefreshing(false); }
  }

  async function save(provider: ProviderView) {
    const draft = drafts[provider.provider];
    setBusyProvider(provider.provider); setActionError(undefined); setNotice(undefined);
    const secrets: Record<string, string | null> = {};
    for (const [key, value] of Object.entries(draft.secrets)) if (value.trim()) secrets[key] = value.trim();
    for (const key of draft.clearSecrets) secrets[key] = null;
    try {
      const config = Object.fromEntries(Object.entries(draft.config).map(([key, value]) => [key, value.trim() === "" ? null : valueForApi(key, value)]));
      const isInternalSettings = provider.provider === "runtime" || provider.provider === "layout";
      const submittedConfig = isInternalSettings
        ? Object.fromEntries(Object.entries(config).filter(([key, value]) => value !== provider.config[key]))
        : config;
      const result = await api<Snapshot>(`/admin/provider-settings/${provider.provider}`, {
        method: "PUT",
        body: JSON.stringify({
          enabled: isInternalSettings ? true : draft.enabled,
          config: submittedConfig,
          secrets,
        }),
      });
      setSnapshot(result); setDrafts(makeDrafts(result));
      setNotice(provider.provider === "runtime" ? "系統設定已儲存並立即套用。" : provider.provider === "layout" ? t("layout.saveSuccess") : `${provider.label} 設定已加密儲存並立即套用。`);
      if (provider.provider === "layout") router.refresh();
    } catch (reason) { setActionError((reason as Error).message); }
    finally { setBusyProvider(undefined); }
  }

  async function testConnection(provider: ProviderView) {
    setBusyProvider(provider.provider); setActionError(undefined); setNotice(undefined);
    try {
      const result = await api<{ status: string; message: string; latency_ms: number }>(`/admin/provider-settings/${provider.provider}/test`, { method: "POST" });
      const resultMessage = `${result.message}（${result.latency_ms} ms）`;
      if (result.status === "success") setNotice(resultMessage);
      else setActionError(resultMessage);
      const refreshed = await api<Snapshot>("/admin/provider-settings");
      setSnapshot(refreshed); setDrafts(makeDrafts(refreshed));
    } catch (reason) { setActionError((reason as Error).message); }
    finally { setBusyProvider(undefined); }
  }

  if (loadError) return <div className="mt-8 rounded-2xl bg-red-50 p-5 text-red-800"><strong>無法開啟管理後台</strong><p className="mt-1 text-sm">{loadError}</p><p className="mt-2 text-xs">請先在主機設定 ADMIN_EMAILS，或將帳號的 is_admin 設為 true。</p></div>;
  if (!snapshot) return <p className="mt-8 flex items-center gap-2 text-[var(--muted)]"><LoaderCircle className="animate-spin" size={18} />正在讀取加密設定…</p>;

  const visibleProviders = snapshot.providers.filter((provider) => {
    if (scope === "system") return provider.provider === "runtime";
    if (scope === "layout") return provider.provider === "layout";
    return provider.provider !== "runtime" && provider.provider !== "layout";
  });
  const visibleAudit = snapshot.audit.filter((item) =>
    scope === "system" ? item.target === "runtime" : scope === "layout" ? item.target === "layout" : item.target !== "runtime" && item.target !== "layout"
  );
  const auditPanel = "__audit";
  const providerPanels = [...visibleProviders.map((provider) => provider.provider), auditPanel];
  const displayedProviders = scope === "providers"
    ? visibleProviders.filter((provider) => provider.provider === activePanel)
    : visibleProviders;
  const showAudit = scope !== "providers" || activePanel === auditPanel;

  function moveTab(event: React.KeyboardEvent<HTMLButtonElement>, index: number) {
    if (!(["ArrowLeft", "ArrowRight", "Home", "End"] as string[]).includes(event.key)) return;
    event.preventDefault();
    const nextIndex = event.key === "Home" ? 0 : event.key === "End" ? providerPanels.length - 1 : (index + (event.key === "ArrowRight" ? 1 : -1) + providerPanels.length) % providerPanels.length;
    const next = providerPanels[nextIndex];
    setActivePanel(next);
    requestAnimationFrame(() => document.getElementById(`provider-tab-${next}`)?.focus());
  }

  return <div className="mt-8 space-y-6">
    {scope === "providers" && <section className="grid gap-4 rounded-[1.75rem] border border-[var(--line)] bg-[var(--ink)] p-6 text-white md:grid-cols-[auto_1fr] md:items-center"><ShieldCheck size={32} className="text-emerald-200" /><div><h2 className="font-bold">秘密資料不會回傳前端</h2><p className="mt-1 text-sm leading-6 text-white/70">資料庫只保存 Fernet 加密內容；畫面只顯示末四碼。此次使用 {snapshot.encryption_source} 衍生加密金鑰，正式環境建議固定設定 SETTINGS_ENCRYPTION_KEY。</p></div></section>}
    {notice && <p role="status" className="flex items-center gap-2 rounded-xl bg-emerald-50 p-4 text-sm text-emerald-800"><Check size={17} />{notice}</p>}
    {actionError && <p role="alert" className="rounded-xl bg-red-50 p-4 text-sm text-red-800">{actionError}</p>}

    {scope === "providers" && <>
      <label className="block text-sm font-semibold md:hidden">
        {t("providerTabs.mobileLabel")}
        <select value={activePanel || visibleProviders[0]?.provider || auditPanel} onChange={(event) => setActivePanel(event.target.value)} className="mt-2 w-full rounded-xl border border-[var(--line)] bg-white px-3 py-3 font-normal">
          {visibleProviders.map((provider) => <option key={provider.provider} value={provider.provider}>{provider.label}</option>)}
          <option value={auditPanel}>{t("providerTabs.audit")}</option>
        </select>
      </label>
      <div role="tablist" aria-label={t("providerTabs.label")} className="hidden gap-2 overflow-x-auto pb-2 md:flex">
        {providerPanels.map((panel, index) => {
          const selected = panel === activePanel;
          const label = panel === auditPanel ? t("providerTabs.audit") : visibleProviders.find((provider) => provider.provider === panel)?.label || panel;
          return <button key={panel} id={`provider-tab-${panel}`} type="button" role="tab" aria-selected={selected} aria-controls={`provider-panel-${panel}`} tabIndex={selected ? 0 : -1} onClick={() => setActivePanel(panel)} onKeyDown={(event) => moveTab(event, index)} className={`shrink-0 rounded-full border px-4 py-2 text-sm font-semibold transition ${selected ? "border-[var(--teal)] bg-[var(--teal)] text-white" : "border-[var(--line)] bg-white text-[var(--ink)] hover:border-[var(--teal)]"}`}>{label}</button>;
        })}
      </div>
    </>}

    <div className="grid gap-6">{displayedProviders.map((provider) => {
      const draft = drafts[provider.provider];
      const busy = busyProvider === provider.provider;
      const usage = provider.usage;
      const internal = provider.provider === "runtime" || provider.provider === "layout";
      return <section key={provider.provider} id={scope === "providers" ? `provider-panel-${provider.provider}` : undefined} role={scope === "providers" ? "tabpanel" : undefined} aria-labelledby={scope === "providers" ? `provider-tab-${provider.provider}` : undefined} className="rounded-[1.75rem] border border-[var(--line)] bg-white p-5 shadow-sm md:p-7">
        <div className="flex flex-wrap items-start justify-between gap-4"><div className="max-w-2xl"><div className="flex flex-wrap items-center gap-2"><h2 className="text-xl font-bold">{provider.label}</h2><span className={`rounded-full px-2.5 py-1 text-xs font-semibold ${statusClass(provider.status)}`}>{provider.status === "ready" ? "已設定" : provider.status === "disabled" ? "已停用" : provider.status === "test_required" ? "待測試" : provider.status === "error" ? "連線失敗" : "待設定"}</span></div><p className="mt-2 text-sm leading-6 text-[var(--muted)]">{provider.description}</p><p className="mt-1 text-xs font-semibold text-[var(--teal)]">{provider.status_message}</p>{!internal && <p className="mt-2 text-xs text-[var(--muted)]">近 24 小時：{provider.requests_24h || 0} 次呼叫 · {provider.errors_24h || 0} 次失敗{provider.last_error_at ? ` · 最近失敗 ${dateTime.format(new Date(provider.last_error_at))}` : ""}</p>}</div>{!internal && <label className="flex items-center gap-2 rounded-full bg-[var(--paper)] px-4 py-2 text-sm font-semibold"><input type="checkbox" checked={draft.enabled} onChange={(event) => patchDraft(provider.provider, { enabled: event.target.checked })} />啟用</label>}</div>

        {provider.provider === "google_maps" && usage && <GoogleUsagePanel usage={usage} refreshing={usageRefreshing} onRefresh={refreshUsage} />}
        {provider.provider === "naver_maps" && usage && <NaverUsagePanel usage={usage} refreshing={usageRefreshing} onRefresh={refreshUsage} />}
        {provider.provider === "youtube_guides" && usage && <YouTubeUsagePanel usage={usage} automaticSearchBudget={Number(provider.config.hotspot_guide_youtube_daily_search_budget || 80)} refreshing={usageRefreshing} onRefresh={refreshUsage} />}

        {Object.keys(provider.config).length > 0 && <div className="mt-6 grid gap-4 md:grid-cols-2">{Object.entries(provider.config).map(([field]) => {
          const meta = fieldMeta[field] || { label: field };
          const label = provider.provider === "layout" ? t(`layout.fields.${field}.label`) : meta.label;
          const help = provider.provider === "layout" ? t(`layout.fields.${field}.help`) : meta.help;
          if (meta.type === "boolean") return <label key={field} className="flex items-start gap-3 rounded-2xl border border-[var(--line)] bg-[var(--paper)] p-4 md:col-span-2"><input type="checkbox" role="switch" checked={draft.config[field] === "true"} onChange={(event) => patchConfig(provider.provider, field, String(event.target.checked))} className="mt-1" /><span><span className="font-semibold">{label}</span><span className="ml-2 text-[.65rem] font-normal text-[var(--muted)]">{provider.config_sources[field] === "database" ? "後台值" : "環境預設"}</span>{help && <span className="mt-1 block text-xs font-normal leading-5 text-[var(--muted)]">{help}</span>}</span></label>;
          return <label key={field} className="text-sm font-semibold">{meta.label}<span className="ml-2 text-[.65rem] font-normal text-[var(--muted)]">{provider.config_sources[field] === "database" ? "後台值" : "環境預設"}</span>{meta.options ? <select value={draft.config[field]} onChange={(event) => patchConfig(provider.provider, field, event.target.value)} className="mt-2 w-full rounded-xl border border-[var(--line)] bg-white px-3 py-3 font-normal">{meta.options.map((option) => <option key={option.value} value={option.value}>{option.label}</option>)}</select> : <input type={meta.type || "text"} step={meta.type === "number" ? "any" : undefined} value={draft.config[field]} onChange={(event) => patchConfig(provider.provider, field, event.target.value)} className="mt-2 w-full rounded-xl border border-[var(--line)] px-3 py-3 font-normal" />}{meta.help && <span className="mt-1 block text-xs font-normal text-[var(--muted)]">{meta.help}</span>}</label>;
        })}</div>}

        {Object.keys(provider.secrets).length > 0 && <div className="mt-6"><h3 className="flex items-center gap-2 text-sm font-bold"><KeyRound size={16} className="text-[var(--teal)]" />API 金鑰與憑證</h3><div className="mt-3 grid gap-4 md:grid-cols-2">{Object.entries(provider.secrets).map(([field, secret]) => { const meta = secretLabels[field] || { label: field }; const clearing = draft.clearSecrets.includes(field); return <div key={field} className="rounded-2xl bg-[var(--paper)] p-4"><label className="text-sm font-semibold">{meta.label}<input type="password" autoComplete="off" value={draft.secrets[field]} onChange={(event) => patchSecret(provider.provider, field, event.target.value)} placeholder={secret.masked || "貼上新金鑰"} className="mt-2 w-full rounded-xl border border-[var(--line)] bg-white px-3 py-3 font-mono text-sm font-normal" /></label><div className="mt-2 flex items-center justify-between gap-3 text-xs text-[var(--muted)]"><span className="flex items-center gap-1"><EyeOff size={13} />{clearing ? "儲存後清除後台值" : sourceLabel[secret.source] || secret.source}</span>{secret.source === "database" && !clearing && <button type="button" onClick={() => clearSecret(provider.provider, field)} className="flex items-center gap-1 font-semibold text-red-700"><Trash2 size={13} />清除</button>}</div>{meta.help && <p className="mt-2 text-xs leading-5 text-[var(--muted)]">{meta.help}</p>}</div>; })}</div></div>}

        <div className="mt-6 flex flex-wrap items-center gap-3"><button type="button" onClick={() => save(provider)} disabled={Boolean(busyProvider)} className="flex items-center gap-2 rounded-xl bg-[var(--teal)] px-5 py-3 text-sm font-semibold text-white disabled:opacity-50">{busy ? <LoaderCircle size={16} className="animate-spin" /> : <Save size={16} />}儲存設定</button>{!internal && <button type="button" onClick={() => testConnection(provider)} disabled={Boolean(busyProvider) || !draft.enabled} className="flex items-center gap-2 rounded-xl border border-[var(--line)] px-5 py-3 text-sm font-semibold disabled:opacity-40"><PlugZap size={16} />測試連線</button>}{!internal && <span className="text-xs text-[var(--muted)]">空白金鑰不會覆蓋現有值；清除後會改用主機環境設定。</span>}</div>
        {provider.last_tested_at && <p className={`mt-4 rounded-xl px-4 py-3 text-sm ${statusClass(provider.last_test_status || "")}`}>上次測試：{dateTime.format(new Date(provider.last_tested_at))} · {provider.last_test_message}</p>}
      </section>;
    })}</div>

    {showAudit && <section id={scope === "providers" ? `provider-panel-${auditPanel}` : undefined} role={scope === "providers" ? "tabpanel" : undefined} aria-labelledby={scope === "providers" ? `provider-tab-${auditPanel}` : undefined} className="rounded-[1.75rem] border border-[var(--line)] bg-white p-5 md:p-7"><h2 className="text-xl font-bold">最近管理紀錄</h2><p className="mt-1 text-sm text-[var(--muted)]">{scope === "system" ? "只記錄異動欄位、操作者與公開註冊結果，不記錄敏感設定內容。" : scope === "layout" ? t("layout.auditDescription") : "只記錄變更欄位名稱、操作者與測試結果，不記錄金鑰內容。"}</p>{visibleAudit.length ? <ol className="mt-5 divide-y divide-[var(--line)]">{visibleAudit.map((item) => <li key={item.id} className="grid gap-1 py-3 text-sm md:grid-cols-[10rem_1fr_auto]"><time className="text-[var(--muted)]">{dateTime.format(new Date(item.created_at))}</time><span className="font-semibold">{item.action === "layout_settings_updated" ? t("layout.auditAction") : auditActionLabel[item.action] || item.action} · {item.target}</span><code className="text-xs text-[var(--muted)]">{auditSummary(item.metadata)}</code></li>)}</ol> : <p className="mt-5 rounded-xl bg-[var(--paper)] p-5 text-sm text-[var(--muted)]">尚無管理操作紀錄。</p>}</section>}
  </div>;
}
