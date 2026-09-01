"use client";

import { Luggage, Menu, X } from "lucide-react";
import { useTranslations } from "next-intl";
import { useEffect, useRef, useState } from "react";
import { LanguageSwitcher } from "@/components/language-switcher";
import { Link } from "@/i18n/navigation";

const links = [
  ["home", "/"], ["hotspots", "/hotspots"], ["trips", "/trips"],
  ["alerts", "/alerts"], ["flightStatus", "/flights/status"],
  ["airlines", "/labs/airlines"], ["pricing", "/pricing"], ["account", "/account"],
] as const;

export function MobileNav() {
  const t = useTranslations("navigation");
  const [open, setOpen] = useState(false);
  const closeButton = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    if (!open) return;
    closeButton.current?.focus();
    const closeOnEscape = (event: KeyboardEvent) => {
      if (event.key === "Escape") setOpen(false);
    };
    window.addEventListener("keydown", closeOnEscape);
    return () => window.removeEventListener("keydown", closeOnEscape);
  }, [open]);

  return <div className="flex items-center gap-2 md:hidden">
    <Link href="/trips" className="flex min-h-11 items-center gap-1.5 whitespace-nowrap rounded-xl px-2.5 text-sm font-semibold text-[var(--teal)] hover:bg-[var(--teal-soft)] focus:bg-[var(--teal-soft)]">
      <Luggage aria-hidden size={17} />
      {t("mobileTrips")}
    </Link>
    <button type="button" aria-label={t("openMenu")} aria-expanded={open} aria-controls="mobile-navigation" onClick={() => setOpen(true)} className="rounded-xl border border-[var(--line)] bg-white p-2.5 text-[var(--ink)]"><Menu size={21} /></button>
    {open && <div className="fixed inset-0 z-50 bg-black/30" onMouseDown={() => setOpen(false)}>
      <nav id="mobile-navigation" aria-label={t("mobileLabel")} onMouseDown={(event) => event.stopPropagation()} className="ml-auto flex h-full w-[min(84vw,22rem)] flex-col bg-white p-5 shadow-2xl">
        <div className="mb-5 flex items-center justify-between"><strong>Travel Scanner</strong><button ref={closeButton} type="button" aria-label={t("closeMenu")} onClick={() => setOpen(false)} className="rounded-xl border border-[var(--line)] p-2"><X size={20} /></button></div>
        <div className="mb-4"><LanguageSwitcher /></div>
        <div className="grid gap-2">{links.map(([key, href]) => <Link key={href} href={href} onClick={() => setOpen(false)} className="rounded-xl px-4 py-3 font-semibold text-[var(--ink)] hover:bg-[var(--teal-soft)] focus:bg-[var(--teal-soft)]">{t(key)}</Link>)}</div>
        <Link href="/login" onClick={() => setOpen(false)} className="mt-auto rounded-xl bg-[var(--teal)] px-4 py-3 text-center font-semibold text-white">{t("login")}</Link>
      </nav>
    </div>}
  </div>;
}
