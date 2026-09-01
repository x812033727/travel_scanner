import { Compass } from "lucide-react";
import { SiteNavigation } from "@/components/site-navigation";
import { Link } from "@/i18n/navigation";

export function SiteHeader() {
  return (
    <header className="mx-auto flex max-w-6xl flex-wrap items-center justify-between gap-4 px-5 py-7 md:px-8">
      <Link href="/" className="flex items-center gap-3 font-semibold">
        <span className="grid h-10 w-10 place-items-center rounded-2xl bg-[var(--teal)] text-white"><Compass size={21} /></span>
        Travel Scanner
      </Link>
      <SiteNavigation />
    </header>
  );
}
