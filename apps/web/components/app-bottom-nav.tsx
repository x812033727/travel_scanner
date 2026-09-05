"use client";

import { Bell, Compass, MapPinned, Route, UserRound } from "lucide-react";
import { useTranslations } from "next-intl";
import { Link, usePathname } from "@/i18n/navigation";
import { useSiteVisibility } from "@/components/site-visibility-provider";
import { featureVisible, type SiteFeature } from "@/lib/site-features";

const items: ReadonlyArray<{
  key: string;
  href: string;
  icon: typeof Compass;
  matches: readonly string[];
  feature?: SiteFeature;
}> = [
  {
    key: "bottomExplore",
    href: "/hotspots",
    icon: Compass,
    matches: ["/hotspots", "/foods"],
    feature: "hotspots",
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
  // The desktop header already honours the admin feature switches; the phone
  // tab bar must not keep advertising a page the site has turned off.
  const visibleItems = items.filter(
    (item) => !item.feature || featureVisible(visibility, item.feature),
  );
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
        const active =
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
            <span>{t(item.key)}</span>
          </Link>
        );
      })}
    </nav>
  );
}
