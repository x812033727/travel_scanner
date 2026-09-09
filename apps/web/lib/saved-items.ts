export type SavedType = "hotspot" | "food" | "restaurant" | "merchant" | "service" | "guide" | "post";
export type SavedContentItem = { id: string; title: string; kind?: string; type?: string; collection_ref?: { kind: string; id: string } | null };
export type SavedState = { key: string; saved: boolean; collection_ids: string[] };
const aliases: Record<string, SavedType> = { hotspot: "hotspot", food: "food", restaurant: "restaurant", merchant: "merchant", service: "service", hotel: "service", guide: "guide", article: "guide", video: "guide", post: "post", itinerary: "post" };
export function savedReference(type: string, id: string): { type: SavedType; id: string; key: string } | null {
  const canonical = aliases[type];
  if (!canonical || !id) return null;
  const lower = id.toLowerCase();
  const hex = lower.replaceAll("-", "");
  const normalized = canonical === "restaurant" ? id : /^(?:[a-f0-9]{32}|[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})$/.test(lower)
    ? `${hex.slice(0, 8)}-${hex.slice(8, 12)}-${hex.slice(12, 16)}-${hex.slice(16, 20)}-${hex.slice(20)}` : lower;
  return { type: canonical, id: normalized, key: `${canonical}:${normalized}` };
}
export function contentSavedReference(item: SavedContentItem) {
  if (item.collection_ref) return savedReference(item.collection_ref.kind, item.collection_ref.id);
  const prefix = item.id.slice(0, item.id.indexOf(":"));
  return savedReference(item.type || item.kind || prefix, aliases[prefix] ? item.id.slice(item.id.indexOf(":") + 1) : item.id);
}
export function parseSavedKey(key: string) {
  const split = key.indexOf(":");
  return split > 0 ? savedReference(key.slice(0, split), key.slice(split + 1)) : null;
}
