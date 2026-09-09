"use client";

import { Bell, Bookmark, Compass, Home, MapPinned, MessageCircle, PlusSquare, Route, UserRound, Users } from "lucide-react";
import { useLocale, useTranslations } from "next-intl";
import { Link, usePathname } from "@/i18n/navigation";
import { useSiteVisibility } from "@/components/site-visibility-provider";
import { featureVisible, type SiteFeature } from "@/lib/site-features";
import { useCommunity } from "@/components/community/provider";
import { useDiscoveryStatus } from "@/lib/discovery";
import { getDiscoveryCopy } from "@/lib/discovery-copy";

const items: ReadonlyArray<{
  key: string;
  href: string;
  icon: typeof Compass;
  matches: readonly string[];
  feature?: SiteFeature;
  /** Shown instead of `href` when `feature` is turned off; foods has no switch of its own. */
  fallbackHref?: string;
}> = [
  {
    key: "bottomExplore",
    href: "/hotspots",
    icon: Compass,
    matches: ["/hotspots", "/foods"],
    feature: "hotspots",
    fallbackHref: "/foods",
  },
  {
    key: "bottomPlan",
    href: "/#trip-search",
    icon: MapPinned,
    matches: ["/", "/search", "/trips/new"],
  },
  { key: "bottomTrips", href: "/trips", icon: Route, matches: ["/trips"], feature: "trips" },
  { key: "bottomAlerts", href: "/alerts", icon: Bell, matches: ["/alerts"], feature: "alerts" },
  {
    key: "bottomMy",
    href: "/account",
    icon: UserRound,
    matches: ["/account", "/login", "/register"],
  },
] as const;

export function AppBottomNav() {
  const pathname = usePathname();
  const t = useTranslations("navigation");
  const visibility = useSiteVisibility();
  const community = useCommunity();
  const tc = useTranslations("community");
  const discovery = useDiscoveryStatus();
  const discoveryCopy = getDiscoveryCopy(useLocale());
  const discoveryItems: typeof items = [
    { key: "explore", href: "/explore", icon: Compass, matches: ["/", "/explore", "/hotspots", "/foods", "/destinations"] },
    { key: "collections", href: "/explore/collections", icon: Bookmark, matches: ["/explore/collections", "/community/collections"] },
    { key: "trips", href: "/trips", icon: Route, matches: ["/trips", "/search"], feature: "trips" },
    { key: "my", href: "/my", icon: UserRound, matches: ["/my", "/account", "/login", "/register", "/community/settings"] },
  ];
  const discoveryLabels: Record<string, string> = {
    explore: discoveryCopy.explore, collections: discoveryCopy.collections,
    trips: discoveryCopy.trips, my: discoveryCopy.my,
  };
  const socialItems: typeof items = [
    { key: "home", href: "/", icon: Home, matches: ["/"] },
    { key: "title", href: "/community", icon: Users, matches: ["/community"] },
    ...(community.flags.posting_enabled ? [{ key: "publish", href: "/community/new", icon: PlusSquare, matches: ["/community/new"] }] : []),
    { key: "messages", href: "/community/messages", icon: MessageCircle, matches: ["/community/messages"] },
    { key: "my", href: "/my", icon: UserRound, matches: ["/my", "/account", "/community/settings", "/community/collections", "/community/drafts"] },
  ];
  // The desktop header already honours the admin feature switches; the phone
  // tab bar must not keep advertising a page the site has turned off. Explore
  // survives a paused hotspots page by pointing at foods instead of vanishing.
  const visibleItems = (discovery.enabled ? discoveryItems : community.flags.enabled ? socialItems : items).flatMap((item) => {
    if (!item.feature || featureVisible(visibility, item.feature)) return [item];
    return item.fallbackHref ? [{ ...item, href: item.fallbackHref }] : [];
  });
  const normalizedPath =
    pathname.replace(/^\/(?:en|ja|ko|zh-TW|zh-CN)(?=\/|$)/, "") || "/";
  if (
    normalizedPath.startsWith("/admin") ||
    normalizedPath.startsWith("/share/") ||
    (normalizedPath.startsWith("/trips/") && normalizedPath !== "/trips/new")
  )
    return null;
  return (
    <nav aria-label={t("mobileLabel")} className="app-bottom-nav lg:hidden" style={{ gridTemplateColumns: `repeat(${visibleItems.length}, minmax(0, 1fr))` }}>
      {visibleItems.map((item) => {
        const active = discovery.enabled
          ? item.matches.some((prefix) => prefix === "/" ? normalizedPath === "/" : normalizedPath === prefix || normalizedPath.startsWith(`${prefix}/`)) &&
            !(item.key === "explore" && normalizedPath.startsWith("/explore/collections"))
          : community.flags.enabled
          ? item.key === "title"
            ? normalizedPath.startsWith("/community") && !socialItems.filter((other) => other.key !== "title").some((other) => other.matches.some((prefix) => prefix !== "/" && normalizedPath.startsWith(prefix)))
            : item.matches.some((prefix) => prefix === "/" ? normalizedPath === "/" : normalizedPath.startsWith(prefix))
          :
          item.key === "bottomTrips" && normalizedPath === "/trips/new"
            ? false
            : item.matches.some((prefix) =>
                prefix === "/"
                  ? normalizedPath === "/"
                  : normalizedPath.startsWith(prefix),
              );
        const Icon = item.icon;
        return (
          <Link
            key={item.key}
            href={item.href}
            aria-current={active ? "page" : undefined}
            className={`app-bottom-nav-item ${active ? "app-bottom-nav-item-active" : ""}`}
          >
            <Icon aria-hidden size={20} strokeWidth={active ? 2.5 : 2} />
            <span>{discovery.enabled ? discoveryLabels[item.key] : community.flags.enabled ? tc(item.key) : t(item.key)}{item.key === "messages" && community.unread > 0 ? ` (${community.unread})` : ""}</span>
          </Link>
        );
      })}
    </nav>
  );
}
