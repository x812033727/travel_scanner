"use client";

import { Check, EyeOff, Gauge, KeyRound, LoaderCircle, PlugZap, RefreshCw, Save, ShieldCheck, Trash2 } from "lucide-react";
import { useLocale, useTranslations } from "next-intl";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { Link, useRouter } from "@/i18n/navigation";
import { AdminReadOnlyNotice, useAdminActionGuard } from "@/components/admin-action-guard";
import { ApiError, api } from "@/lib/api";
import { useHeaderSession } from "@/components/header-session";
import { adminNavigate, useAdminQueryValue } from "@/lib/admin-workspace-navigation";
import { adminSettingsCopy } from "@/lib/admin-settings-copy";
import { adminCatalogBudgetCopy, validCatalogCallLimit } from "@/lib/admin-catalog-budget-copy";
import { klookAffiliateCopy } from "@/lib/klook-affiliate-copy";
import { domainSettingsDependencies, isDomainSettingsScope, settingsHref, settingsOwner, type AdminSettingsScope } from "@/lib/admin-settings-ownership";

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
type FieldOption = { value: string; label?: string; description?: string | null; status?: string };
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
  field_options?: Record<string, FieldOption[]>;
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
type Draft = { base: ProviderView; enabled: boolean; config: Record<string, string>; secrets: Record<string, string>; clearSecrets: string[]; customFields: string[] };
// App-router Back/Forward does not fire beforeunload and cannot be cancelled by
// popstate. Keep drafts in memory across route unmounts, never browser storage.
// The session identity isolates new logins, even for the same account, without
// treating a currency/profile update as a login. Logout releases the old key.
const routeDrafts = new WeakMap<object, Map<AdminSettingsScope, Record<string, Draft>>>();
type FieldMeta = { label?: string; type?: "text" | "number" | "url" | "boolean"; options?: FieldOption[]; help?: string; localized?: boolean; allowCustom?: boolean; emptyOption?: "inheritPlanner" | "inheritGuideSearch" };
type ProviderCategory = "auth" | "ai" | "maps" | "content" | "travelData" | "affiliate" | "other";

const providerCategories: ProviderCategory[] = ["auth", "ai", "maps", "content", "travelData", "affiliate", "other"];
const providerCategoryOf: Record<string, ProviderCategory> = {
  google_login: "auth",
  line_login: "auth",
  apple_login: "auth",
  analytics: "auth",
  ai_vendors: "ai",
  ai_planner: "ai",
  ai_guide_search: "ai",
  hotspot_intros: "ai",
  google_maps: "maps",
  naver_maps: "maps",
  navitime: "maps",
  ekispert: "maps",
  odsay: "maps",
  hotspot_guides: "content",
  youtube_guides: "content",
  brave_guides: "content",
  gemini_guides: "ai",
  amadeus: "travelData",
  skyscanner: "travelData",
  duffel: "travelData",
  flightaware: "travelData",
  google_travel_impact: "travelData",
  booking_demand: "travelData",
  travelpayouts: "affiliate",
  kkday: "affiliate",
  klook: "affiliate",
  airalo: "affiliate",
  trip_com: "affiliate",
  agoda: "affiliate",
  booking: "affiliate",
  skyscanner_affiliate: "affiliate",
};

const fieldMeta: Record<string, FieldMeta> = {
  auth_google_client_id: { localized: true },
  auth_line_channel_id: { localized: true },
  auth_apple_services_id: { label: "Apple Services ID" },
  auth_apple_team_id: { label: "Apple Team ID" },
  auth_apple_key_id: { label: "Apple Key ID" },
  auth_oauth_flow_ttl_seconds: { localized: true, type: "number" },
  auth_oauth_ip_limit: { localized: true, type: "number" },
  ga4_enabled: { localized: true, type: "boolean" },
  ga4_measurement_id: { localized: true },
  analytics_trust_country_header: { localized: true, type: "boolean" },
  analytics_event_ip_limit: { localized: true, type: "number" },
  analytics_event_session_limit: { localized: true, type: "number" },
  analytics_retention_days: { localized: true, type: "number" },
  analytics_rollup_retention_months: { localized: true, type: "number" },
  registration_enabled: { localized: true, type: "boolean" },
  access_token_expire_minutes: { localized: true, type: "number" },
  session_absolute_max_days: { localized: true, type: "number" },
  google_maps_javascript_enabled: { localized: true, type: "boolean" },
  hotspots_enabled: { label: "", type: "boolean" },
  trips_enabled: { label: "", type: "boolean" },
  alerts_enabled: { label: "", type: "boolean" },
  flight_status_enabled: { label: "", type: "boolean" },
  airline_fares_enabled: { label: "", type: "boolean" },
  pricing_enabled: { label: "", type: "boolean" },
  ai_planner_mode: { localized: true, options: [{ value: "auto" }, { value: "openai" }, { value: "anthropic", label: "Claude" }, { value: "minimax", label: "MiniMax" }, { value: "gemini", label: "Gemini" }, { value: "fallback" }, { value: "disabled" }] },
  ai_planner_priority: { localized: true },
  ai_planner_timeout_seconds: { localized: true, type: "number" },
  ai_planner_total_timeout_seconds: { localized: true, type: "number" },
  ai_planner_max_output_tokens: { localized: true, type: "number" },
  hotspot_guide_ai_default_provider: { localized: true, options: [{ value: "minimax", label: "MiniMax" }, { value: "openai", label: "OpenAI" }, { value: "anthropic", label: "Claude" }, { value: "gemini", label: "Gemini" }] },
  hotspot_guide_ai_timeout_seconds: { localized: true, type: "number" },
  hotspot_guide_ai_max_output_tokens: { localized: true, type: "number" },
  hotspot_guide_ai_daily_run_limit: { localized: true, type: "number" },
  hotspot_guide_ai_daily_call_budget: { localized: true, type: "number" },
  hotspot_guide_ai_openai_model: { localized: true, allowCustom: true, emptyOption: "inheritPlanner" },
  hotspot_guide_ai_anthropic_model: { localized: true, allowCustom: true, emptyOption: "inheritPlanner" },
  hotspot_guide_ai_minimax_model: { localized: true, allowCustom: true, emptyOption: "inheritPlanner" },
  hotspot_guide_ai_gemini_model: { localized: true, allowCustom: true, emptyOption: "inheritPlanner" },
  hotspot_intro_ai_default_provider: { localized: true, options: [{ value: "minimax", label: "MiniMax" }, { value: "openai", label: "OpenAI" }, { value: "anthropic", label: "Claude" }, { value: "gemini", label: "Gemini" }] },
  hotspot_intro_ai_timeout_seconds: { localized: true, type: "number" },
  hotspot_intro_ai_max_output_tokens: { localized: true, type: "number" },
  hotspot_intro_ai_daily_run_limit: { localized: true, type: "number" },
  hotspot_intro_ai_daily_call_budget: { localized: true, type: "number" },
  hotspot_intro_ai_openai_model: { localized: true, allowCustom: true, emptyOption: "inheritGuideSearch" },
  hotspot_intro_ai_anthropic_model: { localized: true, allowCustom: true, emptyOption: "inheritGuideSearch" },
  hotspot_intro_ai_minimax_model: { localized: true, allowCustom: true, emptyOption: "inheritGuideSearch" },
  hotspot_intro_ai_gemini_model: { localized: true, allowCustom: true, emptyOption: "inheritGuideSearch" },
  openai_api_base_url: { label: "OpenAI API Base URL", type: "url" },
  openai_model: { localized: true, allowCustom: true },
  anthropic_api_base_url: { label: "Claude API Base URL", type: "url" },
  anthropic_model: { localized: true, allowCustom: true },
  minimax_api_base_url: { label: "MiniMax API Base URL", type: "url" },
  minimax_model: { localized: true, allowCustom: true },
  gemini_model: { localized: true, allowCustom: true },
  travel_provider_mode: { localized: true, options: [{ value: "amadeus", label: "Amadeus" }, { value: "mock" }, { value: "disabled" }] },
  flight_provider_mode: { localized: true, options: [{ value: "auto" }, { value: "skyscanner", label: "Skyscanner" }, { value: "duffel", label: "Duffel" }, { value: "amadeus", label: "Amadeus" }, { value: "mock" }, { value: "disabled" }] },
  flight_search_strategy: { localized: true, options: [{ value: "hybrid" }, { value: "single" }] },
  flight_min_result_count: { localized: true, type: "number" },
  hotel_provider_mode: { localized: true, options: [{ value: "auto" }, { value: "booking", label: "Booking.com Demand API" }, { value: "amadeus", label: "Amadeus" }, { value: "mock" }, { value: "disabled" }] },
  provider_timeout_seconds: { localized: true, type: "number" },
  provider_failure_threshold: { localized: true, type: "number" },
  provider_circuit_seconds: { localized: true, type: "number" },
  route_cache_ttl_seconds: { localized: true, type: "number" },
  naver_place_cache_ttl_seconds: { localized: true, type: "number" },
  naver_maps_monthly_request_limit: { localized: true, type: "number" },
  weather_cache_ttl_seconds: { localized: true, type: "number" },
  google_maps_essentials_free_limit: { localized: true, type: "number" },
  google_maps_pro_free_limit: { localized: true, type: "number" },
  google_maps_enterprise_free_limit: { localized: true, type: "number" },
  restaurant_scan_enabled: { localized: true, type: "boolean" },
  restaurant_aggregate_monthly_budget: { localized: true, type: "number" },
  restaurant_nearby_monthly_budget: { localized: true, type: "number" },
  restaurant_details_monthly_budget: { localized: true, type: "number" },
  restaurant_scan_refresh_days: { localized: true, type: "number" },
  restaurant_scan_max_depth: { localized: true, type: "number" },
  restaurant_scan_batch_call_limit: { localized: true, type: "number" },
  restaurant_location_cache_days: { localized: true, type: "number" },
  hotspot_guide_youtube_daily_search_budget: { localized: true, type: "number" },
  hotspot_guide_youtube_search_daily_free_limit: { localized: true, type: "number" },
  hotspot_guide_youtube_core_daily_free_limit: { localized: true, type: "number" },
  hotspot_guide_refresh_days: { localized: true, type: "number" },
  hotspot_guide_gemini_base_url: { localized: true, type: "url" },
  hotspot_guide_gemini_model: { localized: true, allowCustom: true },
  hotspot_guide_gemini_timeout_seconds: { localized: true, type: "number" },
  hotspot_guide_gemini_daily_search_budget: { localized: true, type: "number" },
  catalog_review_max_calls: { type: "number" },
  hotspot_guide_backfill_enabled: { localized: true, type: "boolean" },
  hotspot_guide_backfill_batch_size: { localized: true, type: "number" },
  hotspot_guide_backfill_locale: { localized: true, type: "text" },
  amadeus_env: { localized: true, options: [{ value: "test", label: "Test" }, { value: "production", label: "Production" }] },
  skyscanner_base_url: { label: "API Base URL", type: "url" },
  skyscanner_market: { localized: true },
  skyscanner_locale: { localized: true },
  skyscanner_currency: { localized: true },
  skyscanner_poll_attempts: { localized: true, type: "number" },
  skyscanner_poll_interval_seconds: { localized: true, type: "number" },
  duffel_env: { localized: true, options: [{ value: "test", label: "Test" }, { value: "live", label: "Live" }] },
  duffel_base_url: { label: "Duffel API Base URL", type: "url" },
  duffel_supplier_timeout_ms: { localized: true, type: "number" },
  flightaware_base_url: { label: "AeroAPI Base URL", type: "url" },
  flightaware_enrich_offer_limit: { localized: true, type: "number" },
  flightaware_cache_ttl_seconds: { localized: true, type: "number" },
  flightaware_track_cache_ttl_seconds: { localized: true, type: "number" },
  google_travel_impact_base_url: { label: "Travel Impact API Base URL", type: "url" },
  travel_impact_cache_ttl_seconds: { localized: true, type: "number" },
  navitime_api_base_url: { localized: true, type: "url" },
  navitime_monthly_request_limit: { localized: true, type: "number" },
  ekispert_api_base_url: { localized: true, type: "url" },
  ekispert_search_type: { localized: true, options: [{ value: "plain" }, { value: "departure" }] },
  ekispert_monthly_request_limit: { localized: true, type: "number" },
  odsay_api_base_url: { localized: true, type: "url" },
  odsay_language: { localized: true, options: [{ value: "0" }, { value: "1" }, { value: "2" }, { value: "3" }, { value: "4" }] },
  odsay_daily_request_limit: { localized: true, type: "number" },
  travelpayouts_api_base_url: { label: "Partner Links API Base URL", type: "url" },
  travelpayouts_marker: { label: "Marker" },
  travelpayouts_project_id: { label: "Project ID" },
  travelpayouts_static_url_template: { localized: true, type: "url" },
  travelpayouts_flight_target_url: { localized: true, type: "url" },
  travelpayouts_hotel_target_url: { localized: true, type: "url" },
  travelpayouts_activities_target_url: { localized: true, type: "url" },
  travelpayouts_transport_target_url: { localized: true, type: "url" },
  travelpayouts_connectivity_target_url: { localized: true, type: "url" },
  travelpayouts_allowed_hosts: { localized: true },
  kkday_cid: { label: "KKpartners CID" },
  kkday_affiliate_url_template: { localized: true, type: "url" },
  kkday_allowed_hosts: { localized: true },
  kkday_api_base_url: { localized: true, type: "url" },
  klook_affiliate_url_template: { localized: true, type: "url" },
  klook_affiliate_id: { label: "Klook Affiliate ID" },
  klook_allowed_hosts: { localized: true },
  klook_api_base_url: { localized: true, type: "url" },
  airalo_affiliate_url_template: { localized: true, type: "url" },
  airalo_allowed_hosts: { localized: true },
  trip_com_affiliate_url_template: { localized: true, type: "url" },
  trip_com_allowed_hosts: { localized: true },
  agoda_cid: { label: "Agoda CID" },
  agoda_affiliate_url_template: { localized: true, type: "url" },
  agoda_allowed_hosts: { localized: true },
  agoda_api_base_url: { localized: true, type: "url" },
  booking_affiliate_id: { label: "Booking.com Affiliate ID" },
  booking_affiliate_url_template: { localized: true, type: "url" },
  booking_allowed_hosts: { localized: true },
  booking_demand_env: { localized: true, options: [{ value: "sandbox", label: "Sandbox" }, { value: "production", label: "Production" }] },
  booking_demand_api_base_url: { localized: true, type: "url" },
  booking_demand_affiliate_id: { localized: true },
  booking_booker_country: { localized: true },
  booking_language: { localized: true },
  booking_location_cache_ttl_seconds: { localized: true, type: "number" },
  skyscanner_affiliate_url_template: { localized: true, type: "url" },
  skyscanner_affiliate_allowed_hosts: { localized: true },
};

