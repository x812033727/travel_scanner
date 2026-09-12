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
  { provider: "tabelog", label: "食べログ", hosts: ["tabelog.com"] },
  { provider: "hotpepper", label: "ホットペッパーグルメ", hosts: ["www.hotpepper.jp", "hotpepper.jp"] },
  { provider: "gurunavi", label: "ぐるなび", hosts: ["r.gnavi.co.jp", "gurunavi.com"] },
  { provider: "autoreserve", label: "AutoReserve", hosts: ["autoreserve.com"] },
  { provider: "naver_booking", label: "네이버 예약", hosts: ["booking.naver.com", "m.booking.naver.com"] },
];

const localePattern = /^(?:en|ja|ko|zh-(?:tw|cn|hk|hant|hans)|th|vi)$/i;
const forbiddenSlugs = new Set([
  "search", "ranking", "rankings", "discovery", "explore", "restaurants",
  "list_of_restaurants", "reserve", "reservations", "shops", "restaurant", "booking", "branches",
]);
const merchantSlug = (value: string | undefined): value is string => Boolean(
  value && /^[A-Za-z0-9][A-Za-z0-9_-]*$/.test(value) && !forbiddenSlugs.has(value.toLowerCase()),
);
// Catchtable uses literal dots inside venue IDs. A dot segment may start with an
// underscore ("hani._.noodle"); empty segments and a leading dot stay invalid.
const catchtableSlug = (value: string | undefined): value is string => Boolean(
  value && /^[A-Za-z0-9][A-Za-z0-9_-]*(?:\.[A-Za-z0-9_][A-Za-z0-9_-]*)*$/.test(value)
    && !forbiddenSlugs.has(value.toLowerCase()),
);
// Tabelog and Gurunavi name their language directories their own way and serve
// Japanese from the bare path. The remaining IDs are each spelled exactly one way.
const tabelogLocale = /^(?:en|tw|cn|kr|th)$/i;
const gurunaviLocale = /^(?:ja|en|ko|zh-hant|zh-hans)$/i;
const tabelogArea = /^A\d+$/i;
const hotpepperId = /^J\d{9}$/i;
const gurunaviId = /^(?:[a-z]\d{6}|[a-z\d]{12})$/i;
const autoreserveId = /^[A-Za-z0-9]{20}$/;
const digits = /^\d+$/;

function merchantIdentity(provider: string, segments: string[], host: string): string | undefined {
  const hasLocale = ["tablecheck", "catchtable_global", "eztable", "chope", "openrice", "hungry_hub", "myconcierge", "autoreserve"].includes(provider)
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
      return path.length === 2 && ["shop", "restaurant", "restaurants"].includes(lower[0]) && catchtableSlug(path[1])
        ? path[1] : undefined;
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
    case "tabelog": {
      // The prefecture and area codes locate the shop page; the number identifies it.
      const rest = tabelogLocale.test(path[0] ?? "") ? path.slice(1) : path;
      return rest.length === 4 && /^[a-z]+$/i.test(rest[0]) && tabelogArea.test(rest[1])
        && tabelogArea.test(rest[2]) && digits.test(rest[3]) ? rest[3] : undefined;
    }
    case "hotpepper":
      return path.length === 1 && /^str/i.test(path[0]) && hotpepperId.test(path[0].slice(3))
        ? path[0].slice(3).toLowerCase() : undefined;
    case "gurunavi":
      // The Japanese and international sites are separate hosts with different routes.
      if (host === "r.gnavi.co.jp") {
        return path.length === 1 && gurunaviId.test(path[0]) ? path[0].toLowerCase() : undefined;
      }
      return path.length === 3 && gurunaviLocale.test(path[0]) && gurunaviId.test(path[1]) && lower[2] === "rst"
        ? path[1].toLowerCase() : undefined;
    case "autoreserve":
      return hasLocale && path.length === 2 && lower[0] === "restaurants" && autoreserveId.test(path[1])
        ? path[1] : undefined;
    case "naver_booking":
      // The leading number is Naver's business category, not the business itself.
      return path.length === 4 && lower[0] === "booking" && digits.test(path[1])
        && lower[2] === "bizes" && digits.test(path[3]) ? path[3] : undefined;
    default:
      return undefined;
  }
}

function reservationPlatformUrl(provider: string, value: string | null | undefined) {
  // Inspect the original authority and path before URL can erase an explicit :443,
  // turn backslashes into slashes, trim controls, or collapse dot segments.
  if (typeof value !== "string" || value.length > 2048 || /[\u0000-\u0020\u007f-\u009f\\]/.test(value)
    || /%(?![\da-f]{2})|%(?:2f|5c|2e|25)/i.test(value)) return undefined;
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
  const identity = merchantIdentity(provider, segments, raw[1].toLowerCase());
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
