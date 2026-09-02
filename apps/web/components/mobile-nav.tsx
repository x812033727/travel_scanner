"use client";

import { CircleUserRound, LogIn } from "lucide-react";
import { LanguageSwitcher } from "@/components/language-switcher";
import { useHeaderSession } from "@/components/header-session";
import { ThemeSwitcher } from "@/components/theme-switcher";
import { Link } from "@/i18n/navigation";

export function MobileNav() {
  const { status } = useHeaderSession();
  return <div className="flex items-center gap-1 md:hidden">
    <ThemeSwitcher />
    <LanguageSwitcher compact />
    <Link href={status === "authenticated" ? "/account" : "/login"} aria-label={status === "authenticated" ? "Account" : "Sign in"} className="grid h-11 w-11 place-items-center rounded-xl text-[var(--teal)] hover:bg-[var(--teal-soft)]">
      {status === "authenticated" ? <CircleUserRound size={21} /> : <LogIn size={21} />}
    </Link>
  </div>;
}
