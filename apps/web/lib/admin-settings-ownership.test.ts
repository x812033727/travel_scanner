import { describe, expect, it } from "vitest";
import { adminSettingsCopy } from "./admin-settings-copy";
import { settingsHref, settingsOwner, type AdminSettingsScope } from "./admin-settings-ownership";

describe("single-owner provider settings registry", () => {
  it.each([
    ["layout", "hotspots_enabled", "hotspots"],
    ["runtime", "hotel_provider_mode", "hotels"],
    ["hotspot_guides", "hotspot_guide_backfill_batch_size", "hotspots"],
    ["ai_guide_search", "hotspot_guide_ai_default_provider", "hotspots"],
    ["hotspot_intros", "hotspot_intro_ai_daily_call_budget", "hotspots"],
    ["google_maps", "restaurant_aggregate_monthly_budget", "foods"],
    ["google_maps", "restaurant_scan_enabled", "foods"],
    ["google_maps", "restaurant_future_setting", "foods"],
    ["booking_demand", "booking_demand_env", "hotels"],
    ["travelpayouts", "travelpayouts_hotel_target_url", "hotels"],
    ["travelpayouts", "travelpayouts_marker", "providers"],
    ["google_maps", "google_maps_enterprise_free_limit", "providers"],
    ["gemini_guides", "hotspot_guide_gemini_daily_search_budget", "providers"],
    ["youtube_guides", "hotspot_guide_refresh_days", "providers"],
    ["brave_guides", "hotspot_guide_brave_daily_search_budget", "providers"],
    ["runtime", "flight_provider_mode", "system"],
    ["layout", "trips_enabled", "layout"],
  ])("%s.%s has exactly one owner: %s", (provider, field, owner) => {
    const scopes: AdminSettingsScope[] = ["providers", "system", "layout", "hotspots", "foods", "hotels"];
    expect(scopes.filter((scope) => settingsOwner(provider, "config", field) === scope)).toEqual([owner]);
  });

  it.each(["hotspot_guides", "ai_guide_search", "hotspot_intros", "booking_demand", "google_maps", "ai_vendors", "runtime", "layout"])("keeps every %s secret exclusively in shared providers", (provider) => {
    expect(settingsOwner(provider, "secret", "unknown_secret")).toBe("providers");
  });

  it("moves enable controls without moving shared services or unknown config", () => {
    for (const provider of ["hotspot_guides", "ai_guide_search", "hotspot_intros"]) {
      expect(settingsOwner(provider, "enabled")).toBe("hotspots");
      expect(settingsOwner(provider, "config", "future_field")).toBe("providers");
    }
    expect(settingsOwner("booking_demand", "enabled")).toBe("hotels");
    expect(settingsOwner("booking_demand", "config", "future_field")).toBe("providers");
    for (const provider of ["google_maps", "ai_vendors", "gemini_guides", "amadeus", "youtube_guides", "brave_guides", "travelpayouts", "future_provider"]) {
      expect(settingsOwner(provider, "enabled")).toBe("providers");
    }
  });

  it("builds canonical domain and shared field deep links", () => {
    expect(settingsHref("foods", "google_maps", "restaurant_scan_enabled")).toBe("/admin/foods?tab=settings&provider=google_maps&field=restaurant_scan_enabled");
    expect(settingsHref("providers", "google_maps", "google_maps_api_key")).toBe("/admin/settings?provider=google_maps&field=google_maps_api_key");
    expect(settingsHref("system", "runtime")).toBe("/admin/system-settings?provider=runtime");
    expect(settingsHref("layout", "layout")).toBe("/admin/layout-settings?provider=layout");
    expect(settingsHref("hotels", "booking_demand", "booking_demand_env")).toBe("/admin/hotels?tab=settings&provider=booking_demand&section=providers&field=booking_demand_env");
  });

  it("provides ownership, unsaved and conflict copy in all five locales", () => {
    const locales = ["zh-TW", "zh-CN", "en", "ja", "ko"];
    expect(new Set(locales.map((locale) => adminSettingsCopy(locale).conflict)).size).toBe(5);
    for (const locale of locales) {
      const copy = adminSettingsCopy(locale);
      expect(Object.values(copy.scopes).every(Boolean)).toBe(true);
      expect(copy.leave && copy.unsaved && copy.reload && copy.discard && copy.shared).toBeTruthy();
    }
  });
});
