import { Compass } from "lucide-react";
import Link from "next/link";

export function SiteHeader() {
  return (
    <header className="mx-auto flex max-w-6xl flex-wrap items-center justify-between gap-4 px-5 py-7 md:px-8">
      <Link href="/" className="flex items-center gap-3 font-semibold">
        <span className="grid h-10 w-10 place-items-center rounded-2xl bg-[var(--teal)] text-white"><Compass size={21} /></span>
        Travel Scanner
      </Link>
      <nav aria-label="主要導覽" className="flex w-full items-center justify-between gap-3 text-sm text-[var(--muted)] sm:w-auto md:gap-5">
        <Link className="hidden md:inline" href="/trips">我的旅程</Link><Link className="hidden lg:inline" href="/alerts">價格通知</Link><Link href="/labs/airlines">航空票價</Link><Link href="/pricing">方案</Link><Link className="rounded-full border border-[var(--line)] bg-white px-4 py-2 text-[var(--ink)]" href="/login">登入</Link>
      </nav>
    </header>
  );
}
