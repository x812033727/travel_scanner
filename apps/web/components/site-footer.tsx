"use client";

import { useTranslations } from "next-intl";
import { Link, usePathname } from "@/i18n/navigation";
import { LanguageSwitcher } from "@/components/language-switcher";

// The admin console is not a public page and has its own chrome. The planner runs as a
// full-screen shell that already hides the bottom navigation, and a footer under it would
// push the itinerary off the fold on a phone.
const HIDDEN_ON = ["/admin", "/trips/"];

export function SiteFooter({ year }: { year: number }) {
  const t = useTranslations("navigation");
  const pathname = usePathname();
  if (HIDDEN_ON.some((prefix) => pathname.startsWith(prefix))) return null;

  return (
    <footer aria-label={t("footerLabel")} className="mt-16 border-t border-[var(--line)] bg-[var(--paper)]">
      <div className="mx-auto grid max-w-6xl gap-8 px-5 py-10 sm:grid-cols-2 lg:grid-cols-4">
        <div className="sm:col-span-2 lg:col-span-1">
          <p className="text-lg font-bold">Mokaair</p>
          <p className="mt-2 max-w-sm text-sm leading-6 text-[var(--muted)]">{t("footerTagline")}</p>
        </div>
        <nav aria-label={t("footerLegal")}>
          <h2 className="text-sm font-bold">{t("footerLegal")}</h2>
          <ul className="mt-3 grid gap-2 text-sm">
            <li><Link className="text-[var(--muted)] underline-offset-4 hover:underline" href="/privacy">{t("footerPrivacy")}</Link></li>
            <li><Link className="text-[var(--muted)] underline-offset-4 hover:underline" href="/terms">{t("footerTerms")}</Link></li>
          </ul>
        </nav>
        <nav aria-label={t("footerSite")}>
          <h2 className="text-sm font-bold">{t("footerSite")}</h2>
          <ul className="mt-3 grid gap-2 text-sm">
            <li><Link className="text-[var(--muted)] underline-offset-4 hover:underline" href="/about">{t("footerAbout")}</Link></li>
            <li><Link className="text-[var(--muted)] underline-offset-4 hover:underline" href="/contact">{t("footerContact")}</Link></li>
          </ul>
        </nav>
        <div>
          <h2 className="text-sm font-bold">{t("footerLanguage")}</h2>
          <div className="mt-3"><LanguageSwitcher compact /></div>
        </div>
      </div>
      {/* The bottom navigation is fixed, and .public-app-shell already reserves 5rem plus the
          safe area below its content for it. Sitting inside that shell is what keeps this
          clear of the bar on a phone; it needs no spacing of its own. */}
      <p className="border-t border-[var(--line)] px-5 py-5 text-center text-xs text-[var(--muted)]">
        {t("footerCopyright", { year })}
      </p>
    </footer>
  );
}