const secretLabels: Record<string, { label?: string; help?: string; localized?: boolean }> = {
  auth_google_client_secret: { localized: true },
  auth_line_channel_secret: { localized: true },
  auth_apple_private_key: { localized: true },
  openai_api_key: { localized: true },
  anthropic_api_key: { localized: true },
  minimax_api_key: { localized: true },
  google_maps_api_key: { localized: true },
  next_public_google_maps_browser_key: { localized: true },
  naver_maps_client_id: { localized: true },
  naver_maps_client_secret: { localized: true },
  amadeus_client_id: { label: "Client ID" },
  amadeus_client_secret: { label: "Client Secret" },
  skyscanner_api_key: { label: "API Key" },
  duffel_access_token: { label: "Access Token" },
  flightaware_api_key: { label: "AeroAPI Key" },
  google_travel_impact_api_key: { label: "Travel Impact API Key" },
  navitime_client_id: { localized: true },
  navitime_api_key: { localized: true },
  ekispert_api_key: { localized: true },
  odsay_api_key: { localized: true },
  travelpayouts_api_token: { label: "API Token" },
  kkday_api_key: { localized: true },
  klook_api_key: { localized: true },
  agoda_api_key: { localized: true },
  booking_demand_api_token: { label: "Demand API Bearer Token" },
  hotspot_guide_youtube_api_key: { localized: true },
  hotspot_guide_brave_api_key: { localized: true },
  hotspot_guide_gemini_api_key: { localized: true },
};

const usageCategoryLabel: Record<string, string> = {
  essentials: "Essentials",
  pro: "Pro",
  enterprise: "Enterprise",
};
type Translator = ReturnType<typeof useTranslations>;

const sourceKeys = new Set(["database", "environment", "none", "disabled"]);
function sourceName(t: Translator, source: string): string {
  return sourceKeys.has(source) ? t(`settingsPanel.sources.${source}`) : source;
}
const auditActionKeys: Record<string, string> = {
  system_settings_updated: "system_settings_updated",
  provider_settings_updated: "provider_settings_updated",
  provider_connection_tested: "provider_connection_tested",
  "admin_role.updated": "admin_role_updated",
};
function auditActionName(t: Translator, action: string): string {
  const key = auditActionKeys[action];
  return key ? t(`settingsPanel.auditActions.${key}`) : action;
}
const usageOperationKeys = new Set(["places_autocomplete", "place_details", "places_text_search", "places_photo", "routes", "weather_current", "weather_daily_forecast", "local_search", "geocode", "directions", "route_transit", "search_course", "search_pub_trans_path", "search_list", "videos_list"]);
function usageOperationName(t: Translator, operation: string): string {
  return usageOperationKeys.has(operation) ? t(`settingsPanel.usageOperations.${operation}`) : operation;
}
function optionalMessage(t: Translator, key: string): string | undefined {
  return t.has(key) ? t(key) : undefined;
}
function secretMeta(t: Translator, field: string): { label: string; help?: string } {
  const meta = secretLabels[field];
  if (!meta) return { label: field };
  if (!meta.localized) return { label: meta.label || field, help: meta.help };
  return { label: t(`providerSecrets.${field}.label`), help: optionalMessage(t, `providerSecrets.${field}.help`) };
}
function useFormatters() {
  const locale = useLocale();
  return useMemo(() => ({
    dateTime: new Intl.DateTimeFormat(locale, { dateStyle: "medium", timeStyle: "short" }),
    dateOnly: new Intl.DateTimeFormat(locale, { dateStyle: "medium", timeZone: "UTC" }),
    numberFormat: new Intl.NumberFormat(locale),
  }), [locale]);
}

function auditSummary(metadata: Record<string, unknown>): string {
  for (const field of ["registration_enabled", "status", "enabled", "is_admin"]) {
    if (field in metadata) return String(metadata[field]);
  }
  if (Array.isArray(metadata.config_fields)) return metadata.config_fields.join(", ");
  return "";
}

function makeDrafts(snapshot: Snapshot): Record<string, Draft> {
  return Object.fromEntries(snapshot.providers.map((provider) => [provider.provider, {
    base: provider,
    enabled: provider.enabled,
    config: Object.fromEntries(Object.entries(provider.config).map(([key, value]) => [key, value == null ? "" : String(value)])),
    secrets: Object.fromEntries(Object.keys(provider.secrets).map((key) => [key, ""])),
    clearSecrets: [],
    customFields: [],
  }]));
}

function isDraftDirty(draft: Draft): boolean {
  return draft.enabled !== draft.base.enabled
    || Object.entries(draft.config).some(([key, value]) => value !== (draft.base.config[key] == null ? "" : String(draft.base.config[key])))
    || Object.values(draft.secrets).some((value) => Boolean(value.trim()))
    || draft.clearSecrets.length > 0;
}

function ownedChanges(draft: Draft, scope: AdminSettingsScope) {
  const provider = draft.base.provider;
  const config = Object.fromEntries(Object.entries(draft.config)
    .filter(([key, value]) => settingsOwner(provider, "config", key) === scope && value !== (draft.base.config[key] == null ? "" : String(draft.base.config[key])))
    .map(([key, value]) => [key, value.trim() === "" ? null : valueForApi(key, value)]));
  const secrets: Record<string, string | null> = {};
  for (const [key, value] of Object.entries(draft.secrets)) {
    if (settingsOwner(provider, "secret", key) === scope && value.trim()) secrets[key] = value.trim();
  }
  for (const key of draft.clearSecrets) if (settingsOwner(provider, "secret", key) === scope) secrets[key] = null;
  const enabled = hasEnableToggle(provider) && settingsOwner(provider, "enabled") === scope && draft.enabled !== draft.base.enabled ? draft.enabled : undefined;
  return { config, secrets, ...(enabled === undefined ? {} : { enabled }) };
}

