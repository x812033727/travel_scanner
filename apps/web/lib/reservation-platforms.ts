/**
 * Reviewed reservation providers, in a fixed display order independent of fees.
 * Keep the accepted URL shapes in sync with app/foods/platform_links.py.
 * Recognizing a URL does not verify that it belongs to the merchant.
 */
export const reservationPlatformDefinitions: readonly {
  provider: string;
  label: string;
  hosts: readonly string[];
}[] = [
  { provider: "tablecheck", label: "TableCheck", hosts: ["tablecheck.com", "www.tablecheck.com"] },
  { provider: "catchtable_global", label: "Catchtable Global", hosts: ["catchtable.net", "www.catchtable.net"] },
  { provider: "eztable", label: "EZTABLE", hosts: ["eztable.com", "www.eztable.com"] },
  { provider: "chope", label: "Chope", hosts: ["chope.co", "www.chope.co"] },
  { provider: "openrice", label: "OpenRice", hosts: ["openrice.com", "www.openrice.com"] },
  { provider: "hungry_hub", label: "Hungry Hub", hosts: ["hungryhub.com", "www.hungryhub.com", "web.hungryhub.com"] },
  { provider: "pasgo", label: "PasGo", hosts: ["pasgo.vn", "www.pasgo.vn"] },
  { provider: "inline", label: "inline", hosts: ["inline.app"] },
  { provider: "maifood", label: "Maifood", hosts: ["reservation.maifood.com.tw"] },
  { provider: "sevenrooms", label: "SevenRooms", hosts: ["sevenrooms.com", "www.sevenrooms.com"] },
  { provider: "ikyu", label: "一休", hosts: ["restaurant.ikyu.com"] },
  { provider: "myconcierge", label: "My Concierge Japan", hosts: ["myconciergejapan.com", "www.myconciergejapan.com"] },
];

const localePattern = /^(?:en|ja|ko|zh-(?:tw|cn|hk|hant|hans)|th|vi)$/i;
const forbiddenSlugs = new Set([
  "search", "ranking", "rankings", "discovery", "explore", "restaurants",
  "list_of_restaurants", "reserve", "reservations", "shops", "restaurant", "booking", "branches",
]);
const merchantSlug = (value: string | undefined): value is string => Boolean(
  value && /^[A-Za-z0-9][A-Za-z0-9_-]*$/.test(value) && !forbiddenSlugs.has(value.toLowerCase()),
);

