import { Compass } from "lucide-react";
import { SiteNavigation } from "@/components/site-navigation";
import { Link } from "@/i18n/navigation";

export function SiteHeader() {
  return (
    <header className="site-header sticky top-0 z-40 mx-auto flex max-w-7xl flex-wrap items-center justify-between gap-4 px-5 py-3 md:px-8 md:py-4">
      <Link href="/" className="flex items-center gap-3 font-semibold">
        <span className="grid h-10 w-10 place-items-center rounded-2xl bg-[var(--teal)] text-white shadow-sm"><Compass size={21} /></span>
        <span className="hidden sm:inline">Travel Scanner</span>
      </Link>
      <SiteNavigation />
    </header>
  );
}