function valueForApi(key: string, value: string): Scalar {
  if (fieldMeta[key]?.type === "number") return Number(value);
  if (fieldMeta[key]?.type === "boolean") return value === "true";
  return value;
}

const customOption = "__custom__";
type AiVendor = "openai" | "anthropic" | "minimax" | "gemini";
const aiVendors: AiVendor[] = ["openai", "anthropic", "minimax", "gemini"];
const aiFeatureCards: Record<string, { selector: string; anchor: string; models: Record<AiVendor, string> }> = {
  ai_planner: { selector: "ai_planner_mode", anchor: "ai_planner_priority", models: { openai: "openai_model", anthropic: "anthropic_model", minimax: "minimax_model", gemini: "gemini_model" } },
  ai_guide_search: { selector: "hotspot_guide_ai_default_provider", anchor: "hotspot_guide_ai_default_provider", models: { openai: "hotspot_guide_ai_openai_model", anthropic: "hotspot_guide_ai_anthropic_model", minimax: "hotspot_guide_ai_minimax_model", gemini: "hotspot_guide_ai_gemini_model" } },
  hotspot_intros: { selector: "hotspot_intro_ai_default_provider", anchor: "hotspot_intro_ai_default_provider", models: { openai: "hotspot_intro_ai_openai_model", anthropic: "hotspot_intro_ai_anthropic_model", minimax: "hotspot_intro_ai_minimax_model", gemini: "hotspot_intro_ai_gemini_model" } },
};
const isAiVendor = (value: string): value is AiVendor => (aiVendors as string[]).includes(value);

function selectedAiVendors(card: (typeof aiFeatureCards)[string], draft: Draft): AiVendor[] {
  const mode = draft.config[card.selector];
  if (isAiVendor(mode)) return [mode];
  if (mode !== "auto") return [];
  const priority = (draft.config.ai_planner_priority || "").split(",").map((item) => item.trim().toLowerCase()).filter(isAiVendor);
  return [...new Set([...priority, ...aiVendors])];
}

function visibleConfigFields(provider: ProviderView, draft: Draft): string[] {
  const card = aiFeatureCards[provider.provider];
  if (!card) return Object.keys(provider.config);
  const modelFields = new Set(Object.values(card.models));
  const fields = Object.keys(provider.config).filter((field) => !modelFields.has(field));
  const models = selectedAiVendors(card, draft).map((vendor) => card.models[vendor]).filter((field) => field in provider.config);
  const anchor = fields.indexOf(card.anchor) + 1;
  return [...fields.slice(0, anchor), ...models, ...fields.slice(anchor)];
}

function hasEnableToggle(provider: string): boolean {
  return !["runtime", "layout", "ai_vendors"].includes(provider);
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
  const t = useTranslations("admin");
  const { dateOnly, numberFormat } = useFormatters();
  return <div className="mt-6 rounded-2xl border border-[var(--line)] bg-[var(--paper)] p-5" aria-label={t("settingsPanel.googleUsageLabel")}>
    <div className="flex flex-wrap items-start justify-between gap-4">
      <div>
        <p className="flex items-center gap-2 text-sm font-bold text-[var(--teal)]"><Gauge size={17} />{t("settingsPanel.googleUsageTitle")}</p>
        {usage.available
          ? <p className="mt-2 text-3xl font-bold tabular-nums">{numberFormat.format(usage.used || 0)} <span className="text-base font-medium text-[var(--muted)]">{t("settingsPanel.observedRequests")}</span></p>
          : <p className="mt-2 font-semibold text-amber-800">{t("settingsPanel.usageUnavailable")}</p>}
      </div>
      <button type="button" onClick={onRefresh} disabled={refreshing} className="flex items-center gap-2 rounded-xl border border-[var(--line)] bg-white px-3 py-2 text-sm font-semibold disabled:opacity-50"><RefreshCw size={15} className={refreshing ? "animate-spin" : ""} />{t("settingsPanel.refreshUsage")}</button>
    </div>

    {usage.available && <>
      <dl className="mt-4 grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
        <div className="rounded-xl bg-white p-3"><dt className="text-xs text-[var(--muted)]">{t("settingsPanel.monthRequests")}</dt><dd className="mt-1 text-xl font-bold tabular-nums">{numberFormat.format(usage.used || 0)}</dd></div>
        <div className="rounded-xl bg-white p-3"><dt className="text-xs text-[var(--muted)]">{t("settingsPanel.freeUsage")}</dt><dd className="mt-1 text-xl font-bold tabular-nums">{numberFormat.format(usage.free_usage || 0)}</dd></div>
        <div className="rounded-xl bg-white p-3"><dt className="text-xs text-[var(--muted)]">{t("settingsPanel.skuRemaining")}</dt><dd className="mt-1 text-xl font-bold tabular-nums">{numberFormat.format(usage.free_remaining || 0)}</dd></div>
        <div className={`rounded-xl p-3 ${usage.billable_overage ? "bg-red-50 text-red-800" : "bg-emerald-50 text-emerald-800"}`}><dt className="text-xs">{t("settingsPanel.possibleOverage")}</dt><dd className="mt-1 text-xl font-bold tabular-nums">{numberFormat.format(usage.billable_overage || 0)}</dd></div>
      </dl>

      <div className="mt-5">
        <h3 className="text-sm font-bold">{t("settingsPanel.skuTitle")}</h3>
        <p className="mt-1 text-xs leading-5 text-[var(--muted)]">{t("settingsPanel.skuHint")}</p>
        <div className="mt-3 grid gap-3 md:grid-cols-2 xl:grid-cols-3">
          {usage.sku_usage.map((item) => {
            const width = Math.min(100, Math.max(0, item.percentage));
            return <article key={item.sku} className="rounded-xl bg-white p-4">
              <div className="flex items-start justify-between gap-3"><div><h4 className="text-sm font-bold">{item.label}</h4><p className="mt-0.5 text-xs text-[var(--muted)]">{usageCategoryLabel[item.category] || item.category}</p></div><span className="text-sm font-bold tabular-nums">{numberFormat.format(item.used)} / {numberFormat.format(item.free_limit)}</span></div>
              <div className="mt-3 h-2 overflow-hidden rounded-full bg-[var(--paper)]" role="progressbar" aria-label={t("settingsPanel.monthlyUsageOf", { label: item.label })} aria-valuemin={0} aria-valuemax={item.free_limit} aria-valuenow={Math.min(item.used, item.free_limit)}><div className={`h-full rounded-full ${item.billable_overage ? "bg-red-500" : item.percentage >= 75 ? "bg-amber-500" : "bg-[var(--teal)]"}`} style={{ width: `${width}%` }} /></div>
              <p className={`mt-2 text-xs ${item.billable_overage ? "font-semibold text-red-700" : "text-[var(--muted)]"}`}>{item.billable_overage ? t("settingsPanel.overageCount", { count: numberFormat.format(item.billable_overage) }) : t("settingsPanel.freeRemainingCount", { count: numberFormat.format(item.free_remaining) })}</p>
            </article>;
          })}
        </div>
      </div>

      <div className="mt-5">
        <h3 className="text-sm font-bold">{t("settingsPanel.recentMonths")}</h3>
        <div className="mt-3 overflow-x-auto rounded-xl border border-[var(--line)] bg-white">
          <table className="min-w-[42rem] w-full text-left text-sm">
            <thead className="bg-[var(--paper)] text-xs text-[var(--muted)]"><tr><th className="px-3 py-2 font-semibold">{t("settingsPanel.thMonth")}</th><th className="px-3 py-2 font-semibold">{t("settingsPanel.thRequests")}</th><th className="px-3 py-2 font-semibold">{t("settingsPanel.freeUsage")}</th><th className="px-3 py-2 font-semibold">{t("settingsPanel.skuRemaining")}</th><th className="px-3 py-2 font-semibold">{t("settingsPanel.thOverage")}</th></tr></thead>
            <tbody className="divide-y divide-[var(--line)]">{usage.monthly_history.map((month) => <tr key={month.period}><th className="px-3 py-2.5 font-semibold">{month.period}</th><td className="px-3 py-2.5 tabular-nums">{numberFormat.format(month.used)}</td><td className="px-3 py-2.5 tabular-nums">{numberFormat.format(month.free_usage)}</td><td className="px-3 py-2.5 tabular-nums">{numberFormat.format(month.free_remaining)}</td><td className={`px-3 py-2.5 tabular-nums ${month.billable_overage ? "font-semibold text-red-700" : ""}`}>{numberFormat.format(month.billable_overage)}</td></tr>)}</tbody>
          </table>
        </div>
      </div>

      <details className="mt-4 rounded-xl bg-white px-4 py-3"><summary className="cursor-pointer text-sm font-semibold">{t("settingsPanel.breakdown")}</summary><dl className="mt-3 grid gap-2 sm:grid-cols-2 lg:grid-cols-4">{Object.entries(usage.breakdown).map(([operation, count]) => <div key={operation}><dt className="text-xs text-[var(--muted)]">{usageOperationName(t, operation)}</dt><dd className="mt-0.5 font-bold tabular-nums">{numberFormat.format(count)}</dd></div>)}</dl></details>
    </>}
    <p className="mt-4 text-xs leading-5 text-[var(--muted)]">{t("settingsPanel.googlePeriodNote", { start: dateOnly.format(new Date(`${usage.period_start}T00:00:00Z`)), end: dateOnly.format(new Date(`${usage.period_end}T00:00:00Z`)) })}</p>
  </div>;
}

type UsageTone = { border: string; bg: string; text: string; bar: string; tableBorder: string };
const naverUsageTone: UsageTone = { border: "border-[#b8e7ca]", bg: "bg-[#f2fbf5]", text: "text-[#087a3f]", bar: "bg-[#03c75a]", tableBorder: "border-[#d7eee0]" };
const navitimeUsageTone: UsageTone = { border: "border-sky-200", bg: "bg-sky-50", text: "text-sky-800", bar: "bg-sky-600", tableBorder: "border-sky-100" };
const ekispertUsageTone: UsageTone = { border: "border-indigo-200", bg: "bg-indigo-50", text: "text-indigo-800", bar: "bg-indigo-600", tableBorder: "border-indigo-100" };
const odsayUsageTone: UsageTone = { border: "border-fuchsia-200", bg: "bg-fuchsia-50", text: "text-fuchsia-800", bar: "bg-fuchsia-600", tableBorder: "border-fuchsia-100" };

