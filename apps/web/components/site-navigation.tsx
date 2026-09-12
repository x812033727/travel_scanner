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
        {/* Outside the three mode branches on purpose. Discovery-on renders only
            frontendDestinations and community-on only its own links, so a link added to
            primaryNavLinks alone vanishes in two of the three modes -- the same defect as
            2026-09-11-no-sign-in-entry-in-discovery. */}
        {!discovery.loading && (discovery.enabled || community.flags.enabled) && (<>
          <Link href="/guides" aria-current={pathname.startsWith("/guides") ? "page" : undefined} className="-mx-2 inline-flex min-h-11 items-center rounded-lg px-2 transition hover:text-[var(--ink)] focus-visible:outline focus-visible:outline-2 focus-visible:outline-[var(--teal)]">{t("guides")}</Link>
          <Link href="/life" aria-current={pathname.startsWith("/life") ? "page" : undefined} className="-mx-2 inline-flex min-h-11 items-center rounded-lg px-2 transition hover:text-[var(--ink)] focus-visible:outline focus-visible:outline-2 focus-visible:outline-[var(--teal)]">{t("life")}</Link>
        </>)}
        {!discovery.enabled && !discovery.loading && <><TextSizeSwitcher />
        <ThemeSwitcher /></>}
        {/* Sign in belongs on every header. Gating it behind !discovery.enabled left the
            live site with no way to sign in or out from the chrome, and made a signed-in
            header identical to a signed-out one. Display preferences can stay in /my;
            knowing whether you are signed in cannot. */}
        {!discovery.loading && <HeaderAuth />}
      </nav>
    </>
  );
}
