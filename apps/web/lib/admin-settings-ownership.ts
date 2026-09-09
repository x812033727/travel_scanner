export type AdminSettingsScope = "providers" | "system" | "layout" | "hotspots" | "foods" | "hotels";
export type SettingsFieldKind = "config" | "secret" | "enabled";

// Explicit ownership keeps new, unknown fields in their shared management scope.
const domainConfig: Record<string, { owner: AdminSettingsScope; fields: readonly string[] }> = {
  layout: { owner: "hotspots", fields: ["hotspots_enabled"] },
  runtime: { owner: "hotels", fields: ["hotel_provider_mode"] },
  hotspot_guides: { owner: "hotspots", fields: ["hotspot_guide_backfill_enabled", "hotspot_guide_backfill_batch_size", "hotspot_guide_backfill_locale"] },
  ai_guide_search: { owner: "hotspots", fields: ["hotspot_guide_ai_default_provider", "hotspot_guide_ai_openai_model", "hotspot_guide_ai_anthropic_model", "hotspot_guide_ai_minimax_model", "hotspot_guide_ai_gemini_model", "hotspot_guide_ai_timeout_seconds", "hotspot_guide_ai_max_output_tokens", "hotspot_guide_ai_daily_run_limit", "hotspot_guide_ai_daily_call_budget"] },
  hotspot_intros: { owner: "hotspots", fields: ["hotspot_intro_ai_default_provider", "hotspot_intro_ai_openai_model", "hotspot_intro_ai_anthropic_model", "hotspot_intro_ai_minimax_model", "hotspot_intro_ai_gemini_model", "hotspot_intro_ai_timeout_seconds", "hotspot_intro_ai_max_output_tokens", "hotspot_intro_ai_daily_run_limit", "hotspot_intro_ai_daily_call_budget"] },
  booking_demand: { owner: "hotels", fields: ["booking_demand_env", "booking_demand_api_base_url", "booking_demand_affiliate_id", "booking_booker_country", "booking_language", "booking_location_cache_ttl_seconds"] },
  travelpayouts: { owner: "hotels", fields: ["travelpayouts_hotel_target_url"] },
};

export function settingsOwner(provider: string, kind: SettingsFieldKind, field?: string): AdminSettingsScope {
  if (kind === "secret") return "providers";
  if (kind === "enabled") {
    if (["hotspot_guides", "ai_guide_search", "hotspot_intros"].includes(provider)) return "hotspots";
    if (provider === "booking_demand") return "hotels";
  }
  if (kind === "config" && field) {
    if (provider === "google_maps" && field.startsWith("restaurant_")) return "foods";
    const entry = domainConfig[provider];
    if (entry?.fields.includes(field)) return entry.owner;
  }
  return provider === "runtime" ? "system" : provider === "layout" ? "layout" : "providers";
}

export function settingsHref(scope: AdminSettingsScope, provider: string, field?: string): string {
  const domain = isDomainSettingsScope(scope);
  const pathname = domain ? `/admin/${scope}` : scope === "providers" ? "/admin/settings" : `/admin/${scope}-settings`;
  const params = new URLSearchParams(domain ? { tab: "settings", provider } : { provider });
  if (scope === "hotels") params.set("section", "providers");
  if (field) params.set("field", field);
  return `${pathname}?${params}`;
}

export function isDomainSettingsScope(scope: AdminSettingsScope): scope is "hotspots" | "foods" | "hotels" {
  return scope === "hotspots" || scope === "foods" || scope === "hotels";
}

export const domainSettingsDependencies: Record<"hotspots" | "foods" | "hotels", readonly string[]> = {
  hotspots: ["ai_vendors", "gemini_guides", "google_maps", "youtube_guides", "brave_guides"],
  foods: ["google_maps", "ai_vendors"],
  hotels: ["booking_demand", "travelpayouts", "amadeus"],
};
