"use client";

import { CircleUserRound, LogIn, Menu, ShieldCheck, X } from "lucide-react";
import { useTranslations } from "next-intl";
import { useEffect, useRef, useState } from "react";
import { LanguageSwitcher } from "@/components/language-switcher";
import { useHeaderSession } from "@/components/header-session";
import { TextSizeSwitcher } from "@/components/text-size-switcher";
import { ThemeSwitcher } from "@/components/theme-switcher";
import { useSiteVisibility } from "@/components/site-visibility-provider";
import { Link } from "@/i18n/navigation";
import { primaryNavLinks } from "@/lib/nav-links";
import { featureVisible } from "@/lib/site-features";

export function MobileNav() {
  const { status, user } = useHeaderSession();
  const nav = useTranslations("navigation");
  const visibility = useSiteVisibility();
  const [open, setOpen] = useState(false);
  const closeRef = useRef<HTMLButtonElement>(null);

  // The bottom tab bar carries only five destinations; flight status, airfares
  // and plans used to be unreachable on a phone without typing the URL.
  const links = primaryNavLinks.filter(
    (item) => !item.feature || featureVisible(visibility, item.feature),
  );

  useEffect(() => {
    if (!open) return;
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") setOpen(false);
    };
    document.addEventListener("keydown", onKeyDown);
    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    closeRef.current?.focus();
    return () => {
      document.removeEventListener("keydown", onKeyDown);
      document.body.style.overflow = previousOverflow;
    };
  }, [open]);

  return <div className="flex items-center gap-1 lg:hidden">
    <ThemeSwitcher />
    <LanguageSwitcher compact />
    {/* The desktop nav that carries the admin link is hidden below lg, and neither the
        bottom bar nor the account page offers one, so without this an administrator on a
        phone can only reach the control centre by typing the URL. */}
    {user?.is_admin && <Link href="/admin" aria-label={nav("admin")} className="grid h-11 w-11 place-items-center rounded-xl text-[var(--teal)] hover:bg-[var(--teal-soft)]">
      <ShieldCheck size={21} />
    </Link>}
    <Link href={status === "authenticated" ? "/account" : "/login"} aria-label={status === "authenticated" ? nav("account") : nav("login")} className="grid h-11 w-11 place-items-center rounded-xl text-[var(--teal)] hover:bg-[var(--teal-soft)]">
      {status === "authenticated" ? <CircleUserRound size={21} /> : <LogIn size={21} />}
    </Link>
    <button type="button" aria-label={nav("openMenu")} aria-expanded={open} onClick={() => setOpen(true)} className="grid h-11 w-11 place-items-center rounded-xl text-[var(--teal)] hover:bg-[var(--teal-soft)]">
      <Menu size={21} />
    </button>
    {open && <div role="presentation" className="fixed inset-0 z-[90] bg-slate-950/45 backdrop-blur-sm" onMouseDown={(event) => { if (event.target === event.currentTarget) setOpen(false); }}>
      <div role="dialog" aria-modal="true" aria-label={nav("primaryLabel")} className="absolute inset-x-0 bottom-0 max-h-[85vh] overflow-y-auto rounded-t-[2rem] bg-[var(--surface)] p-5 pb-[calc(1.5rem+env(safe-area-inset-bottom))] shadow-2xl">
        <div className="mb-3 flex items-center justify-between">
          <p className="text-sm font-bold text-[var(--muted)]">{nav("primaryLabel")}</p>
          <button ref={closeRef} type="button" aria-label={nav("closeMenu")} onClick={() => setOpen(false)} className="grid h-11 w-11 place-items-center rounded-full border border-[var(--line)]">
            <X size={18} />
          </button>
        </div>
        <nav aria-label={nav("primaryLabel")} className="grid gap-1">
          {links.map((item) => <Link key={item.href} href={item.href} onClick={() => setOpen(false)} className="flex min-h-12 items-center rounded-xl px-3 font-semibold hover:bg-[var(--teal-soft)]">
            {nav(item.key)}
          </Link>)}
        </nav>
        <div className="mt-5 border-t border-[var(--line)] pt-5">
          <TextSizeSwitcher variant="expanded" />
        </div>
      </div>
    </div>}
  </div>;
}
