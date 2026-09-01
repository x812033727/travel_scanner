export const siteFeatureKeys = [
  "hotspots",
  "trips",
  "alerts",
  "flight_status",
  "airline_fares",
  "pricing",
] as const;

export type SiteFeature = (typeof siteFeatureKeys)[number];
export type SiteVisibility = Record<`${SiteFeature}_enabled`, boolean>;
export type SiteVisibilityState = {
  status: "ready" | "unavailable";
  features: SiteVisibility;
};

export const openSiteVisibility: SiteVisibility = {
  hotspots_enabled: true,
  trips_enabled: true,
  alerts_enabled: true,
  flight_status_enabled: true,
  airline_fares_enabled: true,
  pricing_enabled: true,
};

export const closedSiteVisibility: SiteVisibility = {
  hotspots_enabled: false,
  trips_enabled: false,
  alerts_enabled: false,
  flight_status_enabled: false,
  airline_fares_enabled: false,
  pricing_enabled: false,
};

export function featureEnabled(state: SiteVisibilityState, feature: SiteFeature) {
  return state.status === "ready" && state.features[`${feature}_enabled`];
}
