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
  // "stale" is a real answer the settings service gave a moment ago, kept because the current
  // read failed. "unavailable" means nothing is known: no read has ever succeeded in this
  // process, or the last one is too old to stand behind.
  status: "ready" | "stale" | "unavailable";
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

// A closed feature must not be indexed, but a settings read that timed out is not a closed
// feature. Answering 200 with `noindex` on a page that is actually open teaches Google the URL
// is noindexed, and it believes that far longer than the outage lasts -- so a stale value the
// service really did return is used, and only a complete absence of knowledge closes the door.
export function featureEnabled(state: SiteVisibilityState, feature: SiteFeature) {
  return state.status !== "unavailable" && state.features[`${feature}_enabled`];
}

// For navigation surfaces only. "unavailable" means the switches could not be
// read, not that the owner closed everything: keep the doors on the map and
// let PublicFeatureGate decide what happens behind each one. Before this, one
// failed settings fetch silently emptied the desktop header and, on a phone,
// the bottom tab bar.
export function featureVisible(state: SiteVisibilityState, feature: SiteFeature) {
  if (state.status === "unavailable") return true;
  return state.features[`${feature}_enabled`];
}
