import { MokaairLogo } from "@/components/mokaair-logo";
import { SiteNavigation } from "@/components/site-navigation";
import { LanguageSwitcher } from "@/components/language-switcher";
import { SiteSearch } from "@/components/site-search/site-search";
import { SiteSearchDialog } from "@/components/site-search/site-search-dialog";
import { ThemeSwitcher } from "@/components/theme-switcher";
import { Link } from "@/i18n/navigation";

export function SiteHeader() {
  return (
    <header className="site-header sticky top-0 z-40 w-full">
      <div className="mx-auto flex max-w-7xl flex-wrap items-center justify-between gap-3 px-5 py-2.5 md:gap-4 md:px-8 md:py-3.5">
        <Link href="/" aria-label="Mokaair" className="flex min-h-11 items-center">
          <MokaairLogo className="text-[1.45rem] sm:text-[1.65rem]" />
        </Link>
        <SiteNavigation />
        {/* The article search: a box on a wide screen, and on every width the same box in
            a sheet that ⌘K or the phone header's magnifier opens (SiteSearchDialog). */}
        <SiteSearch variant="inline" className="hidden lg:block" />
        <SiteSearchDialog />
        {/* Always visible, unlike SiteNavigation's own ThemeSwitcher which
            discovery mode drops: without this, dark mode was reachable only
            from the /my card (see #457's comment on discovery-navigation.tsx). */}
        <div className="hidden lg:flex items-center gap-2">
          <ThemeSwitcher />
          <LanguageSwitcher compact />
        </div>
      </div>
    </header>
  );
}