function MonthlyUsagePanel({ usage, refreshing, onRefresh, title, ariaLabel, progressLabel, limitLabel, remainingLabel, note, tone, period = "month" }: {
  usage: ProviderUsage;
  refreshing: boolean;
  onRefresh: () => void;
  title: string;
  ariaLabel: string;
  progressLabel: string;
  limitLabel: string;
  remainingLabel: string;
  note: string;
  tone: UsageTone;
  period?: "month" | "day";
}) {
  const t = useTranslations("admin");
  const { numberFormat } = useFormatters();
  const hasLimit = usage.monthly_limit > 0;
  const width = hasLimit ? Math.min(100, Math.max(0, usage.percentage || 0)) : 0;
  return <div className={`mt-6 rounded-2xl border ${tone.border} ${tone.bg} p-5`} aria-label={ariaLabel}>
    <div className="flex flex-wrap items-start justify-between gap-4">
      <div><p className={`flex items-center gap-2 text-sm font-bold ${tone.text}`}><Gauge size={17} />{title}</p>{usage.available ? <p className="mt-2 text-3xl font-bold tabular-nums">{numberFormat.format(usage.used || 0)} <span className="text-base font-medium text-[var(--muted)]">{t("settingsPanel.siteRequests")}</span></p> : <p className="mt-2 font-semibold text-amber-800">{t("settingsPanel.usageUnavailable")}</p>}</div>
      <button type="button" onClick={onRefresh} disabled={refreshing} className={`flex items-center gap-2 rounded-xl border ${tone.border} bg-white px-3 py-2 text-sm font-semibold disabled:opacity-50`}><RefreshCw size={15} className={refreshing ? "animate-spin" : ""} />{t("settingsPanel.refreshUsage")}</button>
    </div>
    {usage.available && <>
      <dl className="mt-4 grid gap-3 sm:grid-cols-3">
        <div className="rounded-xl bg-white p-3"><dt className="text-xs text-[var(--muted)]">{t("settingsPanel.periodRequests", { period: t(period === "day" ? "settingsPanel.periodDay" : "settingsPanel.periodMonth") })}</dt><dd className="mt-1 text-xl font-bold tabular-nums">{numberFormat.format(usage.used || 0)}</dd></div>
        <div className="rounded-xl bg-white p-3"><dt className="text-xs text-[var(--muted)]">{limitLabel}</dt><dd className="mt-1 text-xl font-bold tabular-nums">{hasLimit ? numberFormat.format(usage.monthly_limit) : t("settingsPanel.notSet")}</dd></div>
        <div className="rounded-xl bg-white p-3"><dt className="text-xs text-[var(--muted)]">{remainingLabel}</dt><dd className="mt-1 text-xl font-bold tabular-nums">{hasLimit ? numberFormat.format(usage.remaining || 0) : "—"}</dd></div>
      </dl>
      {hasLimit && <div className="mt-4 h-2 overflow-hidden rounded-full bg-white" role="progressbar" aria-label={progressLabel} aria-valuemin={0} aria-valuemax={usage.monthly_limit} aria-valuenow={Math.min(usage.used || 0, usage.monthly_limit)}><div className={`h-full rounded-full ${(usage.percentage || 0) >= 100 ? "bg-red-500" : (usage.percentage || 0) >= 75 ? "bg-amber-500" : tone.bar}`} style={{ width: `${width}%` }} /></div>}
      <details className="mt-4 rounded-xl bg-white px-4 py-3"><summary className="cursor-pointer text-sm font-semibold">{t("settingsPanel.breakdown")}</summary><dl className="mt-3 grid gap-2 sm:grid-cols-3">{Object.entries(usage.breakdown).map(([operation, count]) => <div key={operation}><dt className="text-xs text-[var(--muted)]">{usageOperationName(t, operation)}</dt><dd className="mt-0.5 font-bold tabular-nums">{numberFormat.format(count)}</dd></div>)}</dl></details>
      {usage.monthly_history.length > 0 && <div className={`mt-4 overflow-x-auto rounded-xl border ${tone.tableBorder} bg-white`}><table className="min-w-[32rem] w-full text-left text-sm"><thead className={`${tone.bg} text-xs text-[var(--muted)]`}><tr><th className="px-3 py-2 font-semibold">{t("settingsPanel.thMonth")}</th><th className="px-3 py-2 font-semibold">{t("settingsPanel.thRequests")}</th><th className="px-3 py-2 font-semibold">{limitLabel}</th><th className="px-3 py-2 font-semibold">{t("settingsPanel.thRemaining")}</th></tr></thead><tbody className="divide-y divide-[var(--line)]">{usage.monthly_history.map((month) => <tr key={month.period}><th className="px-3 py-2.5 font-semibold">{month.period}</th><td className="px-3 py-2.5 tabular-nums">{numberFormat.format(month.used)}</td><td className="px-3 py-2.5 tabular-nums">{hasLimit ? numberFormat.format(month.free_limit) : "—"}</td><td className="px-3 py-2.5 tabular-nums">{hasLimit ? numberFormat.format(month.free_remaining) : "—"}</td></tr>)}</tbody></table></div>}
    </>}
    <p className="mt-4 text-xs leading-5 text-[var(--muted)]">{note}</p>
  </div>;
}

function NaverUsagePanel(props: { usage: ProviderUsage; refreshing: boolean; onRefresh: () => void }) {
  const t = useTranslations("admin");
  return <MonthlyUsagePanel {...props} title={t("settingsPanel.naverTitle")} ariaLabel={t("settingsPanel.naverAria")} progressLabel={t("settingsPanel.naverProgress")} limitLabel={t("settingsPanel.naverLimit")} remainingLabel={t("settingsPanel.naverRemaining")} tone={naverUsageTone} note={t("settingsPanel.naverNote")} />;
}

function NavitimeUsagePanel(props: { usage: ProviderUsage; refreshing: boolean; onRefresh: () => void }) {
  const t = useTranslations("admin");
  return <MonthlyUsagePanel {...props} title={t("settingsPanel.navitimeTitle")} ariaLabel={t("settingsPanel.navitimeAria")} progressLabel={t("settingsPanel.navitimeProgress")} limitLabel={t("settingsPanel.monthlyCap")} remainingLabel={t("settingsPanel.capRemaining")} tone={navitimeUsageTone} note={t("settingsPanel.navitimeNote")} />;
}

function EkispertUsagePanel(props: { usage: ProviderUsage; refreshing: boolean; onRefresh: () => void }) {
  const t = useTranslations("admin");
  return <MonthlyUsagePanel {...props} title={t("settingsPanel.ekispertTitle")} ariaLabel={t("settingsPanel.ekispertAria")} progressLabel={t("settingsPanel.ekispertProgress")} limitLabel={t("settingsPanel.monthlyCap")} remainingLabel={t("settingsPanel.capRemaining")} tone={ekispertUsageTone} note={t("settingsPanel.ekispertNote")} />;
}

function OdsayUsagePanel(props: { usage: ProviderUsage; refreshing: boolean; onRefresh: () => void }) {
  const t = useTranslations("admin");
  return <MonthlyUsagePanel {...props} title={t("settingsPanel.odsayTitle")} ariaLabel={t("settingsPanel.odsayAria")} progressLabel={t("settingsPanel.odsayProgress")} limitLabel={t("settingsPanel.dailyCap")} remainingLabel={t("settingsPanel.capRemaining")} period="day" tone={odsayUsageTone} note={t("settingsPanel.odsayNote")} />;
}

