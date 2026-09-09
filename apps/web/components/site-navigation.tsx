"use client";

import { useLocale, useTranslations } from "next-intl";
import { HeaderAuth } from "@/components/header-auth";
import { LanguageSwitcher } from "@/components/language-switcher";
import { MobileNav } from "@/components/mobile-nav";
import { ThemeProvider } from "@/components/theme-provider";
import { TextSizeSwitcher } from "@/components/text-size-switcher";
import { ThemeSwitcher } from "@/components/theme-switcher";
import { useSiteVisibility } from "@/components/site-visibility-provider";
import { Link } from "@/i18n/navigation";
import { primaryNavLinks } from "@/lib/nav-links";
import { featureVisible } from "@/lib/site-features";
import { useCommunity } from "@/components/community/provider";
import { useDiscoveryStatus } from "@/lib/discovery";
import { getDiscoveryCopy } from "@/lib/discovery-copy";

export function SiteNavigation() {
  const t = useTranslations("navigation");
  const visibility = useSiteVisibility();
  const community = useCommunity();
  const tc = useTranslations("community");
  const discovery = useDiscoveryStatus();
  const copy = getDiscoveryCopy(useLocale());
  return (
    <ThemeProvider>
      <MobileNav />
      <nav aria-label={t("primaryLabel")} className="hidden items-center justify-between gap-5 text-sm text-[var(--muted)] lg:flex">
        {discovery.enabled ? <>
          <Link href="/explore" className="inline-flex min-h-11 items-center">{copy.explore}</Link>
          <Link href="/explore/collections" className="inline-flex min-h-11 items-center">{copy.collections}</Link>
          {featureVisible(visibility, "trips") && <Link href="/trips" className="inline-flex min-h-11 items-center">{copy.trips}</Link>}
          <Link href="/my" className="inline-flex min-h-11 items-center">{copy.my}</Link>
          {community.flags.enabled && community.flags.posting_enabled && <Link href="/community/new" className="inline-flex min-h-11 items-center">{copy.publish}</Link>}
          {community.flags.enabled && <Link href="/community/messages" className="inline-flex min-h-11 items-center">{copy.notifications}{community.unread > 0 ? ` (${community.unread})` : ""}</Link>}
        </> : community.flags.enabled ? <>
          <Link href="/explore" className="inline-flex min-h-11 items-center">{tc("exploreTravel")}</Link>
          <Link href="/community" className="inline-flex min-h-11 items-center">{tc("title")}</Link>
          <Link href="/pet-friendly" className="inline-flex min-h-11 items-center">{tc("pets")}</Link>
          {featureVisible(visibility, "trips") && <Link href="/trips" className="inline-flex min-h-11 items-center">{tc("myTrips")}</Link>}
          {community.flags.posting_enabled && <Link href="/community/new" className="inline-flex min-h-11 items-center">{tc("publish")}</Link>}
          <Link href="/community/messages" className="inline-flex min-h-11 items-center">{tc("messages")}{community.unread > 0 ? ` (${community.unread})` : ""}</Link>
        </> : primaryNavLinks.filter((item) => !item.feature || featureVisible(visibility, item.feature)).map((item) => (
          <Link key={item.href} href={item.href} className="-mx-2 inline-flex min-h-11 items-center rounded-lg px-2 transition hover:text-[var(--ink)] focus-visible:outline focus-visible:outline-2 focus-visible:outline-[var(--teal)]">{t(item.key)}</Link>
        ))}
        <TextSizeSwitcher />
        <ThemeSwitcher />
        <LanguageSwitcher compact />
        <HeaderAuth />
      </nav>
    </ThemeProvider>
  );
}
