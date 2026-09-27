export type AdminSettingsScope = "providers" | "system" | "layout" | "hotspots" | "foods" | "hotels";
export type SettingsFieldKind = "config" | "secret" | "enabled";

// Explicit ownership keeps new, unknown fields in their shared management scope.
const domainConfig: Record<string, { owner: AdminSettingsScope; fields: readonly string[] }> = {
  layout: { owner: "hotspots", fields: ["hotspots_enabled"] },
  runtime: { owner: "hotels", fields: ["hotel_provider_mode"] },
  hotspot_guides: { owner: "hotspots", fields: ["hotspot_guide_backfill_enabled", "hotspot_guide_backfill_batch_size", "hotspot_guide_backfill_locale"] },
  // The vendor and model fields of these two cards are chosen with every other AI model on the
  // AI settings page; the hotspot settings tab keeps their limits and lists the rest read-only.
  ai_guide_search: { owner: "hotspots", fields: ["hotspot_guide_ai_timeout_seconds", "hotspot_guide_ai_max_output_tokens", "hotspot_guide_ai_daily_run_limit", "hotspot_guide_ai_daily_call_budget"] },
  hotspot_intros: { owner: "hotspots", fields: ["hotspot_intro_ai_timeout_seconds", "hotspot_intro_ai_max_output_tokens", "hotspot_intro_ai_daily_run_limit", "hotspot_intro_ai_daily_call_budget"] },
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

// The AI category of shared providers (vendor keys, feature models, speech) lives on the
// AI settings page next to the host's subscription accounts, not on /admin/settings.
export const AI_SETTINGS_PATH = "/admin/ai-accounts";
// Its "API keys" tab holds the vendor keys and speech; every card that picks a model is on
// its "models" tab, next to the news and video models.
export const AI_KEY_PROVIDERS: readonly string[] = ["ai_vendors", "azure_speech"];
export const AI_MODEL_PROVIDERS: readonly string[] = ["ai_planner", "ai_guide_search", "hotspot_intros", "gemini_guides"];
export const AI_SETTINGS_PROVIDERS: readonly string[] = [...AI_KEY_PROVIDERS, ...AI_MODEL_PROVIDERS];
export type AiSettingsTab = "subscriptions" | "api" | "models";

export function isAiSettingsProvider(provider: string): boolean {
  return AI_SETTINGS_PROVIDERS.includes(provider);
}

/** The AI settings tab that shows a provider card. */
export function aiSettingsTab(provider: string): Exclude<AiSettingsTab, "subscriptions"> {
  return AI_MODEL_PROVIDERS.includes(provider) ? "models" : "api";
}

/** The AI settings page, on the models tab, scrolled to the news or video models. */
export function aiModelsHref(section: "news" | "video"): string {
  return `${AI_SETTINGS_PATH}?${new URLSearchParams({ tab: "models", section })}`;
}

export function settingsHref(scope: AdminSettingsScope, provider: string, field?: string): string {
  if (scope === "providers" && isAiSettingsProvider(provider)) {
    const params = new URLSearchParams({ tab: aiSettingsTab(provider), provider });
    if (field) params.set("field", field);
    return `${AI_SETTINGS_PATH}?${params}`;
  }
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
