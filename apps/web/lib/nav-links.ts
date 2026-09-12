import type { SiteFeature } from "@/lib/site-features";

// One list for every navigation surface. The desktop header, the mobile menu
// sheet and the bottom tab bar must never disagree about what this site has.
export const primaryNavLinks: Array<{
  key: "guides" | "life" | "hotspots" | "foods" | "trips" | "alerts" | "flightStatus" | "airlines" | "pricing";
  href: string;
  feature?: SiteFeature;
}> = [
  // No `feature`: the guides section is first-party content with no provider cost and
  // no switch behind it, so it must not disappear when a catalog module is closed.
  { key: "guides", href: "/guides" },
  // The lifestyle section shares the guides' article system and the same reasoning: first-party
  // content, no switch. The community surfaces that render this list as "travel tools" filter
  // it out themselves, because it is the one entry here that is not about travel.
  { key: "life", href: "/life" },
  { key: "hotspots", href: "/hotspots", feature: "hotspots" },
  { key: "foods", href: "/foods" },
  { key: "trips", href: "/trips", feature: "trips" },
  { key: "alerts", href: "/alerts", feature: "alerts" },
  { key: "flightStatus", href: "/flights/status", feature: "flight_status" },
  { key: "airlines", href: "/labs/airlines", feature: "airline_fares" },
  { key: "pricing", href: "/pricing", feature: "pricing" },
];