function YouTubeUsagePanel({ usage, automaticSearchBudget, refreshing, onRefresh }: {
  usage: ProviderUsage;
  automaticSearchBudget: number;
  refreshing: boolean;
  onRefresh: () => void;
}) {
  const t = useTranslations("admin");
  const { dateOnly, numberFormat } = useFormatters();
  const search = usage.sku_usage.find((item) => item.sku === "search_queries");
  const core = usage.sku_usage.find((item) => item.sku === "core_api_units");
  const manualReserve = search ? Math.max(0, search.free_limit - automaticSearchBudget) : 0;
  const automaticBudgetExceedsAllowance = Boolean(search && automaticSearchBudget > search.free_limit);

  return <div className="mt-6 rounded-2xl border border-[var(--line)] bg-[var(--paper)] p-5" aria-label={t("settingsPanel.youtubeAria")}>
    <div className="flex flex-wrap items-start justify-between gap-4">
      <div>
        <p className="flex items-center gap-2 text-sm font-bold text-[var(--teal)]"><Gauge size={17} />{t("settingsPanel.youtubeTitle")}</p>
        {usage.available
          ? <p className="mt-2 text-3xl font-bold tabular-nums">{numberFormat.format(usage.used || 0)} <span className="text-base font-medium text-[var(--muted)]">{t("settingsPanel.observedRequests")}</span></p>
          : <p className="mt-2 font-semibold text-amber-800">{t("settingsPanel.usageUnavailable")}</p>}
      </div>
      <button type="button" onClick={onRefresh} disabled={refreshing} className="flex items-center gap-2 rounded-xl border border-[var(--line)] bg-white px-3 py-2 text-sm font-semibold disabled:opacity-50"><RefreshCw size={15} className={refreshing ? "animate-spin" : ""} />{t("settingsPanel.refreshUsage")}</button>
    </div>

    {usage.available && <>
      <dl className="mt-4 grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
        <div className="rounded-xl bg-white p-3"><dt className="text-xs text-[var(--muted)]">{t("settingsPanel.searchUsed")}</dt><dd className="mt-1 text-xl font-bold tabular-nums">{numberFormat.format(search?.used || 0)}</dd></div>
        <div className="rounded-xl bg-white p-3"><dt className="text-xs text-[var(--muted)]">{t("settingsPanel.searchRemaining")}</dt><dd className="mt-1 text-xl font-bold tabular-nums">{numberFormat.format(search?.free_remaining || 0)}</dd></div>
        <div className="rounded-xl bg-white p-3"><dt className="text-xs text-[var(--muted)]">{t("settingsPanel.coreUsed")}</dt><dd className="mt-1 text-xl font-bold tabular-nums">{numberFormat.format(core?.used || 0)}</dd></div>
        <div className="rounded-xl bg-white p-3"><dt className="text-xs text-[var(--muted)]">{t("settingsPanel.coreRemaining")}</dt><dd className="mt-1 text-xl font-bold tabular-nums">{numberFormat.format(core?.free_remaining || 0)}</dd></div>
      </dl>

      <div className="mt-5">
        <h3 className="text-sm font-bold">{t("settingsPanel.poolsTitle")}</h3>
        <p className="mt-1 text-xs leading-5 text-[var(--muted)]">{t("settingsPanel.poolsHint")}</p>
        <div className="mt-3 grid gap-3 md:grid-cols-2">
          {usage.sku_usage.map((item) => {
            const width = Math.min(100, Math.max(0, item.percentage));
            return <article key={item.sku} className="rounded-xl bg-white p-4">
              <div className="flex items-start justify-between gap-3"><div><h4 className="text-sm font-bold">{item.label}</h4><p className="mt-0.5 text-xs text-[var(--muted)]">{t("settingsPanel.googleDefaultQuota")}</p></div><span className="text-sm font-bold tabular-nums">{numberFormat.format(item.used)} / {numberFormat.format(item.free_limit)}</span></div>
              <div className="mt-3 h-2 overflow-hidden rounded-full bg-[var(--paper)]" role="progressbar" aria-label={t("settingsPanel.dailyUsageOf", { label: item.label })} aria-valuemin={0} aria-valuemax={item.free_limit} aria-valuenow={Math.min(item.used, item.free_limit)}><div className={`h-full rounded-full ${item.billable_overage ? "bg-red-500" : item.percentage >= 75 ? "bg-amber-500" : "bg-[var(--teal)]"}`} style={{ width: `${width}%` }} /></div>
              <p className={`mt-2 text-xs ${item.billable_overage ? "font-semibold text-red-700" : "text-[var(--muted)]"}`}>{item.billable_overage ? t("settingsPanel.aboveQuota", { count: numberFormat.format(item.billable_overage) }) : t("settingsPanel.remainingCount", { count: numberFormat.format(item.free_remaining) })}</p>
            </article>;
          })}
        </div>
      </div>

      <div className="mt-4 rounded-xl border border-teal-100 bg-teal-50 px-4 py-3 text-sm leading-6 text-teal-950">
        <p className="font-bold">{t("settingsPanel.autoBudgetTitle")}</p>
        <p>{automaticBudgetExceedsAllowance
          ? t("settingsPanel.autoBudgetOver", { budget: numberFormat.format(automaticSearchBudget), quota: numberFormat.format(search?.free_limit || 0) })
          : t("settingsPanel.autoBudgetOk", { budget: numberFormat.format(automaticSearchBudget), reserve: numberFormat.format(manualReserve) })}</p>
      </div>

      <details className="mt-4 rounded-xl bg-white px-4 py-3"><summary className="cursor-pointer text-sm font-semibold">{t("settingsPanel.breakdown")}</summary><dl className="mt-3 grid gap-2 sm:grid-cols-2">{Object.entries(usage.breakdown).map(([operation, count]) => <div key={operation}><dt className="text-xs text-[var(--muted)]">{usageOperationName(t, operation)}</dt><dd className="mt-0.5 font-bold tabular-nums">{numberFormat.format(count)}</dd></div>)}</dl></details>
    </>}
    <p className="mt-4 text-xs leading-5 text-[var(--muted)]">{t("settingsPanel.youtubePeriodNote", { date: dateOnly.format(new Date(`${usage.period_start}T00:00:00Z`)) })}</p>
  </div>;
}

// What actually went wrong, rather than whatever string the rejection carried. The panel used
// to render `reason.message` straight out of the catch and follow it with the ADMIN_EMAILS
// hint every time. Two things were wrong with that. A rejection that is not an ApiError never
// reached the server at all, so its message is a browser string like "Failed to fetch" —
// untranslated in every locale and about the network, not about permissions. And the
// ADMIN_EMAILS hint is only true for 401 and 403: an administrator whose laptop had dropped
// its wifi was being told to go and edit an environment variable on the host.
type LoadFailure =
  | { kind: "permission"; detail: string; requestId?: string }
  | { kind: "unreachable" }
  | { kind: "failed"; detail: string; requestId?: string };

function loadFailure(reason: unknown): LoadFailure {
  // Anything that is not an ApiError never reached the server, so its message is a browser
  // string about the network. An ApiError's message did come from the server and api() has
  // already localised it, so it is shown for both kinds; only the hint and the retry differ.
  if (!(reason instanceof ApiError)) return { kind: "unreachable" };
  return {
    kind: reason.status === 401 || reason.status === 403 ? "permission" : "failed",
    detail: reason.message,
    requestId: reason.requestId,
  };
}

