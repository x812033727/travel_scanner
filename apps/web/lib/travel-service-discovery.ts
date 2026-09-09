import type { AffiliateModule } from "@/components/affiliate-partner-options";
import { PUBLIC_DESTINATIONS, type Kind } from "@/components/travel-services/options";

const modules: Record<Kind, AffiliateModule> = {
  hotel: "hotel", tour: "activities", transfer: "transport", esim: "connectivity",
};
export function serviceDiscoveryModules(kind: Kind | "all"): AffiliateModule[] {
  return kind === "all" ? Object.values(modules) : [modules[kind]];
}
export function serviceDiscoveryDestinations(destinations: string[]): string[] {
  return [...new Set(destinations.map((destination) =>
    destination === "osaka" || destination === "kyoto" ? "osaka-kyoto" : destination,
  ))].filter((destination) => (PUBLIC_DESTINATIONS as readonly string[]).includes(destination));
}
