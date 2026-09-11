"use client";

import { useLocale, useTranslations } from "next-intl";
import { HeaderAuth } from "@/components/header-auth";
import { MobileNav } from "@/components/mobile-nav";
import { TextSizeSwitcher } from "@/components/text-size-switcher";
import { ThemeSwitcher } from "@/components/theme-switcher";
import { useSiteVisibility } from "@/components/site-visibility-provider";
import { Link, usePathname } from "@/i18n/navigation";
import { primaryNavLinks } from "@/lib/nav-links";
import { featureVisible } from "@/lib/site-features";
import { useCommunity } from "@/components/community/provider";
import { useDiscoveryStatus } from "@/lib/discovery";
import { frontendActive, frontendCopy, frontendDestinations } from "@/lib/frontend-navigation";

export function SiteNavigation() {
  const t = useTranslations("navigation");
  const visibility = useSiteVisibility();
  const community = useCommunity();
  const tc = useTranslations("community");
  const discovery = useDiscoveryStatus();
  const copy = frontendCopy(useLocale());
  const pathname = usePathname();
  return (
    <>
      <MobileNav />
      <nav aria-label={t("primaryLabel")} className="hidden items-center justify-between gap-5 text-sm text-[var(--muted)] lg:flex">
        {discovery.loading ? <span aria-hidden className="h-11 w-64 rounded-xl bg-[var(--paper)]" /> : discovery.enabled ? frontendDestinations.filter((item) => !item.feature || featureVisible(visibility, item.feature)).map((item) => <Link key={item.key} href={item.href} aria-current={frontendActive(item.key, pathname) ? "page" : undefined} className="frontend-nav-link inline-flex min-h-11 items-center rounded-xl px-4 font-semibold focus-visible:outline focus-visible:outline-2 focus-visible:outline-[var(--teal)]">{copy[item.key]}</Link>) : community.flags.enabled ? <>
          <Link href="/explore" className="inline-flex min-h-11 items-center">{tc("exploreTravel")}</Link>
          <Link href="/community" className="inline-flex min-h-11 items-center">{tc("title")}</Link>
          <Link href="/pet-friendly" className="inline-flex min-h-11 items-center">{tc("pets")}</Link>
          {featureVisible(visibility, "trips") && <Link href="/trips" className="inline-flex min-h-11 items-center">{tc("myTrips")}</Link>}
          {community.flags.posting_enabled && <Link href="/community/new" className="inline-flex min-h-11 items-center">{tc("publish")}</Link>}
          <Link href="/community/messages" className="inline-flex min-h-11 items-center">{tc("messages")}{community.unread > 0 ? ` (${community.unread})` : ""}</Link>
        </> : primaryNavLinks.filter((item) => !item.feature || featureVisible(visibility, item.feature)).map((item) => (
          <Link key={item.href} href={item.href} className="-mx-2 inline-flex min-h-11 items-center rounded-lg px-2 transition hover:text-[var(--ink)] focus-visible:outline focus-visible:outline-2 focus-visible:outline-[var(--teal)]">{t(item.key)}</Link>
        ))}
        {/* Sign in is not a "legacy mode" control. Discovery used to drop this whole
            group, which left the desktop header with no way to sign in or out at all —
            the one thing lib/nav-links.ts asks every navigation surface to agree on. */}
        {!discovery.loading && <><TextSizeSwitcher />
        <ThemeSwitcher />
        <HeaderAuth /></>}
      </nav>
    </>
  );
}
