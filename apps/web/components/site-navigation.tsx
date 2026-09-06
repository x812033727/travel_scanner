"use client";

import { useTranslations } from "next-intl";
import { HeaderAuth } from "@/components/header-auth";
import { HeaderSessionProvider } from "@/components/header-session";
import { LanguageSwitcher } from "@/components/language-switcher";
import { MobileNav } from "@/components/mobile-nav";
import { ThemeProvider } from "@/components/theme-provider";
import { TextSizeSwitcher } from "@/components/text-size-switcher";
import { ThemeSwitcher } from "@/components/theme-switcher";
import { useSiteVisibility } from "@/components/site-visibility-provider";
import { Link } from "@/i18n/navigation";
import { primaryNavLinks } from "@/lib/nav-links";
import { featureVisible } from "@/lib/site-features";

export function SiteNavigation() {
  const t = useTranslations("navigation");
  const visibility = useSiteVisibility();
  return (
    <ThemeProvider>
      <HeaderSessionProvider>
        <MobileNav />
        <nav aria-label={t("primaryLabel")} className="hidden items-center justify-between gap-5 text-sm text-[var(--muted)] lg:flex">
          {primaryNavLinks.filter((item) => !item.feature || featureVisible(visibility, item.feature)).map((item) => (
            <Link key={item.href} href={item.href} className="-mx-2 inline-flex min-h-11 items-center rounded-lg px-2 transition hover:text-[var(--ink)] focus-visible:outline focus-visible:outline-2 focus-visible:outline-[var(--teal)]">{t(item.key)}</Link>
          ))}
          <TextSizeSwitcher />
          <ThemeSwitcher />
          <LanguageSwitcher compact />
          <HeaderAuth />
        </nav>
      </HeaderSessionProvider>
    </ThemeProvider>
  );
}