export function AdminSettingsPanel({ scope = "providers", provider: linkedProvider, field: linkedField }: { scope?: AdminSettingsScope; provider?: string; field?: string }) {
  const t = useTranslations("admin");
  const copy = adminSettingsCopy(useLocale());
  const budgetCopy = adminCatalogBudgetCopy(useLocale());
  const affiliateCopy = klookAffiliateCopy(useLocale());
  const { sessionIdentity } = useHeaderSession();
  const { dateTime } = useFormatters();
  const router = useRouter();
  const manage = useAdminActionGuard("settings.manage");
  const [urlProvider] = useAdminQueryValue("provider");
  const [urlField] = useAdminQueryValue("field");
  const panelRef = useRef<HTMLDivElement>(null);
  const focusedLink = useRef<string | undefined>(undefined);
  const latestDrafts = useRef<Record<string, Draft>>({});
  const draftOwner = useRef<object | null | undefined>(undefined);
  const discardOnLeave = useRef(false);
  const snapshotEpoch = useRef(0);
  const [snapshot, setSnapshot] = useState<Snapshot>();
  const [drafts, setDrafts] = useState<Record<string, Draft>>({});
  const [loadError, setLoadError] = useState<LoadFailure>();
  const [busyProvider, setBusyProvider] = useState<string>();
  const [notice, setNotice] = useState<string>();
  const [actionError, setActionError] = useState<string>();
  const [usageRefreshing, setUsageRefreshing] = useState(false);
  const [activePanel, setActivePanel] = useState<string>();
  const [conflictProvider, setConflictProvider] = useState<string>();
  const dirty = Object.values(drafts).some(isDraftDirty);

  const applySnapshot = useCallback((result: Snapshot, resetProvider?: string) => {
    const sameSession = draftOwner.current === sessionIdentity;
    draftOwner.current = sessionIdentity;
    const retained = sessionIdentity ? routeDrafts.get(sessionIdentity)?.get(scope) : undefined;
    if (sessionIdentity) routeDrafts.get(sessionIdentity)?.delete(scope);
    setSnapshot(result);
    setDrafts((current) => {
      const fresh = makeDrafts(result);
      for (const [name, draft] of Object.entries({ ...retained, ...(sameSession ? current : {}) })) {
        // A usage refresh or another provider's save must not advance a dirty
        // draft's version token or replace its edits with the latest snapshot.
        if (fresh[name] && name !== resetProvider && isDraftDirty(draft)) fresh[name] = draft;
      }
      return fresh;
    });
    setActivePanel((current) => current || result.providers.find((provider) => provider.provider !== "runtime" && provider.provider !== "layout")?.provider);
  }, [scope, sessionIdentity]);
  const applySnapshotRef = useRef(applySnapshot);
  useEffect(() => { applySnapshotRef.current = applySnapshot; }, [applySnapshot]);

  useEffect(() => { latestDrafts.current = drafts; }, [drafts]);
  useEffect(() => () => {
    if (!sessionIdentity) return;
    const retained = Object.fromEntries(Object.entries(latestDrafts.current).filter(([, draft]) => isDraftDirty(draft)));
    if (discardOnLeave.current || !Object.keys(retained).length) { routeDrafts.get(sessionIdentity)?.delete(scope); return; }
    const byScope = routeDrafts.get(sessionIdentity) || new Map<AdminSettingsScope, Record<string, Draft>>();
    byScope.set(scope, retained);
    routeDrafts.set(sessionIdentity, byScope);
  }, [scope, sessionIdentity]);

  useEffect(() => {
    let active = true;
    api<Snapshot>("/admin/provider-settings")
      .then((result) => { if (active) applySnapshotRef.current(result); })
      .catch((reason: unknown) => { if (active) setLoadError(loadFailure(reason)); });
    return () => { active = false; };
  }, [sessionIdentity]);

  useEffect(() => {
    if (!dirty) return;
    const beforeUnload = (event: BeforeUnloadEvent) => { event.preventDefault(); event.returnValue = ""; };
    const leavesPage = (url: string) => new URL(url, window.location.href).pathname !== window.location.pathname;
    const confirmLeave = () => {
      const accepted = window.confirm(copy.leave);
      if (accepted) { discardOnLeave.current = true; if (sessionIdentity) routeDrafts.get(sessionIdentity)?.delete(scope); }
      return accepted;
    };
    const beforeNavigate = (event: Event) => {
      const url = (event as CustomEvent<{ url?: string }>).detail?.url;
      if (!event.defaultPrevented && url && leavesPage(url) && !confirmLeave()) event.preventDefault();
    };
    const click = (event: MouseEvent) => {
      if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
      const anchor = event.target instanceof Element ? event.target.closest("a[href]") : null;
      if (!(anchor instanceof HTMLAnchorElement) || anchor.target === "_blank" || anchor.hasAttribute("download")) return;
      if (leavesPage(anchor.href) && !confirmLeave()) { event.preventDefault(); event.stopPropagation(); }
    };
    window.addEventListener("beforeunload", beforeUnload);
    window.addEventListener("admin:before-navigate", beforeNavigate);
    document.addEventListener("click", click, true);
    return () => {
      window.removeEventListener("beforeunload", beforeUnload);
      window.removeEventListener("admin:before-navigate", beforeNavigate);
      document.removeEventListener("click", click, true);
    };
  }, [dirty, copy.leave, scope, sessionIdentity]);

  useEffect(() => {
    if (!snapshot) return;
    const defaultProvider = snapshot.providers.find((item) => item.provider !== "runtime" && item.provider !== "layout")?.provider;
    const requested = linkedProvider || urlProvider;
    const name = requested === "__audit" || snapshot.providers.some((item) => item.provider === requested)
      ? requested
      : scope === "providers" ? defaultProvider : requested;
    const field = linkedField ?? urlField;
    if (!name) return;
    const key = `${scope}:${name}:${field || ""}`;
    if (focusedLink.current === key) return;
    const frame = requestAnimationFrame(() => {
      if (scope === "providers" && activePanel !== name) { setActivePanel(name); return; }
      if (name === "__audit") { focusedLink.current = key; return; }
      const candidates = panelRef.current?.querySelectorAll<HTMLElement>("[data-settings-provider]");
      const target = Array.from(candidates || []).find((item) => item.dataset.settingsProvider === name && (!field || item.dataset.settingsField === field));
      if (!target) return;
      focusedLink.current = key;
      target.scrollIntoView?.({ block: "center" });
      (target.querySelector<HTMLElement>("input, select, button, a, h2") || target).focus();
    });
    return () => cancelAnimationFrame(frame);
  }, [snapshot, scope, linkedProvider, linkedField, activePanel, urlProvider, urlField]);

  function retryLoad() {
    setLoadError(undefined);
    api<Snapshot>("/admin/provider-settings")
      .then((result) => applySnapshot(result))
      .catch((reason: unknown) => setLoadError(loadFailure(reason)));
  }

  function patchDraft(provider: string, patch: Partial<Draft>) {
    // Only a new user edit cancels their earlier discard decision. Late reads
    // must not revive credentials the user explicitly chose to abandon.
    discardOnLeave.current = false;
    setDrafts((current) => ({ ...current, [provider]: { ...current[provider], ...patch } }));
  }

  function patchConfig(provider: string, field: string, value: string) {
    const draft = drafts[provider];
    patchDraft(provider, { config: { ...draft.config, [field]: value } });
  }

  function selectOption(provider: string, field: string, chosen: string) {
    const draft = drafts[provider];
    const custom = chosen === customOption;
    patchDraft(provider, {
      config: { ...draft.config, [field]: custom ? "" : chosen },
      customFields: custom ? [...new Set([...draft.customFields, field])] : draft.customFields.filter((item) => item !== field),
    });
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
    const epoch = snapshotEpoch.current;
    setUsageRefreshing(true); setActionError(undefined);
    try {
      const refreshed = await api<Snapshot>("/admin/provider-settings");
      // A slow read started before a save must not roll its acknowledged value
      // and version token back to the pre-save snapshot.
      if (epoch === snapshotEpoch.current) applySnapshot(refreshed);
    } catch (reason) { setActionError((reason as Error).message); }
    finally { setUsageRefreshing(false); }
  }

  async function save(provider: ProviderView) {
    if (!manage.allowed) return;
    const draft = drafts[provider.provider];
    const changes = ownedChanges(draft, scope);
    if (!Object.keys(changes.config).length && !Object.keys(changes.secrets).length && changes.enabled === undefined) return;
    if ("catalog_review_max_calls" in changes.config && !validCatalogCallLimit(changes.config.catalog_review_max_calls)) {
      setActionError(budgetCopy.invalidLimit);
      return;
    }
    setBusyProvider(provider.provider); setActionError(undefined); setNotice(undefined);
    try {
      const result = await api<Snapshot>(`/admin/provider-settings/${provider.provider}`, {
        method: "PUT",
        body: JSON.stringify({ ...changes, expected_updated_at: draft.base.updated_at ?? null }),
      });
      snapshotEpoch.current += 1;
      applySnapshot(result, provider.provider);
      setConflictProvider(undefined);
      setNotice(provider.provider === "runtime" ? t("settingsPanel.runtimeSaved") : provider.provider === "layout" ? t("layout.saveSuccess") : t("settingsPanel.providerSaved", { label: provider.label }));
      if (provider.provider === "layout") router.refresh();
    } catch (reason) {
      if (reason instanceof ApiError && reason.status === 409) {
        setConflictProvider(provider.provider); setActionError(copy.conflict);
      } else setActionError((reason as Error).message);
    }
    finally { setBusyProvider(undefined); }
  }

  async function reloadConflict() {
    if (!conflictProvider || !window.confirm(copy.discard)) return;
    setBusyProvider(conflictProvider);
    try {
      const refreshed = await api<Snapshot>("/admin/provider-settings");
      snapshotEpoch.current += 1;
      applySnapshot(refreshed, conflictProvider);
      setConflictProvider(undefined); setActionError(undefined);
    } catch (reason) { setActionError((reason as Error).message); }
    finally { setBusyProvider(undefined); }
  }

  async function testConnection(provider: ProviderView) {
    if (!manage.allowed) return;
    setBusyProvider(provider.provider); setActionError(undefined); setNotice(undefined);
    try {
      const result = await api<{ status: string; message: string; latency_ms: number }>(`/admin/provider-settings/${provider.provider}/test`, { method: "POST" });
      snapshotEpoch.current += 1;
      const resultMessage = t("settingsPanel.testResult", { message: result.message, latency: result.latency_ms });
      if (result.status === "success") setNotice(resultMessage);
      else setActionError(resultMessage);
      const refreshed = await api<Snapshot>("/admin/provider-settings");
      applySnapshot(refreshed);
    } catch (reason) { setActionError((reason as Error).message); }
    finally { setBusyProvider(undefined); }
  }

  if (loadError) return <div className="mt-8 rounded-2xl bg-red-50 p-5 text-red-800">
    <strong>{t("settingsPanel.loadErrorTitle")}</strong>
    <p className="mt-1 text-sm">{loadError.kind === "unreachable" ? t("settingsPanel.loadErrorUnreachable") : loadError.detail}</p>
    {/* Only 401 and 403 are actually about who you are signed in as. */}
    {loadError.kind === "permission" && <p className="mt-2 text-xs">{t("settingsPanel.loadErrorHint")}</p>}
    {loadError.kind !== "unreachable" && loadError.requestId && <p className="mt-2 text-xs">{t("settingsPanel.loadErrorRequestId", { id: loadError.requestId })}</p>}
    {loadError.kind !== "permission" && <button type="button" onClick={retryLoad} className="mt-3 inline-flex items-center gap-1.5 rounded-lg border border-red-200 bg-white px-3 py-2 text-sm font-semibold"><RefreshCw size={14} />{t("settingsPanel.loadErrorRetry")}</button>}
  </div>;
  if (!snapshot) return <p className="mt-8 flex items-center gap-2 text-[var(--muted)]"><LoaderCircle className="animate-spin" size={18} />{t("settingsPanel.loading")}</p>;

  const visibleProviders = snapshot.providers.filter((provider) => {
    if (isDomainSettingsScope(scope)) return settingsOwner(provider.provider, "enabled") === scope
      || Object.keys(provider.config).some((field) => settingsOwner(provider.provider, "config", field) === scope);
    if (scope === "system") return provider.provider === "runtime";
    if (scope === "layout") return provider.provider === "layout";
    return provider.provider !== "runtime" && provider.provider !== "layout";
  });
  const visibleAudit = snapshot.audit.filter((item) => visibleProviders.some((provider) => provider.provider === item.target));
  const sharedDependencies = isDomainSettingsScope(scope)
    ? snapshot.providers.filter((item) => domainSettingsDependencies[scope].includes(item.provider)) : [];
  const auditPanel = "__audit";
  const categoryGroups = providerCategories
    .map((category) => ({ category, providers: visibleProviders.filter((provider) => (providerCategoryOf[provider.provider] || "other") === category) }))
    .filter((group) => group.providers.length > 0);
  const categoryPanels: string[] = [...categoryGroups.map((group) => group.category), auditPanel];
  const activeCategory = activePanel === auditPanel
    ? auditPanel
    : categoryGroups.find((group) => group.providers.some((provider) => provider.provider === activePanel))?.category || categoryPanels[0];
  const activeGroupProviders = categoryGroups.find((group) => group.category === activeCategory)?.providers || [];
  const providerPanels = activeGroupProviders.map((provider) => provider.provider);
  const displayedProviders = scope === "providers"
    ? visibleProviders.filter((provider) => provider.provider === activePanel)
    : visibleProviders;
  const showAudit = scope !== "providers" || activePanel === auditPanel;

  function selectProviderPanel(panel: string) {
    setActivePanel(panel);
    if (scope === "providers") {
      const target = new URL(window.location.href);
      target.searchParams.set("provider", panel);
      target.searchParams.delete("field");
      adminNavigate(target);
    }
  }

  function selectCategory(category: string) {
    if (category === auditPanel) { selectProviderPanel(auditPanel); return; }
    const first = categoryGroups.find((group) => group.category === category)?.providers[0];
    if (first) selectProviderPanel(first.provider);
  }

  function categoryLabel(category: string) {
    return category === auditPanel ? t("providerTabs.audit") : t(`providerTabs.categories.${category}`);
  }

  function moveTab(event: React.KeyboardEvent<HTMLButtonElement>, index: number, panels: string[], select: (panel: string) => void, idPrefix: string) {
    if (!(["ArrowLeft", "ArrowRight", "Home", "End"] as string[]).includes(event.key)) return;
    event.preventDefault();
    const nextIndex = event.key === "Home" ? 0 : event.key === "End" ? panels.length - 1 : (index + (event.key === "ArrowRight" ? 1 : -1) + panels.length) % panels.length;
    const next = panels[nextIndex];
    select(next);
    requestAnimationFrame(() => document.getElementById(`${idPrefix}-${next}`)?.focus());
  }

  return <div ref={panelRef} className="mt-8 space-y-6">
    <AdminReadOnlyNotice capability="settings.manage" />
    {scope === "providers" && <section className="grid gap-4 rounded-[1.75rem] border border-[var(--line)] bg-[var(--ink)] p-6 text-white md:grid-cols-[auto_1fr] md:items-center"><ShieldCheck size={32} className="text-emerald-200" /><div><h2 className="font-bold">{t("settingsPanel.secretsTitle")}</h2><p className="mt-1 text-sm leading-6 text-white/70">{t("settingsPanel.secretsHint", { source: snapshot.encryption_source })}</p></div></section>}
    {notice && <p role="status" className="flex items-center gap-2 rounded-xl bg-emerald-50 p-4 text-sm text-emerald-800"><Check size={17} />{notice}</p>}
    {actionError && <p role="alert" className="rounded-xl bg-red-50 p-4 text-sm text-red-800">{actionError}</p>}
    {conflictProvider && <button type="button" onClick={reloadConflict} disabled={Boolean(busyProvider)} className="min-h-11 rounded-xl border border-[var(--line)] px-4 py-3 font-semibold">{copy.reload}</button>}
    {dirty && <p role="status" className="rounded-xl border border-amber-300 bg-amber-50 p-4 text-sm text-amber-900">{copy.unsaved}</p>}
    {sharedDependencies.length > 0 && <section className="rounded-2xl border border-[var(--line)] bg-[var(--paper)] p-5"><h2 className="font-bold">{copy.shared}</h2><ul className="mt-3 grid gap-3 md:grid-cols-2">{sharedDependencies.map((item) => <li key={item.provider} className="rounded-xl border border-[var(--line)] bg-[var(--surface)] p-4"><p className="font-semibold">{item.label} · {item.configured ? copy.configured : copy.missing}</p><p className="mt-1 text-sm text-[var(--muted)]">{item.status_message}</p><Link href={settingsHref("providers", item.provider, Object.keys(item.secrets)[0])} className="mt-2 inline-flex min-h-11 items-center text-sm font-semibold text-[var(--teal)] underline">{copy.scopes.providers}</Link></li>)}</ul></section>}

    {scope === "providers" && <>
      <div className="grid gap-3 md:hidden">
        <label className="block text-sm font-semibold">
          {t("providerTabs.mobileCategoryLabel")}
          <select value={activeCategory} onChange={(event) => selectCategory(event.target.value)} className="mt-2 w-full rounded-xl border border-[var(--line)] bg-white px-3 py-3 font-normal">
            {categoryPanels.map((category) => <option key={category} value={category}>{categoryLabel(category)}</option>)}
          </select>
        </label>
        {activeCategory !== auditPanel && <label className="block text-sm font-semibold">
          {t("providerTabs.mobileLabel")}
          <select value={activePanel || providerPanels[0] || ""} onChange={(event) => selectProviderPanel(event.target.value)} className="mt-2 w-full rounded-xl border border-[var(--line)] bg-white px-3 py-3 font-normal">
            {activeGroupProviders.map((provider) => <option key={provider.provider} value={provider.provider}>{provider.label}</option>)}
          </select>
        </label>}
      </div>
      <div className="hidden md:block">
        <div role="tablist" aria-label={t("providerTabs.categoryLabel")} className="flex gap-2 overflow-x-auto pb-2">
          {categoryPanels.map((category, index) => {
            const selected = category === activeCategory;
            const group = categoryGroups.find((item) => item.category === category);
            const readyCount = group ? group.providers.filter((provider) => provider.status === "ready").length : 0;
            return <button key={category} id={`provider-category-tab-${category}`} type="button" role="tab" aria-selected={selected} tabIndex={selected ? 0 : -1} onClick={() => selectCategory(category)} onKeyDown={(event) => moveTab(event, index, categoryPanels, selectCategory, "provider-category-tab")} className={`flex shrink-0 items-center gap-2 rounded-full border px-4 py-2 text-sm font-semibold transition ${selected ? "border-[var(--teal)] bg-[var(--teal)] text-white" : "border-[var(--line)] bg-white text-[var(--ink)] hover:border-[var(--teal)]"}`}>{categoryLabel(category)}{group && <span className={`rounded-full px-2 py-0.5 text-xs tabular-nums ${selected ? "bg-white/20" : "bg-[var(--paper)] text-[var(--muted)]"}`}>{readyCount}/{group.providers.length}</span>}</button>;
          })}
        </div>
        {activeCategory !== auditPanel && <div role="tablist" aria-label={t("providerTabs.label")} className="mt-3 flex gap-2 overflow-x-auto border-t border-[var(--line)] pb-2 pt-3">
          {activeGroupProviders.map((provider, index) => {
            const panel = provider.provider;
            const selected = panel === activePanel;
            return <button key={panel} id={`provider-tab-${panel}`} type="button" role="tab" aria-selected={selected} aria-controls={`provider-panel-${panel}`} tabIndex={selected ? 0 : -1} onClick={() => selectProviderPanel(panel)} onKeyDown={(event) => moveTab(event, index, providerPanels, selectProviderPanel, "provider-tab")} className={`flex shrink-0 items-center gap-2 rounded-xl border px-3.5 py-2 text-sm font-semibold transition ${selected ? "border-[var(--ink)] bg-[var(--ink)] text-white" : "border-[var(--line)] bg-white text-[var(--ink)] hover:border-[var(--ink)]"}`}><span aria-hidden="true" className={`h-2 w-2 rounded-full ${provider.status === "ready" ? "bg-emerald-400" : provider.status === "disabled" ? "bg-slate-300" : "bg-amber-400"}`} />{provider.label}</button>;
          })}
        </div>}
      </div>
    </>}

    <div className="grid gap-6">{displayedProviders.map((provider) => {
      const draft = drafts[provider.provider];
      const busy = busyProvider === provider.provider;
      const usage = provider.usage;
      const internal = provider.provider === "runtime" || provider.provider === "layout";
      const canEnable = hasEnableToggle(provider.provider) && settingsOwner(provider.provider, "enabled") === scope;
      const configFields = visibleConfigFields(provider, draft).filter((field) => settingsOwner(provider.provider, "config", field) === scope);
      const deepField = linkedField ?? (typeof window !== "undefined" ? new URLSearchParams(window.location.search).get("field") : null);
      if (deepField && deepField in provider.config && settingsOwner(provider.provider, "config", deepField) === scope && !configFields.includes(deepField)) configFields.push(deepField);
      const secretFields = Object.entries(provider.secrets).filter(([field]) => settingsOwner(provider.provider, "secret", field) === scope);
      const references = [
        ...Object.keys(provider.config).filter((field) => settingsOwner(provider.provider, "config", field) !== scope).map((field) => ({ field, owner: settingsOwner(provider.provider, "config", field), value: String(provider.config[field] ?? "—") })),
        ...Object.entries(provider.secrets).filter(([field]) => settingsOwner(provider.provider, "secret", field) !== scope).map(([field, secret]) => ({ field, owner: settingsOwner(provider.provider, "secret", field), value: secret.configured ? copy.configured : copy.missing })),
        ...(hasEnableToggle(provider.provider) && !canEnable ? [{ field: "enabled", owner: settingsOwner(provider.provider, "enabled"), value: provider.enabled ? t("settingsPanel.enable") : t("settingsPanel.statusDisabled") }] : []),
      ];
      const changes = ownedChanges(draft, scope);
      const changed = Object.keys(changes.config).length > 0 || Object.keys(changes.secrets).length > 0 || changes.enabled !== undefined;
      const editable = canEnable || configFields.length > 0 || secretFields.length > 0;
      return <section key={provider.provider} id={scope === "providers" ? `provider-panel-${provider.provider}` : undefined} role={scope === "providers" ? "tabpanel" : undefined} aria-labelledby={scope === "providers" ? `provider-tab-${provider.provider}` : undefined} className="rounded-[1.75rem] border border-[var(--line)] bg-white p-5 shadow-sm md:p-7">
        <div data-settings-provider={provider.provider} className="flex flex-wrap items-start justify-between gap-4"><div className="max-w-2xl"><div className="flex flex-wrap items-center gap-2"><h2 tabIndex={-1} className="text-xl font-bold">{provider.label}</h2><span className={`rounded-full px-2.5 py-1 text-xs font-semibold ${statusClass(provider.status)}`}>{provider.status === "ready" ? t("settingsPanel.statusReady") : provider.status === "disabled" ? t("settingsPanel.statusDisabled") : provider.status === "test_required" ? t("settingsPanel.statusTestRequired") : provider.status === "unverified" ? t("settingsPanel.statusUnverified") : provider.status === "error" ? t("settingsPanel.statusError") : t("settingsPanel.statusPending")}</span></div><p className="mt-2 text-sm leading-6 text-[var(--muted)]">{provider.description}</p><p className="mt-1 text-xs font-semibold text-[var(--teal)]">{provider.status_message}</p>{!internal && <p className="mt-2 text-xs text-[var(--muted)]">{t("settingsPanel.recentCalls", { requests: provider.requests_24h || 0, errors: provider.errors_24h || 0 })}{provider.last_error_at ? t("settingsPanel.lastFailure", { time: dateTime.format(new Date(provider.last_error_at)) }) : ""}</p>}</div>{canEnable && <label data-settings-provider={provider.provider} data-settings-field="enabled" className="flex min-h-11 items-center gap-2 rounded-full bg-[var(--paper)] px-4 py-2 text-sm font-semibold"><input type="checkbox" disabled={busy || !manage.allowed} title={!manage.allowed ? manage.disabledReason : undefined} checked={draft.enabled} onChange={(event) => patchDraft(provider.provider, { enabled: event.target.checked })} />{t("settingsPanel.enable")}</label>}</div>

        {references.length > 0 && <div className="mt-4 space-y-2">{Array.from(new Set(references.map((item) => item.owner))).map((owner) => <details key={owner} open={references.some((item) => item.owner === owner && item.field === deepField)} className="rounded-xl border border-[var(--line)] bg-[var(--paper)] px-4"><summary className="min-h-11 cursor-pointer py-3 text-sm font-semibold">{copy.managedIn} {copy.scopes[owner]} · {references.filter((item) => item.owner === owner).length}</summary><ul className="divide-y divide-[var(--line)] pb-3">{references.filter((item) => item.owner === owner).map((item) => <li key={item.field} data-settings-provider={provider.provider} data-settings-field={item.field} className="flex flex-wrap items-center justify-between gap-x-4 py-2 text-sm"><span className="min-w-0 break-words">{item.field === "enabled" ? t("settingsPanel.enable") : item.field in provider.secrets ? secretMeta(t, item.field).label : provider.provider === "layout" ? t(`layout.fields.${item.field}.label`) : fieldMeta[item.field]?.localized ? t(`providerFields.${item.field}.label`) : fieldMeta[item.field]?.label || item.field} · {item.value}</span><Link href={settingsHref(owner, provider.provider, item.field)} className="inline-flex min-h-11 shrink-0 items-center font-semibold text-[var(--teal)] underline">{copy.scopes[owner]}</Link></li>)}</ul></details>)}</div>}

        {provider.provider === "google_maps" && usage && <GoogleUsagePanel usage={usage} refreshing={usageRefreshing} onRefresh={refreshUsage} />}
        {provider.provider === "naver_maps" && usage && <NaverUsagePanel usage={usage} refreshing={usageRefreshing} onRefresh={refreshUsage} />}
        {provider.provider === "navitime" && usage && <NavitimeUsagePanel usage={usage} refreshing={usageRefreshing} onRefresh={refreshUsage} />}
        {provider.provider === "ekispert" && usage && <EkispertUsagePanel usage={usage} refreshing={usageRefreshing} onRefresh={refreshUsage} />}
        {provider.provider === "odsay" && usage && <OdsayUsagePanel usage={usage} refreshing={usageRefreshing} onRefresh={refreshUsage} />}
        {provider.provider === "youtube_guides" && usage && <YouTubeUsagePanel usage={usage} automaticSearchBudget={Number(provider.config.hotspot_guide_youtube_daily_search_budget || 80)} refreshing={usageRefreshing} onRefresh={refreshUsage} />}

        <fieldset disabled={busy || !manage.allowed} title={!manage.allowed ? manage.disabledReason : undefined} className="min-w-0 disabled:opacity-70">
        {configFields.length > 0 && <div className="mt-6 grid gap-4 md:grid-cols-2">{configFields.map((field) => {
          const meta: FieldMeta = fieldMeta[field] || {};
          const label = field === "catalog_review_max_calls" ? budgetCopy.settingLabel : provider.provider === "layout" ? t(`layout.fields.${field}.label`) : meta.localized ? t(`providerFields.${field}.label`) : meta.label || field;
          const help = field === "catalog_review_max_calls" ? budgetCopy.settingHelp : field === "klook_affiliate_id" ? affiliateCopy.noApi : provider.provider === "layout" ? t(`layout.fields.${field}.help`) : meta.localized ? optionalMessage(t, `providerFields.${field}.help`) : meta.help;
          const sourceBadge = provider.config_sources[field] === "database" ? t("settingsPanel.sourceDatabase") : t("settingsPanel.sourceEnvironment");
          if (meta.type === "boolean") return <label key={field} data-settings-provider={provider.provider} data-settings-field={field} className="flex min-h-11 items-start gap-3 rounded-2xl border border-[var(--line)] bg-[var(--paper)] p-4 md:col-span-2"><input type="checkbox" role="switch" checked={draft.config[field] === "true"} onChange={(event) => patchConfig(provider.provider, field, String(event.target.checked))} className="mt-1" /><span><span className="font-semibold">{label}</span><span className="ml-2 text-xs font-normal text-[var(--muted)]">{sourceBadge}</span>{help && <span className="mt-1 block text-xs font-normal leading-5 text-[var(--muted)]">{help}</span>}</span></label>;
          const value = draft.config[field];
          const serverOptions = provider.field_options?.[field];
          const options = serverOptions?.length ? [...(meta.emptyOption ? [{ value: "", label: t(`providerFields.${meta.emptyOption}`) }] : []), ...serverOptions] : meta.options;
          const custom = Boolean(options && meta.allowCustom && (draft.customFields.includes(field) || !options.some((option) => option.value === value)));
          const selected = options?.find((option) => option.value === value);
          const budgetField = field === "catalog_review_max_calls";
          return <div key={field} data-settings-provider={provider.provider} data-settings-field={field} className="text-sm font-semibold"><label className="block">{label}<span className="ml-2 text-xs font-normal text-[var(--muted)]">{sourceBadge}</span>{options ? <select value={custom ? customOption : value} onChange={(event) => selectOption(provider.provider, field, event.target.value)} className="mt-2 w-full rounded-xl border border-[var(--line)] bg-white px-3 py-3 font-normal">{options.map((option) => <option key={option.value} value={option.value}>{option.label ?? t(`providerFields.${field}.options.${option.value}`)}</option>)}{meta.allowCustom && <option value={customOption}>{t("providerFields.custom")}</option>}</select> : <input type={meta.type || "text"} step={budgetField ? 1 : meta.type === "number" ? "any" : undefined} min={budgetField ? 1 : undefined} max={budgetField ? 1000 : undefined} aria-describedby={budgetField ? "catalog-review-call-limit-help" : undefined} aria-invalid={budgetField && !validCatalogCallLimit(Number(value)) ? true : undefined} value={value} onChange={(event) => patchConfig(provider.provider, field, event.target.value)} className="mt-2 w-full rounded-xl border border-[var(--line)] px-3 py-3 font-normal" />}</label>{custom && <input type="text" value={value} onChange={(event) => patchConfig(provider.provider, field, event.target.value)} aria-label={t("providerFields.customInputLabel", { field: label })} placeholder={t("providerFields.customPlaceholder")} className="mt-2 w-full rounded-xl border border-[var(--line)] px-3 py-3 font-mono text-sm font-normal" />}{help && <span id={budgetField ? "catalog-review-call-limit-help" : undefined} className="mt-1 block text-xs font-normal text-[var(--muted)]">{help}</span>}{selected?.description && <span className="mt-1 block text-xs font-normal text-[var(--muted)]">{selected.description}</span>}</div>;
        })}</div>}

        {secretFields.length > 0 && <div className="mt-6"><h3 className="flex items-center gap-2 text-sm font-bold"><KeyRound size={16} className="text-[var(--teal)]" />{t("settingsPanel.secretsHeading")}</h3><div className="mt-3 grid gap-4 md:grid-cols-2">{secretFields.map(([field, secret]) => { const meta = secretMeta(t, field); const clearing = draft.clearSecrets.includes(field); return <div key={field} data-settings-provider={provider.provider} data-settings-field={field} className="rounded-2xl bg-[var(--paper)] p-4"><label className="text-sm font-semibold">{meta.label}<input type="password" autoComplete="off" value={draft.secrets[field]} onChange={(event) => patchSecret(provider.provider, field, event.target.value)} placeholder={secret.masked || t("settingsPanel.secretPlaceholder")} className="mt-2 w-full rounded-xl border border-[var(--line)] bg-white px-3 py-3 font-mono text-sm font-normal" /></label><div className="mt-2 flex items-center justify-between gap-3 text-xs text-[var(--muted)]"><span className="flex items-center gap-1"><EyeOff size={13} />{clearing ? t("settingsPanel.clearAfterSave") : sourceName(t, secret.source)}</span>{secret.source === "database" && !clearing && <button type="button" onClick={() => clearSecret(provider.provider, field)} className="flex min-h-11 items-center gap-1 font-semibold text-red-700"><Trash2 size={13} />{t("settingsPanel.clear")}</button>}</div>{meta.help && <p className="mt-2 text-xs leading-5 text-[var(--muted)]">{meta.help}</p>}</div>; })}</div></div>}
        </fieldset>

        {editable && <div className="mt-6 flex flex-wrap items-center gap-3"><button type="button" onClick={() => save(provider)} disabled={!manage.allowed || Boolean(busyProvider) || !changed} title={!manage.allowed ? manage.disabledReason : undefined} className="flex min-h-11 items-center gap-2 rounded-xl bg-[var(--teal)] px-5 py-3 text-sm font-semibold text-white disabled:opacity-50">{busy ? <LoaderCircle size={16} className="animate-spin" /> : <Save size={16} />}{t("settingsPanel.saveSettings")}</button>{!internal && scope === "providers" && <button type="button" onClick={() => testConnection(provider)} disabled={!manage.allowed || Boolean(busyProvider) || isDraftDirty(draft) || (hasEnableToggle(provider.provider) && !draft.enabled)} title={!manage.allowed ? manage.disabledReason : undefined} className="flex min-h-11 items-center gap-2 rounded-xl border border-[var(--line)] px-5 py-3 text-sm font-semibold disabled:opacity-40"><PlugZap size={16} />{t("settingsPanel.testConnection")}</button>}{secretFields.length > 0 && <span className="text-xs text-[var(--muted)]">{t("settingsPanel.blankKeyHint")}</span>}</div>}
        {provider.last_tested_at && <p className={`mt-4 rounded-xl px-4 py-3 text-sm ${statusClass(provider.last_test_status || "")}`}>{t("settingsPanel.lastTest", { time: dateTime.format(new Date(provider.last_tested_at)), message: provider.last_test_message ?? "" })}</p>}
      </section>;
    })}</div>

    {showAudit && <section id={scope === "providers" ? `provider-panel-${auditPanel}` : undefined} role={scope === "providers" ? "tabpanel" : undefined} aria-labelledby={scope === "providers" ? `provider-category-tab-${auditPanel}` : undefined} className="rounded-[1.75rem] border border-[var(--line)] bg-white p-5 md:p-7"><h2 className="text-xl font-bold">{t("settingsPanel.auditTitle")}</h2><p className="mt-1 text-sm text-[var(--muted)]">{scope === "system" ? t("settingsPanel.auditSystemHint") : scope === "layout" ? t("layout.auditDescription") : t("settingsPanel.auditProviderHint")}</p>{visibleAudit.length ? <ol className="mt-5 divide-y divide-[var(--line)]">{visibleAudit.map((item) => <li key={item.id} className="grid gap-1 py-3 text-sm md:grid-cols-[10rem_1fr_auto]"><time className="text-[var(--muted)]">{dateTime.format(new Date(item.created_at))}</time><span className="font-semibold">{item.action === "layout_settings_updated" ? t("layout.auditAction") : auditActionName(t, item.action)} · {item.target}</span><code className="text-xs text-[var(--muted)]">{auditSummary(item.metadata)}</code></li>)}</ol> : <p className="mt-5 rounded-xl bg-[var(--paper)] p-5 text-sm text-[var(--muted)]">{t("settingsPanel.auditEmpty")}</p>}</section>}
  </div>;
}
