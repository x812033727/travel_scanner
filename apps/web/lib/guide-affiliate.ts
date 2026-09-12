import type { AffiliateModule } from "@/components/affiliate-partner-options";
import { serviceDiscoveryDestinations } from "@/lib/travel-service-discovery";

/**
 * Which partner modules an article may end with, decided by its topics.
 *
 * An explicit allowlist rather than "everything": a flight or hotel button under an
 * etiquette or safety article is exactly the non-contextual placement the catalog rules
 * avoid, and the reader is one click from the all-modules city page anyway. Topics that
 * have no honest module (entry rules, packing, budget, etiquette, safety, food, shopping,
 * nightlife) and slugs an editor added later contribute nothing.
 */
const TOPIC_MODULES: Readonly<Record<string, AffiliateModule>> = {
  connectivity: "connectivity",
  hotel: "hotel",
  transport: "transport",
  deal: "flight",
  itinerary: "activities",
  season: "activities",
  family: "activities",
  nature: "activities",
  culture: "activities",
  viewpoint: "activities",
  beach: "activities",
};

/** Fixed canonical order, the same one the destination panel uses, never commission-shaped. */
const MODULE_ORDER: readonly AffiliateModule[] = ["flight", "hotel", "activities", "transport", "connectivity"];

export function guideAffiliateModules(topics: ReadonlyArray<{ slug: string }>): AffiliateModule[] {
  const wanted = new Set(topics.map((topic) => TOPIC_MODULES[topic.slug]).filter(Boolean));
  return MODULE_ORDER.filter((module) => wanted.has(module));
}

/** The catalog destination an article's offers belong to; null for cross-destination articles. */
export function guideAffiliateDestination(destinationId: string | null): string | null {
  if (!destinationId) return null;
  return serviceDiscoveryDestinations([destinationId])[0] ?? null;
}
