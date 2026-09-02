import { MokaairLogo } from "@/components/mokaair-logo";
import { SiteNavigation } from "@/components/site-navigation";
import { Link } from "@/i18n/navigation";

export function SiteHeader() {
  return (
    <header className="site-header sticky top-0 z-40 mx-auto flex max-w-7xl flex-wrap items-center justify-between gap-4 px-5 py-3 md:px-8 md:py-4">
      <Link href="/" aria-label="Mokaair" className="flex min-h-11 items-center">
        <MokaairLogo className="text-[1.45rem] sm:text-[1.65rem]" />
      </Link>
      <SiteNavigation />
    </header>
  );
}
