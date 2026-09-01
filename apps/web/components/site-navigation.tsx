"use client";

import { useTranslations } from "next-intl";
import { HeaderAuth } from "@/components/header-auth";
import { HeaderSessionProvider } from "@/components/header-session";
import { LanguageSwitcher } from "@/components/language-switcher";
import { MobileNav } from "@/components/mobile-nav";
import { useSiteVisibility } from "@/components/site-visibility-provider";
import { Link } from "@/i18n/navigation";
import { featureEnabled, type SiteFeature } from "@/lib/site-features";

const desktopLinks: Array<{
  key: "hotspots" | "trips" | "alerts" | "flightStatus" | "airlines" | "pricing";
  href: string;
  feature: SiteFeature;
}> = [
  { key: "hotspots", href: "/hotspots", feature: "hotspots" },
  { key: "trips", href: "/trips", feature: "trips" },
  { key: "alerts", href: "/alerts", feature: "alerts" },
  { key: "flightStatus", href: "/flights/status", feature: "flight_status" },
  { key: "airlines", href: "/labs/airlines", feature: "airline_fares" },
  { key: "pricing", href: "/pricing", feature: "pricing" },
];

export function SiteNavigation() {
  const t = useTranslations("navigation");
  const visibility = useSiteVisibility();
  return (
    <HeaderSessionProvider>
      <MobileNav />
      <nav aria-label={t("primaryLabel")} className="hidden items-center justify-between gap-5 text-sm text-[var(--muted)] md:flex">
        {desktopLinks.filter((item) => featureEnabled(visibility, item.feature)).map((item) => (
          <Link key={item.href} href={item.href}>{t(item.key)}</Link>
        ))}
        <LanguageSwitcher compact />
        <HeaderAuth />
      </nav>
    </HeaderSessionProvider>
  );
}
