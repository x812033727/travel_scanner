import { Compass } from "lucide-react";
import { useTranslations } from "next-intl";
import { HeaderAuth } from "@/components/header-auth";
import { LanguageSwitcher } from "@/components/language-switcher";
import { MobileNav } from "@/components/mobile-nav";
import { Link } from "@/i18n/navigation";

export function SiteHeader() {
  const t = useTranslations("navigation");
  return (
    <header className="mx-auto flex max-w-6xl flex-wrap items-center justify-between gap-4 px-5 py-7 md:px-8">
      <Link href="/" className="flex items-center gap-3 font-semibold">
        <span className="grid h-10 w-10 place-items-center rounded-2xl bg-[var(--teal)] text-white"><Compass size={21} /></span>
        Travel Scanner
      </Link>
      <MobileNav />
      <nav aria-label={t("primaryLabel")} className="hidden items-center justify-between gap-5 text-sm text-[var(--muted)] md:flex">
        <Link href="/hotspots">{t("hotspots")}</Link><Link href="/trips">{t("trips")}</Link><Link href="/alerts">{t("alerts")}</Link><Link href="/flights/status">{t("flightStatus")}</Link><Link href="/labs/airlines">{t("airlines")}</Link><Link href="/pricing">{t("pricing")}</Link><LanguageSwitcher compact /><HeaderAuth />
      </nav>
    </header>
  );
}
