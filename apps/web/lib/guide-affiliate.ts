import type { AffiliateModule } from "@/components/affiliate-partner-options";
import type { GuideKind } from "@/lib/guides";
import type { HotelBookingPlacement } from "@/lib/hotel-booking-placement";
import { serviceDiscoveryDestinations } from "@/lib/travel-service-discovery";

/**
 * Which partner modules an article may end with, decided by its topics.
 *
 * An explicit allowlist rather than "everything": a flight or hotel button under an
 * etiquette or safety article is exactly the non-contextual placement the catalog rules
 * avoid, and the reader is one click from the all-modules city page anyway. Topics that
 * have no honest module (entry rules, packing, budget, etiquette, safety, food, shopping,
 * nightlife) and slugs an editor added later contribute nothing.
 *
 * The `life` exception: lifestyle topics (AI tools, tutorials, software, gadgets, ...) never
 * map to a travel module, so the table above cannot say anything about a `life` article.
 * There the editor's deliberately filled-in destination is the only contextual signal, and
 * the panel behaves like the city page's own (`destination-guide.tsx`: every module,
 * `placement="city"`): all of `MODULE_ORDER`, under `placement="life"`. Three gates still
 * apply before a button shows: the editor's (a destination is set), the operator's (the
 * `life` placement is off by default) and the article's own (`!expired`). Narrowing it later
 * to, say, `["activities", "transport", "connectivity"]` is a one-line change here.
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
export const MODULE_ORDER: readonly AffiliateModule[] = ["flight", "hotel", "activities", "transport", "connectivity"];

export function guideAffiliateModules(topics: ReadonlyArray<{ slug: string }>, kind: GuideKind): AffiliateModule[] {
  if (kind === "life") return [...MODULE_ORDER];
  const wanted = new Set(topics.map((topic) => TOPIC_MODULES[topic.slug]).filter(Boolean));
  return MODULE_ORDER.filter((module) => wanted.has(module));
}

/** The surface the API gates and records clicks under: `life` for a lifestyle article,
 *  `guide` for either travel kind. Both are off until an operator enables them. */
export function guideAffiliatePlacement(kind: GuideKind): HotelBookingPlacement {
  return kind === "life" ? "life" : "guide";
}

/** The catalog destination an article's offers belong to; null for cross-destination articles. */
export function guideAffiliateDestination(destinationId: string | null): string | null {
  if (!destinationId) return null;
  return serviceDiscoveryDestinations([destinationId])[0] ?? null;
}
