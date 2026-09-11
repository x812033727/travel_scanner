"use client";

import { useLocale, useTranslations } from "next-intl";
import { Link, usePathname } from "@/i18n/navigation";
import { destinationsCopy } from "@/lib/destinations-copy";

// The admin console is not a public page and has its own chrome. The planner runs as a
// full-screen shell that already hides the bottom navigation, and a footer under it would
// push the itinerary off the fold on a phone.
const HIDDEN_ON = ["/admin", "/trips/"];

export function SiteFooter({ year }: { year: number }) {
  const t = useTranslations("navigation");
  // Not a navigation.json key: those five files belong to two other tasks, and this label
  // already exists in all five locales next to the destination pages it points at.
  const destinations = destinationsCopy(useLocale()).breadcrumb;
  const pathname = usePathname();
  if (HIDDEN_ON.some((prefix) => pathname.startsWith(prefix))) return null;

  return (
    <footer aria-label={t("footerLabel")} className="mt-16 border-t border-[var(--line)] bg-[var(--paper)]">
      <div className="mx-auto grid max-w-6xl gap-8 px-5 py-10 sm:grid-cols-2 lg:grid-cols-3">
        <div className="sm:col-span-2 lg:col-span-1">
          <p className="text-lg font-bold">Mokaair</p>
          <p className="mt-2 max-w-sm text-sm leading-6 text-[var(--muted)]">{t("footerTagline")}</p>
        </div>
        <nav aria-label={t("footerLegal")}>
          <h2 className="text-sm font-bold">{t("footerLegal")}</h2>
          <ul className="mt-3 grid text-sm">
            <li><Link className="inline-flex min-h-11 items-center text-[var(--muted)] underline-offset-4 hover:underline" href="/privacy">{t("footerPrivacy")}</Link></li>
            <li><Link className="inline-flex min-h-11 items-center text-[var(--muted)] underline-offset-4 hover:underline" href="/terms">{t("footerTerms")}</Link></li>
          </ul>
        </nav>
        <nav aria-label={t("footerSite")}>
          <h2 className="text-sm font-bold">{t("footerSite")}</h2>
          <ul className="mt-3 grid text-sm">
            {/* The only entry point to the 33 city guides that every public page carries. The
                footer is a sibling of {children} in the layout, so unlike the home page rail it
                is in the response body whatever the discovery switch says. */}
            <li><Link className="inline-flex min-h-11 items-center text-[var(--muted)] underline-offset-4 hover:underline" href="/destinations">{destinations}</Link></li>
            {/* Like the destinations link above, this is in the response body of every public
                page whatever the discovery switch says -- the header renders the section only
                once the switch has resolved, so on a first paint this is the only entry. */}
            <li><Link className="inline-flex min-h-11 items-center text-[var(--muted)] underline-offset-4 hover:underline" href="/guides">{t("guides")}</Link></li>
            <li><Link className="inline-flex min-h-11 items-center text-[var(--muted)] underline-offset-4 hover:underline" href="/about">{t("footerAbout")}</Link></li>
            <li><Link className="inline-flex min-h-11 items-center text-[var(--muted)] underline-offset-4 hover:underline" href="/contact">{t("footerContact")}</Link></li>
          </ul>
        </nav>
      </div>
      {/* The bottom navigation is fixed, and .public-app-shell already reserves 5rem plus the
          safe area below its content for it. Sitting inside that shell is what keeps this
          clear of the bar on a phone; it needs no spacing of its own. */}
      {/* text-sm, not text-xs: Tailwind's xs is 12px and readability.spec.ts holds the site
          to a 13px floor, which every route it scans now includes this footer. */}
      <p className="border-t border-[var(--line)] px-5 py-5 text-center text-sm text-[var(--muted)]">
        {t("footerCopyright", { year })}
      </p>
    </footer>
  );
}
