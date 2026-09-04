"use client";

import { CircleUserRound, LogIn, ShieldCheck } from "lucide-react";
import { useTranslations } from "next-intl";
import { LanguageSwitcher } from "@/components/language-switcher";
import { useHeaderSession } from "@/components/header-session";
import { ThemeSwitcher } from "@/components/theme-switcher";
import { Link } from "@/i18n/navigation";

export function MobileNav() {
  const { status, user } = useHeaderSession();
  const nav = useTranslations("navigation");
  return <div className="flex items-center gap-1 md:hidden">
    <ThemeSwitcher />
    <LanguageSwitcher compact />
    {/* The desktop nav that carries the admin link is hidden below md, and neither the
        bottom bar nor the account page offers one, so without this an administrator on a
        phone can only reach the control centre by typing the URL. */}
    {user?.is_admin && <Link href="/admin" aria-label={nav("admin")} className="grid h-11 w-11 place-items-center rounded-xl text-[var(--teal)] hover:bg-[var(--teal-soft)]">
      <ShieldCheck size={21} />
    </Link>}
    <Link href={status === "authenticated" ? "/account" : "/login"} aria-label={status === "authenticated" ? "Account" : "Sign in"} className="grid h-11 w-11 place-items-center rounded-xl text-[var(--teal)] hover:bg-[var(--teal-soft)]">
      {status === "authenticated" ? <CircleUserRound size={21} /> : <LogIn size={21} />}
    </Link>
  </div>;
}
