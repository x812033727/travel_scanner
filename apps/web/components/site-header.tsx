import { Compass } from "lucide-react";
import Link from "next/link";
import { HeaderAuth } from "@/components/header-auth";
import { MobileNav } from "@/components/mobile-nav";

export function SiteHeader() {
  return (
    <header className="mx-auto flex max-w-6xl flex-wrap items-center justify-between gap-4 px-5 py-7 md:px-8">
      <Link href="/" className="flex items-center gap-3 font-semibold">
        <span className="grid h-10 w-10 place-items-center rounded-2xl bg-[var(--teal)] text-white"><Compass size={21} /></span>
        Travel Scanner
      </Link>
      <MobileNav />
      <nav aria-label="主要導覽" className="hidden items-center justify-between gap-5 text-sm text-[var(--muted)] md:flex">
        <Link href="/hotspots">熱門景點</Link><Link href="/trips">我的旅程</Link><Link href="/alerts">價格通知</Link><Link href="/labs/airlines">航空票價</Link><Link href="/pricing">方案</Link><HeaderAuth />
      </nav>
    </header>
  );
}