function merchantIdentity(provider: string, segments: string[]): string | undefined {
  const hasLocale = ["tablecheck", "catchtable_global", "eztable", "chope", "openrice", "hungry_hub", "myconcierge"].includes(provider)
    && localePattern.test(segments[0] ?? "");
  const path = hasLocale ? segments.slice(1) : segments;
  const lower = path.map((part) => part.toLowerCase());
  const venue = (index: number) => merchantSlug(path[index]) ? path[index] : undefined;
  switch (provider) {
    case "tablecheck":
      if (path.length === 3 && lower[0] === "shops" && lower[2] === "reserve") return venue(1);
      if (hasLocale && path.length === 3 && lower[1] === "reserve" && ["message", "landing"].includes(lower[2])) return venue(0);
      return undefined;
    case "catchtable_global":
      return path.length === 2 && ["shop", "restaurant", "restaurants"].includes(lower[0]) ? venue(1) : undefined;
    case "eztable":
      return path.length === 2 && ["restaurant", "restaurants"].includes(lower[0]) ? venue(1) : undefined;
    case "chope":
      return path.length === 3 && /^[a-z]+(?:-[a-z]+)*-restaurants$/.test(lower[0]) && lower[1] === "restaurant" && venue(2)
        ? `${lower[0]}/${path[2]}` : undefined;
    case "openrice": {
      if (!hasLocale || path.length !== 2 || !/^[a-z][a-z-]*$/i.test(path[0])) return undefined;
      const match = /^[pr]-[\p{L}\p{N}_-]+-([pr]\d+)$/iu.exec(path[1]);
      return match ? `${lower[0]}/${match[1].toLowerCase()}` : undefined;
    }
    case "hungry_hub":
      return (path.length === 2 || (path.length === 3 && lower[2] === "web")) && lower[0] === "restaurants" ? venue(1) : undefined;
    case "pasgo":
      return !hasLocale && path.length === 2 && lower[0] === "nha-hang" ? venue(1) : undefined;
    case "inline":
      return !hasLocale && path.length === 3 && lower[0] === "booking"
        && /^[-A-Za-z0-9_]+:[-A-Za-z0-9_]+$/.test(path[1]) && /^[-A-Za-z0-9_]+$/.test(path[2])
        && !forbiddenSlugs.has(lower[2])
        ? `${path[1]}/${path[2]}` : undefined;
    case "maifood":
      return !hasLocale && path.length === 2 && venue(0) && venue(1)
        ? `${path[0]}/${path[1]}` : undefined;
    case "sevenrooms":
      if (!hasLocale && path.length === 2 && lower[0] === "reservations") return venue(1);
      return !hasLocale && path.length === 5 && lower[0] === "explore" && lower[2] === "reservations" && lower[3] === "create" && lower[4] === "search"
        ? venue(1) : undefined;
    case "ikyu":
      return !hasLocale && path.length === 1 && /^\d+$/.test(path[0]) ? path[0] : undefined;
    case "myconcierge":
      return path.length === 2 && lower[0] === "restaurants" ? venue(1) : undefined;
    default:
      return undefined;
  }
}

function reservationPlatformUrl(provider: string, value: string | null | undefined) {
  // Inspect the original authority and path before URL can erase an explicit :443,
  // turn backslashes into slashes, trim controls, or collapse dot segments.
  if (typeof value !== "string" || value.length > 2048 || /[\u0000-\u0020\u007f-\u009f\\]/.test(value)
    || /%(?![\da-f]{2})|%(?:2f|5c|25)/i.test(value)) return undefined;
  const definition = reservationPlatformDefinitions.find((item) => item.provider === provider);
  const raw = /^https:\/\/([^/?#]+)(\/[^?#]*)?(?:\?([^#]*))?$/i.exec(value);
  if (!definition || !raw || !definition.hosts.includes(raw[1].toLowerCase())) return undefined;
  const path = (raw[2] ?? "").replace(/\/$/, "");
  if (!path || path.includes("//")) return undefined;
  let decodedPath: string;
  try {
    decodedPath = decodeURIComponent(path);
  } catch {
    return undefined;
  }
  if (/[\u0000-\u0020\u007f-\u009f\\%]/.test(decodedPath)) return undefined;
  const segments = decodedPath.slice(1).split("/");
  if (segments.some((part) => !part || part === "." || part === "..")) return undefined;
  const identity = merchantIdentity(provider, segments);
  if (!identity) return undefined;
  const query = raw[3];
  // Inline's documented language choice is the only accepted query parameter.
  // Unknown query strings are rejected, never stripped from an identity-bearing URL.
  if (query !== undefined && (provider !== "inline" || !/^language=[A-Za-z-]+$/.test(query)
    || !localePattern.test(query.slice("language=".length)))) return undefined;
  const href = `https://${raw[1].toLowerCase()}${path}${query !== undefined ? `?${query}` : ""}`;
  return { href, identity: `${provider}:${identity}` };
}

export function reservationPlatformHref(provider: string, value: string | null | undefined): string | undefined {
  return reservationPlatformUrl(provider, value)?.href;
}

/** The same branch remains the same identity across reviewed locale and URL variants. */
export function reservationPlatformIdentity(provider: string, value: string | null | undefined): string | undefined {
  return reservationPlatformUrl(provider, value)?.identity;
}
