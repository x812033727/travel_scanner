import type { SiteFeature } from "@/lib/site-features";

// One list for every navigation surface. The desktop header, the mobile menu
// sheet and the bottom tab bar must never disagree about what this site has.
export const primaryNavLinks: Array<{
  key: "hotspots" | "foods" | "trips" | "alerts" | "flightStatus" | "airlines" | "pricing";
  href: string;
  feature?: SiteFeature;
}> = [
  { key: "hotspots", href: "/hotspots", feature: "hotspots" },
  { key: "foods", href: "/foods" },
  { key: "trips", href: "/trips", feature: "trips" },
  { key: "alerts", href: "/alerts", feature: "alerts" },
  { key: "flightStatus", href: "/flights/status", feature: "flight_status" },
  { key: "airlines", href: "/labs/airlines", feature: "airline_fares" },
  { key: "pricing", href: "/pricing", feature: "pricing" },
];
